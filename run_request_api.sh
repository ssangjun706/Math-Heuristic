#!/bin/bash

set -e
source .venv/bin/activate

MODEL="qwen/qwen3-235b-a22b-thinking-2507"
DATASET="hard"
OUTPUT_PATH="./output"
CONFIG_PATH="./config"
MAX_WORKERS=20
ROLLOUT=1
PROMPT_TAG="default"
# CUSTOM_INSTRUCTION_FILE="./prompt/custom_instruction.txt"
# CUSTOM_SYSTEM_PROMPT_FILE="./prompt/custom_system.txt"
# INSTRUCTION_MODE="append"  # append | replace

python request_uri.py \
    --model $MODEL \
    --dataset $DATASET \
    --output-path $OUTPUT_PATH \
    --config-path $CONFIG_PATH \
    --max-workers $MAX_WORKERS \
    --rollout $ROLLOUT \
    --prompt-tag $PROMPT_TAG

# Uncomment below for custom prompt experiments:
#     --custom-instruction-file $CUSTOM_INSTRUCTION_FILE \
#     --custom-system-prompt-file $CUSTOM_SYSTEM_PROMPT_FILE \
#     --instruction-mode $INSTRUCTION_MODE