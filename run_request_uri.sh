#!/bin/bash

set -e

export CUDA_VISIBLE_DEVICES="0,1,2,3"
export HF_HOME="/data2/sangjunsong/.cache/hf_hub"
export HF_HUB_CACHE="/data2/sangjunsong/.cache/hf_hub"
export TRANSFORMERS_CACHE="/data2/sangjunsong/.cache/transformers"
export HF_TOKEN="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"

source .venv/bin/activate

OUTPUT_PATH="./output"
CONFIG_PATH="./config"
TP_SIZE=4
PORT=34437
MAX_WORKERS=16
MODEL="allenai/olmo-3-7b"
# MODEL="nvidia/nemotron-cascade-8b-sft"

ROLLOUT=64
DATASET="hard"
PROMPT_TAG="default"
# CUSTOM_INSTRUCTION_FILE="./prompt/custom_instruction.txt"
# CUSTOM_SYSTEM_PROMPT_FILE="./prompt/custom_system.txt"
# INSTRUCTION_MODE="append"  # append | replace

python request_uri.py \
    --model $MODEL \
    --dataset $DATASET \
    --output-path $OUTPUT_PATH \
    --config-path $CONFIG_PATH \
    --tp-size $TP_SIZE \
    --port $PORT \
    --max-workers $MAX_WORKERS \
    --rollout $ROLLOUT \
    --prompt-tag $PROMPT_TAG

# Uncomment below for custom prompt experiments:
#     --custom-instruction-file $CUSTOM_INSTRUCTION_FILE \
#     --custom-system-prompt-file $CUSTOM_SYSTEM_PROMPT_FILE \
#     --instruction-mode $INSTRUCTION_MODE