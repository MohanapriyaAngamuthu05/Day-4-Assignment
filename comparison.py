# Day 4 - Context Length and Quantization Comparison

def estimate(params_b, bytes_per_param, context_k, kv_per_1k, overhead):
    params = params_b * 1_000_000_000

    weights = (params * bytes_per_param) / (1024 ** 3)

    kv_cache = context_k * kv_per_1k

    total = weights + kv_cache + overhead

    return weights, kv_cache, total


PARAMS = 7
KV_PER_1K = 0.025
OVERHEAD = 1.5
AVAILABLE_MEMORY = 16


print("=" * 80)
print("CONTEXT LENGTH COMPARISON")
print("=" * 80)

contexts = [2, 4, 8, 16]

for context in contexts:

    weights, kv, total = estimate(
        PARAMS,
        0.5,
        context,
        KV_PER_1K,
        OVERHEAD
    )

    print(
        f"Context: {context:>2}K | "
        f"Weights: {weights:.2f} GB | "
        f"KV: {kv:.2f} GB | "
        f"Total: {total:.2f} GB | "
        f"Fits: {'YES' if total <= AVAILABLE_MEMORY else 'NO'}"
    )


print("\n")
print("=" * 80)
print("QUANTIZATION COMPARISON")
print("=" * 80)

quantizations = {
    "Q2": 0.25,
    "Q4": 0.50,
    "Q5": 0.625,
    "Q8": 1.00
}

CONTEXT = 8

for quant, bytes_per_param in quantizations.items():

    weights, kv, total = estimate(
        PARAMS,
        bytes_per_param,
        CONTEXT,
        KV_PER_1K,
        OVERHEAD
    )

    print(
        f"{quant:>2} | "
        f"Weights: {weights:.2f} GB | "
        f"KV: {kv:.2f} GB | "
        f"Total: {total:.2f} GB | "
        f"Fits: {'YES' if total <= AVAILABLE_MEMORY else 'NO'}"
    )