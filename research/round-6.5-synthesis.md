# Round 6.5 — Synthesis: Calibration complete, v0.1 build-ready

## Charter recap

Round 6.5 was a 20-brief mini-round (132–151) with one job: **close the 20 open follow-ups from Round 6** so that Round 7 can start implementation without re-opening any architectural questions. Per `round-6.5-plan.md`, the non-goals were strict — no new substrate primitives, no new commitments, no new axes, no new namespaces, no code. Every brief had to be a *calibration* (X), an *empirical sizing* (Y), a *recipe* (Z), or an *operational* (W) decision grounded in prior briefs.

All twenty briefs are now written. Round 6.5 added **38 new inventions (INV-556 through INV-593)**, bringing the GSPL invention catalog from 246 to **284 total inventions across 151 briefs**.

## What Round 6.5 produced — at a glance

| # | Brief | Tier | Outcome |
|---|---|---|---|
| 132 | Router classifier training data | X | ModernBERT-base 200M, 50k cold-start corpus, daily retrain, ECE ≤0.05 |
| 133 | LATS value function: handcrafted vs learned | X | Composed `V = α·V_symbolic + (1-α)·V_learned`, α from schema verifier fraction |
| 134 | Substrate-native canonical benchmark battery | W | 8 families × ~3000 cases, three cadences, 20% held-out rotated quarterly |
| 135 | Hardware budget v0.1 + context ceiling | Y | Floor 24GB VRAM + 32GB RAM + 200GB NVMe; Qwen3-14B-Thinking int4/int8; 32k context |
| 136 | Deep Research workflow recipe | Z | 5-stage signed pipeline; confidence pills; sanctioned-source allowlist |
| 137 | Multi-modal backbone selection | X | Qwen2.5-VL-3B vision tower mounted on Qwen3-14B; vision.embed primitive tool |
| 138 | Compaction cadence calibration | X | 75% fill / 30min / signed-off triggers; 8:1 ratio default; ≤5s latency |
| 139 | Procedural promotion threshold tuning | X | 4-signal threshold; shape-equivalence on canonical DSL; federation higher-bar |
| 140 | ColBERT storage budget at federation scale | Y | 22KB/doc; v0.1 250k docs = 5.5GB; year-3 selective coverage ≤250GB |
| 141 | Cross-encoder distillation recipe | Z | Distill ModernBERT-base from Qwen3-Reranker-7B; 5M triples; ≥95% teacher BEIR |
| 142 | Grammar compilation performance budget | Y | Precompile ~30 grammars at install; ≤500ms cold-boot load |
| 143 | Differentiable action learning recipe | Z | Creator LoRA + InfoNCE contrastive; collection-only at v0.1; default at v0.4 |
| 144 | Drift detector threshold calibration | X | 3 metric classes, 2σ relative + absolute floors, hourly probe set |
| 145 | GPU-time cost model | Y | ~$3,900/mo on-demand, ~$1,600/mo with spot; year-1 ~$20–33k total |
| 146 | JEPA predictive embedding dataset | Z | Zero-cost lineage-side-effect collection from v0.1; ~5GB at v0.4 |
| 147 | Federation-wide adapter review protocol | W | 3 tiers; 5 automated checks; cross-peer local re-run; signed propagating revocation |
| 148 | World model formalization beyond Brief 131 | X | M = deterministic engine eval; R = composed confidence; v0.5 simulate primitive |
| 149 | v0.1 scope finalization | W | 42 in-scope features; 17 explicit cuts; ~140 of 246 inventions at v0.1 |
| 150 | External benchmark battery selection | W | SWE-bench V, LiveCodeBench, BFCL, MMLU-Pro, ARC-AGI; substrate-uplift framing |
| 151 | Creator-facing seven-axes communication | W | 3-audience messaging; 5 outcome promises; 3 negative promises; Deep Research demo |

## The five consolidated calibration tables

### A. Hardware and compute floor (Briefs 135, 140, 142, 145)

| Resource | v0.1 floor | v0.1 mid | v0.1 ceiling |
|---|---|---|---|
| GPU VRAM | 24 GB | 48 GB | 80 GB |
| System RAM | 32 GB | 64 GB | 128 GB |
| NVMe | 200 GB | 500 GB | 1 TB |
| CPU cores | 8 | 16 | 32 |
| Backbone | Qwen3-14B-Thinking int4 | Qwen3-14B int8 | Qwen3-MoE-A22B int4 |
| Context window | 32k | 128k | 128k |
| ColBERT index | 5.5 GB (250k docs) | 22 GB (1M docs) | 110 GB (5M docs) |
| Grammar cache | ~30 grammars precompiled | ~60 | ~120 |
| Per-PR eval | <60s | <60s | <60s |

### B. Self-improvement cadence costs (Brief 145, all-up)

| Cadence | What runs | Monthly $/creator (on-demand) | Monthly $/creator (spot) |
|---|---|---|---|
| Daily | Router + reranker probe + quality probe | $23 | $9 |
| Weekly | LoRA DPO + full canonical battery | $580 | $232 |
| Monthly | Verifier training + reranker distillation + centroid retraining | $3,200 | $1,280 |
| Quarterly | Council + multi-judge constitutional benchmark + held-out rotation | $85 | $34 |
| **Total** | | **~$3,900** | **~$1,600** |

Year-1 federation total: ~$20–33k. Sublinear scaling: doubling creators only adds ~30% to monthly cost because daily/weekly tasks are amortized across the federation.

### C. Quality, calibration, and latency thresholds

| Metric | Threshold | Source |
|---|---|---|
| Router macro-F1 | ≥0.85 | Brief 132 |
| Router ECE | ≤0.05 | Brief 132 |
| Cross-encoder distillation BEIR | ≥95% of teacher | Brief 141 |
| Procedural promotion repetition | ≥3 | Brief 139 |
| Procedural promotion acceptance | ≥0.8 | Brief 139 |
| Procedural promotion grounding | ≥0.85 | Brief 139 |
| Procedural promotion constitutional | =1.0 | Brief 139 |
| Drift detector quality | within 2σ relative + absolute floor | Brief 144 |
| Drift detector calibration ECE drift | ≤0.02 | Brief 144 |
| Drift detector latency | ≤1.2× floor budget | Brief 144 |
| Compaction latency | ≤5s | Brief 138 |
| Grammar cold-boot load | ≤500ms | Brief 142 |
| Constitutional benchmark family | =100% pass | Brief 134 |
| Held-out canonical regression | <2σ on any family | Brief 134 |

### D. v0.1 evaluation posture (Briefs 134, 150)

| Suite | Cadence | Scope | Reporting position |
|---|---|---|---|
| Canonical battery (substrate-native) | per-PR fast / weekly full / monthly + held-out | 8 families × 3000 cases | **Leads release notes (the moat)** |
| External benchmark suite | monthly | SWE-bench V, LiveCodeBench, BFCL, MMLU-Pro, ARC-AGI | Follows canonical (the parity, substrate-uplift framing) |

External target table (substrate uplift over bare backbone, not frontier ceiling):

| Benchmark | Backbone-only | GSPL v0.1 target |
|---|---|---|
| SWE-bench Verified | ~35% | ≥48% |
| LiveCodeBench | ~45% | ≥52% |
| BFCL avg | ~80% | ≥90% |
| MMLU-Pro | ~62% | ≥66% |
| ARC-AGI public | ~12% | ≥18% |

### E. v0.1 scope summary (Brief 149)

- **42 in-scope features** spanning substrate (8), content (6), operations (7), intelligence (21).
- **17 explicit cuts** to v0.2+ — audio, video, multi-agent topologies, JEPA training enabled, world_model.simulate, long-context default, A22B default, federation peer pool >1, creator tiers 2/3, mobile, multiplayer, all sim engines, hand-drawn variants, AMD/Intel first-class, self-improving language for the kernel itself.
- **~140 of 246 inventions implemented** at v0.1; the rest are v0.2+.

## What we now know that we did not at the end of Round 6

1. **The router classifier is fully specified.** Architecture (ModernBERT-base 200M), heads (17-way namespace + 5-way strategy), training corpus sources (seed armory + composition graph + federation snapshots), update cadence (daily), quality bars (Brief 132).

2. **The LATS value function is fully specified.** Composed neural+symbolic with α derived from gseed schema verifier-annotation fraction; learned head training corpus and cadence pinned (Brief 133).

3. **The benchmark posture is fully specified.** Substrate-native canonical battery as the moat measurement; five external benchmarks as the parity measurement; substrate-uplift framing; dual-reporting at every release with canonical battery leading (Briefs 134, 150).

4. **The hardware floor is signed.** v0.1 ships at 24GB VRAM + 32GB RAM + 200GB NVMe + 8-core CPU minimum, with full latency budget table per battery mode (Brief 135).

5. **The Deep Research workflow is fully specified as the v0.1 headline plugin.** 5-stage signed pipeline, confidence pills, sanctioned-source allowlist, integrates all seven axes in one creator-visible loop (Brief 136).

6. **The vision tower decision is signed.** Qwen2.5-VL-3B mounted on Qwen3-14B as a vision.embed primitive tool; audio defers to v0.2 (Brief 137).

7. **Compaction cadence is calibrated.** Three triggers, 8:1 ratio, ≤5s latency, integrated with Brief 127 four-tier memory (Brief 138).

8. **Procedural promotion threshold is calibrated.** Four-signal gate, shape-equivalence canonicalization, federation higher-bar (Brief 139).

9. **Federation storage budget is sized.** ColBERT-PLAID at 22KB/doc; v0.1 federation ≤6GB; year-3 selective coverage ≤250GB (Brief 140).

10. **Cross-encoder distillation recipe is fully specified.** Teacher Qwen3-Reranker-7B → student ModernBERT-base, monthly cadence, quality bar ≥95% teacher (Brief 141).

11. **Grammar compilation budget is sized.** Precompile at install; ≤500ms cold-boot at floor (Brief 142).

12. **Differentiable action learning recipe is fully specified.** Creator LoRA + InfoNCE; collection-only at v0.1; default at v0.4 (Brief 143).

13. **Drift detector thresholds are calibrated.** Three metric classes, hourly continuous detection, freeze-after-two-rollbacks (Brief 144).

14. **The cost model is signed.** ~$3,900/mo on-demand or ~$1,600/mo with spot, sublinear scaling (Brief 145).

15. **JEPA dataset construction recipe is fully specified.** Zero-cost lineage side effect collection at v0.1, three pair sources, ~5GB at v0.4 (Brief 146).

16. **The federation adapter review protocol is fully specified.** Three tiers, five automated checks, cross-peer local re-run, signed propagating revocation, federation-trust scoring (Brief 147).

17. **The world model claim is formalized.** State = signed typed gseeds; M = deterministic engine eval; R = composed confidence; three differences from learned world models; v0.5 ships world_model.simulate primitive tool (Brief 148).

18. **v0.1 scope is locked.** 42 in-scope features, 17 explicit cuts, signed as `scope-v0.1://canonical/v1` (Brief 149).

19. **The external benchmark suite is committed.** Five benchmarks, target table, dual-reporting, monthly cadence (Brief 150).

20. **The creator-facing message is written.** Three-audience structure, five outcome promises, three negative promises, Deep Research as headline demo (Brief 151).

## v0.1 build-ready statement

**As of the end of Round 6.5, every architectural question required to begin implementation of GSPL v0.1 has a signed answer in a numbered brief. The v0.1 scope is frozen at 42 features and 17 explicit cuts. The hardware floor is signed. The cost model is signed. The benchmark posture is signed. The seven structural axes — Signed, Typed, Lineage-tracked, Graph-structured, Confidence-bearing, Rollback-able, Differentiable — each have at least one operational implementation brief. The creator-facing message is written. Round 7 can start implementation without re-opening any of the twenty Round 6 follow-ups.**

The remaining unknowns are *empirical*, not *architectural*: actual SWE-bench substrate uplift, actual creator response to outcome-first messaging, actual JEPA pair quality at v0.4, actual cost variance vs the model. These are answered by *running* the system, not by writing more briefs.

## Round 6.5 inventions catalog (INV-556 → INV-593)

| INV | Name | Brief |
|---|---|---|
| 556 | Lineage-derived strategy labels | 132 |
| 557 | Constitution-violating-then-correcting training pairs | 132 |
| 558 | Composed neural-symbolic value function with schema-derived α | 133 |
| 559 | Verifier memoization across LATS rollouts | 133 |
| 560 | Eight-family substrate-native benchmark battery | 134 |
| 561 | Three-cadence eval (per-PR fast / weekly full / monthly held-out) | 134 |
| 562 | Quarterly held-out 20% rotation | 134 |
| 563 | Battery mode degradation envelope | 135 |
| 564 | Five-stage signed Deep Research pipeline | 136 |
| 565 | Confidence pill display surface (high/medium/low/disputed) | 136 |
| 566 | Sanctioned-source allowlist with creator-extensible additions | 136 |
| 567 | Vision-tower-as-primitive-tool decoupling | 137 |
| 568 | Three-trigger compaction (fill / time / signed-off) | 138 |
| 569 | Per-namespace compaction ratio override | 138 |
| 570 | Four-signal procedural promotion threshold | 139 |
| 571 | Shape-equivalence canonicalization for repetition counting | 139 |
| 572 | Federation-tier higher-bar promotion gate | 139 |
| 573 | ColBERT-PLAID 22KB/doc at federation scale | 140 |
| 574 | Selective-coverage federation index for year-3+ | 140 |
| 575 | Cross-encoder distillation Qwen3-Reranker-7B → ModernBERT-base | 141 |
| 576 | Vocab-hashed precompiled grammar cache | 142 |
| 577 | InfoNCE outcome-class contrastive action LoRA | 143 |
| 578 | Collection-only-then-default action learning gate | 143 |
| 579 | Three-class drift metric framework | 144 |
| 580 | Hourly continuous drift detection on creator-local probe | 144 |
| 581 | Freeze-after-two-rollbacks circuit breaker | 144 |
| 582 | Zero-cost JEPA pair collection as lineage side effect | 146 |
| 583 | Three-source JEPA pair construction (lineage / cross-modal / cross-namespace) | 146 |
| 584 | Three-tier adapter review protocol | 147 |
| 585 | Sandbox-first adapter install with shadow evaluation | 147 |
| 586 | Signed propagating revocation gseed | 147 |
| 587 | Federation-trust scoring (informational) | 147 |
| 588 | Formal substrate-as-world-model definition | 148 |
| 589 | `world_model.simulate` primitive tool (v0.5) | 148 |
| 590 | Substrate-uplift reporting over bare-backbone baseline | 150 |
| 591 | Three-audience messaging structure | 151 |
| 592 | Vocabulary-by-use onboarding | 151 |
| 593 | Three explicit negative promises | 151 |

**Total: 38 inventions across 20 briefs.**

## Cumulative GSPL totals (end of Round 6.5)

| Round | Briefs | Inventions | Theme |
|---|---|---|---|
| 1 | 1–12 | 1–58 | Substrate primitives |
| 2 | 13–60 | 59–185 | Substrate engineering |
| 3 | 61–67 | 186–202 | Federation primitives |
| 4 | 68–84 | 203–225 | Substrate content |
| 5 | 85–108 | 226–245 | Operations and economics |
| 6 | 109–131 | 246–555 | Intelligence layer + seven-axis claim |
| 6.5 | 132–151 | 556–593 | Calibration close-out |
| **TOTAL** | **151** | **593** | |

(Note: Round 6 invention numbering ran 246–555 across 23 briefs, accounting for the larger surface area of the intelligence layer.)

## What Round 7 inherits

A signed, calibrated, evaluable, costed, scope-frozen v0.1 specification across 151 briefs and ~140 implementable inventions. Every line item Round 7 builds is traceable to a numbered brief; every brief is grounded in either the seven structural axes, the constitutional fence, or a calibrated empirical decision. The substrate is ready to be built.

## Sources

- Round 6 synthesis (`round-6-synthesis.md`)
- Round 6.5 plan (`round-6.5-plan.md`)
- Briefs 132–151
