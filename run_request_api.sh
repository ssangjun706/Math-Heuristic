#!/bin/bash

# set -e

# module load gcc/15.2.0
# module load cuda/12.9.1

source .venv/bin/activate

MODEL="deepseek-ai/DeepSeek-V3.2"
# MODEL="allenai/olmo-3-7b-think-rlvr"
# MODEL="anthropic/claude-sonnet-4.5"
# MODEL="qwen/qwen3-235b-a22b-thinking-2507"

# DATASET="simple"
# DATASET="hard"
DATASET="original"

OUTPUT_PATH="./math-heuristics"
CONFIG_PATH="./config"
MAX_WORKERS=10
ROLLOUT=1

python request_uri.py \
    --model $MODEL \
    --dataset $DATASET \
    --output-path $OUTPUT_PATH \
    --config-path $CONFIG_PATH \
    --max-workers $MAX_WORKERS \
    --rollout $ROLLOUT