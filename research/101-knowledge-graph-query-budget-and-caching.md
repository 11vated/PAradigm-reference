# Brief 101 — Knowledge graph query budget and caching

## Question

What per-query cost model, cache warming strategy, degradation ladder, and storage architecture must GSPL's federated knowledge graph operate under so that the grounding floor (INV-357) remains honored at 1, 1K, 100K, and 1M concurrent users without any layer silently degrading?

## Why it matters

The knowledge graph is the agent's truth contract. Every grounded response depends on it. At scale, an ungated graph becomes either (a) a cost sink that breaks the foundation's budget, or (b) a silent liability where queries degrade to "best effort" results that fabricate their grounding. Neither is acceptable.

## What we know from spec

- Brief 091: federated content-addressed graph.
- Brief 090: tiered source ladder with `ref://` gseeds and confidence scoring.
- INV-357: agent grounding floor — can only compose what the graph proves.
- Brief 097 INV-397: CI grounding gate, zero-hallucination requirement.
- Brief 100 INV-418: replication targets.

## Findings

### Finding 1: Graph query cost dominates at scale

Benchmarks from Neo4j, JanusGraph, Dgraph, TigerGraph, and the Wikidata Query Service show that graph traversal cost scales with the number of edges touched, not just nodes. A grounded response typically touches 50–200 edges per query (character → composition → primitive → reference). At 1M queries/day, that's 50M–200M edge touches/day — serious hardware cost.

The cost model must track:

- Edge touches per query.
- Cache hit/miss ratio.
- Cross-peer fetches (federation traffic).
- Reference fetch cost (from partner archives via Brief 098).

### Finding 2: Three-tier caching is the proven pattern

Cache architecture from Google, Meta, Cloudflare, and large graph deployments uses three tiers:

1. **Hot cache** — in-memory, the most recently and frequently accessed nodes and edges, target <1ms lookup.
2. **Warm cache** — SSD-backed, last-24-hour working set, target <10ms lookup.
3. **Cold storage** — the full graph, target <100ms lookup.

Degradation ladder: if hot cache miss and warm cache miss, fall through to cold. If cold is slow or unavailable, surface the slowness rather than silently timing out.

### Finding 3: Pre-warming matters for armory seeds and common composition paths

The Foundation Kernel (Brief 095) is queried against on every first-user experience. Those 200 seeds and their full composition graphs should be pre-warmed into hot cache. Similarly, the 10 canonical test characters and 12 canonical poses from Brief 096 are queried repeatedly. Pre-warming reduces first-user latency from hundreds of ms to single-digit ms.

### Finding 4: Degradation must downgrade grounding confidence, never fabricate it

When the cache is stale, the partner is slow, or the federation is partitioned, the response must surface the degradation to the user:

- "This response is grounded against a cache from 2 hours ago, not live data."
- "The partner archive is temporarily unreachable; the following references are from cached copies."
- "Two federation peers disagree on this edge; both views are shown."

Never silently return a stale answer as if it were fresh. Never fabricate grounding to avoid a slow response.

### Finding 5: Budget per query is finite and user-visible

Every query gets a budget — a time budget (e.g., 500ms for interactive), an edge-touch budget (e.g., 500 edges), and a fetch budget (e.g., 3 live partner fetches). When a query exceeds budget, it stops and surfaces the partial result with a clear "budget exceeded" flag. Users can grant more budget explicitly for deep research queries.

## Inventions

### INV-422 — Per-query budget envelope

Every query carries a budget envelope:

- `time_budget_ms` (default 500 for interactive, 5000 for research).
- `edge_touches_budget` (default 500 interactive, 10000 research).
- `live_fetch_budget` (default 3 interactive, 30 research).
- `freshness_max_age_sec` (default 3600 interactive, 86400 research).

Queries that exceed any budget stop at that boundary and return partial results with a budget-exceeded marker. Users can grant more budget at query time.

### INV-423 — Three-tier cache with explicit tier-source labeling

Every cached node and edge carries a `cache-tier` marker (hot / warm / cold / live). Every query response carries a per-field tier-source label so users see which parts of the answer were live vs. cached. Degradation is visible, not silent.

### INV-424 — Pre-warm policy for Foundation Kernel and canonical test sets

The Foundation Kernel's 200 seeds, the 10 × 12 × 8 × 5 test grid from Brief 096, and the quarterly hallucination corpus from Brief 097 are pre-warmed into hot cache at startup. Pre-warm completeness is reported in a `cache-warm-status://` gseed.

### INV-425 — The degradation ladder with grounding downgrade

Five degradation states, each with explicit grounding impact:

| State | Response behavior | Grounding confidence |
|---|---|---|
| Live | Full grounding from live sources | Unchanged |
| Warm cache | Served from SSD cache | Downgraded by age-adjusted factor |
| Cold storage | Served from deep storage | Downgraded further |
| Partner unreachable | Served from last cached copy | Downgraded, partner flag set |
| Graph partition | Served from local peer only | Downgraded, partition flag set |

Users see every downgrade. The grounding floor NEVER silently degrades below the threshold that would change a response from grounded to ungrounded — it surfaces the gap instead.

### INV-426 — Cost accounting per namespace

Query costs are accounted per namespace (foundation, creator, federation peer). Namespaces that exceed their budget receive a soft throttle with a warning, then a hard throttle with a refusal. Cost transparency is public: every user can see the foundation's cost envelope and the headroom remaining.

### INV-427 — Cache eviction policy tied to freshness and access

Eviction is governed by a score combining recency, access frequency, and freshness requirement. Foundation Kernel content is exempt from eviction. Partner reference cache eviction respects the partnership terms (Brief 102).

### INV-428 — Budget-exceeded UX affordance

When a query exceeds its budget, the studio surfaces the partial result with a button: "Extend budget and retry." The user can grant more budget (time, fetches) at a visible cost, or accept the partial answer. No silent truncation.

## Phase 1 deliverables

**Months 0–3**
- Per-query budget envelope encoded in the query layer.
- Three-tier cache with tier-source labeling.
- Foundation Kernel pre-warm at startup.
- Degradation ladder with grounding downgrade.

**Months 3–6**
- Cost accounting per namespace.
- Eviction policy tuned against first-user-experience workload.
- Budget-exceeded UX in studio.

**Months 6–12**
- Load testing at 1K, 10K simulated concurrent users.
- Cross-region replication and latency budget.
- Partner crawl rate integration with cache refresh cadence.

## Risks

- **Cold storage latency blowing interactive budgets.** Mitigation: hot/warm cache coverage targets, pre-warming Foundation Kernel, degradation ladder with visible downgrade.
- **Cache poisoning or stale cache masking real data.** Mitigation: content-addressing prevents poisoning; freshness age is visible; users can force refresh.
- **Budget settings too strict, surfacing errors on normal queries.** Mitigation: defaults calibrated against real workload in the load testing phase; user override is one click.
- **Namespace throttling looking like censorship.** Mitigation: cost transparency is public; throttles are logged and visible, not hidden.

## Recommendation

**Adopt INV-422 through INV-428.** Calibrate defaults against Foundation Kernel workload in months 0–3 before opening to wider access. Treat the degradation ladder as a first-class UX feature, not an error path.

## Confidence

**4/5.** Three-tier caching and per-query budgeting are well-understood patterns. The main calibration risk is tuning defaults for real workloads, which can only happen with real traffic.

## Spec impact

Brief 091 gains seven new inventions (INV-422..428). No new substrate primitives. The grounding floor gains explicit operational enforcement at the query layer.

## Open follow-ups

- Hardware sizing per user-count target.
- Regional replication topology.
- Cold-storage medium (object store vs. dedicated graph store).
- Cost pricing for user-granted budget extensions (Brief 106).

## Sources

- Neo4j, JanusGraph, Dgraph, TigerGraph graph database benchmarks.
- Wikidata Query Service published query cost analyses.
- Google, Meta, Cloudflare three-tier cache architecture talks.
- Round 4 Brief 090 for source ladder.
- Round 4 Brief 091 for knowledge graph.
- Round 5 Brief 097 for grounding gate.
- Round 5 Brief 100 for federation replication.
