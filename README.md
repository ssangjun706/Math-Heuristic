# Math-Tag

## Repository Layout

```text
├── request_uri.py                 # 메인 실행 스크립트
├── run_request_api.sh             # API 모델 실행 예시
├── run_request_uri.sh             # 로컬 모델 실행 예시
├── install.sh                     # UV 기반 초기 설치 스크립트
├── config/*.yaml                  # 모델별 설정 파일
└── dataset/
    ├── raw/                       # 원본 데이터
    ├── train/                     # train split
    └── test/                      # test split
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

## Output Format

기본 출력 경로:
- `output/{dataset}/{model_name}_math_perturb_{dataset}_result.json`


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
