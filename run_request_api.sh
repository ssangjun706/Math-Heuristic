#!/bin/bash

# set -e

# module load gcc/15.2.0
# module load cuda/12.9.1

source .venv/bin/activate

# MODEL="deepseek-ai/DeepSeek-V3.2"
# MODEL="anthropic/claude-sonnet-4.5"
MODEL="qwen/qwen3-235b-a22b-thinking-2507"
# MODEL="qwen/qwen3-235b-a22b-instruct-2507"
# MODEL="qwen/qwen3-30b-a3b-thinking-2507"
# MODEL="qwen/qwen3-30b-a3b-instruct-2507"
# MODEL="allenai/olmo-3-7b-think-rlvr"

DATASET="simple"
# DATASET="hard"
# DATASET="original"

OUTPUT_PATH="./output"
CONFIG_PATH="./config"
MAX_WORKERS=20
ROLLOUT=1

python request_uri.py \
    --model $MODEL \
    --dataset $DATASET \
    --output-path $OUTPUT_PATH \
    --config-path $CONFIG_PATH \
    --max-workers $MAX_WORKERS \
    --rollout $ROLLOUT