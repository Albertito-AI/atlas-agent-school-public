# Research foundations

Original source review dated 27 October 2026; publisher identity and link checks repeated for this public edition on 13 November 2026. These works support components of the design; none validates this repository's implementation or establishes that the general school concept is new.

## Education through feedback and reusable procedures

1. Noah Shinn and others, **Reflexion: language agents with verbal reinforcement learning**, NeurIPS 2023. The paper uses linguistic feedback and stored reflections to guide later attempts without updating model weights. Its experimental results concern the evaluated tasks and configurations. [Published proceedings](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html).

2. Guanzhi Wang and others, **Voyager: An Open-Ended Embodied Agent with Large Language Models**, 2023. The Minecraft system combines curriculum generation, an executable skill library and feedback. It uses model queries without parameter finetuning and evaluates reuse in a new world. This supports investigating reusable procedures; it does not establish general competence. [Paper](https://arxiv.org/abs/2305.16291).

3. Mert Cemri and others, **Why Do Multi-Agent LLM Systems Fail?**, NeurIPS 2025. The final publication reports a dataset of more than 1,600 annotated traces from seven frameworks and identifies failures in system design, inter-agent coordination and task verification. [Published proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html).

4. National Institute of Standards and Technology, **Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile**, NIST AI 600-1, July 2024. The voluntary profile addresses governance, content provenance, pre-deployment testing and incident disclosure. [Full report](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf).


## Design inference and scope

This package combines instruction, feedback, explicit evidence records and bounded verification. Whether these materials improve software-agent performance is a research question. Reference tests establish properties of supplied code and teaching examples; controlled evaluations on unseen task families are required for claims about learner improvement. No model weights are trained by this package.
