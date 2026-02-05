# Re-TRAC: Recursive Trajectory Compression for Deep Research Agents

</div>
<p align="center">
🤗 <a href="https://huggingface.co/microsoft/InfoAgent">Model Checkpoint</a> ｜
💻 <a href="https://github.com/microsoft/InfoAgent/tree/main/retrac">GitHub</a> | 
📑 <a href="https://arxiv.org/abs/2602.02486">Paper</a> | 
🌐 <a href="https://huggingface.co/spaces/JialiangZhu/RE-TRAC">Demo</a>

> You Can Try our [RE-TRAC 30B](https://huggingface.co/spaces/JialiangZhu/RE-TRAC) Domo now <br>
> We have released [Re-TRAC-SFT-30B](https://huggingface.co/microsoft/InfoAgent) checkpoint.

## Introduction

We present **Re-TRAC (REcursive TRajectory Compression)**, a recursive framework for deep research agents that enables cross-trajectory exploration via structured state compression. Instead of treating rollouts as independent, Re-TRAC compresses each trajectory into an explicit state (e.g., evidence, uncertainties, failure modes, frontier candidates) and conditions the next rollout on it. This state-guided process supports more efficient search and broader exploration across rollouts.

On BrowseComp, Re-TRAC outperforms ReAct-style baselines by +15–20% absolute improvement. It supports both prompting and supervised fine-tuning; our SFT-only models reach 30% (4B) and 53% (30B).

<p align="center">
  <img width="90%" src="./assets/overview.png">
</p>

<p align="center">
  <img width="90%" src="./assets/model_preformace.png">
</p>

## Features

- 🔄 **Recursive Trajectory Compression**: Compresses each trajectory into a structured state that captures evidence, uncertainties, failures, and next plans, enabling efficient cross-trajectory information transfer.
- 🎯 **Cross-trajectory Exploration**: Conditions subsequent rollouts on compressed states from previous attempts, enabling better planning and less redundancy.
- 📈 **Strong Performance Gains**: Achieves +15–20% absolute improvement over ReAct-style baselines on BrowseComp benchmark.
- 🚀 **Multiple Training Paradigms**: Supports both prompting-based and supervised fine-tuning approaches, with checkpoints available for 4B and 30B models.
- 💾 **Token-Efficient**: Maintains rich information transfer across rollouts while staying within the same token budget constraints.

## Model Download

Code and checkpoints are **coming soon (pending approval)**. 

|            Model            |                                                                           Download Links                                                                           | Model Size |
| :-------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------: | :--------: |
| Re-TRAC-SFT-30B | [🤗 HuggingFace](https://huggingface.co/microsoft/InfoAgent)<br> |  30B   |
| Re-TRAC-SFT-4B | [🤗 HuggingFace]([])<br> *Coming soon* |  4B   |


## Benchmark Results

### Main Results

Comprehensive evaluation results across multiple benchmarks:

| Model | BrowseComp | BrowseComp-zh | GAIA | XBench | HLE |
|-------|------------|---------------|------|--------|-----|
| **Closed Model** | | | | | |
| Claude-4.5-Sonnet | 24.1 | 42.4 | 71.2 | 66.0 | 32.0 |
| o3 | 49.7 | 58.1 | 70.5 | 66.7 | 24.9 |
| OpenAI DeepResearch | 51.5 | 42.9 | 67.4 | - | 26.6 |
| GPT-5-high | 54.9 | 63.0 | 76.7 | 77.9 | 42.0 |
| Gemini-3-pro | 37.8 | 51.6 | 74.8 | - | 38.3 |
| **Model  > 70B** | | | | | |
| Kimi-K2-Thinking-1T | 60.2 | 62.3 | - | - | 51.0 |
| DeepSeek-V3.2-Thinking-685B | 67.6 | 65.0 | - | - | 40.8 |
| GLM-4.7-358B | 52.0 | 66.6 | - | - | 42.8 |
| MiniMax-M2-229B | 44.0 | 48.5 | 75.7 | 72.0 | 31.8 |
| **Model 15B~70B** | | | | | |
| Tongyi-DeepResearch-30B-A3B | 43.4 | 46.7 | 70.9 | 75.0 | **32.9** |
| IterResearch-30B-A3B | 37.3 | 45.2 | 72.8 | - | 28.8 |
| WebSailor-V2-30B-A3B (RL) | 35.3 | 44.1 | 74.1 | 73.7 | 30.6 |
| **RE-TRAC-30B-A3B (Ours)** | **53.0** | **57.3** | **78.2** | **83.0** | 31.5 |
| **Model < 15B** | | | | | |
| InfoAgent-14B | 15.3 | 29.2 | - | 40.4 | - |
| WebExplorer-8B | 15.7 | 32.0 | 50.0 | 53.7 | 17.3 |
| AgentCPM-Explore-4B | 25.0 | 29.0 | 63.9 | 70.0 | 19.1 |
| NestBrowse-4B | 22.4 | 28.4 | 68.9 | 74.0 | - |
| **RE-TRAC-4B (Ours)** | **30.0** | **36.1** | **70.4** | **76.6** | **22.2** |


## Code and Resources


### Model Deployment
First, you need to download the model checkpoint from [HuggingFace](https://huggingface.co/microsoft/InfoAgent).

We recommend to deploy the model via sglang version `0.5.7`.

**IMPORTANT !!!** Do not use `reasoning parser` config in the `sglang` server.

```bash
python -m sglang_router.launch_server \
    --model-path /path/to/your/model \
    --dp 8 \
    --tp 1 \
    --tool-call-parser qwen
```

### initialize the environment
```bash
cd ./retrac
uv venv
uv pip install -r requirements.txt
```
### set the environment variables
```bash
cp .env.example .env
```
```bash
# for openai format agent model in Re-TRAC (deploy via sglang or vllm)
OPENAI_API_BASE=YOUR_OPENAI_API_BASE_HERE
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE 

# for search engine and browse tool
SERPER_API_KEY=YOUR_SERPER_API_KEY_HERE # follow the instructions in https://serper.dev/
JINA_API_KEY=YOUR_JINA_API_KEY_HERE # follow the instructions in https://jina.ai/

# for summarization model in visit tool
MODEL_FOR_VISIT_SUMMARIZE=MODEL_NAME_HERE_FOR_SUMMARIZE_MODEL_IN_VISIT_TOOL
BASE_URL_FOR_VISIT_SUMMARIZE=YOUR_BASE_URL_HERE_FOR_SUMMARIZE_MODEL_IN_VISIT_TOOL
API_KEY_FOR_VISIT_SUMMARIZE=YOUR_API_KEY_HERE_FOR_SUMMARIZE_MODEL_IN_VISIT_TOOL
```

### run the agent in streaming mode
```bash
cd ./retrac
uv run run.py --config deep_research.yaml --question "What is the capital of France?"
```

### run the agent in non-streaming mode
```bash
cd ./retrac
uv run run.py --config deep_research.yaml --question "What is the capital of France?" --non-streaming
```

If you want updates, please **Star / Watch** this repository!

### optional : modify the config file in `deep_research.yaml`

You can modify the config file in `retrac/deep_research.yaml` to change the max cycles, the prompts, etc. <br>

```yaml
max_cycles: 8 # we default set the max cycles to 8, you may change it to 2 or 4 for faster inference
xxx_prompt: # you can modify the xxx_prompt to change the system prompt, the continue prompt, the summary prompt, for other tasks.
```

## Citation

If you find Re-TRAC useful in your research, please cite our paper:

```bibtex
@misc{zhu2026retracrecursivetrajectorycompression,
      title={RE-TRAC: REcursive TRAjectory Compression for Deep Search Agents}, 
      author={Jialiang Zhu and Gongrui Zhang and Xiaolong Ma and Lin Xu and Miaosen Zhang and Ruiqi Yang and Song Wang and Kai Qiu and Zhirong Wu and Qi Dai and Ruichun Ma and Bei Liu and Yifan Yang and Chong Luo and Zhengyuan Yang and Linjie Li and Lijuan Wang and Weizhu Chen and Xin Geng and Baining Guo},
      year={2026},
      eprint={2602.02486},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2602.02486}, 
}
```

## Microsoft Privacy Statement

- Plese refer to [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839).


## License

- MIT License.


## Contact

For questions, issues, or collaboration inquiries, please open an issue on GitHub or contact us by email.
- Kai Qiu - kaqiu@microsoft.com  
- Jialiang Zhu - jialiangzhu@seu.edu.cn
