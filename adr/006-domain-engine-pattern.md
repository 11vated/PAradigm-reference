# ADR-006: Use a Staged-Pipeline Domain Engine Pattern

**Status:** Accepted
**Date:** 2024-09-15
**Layer:** Layer 3 (Domain Engines)

## Context

Paradigm has 15+ implemented domain engines (Sprite, Character, Music, FullGame, Geometry3D, …) and 11 more planned. Every engine takes a seed and produces an artifact. We have to choose how engines are *structured* internally.

Without a pattern, every engine becomes a unique snowflake — different abstractions, different determinism strategies, different ways to inject mutation, different test coverage. New contributors face an N-engine learning curve.

## Decision

Every domain engine implements the `DomainEngine` interface and is structured as an ordered, named **staged pipeline**. Each stage:

- Takes the previous stage's output as input.
- Is a pure function (declares its effects, almost always just `Random` and `GPU`).
- Has a stable name (e.g., `morphogenesis`, `texture`, `compose`).
- Can be intercepted, profiled, replayed, or replaced individually.

Stages are listed in the engine's `stages` array. The runner:

```
fn run(engine: &DomainEngine, seed: Seed, rng: Rng) -> Artifact:
    let mut state = EngineState::initial(seed)
    for stage in &engine.stages:
        let substream = substream(&rng, format("stage:{}", stage.name))
        state = (stage.fn)(state, substream)
    return state.into_artifact()
```

Common stage names appear across multiple engines (`extract`, `morphogenesis`, `parameterize`, `texture`, `pose`, `compose`, `render`, `export`) and have a shared semantic meaning. Engine-specific stages are also allowed.

See [`engines/_template.md`](../engines/_template.md) for the canonical structure.

## Consequences

**Positive:**

- One mental model for all engines. Anyone who can read Sprite can read Music.
- Per-stage substream derivation: each stage gets a deterministic, independent RNG. Mutation strategies can target specific stages without affecting others.
- Per-stage profiling and caching are trivial. The studio can show "morphogenesis: 12ms, texture: 45ms" and cache stages whose inputs haven't changed.
- Replay debugging: re-run a single stage with mocked input to reproduce a bug.
- Determinism is locally checked: each stage's reproducibility is verified in isolation; the whole-engine reproducibility follows.
- New engines are written by copying `_template.md` and filling in stages — onboarding takes hours, not weeks.

**Negative:**

- Some algorithms don't naturally decompose into stages (e.g., iterative solvers). We force them into a single "solve" stage with internal iteration; not elegant but workable.
- Cross-stage data sharing is awkward — everything must flow through `EngineState`. Some engines define large state structs.
- Stage interfaces have to evolve carefully; changing a shared stage name would break every engine that uses it.

## Alternatives Considered

- **Free-form engines:** Each engine writes its own runner. Rejected because it eliminates most of the consistency benefits.
- **Dataflow graph:** Each engine declares a DAG of operations, runner topologically sorts. More flexible but harder to reason about and harder to test.
- **Actor-based:** Each stage is an actor that messages the next. Adds concurrency complexity for no real benefit since stages are sequential per seed.
- **Layered (input → middleware → output):** Closer to web framework conventions. Rejected because "middleware" doesn't map naturally to creative pipelines.

## References

- Pipeline pattern: Hohpe & Woolf, *Enterprise Integration Patterns*
- Halide: a similar staged-pipeline philosophy for image processing — Ragan-Kelley et al., *Halide: A Language and Compiler for Optimizing Parallelism* (PLDI 2013)
