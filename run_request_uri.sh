#!/bin/bash

set -e

module load gcc/15.2.0
module load cuda/12.9.1

source .venv/bin/activate

export HF_HOME="/scratch/x3326a26/.cache/hf_hub"
export HF_HUB_CACHE="/scratch/x3326a26/.cache/hf_hub"
export TRANSFORMERS_CACHE="/scratch/x3326a26/.cache/transformers"
export HF_TOKEN="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"
export CUDA_VISIBLE_DEVICES="1"

# MODEL="nvidia/nemotron-cascade-8b"
# MODEL="nvidia/nemotron-cascade-8b-sft"
# MODEL="allenai/olmo-3-7b-think-sft"
# MODEL="allenai/olmo-3-7b-think-dpo"
MODEL="allenai/olmo-3-7b-rl-zero"

# DATASET="simple"
# DATASET="hard"
DATASET="original"

OUTPUT_PATH="./math-heuristics"
CONFIG_PATH="./config"

TP_SIZE=1
PORT=65002
MAX_WORKERS=20

python request_uri.py \
    --model $MODEL \
    --dataset $DATASET \
    --output-path $OUTPUT_PATH \
    --config-path $CONFIG_PATH \
    --tp-size $TP_SIZE \
    --port $PORT \
    --max-workers $MAX_WORKERS 

