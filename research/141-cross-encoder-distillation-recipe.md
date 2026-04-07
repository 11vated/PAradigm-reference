# 141 — Cross-encoder distillation recipe

## Question

How do we train a small (100-300M) cross-encoder reranker that runs inside the v0.1 floor latency budget (Brief 135) and matches the ranking quality of state-of-the-art 1B+ rerankers?

## Why it matters (blast radius)

Brief 120 places the cross-encoder reranker on the grounding-floor path: every retrieval that feeds a Brief 097 grounded claim passes through it. If it is too slow, latency budgets break. If it is too weak, the grounding floor degrades and the seven-axis "Confidence-bearing" claim weakens. This is a single load-bearing model whose quality determines whether GSPL retrieval beats hosted competitors at the floor hardware.

## What we know from the spec

- Brief 120 specifies a cross-encoder reranker as the second-pass after the five parallel retrieval backends.
- Brief 135 budgets the reranker at 300M params, 600MB VRAM, 80ms p50 / 200ms p99 latency at the floor.
- No brief has yet specified the training recipe.

## Findings

1. **Distillation target: a 7B reranker.** The current open-weight ceiling is BGE-reranker-v2-gemma (7B) and Qwen3-Reranker-7B. Both publish strong scores on BEIR, MTEB, and TREC-DL. The student inherits behavior from these teachers via score distillation.

2. **Student architecture: ModernBERT-base or DeBERTa-v3-large.** ModernBERT-base (149M params) is the leading 2024 small encoder; DeBERTa-v3-large (435M) is slightly larger but not yet over the floor budget. Both outperform older base-class models on retrieval reranking by ~5 points on BEIR. ModernBERT-base is the recommended student because it fits the 300M budget with headroom.

3. **Training data: 5M (query, passage, score) triples from federation graph + public datasets.** Sources: (a) MS-MARCO (already in the public benchmark battery), (b) BEIR (multi-domain), (c) the GSPL federation graph itself — every parent edge in the graph is implicitly a positive (query, document, 1.0) pair, and Brief 091's contradiction nodes provide negatives. Mixing in-distribution (federation) with out-of-distribution (MS-MARCO/BEIR) produces a generalist reranker that does not over-fit to GSPL-specific patterns.

4. **Distillation loss: KL divergence over teacher logits + listwise margin loss.** KL captures the teacher's full score distribution; listwise margin loss preserves the teacher's *ranking* even when absolute scores diverge. Standard practice from ColBERT and BGE distillation papers.

5. **Hard-negative mining is mandatory.** Random negatives are too easy. We mine hard negatives by retrieving top-50 documents with a dense baseline and labeling all non-positive top-50 as hard negatives. This is the same procedure used in ColBERTv2 and DPR.

6. **Training compute budget: ~80 GPU-hours on 8×A100.** For a 150M ModernBERT distilled from a 7B teacher on 5M triples, 5 epochs at batch 64. This is one-day-on-rented-cluster, well within the Brief 145 monthly cadence budget.

7. **Latency at the floor: ModernBERT-base at int8, batch of 50 candidates: ~60ms p50, 150ms p99.** Within Brief 135's 80/200ms budget. The 50-candidate batch is the standard rerank cohort size from Brief 120.

8. **Quality target: ≥95% of teacher BEIR average.** Distillation typically retains 95-98% of teacher quality at 1/40th the size when done well. The 95% floor is the promotion gate — any retrained reranker must clear it on a held-out BEIR slice plus a held-out federation slice.

9. **Monthly retrain cadence.** Per Brief 129, the reranker retrains monthly as part of the verifier-training cadence. The training corpus is updated each month with the previous month's federation additions and accepted/rejected retrieval traces.

10. **Reranker is itself a signed gseed at `model://gspl/cross-encoder-reranker/v1`.** Each monthly retrain produces a signed child with parent edge to the previous version. Promotion gate: must clear ≥95% teacher BEIR + ≥0.85 federation slice nDCG@10, otherwise auto-rollback (Brief 144 cross-reference).

## Risks identified

- **Teacher availability/license.** BGE-reranker-v2-gemma is Gemma-licensed; Qwen3-Reranker-7B is Apache 2.0. Mitigation: prefer Qwen3 to keep license stack uniform.
- **In-distribution vs out-of-distribution mix ratio.** Too much MS-MARCO and the reranker over-fits to news-style queries; too much federation and it under-generalizes. Mitigation: 60/40 federation/public mix at v0.1; tune monthly.
- **Hard-negative mining noise.** Some "hard negatives" are actually correct alternative answers. Mitigation: filter mined negatives with the teacher itself — only keep mined negatives the teacher scores below 0.3.

## Recommendation

**Distill ModernBERT-base (149M) from Qwen3-Reranker-7B as the v0.1 cross-encoder reranker. Training corpus: 5M triples mixing 60% federation graph + 40% MS-MARCO/BEIR. Loss: KL on teacher logits + listwise margin. Hard-negative mining via teacher-filtered top-50 dense retrieval. Training: ~80 GPU-hours on 8×A100, monthly cadence aligned with Brief 129. Promotion gate: ≥95% teacher BEIR average AND ≥0.85 federation slice nDCG@10. Latency at floor: int8 quantized, 60ms p50 / 150ms p99 on a 50-candidate batch. Reranker stored as `model://gspl/cross-encoder-reranker/v1` signed gseed with rollback.**

## Confidence

**4/5.** Distillation is well-established; the recipe is standard. The unknowns are: (a) whether the federation slice has enough volume for nDCG@10 to be stable (defer to Round 7 measurement), and (b) whether ModernBERT-base or a slightly larger DeBERTa-v3-large is the better student empirically.

## Spec impact

- `gspl-reference/intelligence/cross-encoder-recipe.md` — new file with the full distillation recipe, training corpus composition, hard-negative mining protocol, promotion gate.
- `gspl-reference/research/120-rag-evolution.md` — cross-reference at the cross-encoder line.
- `gspl-reference/research/129-gspl-self-improvement-loop.md` — cross-reference at the monthly verifier training cadence.

## New inventions

- **INV-575** — *60/40 federation-public training mix for the GSPL cross-encoder.* Balances generalist out-of-distribution behavior against in-distribution federation specialization. The mix ratio is itself tunable via signed config gseed.

## Open follow-ups

- ModernBERT-base vs DeBERTa-v3-large empirical comparison (Round 7).
- Federation slice size threshold for stable nDCG@10 measurement.
- Whether to publish the trained reranker openly as a contribution to the open-weight community.

## Sources

1. Santhanam et al., *ColBERTv2*, NAACL 2022 (distillation patterns).
2. Wang et al., *BGE-reranker-v2-gemma*, BAAI 2024.
3. Qwen team, *Qwen3-Reranker Technical Report*, 2024.
4. Warner et al., *ModernBERT*, 2024.
5. Karpukhin et al., *Dense Passage Retrieval (DPR)*, EMNLP 2020 (hard-negative mining).
6. Brief 120 — RAG evolution.
7. Brief 129 — GSPL self-improvement loop.
8. Brief 135 — Hardware budget for v0.1.
