# 054 — Rendering pipeline and GPU strategy

## Question
How does GSPL render seeds to viewable outputs across 19 engines on consumer hardware (and increasingly mobile and web), what GPU/CPU strategy keeps it deterministic, and how does the rendering pipeline interact with the differentiable rendering needed for DQD (Brief 037)?

## Why it matters
Rendering is the visible product. Slow renders kill the iteration loop; nondeterministic renders break content addressing; missing GPU support excludes huge user populations. Differentiable rendering for DQD adds another constraint: the same renderer must support both forward (fast) and backward (gradient) modes. Coordinating all of this across 19 engines is the deepest infrastructure problem in GSPL.

## What we know from the spec
- Brief 001: deterministic GPU kernel with WGSL.
- Brief 002: WGSL is the shader language.
- Brief 037: DQD needs differentiable rendering.
- Briefs 021-026: per-engine rendering needs.

## Findings — three rendering tiers

### Tier 1: Deterministic kernel (Brief 001)
The lowest-level renderer. Pure compute, fixed-point arithmetic, deterministic across vendors.
- **What it does:** runs the simulation/scoring/evaluation primitives that must produce identical output regardless of GPU vendor or driver version.
- **When it's used:** content-addressing-critical paths (signing, replay, attestation, evolution rollouts).
- **Cost:** slower than native floating point (~3-5x), but bit-identical.
- **Where it lives:** Tier 1 is mandatory for all evaluation that feeds into lineage.

### Tier 2: Native fast renderer
Standard floating-point GPU rendering for the *display* path.
- **What it does:** renders the same seed with hardware-accelerated floating-point shaders for the studio preview.
- **When it's used:** every interactive preview, every variant grid render, every Forge view.
- **Cost:** fast (60fps for sprites and music waveforms; 30fps for 3D).
- **Determinism:** not bit-identical, but visually equivalent. The studio shows a small "preview" badge to remind users that the displayed pixels may differ from the canonical render.

### Tier 3: Differentiable renderer (DQD)
For engines where DQD applies (Brief 037).
- **What it does:** forward render + backward gradient computation.
- **When it's used:** during DQD evolution, never in interactive preview.
- **Cost:** ~5x forward render cost.
- **Implementations:** nvdiffrast for 3D, custom for sprites (raster gradient), differentiable score-to-feature for music.
- **Determinism:** float64 deterministic on CPU; float32 with vendor-specific reproducibility on GPU.

## Per-engine rendering strategies

### Sprite, Visual2D
- **Tier 1:** CPU fixed-point rasterizer (small, slow, deterministic) for evaluation.
- **Tier 2:** WGPU shader for preview.
- **Tier 3:** Differentiable rasterizer (custom) for DQD.

### Music, Audio
- **Tier 1:** Reference fixed-point synth on CPU for canonical render (Brief 022).
- **Tier 2:** Native float synth for preview (LADSPA/AudioWorklet/AVAudioEngine).
- **Tier 3:** Differentiable score-to-spectrogram for DQD.

### Geometry3D
- **Tier 1:** Fixed-point CPU mesh evaluator for content addressing of mesh op graphs.
- **Tier 2:** WGPU PBR renderer for preview (wgpu-rs).
- **Tier 3:** nvdiffrast for DQD.

### Game, FullGame, Narrative
- **Tier 1:** Fixed-point game state simulator on CPU for rollouts (Brief 001 GPU kernel for batched).
- **Tier 2:** Native game engine integration (Godot/Unity headless) for preview.
- **Tier 3:** Not applicable (game critics are non-differentiable rollouts).

### Physics, Ecosystem, ALife
- **Tier 1:** Fixed-point Q16.16 deterministic solver (Brief 025).
- **Tier 2:** Native float solver for visualization.
- **Tier 3:** Differentiable physics for DQD where applicable (Phase 2).

### UI
- **Tier 1:** CPU layout engine (Brief 026).
- **Tier 2:** Same engine, just rendered to canvas.
- **Tier 3:** Not applicable.

### Procedural
- **Tier 1:** WFC/Wang/Perlin/Voronoi on CPU.
- **Tier 2:** Same on GPU with shader-based generation.
- **Tier 3:** Not applicable for discrete-state generators; differentiable for continuous (Perlin).

## Backend abstraction

GSPL uses **wgpu-rs** as the GPU abstraction:
- Vulkan on Linux/Windows.
- DirectX 12 on Windows.
- Metal on macOS/iOS.
- WebGPU in browser (v1.5).

This is one of the few choices that hits all four major GPU stacks with one shader language (WGSL).

The kernel from Brief 001 is wgpu-based. Tier 2 native renderers use the same wgpu instance.

## Performance budgets

- **Sprite preview render:** ≤ 16ms (60fps).
- **Music preview render:** ≤ 32ms per second of audio (real-time + headroom).
- **Geometry3D preview:** ≤ 33ms (30fps).
- **Game preview frame:** ≤ 16ms.
- **Physics frame (deterministic):** ≤ 16ms for typical world; ≤ 100ms for large worlds.
- **DQD generation step:** ≤ 250ms per candidate.

These budgets are measured on a target machine: M1 MacBook Pro / RTX 3060 / equivalent integrated.

## Cross-platform parity

- **macOS, Windows, Linux** are fully supported at v1.
- **iOS, Android** are v2 (separate native shells).
- **Web (WebGPU)** is v1.5.
- **Headless servers** (no GPU) fall back to Tier 1 CPU rendering for everything.

## Risks identified

- **wgpu maturity:** wgpu-rs is improving fast but still has rough edges. Mitigation: pin known-good versions; CI on all backends.
- **WGSL feature gaps:** some shaders need features WGSL doesn't expose. Mitigation: feature flags per engine; fall back to a slower path.
- **Differentiable renderer fragility:** see Brief 037. Mitigation: opt-in; fall back to plain MAP-Elites.
- **Mobile GPU scarcity:** not all mobile devices have compute shaders. Mitigation: v2 mobile uses CPU fallback for kernel.
- **WebGPU browser support:** still rolling out. Mitigation: feature-detect; fall back to WebGL or CPU.
- **Headless server CI:** GPU CI is hard. Mitigation: software rasterizer (lavapipe) for headless tests.
- **Driver bugs:** every wgpu user hits at least one. Mitigation: workaround library shipped with the kernel; bug reports upstream.

## Recommendation

1. **Adopt three-tier rendering** in `architecture/rendering.md`.
2. **Tier 1 deterministic kernel is mandatory** for all evaluation paths.
3. **Tier 2 native preview** is the default user-facing renderer.
4. **Tier 3 differentiable** is opt-in for DQD-applicable engines.
5. **wgpu-rs is the v1 GPU substrate.**
6. **WGSL is the v1 shader language** (Brief 002).
7. **Performance budgets are release-blocking.**
8. **CPU fallback for headless servers** ensures non-GPU operation.
9. **Cross-platform CI** on macOS/Windows/Linux at v1; mobile + web later.
10. **Driver workaround library** shipped with the kernel.

## Confidence
**4/5.** wgpu and the deterministic kernel are well-architected. The 4/5 reflects the unmeasured cost of cross-platform parity testing and differentiable renderer integration.

## Spec impact

- `architecture/rendering.md` — full three-tier rendering spec.
- `architecture/gpu-backend.md` — wgpu-rs integration.
- `engines/*/rendering.md` — per-engine renderer strategies.
- `tests/rendering-determinism.md` — Tier 1 conformance.
- `tests/rendering-performance.md` — budget enforcement.
- New ADR: `adr/00NN-three-tier-rendering.md`.

## Open follow-ups

- Build a Tier 1 reference rasterizer for SpriteEngine.
- Decide on the differentiable rasterizer (custom vs nvdiffrast for 3D).
- Empirical performance measurement on the target machine.
- WebGPU compatibility audit.
- Mobile rendering strategy for v2.

## Sources

- wgpu-rs documentation and architecture writeups.
- WGSL specification.
- nvdiffrast paper (Laine et al.).
- Internal: Briefs 001, 002, 022, 025, 026, 037.
