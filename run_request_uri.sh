#!/bin/bash

set -e

source .venv/bin/activate

MODEL="allenai/olmo-3-7b-think-rlvr"
# MODEL="deepseek-ai/deepseek-v3.2"
# MODEL="qwen/qwen3-8b-thinking"
# MODEL="qwen/qwen3-235b-a22b-instruct-2507"

DATASET="dataset/test/math_perturb_original.jsonl"
OUTPUT_PATH="output/"
CONFIG_PATH="config/"

python request_uri.py \
    --model $MODEL \
    --dataset $DATASET \
    --output-path $OUTPUT_PATH \
    --config-path $CONFIG_PATH
