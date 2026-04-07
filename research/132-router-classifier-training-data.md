# 132 — Router classifier training data

## Question

How do we construct a substrate-native training corpus for the namespace-routing classifier (Brief 126, INV-484) so that v0.1 ships with a working router rather than a heuristic stub?

## Why it matters (blast radius)

The router is the entry point to the five-layer reasoning kernel. Every request is classified into a namespace (image, sprite, character, sim, code, math, science, lifestyle, lineage, federation, meta) and a planner strategy (ReAct, ToT, LATS, Reflexion, Self-Refine). If the router misroutes, the wrong strategy and the wrong namespace experts run, the wrong tools get parallel-dispatched, the wrong cross-encoder reranker fires, and the user pays extra latency for a worse answer. Worse, mis-routed traces poison the daily router-update signal in Brief 129. The router is the single most leveraged learned component in v0.1.

## What we know from the spec

- Brief 126 specifies the router as a small classifier (target 100M-300M params) with a namespace head and a strategy head.
- Brief 119 (Round 6) specifies daily router updates as the fastest self-improvement cadence.
- Brief 129 specifies that *graph-verified traces* and *constitutional-violation events* are the free training signals.
- Round 4 fixed the namespace taxonomy at ~17 top-level namespaces (chemistry, physics, materials, biology, mathematics, music, linguistics, culture, built-world, lifestyle, psychology, character, image, sprite, sim, code, lineage; meta is implicit).

What is *not* in the spec: the cold-start training data. The router cannot learn from substrate signals it has not yet generated, so v0.1 needs a bootstrap corpus.

## Findings

1. **Three corpus sources are sufficient for cold start.** (a) The 1,000-seed armory from Brief 095, where every seed already has a known namespace and a known canonical generation strategy. (b) The composition graph nodes from Brief 091, where every node has a typed parent edge identifying its namespace. (c) The federation graph snapshots used by Brief 100, which carry namespace metadata in the header. Together these yield ~12-25k labeled (request, namespace, strategy) triples without any synthetic generation.

2. **Strategy labels are derivable from gseed depth and operator type.** Brief 023's modifier-surface DSL records the operator chain that produced any gseed. A single-pass operator chain with no critic invocation maps to ReAct. A chain with branching maps to ToT. A chain with rollback events maps to LATS. A chain with a self-critique loop maps to Self-Refine. A chain with a Reflexion-style refine-and-resubmit maps to Reflexion. This means strategy labels for the cold-start corpus can be auto-derived from existing lineage data — no human labeling.

3. **Synthetic augmentation closes the long tail.** The natural distribution from sources 1-3 is heavily weighted toward image and sprite (because that's where the seed armory is densest). Lineage-namespace, federation-namespace, and meta-namespace requests are under-represented. We close this with two augmentation tactics: (a) prompt-template paraphrase using a teacher model (Qwen3-Thinking) to generate 5-10 phrasings per existing labeled request, and (b) constitution-violating-then-correcting pairs that exercise the meta-namespace.

4. **The router is small enough to retrain daily on a single 24GB GPU.** A 200M classifier with 50k examples retrains in 6-12 minutes on an RTX 4090 at fp16. Daily cadence (Brief 119) is feasible without dedicated training infrastructure.

5. **Calibration matters more than raw accuracy.** The router emits a confidence score that gates whether the multi-namespace ensemble fires. Brier score and expected calibration error (ECE) are the right primary metrics, not top-1 accuracy. A router that is 90% accurate but well-calibrated outperforms one that is 95% accurate but overconfident, because the 5% misroutes from the latter are confidently wrong and cannot be caught downstream.

6. **Cold-start label noise is bounded by the lineage graph.** Because lineage is signed and content-addressed (Round 1-2), no labeled triple in the cold-start corpus can be silently corrupted. If the daily updater encounters disagreement between the router prediction and the lineage label, the lineage label wins by axiom — this is what makes the substrate self-correcting.

7. **Namespace count of 17 is well within classifier capacity.** Standard text classifiers handle 100+ classes comfortably. The challenge is not class count but class boundary fuzziness — `physics + materials` and `chemistry + materials` overlap, `character + sprite` overlap, etc. The fix is hierarchical heads (top-level namespace + sub-namespace) rather than a flat 100-way head.

8. **The router classifier is itself a signed gseed.** Per Brief 129, every model artifact lives in `model://`. The cold-start router gets a content hash, a signature, and a `confidence-bearing` field. Subsequent daily updates produce signed children with parent-edges in the model lineage graph — rollback (Brief 105) works on routers exactly as it works on any other artifact.

## Risks identified

- **Distribution shift from cold-start to live.** The 1,000-seed corpus skews toward image/sprite. v0.1 production traffic will be different. Mitigation: deploy with high temperature on the strategy head and rely on the daily update cadence to converge within the first week.
- **Strategy label derivation from lineage may be circular.** If the operator chain that produced a gseed used the wrong strategy, the derived label perpetuates the mistake. Mitigation: bootstrap with a small (~500 example) human-reviewed gold set that the auto-derived corpus is calibrated against.
- **Hierarchical head adds complexity.** A single flat head is simpler. Mitigation: ship flat for v0.1, switch to hierarchical only if v0.1 telemetry shows boundary fuzziness > 5% misroute rate.

## Recommendation

**Build the v0.1 router on a 200M-parameter base classifier (DeBERTa-v3-base or ModernBERT-base) with a flat 17-way namespace head and a flat 5-way strategy head. Cold-start corpus: 12-25k labeled triples auto-derived from the seed armory + composition graph + federation snapshots, augmented with paraphrase + constitution-violating pairs to ~50k. Daily retrain cadence on a single consumer GPU. Primary metric: ECE ≤ 0.05 and macro-F1 ≥ 0.85. Calibrated against a 500-example human-reviewed gold set kept in `gold-router-eval://`. Promotion gate: any new daily router must beat the previous on both ECE and gold-set macro-F1, otherwise auto-rollback.**

## Confidence

**4/5.** The corpus construction is straightforward because the substrate already labels everything. The metric choice (ECE + macro-F1) is standard. The unknowns are: (a) whether the auto-derived strategy labels are noisy enough to require >500-example human gold, and (b) whether flat heads suffice or hierarchical is needed. Both are decidable empirically inside Round 7 without re-opening the brief.

## Spec impact

- `gspl-reference/intelligence/router.md` — new file documenting the cold-start corpus construction protocol, the gold set spec, and the daily retrain promotion gate.
- `gspl-reference/research/126-gspl-reasoning-kernel.md` — add cross-reference to this brief at the namespace-router section.
- `gspl-reference/research/129-gspl-self-improvement-loop.md` — add cross-reference at the daily cadence section.

## New inventions

- **INV-556** — *Lineage-derived strategy labels.* Use the modifier-surface DSL operator chain on any gseed to mechanically derive its (ReAct/ToT/LATS/Reflexion/Self-Refine) label. Eliminates human labeling for strategy heads.
- **INV-557** — *Constitution-violating-then-correcting pairs as meta-namespace augmentation.* A signed pair of (request, refused-output, corrected-output) that simultaneously trains the meta-namespace classifier and the constitutional fence detector.

## Open follow-ups

- Whether DeBERTa-v3 or ModernBERT-base is the better base; decide empirically in Round 7.
- The exact size of the gold set (500 is a placeholder, may need 1-2k).
- Whether to share router weights across creators or keep them per-creator (defer to Brief 147).

## Sources

1. Brief 095 — 1,000-seed armory curation plan.
2. Brief 091 — Federated knowledge graph.
3. Brief 100 — Federation peer protocol.
4. Brief 119 — Self-improvement loops (Round 6).
5. Brief 126 — GSPL reasoning kernel.
6. Brief 129 — GSPL self-improvement loop.
7. He et al., *DeBERTa-v3*, 2021.
8. Warner et al., *ModernBERT*, 2024.
9. Guo et al., *On Calibration of Modern Neural Networks*, ICML 2017 (ECE definition).
