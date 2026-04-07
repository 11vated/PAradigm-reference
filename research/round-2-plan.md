# Research Round 2 — Plan and Brief Index

Round 1 (briefs 001–012 + synthesis) resolved the load-bearing *technical* questions: GPU determinism, WGSL portability, JCS, RFC 6979, zstd, type system, c2pa, watermarks, EU AI Act, agent reliability, MAP-Elites convergence.

Round 2 finishes the foundation. It covers the remaining unresearched surface area of GSPL — gene types, engines, intelligence layer, evolution stack, sovereignty, studio, infra, compliance, competition — and *invents* net-new GSPL systems where the existing literature does not yet provide what GSPL needs to be unsurpassable.

## Methodology (extends round 1)

Same template: Question / Why it matters / What we know / Findings / Risks / Recommendation / Confidence (1-5) / Spec impact / Open follow-ups / Sources.

Two new conventions in round 2:

1. **Invention briefs are marked `INV` in the title.** They propose net-new mechanisms (gene types, operators, protocols) and are written as design proposals with explicit "what we are inventing and why" sections, not as surveys.
2. **Competitive briefs end with a Paradigm differentiation table** that names the specific axes on which GSPL outperforms or underperforms each rival, with no marketing language.

## Brief Index

### Tier A — Foundations and Identity (briefs 013-020)

| # | Title | Type |
|---|---|---|
| 013 | The 17 gene types: complete catalog, semantics, operators | Research |
| 014 | UniversalSeed schema invariants and validation | Research |
| 015 | The .gseed file format: layout, magic, sections, forward-compat | Research |
| 016 | Cross-domain composition: functor laws, naturality, the category of seeds | Research |
| 017 | Lineage data model: ancestry, breeding, pruning, content addressing | Research |
| 018 | Versioning and migration: how seeds survive spec evolution | Research |
| 019 | Fisher Information Matrix in seed space: theory and use | Research |
| 020 | INV: Five new gene types beyond the 17 | Invention |

### Tier B — Engines (briefs 021-028)

| # | Title | Type |
|---|---|---|
| 021 | Humanoid family: Character + Sprite + Animation engines | Research |
| 022 | Sound family: Music + Audio engines | Research |
| 023 | Interactive family: Narrative + Game + FullGame engines | Research |
| 024 | Visual family: Visual2D + Procedural + Geometry3D engines | Research |
| 025 | Simulation family: Physics + Ecosystem + ALife engines | Research |
| 026 | UI engine | Research |
| 027 | The 11 planned engines: feasibility and priority matrix | Research |
| 028 | INV: Cross-engine emergent compositions | Invention |

### Tier C — Intelligence Layer (briefs 029-034)

| # | Title | Type |
|---|---|---|
| 029 | GSPL Agent end-to-end architecture | Research |
| 030 | Eight sub-agents: roles, contracts, handoffs | Research |
| 031 | Memory system + exemplar feedback loop | Research |
| 032 | Adjective normalization and intent taxonomy | Research |
| 033 | Concept-to-Seed: latency, cost, reliability budget | Research |
| 034 | INV: Self-improving agent via exemplar-archive feedback | Invention |

### Tier D — Evolution Stack (briefs 035-041)

| # | Title | Type |
|---|---|---|
| 035 | Evolution stack synthesis: GA + ME + CMA-ES + Novelty + AURORA + DQD + POET | Research |
| 036 | Novelty search and AURORA in GSPL space | Research |
| 037 | DQD: differentiable quality-diversity | Research |
| 038 | POET: open-ended co-evolution | Research |
| 039 | Speciation, niching, and population health | Research |
| 040 | Refinement loop with critic models and RL from preferences | Research |
| 041 | INV: GSPL-native evolution operators | Invention |

### Tier E — Sovereignty, Trust, Marketplace (briefs 042-047)

| # | Title | Type |
|---|---|---|
| 042 | Key management lifecycle: gen, rotation, recovery, hardware | Research |
| 043 | Federation protocol and trust list | Research |
| 044 | Marketplace economics and lineage royalties | Research |
| 045 | Anti-piracy and replay-attack defense | Research |
| 046 | IP rights: seeds vs outputs vs lineages | Research |
| 047 | INV: Zero-knowledge proof of authorship | Invention |

### Tier F — Studio, UX, Accessibility (briefs 048-052)

| # | Title | Type |
|---|---|---|
| 048 | Studio architecture | Research |
| 049 | Visual seed inspector for the 17 gene types | Research |
| 050 | Breeding UI: comparison, selection, history | Research |
| 051 | Accessibility (WCAG 2.1 AA) for the seed inspector | Research |
| 052 | Onboarding: first 15 minutes | Research |

### Tier G — Backend and Infrastructure (briefs 053-057)

| # | Title | Type |
|---|---|---|
| 053 | GPU compute strategy: workstation, cloud, edge, batch | Research |
| 054 | Database and lineage graph | Research |
| 055 | Storage, CDN, dedup, lifecycle | Research |
| 056 | Monitoring and SLOs for a solo founder | Research |
| 057 | Cost model: per user, per generation, per evolution run | Research |

### Tier H — Compliance, Security, IP (briefs 058-062)

| # | Title | Type |
|---|---|---|
| 058 | Complete threat model | Research |
| 059 | Adversarial robustness: prompt injection, seed poisoning, model abuse | Research |
| 060 | Content moderation across lineages | Research |
| 061 | Patent landscape and prior art | Research |
| 062 | License strategy: spec, engine, marketplace | Research |

### Tier I — Competitive Deep Dives (briefs 063-070)

| # | Title | Type |
|---|---|---|
| 063 | Image generators: Stable Diffusion, Flux, Midjourney | Research |
| 064 | Video generators: Sora, Veo, Runway | Research |
| 065 | Game engines: Unity, Unreal, Godot | Research |
| 066 | Procedural toolkits: Houdini, Blender Geometry Nodes, WFC | Research |
| 067 | Creator platforms: Roblox, Dreams (PS), Inworld | Research |
| 068 | Academic interactive evolution: Picbreeder, EndlessForms, NEAT | Research |
| 069 | Spore postmortem and ambition analogs | Research |
| 070 | Master competitive matrix: Paradigm vs 20+ rivals on 20 axes | Research |

### Synthesis

| # | Title |
|---|---|
| round-2-synthesis.md | Cross-brief findings, spec impact, Phase 1 deltas, invention catalog |

## Reading order

For an AI agent: read this plan, then `round-2-synthesis.md`, then any Tier A brief whose row in the spec impact table is normative for the work you are about to do. Every brief is self-contained; the synthesis is the only mandatory read after the plan.

For a human contributor: skim the plan, read the synthesis, then deep-dive any tier whose decisions you need to challenge or extend.
