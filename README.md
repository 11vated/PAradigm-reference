# GSPL Reference — The Genetic Operating Environment for Digital Creation

**A complete technical and conceptual reference for GSPL (Genetic Seed Programming Language) and the Paradigm platform.**

> This repository is the canonical reference an AI agent (or a human) needs to understand, design, and rebuild the Paradigm GSPL Engine from first principles. It is intended to be exhaustive enough that a capable agent — given this repo and nothing else — can produce a working MVP of every layer of the platform.

— Kahlil Stephens, 11vatedTech LLC · April 2026

---

## What Paradigm Is, In One Paragraph

Paradigm introduces **Genetically Organized Evolution (GOE)** — a computational paradigm in which every digital artifact (images, 3D models, animations, games, music, simulations, stories, interfaces, designs) is encoded as a **living genetic blueprint called a seed**. Seeds are not files. They are genetic programs that unfold through developmental stages the way a fertilized cell unfolds into a complete organism. A seed does not *describe* an artifact — it **grows** one. Same seed + same deterministic RNG + same engine = bit-identical artifact on any machine, forever. From that determinism comes everything else: breeding, lineage, cryptographic sovereignty, marketplace royalties, and cross-domain composition via category theory.

## The Five Core Inventions

1. **The UniversalSeed** — a single data structure that can encode any creative artifact across 26 domains. See [`spec/01-universal-seed.md`](spec/01-universal-seed.md).
2. **The 17-Type Gene System** — a novel type theory where each gene type has its own mutation, crossover, distance, and validation operators. See [`spec/02-gene-system.md`](spec/02-gene-system.md).
3. **Deterministic Developmental Engines** — 26 domain engines that grow seeds into artifacts through staged pipelines. See [`engines/README.md`](engines/README.md).
4. **Category-Theoretic Cross-Domain Composition** — functor bridges that let a character seed become a sprite, a song, or a full game. See [`architecture/cross-domain-composition.md`](architecture/cross-domain-composition.md).
5. **Embedded Cryptographic Sovereignty** — ECDSA P-256 signatures baked into the seed itself, not a database, not a blockchain. See [`spec/05-sovereignty.md`](spec/05-sovereignty.md).

## Repository Map

```
gspl-reference/
├── README.md                     ← you are here
├── GLOSSARY.md                   ← every term defined
├── LICENSE                       ← open spec license
├── CONTRIBUTING.md
│
├── spec/                         ← formal specifications (the spine)
│   ├── 00-overview.md
│   ├── 01-universal-seed.md
│   ├── 02-gene-system.md
│   ├── 03-kernel.md
│   ├── 04-gspl-language.md
│   ├── 05-sovereignty.md
│   ├── 06-gseed-format.md
│   └── 07-determinism.md
│
├── architecture/                 ← how the layers fit together
│   ├── system-overview.md
│   ├── engine-pattern.md
│   ├── evolution-stack.md
│   ├── cross-domain-composition.md
│   ├── intelligence-layer.md
│   ├── studio-architecture.md
│   ├── backend-architecture.md
│   └── 14-technical-pillars.md
│
├── engines/                      ← 26 domain engines (15 built, 11 planned)
│   ├── README.md
│   ├── _template.md
│   ├── character.md  sprite.md  music.md  fullgame.md  animation.md
│   ├── procedural.md  geometry3d.md  narrative.md  ui.md  physics.md
│   ├── visual2d.md  audio.md  ecosystem.md  game.md  alife.md
│   └── planned/
│       ├── shader.md  particle.md  typography.md  architecture.md
│       ├── vehicle.md  furniture.md  fashion.md  robotics.md
│       ├── circuit.md  food.md  choreography.md
│
├── language/                     ← GSPL language spec
│   ├── grammar.ebnf
│   ├── keywords.md
│   ├── type-system.md
│   ├── stdlib.md
│   └── examples/
│
├── algorithms/                   ← pseudocode for all load-bearing math
│   ├── xoshiro256.md
│   ├── fisher-information-matrix.md
│   ├── map-elites.md
│   ├── cma-es.md
│   ├── novelty-search.md
│   ├── aurora.md  dqd.md  poet.md
│   ├── refinement-loop.md
│   ├── functor-composition.md
│   └── marching-cubes.md
│
├── adr/                          ← architecture decision records
│   └── 001..011 — why 17 types, why ECDSA, why category theory, etc.
│
├── intelligence/                 ← the GSPL Agent
│   ├── gspl-agent.md
│   ├── 8-sub-agents.md
│   ├── memory-system.md
│   ├── template-bridge.md
│   ├── adjective-normalization.md
│   └── intent-taxonomy.md
│
├── infrastructure/               ← production stack decisions
│   ├── library-canon.md
│   ├── production-stack.md
│   ├── deployment-architecture.md
│   ├── gpu-compute-strategy.md
│   ├── database-architecture.md
│   └── monitoring-and-observability.md
│
├── compliance/                   ← regulatory obligations
│   ├── c2pa-integration.md
│   ├── eu-ai-act-article-50.md
│   ├── california-sb-942.md
│   └── wcag-2-1-aa.md
│
├── roadmap/                      ← what to build in what order
│   ├── mvp-build-order.md
│   ├── phase-1-kernel.md
│   ├── phase-2-engines.md
│   ├── phase-3-studio-intelligence.md
│   ├── phase-4-marketplace.md
│   └── phase-5-federation.md
│
├── examples/                     ← runnable reference material
│   ├── gspl/                     ← sample .gspl programs
│   ├── seeds/                    ← sample .gseed files (JSON-rendered)
│   └── agent-prompts/            ← prompt → expected seed pairs
│
├── tests/                        ← canonical test contracts
│   ├── determinism-tests.md
│   ├── sovereignty-tests.md
│   ├── composition-laws.md
│   └── property-tests.md
│
├── research/                     ← technical R&D briefs (round 1: 12 briefs + synthesis)
│   ├── README.md                 ← charter, methodology, brief template
│   ├── 001-gpu-determinism-cross-vendor.md
│   ├── 002-wgsl-portable-subset.md
│   ├── 003-jcs-canonicalization-edge-cases.md
│   ├── 004-rfc6979-ecdsa-p256.md
│   ├── 005-zstd-deterministic-encoding.md
│   ├── 006-hm-refinements-feasibility.md
│   ├── 007-c2pa-rs-library-maturity.md
│   ├── 008-image-dct-watermark-robustness.md
│   ├── 009-audiowmark-robustness.md
│   ├── 010-eu-ai-act-2026.md
│   ├── 011-agent-reliability-backstops.md
│   ├── 012-map-elites-convergence.md
│   └── synthesis.md              ← cross-brief findings, spec impact, Phase 1 deltas
│
├── codebase/                     ← mirrored existing production source
│   └── README.md                 ← how to populate this directory
│
└── scripts/
    └── mirror-codebase.sh        ← copies Paradigm_engine source into /codebase
```

## How to Read This Repo

**If you are an AI agent tasked with rebuilding Paradigm from scratch, read in this order:**

1. [`GLOSSARY.md`](GLOSSARY.md) — pin the vocabulary.
2. [`spec/00-overview.md`](spec/00-overview.md) — what Paradigm *is*.
3. [`spec/01-universal-seed.md`](spec/01-universal-seed.md) — the atomic data structure.
4. [`spec/02-gene-system.md`](spec/02-gene-system.md) — the 17 gene types.
5. [`spec/03-kernel.md`](spec/03-kernel.md) — determinism, tick cycle, effects.
6. [`spec/04-gspl-language.md`](spec/04-gspl-language.md) + [`language/grammar.ebnf`](language/grammar.ebnf) — the language.
7. [`spec/05-sovereignty.md`](spec/05-sovereignty.md) — cryptographic identity.
8. [`architecture/system-overview.md`](architecture/system-overview.md) — the layered architecture.
9. [`architecture/engine-pattern.md`](architecture/engine-pattern.md) — how all 26 engines look.
10. [`architecture/evolution-stack.md`](architecture/evolution-stack.md) — GA, MAP-Elites, CMA-ES, Novelty, AURORA, DQD, POET.
11. [`architecture/cross-domain-composition.md`](architecture/cross-domain-composition.md) — category-theoretic functors.
12. [`intelligence/gspl-agent.md`](intelligence/gspl-agent.md) — the Concept-to-Seed pipeline.
13. [`roadmap/mvp-build-order.md`](roadmap/mvp-build-order.md) — what to build first.
14. Deep dive: `engines/`, `algorithms/`, `adr/`.
15. **Before writing any kernel, proof, agent, or evolution code, read [`research/synthesis.md`](research/synthesis.md) and the relevant briefs in [`research/`](research/).** Round 1 of the technical R&D resolved twelve load-bearing open questions and identified normative spec changes (most importantly: the content hash domain is the *uncompressed* canonical payload, not the compressed bytes).

**If you are a human contributor:** start at [`spec/00-overview.md`](spec/00-overview.md) and follow your interest.

## MVP Definition

A Paradigm MVP means: a user writes a GSPL program **or** a natural-language prompt → the GSPL Agent parses it into a UniversalSeed → the appropriate domain engine grows the seed into an artifact → the renderer displays it → the user can evolve a population of variants → breed the best ones → sign them with cryptographic sovereignty → export to a standard format. End-to-end, deterministic, verifiable. See [`roadmap/mvp-build-order.md`](roadmap/mvp-build-order.md) for the exact sequence.

## License

This reference is released under the [GSPL Open Specification License](LICENSE) — free to implement, free to fork, free to extend. The intent is to establish the `.gseed` format and the 17-type gene system as an open public standard.

## Status

This is a living document. The reference repo is maintained alongside the production codebase at [`codebase/`](codebase/) (182,471 lines of TypeScript, 2,807 tests, 0 compilation errors as of April 2026). See [`codebase/README.md`](codebase/README.md) for the mirror process.

---

*"You cannot copy a genetic library. You can only grow one."*
