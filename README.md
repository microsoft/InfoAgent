# InfoAgent
[InfoAgent](https://arxiv.org/abs/2509.25189) is a deep research agent designed to autonomously seek information and reason over long horizons.

## News
* `[2026-2-3]`:🔥We release the [RE-TRAC](retrac/README.md) for deep research!

## Model Details

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

