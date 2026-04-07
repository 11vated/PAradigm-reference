# 116 — Memory architectures: MemGPT, A-Mem, Letta, mem0, zep, Titans, cognitive architectures

## Question

What memory architecture does GSPL need, given that the federated knowledge graph is already a content-addressed persistent substrate?

## Why it matters (blast radius)

Memory is the single biggest felt differentiator between a toy assistant and a long-relationship collaborator. Every 2024–2026 memory research program tried to bolt persistent memory onto LLMs that were not designed for it. GSPL is designed for it. The question is whether GSPL needs a separate memory system at all, or whether the substrate IS the memory.

## What we know from the spec

- Brief 091 (federated knowledge graph) is content-addressed — this is already persistent memory at substrate level.
- Brief 101 (query budget) limits how much memory can be touched per query.
- Brief 127 will own the final memory architecture; this brief is the research input.

## Findings

### 1. The cognitive-architecture baseline: ACT-R, SOAR

Classical cognitive architectures (ACT-R, SOAR) split memory into four canonical types:

- **Working memory:** the current context the agent is actively reasoning about. Small, fast, volatile.
- **Episodic memory:** specific events with time/context tags ("the user asked me this yesterday").
- **Semantic memory:** generalized facts and concepts ("Tokyo is the capital of Japan").
- **Procedural memory:** how-to knowledge and learned skills ("the steps to refactor a function").

This taxonomy is 50 years old and still the right carving. [1]

### 2. MemGPT: OS-inspired memory hierarchy

Packer et al. (2023). MemGPT treats the LLM context window as RAM and adds a "disk" tier the model can page in and out of via tool calls. The model learns when to write/read to each tier and when to summarize. [2]

- **Strengths:** works with any LLM; simple mental model; the page-in/page-out pattern works.
- **Weaknesses:** memory is a scratch store, not a structured graph; no lineage; no confidence; no grounding.

### 3. A-Mem: agent memory as a graph

Xu et al. (2024). A-Mem structures memory as a graph of memory notes with typed links. Each memory is a node; relations are learned; retrieval is graph walk. [3]

- **Strengths:** graph structure matches how people actually remember; retrieval quality beats flat MemGPT on multi-hop recall.
- **Weaknesses:** graph schema is learned per-deployment; no cross-deployment standard; no signing or lineage.

### 4. Letta (formerly MemGPT)

Letta productizes MemGPT as a managed service with persistent per-user memory buckets. Same architecture, more plumbing. [4]

### 5. mem0: hybrid vector + graph memory

mem0 layers vector retrieval on top of a graph memory, using the vectors for fuzzy recall and the graph for hard constraints. [5]

### 6. zep: temporal knowledge graph memory

Getzep's zep uses a temporal knowledge graph (Graphiti) that ingests conversational facts into typed nodes with time ranges. The temporal layer lets the agent reason about "what did we decide last week" vs "what was true last month." [6]

This is the closest published system to what GSPL's substrate already provides — except GSPL's graph is federated, signed, and lineage-tracked, which zep's is not.

### 7. Titans memory-at-test-time (revisited from Brief 111)

Google's Titans (2025) learns a neural memory module at inference time. The memory is a differentiable weight tensor updated by gradient steps as the model reads new context. [7]

Titans' innovation matters for GSPL because it shows that a memory can be *updated continuously during inference* without catastrophic forgetting. The GSPL generalization: the substrate IS the updated-at-inference memory — signing a new gseed is the commit.

### 8. Generative Agents

Park et al. (2023). LLM-driven characters with memory streams, reflection, planning. The memory stream is chronological; reflection synthesizes higher-level memories from raw events; planning queries the stream for relevant memories. [8]

Architecturally clean and influential, but the memory stream is per-agent and does not federate or cross-reference to a substrate.

### 9. The "sleep compaction" pattern

Multiple 2024 systems (Anthropic's internal work, Character.AI, Inflection) converged on a sleep-cycle pattern: during idle time, the agent summarizes, consolidates, and compresses memory. This is biologically inspired (the hippocampus does this during sleep). [9]

### 10. What GSPL already provides

- **Content-addressed persistent store:** check. Every gseed.
- **Typed links (edges):** check. 11-edge ontology from Brief 100.
- **Temporal ordering:** check. Signed timestamps on every gseed.
- **Lineage preservation:** check. Forever-signed credit lineage.
- **Federated across creators:** check. Federation protocol from Brief 100.
- **Confidence type:** check. INV-348.
- **Grounding floor:** check. INV-357.

GSPL already has every core memory primitive that the 2024–2026 memory research was trying to bolt onto vanilla LLMs. What GSPL needs is the **working memory** tier and the **binding** between working memory and the substrate.

### 11. The four-tier memory mapping for GSPL

- **Working memory = current context buffer.** The hybrid attention + SSM kernel's active context (Brief 111). Volatile, budgeted, per-query.
- **Episodic memory = signed session gseeds.** Every conversational turn, tool call, and reasoning trace is signed into the creator's episodic namespace. Queryable. Forkable.
- **Semantic memory = the Foundation Kernel + federation graph.** The substrate as it stands. Read-mostly for most queries; written via the forever-signed-credit path.
- **Procedural memory = signed skill gseeds.** Learned patterns, successful trajectories, tool-use sequences, saved workflows. Reusable as templates (Brief 017's plugin ABI extended).

Each tier is a first-class namespace. Each tier has its own query budget line (Brief 101). Each tier has its own retention policy (Brief 102).

### 12. The sleep-cycle pattern applies

GSPL's "sleep cycle" is the quarterly retrospective (INV-481 from Brief 108) and the iterative alignment loop (Brief 113). Between cycles, memory gets consolidated: duplicate nodes merged, stale session episodes compacted to summaries, successful procedures promoted to skill gseeds.

## Inventions to absorb

Tier W hooks for Brief 127:

- **Four-tier memory mapped onto substrate namespaces.** Working, episodic, semantic, procedural — each a named substrate region with its own budget and retention.
- **Working memory = hybrid attention/SSM context buffer.** Brief 111's hybrid kernel.
- **Episodic memory = signed session namespace.** Every turn, call, and trace signs into `session://<creator>/<session-id>/...`.
- **Semantic memory = the federation graph.** No new structure; the existing graph is the semantic store.
- **Procedural memory = signed skill gseeds.** Reusable workflows.
- **Sleep-cycle compaction as operationalized retrospective.** Brief 108's quarterly retro is the compaction cycle. Between cycles, background jobs summarize stale episodes and promote procedural patterns.
- **Retrieval respects the grounding floor.** Memory retrieval is graph retrieval; the same tier discipline from Brief 101 applies.
- **No new memory system to build.** GSPL already has the memory system; it is the substrate. Brief 127 binds the context buffer to the substrate, nothing more.

## Risks identified

- **Creators may not want every session step signed.** Mitigation: private namespace by default; federation is opt-in; tombstone (Brief 102) removes entries with lineage preservation.
- **Episodic memory grows without bound.** Mitigation: compaction during sleep cycles; retention policy tiered by importance signal.
- **Procedural memory can encode bad habits.** Mitigation: procedural promotion requires a success signal and is reviewable via the consultancy network for sensitive domains.
- **Working memory budget is finite.** Mitigation: Brief 101 envelope; Brief 111 hybrid kernel gives more effective context per token.

## Recommendation

1. **GSPL does not build a separate memory system.** The substrate IS the memory. Brief 127's job is the binding, not the design of a new store.
2. **Four-tier mapping onto substrate namespaces.** Working / episodic / semantic / procedural — each a named region with its own budget, retention, and privacy policy.
3. **Sleep-cycle compaction is Brief 108's quarterly retrospective.** Between retros, background jobs do minor compaction.
4. **No new URL schemes.** Episodic lives in `session://`, procedural lives in `skill://` (already exists for Brief 019 plugin ABI), working is buffer-only (not signed), semantic is the whole federation graph.
5. **Privacy by default.** Episodic and procedural default to creator-private; federation opt-in.

Feeds Brief 127 (memory + context architecture) directly.

## Confidence

**4.5/5.** The four-tier mapping is principled and the substrate already has every primitive the 2024–2026 memory research was trying to reinvent. Execution confidence is high because GSPL is not building a new store — it is using a store it already has.

## Spec impact

- Brief 053 (local-first storage) needs the four-tier namespace mapping.
- Brief 101 needs separate budget lines per memory tier.
- Brief 102 needs retention tiers per memory tier.
- Brief 127 owns the integration.

## Open follow-ups

- Procedural memory promotion criteria.
- Episodic compaction cadence.
- Whether cross-creator memory sharing (via federation) is a first-class feature or opt-in.

## Sources

1. Anderson, "The Architecture of Cognition," 1983 (ACT-R); Laird, "The Soar Cognitive Architecture," 2012.
2. Packer et al., "MemGPT: Towards LLMs as Operating Systems," 2023. arXiv:2310.08560.
3. Xu et al., "A-Mem: Agentic Memory for LLM Agents," 2024.
4. Letta / MemGPT product documentation, 2024–2025.
5. mem0, open-source documentation, 2024.
6. Getzep, "Graphiti: Temporal Knowledge Graphs for Agents," 2024.
7. Behrouz et al., "Titans: Learning to Memorize at Test Time," Google, 2025. arXiv:2501.00663.
8. Park et al., "Generative Agents: Interactive Simulacra of Human Behavior," 2023. arXiv:2304.03442.
9. Various industry talks and blog posts, 2024.
