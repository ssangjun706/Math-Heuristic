import json
from pathlib import Path


def convert_json_to_jsonl(input_file, output_file=None):
    """
    Convert JSON file with trials structure to JSONL format.
    Each trial becomes a separate line in the JSONL file.

    Args:
        input_file: Path to input JSON file
        output_file: Path to output JSONL file (optional, defaults to output/human/ directory)
    """
    input_path = Path(input_file)

    if output_file is None:
        # Default: change output/{type}/ to output/human/
        parts = input_path.parts
        if "output" in parts:
            output_idx = parts.index("output")
            # Replace the type directory (next after "output") with "human"
            new_parts = (
                list(parts[: output_idx + 1])
                + ["human"]
                + list(parts[output_idx + 2 :])
            )
            output_file = Path(*new_parts).with_suffix(".jsonl")
        else:
            # Fallback: just change extension
            output_file = input_path.with_suffix(".jsonl")
    else:
        output_file = Path(output_file)

    print(f"Converting: {input_path} -> {output_file}")

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"  Error reading file: {e}")
        return

    # Handle both list and dict with "problems" key
    if isinstance(data, dict) and "problems" in data:
        problems = data["problems"]
    elif isinstance(data, list):
        problems = data
    else:
        print(f"  Error: Unexpected data structure")
        return

    # Convert to JSONL format
    jsonl_lines = []
    total_trials = 0

    for problem in problems:
        # Common fields from problem level
        problem_fields = {
            "problem_id": problem.get("problem_id", 0),
            "problem": problem.get("problem", ""),
            "answer": problem.get("answer", ""),
            "level": problem.get("level", ""),
            "type": problem.get("type", ""),
            "original_split": problem.get("original_split", ""),
            "final_prompt": problem.get("final_prompt", ""),
        }

        # Get trials
        trials = problem.get("trials", [])

        if not trials:
            # If no trials, check if trial fields exist at problem level
            if "generated_text" in problem or "generated_answer" in problem:
                line = {
                    **problem_fields,
                    "reasoning": problem.get("reasoning", ""),
                    "generated_text": problem.get("generated_text", ""),
                    "generated_answer": problem.get("generated_answer", ""),
                    "is_correct": problem.get("is_correct", False),
                }
                jsonl_lines.append(line)
                total_trials += 1
        else:
            # Create one JSONL line per trial
            for trial in trials:
                line = {
                    **problem_fields,
                    "reasoning": trial.get("reasoning", ""),
                    "generated_text": trial.get("generated_text", ""),
                    "generated_answer": trial.get("generated_answer", ""),
                    "is_correct": trial.get("is_correct", False),
                }
                jsonl_lines.append(line)
                total_trials += 1

    # Write JSONL file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for line in jsonl_lines:
                f.write(json.dumps(line, ensure_ascii=False) + "\n")

        print(f"  ✓ Converted {len(problems)} problems -> {total_trials} JSONL lines")
        print(f"  ✓ Output: {output_file}")
    except Exception as e:
        print(f"  Error writing file: {e}")


def convert_all_json_files(input_dir="output", output_dir=None):
    """
    Convert all JSON files in a directory to JSONL format.

    Args:
        input_dir: Directory containing JSON files to convert
        output_dir: Output directory for JSONL files (optional, defaults to output/human)
    """
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Error: Input directory not found: {input_path}")
        return

    if output_dir is None:
        # Default: use output/human directory
        output_path = Path("output") / "human"
    else:
        output_path = Path(output_dir)

    output_path.mkdir(parents=True, exist_ok=True)

    # Allowed model names
    allowed_models = [
        "claude-sonnet-4.5",
        "deepseek-v3.2",
        "qwen3-235b-a22b-instruct-2507",
        "qwen3-235b-a22b-thinking-2507",
        "qwen3-30b-a3b-instruct-2507",
        "qwen3-30b-a3b-thinking-2507",
    ]

    # Find all JSON files
    all_json_files = list(input_path.rglob("*.json"))

    # Filter by allowed models
    json_files = []
    for json_file in all_json_files:
        filename = json_file.name.lower()
        # Check if any allowed model name is in the filename
        if any(model in filename for model in allowed_models):
            json_files.append(json_file)

    if not json_files:
        print(f"No JSON files found matching allowed models")
        print(f"Allowed models: {', '.join(allowed_models)}")
        return

    print(f"Found {len(json_files)} JSON files matching allowed models\n")

    for json_file in sorted(json_files):
        # Get just the filename (without directory structure)
        output_file = output_path / json_file.name.replace(".json", ".jsonl")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        convert_json_to_jsonl(json_file, output_file)
        print()

    print("=" * 60)
    print("All files converted successfully!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Single file conversion
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_json_to_jsonl(input_file, output_file)
    else:
        # Batch conversion
        convert_all_json_files("output")
