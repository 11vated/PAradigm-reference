# 129 — GSPL self-improvement and evolution loop (Tier W integration)

## Question

How does GSPL run a continuous self-improvement loop on its own substrate data that compounds creator value every cycle, without drift and without violating the constitutional commitments?

## Why it matters (blast radius)

Self-improvement is the compounding lever. A system that gets measurably better every week from its own usage dominates every system that only improves when a closed lab releases a new model. GSPL is the only agentic platform with a signed, lineage-bearing substrate as its training signal source.

## What we know from prior briefs

- **040:** refinement loop with critics + RL committed.
- **113:** SFT → DPO/IPO → RFT recipe with constitutional critics.
- **119:** tiered self-improvement cadence (daily/weekly/monthly/quarterly); substrate as only ground truth; constitutional fence load-bearing; rollback-by-default.
- **115:** evaluator-optimizer pattern.
- **122:** Qwen's public recipes validate the training pipeline.
- **125:** Devin's failure mode: long-horizon autonomy is about recovery, not execution.

## Architecture

### The five signal sources (free training data)

1. **Graph-verified reasoning traces.** Every reasoning step that was audited against the graph and passed is a positive example. Every trace that failed is a negative.
2. **Constitutional-violated outputs.** Every output that the constitutional check rejected is a labeled negative.
3. **Signed creator overrides.** When a creator edits, rejects, or accepts a proposal, that's a preference label.
4. **Signed forks.** A fork signals "this was useful." A branch that never gets forked signals the opposite.
5. **Refusals and creator responses to refusals.** When a refusal is accepted, the boundary is correct. When overridden, the boundary needs tuning.

All five are structurally free: the substrate produces them as a side effect of normal operation.

### The four cadences

#### Daily (hot path)

- **Router updates:** the namespace router (Brief 126 Layer 2) retrains on the last 24 hours of task-strategy pairs.
- **Retrieval reranker:** the cross-encoder reranker (Brief 127) retrains on yesterday's clicked-through candidates.
- **Planner strategy weights:** the strategy classifier adjusts based on yesterday's success rates.

All updates are tiny, in-memory, and do NOT touch the backbone weights. Rollback is trivial (revert the classifier state).

#### Weekly

- **LoRA adapter training (iterative DPO).** A fresh LoRA adapter is trained on the week's signed preference pairs. The adapter is rank 8–16, targets attention and MLP projections, and is scoped to a namespace.
- **Held-out constitutional benchmark** runs before promotion.
- **Promotion is signed.** The new adapter is a signed gseed in `adapter://<creator>/<namespace>/<date>/`.
- **Rollback** is one operation: revert to the previous adapter.

#### Monthly

- **Verifier training on graph-audited traces.** The process reward model (Brief 109) retrains on the month's grounding-audited reasoning traces.
- **Full constitutional benchmark pass** with multi-judge ensemble.
- **Consultancy review** for any sensitive-namespace adapter (Brief 099).
- **Promotion is signed.**

#### Quarterly

- **Full retrospective (Brief 108).** The council (Brief 107) reviews drift, alignment, and creator outcomes.
- **Adapter reset if drift detected.** Baseline adapters can be re-promoted if the current ones have drifted.
- **Constitutional commitment review.** No changes to the 13 non-amendable commitments; only clarifications and documentation updates.
- **Public improvement log published** as a signed gseed.

### The constitutional fence

No adapter promotes unless it:
- Passes the held-out constitutional benchmark with score ≥ baseline.
- Does not reduce grounding floor coverage on any namespace.
- Does not degrade refusal quality on constitutional categories.
- Passes the identity metric (Brief 096) for drift detection.
- Has a rollback path at least as clean as the prior adapter.

### The drift detector

A continuous background job runs against a held-out set of canonical queries. If any of:
- Response style drifts more than a calibrated threshold.
- Grounding coverage drops below baseline.
- Refusal patterns change without justification.
- Creative outputs lose diversity (measured by identity metric variance).

...then the most recent adapter is auto-rolled back, and the council (Brief 107) is notified.

### The rollback primitive

Every adapter is a signed gseed. Rollback is:
1. Mark the current adapter's `current` pointer as rolled back.
2. Update the pointer to the prior adapter.
3. Sign the rollback event.

One operation. Brief 105 handles the substrate mechanics.

### LoRA adapters at every tier

v1 uses LoRA adapters exclusively. Full fine-tunes are rare and reserved for monthly verifier training. This is the "LoRA-only by default" discipline from Brief 119.

Adapter composition:
- **Base backbone** (Qwen3-MoE-A22B or equivalent).
- **Namespace adapter** (per creator namespace, weekly).
- **Creator personalization adapter** (per creator, rare).
- **Task-specific adapter** (code, writing, math, etc., monthly).

At inference, the router selects the active adapters and the kernel composes them.

### The public improvement log

Every promotion is signed and published to `improvement-log://` as a lineage-only gseed. The log includes:
- What changed (adapter, dataset, metric).
- Benchmarks before and after.
- Rollback path.
- Council review if applicable.

Creators can inspect, audit, and (via federation) replicate improvements on their own adapters.

## Inventions (INV-527 through INV-537)

- **INV-527:** five-signal training data sourcing from substrate-native events.
- **INV-528:** four-cadence improvement loop (daily/weekly/monthly/quarterly).
- **INV-529:** daily hot-path updates to router, reranker, and strategy classifier without touching backbone.
- **INV-530:** weekly LoRA DPO with held-out constitutional benchmark gate.
- **INV-531:** monthly verifier training with multi-judge ensemble.
- **INV-532:** quarterly retrospective with council review and public log.
- **INV-533:** constitutional fence as promotion gate (five criteria).
- **INV-534:** continuous drift detector with auto-rollback.
- **INV-535:** adapter://<creator>/<namespace>/<date>/ as signed adapter namespace.
- **INV-536:** composed adapter stack (base + namespace + creator + task).
- **INV-537:** improvement-log:// as public signed gseed lineage for every promotion.

## What makes this unsurpassable

1. **Free training signal.** Every creator action produces labeled data automatically.
2. **Substrate as ground truth.** No human labelers; graph audits are the reward.
3. **Constitutional fence.** Every promotion is gated by non-amendable commitments.
4. **Rollback at every tier.** Any adapter can be reverted in one operation.
5. **Creator-private by default.** Federation is opt-in; personal adapters never leak.
6. **Public improvement log.** Transparency builds trust; replication builds community.
7. **Tiered cadence.** Daily wins compound; weekly wins are rollbackable; monthly wins are audited.
8. **Drift detector is structural.** The constitutional check IS the drift signal.
9. **No closed lab can match** because no closed lab has signed substrate as a signal source.

## Risks identified

- **Reward hacking on graph audit.** Mitigation: held-out audit set; multi-judge ensemble; periodic human spot-check via consultancy (Brief 099).
- **Diversity collapse.** Mitigation: creative-namespace adapters use diversity-preserving objectives (KTO with diversity reg, Brief 113); identity metric (Brief 096) monitors variance.
- **Consultancy bottleneck.** Mitigation: consultancy review is only for sensitive namespaces; most adapters ship without review.
- **Rollback complexity.** Mitigation: adapter stack is flat; each layer rollbacks independently.
- **Silent drift.** Mitigation: continuous drift detector with auto-rollback.
- **Training cost at monthly/quarterly cadence.** Mitigation: LoRA-only default; full fine-tunes rare; GPU budget is explicit in Brief 106 tier economics.
- **Creator-private adapter leakage.** Mitigation: adapters are signed in creator namespace; federation requires explicit creator action.
- **Federation-wide bad adapter.** Mitigation: federated adapters pass the same constitutional benchmark before subscribers accept them; subscribers can reject.

## Recommendation

1. **Ship the daily cadence in v0.1** — router and reranker updates, in-memory, rollback-trivial.
2. **Ship the weekly cadence in v0.2** — LoRA DPO with constitutional benchmark gate.
3. **Ship the monthly cadence in v0.3** — verifier training with multi-judge ensemble.
4. **Ship the quarterly cadence in v0.3** aligned with Brief 108's retrospective.
5. **Constitutional fence is load-bearing from v0.1.** Every promotion passes the benchmark.
6. **Drift detector is live from v0.1.**
7. **Public improvement log is live from v0.2.**
8. **Consultancy review budget is explicit in Brief 099.**

## Confidence

**4.0/5.** The individual techniques (iterative DPO, RFT, verifier training) are mature. The substrate-native signal sourcing is novel but mechanically straightforward. The 3.5/5 pieces are:
- Operational load for a solo founder at monthly+quarterly cadence.
- Empirical drift detector calibration.
- Training budget at scale.

Mitigations: LoRA-only default, strict rollback discipline, and weekly cadence as the primary lever (monthly/quarterly can defer if budget is tight).

## Spec impact

- Brief 040 needs the substrate-as-signal amendment.
- Brief 105 needs the adapter rollback protocol.
- Brief 106 needs the GPU budget tier breakdown.
- Brief 108 integrates with the quarterly cadence.
- Brief 113 confirms the training recipe.
- Brief 129 this brief completes.

## Open follow-ups

- Weekly/monthly adapter training budget (GPU-time cost model).
- Drift detector threshold calibration.
- Adapter composition ordering at inference.
- Federation-wide adapter review protocol.

## Sources

Briefs 040, 108, 109, 113, 115, 119, 122, and their cited sources.
