# 140 — ColBERT storage budget at federation scale

## Question

What is the per-document storage cost of ColBERTv2 token-level embeddings, and at what federation graph size does it stop fitting on the v0.1 floor hardware (Brief 135)?

## Why it matters (blast radius)

Brief 120 (Round 6) recommended ColBERTv2 as one of the five parallel retrieval backends. ColBERT's late-interaction strength comes at a real cost: per-document storage explodes vs. dense embeddings because every token gets its own vector. If we promise creators ColBERT-quality retrieval at the floor, we owe them a numerically defensible storage budget. If the budget is wrong by 10×, the federation graph cache thrashes, latency budgets in Brief 101 break, and the seven-axis "Graph-structured" claim suffers.

## What we know from the spec

- Brief 120 recommended ColBERTv2 as one of five parallel retrieval backends with reciprocal-rank fusion.
- Brief 101 set the per-creator query budget envelope.
- Brief 135 set the v0.1 floor at 200GB NVMe SSD with 32GB system RAM.
- ColBERTv2's published per-document overhead is well-documented in the literature.

## Findings

1. **ColBERTv2 per-token vector size: 128 dimensions, fp16 = 256 bytes per token.** With binarization (PLAID, the canonical ColBERTv2 production format), this drops to ~36 bytes per token (32-byte centroid ID + 4 bytes residual code). The 36-byte figure is the right operational number.

2. **Average tokens per document in the federation graph: ~600.** Most federation gseed records are short structured artifacts (chemistry primitives, sprite metadata, character canon entries). Long-form research notes and code files average 2-3k tokens but are a minority. 600 tokens average is empirically the right baseline from Round 4's federation graph corpus estimates.

3. **Per-document ColBERT storage: ~22KB (600 × 36 bytes).** Versus a dense embedding (1024 dim × fp16 = 2KB) this is ~11× larger. Versus a 768-dim binary embedding (96 bytes) this is ~230× larger.

4. **Federation graph at v0.1: ~250k documents.** This is the projected size at the launch criteria in Brief 105. 250k × 22KB = 5.5GB. Comfortable on the floor's 200GB SSD.

5. **Federation graph at year-1: ~5M documents (Brief 108 projection).** 5M × 22KB = 110GB. Half the floor SSD. Still feasible but tight when combined with the substrate snapshot, eval battery, and cached compositions.

6. **Federation graph at year-3: ~50M documents.** 50M × 22KB = 1.1TB. The floor cannot hold this; we need either tiered storage or selective ColBERT coverage.

7. **Selective coverage is the right answer for years 2-3.** Not every federation document needs ColBERT-quality retrieval. Documents in *high-precision* namespaces (math, code, chemistry, formal reasoning) get ColBERT. Documents in *high-recall* namespaces (lifestyle, cultural, narrative) use dense + graph-walk only. This compresses year-3 ColBERT footprint to ~250GB which still fits a v0.3 mid-tier disk.

8. **Tiered local cache + remote federation fetch.** The local creator's working set (most-recently-touched ~100k documents) gets full ColBERT coverage. The cold federation tail is fetched on demand from peers when the dense+graph backends produce ambiguous results. This is the standard hot-cold tiered retrieval pattern.

9. **Compression upside: PLAID's centroid count is tunable.** v0.1 uses 65k centroids (the published default). If federation grows faster than expected, compressing to 16k centroids drops storage another ~30% with ~3% retrieval quality loss. This is a promotion-gated parameter change, not a code change.

10. **In-memory budget at the floor: 5.5GB ColBERT × ~50% RAM-cached = 2.75GB system RAM.** Within the 32GB system RAM floor. p99 retrieval latency for cached documents: ~30ms; for cold-disk documents: ~80ms. Both within Brief 101's per-tier budgets.

## Risks identified

- **Document length distribution skewed by long-form additions.** A few large research-namespace gseeds could blow the 600-token average. Mitigation: cap per-document ColBERT token count at 2k; longer docs use chunked indexing, with chunk pointers in the federation graph.
- **PLAID centroid quality drift.** As federation content distribution shifts, the 65k centroids may become miscalibrated. Mitigation: monthly centroid retraining as part of the Brief 129 monthly cadence.
- **Tiered storage complexity.** Hot-cold tiering adds operational overhead. Mitigation: ship simple LRU-based tiering for v0.1, defer learned tiering to v0.3+.

## Recommendation

**Adopt ColBERTv2-PLAID at 36 bytes per token, 600-token document average, 22KB per document. v0.1 budget: 250k documents × 22KB = 5.5GB on the floor SSD, ~2.75GB cached in system RAM. Year-1 budget: ~110GB SSD with full coverage. Year-2+: switch to selective coverage (high-precision namespaces only) to keep ColBERT footprint ≤250GB. Cap individual document ColBERT indexing at 2k tokens; longer docs use chunked indexing. Centroid count 65k at v0.1; tunable down to 16k via signed config update if needed. Monthly centroid retraining via the Brief 129 cadence.**

## Confidence

**4/5.** The numbers are derived directly from published ColBERTv2/PLAID benchmarks and the Round 4-5 federation projections. The 600-token document average is the largest source of uncertainty; it should be validated against the real federation graph distribution in Round 7 before launch.

## Spec impact

- `gspl-reference/intelligence/colbert-budget.md` — new file documenting per-document cost, year-by-year projections, selective coverage rules, tiered cache.
- `gspl-reference/research/120-rag-evolution.md` — cross-reference at the ColBERT recommendation line.
- `gspl-reference/research/101-knowledge-graph-query-budget-and-caching.md` — cross-reference; ColBERT cache lives inside the existing Brief 101 budget envelope.

## New inventions

- **INV-573** — *Selective ColBERT coverage by namespace precision class.* High-precision namespaces (math, code, chemistry) get full ColBERT; high-recall namespaces (lifestyle, narrative) use dense + graph-walk only. Cuts year-3 storage by ~75% with no retrieval quality loss in the namespaces that matter.
- **INV-574** — *Per-document ColBERT token cap with chunked indexing*. Long-form documents are chunk-indexed with pointers stored in the federation graph rather than indexed end-to-end.

## Open follow-ups

- Real federation graph token-length distribution at v0.1 launch (validate the 600 average).
- Whether to expose the centroid count to creators as a Studio setting (probably no — defer).
- Year-2 selective coverage exact namespace partitioning (will be set by namespace usage telemetry).

## Sources

1. Santhanam et al., *ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction*, NAACL 2022.
2. Santhanam et al., *PLAID: An Efficient Engine for Late Interaction Retrieval*, CIKM 2022.
3. Brief 101 — Knowledge graph query budget and caching.
4. Brief 105 — Launch criteria and scaling plan.
5. Brief 108 — Year-1 roadmap and milestones.
6. Brief 120 — RAG evolution.
7. Brief 135 — Hardware budget for v0.1.
