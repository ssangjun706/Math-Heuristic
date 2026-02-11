#!/bin/bash

set -e

source .venv/bin/activate

export HF_HOME="/scratch/x3326a26/.cache/hf_hub"
export HF_HUB_CACHE="/scratch/x3326a26/.cache/hf_hub"
export TRANSFORMERS_CACHE="/scratch/x3326a26/.cache/transformers"
export HF_TOKEN="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"


MODEL="nvidia/nemotron-cascade-8b"
# MODEL="nvidia/nemotron-cascade-8b-sft"

DATASET="dataset/test/math_perturb_original.jsonl"
OUTPUT_PATH="output/"
CONFIG_PATH="config/"
TP_SIZE=1
PORT=65001

python request_uri.py \
    --model $MODEL \
    --dataset $DATASET \
    --output-path $OUTPUT_PATH \
    --config-path $CONFIG_PATH \
    --tp-size $TP_SIZE \
    --port $PORT
