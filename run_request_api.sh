#!/bin/bash

set -e
source .venv/bin/activate

MODEL="qwen/qwen3-235b-a22b-thinking-2507"
DATASET="hard"
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