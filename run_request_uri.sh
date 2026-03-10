#!/bin/bash

set -e

source .venv/bin/activate

MODEL="allenai/olmo-3-7b-rl-zero"
DATASET="hard"
OUTPUT_PATH="./output"
CONFIG_PATH="./config"
TP_SIZE=1
PORT=35002
MAX_WORKERS=8
ROLLOUT=1

python request_uri.py \
    --model $MODEL \
    --dataset $DATASET \
    --output-path $OUTPUT_PATH \
    --config-path $CONFIG_PATH \
    --tp-size $TP_SIZE \
    --port $PORT \
    --max-workers $MAX_WORKERS \
    --rollout $ROLLOUT
