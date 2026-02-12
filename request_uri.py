import re
import argparse
import json
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

import requests
import yaml
from dotenv import load_dotenv
from tqdm import tqdm

from evaluation.answer_extraction import extract_answer
from evaluation.eval_script import is_correct
from src.format_prompt import PromptFormatter
from src.vllm_serve import setup_local_vllm


def load_jsonl(path: Path) -> list[dict]:
    items: list[dict] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_processed_ids(output_path: Path) -> set[str]:
    if not output_path.exists():
        return set()

    processed_ids: set[str] = set()
    with output_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if "problem_id" in data:
                    processed_ids.add(data["problem_id"])
            except json.JSONDecodeError:
                continue
    return processed_ids


def extract_reasoning_from_content(content: str) -> tuple[str | None, str]:
    think_pattern = r"<think>(.*?)</think>"
    think_matches = re.findall(think_pattern, content, re.DOTALL)

    if think_matches:
        reasoning = "\n".join(think_matches)
        clean_content = re.sub(think_pattern, "", content, flags=re.DOTALL).strip()
        return reasoning, clean_content

    fallback_think_pattern = "</think>"
    blocks = content.split(fallback_think_pattern)

    if len(blocks) != 2:
        return None, content

    reasoning = blocks[0].strip()
    clean_content = blocks[-1].strip()
    
    return reasoning, clean_content


def process_single_problem(
    item: dict,
    formatter: PromptFormatter,
    api_base_url: str,
    model_name: str,
    model_parameter: dict,
    api_key: str | None,
    output_path: Path,
    write_lock: Lock,
) -> dict | None:
    try:
        problem = item.get("problem", "")
        messages = formatter.format_prompt(problem)

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        response = requests.post(
            url=api_base_url,
            headers=headers,
            data=json.dumps(
                {
                    "model": model_name,
                    "messages": messages,
                    **model_parameter,
                }
            ),
        )

        if response.status_code != 200:
            raise RuntimeError(f"{response.status_code}: {response.text}")

        completion = response.json()
        message = completion["choices"][0]["message"]
        generated_text = message.get("content", "")
        reasoning = message.get("reasoning", None)
        generated_answer = extract_answer(generated_text)

        if reasoning is None and generated_text:
            extracted_reasoning, clean_content = extract_reasoning_from_content(
                generated_text
            )
            if extracted_reasoning:
                reasoning = extracted_reasoning
                generated_text = clean_content

        is_correct_value = is_correct(
            {
                "prediction": generated_answer,
                "answer": str(item.get("answer")),
            }
        )

        result = {
            "problem_id": item.get("problem_id"),
            "problem": problem,
            "answer": item.get("answer"),
            "level": item.get("level"),
            "type": item.get("type"),
            "original_split": item.get("original_split"),
            "reasoning": reasoning,
            "generated_text": generated_text,
            "generated_answer": generated_answer,
            "is_correct": is_correct_value,
            "final_prompt": str(messages),
        }

        with write_lock:
            with output_path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(result, ensure_ascii=False) + "\n")

        return result

    except Exception as e:
        print(f"\nError processing query {item.get('problem_id')}: {e}")
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output-path", type=str, required=True)
    parser.add_argument("--config-path", type=str, required=True)
    parser.add_argument("--tp-size", type=int, default=1)
    parser.add_argument("--port", type=int, default=65001)
    parser.add_argument("--max-workers", type=int, default=1)
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    dataset_path = Path(args.dataset)
    output_dir = Path(args.output_path)

    config_dir = Path(args.config_path)
    model_name_escaped = args.model.split("/")[-1].lower()
    config_path = config_dir / f"{model_name_escaped}.yaml"

    model_config = load_yaml(config_path)
    model_name = model_config["model_name"]
    model_parameter = model_config.get("parameter", {})

    is_local = model_config.get("local", False)
    has_chat_template = model_config.get("has_chat_template", True)

    if is_local:
        endpoint = "chat/completions" if has_chat_template else "completions"
        api_base_url = model_config.get(
            "api_base_url", f"http://localhost:{args.port}/v1/{endpoint}"
        )

        auto_start = model_config.get("auto_start", True)
        if auto_start:
            setup_local_vllm(
                model_name=model_name,
                api_base_url=api_base_url,
                vllm_args={
                    "tensor-parallel-size": args.tp_size,
                },
            )
    else:
        api_base_url = model_config.get(
            "api_base_url", "https://openrouter.ai/api/v1/chat/completions"
        )

    dataset_name = dataset_path.name.split(".jsonl")[0].lower()
    output_path = output_dir / f"{model_name_escaped}_{dataset_name}_result.jsonl"
    problems = load_jsonl(dataset_path)

    processed_ids = load_processed_ids(output_path)

    problems_to_process = [
        p for p in problems if p.get("problem_id") not in processed_ids
    ]
    print(f"Model: {model_name}")
    print(f"Dataset: {dataset_name}")
    print(f"Output: {output_path}")
    print(f"Found {len(processed_ids)} already processed problems. Skipping them.")
    print(f"Processing {len(problems_to_process)} problems / {len(problems)} total.")
    print(f"Using {args.max_workers} parallel workers.")

    formatter = PromptFormatter(args.model)
    write_lock = Lock()

    # Process problems in parallel
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        # Submit all tasks
        future_to_item = {
            executor.submit(
                process_single_problem,
                item,
                formatter,
                api_base_url,
                model_name,
                model_parameter,
                api_key,
                output_path,
                write_lock,
            ): item
            for item in problems_to_process
        }

        try:
            with tqdm(total=len(problems_to_process)) as pbar:
                for future in as_completed(future_to_item):
                    result = future.result()
                    pbar.update(1)
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting...")
            executor.shutdown(wait=False, cancel_futures=True)
            return

    print("Sorting results by problem_id...")
    if output_path.exists():
        results = load_jsonl(output_path)
        results.sort(key=lambda x: x.get("problem_id", ""))

        with output_path.open("w", encoding="utf-8") as file:
            for result in results:
                file.write(json.dumps(result, ensure_ascii=False) + "\n")
        print(f"Results sorted and saved to {output_path}")


if __name__ == "__main__":
    main()
