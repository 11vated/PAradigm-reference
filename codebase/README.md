# Codebase Manifest

This directory is the bridge between the *spec* in this repo and the *existing prototype* that lives in parallel folders inside `Paradigm_GSPL_Engine/`. The spec is the source of truth for the v1 rebuild, but the prototype is the practical reference for "what already works" and "what was tried."

The prototype is **not mirrored byte-for-byte** into this repo for two reasons: (1) it is large and contains many transient build artifacts, and (2) the v1 rebuild described in `/roadmap` is intentionally *not* a refactor of the prototype but a clean-slate implementation of the spec. The prototype is preserved as historical reference, not a production codebase.

## Where the prototype lives

```
Paradigm_GSPL_Engine/
├── Paradigm_engine/                  ← TypeScript prototype (main)
│   ├── src/
│   │   ├── ai/                       Agent and intelligence prototypes
│   │   ├── alife/                    Artificial life experiments
│   │   ├── api/                      HTTP API surface
│   │   ├── composition/              Cross-domain composition
│   │   ├── desktop/                  Desktop wrapper
│   │   ├── engines/                  Domain engine implementations
│   │   ├── evolution/                Evolution algorithms
│   │   └── formats/                  Export format encoders
│   ├── studio/                       Studio web app
│   ├── seeds/                        Sample seed JSONs
│   ├── examples/                     Sample programs
│   ├── docs/                         Prototype documentation
│   ├── backend/                      Server-side code
│   └── prototypes_Research_only/     Research prototypes (not production)
│
├── Paradigm_GSPL_GOE_OS/             ← Documentation set
│   ├── 00_INDEX.md
│   ├── 01_EXECUTIVE_VISION.md
│   ├── 02_GSPL_LANGUAGE_SPECIFICATION.md
│   ├── 03_SEED_ARCHITECTURE.md
│   ├── 04_DOMAIN_ENGINES.md
│   ├── 05_EVOLUTION_SYSTEM.md
│   ├── 06_PLATFORM_ARCHITECTURE.md
│   ├── 07_ECONOMIC_MODEL.md
│   ├── 08_SOVEREIGNTY_FRAMEWORK.md
│   ├── 09_MARKETPLACE.md
│   ├── 10_API_REFERENCE.md
│   ├── 11_STUDIO_DOCUMENTATION.md
│   ├── 12_CROSS_DOMAIN_COMPOSITION.md
│   ├── 13_INTELLIGENCE_LAYER.md
│   ├── 14_MATHEMATICAL_FOUNDATIONS.md
│   ├── 15_ARTIFICIAL_LIFE.md
│   ├── 16_DEPLOYMENT_INFRASTRUCTURE.md
│   ├── 17_DEVELOPER_GUIDE.md
│   ├── 18_ROADMAP_VISION.md
│   └── 19_GLOSSARY.md
```

## Mapping prototype → spec

| Prototype location | Spec location |
|---|---|
| `Paradigm_engine/src/ai/` | `intelligence/` (8 sub-agents, memory, templates, taxonomy) |
| `Paradigm_engine/src/alife/` | `engines/alife.md`, `engines/ecosystem.md` |
| `Paradigm_engine/src/api/` | `architecture/api-surface.md`, `infrastructure/production-stack.md` |
| `Paradigm_engine/src/composition/` | `algorithms/functor-composition.md`, `architecture/composition.md` |
| `Paradigm_engine/src/engines/` | `engines/_template.md` and the 26 engine specs |
| `Paradigm_engine/src/evolution/` | `algorithms/{ga,map-elites,cma-es,novelty-search,aurora,dqd,poet}.md` |
| `Paradigm_engine/src/formats/` | `infrastructure/gseed-format.md`, export format docs |
| `Paradigm_engine/studio/` | `roadmap/phase-4-intelligence.md` §"Studio" |
| `Paradigm_engine/seeds/` | `examples/*.gseed.json` (canonical seeds) |
| `Paradigm_engine/backend/` | `infrastructure/production-stack.md`, `infrastructure/db-schema.md` |
| `Paradigm_GSPL_GOE_OS/02_GSPL_LANGUAGE_SPECIFICATION.md` | `language/grammar.ebnf`, `language/keywords.md`, `language/types.md` |
| `Paradigm_GSPL_GOE_OS/03_SEED_ARCHITECTURE.md` | `spec/seed.md`, `spec/genes.md` |
| `Paradigm_GSPL_GOE_OS/04_DOMAIN_ENGINES.md` | `engines/` directory |
| `Paradigm_GSPL_GOE_OS/05_EVOLUTION_SYSTEM.md` | `algorithms/` directory |
| `Paradigm_GSPL_GOE_OS/08_SOVEREIGNTY_FRAMEWORK.md` | `spec/sovereignty.md`, ADRs 002-004 |
| `Paradigm_GSPL_GOE_OS/12_CROSS_DOMAIN_COMPOSITION.md` | `algorithms/functor-composition.md`, ADR-008 |
| `Paradigm_GSPL_GOE_OS/13_INTELLIGENCE_LAYER.md` | `intelligence/` directory |
| `Paradigm_GSPL_GOE_OS/14_MATHEMATICAL_FOUNDATIONS.md` | `algorithms/fisher-information.md`, math sections in engine docs |
| `Paradigm_GSPL_GOE_OS/16_DEPLOYMENT_INFRASTRUCTURE.md` | `infrastructure/` directory |
| `Paradigm_GSPL_GOE_OS/19_GLOSSARY.md` | `spec/glossary.md` |

## Where the prototype agrees with the spec

The prototype and the spec agree on:

- The 7-layer architecture
- The seed system as the central data structure
- ECDSA P-256 + JCS canonicalization for sovereignty
- The staged-pipeline pattern for engines
- MAP-Elites as the default evolution algorithm
- Cross-domain functors as the composition primitive
- The 5-stage Concept-to-Seed pipeline
- The 4-layer memory system
- C2PA compliance for exports
- Postgres + Redis + Fastify backend stack

## Where the spec diverges from the prototype

The spec deliberately diverges from the prototype in these places:

1. **Language is Rust + WGSL for engines, not TypeScript.** The prototype is fully TypeScript. The spec calls for hot paths in Rust with WGSL GPU kernels for determinism and performance. This is the single biggest engineering shift.

2. **GSPL is a parsed language, not a JSON DSL.** The prototype represents seeds as JSON and treats "GSPL programs" informally. The spec defines GSPL as a real language with a grammar, type checker, and IR.

3. **Algebraic effects are explicit.** The prototype mostly assumes purity. The spec makes effects part of the type system and tracks them through the compiler.

4. **6 engines for v1, not 26.** The prototype attempts breadth across all 26 engines. The spec ships only 6 in v1 and treats the other 20 as post-launch.

5. **Federation is a v1 feature, not a v0 feature.** The prototype's federation is partial and untested at scale. The spec defers federation to Phase 5 and specs the protocol cleanly.

6. **`.gseed` binary format is normative.** The prototype has multiple ad hoc seed file formats. The spec defines `.gseed` as *the* canonical container.

7. **Compliance is built in from day one.** The prototype has C2PA support in some paths. The spec requires C2PA + watermarking on every export, no opt-out.

8. **Studio is built on Radix, not from scratch.** The prototype uses custom UI components. The spec specifies Radix primitives with a hard accessibility budget.

## Use of the prototype

The prototype is useful as:

- **Concrete examples of intent.** When the spec says "the engine produces a quality vector," the prototype's `src/engines/sprite/quality.ts` is a worked example of *what* a quality vector looks like in practice.
- **Reference implementations of algorithms.** The prototype's CMA-ES, MAP-Elites, and Marching Cubes implementations can be ported to Rust as a starting point.
- **Test fixtures.** The prototype's `seeds/` directory contains hundreds of sample seeds that can become regression test inputs.
- **UI patterns.** The prototype's Studio is the most direct guide to "what a Paradigm interface feels like."
- **Documentation cross-reference.** The prototype's docs (in `Paradigm_engine/*.md` and `Paradigm_GSPL_GOE_OS/*`) are useful as second opinions on concepts the spec covers.

The prototype is *not* useful as:

- A starting codebase. The v1 rebuild starts from an empty repo (see `roadmap/phase-1-kernel.md`).
- The source of truth on architecture. The spec is authoritative.
- A reference for performance. The prototype's TypeScript engines are 10-100× slower than the Rust engines specified for v1.

## Migration of artifacts

The following prototype artifacts will be migrated *as data*, not as code:

- All sample seeds in `Paradigm_engine/seeds/` will be re-canonicalized through the v1 kernel and stored as test fixtures in `tests/golden-seeds/`.
- All sample GSPL programs in `Paradigm_engine/examples/` will be ported to the v1 GSPL grammar and stored alongside `examples/` in this repo.
- The prototype's lineage tree (which seeds derived from which) will be preserved in the migration so authorship is not lost.
- The prototype's documentation will be cross-referenced from the spec where useful but not duplicated.

A migration script (`tools/migrate-from-prototype.ts`) will be written in Phase 1 week 8 to perform the canonicalization.

## What is *not* in `/codebase`

This directory is intentionally manifest-only. The actual source files of the prototype remain in `Paradigm_engine/` and `Paradigm_GSPL_GOE_OS/`, where they belong. Copying them into `gspl-reference/codebase/` would create a maintenance trap (two copies that can drift) and would inflate this repo by hundreds of MB of build artifacts and `node_modules`.

If you are an agent (Gemini, Claude, or otherwise) reading this repo to plan a build, you should:

1. **Read the spec first** — the entire `gspl-reference/` tree.
2. **Treat the prototype as worked examples** — read individual files when you need to see "how was this done in practice."
3. **Build to the spec, not the prototype.** When the two disagree, the spec wins.
