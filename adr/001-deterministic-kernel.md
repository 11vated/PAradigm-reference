# ADR-001: Adopt a Deterministic Kernel as the Foundation

**Status:** Accepted
**Date:** 2024-08-12
**Layer:** Layer 0 (Kernel) — cross-cutting

## Context

Paradigm seeds are meant to be reproducible artifacts. The same seed handed to two different machines, or to the same machine a year later, must produce bit-identical output. This is the foundation on which sovereignty (you can prove a seed is yours), royalty propagation (you can prove a derivative came from a parent), and federation (two nodes can verify they computed the same thing) are built.

Most game/creative tools are *not* deterministic. They use the OS-level RNG, walltime, GPU non-determinism, hash-randomized iteration, or floating-point operations whose order depends on thread scheduling. Even nominally deterministic engines (Unity with fixed seed) have subtle non-determinism in physics, particle systems, and shader compilation.

We must choose between:

1. Building everything on existing engines and accepting that reproducibility is best-effort.
2. Building a thin deterministic kernel and forcing all higher layers to live inside its constraints.

## Decision

We will build a deterministic kernel (Layer 0) that exposes only deterministic primitives, and we will require every higher layer to use it. The kernel provides:

- A deterministic RNG (`xoshiro256**` + `splitmix64`, see ADR-003).
- A deterministic JSON canonicalizer (JCS, see ADR-002).
- A deterministic hash (SHA-256 over canonical bytes).
- A deterministic clock (logical time, not walltime).
- An algebraic-effect system that requires every effectful operation to be declared in a function's type, so non-determinism cannot leak in implicitly.

Any code that wants to use a non-deterministic primitive (walltime, OS RNG, network I/O) must do so via an explicit effect handler that the user can intercept and replay.

## Consequences

**Positive:**

- Two machines running the same GSPL program with the same seed produce bit-identical artifacts. Always. Forever.
- Sovereignty signatures and royalty propagation become possible (you can re-verify a derivation).
- Bug reproduction is trivial: ship the seed.
- Federation is possible: nodes verify each other's work.
- The codebase is testable to a degree most software cannot reach.

**Negative:**

- Every domain engine must be built carefully to avoid non-deterministic constructs. Even `HashMap` iteration order is forbidden — we use sorted iteration.
- GPU acceleration is harder. We pin shader algorithms, disable GPU optimizations that reorder operations, and verify outputs against a CPU reference for every release.
- Some external libraries cannot be used at all. We have written internal replacements for many things (image codecs, audio synthesis, mesh extraction).
- Onboarding new contributors takes longer; they have to internalize the discipline.

## Alternatives Considered

- **Best-effort determinism (Unity-style):** Use a fixed seed where possible and accept divergence elsewhere. Rejected because it makes sovereignty and federation impossible — the entire point of Paradigm.
- **Compile-to-WebAssembly sandbox:** Run all engines inside a WASM sandbox to bound non-determinism. Rejected because WASM does not actually guarantee determinism (NaN payloads, SIMD vendor variance), and the performance cost is prohibitive.
- **Snapshot-based reproducibility:** Store the *output* of every run, not the *seed*. Rejected because it bloats storage by 1000× and defeats lineage propagation (you cannot derive new things from a snapshot).

## References

- *Determinism in Distributed Systems* — Lamport 1978 (logical clocks)
- *Building Reproducible Artifacts* — NixOS / Reproducible Builds project
