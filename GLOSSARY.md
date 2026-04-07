# Glossary

Every term used throughout this repository, defined precisely. Pin this vocabulary before reading anything else.

## Core Concepts

**Paradigm** — The platform name. The overall Genetic Operating Environment for digital creation, built by Kahlil Stephens / 11vatedTech LLC.

**GOE (Genetic Operating Environment)** — The computational paradigm Paradigm implements: creative artifacts encoded as living genetic blueprints that grow through developmental stages. Distinguished from a "Genetic Operating System" because it sits above any OS and operates on creative artifacts rather than processes.

**GSPL (Genetic Seed Programming Language)** — The domain-specific language used to write, breed, mutate, compose, and evolve seeds. 26 reserved keywords, recursive-descent parsed, Hindley–Milner–style type system with dependent-type extensions, compiles to both an AST interpreter and WGSL for GPU execution.

**GST (Genetic Seed Type)** — The root type tag on every `UniversalSeed`. Identifies a seed as conformant to the Paradigm genetic specification.

**Seed** — Short for UniversalSeed. A typed, signed, hashed, lineage-carrying data structure that grows into an artifact when passed through a domain engine.

**Artifact** — The concrete output produced when an engine runs a seed through its developmental pipeline. Can be a 2D image, a 3D mesh, an audio file, a playable game, a narrative, a simulation, etc.

**Developmental Pipeline** — The ordered sequence of stages inside a domain engine that transforms a seed into an artifact. Each stage is a pure, deterministic, side-effect-free function of the seed's genes plus prior stages' outputs.

**Domain** — One of 26 creative categories Paradigm targets (Sprite, Character, Music, FullGame, Animation, Procedural, Geometry3D, Narrative, UI, Physics, Visual2D, Audio, Ecosystem, Game, ALife, Shader, Particle, Typography, Architecture, Vehicle, Furniture, Fashion, Robotics, Circuit, Food, Choreography).

**Engine** — The implementation of a single domain's developmental pipeline. All 26 engines conform to the `DomainEngine` interface.

**Gene** — An individual typed value inside a seed's `genes` object, carrying a name, a type (one of 17), and domain-specific operators (mutate, crossover, distance, validate).

**Gene Type** — One of 17 fundamental kinds of creative information. The full list is in [`spec/02-gene-system.md`](spec/02-gene-system.md).

**Lineage** — The complete ancestry of a seed, stored inside the seed itself, linking back to parent seed hashes through every breeding operation.

**Breeding** — The operation `breed(parentA, parentB) → child`. Combines two parent seeds using gene-type-specific crossover operators, produces a child seed whose lineage references both parents.

**Mutation** — The operation `mutate(seed, rate) → variant`. Applies gene-type-specific mutation operators under control of the deterministic RNG.

**Evolution** — A population-level process that runs many rounds of selection, crossover, and mutation under a fitness or quality-diversity criterion. Paradigm ships 7+ algorithms: GA, MAP-Elites, CMA-ES, Novelty Search, AURORA, DQD, POET.

**Composition** — The operation `compose(seedA, functor) → seedB` or `compose(seedA, seedB, …) → multiSeed`. Routes seeds across domains through pre-registered category-theoretic functor bridges.

**Functor Bridge** — A category-theoretic mapping between two domains that defines gene-to-gene correspondences, artifact-to-artifact correspondences, and a coherence scoring function. 9 are pre-registered.

**Sovereignty** — The cryptographic property that every seed is signed by its author with an ECDSA P-256 key, and that signature lives inside the seed itself, producing an immutable ownership chain without a blockchain or central registry.

**Fitness** — A scalar or vector measure of how "good" a seed is. In Paradigm this is computed by the `refinement-loop` as a 6-dimensional `QualityVector`: geometry, texture, animation, coherence, style, novelty.

**QualityVector** — The six-dimensional quality metric used across all engines: `{ geometry, texture, animation, coherence, style, novelty }`. Each component is in `[0, 1]`.

**Refinement Loop** — The closed-loop quality engine: evaluate → critique → mutate (choosing from 8 strategies) → re-evaluate → commit or revert. Implements identity preservation via a deviation threshold.

## Identity & Addressing

**Content Hash** — The SHA-256 hash of the canonicalized seed, used as the seed's primary identity. Stored in the `$hash` field.

**Canonicalization** — The deterministic serialization procedure that produces a byte-identical representation of a seed regardless of how it was constructed. Defined in [`spec/05-sovereignty.md`](spec/05-sovereignty.md).

**JWK** — JSON Web Key. The portable format used to serialize ECDSA P-256 public and private keys for storage and exchange.

**ECDSA P-256** — Elliptic Curve Digital Signature Algorithm over the NIST P-256 curve. The only signing primitive Paradigm uses. Available natively via the Web Crypto API in all modern browsers.

## Runtime

**xoshiro256\*\*** — The deterministic pseudo-random number generator used throughout Paradigm. Fast, high-quality, small state, seedable from the content hash. Pronounced "xoshi-ro two-fifty-six star-star."

**SplitMix64** — The seeding function used to initialize xoshiro256\*\*'s four state words from a single 64-bit seed.

**Box–Muller** — The transform used to draw normally distributed values from uniform ones, for Gaussian mutation operators.

**FNV-1a** — The hash function used to derive per-gene sub-seeds from a parent seed without consuming the parent's RNG state.

**Fisher Information Matrix (FIM)** — The matrix of expected second derivatives of the log-likelihood of a seed under its fitness distribution. Used to define the `SeedManifold` — the curved space of all seeds with the FIM as its metric — and to compute natural gradient descent for evolution.

**SeedManifold** — The abstract geometric object representing the space of all seeds, equipped with the Fisher Information Matrix as its Riemannian metric. Enables natural gradient descent and informed mutation step sizes.

**Tick Cycle** — The 8-phase deterministic execution loop of the kernel: `intake → validate → plan → mutate → execute → reduce → emit → persist`. Every evolution step, every breeding operation, every seed growth runs through a tick cycle.

**Algebraic Effects** — The 8 effect types the kernel uses to separate pure computation from side effects: `Read`, `Write`, `Random`, `Time`, `Network`, `GPU`, `Log`, `Sign`. Inspired by Koka / Eff / Unison.

## Language

**Keyword** — One of the 26 reserved words in GSPL. Full list in [`language/keywords.md`](language/keywords.md).

**AST (Abstract Syntax Tree)** — The parsed representation of a GSPL program, consisting of 25+ node types.

**Type Checker** — The pass that verifies every expression in a GSPL program has a consistent type under Hindley–Milner inference with dependent-type refinements.

**WGSL (WebGPU Shading Language)** — The GPU code format that GSPL compiles to for compute-heavy paths (fitness evaluation, field sampling, mesh generation, shader materials).

## Formats

**.gseed** — The canonical binary seed file format. MessagePack-serialized for efficiency. Carries genes, lineage, sovereignty, hash, metadata.

**.gspl** — The canonical GSPL source-code file format. UTF-8 text, `.gspl` extension.

**.gcapsule** — A bundle containing a seed plus all its ancestors, transitively. Used for offline exchange and auditing.

**.gworld** — A bundle of multiple seeds plus their composition graph, representing a full scene or game.

**.gresonance** — An audio-domain bundle containing a seed plus pre-baked WAV renders at multiple sample rates.

**glTF / USD / FBX** — Standard interoperability formats Paradigm exports to, for interop with Unity, Unreal, Godot, Blender, Three.js, etc.

**C2PA Manifest** — Content Credentials metadata binding an artifact to its sovereign author and provenance chain. Required for EU AI Act Article 50 compliance (August 2026) and California SB 942 (January 2026).

## Infrastructure

**MAP-Elites** — A quality-diversity evolution algorithm that maintains an archive of elite seeds indexed by behavioral descriptors, producing a diverse population of high-quality solutions rather than a single optimum.

**CMA-ES (Covariance Matrix Adaptation Evolution Strategy)** — A continuous numeric optimizer that adapts the covariance matrix of its sampling distribution to the fitness landscape.

**Novelty Search** — An evolution algorithm that rewards behavioral novelty rather than fitness directly, avoiding local optima and stepping-stone exploration.

**AURORA** — An unsupervised quality-diversity algorithm that learns its own behavioral descriptors from the data.

**DQD (Differentiable Quality-Diversity)** — A gradient-informed extension of MAP-Elites that uses fitness gradients to accelerate exploration.

**POET (Paired Open-Ended Trailblazer)** — A co-evolutionary algorithm that evolves environments and agents together, producing open-ended complexity growth.

**Federation** — The WebSocket-based distributed evolution system in which multiple Paradigm instances exchange seeds, run island-model evolution, and propagate breeding royalties across jurisdictional boundaries.

**Stripe Connect** — The payment infrastructure Paradigm uses for marketplace transactions. Platform takes 10%; Stripe Connect destination charges route breeding royalties backward through lineage chains with diminishing per-generation rates.

## Intelligence Layer

**GSPL Agent** — The Concept-to-Seed intelligence layer. A five-stage pipeline (Intent Classification → NL Gene Mapping → Active Web Cross-Referencing → Seed Assembly & Validation → Artifact Generation) coordinated by 8 sub-agents and backed by a 4-layer memory system.

**ReAct** — Reasoning + Acting. The LLM agent loop pattern in which the model interleaves chain-of-thought reasoning with tool calls.

**Template Bridge** — The curated library of 26+ starting-point seeds per domain (warrior, mage, trickster archetypes; sonata, ballad, rondo musical forms; platformer, metroidvania, roguelike game skeletons) that the agent uses to warm-start generation rather than cold-generate.

**Intent Taxonomy** — The 13-entry classification of user intents: `create`, `breed`, `evolve`, `compose`, `mutate`, `refine`, `critique`, `explain`, `compare`, `export`, `search`, `tag`, `declare-sovereignty`.

**Adjective Normalization Table** — The per-domain mapping from natural-language adjectives ("menacing," "ethereal," "crunchy") to concrete gene mutations. A single adjective typically touches multiple gene types (e.g., "menacing" → darker color + sharper topology + twitchier temporal + aggression-biased regulatory).

## Regulatory

**C2PA (Coalition for Content Provenance and Authenticity)** — The open industry standard for cryptographically signed content credentials. 6,000+ member organizations as of 2026. Becoming legally required in select jurisdictions.

**EU AI Act Article 50** — Requires machine-readable AI disclosure on AI-generated content. Enforcement begins August 2026.

**California SB 942** — Requires AI transparency metadata. Effective January 2026.

**WCAG 2.1 AA** — The Web Content Accessibility Guidelines level Paradigm's Creation Studio targets for compliance.
