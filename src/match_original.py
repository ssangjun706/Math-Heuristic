import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from evaluation.answer_extraction import extract_answer


Key = Tuple[str, str]


def iter_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                raise SystemExit(f"Invalid JSON in {path} at line {line_num}: {e}")


def build_raw_index(raw_path: Path) -> Dict[Key, List[dict]]:
    index: Dict[Key, List[dict]] = {}
    for obj in iter_jsonl(raw_path):
        key = (obj.get("level"), obj.get("type"))
        index.setdefault(key, []).append(obj)
    return index


def common_prefix_len(a: str, b: str) -> int:
    max_len = min(len(a), len(b))
    i = 0
    while i < max_len and a[i] == b[i]:
        i += 1
    return i


def select_top_candidates(
    candidates: List[dict],
    query_problem: str,
    top_k: int,
    min_prefix_ratio: float,
    min_prefix_len: int,
) -> List[dict]:
    if not candidates:
        return []

    scored: List[tuple[int, dict]] = []
    for cand in candidates:
        cand_problem = cand.get("problem") or ""
        score = common_prefix_len(query_problem, cand_problem)
        scored.append((score, cand))

    scored.sort(key=lambda x: x[0], reverse=True)
    query_len = max(1, len(query_problem))

    filtered: List[dict] = []
    for score, cand in scored:
        ratio = score / query_len
        if score >= min_prefix_len and ratio >= min_prefix_ratio:
            filtered.append(cand)
        if len(filtered) >= top_k:
            break

    if filtered:
        return filtered
    return [scored[0][1]]


def merge_original_with_extra(
    original: dict,
    perturb: dict,
    key_order: List[str],
    match_meta: Dict[str, object],
) -> dict:
    merged: Dict[str, object] = {}

    parsed_answer = extract_answer(original.get("solution", ""))

    for key in key_order:
        if key == "answer":
            merged[key] = parsed_answer
            continue
        if key in original:
            merged[key] = original[key]
            continue
        if key in perturb:
            merged[key] = perturb[key]

    for key, value in match_meta.items():
        if key not in merged:
            merged[key] = value

    for key, value in original.items():
        if key not in merged:
            merged[key] = value
    return merged


def get_perturb_key_order(split_dir: Path, sources: List[str]) -> List[str]:
    for name in sources:
        src = split_dir / name
        if not src.exists():
            continue
        for obj in iter_jsonl(src):
            return list(obj.keys())
    return ["problem_id", "problem", "answer", "level", "type", "original_split"]


def process_split(
    split_dir: Path,
    raw_index: Dict[Key, List[dict]],
    sources: List[str],
    top_k: int,
    min_prefix_ratio: float,
    min_prefix_len: int,
) -> None:
    output_path = split_dir / "math_perturb_original.jsonl"
    key_order = get_perturb_key_order(split_dir, sources)

    total = 0
    matched_queries = 0
    missing = 0
    written = 0
    skipped_dup = 0
    per_source = {name: {"total": 0, "matched": 0, "missing": 0} for name in sources}
    seen_ids = set()

    with output_path.open("w", encoding="utf-8") as f_out:
        for name in sources:
            src = split_dir / name
            if not src.exists():
                continue
            for obj in iter_jsonl(src):
                total += 1
                per_source[name]["total"] += 1

                dedup_id = obj.get("problem_id")
                if dedup_id is not None:
                    if dedup_id in seen_ids:
                        skipped_dup += 1
                        continue
                    seen_ids.add(dedup_id)

                key = (obj.get("level"), obj.get("type"))
                candidates = raw_index.get(key)
                selected = select_top_candidates(
                    candidates or [],
                    obj.get("problem") or "",
                    top_k,
                    min_prefix_ratio,
                    min_prefix_len,
                )
                if not selected:
                    missing += 1
                    per_source[name]["missing"] += 1
                    continue
                matched_queries += 1
                per_source[name]["matched"] += 1

                for rank, cand in enumerate(selected, 1):
                    score = common_prefix_len(
                        obj.get("problem") or "", cand.get("problem") or ""
                    )
                    ratio = score / max(1, len(obj.get("problem") or ""))
                    match_meta = {
                        "match_rank": rank,
                        "match_score": score,
                        "match_ratio": round(ratio, 6),
                    }
                    merged = merge_original_with_extra(cand, obj, key_order, match_meta)
                    f_out.write(json.dumps(merged, ensure_ascii=False) + "\n")
                    written += 1

    print(
        f"{split_dir.name}: matched={matched_queries} / total={total}"
        f" (missing={missing}, written={written})"
    )
    if skipped_dup:
        print(f"  - skipped duplicates: {skipped_dup}")
    for name in sources:
        counts = per_source[name]
        if counts["total"] == 0:
            continue
        print(
            f"  - {name}: matched={counts['matched']} / total={counts['total']}"
            f" (missing={counts['missing']})"
        )
    print(f"  output: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Match perturb data to raw MATH dataset and create math_perturb_original.jsonl"
    )
    parser.add_argument(
        "--raw",
        default="dataset/raw/hendrycks_math.jsonl",
        help="Path to raw MATH jsonl",
    )
    parser.add_argument(
        "--dataset",
        default="dataset",
        help="Dataset root containing train/test folders",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Maximum number of high-similarity matches to include per problem",
    )
    parser.add_argument(
        "--min-prefix-ratio",
        type=float,
        default=0.3,
        help="Minimum common-prefix ratio (0-1) to include a candidate",
    )
    parser.add_argument(
        "--min-prefix-len",
        type=int,
        default=20,
        help="Minimum common-prefix length to include a candidate",
    )
    args = parser.parse_args()

    raw_path = Path(args.raw)
    dataset_root = Path(args.dataset)

    if not raw_path.exists():
        raise SystemExit(f"Raw file not found: {raw_path}")

    raw_index = build_raw_index(raw_path)

    sources = ["math_perturb_simple.jsonl", "math_perturb_hard.jsonl"]
    for split_name in ["train", "test"]:
        split_dir = dataset_root / split_name
        if not split_dir.exists():
            print(f"Skip missing split dir: {split_dir}")
            continue
        process_split(
            split_dir,
            raw_index,
            sources,
            args.top_k,
            args.min_prefix_ratio,
            args.min_prefix_len,
        )


if __name__ == "__main__":
    main()
