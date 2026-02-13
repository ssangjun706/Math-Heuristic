# Math-Tag

## Rollout Progress

### API

| Type  | Model                         | Original | Easy | Hard |
|-------|------------------------------ |----------|------|------|
| API   | Claude-Sonnet-4.5             | ✓        | ✗    | ✓    |
| API   | DeepSeek-V3.2                 | ✓        | ✗    | ✓    |
| API   | Qwen3-235B-A22B-Instruct-2507 | ✓        | ✗    | ✓    |
| API   | Qwen3-235B-A22B-Thinking-2507 | ✓        | ✗    | ✓    |
| API   | Qwen3-30B-A3B-Instruct-2507   | ✓        | ✗    | ✓    |
| API   | Qwen3-30B-A3B-Thinking-2507   | ✓        | ✗    | ✓    |

### Local

| Type  | Model                   | Original | Easy | Hard |
|-------|-------------------------|----------|------|------|
| Local | Qwen3-8B (Thinking)     | ✓        | ✗    | ✓    |
| Local | OLMo-3-7B-Think-DPO     | ✗        | ✗    | ✗    |
| Local | OLMo-3-7B-Think-SFT     | ✗        | ✗    | ✗    |
| Local | OLMo-3-7B-Think-RLVR    | ✓        | ✗    | ✓    |
| Local | OLMo-3-RL-Zero          | ✓        | ✗    | ✓    |
| Local | Nemotron-Cascade-8B     | ✓        | ✗    | ~    |
| Local | Nemotron-Cascade-8B-SFT | ✗        | ✗    | ✗    |


### N-Rollout (N=128)

| Type  | Model                   | Original | Easy | Hard |
|-------|-------------------------|----------|------|------|
| Local | Qwen3-8B (Thinking)     | ✗        | ✗    | ✗    |
| Local | OLMo-3-7B-Think-DPO     | ✗        | ✗    | ✗    |
| Local | OLMo-3-7B-Think-SFT     | ✗        | ✗    | ✗    |
| Local | OLMo-3-RL-Zero          | ✗        | ✗    | ✗    |
| Local | Nemotron-Cascade-8B     | ✗        | ✗    | ✗    |
| Local | Nemotron-Cascade-8B-SFT | ✗        | ✗    | ✗    |


#### Legend:
- ✓ Completed
- ~ In Progress
- ✗ Not Started


## TODO

- [v] N Rollout Support
- [v] Evaluation Retry
- [ ] Pass@K Sampling (k=128) -> Open-source model only


