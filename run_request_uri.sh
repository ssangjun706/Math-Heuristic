#!/bin/bash

set -e

source .venv/bin/activate

MODEL="qwen/qwen3-8b-thinking"
DATASET="dataset/test/math_perturb_hard.jsonl"
OUTPUT_PATH="output/"
CONFIG_PATH="config/"

python request_uri.py \
    --model $MODEL \
    --dataset $DATASET \
    --output-path $OUTPUT_PATH \
    --config-path $CONFIG_PATH
