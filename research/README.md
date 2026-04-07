# Paradigm GSPL Engine — Technical R&D

This directory holds the technical research that resolves the load-bearing open questions in the spec **before** any code is written. The goal is to de-risk the parts of the spec that, if wrong, would force a major rewrite during Phase 1.

## Charter

Each brief in this directory addresses **one** open question, follows a fixed template, and ends with an actionable conclusion. The audience is an AI coding agent (or a human engineer working through Phase 1) — the briefs are written to be machine-actionable, not narrative.

The briefs are **research outputs**, not normative spec. When a brief recommends a change to the spec, it's flagged in the `Spec impact` section and will be folded into the spec in a separate, traceable PR.

## Methodology

1. **Primary sources only.** RFCs, language specs, library source code, peer-reviewed papers, and authoritative documentation. Blog posts are admissible as secondary corroboration but never as the only source.
2. **Confidence ratings.** Every conclusion carries a confidence score from 1 (speculative) to 5 (verified against source code or formal spec). Anything below 3 is a red flag for further investigation.
3. **Reproducibility.** Where a finding depends on a specific tool version, library commit, or empirical measurement, that version is pinned in the brief.
4. **Conservative bias.** When sources disagree or evidence is thin, the brief recommends the more conservative path and flags the disagreement.
5. **Spec impact is explicit.** Every brief lists exactly which spec files it touches and what the proposed change is. No silent drift.

## Brief template

Every brief in this directory has these sections, in this order:

```
# NNN — <Question title>

## Question
One sentence stating the question.

## Why it matters (blast radius)
What breaks in the spec / Phase 1 plan if we get this wrong.

## What we know from the spec
Pointers to the relevant spec sections that depend on this.

## Findings
Numbered findings, each with citations to primary sources.

## Risks identified
Specific failure modes the findings revealed.

## Recommendation
Concrete, actionable. "Use X with config Y" or "Defer to Phase N because Z."

## Confidence
1-5, with rationale.

## Spec impact
List of spec files to update and the proposed change.

## Open follow-ups
Things we still don't know that the brief did not resolve.

## Sources
Numbered list of citations matching the inline references.
```

## Brief index

### Tier 1 — Foundational (Phase 1 blockers)

| # | Title | Status | Confidence |
|---|-------|--------|------------|
| 001 | GPU determinism cross-vendor | done | 3 |
| 002 | WGSL portable subset | done | 4 |
| 003 | JCS canonicalization edge cases | done | 4 |
| 004 | RFC 6979 ECDSA via p256 crate | done | 4 |
| 005 | zstd deterministic encoding | done | 4 |
| 006 | HM + refinements feasibility | done | 3 |

### Tier 2 — Compliance (cannot ship without)

| # | Title | Status | Confidence |
|---|-------|--------|------------|
| 007 | c2pa-rs library maturity | done | 4 |
| 008 | Image DCT watermark robustness | done | 3 |
| 009 | audiowmark robustness | done | 4 |
| 010 | EU AI Act 2026 application details | done | 4 |

### Tier 3 — Operational (cannot run as solo founder without)

| # | Title | Status | Confidence |
|---|-------|--------|------------|
| 011 | Agent reliability backstops | done | 3 |
| 012 | MAP-Elites convergence in our budgets | done | 3 |

### Synthesis

| Doc | Purpose |
|-----|---------|
| `synthesis.md` | Round 1 cross-brief findings, spec impact summary, Phase 1 plan deltas |
| `round-2-synthesis.md` | Round 2 (briefs 013-070) cross-brief synthesis, constitutional commitments, Phase 1 deltas, invention catalog |
| `round-2-plan.md` | Round 2 charter and brief inventory |

## Round 2 (briefs 013-070)

Round 2 took the spec from "principled foundation" to "exhaustively defined platform." 58 briefs across 9 tiers, with 12 net-new inventions (marked **INV**). Read `round-2-synthesis.md` first for the integrated view; dive into individual briefs for depth.

### Tier A — Substrate deepening (013-028)

| # | Title |
|---|---|
| 013 | Content-addressing scheme |
| 014 | Cross-engine breeding via naturality squares |
| 015 | gseed format v1 |
| 016 | Gseed compression |
| 017 | Federation transport selection |
| 018 | Versioning and compatibility |
| 019 | Plugin ABI v1 |
| 020 | Determinism contract per engine |
| 021 | Sprite engine deep dive |
| 022 | Image engine deep dive |
| 023 | Modifier-surface DSL |
| 024 | Lineage entry schema |
| 025 | Renderer determinism contract |
| 026 | Deterministic kernel implementation |
| 027 | Reproducibility test harness |
| 028 | Per-engine spec format |

### Tier B — Agent and conversational layer (029-034)

| # | Title |
|---|---|
| 029 | Planner agent architecture |
| 030 | Critic ensemble architecture |
| 031 | Refinement loop policy |
| 032 | Modifier-surface UI binding |
| 033 | Agent permission model |
| 034 | Agent observability |

### Tier C — Renderer (035, deferred to Tier G)

| # | Title |
|---|---|
| 035 | Renderer architecture overview |

### Tier D — Evolution layer (036-041)

| # | Title |
|---|---|
| 036 | Novelty search and AURORA |
| 037 | Differentiable Quality Diversity (DQD) |
| 038 | POET open-ended coevolution |
| 039 | Speciation, niching, population health |
| 040 | Refinement loop with critics + RL |
| 041 | **INV** GSPL-native evolution operators |

### Tier E — Sovereignty / trust / marketplace (042-047)

| # | Title |
|---|---|
| 042 | Key management lifecycle |
| 043 | Federation protocol |
| 044 | Marketplace economics |
| 045 | Anti-piracy and leak resilience |
| 046 | IP rights and licensing |
| 047 | **INV** zk-proof of authorship |

### Tier F — Studio / UX / accessibility (048-052)

| # | Title |
|---|---|
| 048 | Studio IDE architecture |
| 049 | Compose and conversational UX |
| 050 | Accessibility and internationalization |
| 051 | Onboarding and progression |
| 052 | **INV** Lineage-aware time machine |

### Tier G — Backend / infrastructure (053-057)

| # | Title |
|---|---|
| 053 | Local-first storage and sync |
| 054 | Rendering pipeline and GPU |
| 055 | LLM runtime and BYO models |
| 056 | Observability, telemetry, privacy |
| 057 | Release engineering and update channels |

### Tier H — Compliance / security / IP (058-062)

| # | Title |
|---|---|
| 058 | EU AI Act deep compliance |
| 059 | GDPR and data protection |
| 060 | Supply chain and dependency security |
| 061 | Content moderation and AUP |
| 062 | Incident response and disclosure |

### Tier I — Competitive deep dives (063-070)

| # | Title |
|---|---|
| 063 | Image generators: SD, Flux, Midjourney |
| 064 | Video generators: Sora, Veo, Runway |
| 065 | Game engines: Unity, Unreal, Godot |
| 066 | Procedural toolkits: Houdini, Blender, WFC |
| 067 | Creator platforms: Roblox, Dreams, Inworld |
| 068 | Academic interactive evolution: Picbreeder, NEAT |
| 069 | Spore postmortem and ambition analogs |
| 070 | Master competitive matrix: Paradigm vs 20+ rivals on 20 axes |

## How to read this directory

If you are a human engineer:
- Start with `synthesis.md`. It tells you what changed and why.
- Read briefs 001–006 before writing any kernel code.
- Read briefs 007–010 before designing the export pipeline.
- Read briefs 011–012 before building the agent and evolution loops.

If you are an AI coding agent:
- Each brief's `Recommendation` is your operating instruction for the relevant subsystem.
- Each brief's `Spec impact` lists files in the parent repo that take precedence over the brief if they conflict.
- Treat any finding with confidence ≤ 2 as a hard stop — surface it to the human and ask before proceeding.

## What is deliberately NOT in this directory

- **Build planning.** That belongs in `roadmap/`.
- **Architecture decisions.** Those belong in `adr/`. A brief can recommend an ADR but does not replace one.
- **Performance benchmarks against real hardware.** Those require Phase 1 infrastructure to be stood up first. The briefs cite published benchmarks where they exist and flag where empirical measurement is required.
- **Anything resolved by spec text already.** If the spec answers the question, it's not an open question.
