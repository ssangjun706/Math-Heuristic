import argparse
import json
import os
from pathlib import Path

import requests
import yaml
from dotenv import load_dotenv
from tqdm import tqdm

from evaluation.answer_extraction import extract_answer
from evaluation.eval_script import is_correct
from src.format_prompt import PromptFormatter


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
    """Load already processed problem_ids from output file."""
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--config-path", required=True)
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    dataset_path = Path(args.dataset)
    output_dir = Path(args.output_path)

    config_dir = Path(args.config_path)
    model_name_escaped = args.model.split("/")[-1].lower()
    config_path = config_dir / f"{model_name_escaped}.yaml"

    model_config = load_yaml(config_path)
    model_name = model_config["model_name"]
    model_parameter = model_config.get("parameter", {})

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
    formatter = PromptFormatter(args.model)

    for item in tqdm(problems_to_process):
        problem = item.get("problem", "")
        messages = formatter.format_prompt(problem)

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
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
                "final_prompt": None,
            }

            with output_path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(result, ensure_ascii=False) + "\n")

        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\nError processing query {item.get('problem_id')}: {e}")
            continue


if __name__ == "__main__":
    main()
