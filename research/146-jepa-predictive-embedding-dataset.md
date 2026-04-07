# 146 — JEPA predictive embedding dataset construction

## Question

Brief 130 deferred JEPA-style predictive embeddings to v0.4. What is the dataset construction recipe so that the deferral is principled rather than hand-wavy, and so that v0.4 can begin training on day one?

## Why it matters (blast radius)

Brief 130 names JEPA as the v0.4 mechanism for "world-model-as-substrate." If we don't have a dataset construction recipe written down, v0.4 inherits an unbounded research problem. Worse, if we don't begin *collecting* the data starting at v0.1, v0.4 launches with an empty dataset and a multi-month bootstrap delay. The recipe for dataset construction must begin now even though training does not.

## What we know from the spec

- Brief 130 (Round 6) declares JEPA-style predictive embedding deferred to v0.4.
- Brief 131's release arc places JEPA in v0.4 (+12 months).
- Brief 091 specifies the federated knowledge graph as the corpus source.
- LeCun-style JEPA / I-JEPA / V-JEPA papers describe the canonical recipe.

## Findings

1. **JEPA needs (context, target) pairs in an embedding space.** Unlike contrastive learning over raw inputs, JEPA learns to *predict* a target embedding from a context embedding. The dataset is pairs `(context_view, target_view)` of the same underlying gseed in different states, modalities, or partial views.

2. **Three natural pair sources in the GSPL substrate.**
   (a) *Lineage pairs* — every parent→child edge in the composition graph is a `(state_before, state_after)` pair where the child is a transformation of the parent. ~5M pairs at year-1 federation size.
   (b) *Cross-modal pairs* — Brief 089's universal anything-to-gseed pipeline produces `(image, gseed)` and `(text, gseed)` pairs naturally; these are perfect cross-modal JEPA training pairs.
   (c) *Cross-namespace pairs* — Brief 091's federation graph contains nodes that exist in multiple namespaces (e.g., a chemical compound that has both a chemistry-namespace gseed and a materials-namespace gseed). These cross-namespace anchors are the bridge for training a unified embedding space.

3. **Targets and contexts are signed.** Every JEPA training pair carries a `pair-of://<context-id>/<target-id>` lineage entry. This makes the dataset auditable, reversible, and compatible with rollback (Brief 105). If a pair is later determined to be malformed (e.g., the parent edge was wrong), the pair is rolled back and the training corpus snapshot becomes a new signed version.

4. **Collection begins at v0.1.** Every signed gseed produced after v0.1 launch automatically generates the relevant pair entries as a side effect of normal lineage tracking. By v0.4 (12 months later) we expect ~50M lineage pairs, ~10M cross-modal pairs, ~2M cross-namespace pairs. Plenty for JEPA training.

5. **No collection cost beyond what lineage already pays.** Pair entries are derived from existing lineage data, not stored separately. This is zero-marginal-cost data collection — the substrate already produces the data; we just label and index it.

6. **Storage budget for the JEPA dataset index: ~5GB at v0.4.** Each pair is a (parent-id, child-id, relationship-type) triple, ~30 bytes. 50M pairs × 30 bytes = 1.5GB lineage pairs. Cross-modal pairs slightly larger (modality tags add bytes) → ~3GB total. Add federation index → ~5GB. Negligible against the Brief 135 budget.

7. **Quality filtering at training time, not collection time.** Collect everything; filter at training time on `(grounding-floor-passed, constitutional-fence-passed, accepted-not-rolled-back)`. This avoids losing data that might be useful for some training objective even if it failed another.

8. **JEPA target architecture: I-JEPA + V-JEPA hybrid.** I-JEPA for static gseeds (images, materials, sprite frames). V-JEPA for time-evolving gseeds (animation frames, lineage chains, simulation traces). Cross-modal JEPA bridges the two.

9. **Cold-start at v0.4: no creator data, only published seed armory.** The 1,000 canonical seeds (Brief 095) plus their derived gseeds (Brief 088A canonical seed armory) form the cold-start corpus for any new federation peer. ~50k pairs at minimum, enough for a meaningful first training run.

10. **The dataset is itself a signed gseed at `dataset://gspl/jepa-pairs/v1`.** Every quarter, a new snapshot is signed. Models trained on a snapshot record the snapshot version in their lineage, so reproducibility is preserved.

## Risks identified

- **Lineage pair quality varies.** Some parent→child relationships are very loose (a complete rewrite). Mitigation: filter at training time by edit-distance or operator-chain length; use only pairs with semantically meaningful relationships.
- **Cross-modal pair labeling depends on Brief 089's pipeline being mature.** If Brief 089 is half-built at v0.4, the cross-modal pair count is low. Mitigation: prioritize Brief 089 maturity in v0.2-v0.3 (Brief 149 scope).
- **JEPA training compute is large.** A v0.4 JEPA model on 50M pairs is ~500-1000 GPU-hours. Mitigation: this is the v0.4 training cost, not v0.1; absorb into the Brief 145 cost model with a 12-month lead time to budget for it.

## Recommendation

**Begin JEPA pair collection at v0.1 launch as a zero-cost side effect of lineage tracking. Three pair sources: lineage parent→child (composition graph), cross-modal (Brief 089's universal pipeline), cross-namespace (federation graph multi-namespace nodes). Pairs are signed `pair-of://` lineage entries; storage ~5GB at v0.4. Quality filtering happens at training time, not collection. Dataset snapshots quarterly at `dataset://gspl/jepa-pairs/v<n>`. Cold-start corpus for new federation peers is the 1k seed armory plus derived gseeds. v0.4 training: I-JEPA + V-JEPA hybrid, ~500-1000 GPU-hours, budgeted into Brief 145's v0.4 line item with a 12-month lead time.**

## Confidence

**3.5/5.** The collection recipe is sound and zero-cost. The unknowns are at the v0.4 training step: which JEPA variant works best on substrate-typed data, what the exact pair filtering criteria should be, and whether cross-namespace pairs are noisy enough to harm training. These are answerable in the v0.4 build, not earlier.

## Spec impact

- `gspl-reference/intelligence/jepa-dataset.md` — new file with collection recipe, pair sources, storage layout, filtering criteria, snapshot cadence.
- `gspl-reference/research/130-gspl-neurosymbolic-binding.md` — cross-reference at the JEPA deferral line.
- `gspl-reference/research/131-gspl-differentiable-reasoning-substrate.md` — cross-reference at the v0.4 release arc.
- `gspl-reference/research/091-federated-knowledge-graph.md` — note that `pair-of://` lineage entries are added.

## New inventions

- **INV-582** — *Zero-cost JEPA pair collection as lineage side effect.* Every signed lineage edge is also a JEPA training pair. The substrate produces its own pre-training corpus for free.
- **INV-583** — *Three-source JEPA pair construction* (lineage / cross-modal / cross-namespace) producing a unified embedding space across all GSPL content types.

## Open follow-ups

- I-JEPA vs V-JEPA architecture selection at v0.4 (defer).
- Optimal pair filtering criteria (defer).
- Whether the JEPA model itself becomes a kernel embedding-space replacement at v0.5 (per Brief 131 release arc, yes).

## Sources

1. Assran et al., *I-JEPA: Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture*, CVPR 2023.
2. Bardes et al., *V-JEPA: Video Joint Embedding Predictive Architecture*, 2024.
3. LeCun, *A Path Towards Autonomous Machine Intelligence*, 2022.
4. Brief 089 — Universal anything-to-gseed pipeline.
5. Brief 091 — Federated knowledge graph.
6. Brief 130 — GSPL neurosymbolic binding.
7. Brief 131 — GSPL as a differentiable reasoning substrate.
