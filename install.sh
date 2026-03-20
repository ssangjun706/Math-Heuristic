#!/bin/bash

uv init . -p 3.13
uv venv -p 3.13

source .venv/bin/activate

uv add dotenv numpy openai pyyaml regex requests sympy tqdm transformers torch
uv pip install vllm --torch-backend=auto
uv pip install math-verify[antlr4_13_2]
