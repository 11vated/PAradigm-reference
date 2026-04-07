# 002 — WGSL portable subset

## Question
Which WGSL features can the Paradigm kernel rely on across the wgpu Vulkan, Metal, and DX12 backends today, and which features are forbidden because they are unsupported, lowered inconsistently, or non-deterministic?

## Why it matters (blast radius)
A WGSL feature that compiles cleanly on one backend and fails (or silently degrades) on another forces per-vendor kernel forks, which destroys the "one source, all vendors" property that the spec depends on. Brief 001 establishes the *determinism* envelope; this brief establishes the *portability* envelope. The two together define the actual writable subset.

## What we know from the spec
- `kernels/README.md` requires a single WGSL source file per kernel stage, no per-vendor forks.
- `runtime/gpu-pipeline.md` names wgpu/Naga as the only supported translation layer.
- The spec assumes mesh shaders, compute shaders, and storage buffers are available everywhere.

## Findings

1. **Compute shaders, storage buffers, and uniform buffers are universally supported.** All four wgpu backends (Vulkan, Metal, DX12, GLES via ANGLE) implement these as core features [1]. This is the safe core of the portable subset.

2. **Mesh shaders are Vulkan-only as first-class.** wgpu exposes mesh shaders through a feature flag; on Vulkan they map to native `VK_EXT_mesh_shader`. On Metal and DX12, support is either passthrough or unavailable depending on the wgpu version [1, 2]. **Implication: any kernel stage that uses mesh shaders must have a compute-shader fallback or be flagged as Vulkan-only.**

3. **Subgroup operations have partial cross-backend support.** wgpu has been adding subgroup ops (ballot, broadcast, reduce, shuffle) progressively. As of recent wgpu releases, subgroup arithmetic reductions on integer types are supported on Vulkan (via `VK_KHR_shader_subgroup_*`), Metal (via SIMD-group ops), and DX12 (via wave intrinsics). Float subgroup reductions are non-deterministic by definition (reduction order is implementation-defined) and are forbidden by Brief 001 anyway.

4. **Cooperative matrix / cooperative load-store has narrow support.** Naga's input handling for cooperative ops accepts WGSL on input but only emits to SPIR-V, MSL, and WGSL on output [3]. HLSL/DX12 backend support is incomplete. **Implication: cooperative matrix is off the table for the portable subset.**

5. **Push constants exist on Vulkan and Metal but are emulated as a tiny uniform buffer on DX12.** wgpu exposes a uniform `PushConstants` API. Functionality is portable; performance characteristics differ.

6. **Texture formats: only the WebGPU "core" format set is universally supported.** Anything in the "Tier 2" or vendor-specific extension list (BC7, ASTC HDR, ETC2 on desktop) is portability-fragile.

7. **Atomic operations on storage buffers are universally supported for `i32`/`u32`.** Atomic float ops are not part of WebGPU core and are forbidden in the portable subset.

8. **`workgroupBarrier` and `storageBarrier` are universally supported and behave identically.** This is the only intra-workgroup synchronization primitive the kernel may use.

9. **Workgroup sizes are constrained to (256, 256, 64) max in any single dimension and 256 max threads per workgroup on the conservative envelope.** Higher limits exist on most desktop hardware but the conservative envelope is what the portable subset must target.

## Risks identified

- **Naga version drift can change emitted shader code** even for unchanged WGSL. A wgpu bump must be treated as a kernel-format change and re-run the conformance suite from Brief 001.
- **Mesh shaders are tempting for the geometry stage** because of their performance characteristics, but adopting them creates a Vulkan-only fast path and a compute-shader slow path — two code paths to maintain. The brief recommends compute-shader-only at v1.
- **DX12 push-constant emulation** can blow out the uniform descriptor budget if push constants are large; keep them under 128 bytes.
- **Vendor-specific texture formats** sneaking into the spec are an easy way to break Apple Silicon support; only formats in the WebGPU core list may appear in the kernel.

## Recommendation

**The Paradigm portable WGSL subset is:**

| Feature | Status | Notes |
|---|---|---|
| Compute shaders | REQUIRED | The only shader stage used by the kernel |
| Storage buffers (read/write) | REQUIRED | Layout: `std430`-equivalent, explicit `@align` and `@size` |
| Uniform buffers | REQUIRED | Cap at 16 KB |
| Atomic ops on `i32`/`u32` | ALLOWED | Required for accumulator stages |
| `workgroupBarrier`, `storageBarrier` | ALLOWED | Only intra-workgroup sync |
| Subgroup integer reductions | ALLOWED behind feature flag | Must compile to a portable fallback if unavailable |
| Push constants | ALLOWED | Cap at 128 bytes |
| Textures (core format set only) | ALLOWED | RGBA8, RGBA16F, R32U, R32F, etc. |
| Mesh shaders | FORBIDDEN at v1 | Re-evaluate at v2 if cross-vendor support matures |
| Cooperative matrix | FORBIDDEN | DX12 backend incomplete |
| Atomic floats | FORBIDDEN | Not in WebGPU core |
| Subgroup float reductions | FORBIDDEN | Non-deterministic |
| Texture formats outside core | FORBIDDEN | BC7, ASTC HDR, ETC2 on desktop |
| FMA, fast-math, transcendental intrinsics in proof-bearing code | FORBIDDEN | See Brief 001 |

**Operational rules:**

1. **One WGSL file per kernel stage, no per-vendor branches.**
2. **Workgroup size: 64 or 256 (powers of two only) for all proof-bearing kernels.** Non-power-of-two sizes hit slow paths on at least one vendor.
3. **All buffer layouts are explicitly annotated with `@align` and `@size`.** Never rely on implicit layout — Naga's emission rules differ subtly across backends.
4. **wgpu version is pinned in `Cargo.toml`** and bumping requires re-running the Brief 001 conformance suite plus a kernel format version bump.
5. **A WGSL linter (custom, scriptable) runs in CI** and rejects any feature outside the table above.

## Confidence
**4/5.** The portable subset above is the intersection of well-documented wgpu/Naga support across the four backends. The one open question is the long-term stability of subgroup ops — wgpu is actively adding them and the support matrix is moving — which is why subgroup reductions are gated behind a feature flag with a portable fallback.

## Spec impact

- `kernels/README.md` — embed the portable subset table verbatim and forbid features outside it.
- `kernels/wgsl-style.md` — new file with the operational rules (workgroup sizes, layout annotation, linter rules).
- `runtime/gpu-pipeline.md` — add the wgpu version pin and the bump-process requirement.
- `infrastructure/ci.md` — add the WGSL linter as a required CI gate.
- New ADR: `adr/00NN-wgsl-portable-subset.md` capturing the v1 subset and the explicit "no mesh shaders, no cooperative matrix at v1" decision.

## Open follow-ups

- Empirical measurement: which workgroup sizes actually perform best on each vendor for our representative kernels? Phase 1 task.
- Decision: do we ship a Vulkan-only "fast path" using mesh shaders for the geometry stage at v2? Defer until v1 ships.
- Investigate the wgpu `Features::SHADER_F16` flag — half-precision could halve memory bandwidth on some stages but is not universally supported.
- Build the WGSL linter. It is small but it does not exist yet.

## Sources

1. wgpu (gfx-rs/wgpu) repository and feature matrix. https://github.com/gfx-rs/wgpu
2. wgpu issue #1416: mesh shader cross-backend status. https://github.com/gfx-rs/wgpu/issues/1416
3. Naga shader translation matrix (in-repo at gfx-rs/wgpu/naga). https://github.com/gfx-rs/wgpu/tree/trunk/naga
4. WebGPU Shading Language (WGSL) W3C Working Draft. https://www.w3.org/TR/WGSL/
