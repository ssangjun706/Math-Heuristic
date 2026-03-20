#!/bin/bash

set -e

source .venv/bin/activate

OUTPUT_PATH="./output"
CONFIG_PATH="./config"
TP_SIZE=1
PORT=34437
MAX_WORKERS=16
MODEL="nvidia/nemotron-cascade-8b"

ROLLOUT=4
DATASET="hard"

python request_uri.py \
    --model $MODEL \
    --dataset $DATASET \
    --output-path $OUTPUT_PATH \
    --config-path $CONFIG_PATH \
    --tp-size $TP_SIZE \
    --port $PORT \
    --max-workers $MAX_WORKERS \
    --rollout $ROLLOUT