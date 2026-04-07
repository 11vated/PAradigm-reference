# Phase 3 — Domain Engines and Evolution

**Duration:** Months 5-7 (12 weeks)
**Goal:** Six production domain engines plus the evolution and composition layer. At the end, Paradigm is a complete creative-evolution toolkit usable by anyone willing to write GSPL by hand.

## Why this is third

The engines are where GSPL programs become *output*. Without engines, GSPL is an abstract DSL with nothing to render. Without evolution, every seed must be hand-written. Both are required before the agent (Phase 4) has anything useful to call.

## Deliverables

| Deliverable | Acceptance |
|---|---|
| Sprite engine | Renders 256×256-2048×2048 sprite atlases from a seed |
| Texture engine | Renders 256-4096px textures with OKLab color science |
| Sculpt engine | Produces a watertight mesh via Marching Cubes from an SDF seed |
| Music engine | Produces a 30s-3min Opus track from a seed |
| Particles engine | Renders a particle simulation as image or video |
| Animation engine | Produces a temporal sequence (sprite atlas + JSON) |
| MAP-Elites | Default evolution algorithm working on all 6 engines |
| Novelty Search | Working on all 6 engines |
| CMA-ES | Continuous gene refinement working |
| Functor registry | Cross-domain functors with Dijkstra path-finding |
| Mutation bandit | UCB1 over 8 mutation operators |
| GPU compute | Marching Cubes + Verlet on wgpu, with CPU fallback |
| `.gseed` exports | Every engine produces signed `.gseed` files |

## Week-by-week plan

### Weeks 1-2: Sprite engine (the reference)

The Sprite engine is built first because it is the simplest and the template every other engine follows.

- Stage runner: shared across engines
- Sprite stages: layout → color → shading → details → finalize
- Output: PNG atlas + JSON metadata
- Quality vector computation
- Round-trip via `.gseed`

### Week 3: Texture engine

- OKLab color science (port the WGSL from `infrastructure/gpu-kernels.md`)
- Procedural noise (Perlin, Simplex, Worley)
- Tiling support (mirror, wrap, Wang)
- Output: PNG / WebP

### Weeks 4-5: Sculpt engine

- SDF primitives + boolean operations
- Marching Cubes on CPU
- Marching Cubes on GPU via wgpu
- Mesh decimation (quadric error metrics)
- Watertight check
- Output: GLB

### Week 6: Music engine

- Synth chain: oscillators → filters → envelopes → mixer
- MIDI-style pattern grid
- Audio rendering at 48 kHz
- Loudness normalization (-14 LUFS)
- Output: Opus

### Week 7: Particles engine

- Particle pool data structure
- Verlet integration on CPU + GPU
- Force fields, emitters, killers
- Render to image or short video
- Output: PNG (single frame), MP4 (sequence)

### Week 8: Animation engine

- Temporal sequencing (keyframes + interpolation)
- IK solvers (FABRIK, CCD)
- Skeletal blending
- Sprite atlas generation
- Output: PNG atlas + JSON timeline

### Week 9: MAP-Elites

- Archive data structure (n-d grid)
- Behavior characterization (engine-specific)
- Elite selection + replacement
- Mutation operators (8 standard, see `algorithms/`)
- UCB1 bandit selecting operators
- Test: 100 generations on each engine

### Week 10: Novelty Search + CMA-ES

- k-NN-based novelty score
- NSLC (Novelty + Local Competition) variant
- CMA-ES for continuous gene refinement
- Test: same engines as MAP-Elites

### Week 11: Composition layer

- Functor registry
- Cross-domain functor implementations: Sprite↔Music, Sculpt↔Sprite, Music↔Particles
- Dijkstra path-finder for arbitrary cross-domain composition
- Functor laws as test cases
- Test: round-trip Sprite → Music → Sprite for at least 10 seeds

### Week 12: Hardening + golden tests + integration

- Per-engine golden test suite (20 seeds each)
- Cross-engine consistency tests (same seed across engines)
- Performance budgets enforced in CI: each engine renders the canonical seed in <5s
- GPU determinism tests passing
- Tag `engines-0.3.0`

## Engine implementation pattern

Every engine follows the staged-pipeline pattern from `engines/_template.md`:

```
fn run_engine(seed: Seed) -> EngineOutput:
    let mut ctx = EngineContext::new(seed)
    for stage in STAGES:
        ctx = stage.execute(ctx)
        ctx = ctx.checkpoint()       // for cache + replay
    return ctx.finalize()
```

The shared infrastructure handles: kernel context, RNG seeding, stage timing, error wrapping, hash computation, output writing. Each engine supplies only its `STAGES` list and the stage implementations.

This is why the second engine takes half as long as the first.

## Performance budgets

| Engine | Cold p95 | Warm p95 |
|---|---|---|
| Sprite (1024²) | 5s | 1s |
| Texture (1024²) | 3s | 0.5s |
| Sculpt (256³) | 8s | 2s |
| Music (60s) | 6s | 1.5s |
| Particles (10s, 100k particles) | 10s | 3s |
| Animation (32 frames @ 256²) | 7s | 1.5s |

These are the budgets we test against in CI on a reference machine (4 vCPU, 16 GB RAM, no GPU). With GPU, divide all numbers by ~5×.

## Risks and mitigations

**Risk:** GPU determinism fails on Marching Cubes.
**Mitigation:** CPU reference always available; ship with `--cpu-only` if needed for v1.

**Risk:** Marching Cubes mesh quality is poor at 256³ resolution.
**Mitigation:** Add quadric error metric decimation pass; document the resolution / cost tradeoff.

**Risk:** Music engine output sounds "AI-bad" (musically incoherent).
**Mitigation:** Lean on the MusicTheoryAgent in Phase 4 for musical structure; in Phase 3 the Music engine just needs to produce *valid* output, not *good* output.

**Risk:** MAP-Elites archive grows unbounded.
**Mitigation:** Bounded grid with deterministic eviction; archive trimming during evolution.

## What is *not* in Phase 3

- No GSPL Agent (Phase 4)
- No LLM calls
- No Studio
- No marketplace

## Done definition

1. All 6 engines pass their golden test suites.
2. MAP-Elites produces a stable archive on all 6 engines.
3. Cross-domain functor composition works for at least 3 functor pairs.
4. CI is green and performance budgets met on the reference machine.
5. A user (engineer) can hand-write GSPL, run an engine, and get a signed `.gseed` in <30s end-to-end.
6. Tag `engines-0.3.0`.
