# Math-Tag

MATH-Perturb 데이터셋(`simple`, `hard`)에 대해 다양한 LLM 응답을 수집하고, 평가를 수행하는 프로젝트입니다.


## Repository Layout

```text
.
├── request_uri.py                 # 메인 실행 스크립트
├── run_request_api.sh             # API 모델 실행 예시
├── run_request_uri.sh             # 로컬 모델 실행 예시
├── install.sh                     # UV 기반 초기 설치 스크립트
├── config/*.yaml                  # 모델별 설정 파일
├── dataset/
│   ├── raw/                       # 원본 데이터
│   ├── train/                     # train split
│   └── test/                      # test split
├── output/{original,simple,hard}/ # 모델별 결과 저장
└── src/
		├── check_accuracy.py
		└── check_pass_at_k.py
```

## Setup

### 1) Install

```bash
bash install.sh
source .venv/bin/activate
```

### 2) API Key

API 모델(OpenRouter 경유) 실행 시 `.env`에 아래 키를 설정하세요.

```bash
OPENROUTER_API_KEY=your_key_here
```

## Quick Start

### API 모델 실행

```bash
bash run_request_api.sh
```

### 로컬(vLLM) 모델 실행

```bash
bash run_request_uri.sh
```

두 스크립트 모두 내부에서 `request_uri.py`를 호출합니다.

## Main CLI (`request_uri.py`)

```bash
python request_uri.py \
	--model allenai/olmo-3-7b-rl-zero \
	--dataset hard \
	--output-path ./output \
	--config-path ./config \
	--tp-size 1 \
	--port 35002 \
	--max-workers 8 \
	--rollout 1
```

### Arguments

- `--model`: 모델 식별자. config 파일명 매핑에 사용
- `--dataset`: `original | simple | hard`
- `--output-path`: 결과 루트 디렉터리
- `--config-path`: YAML 설정 폴더
- `--tp-size`: 로컬 vLLM tensor parallel 크기
- `--port`: 로컬 vLLM 포트
- `--max-workers`: 동시 요청 스레드 수
- `--rollout`: 문제당 trial 개수
- `--prompt-tag`: 프롬프트 실험 태그(default: `default`). 커스텀 실험 결과 파일명 분리에 사용
- `--custom-instruction-file`: 사용자 지시문 텍스트 파일 경로(optional)
- `--custom-system-prompt-file`: 시스템 프롬프트 텍스트 파일 경로(optional)
- `--instruction-mode`: `append | replace` (default: `append`)
	- `append`: 기본 지시문 + 커스텀 지시문
	- `replace`: 기본 지시문 대신 커스텀 지시문 사용

## Model Config (`config/*.yaml`)

예시:

```yaml
model_name: allenai/Olmo-3-7B-RL-Zero-Math
local: true
parameter:
	max_tokens: 16384
	top_p: 0.95
	top_k: 50
```

주요 필드:
- `model_name`: 실제 요청에 사용할 모델명
- `local`: `true`면 로컬 vLLM 경로 사용
- `parameter`: API payload에 그대로 병합될 파라미터
- `has_chat_template`(optional): `chat/completions` vs `completions` 분기
- `api_base_url`(optional): 엔드포인트 직접 지정
- `auto_start`(optional): 로컬 vLLM 자동 기동 여부
- `vllm_args`(optional): vLLM 실행 추가 인자

## Output Format

기본 출력 경로:
- `output/{dataset}/{model_name}_math_perturb_{dataset}_result.json`

커스텀 프롬프트 실험 시(또는 `--prompt-tag`가 default가 아닐 때):
- `output/{dataset}/{model_name}_math_perturb_{dataset}_prompt-{prompt_tag}_result.json`

예시:
- `output/hard/olmo-3-7b_math_perturb_hard_prompt-cot-v2_result.json`

파일 구조(요약):

```json
[
	{
		"problem_id": "...",
		"problem": "...",
		"answer": "...",
		"trials": [
			{
				"n": 1,
				"reasoning": "...",
				"generated_text": "...",
				"generated_answer": "...",
				"is_correct": true,
				"generated_tokens": 123
			}
		]
	}
]
```

추적을 위해 각 problem object에 다음 메타데이터가 추가됩니다.
- `prompt_tag`
- `instruction_mode`
- `custom_instruction_file`
- `custom_system_prompt_file`


## Rollout Progress

### API

| Type  | Model                         | Original | Simple | Hard |
|-------|------------------------------ |----------|--------|------|
| API   | Claude-Sonnet-4.5             | ✓        | ✗      | ✓    |
| API   | DeepSeek-V3.2                 | ✓        | ✓      | ✓    |
| API   | Qwen3-235B-A22B-Instruct-2507 | ✓        | ✓      | ✓    |
| API   | Qwen3-235B-A22B-Thinking-2507 | ✓        | ✓      | ✓    |
| API   | Qwen3-30B-A3B-Instruct-2507   | ✓        | ✓      | ✓    |
| API   | Qwen3-30B-A3B-Thinking-2507   | ✓        | ✓      | ✓    |
| API   | Qwen3-8B (Thinking)           | ✓        | ✓      | ✓    |

### Local

| Type  | Model                   | Original | Simple | Hard |
|-------|-------------------------|----------|--------|------|
| Local | OLMo-3-7B-Base          | ✓        | ✓      | ✓    |
| Local | OLMo-3-7B-Think-DPO     | ✓        | ✓      | ✓    |
| Local | OLMo-3-7B-Think-SFT     | ✓        | ✓      | ✓    |
| Local | OLMo-3-7B-Think-RLVR    | ✓        | ✓      | ✓    |
| Local | OLMo-3-RL-Zero          | ✓        | ✓      | ✓    |
| Local | Nemotron-Cascade-8B     | ✓        | ✓      | ✓    |
| Local | Nemotron-Cascade-8B-SFT | ✓        | ✓      | ✓    |
| Local | Qwen3-8B-Base           | ✓        | ✓      | ✓    |


### Rollout (N=64)

| Type  | Model                   | Original | Simple | Hard |
|-------|-------------------------|----------|--------|------|
| Local | OLMo-3-7B-Base          | ✓        | x      | ✓    | 
| Local | Nemotron-Cascade-8B-SFT | ✓        | ✓      | ✓    | ✓
| Local | Nemotron-Cascade-8B     | ✓        | ✓      | ✓    | ✓
| Local | OLMo-3-7B-Think-RLVR    | ✓        | ✓      | ✓    | ✓
| Local | OLMo-3-RL-Zero          | ✓        | ✓      | ✓    | ✓
| Local | Qwen3-8B-Base           | ✓        | ✓      | ✓    | ✓
| Local | Qwen3-1.7B-Base         | ✓        | ✓      | ✓    | ✓
