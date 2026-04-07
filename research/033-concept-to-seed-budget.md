# 033 — Concept-to-Seed: latency, cost, reliability budget

## Question
What are the latency, cost, and reliability budgets for the Concept-to-Seed path — the user-visible loop from "I want a frosty cyberpunk warrior" to a rendered preview of a valid seed — and how does the architecture meet them?

## Why it matters
Latency is the difference between a tool and a toy. Stable Diffusion at 20 seconds per image is acceptable; at 60 seconds it isn't. The agent path adds layers (planning, schema, validation) that compound. If the budget isn't pinned, every layer takes its share until the loop is unusable.

## What we know from the spec
- Brief 029 defines the eight sub-agents.
- Brief 032 defines the intent normalizer.
- Brief 011 defines the four-layer reliability stack.

## Findings — the budget

### Top-level targets

| Mode | First preview | Full result | Notes |
|---|---|---|---|
| **Interactive (default)** | ≤ 5 seconds | ≤ 15 seconds | First preview is a low-fidelity sketch; full result is the rendered seed |
| **Interactive (complex)** | ≤ 8 seconds | ≤ 30 seconds | Multi-engine compositions, e.g., character + theme music |
| **Autonomous** | N/A | ≤ 60 seconds per seed in a generation | Used for evolutionary loops |
| **Coach mode** | ≤ 2 seconds | N/A | Suggestions only; no execution |

### Per-stage budget (interactive default)

| Stage | Budget | Notes |
|---|---|---|
| Intent normalization | 200 ms | Pure text manipulation; no model call needed if synonym table covers the input |
| Planner (ToT, beam=2 depth=4) | 2.5 s | The dominant cost; model-heavy |
| Schema agent dispatch | 300 ms | Cached most of the time |
| Composer agent | 200 ms | Pattern matching; cached |
| Validator | 100 ms | Local pure function |
| Critic (sketch level) | 800 ms | Fast critic only at preview stage |
| Render preview (low-fidelity) | 700 ms | Engine-dependent; sprite is fast, music is slower |
| **Total to first preview** | **~4.8 s** | Within the 5 s budget |

For full result, add: refinement loop (Brief 040), full-fidelity render, watermarking, signing.

### Cost budget

- **Model token cost per intent**: target ≤ $0.03 for interactive default. Multi-engine compositions can rise to ≤ $0.10.
- **Daily budget per user**: configurable; default $5. Excess triggers cost-aware mode (smaller model, narrower beam).
- **Cost-quality trade-off knob**: the user can choose between "fast & cheap" (smaller beam, fewer critic dimensions) and "slow & deep" (larger beam, full critic suite, longer ToT).

### Reliability budget

- **Validation success on first try**: ≥ 95% of seeds emitted by the agent must pass validation without repair.
- **Validation success after one repair pass**: ≥ 99.5%.
- **Tool-call failure rate**: ≤ 0.5% of tool calls return errors (excluding deliberate validation fails).
- **End-to-end success (concept → valid seed)**: ≥ 99% in interactive default mode.
- **Hallucinated gene names**: 0%. The Schema agent rejects them mechanically (Layer 1 of Brief 011).

### How the architecture meets the budget

1. **Caching**: Every sub-agent caches its outputs by input hash. Schema and Composer hit cache > 80% in steady-state for a given user.
2. **Parallel dispatch**: Planner dispatches Schema and Researcher in parallel where dependencies allow.
3. **Constrained decoding**: The Schema agent uses constrained decoding (Brief 011 Layer 1) so it cannot produce off-schema output, eliminating the largest source of latency variance.
4. **Local-first execution**: The kernel runs locally; only the model calls go to the network. Network round-trip is the largest single cost.
5. **Batched model calls**: When the Planner dispatches multiple sub-agents to the same model, calls are batched.
6. **Streaming previews**: First preview begins rendering before the full plan finishes. The user sees something within ~1.5 s of pressing enter even though the plan continues for another 3 s.

## Risks identified

- **Model latency variance**: a frontier model with a 95th-percentile of 8 seconds blows the budget. Mitigation: pin a model with stable latency; have a smaller fallback model ready (Layer 4 of Brief 011).
- **Budget creep**: every new sub-agent or critic dimension adds latency. Mitigation: budget is pinned in CI as a regression test; PRs that exceed it require explicit waiver.
- **Cost surprise**: a user runs an evolutionary loop and racks up $100. Mitigation: hard cost ceilings per session, surfaced in the UI.
- **Cache invalidation**: a schema change invalidates cached schema-agent outputs. Mitigation: cache keys include the schema version.
- **First-preview-to-full result gap feels jarring**: the low-fi preview is too different from the final. Mitigation: low-fi previews use the same kernel but at a lower render quality, not a different model.

## Recommendation

1. **Adopt the budget table above as normative** in `architecture/agent-budgets.md`.
2. **5 s first preview, 15 s full result** for interactive default.
3. **Per-sub-agent caches** keyed on input hash + schema version.
4. **Constrained decoding everywhere** the structure is known.
5. **Streaming previews** are a hard requirement, not an optimization.
6. **CI regression tests** measure budget adherence on a fixed corpus of intents; PRs that exceed must waive.
7. **Hard cost ceilings per session**, default $5/day.
8. **Cost-quality knob** exposed in the UI.
9. **Reliability targets ≥ 99% end-to-end success** in interactive default.

## Confidence
**3/5.** The budget is achievable on paper given the right model and caching, but unmeasured at GSPL's actual workload. The 3/5 reflects honest uncertainty until benchmarks are run.

## Spec impact

- `architecture/agent-budgets.md` — the budget table.
- `tests/agent-budget-conformance.md` — CI regression suite.
- `algorithms/streaming-preview.md` — pseudocode for the streaming render.
- New ADR: `adr/00NN-agent-budget-pinning.md`.

## Open follow-ups

- Empirically measure first-preview latency on three candidate models in Phase 1.
- Build the CI budget regression suite with a representative intent corpus.
- Define the cost-quality knob's exact preset levels.
- Decide on the fallback model strategy if the primary degrades.

## Sources

- *Designing Data-Intensive Applications* (latency budgeting principles).
- Internal: Briefs 011, 029, 030, 032.
