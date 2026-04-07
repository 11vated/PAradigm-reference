# 120 — Retrieval-augmented generation evolution: GraphRAG, HyDE, Self-RAG, CRAG, RAPTOR, Contextual Retrieval, Late Chunking, ColBERT

## Question

How does GSPL's federated knowledge graph make every published RAG technique a special case of substrate-native retrieval, and which techniques must GSPL absorb explicitly?

## Why it matters (blast radius)

RAG is where grounding lives or dies. Every 2023–2025 RAG advance tried to work around the fact that the underlying store was a flat vector database with no structure, no lineage, and no signed provenance. GSPL's substrate already has the structure every advanced RAG paper reinvents. The question is how to make that explicit and expose the best of the published techniques as first-class substrate retrieval primitives.

## What we know from the spec

- Brief 091 (federated knowledge graph) is content-addressed and typed with 11 edges.
- Brief 090 (web search / external corpora) commits to an external retrieval layer.
- Brief 100 (federation protocol) handles cross-creator sharing.
- Brief 101 (query budget) bounds retrieval depth and candidate counts.
- INV-357 (grounding floor) is enforced on every response.

## Findings

### 1. Naive RAG is already obsolete

Vector search over chunked documents with a top-K retrieval and LLM stuffing was the 2022–2023 baseline. Every serious RAG paper since has shown its failure modes: irrelevant chunks, conflicting chunks, Lost-in-the-Middle, lost context across chunk boundaries, hallucinated citations. [1]

Naive RAG is a floor, not a target.

### 2. HyDE: Hypothetical Document Embeddings

Gao et al. (2022). The model writes a *hypothetical* answer to the query, embeds that, and uses it to retrieve. The hypothetical answer is closer in vector space to real answers than the query itself is. [2]

- **Strengths:** no retrieval model training; works zero-shot; improves recall on hard queries.
- **Weaknesses:** adds a generation step; hypothetical can be wrong and mislead retrieval.

### 3. Self-RAG

Asai et al. (2023). The model is trained to emit special tokens that decide when to retrieve, what to retrieve, and whether retrieved passages are useful. Retrieval becomes a learned decision, not a fixed step. [3]

- **Strengths:** eliminates unnecessary retrieval; improves grounding quality; the model critiques its own retrievals.
- **Weaknesses:** requires fine-tuning; the retrieval-decision tokens are a vocabulary extension.

### 4. CRAG: Corrective RAG

Yan et al. (2024). A lightweight retrieval evaluator scores each retrieved passage and classifies it as correct, incorrect, or ambiguous. Incorrect triggers web search; ambiguous triggers refinement. [4]

- **Strengths:** robust to bad retrieval; the evaluator is cheap; empirically strong.
- **Weaknesses:** the evaluator is another model to train; the decision boundary is fragile.

### 5. RAPTOR: recursive summary tree

Sarthi et al. (2024). Documents are clustered, each cluster is summarized, clusters are re-clustered recursively. Retrieval queries the tree at the level of abstraction the query implies. [5]

- **Strengths:** multi-resolution retrieval; handles long documents; retrieves the right level of detail.
- **Weaknesses:** tree construction is expensive; summaries can hallucinate; updates require re-clustering.

### 6. GraphRAG

Microsoft (2024). Build a knowledge graph from a corpus, cluster the graph into communities, summarize each community, retrieve by community. Global queries traverse the community summaries; local queries walk the graph. [6]

- **Strengths:** captures global corpus structure; handles "what are the themes of this book" queries that flat RAG fails at.
- **Weaknesses:** graph construction is expensive; quality depends on the extraction model; brittle on noisy corpora.

**GSPL-specific:** the federation graph IS the GraphRAG graph, built incrementally from every signed gseed. No construction step. The 11-edge ontology (Brief 100) is the schema. No extraction noise because every edge is signed by a creator.

### 7. Contextual Retrieval

Anthropic (2024). Before embedding, prepend a chunk with a short LLM-generated description of how the chunk fits its source document. Reduces retrieval failure rate by 49% at Anthropic's benchmark. [7]

- **Strengths:** simple, cheap, composable; fixes most chunk-isolation failures.
- **Weaknesses:** requires a generation pass per chunk; doesn't help with cross-document reasoning.

### 8. Late Chunking

Jina AI (2024). Embed the entire document at once, *then* chunk the embeddings. Each chunk's embedding is contextualized by the rest of the document without prepending anything. [8]

- **Strengths:** captures cross-chunk context for free at embedding time; no extra generation cost.
- **Weaknesses:** limited to long-context embedding models; requires one embedding pass over full documents.

### 9. ColBERT and ColBERTv2

Khattab & Zaharia (2020, 2022). Instead of embedding a chunk as one vector, embed every token and use late-interaction (max-sim over token pairs) at retrieval time. Matches cross-encoder quality at bi-encoder cost. [9]

- **Strengths:** the strongest published bi-encoder quality; interpretable (you can see which tokens matched); handles long queries well.
- **Weaknesses:** storage is larger (N vectors per chunk); compression is required; inference is slightly slower.

### 10. DRAGON and diverse augmentation

Lin et al. (2023). Train a dense retriever with diverse augmentations (query rewrites, hard negatives, progressive fine-tuning) to get state-of-the-art zero-shot retrieval. [10]

Feeds directly into retriever training for GSPL's substrate-tuned retriever.

### 11. Matryoshka embeddings

Kusupati et al. (2022). Embeddings are trained so that prefixes of the vector are themselves useful embeddings. Allows dynamic truncation: use 64-dim for coarse filter, 768-dim for final ranking. [11]

- **Strengths:** single embedding serves multiple quality/cost tiers; perfect for Brief 101's budget envelope.
- **Weaknesses:** small quality hit on truncated vectors; requires training the embedding model this way.

### 12. Cross-encoder reranking

Standard pattern: bi-encoder for recall, cross-encoder for precision. The bi-encoder returns top-100; the cross-encoder re-scores all 100 and returns top-10. [12]

This is mandatory for any production RAG system and GSPL's grounding floor effectively requires it.

### 13. RAG-fusion and reciprocal rank fusion

Multiple query rewrites are run in parallel; results are merged by reciprocal rank fusion. Improves recall cheaply. [13]

### 14. Fusion-in-Decoder (FiD)

Izacard & Grave (2021). The LLM attends to multiple retrieved passages jointly at decode time, not by stuffing them in the prompt. Requires a model trained for it but gives dramatic quality wins on knowledge-intensive tasks. [14]

- **Strengths:** cleanly separates retrieval from generation; scales to many passages.
- **Weaknesses:** requires a custom decoder; newer retrieval-augmented architectures (RETRO, Atlas) use variants.

### 15. The GSPL substrate collapses most of these into one abstraction

Every technique above is trying to recover structure that GSPL's substrate already has:

- **HyDE** tries to bridge the query-document gap. The substrate has signed typed nodes; the gap is smaller because the "document" is already structured.
- **Self-RAG** tries to learn when to retrieve. The substrate has confidence (INV-348) — the model knows when its grounding is insufficient.
- **CRAG** tries to evaluate retrieved passages. The substrate has grounding audits built in (INV-357).
- **RAPTOR** tries to build multi-resolution summaries. The substrate has explicit zoom edges (Brief 100's 11-edge ontology includes zoom/abstraction edges).
- **GraphRAG** tries to build a graph from flat text. The substrate IS a graph, signed and federated.
- **Contextual Retrieval** tries to recover chunk context. The substrate doesn't chunk — gseeds are the atomic unit.
- **Late Chunking** tries to embed with full context. The substrate embeds gseeds in their full typed context.
- **ColBERT** tries to get cross-encoder quality at bi-encoder cost. The substrate's typed edges give token-level structure for free at the edge, not at the token.

The GSPL lesson: we don't ship RAG. We ship substrate-native retrieval, and the RAG techniques become retrieval strategies inside it.

### 16. What GSPL still needs from published RAG

Despite the collapses, six specific techniques need to be absorbed as explicit retrieval strategies:

- **HyDE** for queries where the user's phrasing is mismatched with substrate language (rare but real).
- **Cross-encoder reranking** for the top-K → top-N step; the grounding floor requires this.
- **ColBERT-style token-level late-interaction** as one retrieval backend alongside dense and graph-walk.
- **Contextual Retrieval–style annotation** for external corpora (Brief 090 web fetches), where the substrate structure isn't present.
- **Matryoshka embeddings** for the budget tier system (Brief 106 subscription tiers get different retrieval precision).
- **Reciprocal rank fusion** across multiple retrieval backends (dense, graph-walk, ColBERT, keyword) — cheap and free recall wins.

## Inventions to absorb

Tier W hooks for Brief 127 and Brief 131:

- **Substrate-native retrieval replaces RAG.** The federation graph is the retrieval index; no separate vector store.
- **Multi-backend retrieval fusion.** Dense embeddings + graph walk + ColBERT late-interaction + keyword, merged by reciprocal rank fusion.
- **Cross-encoder reranking is mandatory** on the grounding floor path.
- **Matryoshka embeddings tier retrieval precision** against Brief 106 subscription tiers and Brief 101 budget envelope.
- **HyDE as optional rewrite step** for vocabulary-mismatch queries.
- **Contextual annotation for external corpora** (Brief 090); the substrate doesn't need it but web-fetched passages do.
- **Graph-walk retrieval uses the 11-edge ontology** to propagate relevance; multi-hop is first-class.
- **Self-RAG-like retrieval gating** is free: the substrate's confidence type (INV-348) tells the planner when to retrieve more.
- **CRAG-like correction is free:** the grounding floor audit IS the correction step.
- **RAPTOR-like multi-resolution is free:** zoom edges in the ontology are the summary hierarchy.

## Risks identified

- **ColBERT storage blowup.** Mitigation: quantize token embeddings (ColBERTv2 does this); only apply to frequently-retrieved gseeds.
- **Cross-encoder reranking latency.** Mitigation: budget envelope caps rerank candidates; distilled cross-encoder for fast path.
- **HyDE misleading retrieval.** Mitigation: HyDE is opt-in and only runs on query-rewrite rounds when initial retrieval's confidence is low.
- **External corpus grounding weaker than substrate.** Mitigation: external passages marked with a lower-confidence provenance tag; the grounding floor treats them as weaker evidence.
- **Multi-backend fusion is slow.** Mitigation: backends run in parallel; envelope caps per-backend cost.

## Recommendation

1. **GSPL does not ship RAG.** It ships substrate-native retrieval on top of the federation graph.
2. **Five retrieval backends run in parallel,** merged by reciprocal rank fusion: dense (Matryoshka), graph-walk (11-edge ontology), ColBERT late-interaction, keyword (BM25), HyDE (optional).
3. **Cross-encoder reranker gates the grounding floor.** No response grounds on un-reranked candidates.
4. **Matryoshka embeddings** tier precision by budget envelope.
5. **Contextual annotation** is only for Brief 090 external corpora.
6. **Self-RAG-style gating** is free via substrate confidence; no vocabulary extension needed.
7. **RAPTOR multi-resolution** is free via zoom edges in the 11-edge ontology.
8. **GraphRAG** is the substrate itself; no construction step.

Feeds Brief 127 (memory and context architecture) and Brief 131 (differentiable reasoning substrate).

## Confidence

**4.5/5.** Every published technique cited is mature and well-understood. The "substrate collapses RAG into a special case" framing is principled — GSPL genuinely has the structure the RAG papers were trying to reconstruct. The one 3.5/5 piece is ColBERT storage at federation scale; this needs empirical validation at ~1M gseed corpora before launch.

## Spec impact

- Brief 090 (web search) needs the contextual annotation addendum.
- Brief 091 (knowledge graph) needs the retrieval backend API spec.
- Brief 100 (federation protocol) is already compatible; no change.
- Brief 127 owns the memory-retrieval integration.
- Brief 131 owns the differentiable-retrieval integration.

## Open follow-ups

- ColBERT storage budget at federation scale.
- Cross-encoder distillation recipe.
- Matryoshka embedding dimensions per budget tier.
- Reciprocal rank fusion weighting calibration.

## Sources

1. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," 2020. arXiv:2005.11401.
2. Gao et al., "Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE)," 2022. arXiv:2212.10496.
3. Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection," 2023. arXiv:2310.11511.
4. Yan et al., "Corrective Retrieval Augmented Generation," 2024. arXiv:2401.15884.
5. Sarthi et al., "RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval," 2024. arXiv:2401.18059.
6. Microsoft Research, "GraphRAG: Unlocking LLM Discovery on Narrative Private Data," 2024.
7. Anthropic, "Introducing Contextual Retrieval," Sep 2024.
8. Jina AI, "Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models," 2024.
9. Khattab & Zaharia, "ColBERT" 2020; "ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction," 2022.
10. Lin et al., "How to Train Your DRAGON: Diverse Augmentation Towards Generalizable Dense Retrieval," 2023.
11. Kusupati et al., "Matryoshka Representation Learning," 2022. arXiv:2205.13147.
12. Nogueira & Cho, "Passage Re-ranking with BERT," 2019.
13. Rackauckas, "RAG-Fusion," 2024.
14. Izacard & Grave, "Fusion-in-Decoder," 2021. arXiv:2007.01282.
