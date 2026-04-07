# 127 — GSPL memory and context architecture (Tier W integration)

## Question

How does GSPL bind the reasoning kernel's context buffer to the substrate so that memory is structurally unsurpassable, without building a new memory system?

## Why it matters (blast radius)

Memory is where creator relationships compound. A system that remembers every prior interaction in a way that preserves creator ownership, lineage, and privacy has a moat no closed lab can cross. GSPL already has the primitives; Brief 127's job is the binding.

## What we know from prior briefs

- **111:** hybrid attention+SSM context buffer deferred to v2; YaRN-extended attention in v1.
- **116:** GSPL does not build a separate memory system; the substrate IS the memory; four-tier mapping onto substrate namespaces.
- **120:** substrate-native retrieval with multi-backend fusion.
- **121–125:** every published coding agent has flat or per-session memory; no signed lineage; no cross-session compounding.

## Architecture

### Four-tier memory mapping (from Brief 116)

- **Working memory = reasoning kernel context buffer.** The Layer 0 backbone's active context. Volatile, budgeted per-query (Brief 101). YaRN-extended to 256K in v1; hybrid SSM in v2.
- **Episodic memory = signed session namespace.** Every turn, tool call, and reasoning trace is signed into `session://<creator>/<session-id>/...`. Private by default. Forkable. Queryable. Retention policy tiered.
- **Semantic memory = Foundation Kernel + federation graph.** The substrate as it stands. Read-mostly for most queries; written via Brief 100's forever-credit path.
- **Procedural memory = signed skill gseeds.** Successful workflows, tool sequences, substrate mutations that produced a grounding+constitutional pass. Reusable as templates via Brief 017/019's plugin ABI.

### Tier budgets (Brief 101 lines)

Each memory tier has its own budget envelope line:

| Tier | Budget line | Scales with |
|---|---|---|
| Working | tokens in active context | subscription tier (Brief 106) |
| Episodic | session retrieval depth and candidate count | per-turn query |
| Semantic | graph walk depth and candidate count | per-turn query + namespace tier |
| Procedural | skill lookup candidates and instantiation cost | per-task |

### Retention policy (Brief 102)

- **Working:** ephemeral; cleared at session end.
- **Episodic:** tiered by explicit creator signal. Default 30-day rolling for unsigned; forever for signed.
- **Semantic:** forever (signed gseeds are immutable; tombstones preserve lineage).
- **Procedural:** forever once promoted; promotion requires Brief 096 identity metric + grounding + constitutional pass.

### Privacy model

- **Episodic is private by default.** Federation is opt-in per session.
- **Procedural is private by default.** Federation is opt-in per skill.
- **Semantic federation follows Brief 100** — explicit sharing with signed lineage.
- **Working is never persisted** beyond session.
- **Tombstones (Brief 102)** remove an entry with lineage preservation.

### Compaction (the sleep cycle)

- **Daily background compaction:** summarize stale sessions, promote frequently-used reasoning traces to procedural, prune duplicate edges.
- **Weekly:** iterative DPO pass on new preference data (Brief 113).
- **Monthly:** verifier training on graph-audited traces (Brief 119).
- **Quarterly:** full retrospective (Brief 108) with council review (Brief 107).

### Binding to the reasoning kernel

1. **On query arrival:** the kernel receives the active context window budget, the creator's namespace, and the current task type.
2. **Retrieval dispatch (Brief 120):** multi-backend fusion runs dense + graph-walk + ColBERT + keyword in parallel. Candidates are merged by reciprocal rank fusion.
3. **Cross-encoder reranking:** top-K candidates are reranked by a distilled cross-encoder.
4. **Grounding floor gate:** candidates below grounding threshold are dropped; remaining candidates are loaded into working memory.
5. **Episodic pull:** recent session turns within the creator's session namespace are prioritized in the working memory.
6. **Procedural pull:** skill gseeds matching the task template are loaded as templates.
7. **Generation:** the kernel generates with the full context.
8. **Commit:** every signed intermediate is written to episodic; successful trajectories are candidates for procedural promotion.

### What no new primitive is required

- No new URL schemes (session://, skill:// already exist).
- No new substrate types.
- No new retrieval index (the federation graph is the index).
- No new memory format (signed gseeds are the memory unit).
- No new privacy model (Brief 033 already handles it).

## Inventions (INV-506 through INV-514)

- **INV-506:** four-tier memory mapped onto substrate namespaces with per-tier budgets and retention.
- **INV-507:** session:// namespace as episodic memory; signed per turn.
- **INV-508:** procedural promotion requires grounding + constitutional + identity-metric pass.
- **INV-509:** daily compaction cycle for session summarization and procedural promotion.
- **INV-510:** multi-backend retrieval fusion (dense + graph + ColBERT + keyword) on substrate.
- **INV-511:** cross-encoder reranker gates the grounding floor.
- **INV-512:** working memory is never persisted; only signed intermediates are.
- **INV-513:** private-by-default for episodic and procedural; federation opt-in per entry.
- **INV-514:** tombstone-with-lineage preservation for memory deletion (Brief 102).

## What makes this unsurpassable

1. **Memory compounds across sessions** because every signed gseed is permanent and lineage-tracked.
2. **Memory is owned by the creator** because every entry is in the creator's namespace.
3. **Memory is auditable** because every entry has signed provenance.
4. **Memory federates safely** because the federation protocol is signed and revocable.
5. **Memory degrades gracefully** because stale episodes compact into summaries without losing lineage.
6. **Memory retrieval respects the grounding floor** because retrieval is substrate-native.
7. **Memory has a built-in privacy model** because namespaces are privacy primitives.
8. **Memory doesn't require a separate system** because the substrate IS the system.

No published memory architecture has more than three of these properties simultaneously.

## Risks identified

- **Episodic grows without bound.** Mitigation: daily compaction; retention tiers; tombstone with lineage.
- **Procedural promotion encodes bad habits.** Mitigation: promotion gates (grounding + constitutional + identity metric); consultancy review for sensitive namespaces.
- **Retrieval latency compounds across backends.** Mitigation: parallel dispatch; per-backend budget cap; Matryoshka embeddings for fast-tier filtering.
- **Cross-encoder latency.** Mitigation: distilled model; candidate cap from Brief 101 envelope.
- **Private-by-default friction for collaborative creators.** Mitigation: workspace-level defaults; explicit collaborative namespaces with shared episodic.

## Recommendation

1. **Ship four-tier memory in v0.1** — the mapping is free because substrate already has the primitives.
2. **Multi-backend retrieval fusion in v0.2** — start with dense + graph-walk, add ColBERT and keyword in v0.2.
3. **Daily compaction cycle in v0.2.** Background job.
4. **Procedural promotion in v0.3.** Requires Brief 096 identity metric to be mature.
5. **Private-by-default from v0.1.** Federation is opt-in per entry from day one.
6. **Cross-encoder reranker in v0.1** for the grounding floor path. Non-negotiable.

## Confidence

**4.5/5.** The architecture is a direct mapping from Brief 116's recommendation onto primitives GSPL already has. No new substrate work required. The 3.5/5 piece is procedural promotion criteria calibration — needs real usage data to tune.

## Spec impact

- Brief 053 (local-first storage) needs the four-tier namespace mapping confirmation.
- Brief 091 (knowledge graph) needs the retrieval backend API spec.
- Brief 101 (budget) needs per-tier lines.
- Brief 102 (retention) needs per-tier tiers.
- Brief 127 this brief completes the integration.

## Open follow-ups

- Compaction cadence calibration.
- Procedural promotion threshold tuning.
- ColBERT storage budget.
- Cross-encoder distillation recipe.

## Sources

Briefs 111, 116, 120, and their cited sources.
