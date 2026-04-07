# 4-Layer Memory System

## What it does

The GSPL Agent and its 8 sub-agents need memory: facts they have learned, conventions they follow, conversations in progress, and instincts about what works. We split memory into **four distinct layers**, each with different write semantics, retention, and retrieval style. This separation prevents the most common LLM-agent failure modes (context bloat, hallucinated history, unbounded growth) and gives us a clean place to plug in human curation.

## The four layers

```
┌────────────────────────────────────────────────────────┐
│  Layer 1: Working Memory       (per conversation)      │  volatile
├────────────────────────────────────────────────────────┤
│  Layer 2: Episodic Memory      (per user)              │  durable, private
├────────────────────────────────────────────────────────┤
│  Layer 3: Semantic Memory      (per workspace/team)    │  durable, shared
├────────────────────────────────────────────────────────┤
│  Layer 4: World Knowledge      (global, curated)       │  durable, public
└────────────────────────────────────────────────────────┘
```

| Layer | Lifetime | Scope | Write authority | Storage |
|---|---|---|---|---|
| 1 Working | Single agent run | One conversation | Agent itself | In-memory scratchpad |
| 2 Episodic | Months/years | One user | User + agent | Per-user encrypted store |
| 3 Semantic | Years | Workspace/team | Workspace admins | Postgres + pgvector |
| 4 World | Permanent | Global | Curator review | Postgres + pgvector + Meilisearch |

## Layer 1: Working Memory

**What it stores:** Everything the agent has learned in the current conversation — the user's last 5 utterances, the parsed intent so far, the partial construction plan, any sub-agent reports.

**Why separate it:** Without a working layer, the agent re-derives everything on every LLM call, paying token cost and risking inconsistency. With it, we have a single canonical scratchpad that all sub-agents can read and write.

**Implementation:** A typed JSON object held in process memory, scoped to the conversation ID. Discarded when the conversation ends.

```
struct WorkingMemory:
    conversation_id: string
    user_id: string
    turn_history: [Turn]
    parsed_intent: Option<ParsedIntent>
    resolved_spec: Option<ResolvedSpec>
    construction_plan: Option<ConstructionPlan>
    sub_agent_reports: Map<AgentName, AgentReport>
    token_budget_remaining: int
```

**Eviction:** When `token_budget_remaining` drops below 25%, the agent runs a *summarization pass* that compresses the oldest turns into a `turn_history_summary` field, freeing space without losing the conversational thread.

## Layer 2: Episodic Memory

**What it stores:** The user's history of seeds, preferences, named templates they have saved, named styles they prefer, projects they are working on, and any explicit "remember this" facts.

**Why separate it:** Personal continuity. When the user comes back tomorrow, the agent should remember that they like muted color palettes, that "their world" has elves and dwarves but no gnomes, and that they tend to prefer 4/4 time signatures. None of this should leak to other users.

**Implementation:** Per-user encrypted Postgres table with row-level security. Sub-fields:

- `seeds_authored: [SeedRef]` — every seed the user has signed.
- `preferences: PreferenceProfile` — extracted from past behavior.
- `saved_templates: [Template]` — explicit user-named templates.
- `pinned_facts: [Fact]` — facts the user has marked "always remember."
- `vector_index: pgvector` — embeddings for fast retrieval.

**Retrieval style:** Vector similarity search at the start of each new conversation, retrieving the top-20 most relevant facts to seed the working memory. Updated whenever the user finishes a conversation or explicitly pins a fact.

**Privacy:** Layer 2 is *private to the user.* It is encrypted at rest with a per-user key derived from the user's sovereignty key, and it is *never* used as training data for any model.

## Layer 3: Semantic Memory

**What it stores:** The workspace's shared conventions — the team's brand voice, custom archetypes, internal style guides, naming conventions, project lore. This is the layer where a game studio's "world bible" lives.

**Why separate it:** Teams need shared context. If three illustrators on the same team are all generating sprites for "World of Tirumel," they should all draw from the same lore, the same style guide, and the same character archetypes — but those facts shouldn't bleed into other teams' work.

**Implementation:** Per-workspace Postgres table. Sub-fields:

- `archetypes: [CustomArchetype]` — team-defined character/style archetypes.
- `style_guides: [StyleGuide]` — visual, narrative, and tonal guides.
- `lore_facts: [Fact]` — world-bible entries with citations.
- `naming_conventions: NamingRules`
- `vector_index: pgvector`

**Retrieval style:** Same as Layer 2, but scoped to workspace. The agent automatically queries Layer 3 whenever it sees a proper noun that matches a known lore entity.

**Write authority:** Workspace admins curate Layer 3. The agent *suggests* additions ("you mentioned 'the Vael Conclave' three times — should I add it to your lore?") but does not write directly.

## Layer 4: World Knowledge

**What it stores:** Curated public knowledge — color theory, music theory, art history, design patterns, named artistic styles, common archetypes, materials science, basic physics. The encyclopedic backdrop that the StyleAgent, MusicTheoryAgent, and PhysicsAgent draw on.

**Why separate it:** This is the only layer that benefits from being *shared* across all users. It is also the only layer that needs editorial review — bad facts here would corrupt every agent run on the platform.

**Implementation:** A global Postgres + Meilisearch + pgvector store, version-controlled like a wiki. Sub-fields:

- `topics: [Topic]` — structured articles on a topic, with references.
- `references: [Reference]` — primary source citations.
- `embedding_index: pgvector`
- `full_text_index: meilisearch`

**Retrieval style:** Hybrid: a query first hits Meilisearch for keyword matches, then pgvector for semantic neighbors. Top-K results from each are reranked by a small cross-encoder.

**Write authority:** Curator review. Contributions are submitted as PRs (literally — Layer 4 lives in a public Git repo that mirrors into Postgres on each merge). Every fact must cite a primary source.

## Cross-layer interaction

When a sub-agent needs to look something up, it queries layers in *order from most specific to most general* and stops as soon as it has enough:

```
fn lookup(query: string, working: &WorkingMemory, episodic: &EpisodicStore,
            semantic: &SemanticStore, world: &WorldStore) -> [Fact]:
    let mut results = []
    results.extend(working.search(query))
    if results.length >= 5: return results
    results.extend(episodic.search(query, top_k = 5))
    if results.length >= 5: return results
    results.extend(semantic.search(query, top_k = 5))
    if results.length >= 5: return results
    results.extend(world.search(query, top_k = 5))
    return dedupe(results)
```

This ordering is critical: a fact in the user's own episodic memory ("I prefer blue, never red") *always* takes precedence over a generic Layer 4 fact ("most fantasy art uses warm tones"). The agent never overrides the user with the world.

## Determinism considerations

- Layers 1, 2, 3, 4 are not deterministic (LLM responses, vector retrievals, ranking).
- The lookups *are* logged and replayable: each agent run records the query, the layer queried, and the IDs returned.
- If a seed needs to be reproduced, the agent run is replayed against the *snapshot* of memory at the original time, not the current memory.

## Privacy and PII

- Layer 1: ephemeral, never persisted.
- Layer 2: encrypted per-user, never used for training, never shared.
- Layer 3: encrypted per-workspace, never used for training, never shared outside workspace.
- Layer 4: public by definition.

The boundaries are *enforced at the database level* by row-level security. A bug in the agent code cannot accidentally leak Layer 2 data to Layer 4.

## References

- *Generative Agents: Interactive Simulacra of Human Behavior* — Park et al. 2023 (the memory architecture inspiration)
- *MemGPT: Towards LLMs as Operating Systems* — Packer et al. 2023
- *RETRO: Improving Language Models by Retrieving from Trillions of Tokens* — Borgeaud et al. 2021
