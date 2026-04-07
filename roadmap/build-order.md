# Build Order

## The dependency graph

```
                              ┌──────────────────┐
                              │  L6: Marketplace │
                              │   + Federation   │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │   L5: Studio     │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │  L4: Intelligence│
                              │  (GSPL Agent)    │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │  L3: Evolution   │
                              │  + Composition   │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │ L2: Domain       │
                              │     Engines      │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │ L1: GSPL         │
                              │  Language        │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │ L0a: Seed System │
                              │  + Sovereignty   │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │ L0: Kernel       │
                              │ (RNG, JCS, sigs) │
                              └──────────────────┘
```

Each layer is built only after its predecessor is feature-complete and tested. Within a layer, components are built in the order their internal docs specify.

## Layer-by-layer

### L0 — Kernel (Phase 1 weeks 1-3)

- `kernel/rng.rs` — DeterministicRng (xoshiro256** + splitmix64 + Box-Muller)
- `kernel/canonical.rs` — JCS canonicalization
- `kernel/effects.rs` — Algebraic effect runtime
- `kernel/hash.rs` — SHA-256 wrapper, RFC 7638 thumbprint
- `kernel/sign.rs` — ECDSA P-256 (RFC 6979 deterministic)
- Tests: 1000+ unit tests, property-based with proptest, byte-level reproducibility tests

**Exit criterion:** every test passes, two independent runs produce byte-identical output, the kernel public API is frozen.

### L0a — Seed System + Sovereignty (Phase 1 weeks 4-7)

- `seeds/types.rs` — UniversalSeed + 17 gene types
- `seeds/canonical.rs` — Canonical JSON form
- `seeds/sign.rs` — Sign / verify a seed
- `seeds/lineage.rs` — Lineage edge structures
- `seeds/quality.rs` — QualityVector
- `seeds/serde.rs` — `.gseed` writer + reader
- Tests: full round-trip on 100 sample seeds; signature verification matches across machines

**Exit criterion:** `.gseed` files are interchangeable across two independent reference implementations.

### L1 — GSPL Language (Phase 2 months 3-4)

Built in this order:

1. Lexer (chumsky)
2. Parser → AST
3. Name resolver
4. Type checker (Hindley-Milner + refinements)
5. Effect checker
6. IR lowering
7. WGSL/Rust codegen for the first engine target
8. Standard library (`Std.*` modules)
9. Compiler driver + diagnostics

**Exit criterion:** the canonical "Sprite of a melancholy bard" example program compiles and runs against a stub Sprite engine.

### L2 — Domain Engines (Phase 3 months 5-7)

Six engines for v1, in this order (chosen to maximize learning while exercising the staged-pipeline pattern):

1. **Sprite** — 2D, simplest
2. **Texture** — 2D, image-space
3. **Sculpt** — 3D mesh, exercises Marching Cubes
4. **Music** — audio, exercises non-visual domain
5. **Particles** — exercises GPU compute path
6. **Animation** — exercises temporal sequencing + IK

Each engine follows `engines/_template.md`. Engines are built one at a time; the second is faster than the first because shared infrastructure (the staged-pipeline runner, CPU/GPU dispatch, hashing) is reused.

**Exit criterion:** each engine can ingest a seed and produce a deterministic, hashed output that round-trips through `.gseed`.

### L3 — Evolution + Composition (Phase 3 month 7, parallel with last engine)

- `evolution/ga.rs` — base genetic algorithm
- `evolution/map_elites.rs` — MAP-Elites (the default)
- `evolution/novelty.rs` — Novelty Search
- `evolution/cma_es.rs` — CMA-ES for continuous gene refinement
- `evolution/bandit.rs` — UCB1 mutation operator selector
- `composition/functor.rs` — functor registry + Dijkstra path
- Tests: golden tests over 50-step evolution runs; same seed → same output

**Exit criterion:** running 100 generations of MAP-Elites on a sprite seed produces a stable, browsable archive in <30s on a single core.

### L4 — Intelligence (Phase 4 months 8-10)

- `agent/intent_classifier.rs` — Stage 1
- `agent/spec_resolver.rs` — Stage 2
- `agent/planner.rs` — Stage 3
- `agent/assembler.rs` — Stage 4
- `agent/validator.rs` — Stage 5
- `agent/sub_agents/*` — 8 specialist sub-agents
- `agent/memory/*` — 4-layer memory system
- `agent/templates/*` — Template Bridge
- `agent/normalizer.rs` — Adjective normalization
- LLM provider integrations: Anthropic (primary), OpenAI (fallback)

**Exit criterion:** the canonical "melancholy bard" prompt produces a high-quality sprite seed end-to-end in <12s.

### L5 — Studio (Phase 4 month 10, parallel with agent polish)

- React + Vite scaffolding
- Auth (passkeys via @simplewebauthn)
- Project list + project view
- Seed gallery
- Seed detail view (gene tree + 3D viewport)
- Agent chat panel
- Evolution panel (start a run, browse archive)
- Export panel (PNG/JPEG/GLB/etc.)
- Accessibility pass

**Exit criterion:** a brand-new user can create their first seed in under 60 seconds with no documentation.

### L6 — Marketplace + Federation (Phase 5 months 11-12)

- Marketplace tables + APIs
- Stripe Connect onboarding
- Listing UI in Studio
- Buy flow with C2PA-signed receipts
- Royalty distribution worker
- Federation peer protocol
- Federation gateway (uWebSockets.js)
- Public verifier tool (`/verify`)
- Public seed pages (`/s/<hash>`)
- Launch landing page

**Exit criterion:** an external user can list a seed, sell it, and have royalties distributed automatically across the lineage tree; a second Paradigm node can subscribe to the first and import seeds.

## Parallel work streams

The critical path is fully sequential, but several non-blocking workstreams can run alongside:

- **Documentation** runs throughout. Every layer's spec is written in this repo before any code, and tutorial docs are written as features land.
- **Infrastructure / DevOps** can be built ahead of time. The Postgres schema, Docker setup, CI pipeline, and observability stack can be in place by the end of Phase 1.
- **Compliance** plumbing (C2PA library wrappers, watermarking research) can be done in Phase 2-3 even before the engines that need it exist.
- **Test fixtures** are written alongside their target code, never after.

## Shippable intermediate states

If development pauses at any phase boundary, what exists is a complete product:

- **End of Phase 1:** A signing and seed library that other developers can use as a standalone crate. Useful for any project that wants reproducible cryptographically signed structured data.
- **End of Phase 2:** GSPL — a deterministic creative DSL with one reference engine. Usable as a standalone tool by sprite-pipeline enthusiasts.
- **End of Phase 3:** A complete creative-evolution toolkit with six domain engines and MAP-Elites. Equivalent in capability to many academic ALife systems.
- **End of Phase 4:** A working AI creative tool — Studio + Agent — that takes natural language and produces signed exports. This is the MVP.
- **End of Phase 5:** v1.0 — a federated marketplace platform with all of the above plus economic mechanics.

This phasing provides multiple valid stopping points and graceful failure modes.
