#!/usr/bin/env python3
"""
Compute pass@k for each result file using the unbiased estimator.

  pass@k = 1 - C(n-c, k) / C(n, k)

where n = N (trials used per problem), c = correct trials, k = K option.

Usage:
  python check_pass_at_k.py [--N <int>] [--K <int>]

Options:
  --N   Number of trials per problem to use (default: 64).
        Problems with fewer than N trials are excluded from metrics.
        If a problem has MORE than N trials, only the first N are used.
  --K   k value for pass@k (default: same as N). Must satisfy 1 <= K <= N.
"""
import argparse
import json
import math
from pathlib import Path


# ---------------------------------------------------------------------------
# Core math
# ---------------------------------------------------------------------------


def pass_at_k_unbiased(n: int, c: int, k: int) -> float:
    """
    Unbiased pass@k estimator.

    pass@k = 1 - C(n-c, k) / C(n, k)

    Special cases:
      - k > n  → 0.0  (not enough samples to estimate)
      - c >= n → 1.0  (all samples correct)
    """
    if k > n:
        return 0.0
    if c >= n:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


# ---------------------------------------------------------------------------
# Per-file analysis
# ---------------------------------------------------------------------------


def analyze_json_file(file_path, n_trials: int, k: int):
    """
    Analyze a single result JSON file.

    Each problem's trials list is capped to the first `n_trials` entries.
    Problems with fewer than `n_trials` trials are excluded from all metrics.

    Returns:
        (
            object_count,               # total objects in file
            valid_count,                # problems with >= n_trials trials
            total_trials_used,          # valid_count * n_trials
            insufficient_trial_ids,     # problem_ids with < n_trials trials
            avg_correct_rate,           # total correct / total trials used * 100
            pass_at_1,                  # fraction of valid problems where trial[0] is correct (%)
            pass_at_k,                  # mean per-problem pass@k over valid problems (%)
        )
        or (None, ...) on error.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return (None,) * 7

        object_count = len(data)
        valid_count = 0
        total_trials_used = 0
        total_correct = 0
        pass_at_1_count = 0
        pass_at_k_sum = 0.0
        insufficient_trial_ids = []

        for obj in data:
            if not isinstance(obj, dict):
                continue

            problem_id = obj.get("problem_id", "unknown")
            trials_all = obj.get("trials")

            if not isinstance(trials_all, list) or len(trials_all) < n_trials:
                insufficient_trial_ids.append(problem_id)
                continue

            # Cap to first n_trials
            trials = trials_all[:n_trials]
            valid_count += 1
            total_trials_used += n_trials

            correct = [t for t in trials if t.get("is_correct", False)]
            c = len(correct)
            total_correct += c

            if trials[0].get("is_correct", False):
                pass_at_1_count += 1

            pass_at_k_sum += pass_at_k_unbiased(n_trials, c, k)

        avg_correct_rate = (
            (total_correct / total_trials_used * 100) if total_trials_used > 0 else 0.0
        )
        pass_at_1 = (pass_at_1_count / valid_count * 100) if valid_count > 0 else 0.0
        pass_at_k = (pass_at_k_sum / valid_count * 100) if valid_count > 0 else 0.0

        return (
            object_count,
            valid_count,
            total_trials_used,
            insufficient_trial_ids,
            avg_correct_rate,
            pass_at_1,
            pass_at_k,
        )

    except Exception as e:
        print(f"  ❌ Error reading {file_path.name}: {e}")
        return (None,) * 7


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Compute pass@k for JSON result files using the unbiased estimator."
    )
    parser.add_argument(
        "--N",
        type=int,
        default=64,
        dest="n_trials",
        metavar="N",
        help="Number of trials per problem to use (default: 64). "
        "Problems with fewer trials are excluded; extras are ignored.",
    )
    parser.add_argument(
        "--K",
        type=int,
        default=None,
        dest="k",
        metavar="K",
        help="k value for pass@k (default: same as N). Must satisfy 1 <= K <= N.",
    )
    args = parser.parse_args()

    n_trials: int = args.n_trials
    k: int = args.k if args.k is not None else n_trials

    if n_trials < 1:
        parser.error("N must be >= 1.")
    if k < 1:
        parser.error("K must be >= 1.")
    if k > n_trials:
        parser.error(f"K ({k}) must be <= N ({n_trials}).")

    base_dir = Path("math-heuristics")
    # base_dir = Path("output")
    folders = ["simple", "hard", "original"]
    # folders = ["simple"]
    expected_count = 115

    W = 145
    print("=" * W)
    print(f"Pass@k Evaluation  —  unbiased estimator")
    print("=" * W)
    print(f"Expected problems per file : {expected_count}")
    print(f"N (trials per problem used): {n_trials}")
    print(f"K (for pass@k)            : {k}")
    print(
        f"Metrics: AvgCorr = correct trials / total trials used | "
        f"P@1 = Pass@1 | P@{k} = Pass@{k} (unbiased)"
    )
    print()

    total_files = 0
    files_with_issues = []
    files_with_insufficient = []

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
        header = (
            f"{'Model':<50} {'Status':<8} {'Total':<7} {'Valid':<7} "
            f"{'TrialsUsed':<12} {'AvgCorr':>8} {'P@1':>7} {f'P@{k}':>9}"
        )
        print(header)
        print("─" * W)

        for json_file in json_files:
            result = analyze_json_file(json_file, n_trials, k)
            total_files += 1

            if result[0] is None:
                continue

            (
                object_count,
                valid_count,
                total_trials_used,
                insufficient_trial_ids,
                avg_correct_rate,
                pass_at_1,
                pass_at_k,
            ) = result

            model_name = json_file.stem.replace(f"_math_perturb_{folder}_result", "")
            status = "✅" if valid_count == expected_count else "❌"
            status_str = status + (" ⚠️" if insufficient_trial_ids else "")

            print(
                f"{model_name:<50} {status_str:<8} {object_count:<7} {valid_count:<7} "
                f"{total_trials_used:<12} {avg_correct_rate:>7.2f}% {pass_at_1:>6.2f}% "
                f"{pass_at_k:>8.2f}%"
            )

            if valid_count != expected_count:
                files_with_issues.append(
                    (folder, model_name, object_count, valid_count)
                )
            if insufficient_trial_ids:
                files_with_insufficient.append(
                    (folder, model_name, insufficient_trial_ids)
                )

    # Summary
    print("\n" + "=" * W)
    print("SUMMARY")
    print("=" * W)
    print(f"Total files checked                          : {total_files}")
    print(
        f"Files with correct valid count ({expected_count})    : "
        f"{total_files - len(files_with_issues)}"
    )
    print(f"Files with valid count issues                : {len(files_with_issues)}")
    print(
        f"Files with problems having < {n_trials} trial(s)   : {len(files_with_insufficient)}"
    )

    if files_with_issues:
        print()
        print("⚠️  FILES WITH INCORRECT VALID PROBLEM COUNT:")
        for folder, model_name, total_obj, valid in files_with_issues:
            diff = valid - expected_count
            print(
                f"  - {folder}/{model_name}: {valid} valid / {total_obj} total ({diff:+d})"
            )

    if files_with_insufficient:
        print()
        print(f"⚠️  FILES WITH PROBLEMS HAVING < {n_trials} TRIAL(S):")
        for folder, model_name, problem_ids in files_with_insufficient:
            print(
                f"  - {folder}/{model_name}: {len(problem_ids)} problems with insufficient trials"
            )
            shown = problem_ids[:5]
            rest = len(problem_ids) - len(shown)
            suffix = f" ... (and {rest} more)" if rest > 0 else ""
            print(f"    Problem IDs: {shown}{suffix}")

    if not files_with_issues and not files_with_insufficient:
        print()
        print("🎉 All files have the correct problem count and sufficient trials!")

    print("=" * W)


if __name__ == "__main__":
    main()
