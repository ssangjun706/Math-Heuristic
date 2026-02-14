#!/usr/bin/env python3
"""
Check the number of JSON objects in each result file.
Each file should contain 115 objects with trials arrays.
"""
import json
from pathlib import Path


def analyze_json_file(file_path):
    """Analyze JSON file for object count and trials information."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, list):
                return None, None, None

            object_count = len(data)
            total_trials = 0
            objects_without_trials = []

            for obj in data:
                if isinstance(obj, dict):
                    if "trials" in obj and isinstance(obj["trials"], list):
                        trial_count = len(obj["trials"])
                        total_trials += trial_count
                        if trial_count == 0:
                            problem_id = obj.get("problem_id", "unknown")
                            objects_without_trials.append(problem_id)
                    else:
                        problem_id = obj.get("problem_id", "unknown")
                        objects_without_trials.append(problem_id)

            return object_count, total_trials, objects_without_trials

    except Exception as e:
        print(f"  ❌ Error reading {file_path.name}: {e}")
        return None, None, None


def main():
    base_dir = Path("math-heuristics")
    folders = ["simple", "hard", "original"]
    expected_count = 115

    print("=" * 80)
    print("JSON Object Count & Trials Verification")
    print("=" * 80)
    print(f"Expected object count per file: {expected_count}")
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

        print(f"📁 {folder.upper()}:")
        print("-" * 80)

        for json_file in json_files:
            object_count, total_trials, objects_without_trials = analyze_json_file(
                json_file
            )
            total_files += 1

            if object_count is None:
                continue

            status = "✅" if object_count == expected_count else "❌"
            filename = json_file.name

            trials_info = f"({total_trials} trials)"
            if objects_without_trials:
                trials_info += f" ⚠️ {len(objects_without_trials)} without trials"

            print(f"  {status} {filename:<60} {object_count:>4} objects {trials_info}")

            if object_count != expected_count:
                files_with_issues.append((folder, filename, object_count))

            if objects_without_trials:
                files_with_missing_trials.append(
                    (folder, filename, objects_without_trials)
                )

        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files checked: {total_files}")
    print(
        f"Files with correct object count ({expected_count}): {total_files - len(files_with_issues)}"
    )
    print(f"Files with object count issues: {len(files_with_issues)}")
    print(f"Files with missing trials: {len(files_with_missing_trials)}")

    if files_with_issues:
        print()
        print("⚠️  FILES WITH INCORRECT OBJECT COUNT:")
        for folder, filename, count in files_with_issues:
            diff = count - expected_count
            diff_str = f"({diff:+d})" if diff != 0 else ""
            print(f"  - {folder}/{filename}: {count} objects {diff_str}")

    if files_with_missing_trials:
        print()
        print("⚠️  FILES WITH MISSING TRIALS:")
        for folder, filename, problem_ids in files_with_missing_trials:
            print(
                f"  - {folder}/{filename}: {len(problem_ids)} problems without trials"
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

    print("=" * 80)


if __name__ == "__main__":
    main()
