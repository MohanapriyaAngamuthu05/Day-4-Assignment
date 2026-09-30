# Day 4 - Memory Estimator for Local LLMs

def estimate_memory(
    params_b,
    bytes_per_param,
    context_k,
    kv_gb_per_1k_tokens,
    overhead_gb,
    available_memory_gb
):
    # Convert parameters from billions to actual parameters
    params = params_b * 1_000_000_000

    # Weight memory
    weights_gb = (params * bytes_per_param) / (1024 ** 3)

    # KV cache memory
    context_tokens = context_k * 1000
    kv_cache_gb = (context_tokens / 1000) * kv_gb_per_1k_tokens

    # Total memory
    total_gb = weights_gb + kv_cache_gb + overhead_gb

    # Fit check
    fits = total_gb <= available_memory_gb

    return weights_gb, kv_cache_gb, total_gb, fits


# Available machine memory
AVAILABLE_MEMORY_GB = 16

# Example configurations
models = [
    {
        "name": "Llama 3.2 3B Q4",
        "params": 3,
        "bytes": 0.5,
        "context": 4,
        "kv": 0.015,
        "overhead": 1.0
    },
    {
        "name": "Qwen2.5 7B Q4",
        "params": 7,
        "bytes": 0.5,
        "context": 4,
        "kv": 0.025,
        "overhead": 1.5
    },
    {
        "name": "Mistral 7B Q4",
        "params": 7,
        "bytes": 0.5,
        "context": 8,
        "kv": 0.025,
        "overhead": 1.5
    },
    {
        "name": "Llama 3.1 8B Q4",
        "params": 8,
        "bytes": 0.5,
        "context": 8,
        "kv": 0.03,
        "overhead": 1.5
    }
]


print("=" * 75)
print("DAY 4 - OPEN LLM MEMORY ESTIMATOR")
print("=" * 75)

print(f"Available memory: {AVAILABLE_MEMORY_GB} GB\n")

for model in models:

    weights, kv, total, fits = estimate_memory(
        model["params"],
        model["bytes"],
        model["context"],
        model["kv"],
        model["overhead"],
        AVAILABLE_MEMORY_GB
    )

    print(f"Model       : {model['name']}")
    print(f"Parameters  : {model['params']} B")
    print(f"Precision   : Q4")
    print(f"Context     : {model['context']}K")
    print(f"Weights     : {weights:.2f} GB")
    print(f"KV Cache    : {kv:.2f} GB")
    print(f"Total       : {total:.2f} GB")
    print(f"Fits?       : {'YES' if fits else 'NO'}")
    print("-" * 75)