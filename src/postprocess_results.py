import json
from pathlib import Path
from collections import defaultdict

from math_verify import parse, verify


def calculate_pass_at_k(problems, k):
    """
    Calculate pass@k metric: percentage of problems where at least one of
    the first k trials is correct.
    """
    passed = 0
    total = 0

    for problem in problems:
        trials = problem.get("trials", [])
        if not trials:
            continue

        total += 1
        # Check if any of the first k trials is correct
        first_k_trials = trials[:k]
        if any(trial.get("is_correct", False) for trial in first_k_trials):
            passed += 1

    return (passed / total * 100) if total > 0 else 0.0


def postprocess_json_file(file_path):
    print(f"Processing: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  Error: Failed to parse JSON file: {e}")
        return
    except Exception as e:
        print(f"  Error reading file: {e}")
        return

    # 파일 구조 확인: metadata가 있으면 problems 추출, 없으면 전체를 data로 사용
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

    # 데이터가 이미 trials 배열을 가지고 있는지 확인
    if data and "trials" in data[0]:
        # 이미 변환된 형식 - 그대로 사용하고 is_correct만 업데이트
        updated_count = 0
        for item in data:
            if "trials" in item and "answer" in item:
                for trial in item["trials"]:
                    if "generated_answer" in trial:
                        old_is_correct = trial.get("is_correct", None)

                        solution_str = trial.get("generated_text", "")
                        ground_truth = parse(
                            f"\\boxed{{{item['answer']}}}", parsing_timeout=None
                        )
                        predicted = parse(solution_str, parsing_timeout=None)
                        new_is_correct = verify(
                            ground_truth, predicted, parsing_timeout=None
                        )

                        trial["is_correct"] = new_is_correct

                        if old_is_correct != new_is_correct:
                            updated_count += 1

        transformed_data = data
    else:
        # 원본 형식 - 변환 필요
        updated_count = 0
        sample_n_added = 0
        for item in data:
            if "answer" in item and "generated_answer" in item:
                old_is_correct = item.get("is_correct", None)

                solution_str = item.get("generated_text", "")
                ground_truth = parse(
                    f"\\boxed{{{item['answer']}}}", parsing_timeout=None
                )
                predicted = parse(solution_str, parsing_timeout=None)
                new_is_correct = verify(ground_truth, predicted, parsing_timeout=None)

                item["is_correct"] = new_is_correct

                if old_is_correct != new_is_correct:
                    updated_count += 1

            if "sample_n" not in item:
                item["sample_n"] = 1
                sample_n_added += 1

        # problem_id로 그룹화
        grouped_data = defaultdict(list)
        for item in data:
            problem_id = item.get("problem_id", 0)
            grouped_data[problem_id].append(item)

        # 새로운 형식으로 변환
        transformed_data = []
        for problem_id in sorted(grouped_data.keys()):
            trials = grouped_data[problem_id]

            # 첫 번째 trial에서 공통 필드 추출
            first_trial = trials[0]

            # 문제 레벨 필드
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

            # 각 trial 정보 추가
            for trial in trials:
                trial_entry = {
                    "n": trial.get("sample_n", 1),
                    "reasoning": trial.get("reasoning", ""),
                    "generated_text": trial.get("generated_text", ""),
                    "generated_answer": trial.get("generated_answer", ""),
                    "is_correct": trial.get("is_correct", False),
                }
                problem_entry["trials"].append(trial_entry)

            # trial을 n으로 정렬
            problem_entry["trials"].sort(key=lambda x: x["n"])

            transformed_data.append(problem_entry)

    # 정답률 계산
    total_trials = sum(len(item["trials"]) for item in transformed_data)
    correct_trials = sum(
        sum(1 for trial in item["trials"] if trial["is_correct"])
        for item in transformed_data
    )
    accuracy = (correct_trials / total_trials * 100) if total_trials > 0 else 0.0

    # pass@k 계산
    num_problems = len(transformed_data)
    pass_at_1 = calculate_pass_at_k(transformed_data, 1)

    # 통계 정보는 출력만 하고 파일에는 저장하지 않음
    # JSON 파일로 쓰기 (메타데이터 없이 problems 배열만 저장)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(transformed_data, f, ensure_ascii=False, indent=2)

        print(
            f"  ✓ Processed {num_problems} problems, {total_trials} trials, "
            f"updated {updated_count} is_correct values"
        )
        print(f"  ✓ Accuracy: {correct_trials}/{total_trials} = {accuracy:.2f}%")
        print(f"  ✓ Pass@1: {pass_at_1:.2f}%")
        print(f"  ✓ Updated: {file_path}")
    except Exception as e:
        print(f"  Error writing file: {e}")


def process_all_output_files():
    """output/ 폴더의 모든 json 파일 후처리"""
    output_dir = Path("../output")

    if not output_dir.exists():
        print(f"Error: output directory not found: {output_dir}")
        return

    # output/ 하위의 모든 json 파일 찾기
    json_files = list(output_dir.rglob("*.json"))

    if not json_files:
        print("No json files found in output/ directory")
        return

    print(f"Found {len(json_files)} json files\n")

    # 각 파일 처리
    for file_path in sorted(json_files):
        postprocess_json_file(file_path)
        print()

    print("=" * 60)
    print("All files processed successfully!")


if __name__ == "__main__":
    process_all_output_files()
