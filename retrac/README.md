# Re-TRAC: Recursive Trajectory Compression for Deep Research Agents

<!-- <div align="center">
  <picture>
      <img src="./assets/logo.png" width="100%">
  </picture>
</div> -->

<!-- <hr> -->

<!-- <div align="center" style="line-height: 1;"> -->

<!-- [![PAPER](https://img.shields.io/badge/Paper-red?style=for-the-badge&logo=arxiv&logoColor=white)]([TODO: arxiv_url])
[![GITHUB](https://img.shields.io/badge/Github-24292F?style=for-the-badge&logo=github&logoColor=white)]([TODO: repo_url])
[![MODELS](https://img.shields.io/badge/Models-5EDDD2?style=for-the-badge&logo=huggingface&logoColor=ffffff&labelColor)]([TODO: hf_url])
[![DEMO](https://img.shields.io/badge/Demo-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white)]([TODO: project_url]) -->

</div>
<p align="center">
🤗 <a href="[TODO: hf_url]" target="_blank">HuggingFace</a> ｜
💻 <a href="[TODO: repo_url]" target="_blank">GitHub</a> | 
📑 <a href="[TODO: arxiv_url]">Paper</a> | 
🌐 <a href="[TODO: project_url]">Demo</a>

<!-- > [!NOTE]
> This demo is for quick exploration only. Response times may vary or fail intermittently due to model latency and tool QPS limits. For a stable experience we recommend local deployment. -->

# Introduction

We present **Re-TRAC (REcursive TRajectory Compression)**, a recursive framework for deep research agents that enables cross-trajectory exploration via structured state compression. Instead of treating rollouts as independent, Re-TRAC compresses each trajectory into an explicit state (e.g., evidence, uncertainties, failure modes, frontier candidates) and conditions the next rollout on it. This state-guided process supports more efficient search and broader exploration across rollouts.

On BrowseComp, Re-TRAC outperforms ReAct-style baselines by +15–20% absolute improvement. It supports both prompting and supervised fine-tuning; our SFT-only models reach 30% (4B) and 53% (30B).

<p align="center">
  <img width="100%" src="./assets/overview.png">
</p>



## Features

- 🔄 **Recursive Trajectory Compression**: Compresses each trajectory into a structured state that captures evidence, uncertainties, failures, and next plans, enabling efficient cross-trajectory information transfer.
- 🎯 **Cross-trajectory Exploration**: Conditions subsequent rollouts on compressed states from previous attempts, enabling better planning and less redundancy.
- 📈 **Strong Performance Gains**: Achieves +15–20% absolute improvement over ReAct-style baselines on BrowseComp benchmark.
- 🚀 **Multiple Training Paradigms**: Supports both prompting-based and supervised fine-tuning approaches, with checkpoints available for 4B and 30B models.
- 💾 **Token-Efficient**: Maintains rich information transfer across rollouts while staying within the same token budget constraints.

# Model Download

Code and checkpoints are **coming soon (pending approval)**. 

|            Model            |                                                                           Download Links                                                                           | Model Size |
| :-------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------: | :--------: |
| Re-TRAC-SFT-30B | [🤗 HuggingFace]([])<br> *Coming soon* |  30B   |
| Re-TRAC-SFT-4B | [🤗 HuggingFace]([])<br> *Coming soon* |  4B   |

<!-- # News

[2025/XX/XX]🚀 Re-TRAC paper released on arXiv. -->

<!-- [2025/XX/XX]🔥 We have released **Re-TRAC-SFT-30B** and **Re-TRAC-SFT-4B** checkpoints. -->

# Benchmark Results

## Main Results

Comprehensive evaluation results across multiple benchmarks:

| Model | BrowseComp | BrowseComp-zh | GAIA | XBench | HLE |
|-------|------------|---------------|------|--------|-----|
| **Closed** | | | | | |
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

<!-- ## SFT Models

<p align="center">
  <img width="100%" src="./assets/benchmark.png">
</p>

## Training Free for frontier model

<p align="center">
  <img width="100%" src="./assets/prompting_results.png">
</p> -->

# Code and Resources

Code and resources are **coming soon (pending approval)**. We are finalizing internal release approval for:

- **Model Checkpoints**: 4B and 30B SFT models
- **Inference Code**: Complete inference pipeline and scripts
- **Reproduction Scripts**: Evaluation and reproduction configs
- **Training Data**: Dataset used for supervised fine-tuning
- **Training Code**: Training scripts and configurations

If you want updates, please **Star / Watch** this repository!



# Citation

If you find Re-TRAC useful in your research, please cite our paper:

```bibtex
@inproceedings{retrac2026,
  title={Re-TRAC: Recursive Trajectory Compression for Deep Research Agents},
}
```

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Contact

For questions, issues, or collaboration inquiries, please open an issue on GitHub or contact [TODO: Add contact information].
