# The 14 Technical Pillars

Paradigm rests on 14 technical pillars. Each one is necessary; none is sufficient. The platform's identity comes from how they fit together. This document names each pillar, states what it provides, where it lives in the layered architecture, and why removing it would collapse the system.

| # | Pillar | Layer | Status |
|---|---|---|---|
| 1 | Deterministic Kernel | L1 | Implemented |
| 2 | Universal Seed Schema | L2 | Implemented |
| 3 | 17-Type Gene System | L2 | Implemented |
| 4 | GSPL Language | L3 | Partially implemented |
| 5 | Domain Engine Pattern | L4 | 15 of 26 implemented |
| 6 | Quality-Diversity Evolution | L5 | Implemented |
| 7 | Cross-Domain Functor Composition | L5 | 9 functors registered |
| 8 | Refinement Loop with QualityVector | L5 | Implemented |
| 9 | GSPL Agent (Concept-to-Seed) | L6 | Designed, partial implementation |
| 10 | Sovereignty (Sign / Verify / Royalty) | L2 | Implemented |
| 11 | `.gseed` Binary Format | L2 | Implemented |
| 12 | Federation (WebSocket Island Model) | L7 | Designed |
| 13 | GPU Compute (WebGPU) | L4/L5 | Partial |
| 14 | C2PA Compliance | L7 | Required for ship |

## Pillar 1 — Deterministic Kernel

**What:** A pure-function substrate of RNG (`xoshiro256**` + `splitmix64` + Box–Muller normal sampling), the Fisher Information seed manifold, the 8-phase tick cycle, and the 8 algebraic effects (`Read`, `Write`, `Random`, `Time`, `Network`, `GPU`, `Log`, `Sign`).

**Provides:** The bit-level reproducibility that everything else depends on.

**If removed:** Lineage breaks (you can't audit a chain you can't replay). Royalties break (you can't prove which ancestors contributed). Federation breaks (peers can't verify each other's claims). Marketplace fraud detection breaks. The system collapses into "another generative AI tool."

**Spec:** [`spec/03-kernel.md`](../spec/03-kernel.md), [`spec/07-determinism.md`](../spec/07-determinism.md).

## Pillar 2 — Universal Seed Schema

**What:** The single typed JSON object that describes any creative artifact across all 26 domains. Includes lineage edges, sovereignty signatures, content hash, and gene table.

**Provides:** A *unified* representation that lets the same algorithms (mutate, breed, evolve, compose) work for sprites, music, characters, games, and 22 other domains without per-domain rewrites.

**If removed:** Each domain becomes its own silo. Cross-domain composition is impossible. The marketplace can't be uniform. Tooling fragments.

**Spec:** [`spec/01-universal-seed.md`](../spec/01-universal-seed.md).

## Pillar 3 — 17-Type Gene System

**What:** Seventeen primitive gene types (scalar, categorical, vector, expression, struct, array, graph, topology, temporal, regulatory, field, symbolic, quantum, gematria, resonance, dimensional, sovereignty), each with mutate/crossover/distance/validate/canonicalize operators.

**Provides:** A complete vocabulary for expressing any artifact's parameters in a way that can be evolved, compared, and traded.

**If removed:** Engines have to invent their own parameter types. Evolution operators become per-engine. Cross-domain functors lose a common type system to map between.

**Spec:** [`spec/02-gene-system.md`](../spec/02-gene-system.md).

## Pillar 4 — GSPL Language

**What:** A typed, deterministic, GPU-aware DSL for declaring seeds, defining engines, expressing gene grammars, and writing fitness functions. Includes parser, type checker (Hindley-Milner + refinements + dependent types + effect polymorphism), AST interpreter, and WGSL code generator. 26 keywords.

**Provides:** A *human-writable* alternative to natural language for users who want fine control. The same seeds can be authored in GSPL or via the Agent.

**If removed:** The platform is at the mercy of the LLM forever. Power users can't write deterministic generators. Engines must be implemented in TypeScript only.

**Spec:** [`spec/04-gspl-language.md`](../spec/04-gspl-language.md), grammar in [`language/grammar.ebnf`](../language/grammar.ebnf).

## Pillar 5 — Domain Engine Pattern

**What:** A uniform interface (`DomainEngine`) and a staged-pipeline pattern that all 26 domain engines implement. Stages are pure, typed, deterministic, and compositional.

**Provides:** Engines are interchangeable, third parties can ship new engines in days, the same operators (validate, grow, render hint, export hint) work for every domain.

**If removed:** Engine sprawl. Each engine becomes a snowflake. Adding a 16th engine takes weeks. The platform stops scaling.

**Spec:** [`architecture/engine-pattern.md`](engine-pattern.md), per-engine specs in [`engines/`](../engines/).

## Pillar 6 — Quality-Diversity Evolution

**What:** Seven evolution algorithms (GA, MAP-Elites, CMA-ES, Novelty Search, AURORA, DQD, POET) sharing a common interface. The default is MAP-Elites because *galleries beat single answers*.

**Provides:** When the user clicks "Evolve 50," they get 50 *diverse* high-quality results, not 50 copies of one local optimum.

**If removed:** The studio becomes "generate one thing, regenerate, regenerate, regenerate" — exactly the fatigue pattern that haunts current generative tools.

**Spec:** [`architecture/evolution-stack.md`](evolution-stack.md), pseudocode in [`algorithms/`](../algorithms/).

## Pillar 7 — Cross-Domain Functor Composition

**What:** A category-theoretic registry of typed functors mapping seeds across domains, with shortest-path BFS resolution and 6 verifiable laws (determinism, hash consistency, lineage propagation, identity, associativity, no information fabrication).

**Provides:** "Make a character with a theme song and a level designed around them" works as a single composition, not as three disconnected generators.

**If removed:** Cross-domain creation requires manual handoffs. The platform feels like 26 disconnected tools instead of one unified one.

**Spec:** [`architecture/cross-domain-composition.md`](cross-domain-composition.md).

## Pillar 8 — Refinement Loop with QualityVector

**What:** A 6-dimensional fitness model (geometry, texture, animation, coherence, style, novelty) and an 8-strategy mutation bandit (UCB1) that learns which mutation strategy works best for the current seed and domain.

**Provides:** Evolution loops know what "better" means in a way that aligns with human aesthetics, not just one scalar.

**If removed:** Evolution optimizes for whatever single metric you pick, and the result is mediocre by every other axis. Quality stagnates.

**Spec:** [`algorithms/refinement-loop.md`](../algorithms/refinement-loop.md).

## Pillar 9 — GSPL Agent (Concept-to-Seed)

**What:** A 5-stage pipeline (Parse → Resolve → Plan → Assemble → Validate) plus 8 sub-agents (Vision, Personality, MusicTheory, Mechanics, Narrative, Physics, Style, Critique) plus 4-layer memory plus the Template Bridge with 26+ archetypes per domain.

**Provides:** Natural-language input. Without it, the user has to write GSPL. With it, "menacing iron warrior" is enough.

**If removed:** The market shrinks from "anyone with an idea" to "developers who know GSPL." The TAM collapses by 99%.

**Spec:** [`architecture/intelligence-layer.md`](intelligence-layer.md), [`intelligence/`](../intelligence/).

## Pillar 10 — Sovereignty (Sign / Verify / Royalty)

**What:** ECDSA P-256 signatures (RFC 6979 deterministic), JCS canonicalization (RFC 8785), JWK identity (RFC 7517 + 7638 thumbprint), and a recursive royalty propagation algorithm with diminishing per-generation rates.

**Provides:** A user can prove they made a seed. Buyers can verify lineage. Royalties flow to ancestors automatically when descendants sell. The economic model has cryptographic teeth.

**If removed:** No marketplace. No incentive to publish. No way to attribute breeding. The system is a free-for-all that nobody trusts.

**Spec:** [`spec/05-sovereignty.md`](../spec/05-sovereignty.md).

## Pillar 11 — `.gseed` Binary Format

**What:** A compact, schema-validated, tamper-evident, streamable binary envelope (Magic `GSED`, length-prefixed, SHA-256 protected, MessagePack payload, optional zstd compression, optional appendix for C2PA / signatures / attestations).

**Provides:** A canonical at-rest representation. Files are 2–4× smaller than JSON, decode failures are typed, integrity is verified before use.

**If removed:** Seeds float around as JSON, sizes balloon, decode is fragile, tampering is undetectable, and there's no good way to attach C2PA manifests to seeds.

**Spec:** [`spec/06-gseed-format.md`](../spec/06-gseed-format.md).

## Pillar 12 — Federation (WebSocket Island Model)

**What:** A small-world peer graph where each Studio runs its own evolution loop on a sub-population (an "island") and periodically exchanges 1–5% of elites with neighbors. Migration messages are signed, content-addressed, and verified on receipt.

**Provides:** Cross-cultural style mixing, planet-scale genetic library, no central server bottleneck. Effects no single instance can produce alone.

**If removed:** Each user's creative space is an island. Discovery dies. The "genetic library" stays local. Network effects evaporate.

**Spec:** [`architecture/evolution-stack.md`](evolution-stack.md) §Federation, server side in [`architecture/backend-architecture.md`](backend-architecture.md) §Federation.

## Pillar 13 — GPU Compute (WebGPU)

**What:** WGSL kernels for fitness evaluation, generated from `@gpu`-annotated GSPL functions or hand-written. The studio detects WebGPU support and dispatches batches of seeds to compute shaders.

**Provides:** 10–50× speedup on fitness evaluation, which is the bottleneck of every evolution loop. Without it, interactive evolution at 50-pop is sluggish; with it, it's sub-second.

**If removed:** Evolution happens overnight, not interactively. The "describe and watch evolution" UX is gone.

**Spec:** [`architecture/evolution-stack.md`](evolution-stack.md) §GPU Acceleration, kernels in [`infrastructure/gpu-kernels.md`](../infrastructure/gpu-kernels.md).

## Pillar 14 — C2PA Compliance

**What:** Every generated artifact embeds a Coalition for Content Provenance and Authenticity manifest declaring it as AI-generated, listing the model lineage, and binding the manifest to a signature.

**Provides:** Legal compliance with EU AI Act Article 50 (effective August 2026) and California SB 942 (effective January 2026), plus alignment with the broader provenance movement.

**If removed:** The platform cannot legally operate in the EU or California. Distribution to enterprise customers becomes impossible.

**Spec:** [`compliance/c2pa.md`](../compliance/c2pa.md).

## How the Pillars Reinforce Each Other

The 14 pillars are not a bag of features. Each one *enables* the others:

- Pillar 1 (determinism) makes Pillar 10 (sovereignty) cryptographically meaningful.
- Pillar 2 (universal seed) makes Pillar 5 (engine pattern) work across domains.
- Pillar 3 (17-type gene system) gives Pillar 6 (evolution) primitives to operate on and Pillar 7 (functors) types to map between.
- Pillar 4 (GSPL) and Pillar 9 (Agent) are peers — both produce seeds, both feed the same downstream stack.
- Pillar 8 (refinement loop) gives Pillar 6 (evolution) a meaningful fitness signal.
- Pillar 11 (`.gseed`) wraps Pillar 14 (C2PA) into the canonical at-rest format.
- Pillar 12 (federation) needs Pillar 1 (determinism) for trust between peers.
- Pillar 13 (GPU) makes Pillar 6 (evolution) fast enough to feel real-time.

If you remove any one pillar, the structure leans. If you remove three, it collapses. The 14 are minimal, not bloated.

## What Is Not a Pillar

Things that are *not* pillars (despite being important):

- The Studio UI. It's a thin client. A CLI replacement would still be Paradigm.
- The choice of Postgres / Redis / Stripe. Those are infrastructure choices, replaceable.
- The 26 specific domains. The pattern matters more than the count.
- Any single LLM provider. The intelligence layer is provider-agnostic.

The pillars are the things that, if you removed them, the result would no longer be Paradigm. Everything else is implementation detail.
