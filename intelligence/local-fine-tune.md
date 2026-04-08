# Local Fine-Tune

**Status:** canonical
**License:** GSPL Open Specification License (GSPL-OSL-1.0)
**Materializes:** `agent/fine_tune/qlora_recipe.yaml`,
`agent/fine_tune/eval_harness.py`

Every GSPL agent operator can fine-tune CodeSmith on their own
hardware, from their own data, without touching any hosted service.
This document describes the canonical recipe.

## Method

QLoRA 4-bit via Unsloth. The base model is any open-weights model
listed in `manifest.yaml#fine_tune.base_models_accepted`. The default
is `meta-llama/Llama-3.3-70B-Instruct`, but any of the accepted
base models is interchangeable — the eval harness is model-agnostic.

## Hardware floor

- 7B / 13B bases: single 24 GB consumer GPU (RTX 4090, RTX 3090,
  A5000, etc.).
- 70B bases: single 80 GB H100 or A100.

No multi-node training is required. No cluster is required. No cloud
is required.

## Data mix

Declared in `qlora_recipe.yaml#dataset.mix_ratios`:

    gold       0.70    (agent-generated gold corpus)
    substrate  0.25    (seed_commons + spec + language)
    negative   0.05    (contrastive failures from bootstrap loop)

Gold and negative examples come from the bootstrap loop. Substrate
examples are regenerated deterministically from the repository at
fine-tune time so the training set is always pinned to the current
substrate version.

## Training invariants

- `seed = 0` for both the optimizer and the data loader.
- `packing = true` with `max_seq_length = 8192`.
- `bf16 = true`, `gradient_checkpointing = true`.
- LoRA rank 64, alpha 128, dropout 0.0 (deterministic).
- Cosine LR schedule, warmup ratio 0.03.

Determinism: two independent operators running this recipe against
the same data mix and the same base model MUST produce adapters with
byte-identical eval metrics. (They need not produce byte-identical
weights because floating-point accumulation order is hardware
dependent, but the downstream evaluation must agree.)

## Promotion gate

An adapter is promoted to production only if every metric in
`agent/fine_tune/eval_harness.py#EvalMetrics.all_pass` meets or
exceeds `required_pass_rate` (default 0.995):

  - `stage_4_first_try_pass_rate`
  - `jcs_round_trip_byte_identity`
  - `lineage_closure_rate`
  - `refusal_calibration`

If any metric falls short, the adapter is archived at
`agent/fine_tune/adapters/archived/<timestamp>/` and the previous
adapter stays in production.

## Sovereignty

Every promoted adapter is signed by the SovereignSigner with
ECDSA-P256 RFC 6979 over the concatenation of:

  - SHA-256(adapter tensor bytes)
  - SHA-256(qlora_recipe.yaml bytes used for training)
  - SHA-256(data mix manifest)

The signature and the recipe bytes are archived next to the adapter,
so any future fork can verify exactly how the adapter was produced.

## Air-gap compatibility

Fine-tuning is fully local. No telemetry, no wandb, no cloud metrics
upload. The eval harness runs entirely inside the Wasm code-execution
sandbox. An operator can fine-tune, evaluate, promote, and sign an
adapter with the network physically disconnected.
