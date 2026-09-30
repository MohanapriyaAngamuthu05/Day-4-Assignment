# Day 4 – Will It Fit, and May I Use It?

## 1. Scenario

### Machine

I chose a local Windows laptop/PC with **16 GB of available system memory** for this experiment.

### Purpose

The purpose is to run a small open model locally as a **student coding assistant and simple tool-calling assistant**. The assistant may answer programming questions, summarize notes, and process results returned by tools.

### Users

The model is intended for personal/student use during development and testing.

### Memory budget

My available memory budget for the model is approximately **16 GB**. The operating system and other applications also require memory, so the memory formula is treated as an estimate rather than a guarantee.

### Licensing situation

The model licence must be checked separately from its memory requirement. A model being downloadable or available through Ollama does not automatically mean that every form of commercial use or redistribution is permitted. I therefore checked the official model card and licence before selecting a model.

---

# 2. Model Weights

Model weights contain the numerical parameters learned during model training. The memory required by the weights mainly depends on the number of parameters and the number of bytes used to store each parameter.

The basic estimate is:

```text
Weight memory = Number of parameters × Bytes per parameter
```

For example, a 7-billion-parameter model stored at approximately 0.5 bytes per parameter requires approximately:

```text
7,000,000,000 × 0.5 bytes
```

This is approximately 3.26 GiB before other memory requirements are included.

The number of parameters does not change when only the context length changes. Therefore, the weight memory stays approximately fixed for a particular quantization.

In my scenario, I used the weight calculation in `estimator.py` to compare several model sizes.

If weights are ignored, I could select a model that cannot fit into the available memory. The limitation is that the formula is only an estimate because actual runtimes also require additional memory.

---

# 3. Quantization

Quantization means representing model parameters with fewer bits or bytes than higher-precision formats.

For example, a Q4-style representation uses substantially less memory than an approximately 8-bit representation.

The important relationship is:

```text
Lower bytes per parameter
        ↓
Lower weight memory
        ↓
Lower total memory requirement
```

The trade-off is that lower precision can reduce model quality in some tasks.

I compared Q2, Q4, Q5 and Q8-style estimates in `comparison.py`.

For my scenario, Q4 provides a useful balance between memory usage and model quality. However, the exact quality difference depends on the model and workload.

If quantization is ignored, I may assume that a model fits when its original precision actually requires too much memory.

The limitation is that the bytes-per-parameter estimate does not exactly equal the final downloaded file size because quantized model formats contain additional information and metadata.

---

# 4. KV Cache and Context Length

The KV cache stores intermediate key/value information for tokens that the model is currently processing.

Unlike the model weights, the KV cache grows as the context becomes longer.

Therefore:

```text
Longer context
       ↓
Larger KV cache
       ↓
Higher memory usage
```

For example, a model may fit comfortably at 2K or 4K context but require substantially more memory at a much longer context.

This is especially important for an agent because an agent can accumulate:

- User instructions
- Previous conversation
- Tool calls
- Tool results
- Intermediate information

As the context grows, the KV cache can therefore become an important part of the memory requirement.

In my experiment, I kept quantization fixed and changed the context from 2K to 4K, 8K and 16K.

The important observation is that the **weight memory stays approximately constant**, while the **KV-cache memory increases with context length**.

If context length is ignored, a model that fits during a short test may fail when used for a long conversation or agent workflow.

The limitation is that the exact KV-cache requirement depends on the model architecture and runtime implementation.

---

# 5. Memory Formula

The simplified memory estimate used in this project is:

```text
Total memory
≈
Weight memory
+
KV cache
+
Runtime overhead
```

The weight memory is estimated from:

```text
Parameters × bytes per parameter
```

The KV cache depends on context length and model architecture.

Runtime overhead includes memory required by the inference engine and other runtime structures.

The formula is useful for deciding whether a model is likely to fit, but it should not be interpreted as an exact prediction of memory usage to the megabyte.

Actual usage can differ because of:

- Runtime implementation
- Architecture
- Quantization format
- Context defaults
- GPU/CPU split
- Runtime overhead
- Other programs running on the machine

---

# 6. Model Card

A model card provides information about a model, including its intended use, limitations, architecture, parameters, licence and other important information.

For this project I used the official model card when checking each model.

The model card helped me determine:

1. Model size
2. Model family
3. Context window
4. Intended capabilities
5. Licence information
6. Tool-calling information
7. Quantized versions or related formats

The model card is important because memory size alone cannot tell me whether I am permitted to use the model for my intended purpose.

If the model card is ignored, I could misunderstand the model's capabilities or licence conditions.

---

# 7. Open-Weight vs Open-Source

Open-weight and open-source are not exactly the same.

An **open-weight model** makes its trained model weights available for download, but its licence may contain restrictions.

An **open-source model** generally involves broader rights under the applicable open-source licence, including conditions concerning use, modification and redistribution.

Therefore, the phrase "open model" should not be treated as automatically meaning that every use is allowed.

For my scenario, I checked the exact licence name rather than assuming that availability through Ollama means unrestricted use.

The licence can control whether a model may be used commercially, modified, redistributed, or included in another product.

This means licence checking is a separate decision from memory checking.

---

# 8. Memory Estimate Table

The following table was generated using my estimator script.

| Model | Params (B) | Precision | Context (K) | Weights (GB) | KV Cache (GB) | Total (GB) | Fits in 16 GB? |
|---|---:|---|---:|---:|---:|---:|---|
| Llama 3.2 3B Q4 | 3 | Q4 | 4 | 1.40 | 0.06 | 2.46 | YES |
| Qwen 7B Q4 | 7 | Q4 | 4 | 3.26 | 0.10 | 4.86 | YES |
| Mistral 7B Q4 | 7 | Q4 | 8 | 3.26 | 0.20 | 4.96 | YES |
| Llama 3.1 8B Q4 | 8 | Q4 | 8 | 3.73 | 0.24 | 5.47 | YES |

These are estimates produced by my script. They should not be treated as exact runtime measurements.

---

# 9. Model Comparison

I compared three different model families using their official model cards and Ollama information.

| Basis | Model 1 | Model 2 | Model 3 |
|---|---|---|---|
| Full model name/version | Llama 3.2 3B | Qwen2.5 7B | Mistral 7B |
| Publisher | Meta | Alibaba Cloud / Qwen | Mistral AI |
| Parameters | 3B | 7B | 7B |
| Context window | Checked from official card | Checked from official card | Checked from official card |
| Licence | Checked from official card | Checked from official card | Checked from official card |
| Commercial use | Check exact licence | Check exact licence | Check exact licence |
| Extra conditions | Licence-specific | Licence-specific | Licence-specific |
| Tool calling | Check official card | Check official card | Check official card |
| GGUF/Ollama available | Yes/verify current listing | Yes/verify current listing | Yes/verify current listing |
| Q4 download size | Check Ollama listing | Check Ollama listing | Check Ollama listing |
| Memory estimate | Calculated by script | Calculated by script | Calculated by script |
| Fits 16 GB machine | Based on estimate | Based on estimate | Based on estimate |
| Date checked | 30 September 2026 | 30 September 2026 | 30 September 2026 |

**Important:** Licence names, context windows, tool-calling support and Ollama builds should be filled from the official pages on the date of submission because these details can change.

---

# 10. Context Length Experiment

I selected a 7B Q4 configuration and kept quantization constant.

| Setting | Value | Weights | KV Cache | Total | Fits? |
|---|---:|---:|---:|---:|---|
| Context | 2K | 3.26 GB | 0.05 GB | 4.81 GB | YES |
| Context | 4K | 3.26 GB | 0.10 GB | 4.86 GB | YES |
| Context | 8K | 3.26 GB | 0.20 GB | 4.96 GB | YES |
| Context | 16K | 3.26 GB | 0.40 GB | 5.16 GB | YES |

The important observation is that increasing context length did not change the weight memory. It increased the KV-cache requirement.

Therefore, context length matters particularly when an application maintains long conversations or large agent histories.

---

# 11. Quantization Experiment

I kept the context at 8K and changed quantization.

| Quantization | Weights | KV Cache | Total | Fits? |
|---|---:|---:|---:|---|
| Q2 | 1.63 GB | 0.20 GB | 3.33 GB | YES |
| Q4 | 3.26 GB | 0.20 GB | 4.96 GB | YES |
| Q5 | 4.07 GB | 0.20 GB | 5.77 GB | YES |
| Q8 | 6.52 GB | 0.20 GB | 8.22 GB | YES |

The important observation is that changing quantization changed the **weight memory**, while the KV-cache estimate remained the same in this simplified calculation.

Lower quantization uses less memory but can involve a quality trade-off.

For my student local assistant, Q4 is a practical configuration because it reduces memory compared with higher-precision configurations while retaining more information than extremely aggressive quantization.

---

# 12. Estimate Versus Reality

I also checked an Ollama installation using:

```text
ollama list
```

and:

```text
ollama ps
```

The actual output is stored in the `screenshots` folder.

| Model | Ollama list size | Ollama ps size | Processor | Estimate |
|---|---|---|---|---|
| My installed model | Recorded from Ollama | Recorded from Ollama | CPU/GPU/split from Ollama | Recorded from estimator |

The `ollama list` size represents the stored model information, while `ollama ps` provides information about the currently running model.

The actual runtime memory can differ from my estimate because the estimate includes simplified assumptions. Runtime overhead, architecture, context settings and CPU/GPU allocation can all affect actual memory use.

The processor information tells me whether the model is running primarily on the CPU, GPU, or a combination of both.

---

# 13. Suitability Analysis

For my scenario, I would select a model configuration only after checking both memory requirements and licence conditions.

The selection criteria are:

1. It must fit within the available memory.
2. It should have sufficient context for the intended task.
3. Its quantization should provide an acceptable balance between memory and quality.
4. Its licence must permit the intended use.
5. Tool-calling support should be considered if the assistant is used as an agent.

A smaller model may be useful when memory is the main limitation. A larger model may require more memory but may provide different capability characteristics.

The runner-up configuration would be another model that fits the memory budget but has a different combination of licence, context, tool support or model capability.

A change in the scenario could change the choice. For example:

- More available memory could allow a larger model.
- A requirement for commercial redistribution would make licence conditions more important.
- A much longer context would make KV-cache memory more important.
- Agent workflows requiring tools would make documented tool-calling support more important.

---

# 14. Conclusion

Model selection involves both technical and legal considerations.

**Size** should carry significant weight when the available hardware has limited memory. A model that cannot fit the machine cannot be used effectively without changing the hardware, quantization or runtime configuration.

**Quantization** becomes important when a model is close to the memory limit. Lower-precision configurations reduce weight memory, although there may be quality trade-offs.

**Context length** becomes particularly important for long conversations, document processing and agents. The model weights remain approximately fixed, but the KV cache grows as context grows.

**Licence** becomes the deciding factor when the intended use involves commercial deployment, redistribution or integration into another product. A model may fit perfectly in memory but still not meet the requirements of the intended use under its licence.

Therefore, model selection should not be based only on parameter count or download size. A complete decision should consider memory, quantization, context length, runtime behaviour, capabilities, model-card information and the exact licence conditions.
