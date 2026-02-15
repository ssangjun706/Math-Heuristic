#!/usr/bin/env python3
"""
Check the number of JSON objects in each result file.
Each file should contain 115 objects with trials arrays.
"""
import json
from pathlib import Path


def analyze_json_file(file_path):
    """Analyze JSON file for object count, trials information, and accuracy metrics."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, list):
                return None, None, None, None, None, None

            object_count = len(data)
            total_trials = 0
            objects_without_trials = []

            # Accuracy metrics
            total_correct_trials = 0
            pass_at_1_count = 0  # First trial correct
            pass_at_k_count = 0  # At least one trial correct

            for obj in data:
                if isinstance(obj, dict):
                    if "trials" in obj and isinstance(obj["trials"], list):
                        trials = obj["trials"]
                        trial_count = len(trials)
                        total_trials += trial_count

                        if trial_count == 0:
                            problem_id = obj.get("problem_id", "unknown")
                            objects_without_trials.append(problem_id)
                        else:
                            # Count correct trials
                            correct_trials = [
                                t for t in trials if t.get("is_correct", False)
                            ]
                            total_correct_trials += len(correct_trials)

                            # pass@1: first trial is correct
                            if trials[0].get("is_correct", False):
                                pass_at_1_count += 1

                            # pass@k: at least one trial is correct
                            if len(correct_trials) > 0:
                                pass_at_k_count += 1
                    else:
                        problem_id = obj.get("problem_id", "unknown")
                        objects_without_trials.append(problem_id)

            # Calculate metrics
            overall_accuracy = (
                (total_correct_trials / total_trials * 100) if total_trials > 0 else 0
            )
            pass_at_1 = (
                (pass_at_1_count / object_count * 100) if object_count > 0 else 0
            )
            pass_at_k = (
                (pass_at_k_count / object_count * 100) if object_count > 0 else 0
            )

            return (
                object_count,
                total_trials,
                objects_without_trials,
                overall_accuracy,
                pass_at_1,
                pass_at_k,
            )

    except Exception as e:
        print(f"  ❌ Error reading {file_path.name}: {e}")
        return None, None, None, None, None, None


def main():
    base_dir = Path("math-heuristics")
    # base_dir = Path("output")
    folders = ["simple", "hard", "original"]
    expected_count = 115

    print("=" * 130)
    print("JSON Object Count, Trials & Accuracy Verification")
    print("=" * 130)
    print(f"Expected object count per file: {expected_count}")
    print(f"Metrics: Acc = Overall accuracy | P@1 = Pass@1 | P@k = Pass@k")
    print()

    total_files = 0
    files_with_issues = []
    files_with_missing_trials = []

    for folder in folders:
        folder_path = base_dir / folder
        if not folder_path.exists():
            print(f"⚠️  Folder not found: {folder}")
            continue

        json_files = sorted(folder_path.glob("*.json"))

        if not json_files:
            print(f"📁 {folder.upper()}: No JSON files found")
            print()
            continue

        print(f"\n📁 {folder.upper()}")
        print("─" * 130)

        # Table header
        print(
            f"{'Model':<50} {'Status':<8} {'Problems':<10} {'Trials':<8} {'Acc %':<8} {'P@1 %':<8} {'P@k %':<8}"
        )
        print("─" * 130)

        for json_file in json_files:
            result = analyze_json_file(json_file)
            total_files += 1

            if result[0] is None:
                continue

            (
                object_count,
                total_trials,
                objects_without_trials,
                overall_accuracy,
                pass_at_1,
                pass_at_k,
            ) = result

            status = "✅" if object_count == expected_count else "❌"

            # Extract model name from filename (remove _math_perturb_*_result.json)
            model_name = json_file.stem.replace(f"_math_perturb_{folder}_result", "")

            # Status with warning if trials missing
            status_str = status
            if objects_without_trials:
                status_str += f" ⚠️"

            print(
                f"{model_name:<50} {status_str:<8} {object_count:<10} "
                f"{total_trials:<8} {overall_accuracy:>6.1f}% {pass_at_1:>6.1f}% {pass_at_k:>6.1f}%"
            )

            if object_count != expected_count:
                files_with_issues.append((folder, model_name, object_count))

            if objects_without_trials:
                files_with_missing_trials.append(
                    (folder, model_name, objects_without_trials)
                )

    # Summary
    print("\n" + "=" * 130)
    print("SUMMARY")
    print("=" * 130)
    print(f"Total files checked: {total_files}")
    print(
        f"Files with correct object count ({expected_count}): {total_files - len(files_with_issues)}"
    )
    print(f"Files with object count issues: {len(files_with_issues)}")
    print(f"Files with missing trials: {len(files_with_missing_trials)}")

    if files_with_issues:
        print()
        print("⚠️  FILES WITH INCORRECT OBJECT COUNT:")
        for folder, model_name, count in files_with_issues:
            diff = count - expected_count
            diff_str = f"({diff:+d})" if diff != 0 else ""
            print(f"  - {folder}/{model_name}: {count} objects {diff_str}")

    if files_with_missing_trials:
        print()
        print("⚠️  FILES WITH MISSING TRIALS:")
        for folder, model_name, problem_ids in files_with_missing_trials:
            print(
                f"  - {folder}/{model_name}: {len(problem_ids)} problems without trials"
            )
            if len(problem_ids) <= 5:
                print(f"    Problem IDs: {problem_ids}")
            else:
                print(
                    f"    Problem IDs: {problem_ids[:5]} ... (and {len(problem_ids) - 5} more)"
                )

    if not files_with_issues and not files_with_missing_trials:
        print()
        print("🎉 All files have the correct object count and trials!")

    print("=" * 130)


if __name__ == "__main__":
    main()
