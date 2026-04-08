# ADR 0012 — Full-Capacity Sovereign Self-Bootstrapping Agent

**Status:** Accepted
**Date:** 2026-04-08
**License:** GSPL Open Specification License (GSPL-OSL-1.0)

## Context

The GSPL agent was originally specified as a six-stage pipeline with
LLM-bearing IntentOracle and CodeSmith sub-agents, but the manifest,
stage modules, sub-agents, tool layer, bootstrap loop, and fine-tune
recipe were scattered across `intelligence/gspl-agent-full-capacity.md`
and `intelligence/tool-layer.md` without a single runnable materialization.
Operators who wanted to fork the agent had no single source of truth.

At the same time, the project's non-negotiable constraints are:

- 100% free forever. No paywalls. No rate limits.
- Forkable and self-hostable.
- No cloud dependency.
- Air-gap capable.
- Deterministic output across compliant readers.
- Every seed cryptographically signed and lineage-recorded.

These constraints preclude any design that assumes hosted inference,
hosted training, hosted storage, or hosted search.

## Decision

Materialize the full-capacity agent as a self-contained module rooted
at `agent/` with the following structure:

    agent/
    ├── manifest.yaml                  # single source of truth
    ├── stages/                        # six deterministic stage modules
    │   ├── _shared.py
    │   ├── stage_0_live_context.py
    │   ├── stage_1_intent_resolution.py
    │   ├── stage_2_code_generation.py
    │   ├── stage_3_deterministic_growth.py
    │   ├── stage_4_validation.py
    │   ├── stage_5_evolution_and_composition.py
    │   └── stage_6_archive_and_sign.py
    ├── sub_agents/                    # eight bounded sub-agents
    │   ├── intent_oracle.py           # LLM, pluggable backend
    │   ├── researcher.py              # LLM, tool layer owner
    │   ├── code_smith.py              # fine-tuned, no tool access
    │   ├── validator.py               # deterministic
    │   ├── evolver.py                 # deterministic
    │   ├── composer.py                # LLM, may_suggest_only
    │   ├── memory_archivist.py        # deterministic
    │   └── sovereign_signer.py        # deterministic, RFC 6979
    ├── tools/                         # eight optional tools
    │   ├── web_search.py
    │   ├── browse_page.py
    │   ├── code_execution.py          # Wasm sandbox
    │   ├── seed_inventory_query.py
    │   ├── evolution_run.py
    │   ├── fetch_real_world_data.py
    │   ├── multimodal_analyze.py
    │   └── self_fine_tune_trigger.py
    ├── bootstrap/
    │   └── loop.py                    # self-bootstrapping closed loop
    ├── fine_tune/
    │   ├── qlora_recipe.yaml          # QLoRA 4-bit via Unsloth
    │   └── eval_harness.py            # 4-metric promotion gate
    └── airgap/
        └── __init__.py                # air-gap enforcement

The manifest declares the substrate libraries the agent may reference
(all 17 `seed_commons.libraries.*@v1` modules materialized from Round
4 Briefs 082-094), the stage ownership graph, the sub-agent backends,
the tool providers, the bootstrap-loop parameters, and the sovereignty
contract.

### Trust boundaries

- **Raw prompt never reaches CodeSmith.** Only the sanitized
  `IntentEnvelope` produced by Stage 1 crosses the Stage 1 → Stage 2
  boundary. Live-context records are attached to the envelope as
  typed, hashed fields — never as raw bytes.
- **Tool access is bounded per sub-agent.** Only the Researcher can
  invoke web_search, browse_page, fetch_real_world_data, and
  multimodal_analyze. CodeSmith has zero tool access.
- **Air-gap mode is the default.** `GSPL_AIR_GAP=1` is assumed unless
  explicitly disabled; every network-touching tool short-circuits.
- **Sovereignty gene is immutable.** CodeSmith's purity contract
  rejects any emission that mutates the sovereignty gene.

### Determinism

- Stage 3's RNG seed is `SHA-256("gspl.stage3:" || intent_id)`.
- Stage 6 uses ECDSA-P256 with RFC 6979 deterministic nonces.
- The bootstrap loop's per-cycle RNG seed is
  `SHA-256("gspl.bootstrap:" || manifest_version || cycle_index)`.
- Fine-tune recipe pins `seed = 0` for optimizer and data loader.

### Fine-tune path

QLoRA 4-bit via Unsloth against any open-weights base model listed in
the manifest. Single 24 GB GPU suffices for 7B/13B bases, single
80 GB H100 for 70B. Promotion requires all four canonical metrics
(stage_4_first_try_pass_rate, jcs_round_trip_byte_identity,
lineage_closure_rate, refusal_calibration) to reach 0.995.

## Consequences

### Positive

- A single `agent/` directory is the complete, runnable contract for
  the full-capacity agent. Forks drop in, set their preferred LLM
  backend, and go.
- Air-gap operators have a signed, reproducible pipeline with zero
  external dependencies.
- Every seed produced by the agent carries a full lineage ledger
  referencing the 17 substrate libraries, so every claim the agent
  makes is traceable to source.
- Two independent operators running the same recipe against the same
  data mix converge on byte-identical eval metrics, enabling
  decentralized adapter federation.

### Negative

- Stage modules use typed `raise NotImplementedError` stubs where the
  runtime binding plugs in. Consumers of this repo must link the
  kernel, the Wasm sandbox, and a chosen LLM backend before the
  pipeline is executable. This is deliberate: we ship the contract,
  not a bundled runtime.
- QLoRA on 70B requires an 80 GB GPU, which is not quite consumer
  hardware. Operators without one should choose a 7B/13B base; the
  pipeline is base-model agnostic.
- The self-bootstrapping loop produces a large corpus over time. The
  manifest caps per-cycle additions, but operators should budget disk
  accordingly.

### Neutral

- The sovereignty contract forbids claims of human authorship on
  agent-produced seeds. This is consistent with existing project
  sovereignty invariants but should be clearly documented for
  contributors.

## Alternatives considered

1. **Single monolithic agent module.** Rejected — no clear trust
   boundaries between tool-using and tool-free sub-agents, making
   CodeSmith's purity contract unenforceable.
2. **Hosted LLM backend as default.** Rejected — violates the "no
   cloud dependency" constraint. Operators may plug in a hosted
   backend if they wish, but the default must be a local one.
3. **Full training from scratch instead of QLoRA.** Rejected —
   pre-training a competitive base model is outside the hardware
   budget of the target operator.
4. **Skip the bootstrap loop and train CodeSmith once.** Rejected —
   foreclosed iterative improvement and locked operators into a
   static CodeSmith adapter forever.

## References

- `intelligence/gspl-agent-full-capacity.md`
- `intelligence/tool-layer.md`
- `intelligence/self-bootstrapping-loop.md`
- `intelligence/local-fine-tune.md`
- `intelligence/data-sources.yaml`
- `agent/manifest.yaml`
- ADR 0009 — Content-address hashing with JCS + SHA-256
- Round 4 Library Briefs 082-094 materializations in
  `seed_commons/libraries/`
