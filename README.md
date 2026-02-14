# Math-Tag

## Rollout Progress

### API

| Type  | Model                         | Original | Simple | Hard |
|-------|------------------------------ |----------|--------|------|
| API   | Claude-Sonnet-4.5             | ✓        | ✗      | ✓    |
| API   | DeepSeek-V3.2                 | ✓        | ✓      | ✓    |
| API   | Qwen3-235B-A22B-Instruct-2507 | ✓        | ✓      | ✓    |
| API   | Qwen3-235B-A22B-Thinking-2507 | ✓        | ✓      | ✓    |
| API   | Qwen3-30B-A3B-Instruct-2507   | ✓        | ✓      | ✓    |
| API   | Qwen3-30B-A3B-Thinking-2507   | ✓        | ✓      | ✓    |
| API   | Qwen3-8B (Thinking)           | ✓        | ✓      | ✓    |
| API   | OLMo-3-7B-Think-RLVR          | ✓        | ✓      | ✓    |


### Local

| Type  | Model                   | Original | Simple | Hard |
|-------|-------------------------|----------|--------|------|
| Local | OLMo-3-7B-Think-DPO     | ✓        | ✓      | ✓    |
| Local | OLMo-3-7B-Think-SFT     | ✓        | ✓      | ✓    |
| Local | OLMo-3-RL-Zero          | ✓        | ✓      | ✓    |
| Local | Nemotron-Cascade-8B     | ✓        | ✓      | ✓    |
| Local | Nemotron-Cascade-8B-SFT | ~        | ✓      | ✗    |


### N-Rollout (N=128)

| Type  | Model                   | Original | Simple | Hard |
|-------|-------------------------|----------|--------|------|
| Local | OLMo-3-7B-Think-DPO     | ✗        | ✗      | ✗    |
| Local | OLMo-3-7B-Think-SFT     | ✗        | ✗      | ✗    |
| Local | OLMo-3-RL-Zero          | ✗        | ✗      | ✗    |
| Local | Nemotron-Cascade-8B     | ✗        | ✗      | ✗    |
| Local | Nemotron-Cascade-8B-SFT | ✗        | ✗      | ✗    |


#### Legend:
- ✓ Completed
- ~ In Progress
- ✗ Not Started


## TODO

- [ ] Pass@K Sampling (k=128)


