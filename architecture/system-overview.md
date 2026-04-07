# System Overview

Paradigm is a layered system. Each layer depends only on the layer below it, and each layer can be replaced independently as long as it preserves the interface contracts. This document gives the canonical layering, the data flows, and the invariants between layers.

## The Seven Layers

```
┌────────────────────────────────────────────────────────────┐
│  Layer 7 — Studio & Marketplace (UI, federation, payments) │
├────────────────────────────────────────────────────────────┤
│  Layer 6 — Intelligence (GSPL Agent, sub-agents, memory)   │
├────────────────────────────────────────────────────────────┤
│  Layer 5 — Evolution & Composition (GA, MAP-E, functors)   │
├────────────────────────────────────────────────────────────┤
│  Layer 4 — Domain Engines (26 developmental pipelines)     │
├────────────────────────────────────────────────────────────┤
│  Layer 3 — GSPL Language (lexer, parser, typecheck, codegen)│
├────────────────────────────────────────────────────────────┤
│  Layer 2 — Seed System (UniversalSeed, 17 gene types)      │
├────────────────────────────────────────────────────────────┤
│  Layer 1 — Kernel (RNG, FIM, tick cycle, effects)          │
└────────────────────────────────────────────────────────────┘
```

### Layer 1 — Kernel

The deterministic substrate. Owns the RNG (`xoshiro256**` + `SplitMix64` + `FNV-1a`), the Fisher Information seed manifold, the 8-phase tick cycle, the 8-effect algebraic effects system, and the deterministic scheduler. Has zero domain knowledge. See [`spec/03-kernel.md`](../spec/03-kernel.md).

**Public API surface:** `Kernel` interface (rngFromSeed, tick, withHandlers, approximateFim, canonicalize, hash, validate).

**Dependencies:** None above the language standard library and a SHA-256 implementation.

### Layer 2 — Seed System

The UniversalSeed schema, the 17 gene types with their operators, canonicalization, validation, signing, verification, and the `.gseed` binary format. Pure data plus pure functions over data. See [`spec/01-universal-seed.md`](../spec/01-universal-seed.md), [`spec/02-gene-system.md`](../spec/02-gene-system.md), [`spec/05-sovereignty.md`](../spec/05-sovereignty.md), [`spec/06-gseed-format.md`](../spec/06-gseed-format.md).

**Public API:** `UniversalSeed` type, `Gene` interface, `canonicalize`, `hash`, `sign`, `verify`, `mutate`, `breed`, `compose`, `distance`, `decode`, `encode`.

**Dependencies:** Layer 1 (uses Kernel for RNG and effects).

### Layer 3 — GSPL Language

Lexer, parser, type checker, optimizer, AST interpreter, WGSL code generator, and Language Server Protocol implementation. See [`spec/04-gspl-language.md`](../spec/04-gspl-language.md), [`language/grammar.ebnf`](../language/grammar.ebnf).

**Public API:** `parse`, `typeCheck`, `interpret`, `compileToWgsl`, plus an LSP-compatible server.

**Dependencies:** Layer 2 (the language operates on seeds and gene types).

### Layer 4 — Domain Engines

26 developmental pipelines, one per domain. Each implements the `DomainEngine` interface with a fixed sequence of stages. See [`architecture/engine-pattern.md`](engine-pattern.md), [`engines/README.md`](../engines/README.md).

**Public API:** `DomainEngine` interface (stages, validate, grow, render hints, export hints).

**Dependencies:** Layer 2 (engines consume seeds and gene values). May optionally consume Layer 3 if the engine uses GSPL expressions internally.

### Layer 5 — Evolution & Composition

The 7+ evolution algorithms (GA, MAP-Elites, CMA-ES, Novelty, AURORA, DQD, POET), the cross-domain functor registry, the refinement loop, and the QualityVector evaluator. See [`architecture/evolution-stack.md`](evolution-stack.md), [`architecture/cross-domain-composition.md`](cross-domain-composition.md), [`algorithms/refinement-loop.md`](../algorithms/refinement-loop.md).

**Public API:** `evolve(population, algorithm, fitness, ...)`, `compose(seed, target_domain | functor)`, `refine(seed, strategy)`.

**Dependencies:** Layer 4 (evolution evaluates fitness by growing seeds via engines).

### Layer 6 — Intelligence

The GSPL Agent's 5-stage Concept-to-Seed pipeline, the 8 sub-agents, the 4-layer memory system, the Template Bridge, and the multi-provider LLM abstraction. See [`intelligence/gspl-agent.md`](../intelligence/gspl-agent.md).

**Public API:** `parseIntent(natural_language) -> ParsedIntent`, `intentToSeed(intent) -> Seed`, `agentStep(state) -> next_state`, plus the LLM provider abstraction.

**Dependencies:** Layer 5 (the agent uses evolution and composition as primitive moves).

### Layer 7 — Studio & Marketplace

The Creation Studio (React UI), the marketplace backend (Express/Fastify, Stripe Connect, federation WebSocket), and the persistence layer (SQLite/PostgreSQL + Meilisearch + Qdrant). See [`architecture/studio-architecture.md`](studio-architecture.md), [`architecture/backend-architecture.md`](backend-architecture.md).

**Public API:** REST endpoints, WebSocket federation protocol, React component library.

**Dependencies:** Layer 6 (the studio is the human interface to the agent).

## Layering Rules

These are non-negotiable:

1. **A layer may only import from layers below it.** A Layer 4 engine may not call into Layer 5 evolution. If you need an engine to evolve internally, refactor: lift the loop into Layer 5.
2. **Lower layers know nothing about higher layers.** The kernel knows nothing about engines. The seed system knows nothing about the language. This is what lets the kernel be reused in non-Paradigm contexts.
3. **Cross-layer communication is via interfaces, not concrete types.** A new domain engine plugs in by implementing `DomainEngine`; the rest of the system doesn't need to know it exists.
4. **Effects are explicit at every layer.** Pure functions are pure all the way down. Side effects are confined to the kernel's effect system and propagate upward through declared effect annotations.

## The Two Entry Points

A user can enter the platform in exactly two ways:

```
        ┌──────────────────────────────────────────┐
        │              User Input                  │
        └────────────────┬─────────────────────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       ┌──────────────┐      ┌──────────────┐
       │  GSPL source │      │ Natural lang │
       │   (.gspl)    │      │   "warrior"  │
       └──────┬───────┘      └──────┬───────┘
              │                     │
              │ Layer 3             │ Layer 6
              │ (parser+typecheck)  │ (GSPL Agent)
              ▼                     ▼
       ┌──────────────────────────────────┐
       │         UniversalSeed            │
       │       (Layer 2 — canonical)      │
       └──────────────────┬───────────────┘
                          │
                          │ Layer 4 (engine)
                          ▼
                    ┌──────────┐
                    │ Artifact │
                    └──────────┘
```

Both entry points produce a UniversalSeed. Once a seed exists, all downstream operations are identical regardless of how it was created. This is why the GSPL language and the GSPL Agent are *peers* rather than one being built on top of the other.

## Data Flow Through a Single User Action

User clicks **"Generate a menacing iron warrior"** in the Studio:

```
1. Studio (L7)        → emit user prompt to Agent
2. Agent (L6)         → parseIntent("menacing iron warrior")
                        → ParsedIntent { domain: character, modifiers: [menacing, iron], ... }
                        → intentToSeed(intent)
                          → consult Template Bridge for "warrior" archetype
                          → apply adjective normalization for "menacing"
                          → assemble UniversalSeed
                          → kernel.hash + kernel.sign
3. Seed (L2)          → validated UniversalSeed
4. Engine (L4)        → character engine: grow(seed)
                          → stage 1: morphogenesis
                          → stage 2: personality
                          → stage 3: archetype rendering
                          → ... (7 stages total)
                          → Artifact { mesh, textures, animation, metadata }
5. Studio (L7)        → render artifact in viewport
6. User clicks "Evolve 50"
7. Evolution (L5)     → MAP-Elites with refinement-loop fitness
                          → spawn 50 mutants via gene operators (L2)
                          → grow each via engine (L4)
                          → evaluate quality (L5)
                          → archive elites (L5)
                          → return diverse population
8. User picks 2, clicks "Breed"
9. Seed (L2)          → breed(parentA, parentB)
10. Studio shows child, user clicks "Sign and publish"
11. Sovereignty (L2)  → seed already signed at step 2, but re-sign with current key
12. Marketplace (L7)  → publish to backend, index in Meilisearch + Qdrant
13. Backend (L7)      → emit to federation peers via WebSocket
```

Every step is deterministic given its inputs (with the exception of the LLM call inside the Agent at step 2, which is captured at the seed-creation boundary). The artifact at step 4 is bit-identical regardless of which machine produces it; the breeding at step 9 is bit-identical given the same parents.

## Where Each Repo File Belongs

- `spec/` — Layers 1, 2, 3 contracts.
- `architecture/` — How layers fit together.
- `engines/` — Layer 4 (each engine).
- `algorithms/` — Layer 5 algorithms.
- `intelligence/` — Layer 6.
- `infrastructure/` — Layer 7 (production stack, deployment).
- `language/` — Layer 3 grammar and stdlib.
- `adr/` — Cross-cutting decisions affecting multiple layers.

## Replacing a Layer

Each layer can be swapped:

- **Swap kernel:** rewrite Layer 1 in Rust + WASM, keep the same `Kernel` interface. The seed system and everything above it work unchanged.
- **Swap language:** add a Python or visual-block front-end in Layer 3. The seed system below and engines above don't change.
- **Swap engines:** ship a third-party fashion engine that conforms to `DomainEngine`. It plugs into the registry and the system uses it.
- **Swap evolution:** replace MAP-Elites with a custom algorithm; everything that consumes `evolve()` keeps working.
- **Swap intelligence:** plug a different LLM (Gemini → Claude → Ollama). The pipeline structure is unchanged.
- **Swap studio:** ship a CLI, a Figma plugin, a VS Code extension, or a native app. They all consume the same Layer 6 API.

This is what makes Paradigm a *platform* rather than a monolithic application. The contracts in `spec/` are the only things that can never be silently changed.
