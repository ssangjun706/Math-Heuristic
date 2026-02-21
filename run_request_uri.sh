#!/bin/bash

set -e

# module load gcc/15.2.0
# module load cuda/12.9.1

source .venv/bin/activate

export HF_TOKEN="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"
export CUDA_VISIBLE_DEVICES="0,1"

MODEL="qwen/qwen3-8b-base"
# MODEL="nvidia/nemotron-cascade-8b"
# MODEL="nvidia/nemotron-cascade-8b-sft"
# MODEL="allenai/olmo-3-7b-think-sft"
# MODEL="allenai/olmo-3-7b-think-dpo"
# MODEL="allenai/olmo-3-7b-rl-zero"

# DATASET="simple"
# DATASET="hard"
DATASET="original"

# OUTPUT_PATH="./math-heuristics"
OUTPUT_PATH="./output"
CONFIG_PATH="./config"

TP_SIZE=2
PORT=65002
MAX_WORKERS=20
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

