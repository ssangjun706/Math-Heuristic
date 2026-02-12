#!/bin/bash

module load gcc/15.2.0
module load cuda/12.9.1
module update

uv init . -p 3.13
uv venv -p 3.13

source .venv/bin/activate

uv add dotenv numpy openai pyyaml regex requests sympy tqdm transformers torch
uv pip install vllm --torch-backend=auto