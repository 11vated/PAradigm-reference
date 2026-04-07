# Algorithms

This directory holds canonical pseudocode for the load-bearing algorithms in Paradigm. Each file is implementation-language-agnostic; the goal is for any AI or engineer to read the pseudocode and produce a conformant implementation in TypeScript, Rust, Go, or Python.

## Index

| File | Algorithm | Used by |
|---|---|---|
| [`xoshiro256.md`](xoshiro256.md) | xoshiro256** + splitmix64 RNG | Kernel deterministic RNG |
| [`fisher-information.md`](fisher-information.md) | Fisher Information Matrix approximation | SeedManifold (Layer 1) |
| [`map-elites.md`](map-elites.md) | MAP-Elites quality-diversity | Default evolution algorithm |
| [`cma-es.md`](cma-es.md) | Covariance Matrix Adaptation ES | Continuous numeric optimization |
| [`novelty-search.md`](novelty-search.md) | Novelty Search | Deceptive fitness landscapes |
| [`aurora.md`](aurora.md) | AURORA (auto-encoder repertoire) | Quality-diversity without hand-designed descriptors |
| [`dqd.md`](dqd.md) | Differentiable Quality-Diversity | Gradient-informed QD |
| [`poet.md`](poet.md) | Paired Open-Ended Trailblazer | ALife and ecosystem co-evolution |
| [`refinement-loop.md`](refinement-loop.md) | UCB1 mutation-strategy bandit + QualityVector | Inner loop of every evolution |
| [`functor-composition.md`](functor-composition.md) | Cross-domain composition pathfinding | Layer 5 functor registry |
| [`marching-cubes.md`](marching-cubes.md) | Marching cubes | Geometry3D mesh extraction |
| [`canonicalization.md`](canonicalization.md) | JCS-style JSON canonicalization | Sovereignty + hashing |

## Why Pseudocode and Not Code

The reference repository's purpose is to be **language-agnostic** — Gemini, Claude, GPT-4, or a human engineer should all be able to consume it and produce a working implementation. Real code in one language locks readers in. Pseudocode in a consistent style reads like math and ports cleanly.

The pseudocode style:

- Static-typed annotations where they clarify intent (`fn foo(x: int) -> int:`).
- Imperative loops where they're clearer than functional combinators.
- No language-specific syntax sugar.
- Comments that explain the *why*, not the *what*.
