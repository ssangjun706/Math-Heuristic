import re
import argparse
import json
import logging
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

import requests
import yaml
from dotenv import load_dotenv
from tqdm import tqdm

from math_verify import parse, verify

from src.format_prompt import PromptFormatter
from src.vllm_serve import setup_local_vllm


class NoWarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.WARNING


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

for handler in logging.root.handlers:
    handler.addFilter(NoWarningFilter())

logger = logging.getLogger(__name__)


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


def load_existing_results(output_path: Path) -> dict[str, dict]:
    if not output_path.exists():
        return {}

    results: dict[str, dict] = {}
    try:
        with output_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict) and "problems" in data:
            problems = data["problems"]
        elif isinstance(data, list):
            problems = data
        else:
            return {}

        for problem in problems:
            if "problem_id" in problem:
                results[problem["problem_id"]] = problem

    except (json.JSONDecodeError, FileNotFoundError):
        pass

    return results


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


def process_single_trial(
    item: dict,
    trial_n: int,
    formatter: PromptFormatter,
    api_base_url: str,
    model_name: str,
    model_parameter: dict,
    api_key: str | None,
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
        answer = item.get("answer", "")
        generated_text = message.get("content", "")
        reasoning = message.get("reasoning", None)

        try:
            parsed_answer = parse(f"\\boxed{{{answer}}}", parsing_timeout=None)
            parsed_generated = parse(generated_text, parsing_timeout=None)
        except:
            raise RuntimeError("Parsing error due to timeout or invalid format.")

        generated_answer = str(parsed_generated) if parsed_generated else ""

        if reasoning is None and generated_text:
            extracted_reasoning, clean_content = extract_reasoning_from_content(
                generated_text
            )
            if extracted_reasoning:
                reasoning = extracted_reasoning
                generated_text = clean_content

        is_correct_value = verify(
            parsed_answer,
            parsed_generated,
            timeout_seconds=None,
        )

        trial = {
            "n": trial_n,
            "reasoning": reasoning,
            "generated_text": generated_text,
            "generated_answer": generated_answer,
            "is_correct": is_correct_value,
        }

        return trial

    except Exception as e:
        logging.error(
            f"Error processing trial {trial_n} for {item.get('problem_id')}: {e}"
        )
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--output-path", type=str, required=True)
    parser.add_argument("--config-path", type=str, required=True)
    parser.add_argument("--tp-size", type=int, default=1)
    parser.add_argument("--port", type=int, default=65001)
    parser.add_argument("--max-workers", type=int, default=1)
    parser.add_argument("--rollout", type=int, default=1)
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
    output_path = output_dir / f"{model_name_escaped}_{dataset_name}_result.json"
    problems = load_jsonl(dataset_path)

    existing_results = load_existing_results(output_path)

    results_dict: dict[str, dict] = {}
    for problem in problems:
        problem_id = problem.get("problem_id")
        if problem_id in existing_results:
            results_dict[problem_id] = existing_results[problem_id]
        else:
            formatter = PromptFormatter(args.model)
            messages = formatter.format_prompt(problem.get("problem", ""))
            results_dict[problem_id] = {
                "problem_id": problem_id,
                "problem": problem.get("problem", ""),
                "answer": problem.get("answer"),
                "level": problem.get("level"),
                "type": problem.get("type"),
                "original_split": problem.get("original_split"),
                "final_prompt": str(messages),
                "trials": [],
            }

    trials_to_process = []
    for problem in problems:
        problem_id = problem.get("problem_id")
        current_trial_count = len(results_dict[problem_id].get("trials", []))

        for trial_n in range(current_trial_count, args.rollout):
            trials_to_process.append((problem, trial_n))

    total_trials = len(problems) * args.rollout
    completed_trials = total_trials - len(trials_to_process)

    logger = logging.getLogger(__name__)
    logger.info(f"Model: {model_name}")
    logger.info(f"Dataset: {dataset_name}")
    logger.info(f"Output: {output_path}")
    logger.info(f"Rollout: {args.rollout}")
    logger.info(f"Total problems: {len(problems)}")
    logger.info(f"Completed trials: {completed_trials} / {total_trials}")
    logger.info(f"Remaining trials: {len(trials_to_process)}")
    logger.info(f"Using {args.max_workers} parallel workers.")

    formatter = PromptFormatter(args.model)
    results_lock = Lock()

    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        future_to_trial = {
            executor.submit(
                process_single_trial,
                problem,
                trial_n,
                formatter,
                api_base_url,
                model_name,
                model_parameter,
                api_key,
            ): (problem, trial_n)
            for problem, trial_n in trials_to_process
        }

        try:
            with tqdm(total=len(trials_to_process), desc="Processing trials") as pbar:
                for future in as_completed(future_to_trial):
                    problem, trial_n = future_to_trial[future]
                    problem_id = problem.get("problem_id")

                    trial_result = future.result()
                    if trial_result:
                        with results_lock:
                            results_dict[problem_id]["trials"].append(trial_result)

                            sorted_results = sorted(
                                results_dict.values(),
                                key=lambda x: x.get("problem_id", ""),
                            )

                            for result in sorted_results:
                                result["trials"] = sorted(
                                    result["trials"], key=lambda t: t.get("n", 0)
                                )

                            with output_path.open("w", encoding="utf-8") as file:
                                json.dump(
                                    sorted_results, file, ensure_ascii=False, indent=2
                                )

                    pbar.update(1)
        except KeyboardInterrupt:
            logger.info("Interrupted by user, saving progress...")
            executor.shutdown(wait=False, cancel_futures=True)
            sorted_results = sorted(
                results_dict.values(), key=lambda x: x.get("problem_id", "")
            )

            for result in sorted_results:
                result["trials"] = sorted(result["trials"], key=lambda t: t.get("n", 0))

            with output_path.open("w", encoding="utf-8") as file:
                json.dump(sorted_results, file, ensure_ascii=False, indent=2)

            logger.info(f"Progress saved to {output_path}")
            return

    logger.info(f"All trials completed. Results saved to {output_path}")


if __name__ == "__main__":
    main()
