import json
from pathlib import Path
from collections import defaultdict

from math_verify import parse, verify


def postprocess_json_file(file_path):
    print(f"Processing: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            if file_path.suffix == ".jsonl":
                lines = f.readlines()
                file_content = [
                    json.loads(line.strip()) for line in lines if line.strip()
                ]
            else:
                file_content = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  Error: Failed to parse JSON/JSONL file: {e}")
        return
    except Exception as e:
        print(f"  Error reading file: {e}")
        return

    if isinstance(file_content, dict) and "problems" in file_content:
        data = file_content["problems"]
    elif isinstance(file_content, list):
        data = file_content
    else:
        print(f"  Warning: Unexpected file structure in {file_path}")
        return

    if not data:
        print(f"  Warning: No valid data found in {file_path}")
        return

    if data and "trials" in data[0]:
        updated_count = 0
        for item in data:
            if "trials" in item and "answer" in item:
                for trial in item["trials"]:
                    if "generated_answer" in trial:
                        old_is_correct = trial.get("is_correct", None)

                        solution_str = trial.get("generated_text", "")
                        ground_truth = parse(f"\\boxed{{{item['answer']}}}")
                        predicted = parse(solution_str)
                        new_is_correct = verify(ground_truth, predicted)

                        trial["is_correct"] = new_is_correct

                        if old_is_correct != new_is_correct:
                            updated_count += 1

        transformed_data = data
    else:
        updated_count = 0
        sample_n_added = 0
        for item in data:
            if "answer" in item and "generated_answer" in item:
                old_is_correct = item.get("is_correct", None)

                solution_str = item.get("generated_text", "")
                ground_truth = parse(f"\\boxed{{{item['answer']}}}")
                predicted = parse(solution_str)
                new_is_correct = verify(ground_truth, predicted)

                item["is_correct"] = new_is_correct

                if old_is_correct != new_is_correct:
                    updated_count += 1

            if "sample_n" not in item:
                item["sample_n"] = 1
                sample_n_added += 1

        grouped_data = defaultdict(list)
        for item in data:
            problem_id = item.get("problem_id", 0)
            grouped_data[problem_id].append(item)

        transformed_data = []
        for problem_id in sorted(grouped_data.keys()):
            trials = grouped_data[problem_id]

            first_trial = trials[0]

            problem_entry = {
                "problem_id": problem_id,
                "problem": first_trial.get("problem", ""),
                "answer": first_trial.get("answer", ""),
                "level": first_trial.get("level", ""),
                "type": first_trial.get("type", ""),
                "original_split": first_trial.get("original_split", ""),
                "final_prompt": first_trial.get("final_prompt", ""),
                "trials": [],
            }

            for trial in trials:
                trial_entry = {
                    "n": trial.get("sample_n", 1),
                    "reasoning": trial.get("reasoning", ""),
                    "generated_text": trial.get("generated_text", ""),
                    "generated_answer": trial.get("generated_answer", ""),
                    "is_correct": trial.get("is_correct", False),
                }
                problem_entry["trials"].append(trial_entry)

            problem_entry["trials"].sort(key=lambda x: x["n"])
            transformed_data.append(problem_entry)

    total_trials = sum(len(item["trials"]) for item in transformed_data)
    num_problems = len(transformed_data)
    output_path = (
        file_path.with_suffix(".json") if file_path.suffix == ".jsonl" else file_path
    )
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transformed_data, f, ensure_ascii=False, indent=2)

        print(
            f"  ✓ Processed {num_problems} problems, {total_trials} trials, "
            f"updated {updated_count} is_correct values"
        )
        print(f"  ✓ Updated: {output_path}")
    except Exception as e:
        print(f"  Error writing file: {e}")


def process_all_output_files():
    output_dir = Path("./output")

    if not output_dir.exists():
        print(f"Error: output directory not found: {output_dir}")
        return

    json_files = list(output_dir.rglob("*.json")) + list(output_dir.rglob("*.jsonl"))

    if not json_files:
        print("No json/jsonl files found in output/ directory")
        return

    print(f"Found {len(json_files)} json/jsonl files\n")

    for file_path in sorted(json_files):
        postprocess_json_file(file_path)
        print()

    print("=" * 60)
    print("All files processed successfully!")


if __name__ == "__main__":
    process_all_output_files()
