import argparse
import json
from pathlib import Path


def extract_json_array_text(raw_text: str) -> str | None:
    """Extract JSON array text, preferring the `problems` array if present."""
    problems_key = '"problems"'
    key_idx = raw_text.find(problems_key)

    search_start = 0 if key_idx < 0 else key_idx + len(problems_key)
    array_start = raw_text.find("[", search_start)
    if array_start < 0:
        return None

    in_string = False
    escaped = False
    depth = 0

    for idx in range(array_start, len(raw_text)):
        ch = raw_text[idx]

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue

        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return raw_text[array_start : idx + 1]

    return raw_text[array_start:]


def recover_problem_objects(raw_text: str) -> list[dict]:
    """Recover valid dict objects from possibly malformed JSON array text."""
    array_text = extract_json_array_text(raw_text)
    if not array_text:
        return []

    body = array_text[1:] if array_text.startswith("[") else array_text

    decoder = json.JSONDecoder()
    idx = 0
    recovered: list[dict] = []

    while idx < len(body):
        while idx < len(body) and body[idx] in " \t\r\n,":
            idx += 1

        if idx >= len(body) or body[idx] == "]":
            break

        try:
            obj, next_idx = decoder.raw_decode(body, idx)
        except json.JSONDecodeError:
            break

        idx = next_idx
        if isinstance(obj, dict) and "problem_id" in obj:
            recovered.append(obj)

    return recovered


def repair_json_file(input_path: Path, output_path: Path, wrap_key: str) -> tuple[int, int]:
    raw_text = input_path.read_text(encoding="utf-8")

    total_detected = raw_text.count('"problem_id"')
    recovered = recover_problem_objects(raw_text)

    if wrap_key == "problems":
        payload: dict | list = {"problems": recovered}
    else:
        payload = recovered

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return len(recovered), total_detected


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Repair malformed result JSON by recovering valid problem objects."
    )
    parser.add_argument("--input", required=True, help="Path to broken JSON file")
    parser.add_argument(
        "--output",
        default=None,
        help="Path to output JSON file (default: overwrite input)",
    )
    parser.add_argument(
        "--wrap",
        choices=["problems", "list"],
        default="problems",
        help="Output format: {'problems': [...]} or plain list",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path

    recovered_count, total_detected = repair_json_file(
        input_path=input_path,
        output_path=output_path,
        wrap_key=args.wrap,
    )

    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Recovered objects: {recovered_count}")
    print(f"Detected 'problem_id' tokens in raw file: {total_detected}")

    if recovered_count == 0:
        print("Warning: no recoverable objects found.")


if __name__ == "__main__":
    main()
