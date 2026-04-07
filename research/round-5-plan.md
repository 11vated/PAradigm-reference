# Round 5 — From Locked Architecture to First Thousand Users (charter)

## Directive

Rounds 1–4 built the substrate. Round 4 locked the architecture at confidence 4.5/5 and left nine explicit open follow-ups. Round 5 closes those follow-ups and answers a single binding question:

> **What has to be true for GSPL to ship its foundation to the first thousand real creators without any of its 13 constitutional commitments bending, any of its 72+ Round 4 inventions degrading into marketing copy, or any layer of the stack revealing a placeholder?**

Round 5 is the bridge. Architecture is locked; Round 5 is about the curation effort, the partner engagements, the operational substrate, and the ship-readiness discipline that turn a locked design into a foundation creators can actually live inside.

## What Round 5 must deliver

1. **Curation discipline** — the 1,000-seed armory, the 80 style adapters, and the anti-hallucination grounding gates must become executable work plans with measurable acceptance criteria, not aspirational totals.
2. **Partner engagement** — the tiered source ladder (Brief 090) and the culture respect contracts (Briefs 086E, 088) must become a concrete partnership program with named institutions, outreach templates, licensing terms, and a lived-experience consultancy network.
3. **Operational substrate** — the federation protocol (Brief 043), knowledge graph (Brief 091), and reference cache (Brief 090) must become runnable systems with query budgets, eviction policies, peer reputation, conflict-resolution UX, and cost models.
4. **Ship-readiness discipline** — the studio (Brief 079), the woah moments (Brief 080), and the composition graph must become a concrete first-user experience with a measurable "first ten minutes" path, launch criteria, scaling plan, creator economics, governance framework, and a year-1 roadmap.

Round 5 introduces **no new substrate primitives**. Round 5 introduces **no new URL schemes**. The substrate is locked. Round 5 is about making the locked substrate shippable without diluting it.

## Brief inventory

### Tier P — Curation and quality discipline

- **095 — The 1,000-seed armory curation plan.** Selection criteria, reviewer rubric, quality bar, category quotas, batch schedule, rejection protocol, exemplar seeds for every category, how curation decisions are themselves signed and lineage-tracked so the armory's composition is auditable.
- **096 — Style adapter quality acceptance criteria.** Gold-standard test set (characters × styles × poses × expressions), identity preservation metrics (face embedding cosine similarity, silhouette IoU, color-palette delta-E), style invariance metrics, acceptance thresholds, mutation-test coverage, failure-mode taxonomy.
- **097 — Anti-hallucination test suite and grounding gates.** Adversarial prompt corpus, grounding floor enforcement (INV-357), CI integration, regression prevention, failure-mode taxonomy, red-team budget, gap-surfacing UX so users always see when the agent is reaching beyond the graph.

### Tier Q — Partnerships and sourcing

- **098 — Source-archive partnership program.** Named partner list (Met, Smithsonian, V&A, BL, Europeana, LoC, Wikimedia, Tasveer Ghar, Nasher, and source-culture institutions), tiered outreach templates, licensing terms, attribution contracts, conflict escalation, partner crawl agreements, renewal cadence.
- **099 — Lived-experience consultancy network.** Domains requiring consultancy (mental health depiction, clinical conditions, sacred/restricted cultural symbols, marginalized-community representation), recruitment criteria, compensation model, review cadence, conflict resolution, exit clauses, how consultancy review is lineage-tracked on every affected gseed.
- **100 — Federation peer protocol details.** Gossip layer, conflict resolution UX, peer reputation scoring, sybil resistance, node-outage recovery, moderation federation (how one peer's constitutional refusal propagates), fork-and-reconcile semantics, the "refutes" and "supersedes" edge lifecycle from Brief 091 operationalized.

### Tier R — Operational substrate

- **101 — Knowledge graph query budget and caching.** Per-query cost model, cache warming strategy, degradation ladder (full → cached → stale-with-warning → refusal), multi-tier storage, cross-region replication, compliance with the grounding floor under load.
- **102 — Reference cache lifecycle.** Eviction policy, partner crawl rate limits, retention tiers (hot / warm / cold / archived), storage economics, legal hold for provenance disputes, transparency surface so users see cache freshness on every `ref://` gseed they compose against.
- **103 — Studio composition graph viewer and reference transparency UI.** Concrete UI spec for the composition graph browser (nodes, edges, zoom levels, lineage walk, fork affordances), the reference transparency panel (every source cited, every confidence score visible, every ungrounded field flagged), the constitutional refusal surface (why the agent said no, what creator-namespace alternatives exist).

### Tier S — Ship readiness

- **104 — The first-user experience: the critical first ten minutes.** Onboarding path, first armory fork, first conversion pipeline run, first reference fetch, first constitutional refusal handled gracefully, the three designed woah moments every new user hits before minute ten, abandonment-failure modes and how each is prevented.
- **105 — Launch criteria and scaling plan.** Gate criteria for foundation v1.0 release, phased rollout (alpha → closed beta → open beta → GA), regional scaling, cost model at 1K / 10K / 100K / 1M users, degradation strategy under unexpected load, rollback protocol.
- **106 — Creator economics and marketplace pricing.** Revenue model, federation tolls, lineage-based royalty distribution (how forks pay upstream creators via the forever-signed-by edge), free-tier boundaries, subscription tiers, marketplace transaction economics, the constitutional commitment that creator credit is never erasable.
- **107 — Governance framework and constitutional amendment process.** Council composition (founder + community + lived-experience consultancies + technical stewards), amendment thresholds for constitutional commitments (13 non-patchable commitments remain non-patchable), ordinary governance workflow, transparency obligations, how governance decisions themselves become signed lineage-tracked gseeds in the federation graph.
- **108 — Year-1 roadmap and milestones.** Quarterly milestones, dependency graph, risk register, budget envelope, go/no-go gates, the honest list of what gets dropped if something slips.

**14 briefs total for Round 5.**

## How Round 5 composes

```
                    CONSTITUTIONAL LAYER (13 commitments, non-patchable)
                                    │
                                    ↓
        ┌────────────── GOVERNANCE (107) ──────────────┐
        │                                              │
        ↓                                              ↓
  CURATION (095, 096, 097)                    PARTNERSHIPS (098, 099)
        │                                              │
        └─────────────────────┬────────────────────────┘
                              ↓
                  OPERATIONAL SUBSTRATE
                  (100, 101, 102, 103)
                              ↓
                  FIRST-USER EXPERIENCE (104)
                              ↓
                  LAUNCH (105)
                              ↓
                  CREATOR ECONOMY (106)
                              ↓
                  YEAR-1 ROADMAP (108)
```

Every brief in Round 5 honors the Round 4 constitutional commitments. Every brief is evidence-backed: citing measured ship data from comparable platforms (Hugging Face, Wikimedia, Blender, Krita, Godot, Unreal Marketplace, itch.io, GitHub, Steam, Substack) rather than projecting from intuition. Every brief ends in executable next actions with named owners even if the owner is Kahlil-as-solo-founder.

## Round 5 non-goals (explicitly)

- **No new substrate primitives.** If a brief discovers the need for a new `xyz://` scheme, that goes into Round 6 and is not smuggled into Round 5.
- **No new constitutional commitments.** If a brief discovers the need for a new commitment, it becomes a governance amendment proposal for Round 6 review.
- **No architecture changes to locked Round 4 systems.** Round 5 operates within the locked architecture and surfaces any tension as an open follow-up for Round 6.
- **No partner lock-in.** All partnerships must remain revocable; the foundation cannot be made dependent on any single institution.
- **No placeholder ship plans.** Every launch gate, every scaling assumption, every cost number cites a real comparable.

## Round 5 confidence target

**4/5 per brief minimum, 4.5/5 for Round 5 as a whole.**

Lower than Round 4's 4.5/5 is acceptable because Round 5 depends on partner response and live ship data that cannot be known until engaged. The lower bound is bounded by *execution uncertainty*, not design uncertainty — the design itself should remain 5/5 within the envelope of what is knowable at plan time.

## How Round 5 ends

Round 5 ends when:

1. All 14 briefs are written and cross-referenced.
2. The Round 5 synthesis (round-5-synthesis.md) captures the ship-readiness posture as a single readable artifact.
3. The README is updated to reflect 108 total briefs and the Round 5 set.
4. The year-1 roadmap (Brief 108) is specific enough to be executable next week.
5. The nine open follow-ups from Round 4 are each explicitly closed or re-scoped into Round 6.

After Round 5, GSPL is not "ready to ship" in the sense that all work is done. GSPL is ready to ship in the sense that **every remaining piece of work has a named owner, a named gate, a named comparable, and a named risk**, and none of them are architecture problems.
