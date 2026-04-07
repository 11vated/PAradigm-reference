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
| `round-3-synthesis.md` | Round 3 (briefs 071-077) closes every concession; 25 new inventions (INV-200 to INV-224); overall substrate confidence raised to 4/5 |
| `round-4-plan.md` | Round 4 charter — fill the substrate with the stuff of the world |
| `round-4-synthesis.md` | Round 4 (briefs 081-094) ships 17 measured-world libraries + character canon + canonical seed armory + universal conversion pipeline + agent web cross-reference + federated knowledge graph; 72 new inventions (INV-310 to INV-381); 13 non-patchable constitutional commitments; substrate confidence 4.5/5 |
| `round-5-plan.md` | Round 5 charter — from locked architecture to first thousand users |
| `round-5-synthesis.md` | Round 5 (briefs 095-108) ships curation, partnerships, consultancies, federation operations, query budgets, cache lifecycle, composition graph viewer, first-ten-minutes path, launch criteria, creator economics, governance, and year-1 roadmap; 100 new inventions (INV-382 to INV-481); ship-readiness posture; round confidence 4.5/5 |
| `round-6-plan.md` | Round 6 charter — research-first teardown of frontier models, agent frameworks, and code platforms to specify how GSPL becomes structurally unsurpassable |
| `round-6-synthesis.md` | Round 6 (briefs 109-131) lands the seven-axis structural claim (Signed, Typed, Lineage-tracked, Graph-structured, Confidence-bearing, Rollback-able, Differentiable), the five-layer reasoning kernel, four-tier memory, four-layer action space, four-cadence self-improvement loop, neurosymbolic binding, and v0.1→v0.5 release arc; 74 new inventions (INV-482 to INV-555); round confidence 4.4/5 |
| `round-6.5-plan.md` | Round 6.5 charter — close the 20 open follow-ups from Round 6 so Round 7 can start implementation without re-opening any architectural questions |
| `round-6.5-synthesis.md` | Round 6.5 (briefs 132-151) calibrates router/value-function/benchmark/hardware/cost/cadence/threshold/scope/messaging across 20 briefs in four tiers (X-Calibration / Y-Empirical / Z-Recipe / W-Operational); freezes v0.1 scope at 42 features with 17 explicit cuts; signs the cost model and benchmark posture; ships the creator-facing message; 38 new inventions (INV-556 to INV-593); v0.1 build-ready statement |

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

## Round 3 — Closing the gaps (briefs 071-077)

Round 3 takes the weaknesses honestly named in the Round 2 synthesis and turns each one into a GSPL-native strength via substrate-level architecture and 25 net-new inventions (INV-200 to INV-224). Every Round 2 concession is reversed in the record. Read `round-3-synthesis.md` for the integrated view.

| # | Title | Closes concession | Confidence |
|---|---|---|---|
| 071 | Beating Houdini at hard simulation | "Houdini will be better at hard simulation for years" | 4/5 |
| 072 | Beating Unreal at AAA 3D rendering | "Unreal wins at AAA 3D rendering" | 4/5 |
| 073 | Beating MetaHuman at photoreal humans | "MetaHuman wins at photoreal humans" | 4/5 |
| 074 | GSPL multiplayer runtime | "GSPL doesn't have a multiplayer runtime" | 4/5 |
| 075 | GSPL without a real GPU | "Depends on a real GPU for the best engines" | 4/5 |
| 076 | Open-weight licensing resilience | "Open-weight licensing volatility is a risk" | 4/5 |
| 077 | ZK anonymous publication confidence path | "ZK anonymous publication is 2/5 confidence" | 4/5 at v1.5, 4.5/5 at v2 |

## Round 4 — The inventory and the look (briefs 081-094)

Round 4 fills the substrate with the stuff of the world: 17 measured-world libraries, the character canon, the canonical seed armory, the universal anything-to-gseed conversion pipeline, the agent web cross-reference system, and the federated knowledge graph that holds it all together. 72 new inventions (INV-310..381). 13 non-patchable constitutional commitments. Read `round-4-synthesis.md` for the integrated view.

| # | Title |
|---|---|
| 081 | Chemistry primitives |
| 082 | Physics constants and laws |
| 083 | Materials |
| 084 | Particles and fields |
| 085 | Biology and anatomy |
| 086 | Earth sciences |
| 086A | Cosmology and astronomy |
| 086B | Mathematics and geometry |
| 086C | Music and audio |
| 086D | Language and linguistics |
| 086E | Culture, history, mythology |
| 086F | Built world (architecture, urbanism, vehicles, tools) |
| 086G | Lifestyle (textiles, garments, food) |
| 086H | Psychology and emotion |
| 087 | Visual phenomena coverage atlas |
| 088 | Cross-art-style and character canon |
| 088A | Canonical seed armory |
| 089 | Universal anything-to-gseed pipeline |
| 090 | Agent web cross-reference system |
| 091 | Federated knowledge graph |
| 092 | Character power systems, transformations, and movesets |
| 093 | Full media spectrum and studio technique substrate |
| 094 | Vehicles full-spectrum + substrate open-extension grammar |

## Round 5 — From locked architecture to first thousand users (briefs 095-108)

Round 5 turns the locked Round 4 architecture into ship-readiness: curation discipline, partner engagements, lived-experience consultancies, federation operations, query budgets, cache lifecycle, composition graph UI, first-ten-minutes UX, launch gates, creator economy, governance council, and year-1 roadmap. 100 new inventions (INV-382..481). No new substrate primitives, no new constitutional commitments. Read `round-5-synthesis.md` for the integrated view.

| # | Title |
|---|---|
| 095 | 1,000-seed armory curation plan |
| 096 | Style adapter quality acceptance criteria |
| 097 | Anti-hallucination test suite and grounding gates |
| 098 | Source-archive partnership program |
| 099 | Lived-experience consultancy network |
| 100 | Federation peer protocol details |
| 101 | Knowledge graph query budget and caching |
| 102 | Reference cache lifecycle |
| 103 | Composition graph viewer + reference transparency UI |
| 104 | First-user experience: the critical first ten minutes |
| 105 | Launch criteria and scaling plan |
| 106 | Creator economics and marketplace pricing |
| 107 | Governance framework and constitutional amendment process |
| 108 | Year-1 roadmap and milestones |

## Round 6 — Surpassing the frontier (briefs 109-131)

Round 6 answers the charter question: "how to truly surpass what's already available." It is a research-first round that tears down every frontier model, agent framework, and code platform at the source level, then specifies a reasoning kernel, memory system, action space, self-improvement loop, and neurosymbolic binding that compound into a structurally unsurpassable substrate. 23 briefs across four tiers. 74 new inventions (INV-482..555). The culminating Brief 131 states the seven-axis structural claim and the v0.1→v0.5 release arc. Read `round-6-synthesis.md` for the integrated view.

### Tier T — Frontier model teardowns (109-114)

| # | Title |
|---|---|
| 109 | Frontier reasoning training recipes (OpenAI o1/o3, DeepSeek-R1, Qwen3-Thinking) |
| 110 | Open-weight backbone survey and selection |
| 111 | Long-context architectures (YaRN, Mamba, hybrid SSM) |
| 112 | RLHF / DPO / KTO / RFT recipe landscape |
| 113 | Constitutional training and non-amendable commitments |
| 114 | Neurosymbolic reasoning and world-model primitives |

### Tier U — Agent frameworks and reasoning topologies (115-120)

| # | Title |
|---|---|
| 115 | LATS, ToT, GoT, Reflexion, Self-Refine taxonomy |
| 116 | Multi-agent topologies (AutoGen, CrewAI, MetaGPT, Camel) |
| 117 | Tool-use protocols (MCP, Toolformer, Gorilla, xgrammar, CodeAct) |
| 118 | Multi-agent hand-off and signed lineage |
| 119 | Tiered self-improvement cadence and substrate-as-signal |
| 120 | RAG evolution: HyDE → Self-RAG → GraphRAG → Contextual Retrieval |

### Tier V — Code platform source-level teardowns (121-125)

| # | Title |
|---|---|
| 121 | Claude Code architecture teardown |
| 122 | Qwen Code / Qwen-Agent architecture teardown |
| 123 | Gemini Code / Gemini CLI teardown |
| 124 | Cursor / Aider / Cline / Continue / Roo / OpenHands teardown |
| 125 | Copilot Workspace / Devin / SWE-agent / Augment teardown |

### Tier W — GSPL intelligence design (126-131)

| # | Title |
|---|---|
| 126 | GSPL reasoning kernel (five-layer stack) |
| 127 | GSPL memory and context (four-tier on substrate namespaces) |
| 128 | GSPL tool-use and modifier-surface intelligence (four-layer action space) |
| 129 | GSPL self-improvement and evolution loop (four cadences) |
| 130 | GSPL neurosymbolic substrate binding (three surfaces, four mechanisms) |
| 131 | GSPL as a differentiable reasoning substrate (seven-axis structural claim + v0.1→v0.5 release arc) |

## Round 6.5 — Calibration close-out (briefs 132-151)

Round 6.5 is a 20-brief mini-round that closes every open follow-up from Round 6 so that Round 7 can start implementation without re-opening any architectural questions. Strict non-goals: no new substrate primitives, no new commitments, no new axes, no new namespaces, no code. Each brief is a calibration (X), empirical sizing (Y), recipe (Z), or operational (W) decision. 38 new inventions (INV-556..593). v0.1 scope frozen at 42 features with 17 explicit cuts. Read `round-6.5-synthesis.md` for the consolidated calibration tables and the v0.1 build-ready statement.

### Tier X — Calibration

| # | Title |
|---|---|
| 132 | Router classifier training data and labels |
| 133 | LATS value function: handcrafted vs learned |
| 137 | Multi-modal backbone selection (vision tower) |
| 138 | Compaction cadence calibration |
| 139 | Procedural promotion threshold tuning |
| 144 | Drift detector threshold calibration |
| 148 | World model formalization beyond Brief 131 |

### Tier Y — Empirical sizing

| # | Title |
|---|---|
| 135 | Hardware budget v0.1 + context ceiling |
| 140 | ColBERT storage budget at federation scale |
| 142 | Grammar compilation performance budget |
| 145 | GPU-time cost model |

### Tier Z — Recipes

| # | Title |
|---|---|
| 136 | Deep Research workflow recipe (v0.1 headline plugin) |
| 141 | Cross-encoder distillation recipe |
| 143 | Differentiable action learning recipe |
| 146 | JEPA predictive embedding dataset construction |

### Tier W — Operational

| # | Title |
|---|---|
| 134 | Substrate-native canonical benchmark battery |
| 147 | Federation-wide adapter review protocol |
| 149 | v0.1 scope finalization and feature cuts |
| 150 | External benchmark battery selection |
| 151 | Creator-facing communication of the seven axes |

## How to read this directory

If you are a human engineer:
- Start with `synthesis.md`. It tells you what changed and why.
- Read briefs 001–006 before writing any kernel code.
- Read briefs 007–010 before designing the export pipeline.
- Read briefs 011–012 before building the agent and evolution loops.
- Read `round-4-synthesis.md` and `round-5-synthesis.md` for the locked architecture and the ship-readiness posture across the 108 total briefs and 172 inventions in Rounds 4–5.
- Read `round-6-synthesis.md` for the seven-axis structural claim, the reasoning kernel, and the v0.1→v0.5 release arc across briefs 109-131.
- Read `round-6.5-synthesis.md` for the consolidated calibration tables, the cost model, the frozen v0.1 scope, the benchmark posture, and the creator-facing message — and the v0.1 build-ready statement that closes the architectural phase. **151 total briefs and 593 inventions through Round 6.5.**

If you are an AI coding agent:
- Each brief's `Recommendation` is your operating instruction for the relevant subsystem.
- Each brief's `Spec impact` lists files in the parent repo that take precedence over the brief if they conflict.
- Treat any finding with confidence ≤ 2 as a hard stop — surface it to the human and ask before proceeding.

## What is deliberately NOT in this directory

- **Build planning.** That belongs in `roadmap/`.
- **Architecture decisions.** Those belong in `adr/`. A brief can recommend an ADR but does not replace one.
- **Performance benchmarks against real hardware.** Those require Phase 1 infrastructure to be stood up first. The briefs cite published benchmarks where they exist and flag where empirical measurement is required.
- **Anything resolved by spec text already.** If the spec answers the question, it's not an open question.
