# InfoAgent



## Model Details

### Model Description

InfoAgent is a deep research agent designed to autonomously seek information and reason over long horizons. It leverages a novel data synthesis pipeline and orchestrated web search tools, enabling it to solve complex, multi-step queries by interacting with external resources. The model is post-trained from Qwen3-14B using a two-stage process: supervised fine-tuning to instill long-horizon search behaviors, followed by reinforcement learning to enhance reasoning-driven tool use. [1](https://office.com?path=b1abcdd0-59df-4b9f-904e-081f55075c63)

- **Model type:** Language Model  
- **Language(s):** English  
- **License:** MIT  

## Uses

### Direct Intended Uses

- Autonomous information-seeking and deep research tasks.
- Solving complex, multi-step queries by planning, searching, and reasoning with external tools. 
- Benchmarking and evaluating agentic models on tasks requiring long-horizon reasoning.

### Out-of-Scope Uses

- Any use without human oversight, especially in high-stakes or safety-critical domains.
- Applications where provenance, bias, or misinformation risks are not mitigated.

## Risks and Limitations

- The model may inherit biases and inaccuracies from its Wikipedia-based training data.
- There is a risk of propagating false facts or misinformation if deployed without safeguards. 
- The data synthesis pipeline is currently limited to Wikipedia, which may restrict the diversity of generated problems. 

### Recommendations

- Employ human oversight and bias detection mechanisms. 
- Track provenance and ensure responsible deployment.
- Expand the data synthesis pipeline to broader web sources for greater diversity and challenge.
 
## Evaluation

### Testing Data, Factors, and Metrics

- Evaluated on public benchmarks: BrowseComp, BrowseComp-ZH, Xbench-DS. 
- Metrics include accuracy (%), tool call distribution, recall rates, and context length usage.

## License

- MIT License.

## Microsoft Privacy Statement

- Plese refer to [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839).

## Model Card Contact

- Kai Qiu - kaqiu@microsoft.com  
