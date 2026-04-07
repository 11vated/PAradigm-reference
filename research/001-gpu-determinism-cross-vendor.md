# 001 — GPU determinism cross-vendor

## Question
Can a single WGSL compute pipeline produce bitwise-identical outputs across NVIDIA, AMD, Intel, and Apple GPUs through wgpu, and if not, what is the smallest envelope that can?

## Why it matters (blast radius)
The GSPL kernel pipeline is the determinism root of the entire system. If two users running the same seed on different hardware get even one differing bit in any stage output, every downstream invariant collapses: content hashes diverge, C2PA manifests fail to verify, the exemplar archive becomes per-machine, and the "same seed → same artifact" promise is dead. This brief gates `kernels/`, `runtime/gpu-pipeline.md`, and the entire `proof/` subsystem.

## What we know from the spec
- `kernels/` mandates a portable WGSL subset and forbids non-deterministic intrinsics.
- `runtime/gpu-pipeline.md` requires the same WGSL source to compile and execute identically across all four major vendors via wgpu/Naga.
- `proof/content-hash.md` hashes raw kernel outputs before any post-processing, so any cross-vendor bit difference is fatal.

## Findings

1. **WebGPU does not guarantee bitwise-identical floating-point results across implementations.** The W3C WGSL spec [1] explicitly allows implementations latitude in floating-point evaluation order, fused multiply-add formation, and transcendental precision. The gpuweb working group issue #1048 [2] documents that the same compute shader returns different results on a mobile GPU, an integrated GPU, and a discrete GPU on the same machine. The group has discussed but not adopted a "guaranteed precision" mode.

2. **WGSL is stricter than GLSL but not deterministic by construction.** WGSL forbids implicit conversions, requires explicit precision in many places, and disallows several non-deterministic GLSL idioms [1]. This narrows the gap considerably — many shaders that diverge in GLSL converge in WGSL — but it does not close it. FMA contraction, denormal flushing, and `fast-math`-style reassociation remain implementation-defined.

3. **Integer compute is deterministic across vendors when the kernel uses only integer ops, bitwise ops, and well-defined wraparound.** Nothing in the WGSL spec or any vendor's WGSL backend permits integer reordering. This is the only path to bitwise reproducibility today.

4. **wgpu/Naga is the only mature cross-vendor translation layer.** Naga compiles WGSL to SPIR-V (Vulkan), MSL (Metal), HLSL (DX12), and GLSL. The Vulkan backend is the most feature-complete; Metal and DX12 use translation layers with their own constraints [3]. Mesh shaders are first-class on Vulkan only.

5. **No existing project has achieved bitwise cross-vendor determinism for nontrivial floating-point compute kernels via WebGPU/wgpu.** Several projects (notably some scientific viz and gamedev physics libraries) have tried; the consistent finding is that determinism requires either (a) staying integer-only or (b) running on a single vendor.

## Risks identified

- **Float ops in any kernel stage will produce per-vendor drift.** Even a single `cos`, `sqrt`, or `*` followed by `+` can diverge.
- **Driver updates can change results on the same GPU.** Vendor driver releases ship new shader compilers that may legalize FMA differently or change transcendental precision.
- **Naga's translation is not bit-stable across versions.** Upgrading wgpu can change generated SPIR-V/MSL/HLSL even for unchanged WGSL source.
- **Apple GPUs (Metal) historically have the largest divergence** because MSL's float semantics are the loosest of the four backends.

## Recommendation

**Adopt an "integer-only kernel core" architecture.** Concretely:

1. **All bit-exact stages of the kernel pipeline run in fixed-point integer arithmetic.** Define a `Q16.16` (or `Q24.8` where range demands) fixed-point type for everything that hashes into the content hash. Implement add, sub, mul, div, and any required transcendentals as integer table lookups or polynomial approximations operating on the fixed-point representation.
2. **Float ops are confined to a "post-processing" stage that runs after the content hash is computed.** Tone mapping, color grading, and final-display conversion can be float; their outputs are not proof-relevant.
3. **Pin wgpu to a single minor version per release.** Bumping wgpu requires re-running the determinism conformance suite and bumping the kernel format version.
4. **Conformance suite: every supported vendor × OS pair runs the same seeds and the kernel output hash must match.** Vendors covered at launch: NVIDIA (Linux/Win), AMD (Linux/Win), Intel iGPU (Linux/Win), Apple Silicon (macOS). Until the suite passes on a vendor, that vendor is not in the support matrix.
5. **No FMA, no `fast-math`, no transcendental intrinsics in proof-bearing code.** Use software implementations only.

## Confidence
**3/5.** The "integer-only" path is well understood in principle and has been used in deterministic lockstep multiplayer game engines for decades. The risk is that we have not yet measured how much GPU compute throughput we lose moving the proof-bearing kernels from float to fixed-point on representative scenes — that requires Phase 1 hardware. We are confident the approach works; we are not yet confident the performance is acceptable.

## Spec impact

- `kernels/README.md` — add a "Determinism root" section mandating fixed-point for proof-bearing stages, naming `Q16.16` as the default representation, and forbidding floats in any stage whose output feeds the content hash.
- `runtime/gpu-pipeline.md` — add a "Conformance matrix" section listing the vendor × OS pairs the implementation must pass before a release ships.
- `proof/content-hash.md` — clarify that the hash input is the fixed-point integer buffer, not the post-processed float buffer.
- `infrastructure/library-canon.md` — pin wgpu to a specific minor version and require the version bump process to re-run the conformance suite.
- New ADR: `adr/00NN-fixed-point-kernel-core.md` capturing the decision to use fixed-point for proof-bearing kernels.

## Open follow-ups

- Empirical: measure fixed-point vs float throughput on a representative scene on each vendor. Phase 1 task.
- Empirical: build the conformance suite and run it on all four vendors. Phase 1 task.
- Investigate whether `subgroup` operations (added to WGSL recently) preserve determinism — preliminary reading suggests yes for reductions on integer types, but unverified.
- Decide whether `Q16.16` is enough range for the color and geometry stages, or whether some stages need wider fixed-point.

## Sources

1. WebGPU Shading Language (WGSL) W3C Working Draft. https://www.w3.org/TR/WGSL/ — sections on floating-point evaluation, conversion, and built-in functions.
2. gpuweb issue #1048: "Floating point determinism." https://github.com/gpuweb/gpuweb/issues/1048
3. wgpu (gfx-rs/wgpu) documentation and source. https://github.com/gfx-rs/wgpu — backend feature matrix and Naga translation notes.
