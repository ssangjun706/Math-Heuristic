#!/usr/bin/env python3
"""
Check per-file accuracy assuming N=K=1.
Each problem must have at least 1 trial; the first trial's `is_correct` field
is used to determine correctness.

Usage:
  python check_accuracy.py
"""
import json
import re
from pathlib import Path


def analyze_json_file(file_path):
    """
    For each problem in the file, read only the FIRST trial and check correctness.

    Returns:
        (
            object_count,           # total objects in file
            valid_count,            # problems that have >= 1 trial
            problems_no_trial,      # list of problem_ids with no trials
            accuracy,               # correct / valid_count * 100
        )
        or (None, None, None, None) on error.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return None, None, None, None

        object_count = len(data)
        valid_count = 0
        correct_count = 0
        problems_no_trial = []

        for obj in data:
            if not isinstance(obj, dict):
                continue

            problem_id = obj.get("problem_id", "unknown")
            trials = obj.get("trials")

            if not isinstance(trials, list) or len(trials) == 0:
                problems_no_trial.append(problem_id)
                continue

            valid_count += 1
            if trials[0].get("is_correct", False):
                correct_count += 1

        accuracy = (correct_count / valid_count * 100) if valid_count > 0 else 0.0

        return object_count, valid_count, problems_no_trial, accuracy

    except Exception as e:
        print(f"  ❌ Error reading {file_path.name}: {e}")
        return None, None, None, None


def parse_model_and_prompt_tag(file_path: Path, folder: str) -> tuple[str, str]:
    stem = file_path.stem
    pattern = (
        rf"^(?P<model>.+?)_math_perturb_{re.escape(folder)}"
        rf"(?:_prompt-(?P<prompt>.+))?_result$"
    )
    match = re.match(pattern, stem)
    if not match:
        model_name = stem.replace(f"_math_perturb_{folder}_result", "")
        return model_name, "default"

    model_name = match.group("model")
    prompt_tag = match.group("prompt") or "default"
    return model_name, prompt_tag


def main():
    # base_dir = Path("math-heuristics")
    base_dir = Path("output")
    folders = ["simple", "hard", "original"]
    expected_count = 115

    W = 120
    print("=" * W)
    print("Accuracy Check (N=K=1)  —  first trial per problem")
    print("=" * W)
    print(f"Expected problems per file: {expected_count}")
    print(f"Metric: Accuracy = (# problems where first trial is correct) / valid_count")
    print()

    total_files = 0
    files_with_issues = []
    files_with_no_trial = []

    for folder in folders:
        folder_path = base_dir / folder
        if not folder_path.exists():
            print(f"⚠️  Folder not found: {folder}")
            continue

        json_files = sorted(folder_path.glob("*.json"))
        if not json_files:
            print(f"📁 {folder.upper()}: No JSON files found\n")
            continue

        print(f"\n📁 {folder.upper()}")
        print("─" * W)
        print(
            f"{'Model':<42} {'PromptTag':<20} {'Status':<8} {'Total':<8} {'Valid':<8} {'Accuracy':>9}"
        )
        print("─" * W)

        for json_file in json_files:
            result = analyze_json_file(json_file)
            total_files += 1

            if result[0] is None:
                continue

            object_count, valid_count, problems_no_trial, accuracy = result
            model_name, prompt_tag = parse_model_and_prompt_tag(json_file, folder)

            status = "✅" if valid_count == expected_count else "❌"
            status_str = status + (" ⚠️" if problems_no_trial else "")

            print(
                f"{model_name:<42} {prompt_tag:<20} {status_str:<8} {object_count:<8} {valid_count:<8} "
                f"{accuracy:>8.2f}%"
            )

            if valid_count != expected_count:
                files_with_issues.append(
                    (folder, model_name, prompt_tag, object_count, valid_count)
                )
            if problems_no_trial:
                files_with_no_trial.append(
                    (folder, model_name, prompt_tag, problems_no_trial)
                )

    # Summary
    print("\n" + "=" * W)
    print("SUMMARY")
    print("=" * W)
    print(f"Total files checked                       : {total_files}")
    print(
        f"Files with correct problem count ({expected_count}): "
        f"{total_files - len(files_with_issues)}"
    )
    print(f"Files with problem count issues            : {len(files_with_issues)}")
    print(f"Files with problems missing trials         : {len(files_with_no_trial)}")

    if files_with_issues:
        print()
        print("⚠️  FILES WITH INCORRECT VALID PROBLEM COUNT:")
        for folder, model_name, prompt_tag, total_obj, valid in files_with_issues:
            diff = valid - expected_count
            print(
                f"  - {folder}/{model_name} [prompt={prompt_tag}]: {valid} valid / {total_obj} total ({diff:+d})"
            )

    if files_with_no_trial:
        print()
        print("⚠️  FILES WITH PROBLEMS MISSING ALL TRIALS:")
        for folder, model_name, prompt_tag, problem_ids in files_with_no_trial:
            print(
                f"  - {folder}/{model_name} [prompt={prompt_tag}]: {len(problem_ids)} problems without any trial"
            )
            shown = problem_ids[:5]
            rest = len(problem_ids) - len(shown)
            suffix = f" ... (and {rest} more)" if rest > 0 else ""
            print(f"    Problem IDs: {shown}{suffix}")

    if not files_with_issues and not files_with_no_trial:
        print()
        print("🎉 All files have the correct problem count and trials!")

    print("=" * W)


if __name__ == "__main__":
    main()
