#!/bin/bash

set -e

export CUDA_VISIBLE_DEVICES="3"
export HF_HOME="/data2/sangjunsong/.cache/hf_hub"
export HF_HUB_CACHE="/data2/sangjunsong/.cache/hf_hub"
export TRANSFORMERS_CACHE="/data2/sangjunsong/.cache/transformers"
export HF_TOKEN="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"

source .venv/bin/activate

MODEL="nvidia/Nemotron-Cascade-8B"
DATASET="simple"
OUTPUT_PATH="./output"
CONFIG_PATH="./config"
TP_SIZE=1
PORT=35002
MAX_WORKERS=8

for ROLLOUT in $(seq 1 64); do
    python request_uri.py \
        --model $MODEL \
        --dataset $DATASET \
        --output-path $OUTPUT_PATH \
        --config-path $CONFIG_PATH \
        --tp-size $TP_SIZE \
        --port $PORT \
        --max-workers $MAX_WORKERS \
        --rollout $ROLLOUT
done
