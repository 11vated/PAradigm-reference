# 162 — Particle and VFX runtime

## Question

How does GSPL equip the runtime particle and visual-effects system — emitters, simulators, GPU/CPU paths, deterministic mode, typed VFX gseeds — as a substrate namespace where every effect is signed, replay-deterministic, and composable across genres without breaking the frame budget?

## Why it matters (blast radius)

Particles and VFX are the second-largest visual surface after animation and the largest single contributor to "game feel." Smoke, sparks, weather, magic, explosions, screen-space distortion, decals, trails, ribbons. Every game engine ships its own particle system (Unity Shuriken/VFX Graph, Unreal Niagara, Godot GPUParticles, Phaser ParticleEmitter) and they all diverge on determinism, ordering, and budget. Without a substrate VFX runtime, exports diverge visually across engines (breaking Tier D parity) and replays diverge across runs (breaking the seven-axis claim).

## What we know from the spec

- Round 2 Brief 022 — image engine deep dive (the pipeline VFX particles render through).
- Brief 152 — fixed/variable tick split; particle simulation runs on fixed for determinism, rendering on variable.
- Brief 153 — ECS particle.emitter component placeholder; this brief fills it.
- Brief 131 — seven-axis claim; VFX is signed and lineage-tracked.
- Brief 149 — v0.1 ships particle/VFX for 2D-default; 3D particles ship substrate but are gated to 3D-capable export targets.

## Findings

1. **Particle = transient ECS entity with `particle` component, lifetime-bounded.** Particles are entities, not opaque buffers. This makes them queryable, signable, and rollback-able like every other entity. Each particle carries `(position, velocity, age, lifetime, size, color, rotation, custom_floats[4])` at minimum. Custom_floats allow creator extensions without schema changes.

2. **Emitters are signed gseeds in `vfx.emitter`.** Schema: `(name, particle_template, spawn_rate, burst_schedule, lifetime_range, position_distribution, velocity_distribution, color_curve, size_curve, rotation_curve, modifiers[], render_mode)`. This is the consensus emitter shape from Shuriken/Niagara/Godot.

3. **Modifiers are typed sub-gseeds.** v0.1 ships: `gravity`, `drag`, `force`, `attractor`, `noise`, `vortex`, `collide_world`, `color_over_lifetime`, `size_over_lifetime`, `velocity_over_lifetime`, `align_to_velocity`, `trail`, `sub_emitter`. Modifiers run in a deterministic order set by the emitter gseed.

4. **GPU vs CPU path is signed per emitter.** A `vfx.emitter.compute = "cpu" | "gpu"` flag selects the path. CPU is deterministic by default and supports per-particle ECS queries (e.g., particles that detect collision and become entities). GPU is faster but more limited (no per-particle ECS interaction; deterministic only with strict compile flags). Default at v0.1: CPU for ≤500 particles per emitter, GPU for >500.

5. **Particle simulation runs on fixed tick; rendering on variable tick with interpolation.** Per Brief 152. Particle positions at variable-frame intermediates are interpolated between the two surrounding fixed-tick samples. Same fixed-tick state = same particles every replay regardless of display refresh rate.

6. **Determinism via the fixed-tick PRNG sub-seeding from Brief 152.** Particle spawning, randomized lifetime, randomized velocity, noise modifier — all use sub-seeds derived from `(scene_seed, tick, emitter_id)`. No private RNGs.

7. **VFX templates ship as canonical signed gseeds.** v0.1 ships ~40 starter templates: `explosion_small`, `explosion_large`, `fire`, `smoke`, `dust`, `spark`, `magic_burst`, `heal`, `damage_pop`, `pickup_glint`, `rain`, `snow`, `lightning`, `confetti`, `blood_splash`, `bullet_trail`, `laser_beam`, `shockwave`, `portal`, `teleport`, `level_up`, `coin_burst`, `splash`, `ripple`, `flame_jet`, `cloud_puff`, `slash_arc`, `impact_dust`, `weapon_glow`, `aura`, `electricity_arc`, `summon_circle`, `petals_falling`, `bubbles`, `steam`, `falling_leaves`, `water_droplets`, `embers`, `fireworks`, `spirit_orbs`. Each is a fully-authored signed `vfx.emitter` gseed creators can drop into a scene.

8. **Sub-emitters and chains.** A particle dying can spawn another emitter (e.g., a firework explodes into smaller fireworks; a bullet impact spawns sparks then smoke). Sub-emission is a typed modifier with signed parent lineage. Depth limit of 4 to prevent runaway chains.

9. **Decals and screen-space effects.** A `vfx.decal` is a flat textured quad pasted onto world surfaces (bullet holes, scorch marks, footprints). Lifetime-bounded. Signed. Stored as ECS entities. v0.1 ships 2D decals; 3D decals ship at v0.4 (3D-default).

10. **Weather and ambient systems.** Rain, snow, fog, dust motes ship as long-lived emitters with bounded particle counts and culling-aware spawning (only spawn within camera bounds + margin). Weather state is a signed scene-level gseed; weather changes propagate to lighting, audio, and gameplay (slippery surfaces).

11. **Trails and ribbons.** A `vfx.trail` is a particle that emits a strip following the parent entity's motion path over the last N samples. Ribbons are similar but render as continuous polygon strips. Both are typed primitives. Common uses: bullet trails, sword swipes, fire trails behind moving entities.

12. **Performance budget.** v0.1 budgets VFX at 3ms variable + 1ms fixed for: 5000 simultaneous CPU particles, 50,000 simultaneous GPU particles, 100 active emitters on the hardware floor. Brief 134 canonical battery validates.

13. **VFX export pipeline parity is non-trivial.** Different target engines have different particle systems. Tier D briefs handle this by exporting CPU-mode VFX as engine-native CPU particles (Phaser ParticleEmitter, GameMaker effect system) and GPU-mode VFX as engine-native GPU particles (Unity VFX Graph, Unreal Niagara, Godot GPUParticles), with a parity test (Brief 196) verifying visual similarity within tolerance.

14. **Differentiable VFX defaults.** Creator-tuned VFX templates that get high acceptance via the drift detector become genre-default suggestions for new projects. The 40 starter templates expand over time via federation.

## Risks identified

- **GPU determinism is fragile across drivers.** Mitigation: GPU-mode VFX is documented as "visually similar" not "bit-identical"; rollback-critical determinism stays on the CPU path; creators choose per emitter.
- **Sub-emitter chains can explode the particle budget.** Mitigation: depth limit of 4, hard particle cap per scene, drift detector emits `vfx.budget.breach`.
- **Decal accumulation in long sessions can balloon ECS entity count.** Mitigation: decals have a hard scene-wide cap (1024 default at v0.1); oldest decals fade and despawn first.
- **Weather systems' culling can pop visibly when camera moves fast.** Mitigation: spawn margin scales with camera velocity; ship as a built-in heuristic.
- **Cross-engine VFX visual divergence is the largest Tier D parity risk.** Mitigation: Brief 196 publishes per-template per-engine reference screenshots and visual-similarity bands; creators see expected divergence on hover.

## Recommendation

**GSPL ships a `vfx` namespace at v0.1 with: particles as ECS entities, signed `vfx.emitter` gseeds with the consensus shape, ~13 typed modifiers, signed CPU/GPU compute path selection (CPU default for ≤500, GPU above), fixed-tick deterministic simulation with variable-tick interpolation, sub-seeded PRNGs from Brief 152, ~40 canonical starter VFX templates as signed gseeds, sub-emitter chains with depth-4 limit, decals as lifetime-bounded ECS entities (1024 cap), weather and ambient systems as long-lived emitters with camera-aware culling, trails and ribbons as typed primitives, ~5000 CPU + ~50,000 GPU particle budget with 100 active emitters on the hardware floor, signed export-pipeline parity to all 8 Tier D targets with documented similarity tolerance, and creator-tuned VFX templates propagating via the Differentiable axis.**

## Confidence

**4/5.** The architecture is the consensus of Shuriken, Niagara, GPUParticles, and Phaser, with the seven-axis discipline added. The 5th confidence point waits on Brief 196 actually validating cross-engine parity for the 40 starter templates.

## Spec impact

- `gspl-reference/namespaces/vfx.md` — new namespace
- `gspl-reference/research/152-game-loop-tick-model-namespace.md` — fixed-tick simulation, variable-tick render
- `gspl-reference/research/153-ecs-substrate-binding.md` — particle, decal as ECS entities; emitter as ECS component
- `gspl-reference/research/022-image-engine-deep-dive.md` — render path
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — VFX battery: 5k CPU + 50k GPU at 60 Hz, 40-template parity test
- Tier D Brief 196 — VFX cross-engine parity validation
- Tier H Brief 224 — game-feel and juice library composes VFX with audio + camera shake

## New inventions

- **INV-645** — *Particles as queryable signed ECS entities* (not opaque buffers) so they inherit the seven-axis discipline and can be inspected, replayed, rolled back, and lineage-tracked like any other entity.
- **INV-646** — *40-template canonical VFX starter library* shipped as signed `vfx.emitter` gseeds — covers ~80% of v0.1 starter-genre VFX needs without composition.
- **INV-647** — *Per-emitter signed CPU/GPU compute selection* with deterministic CPU as the default for low particle counts and documented GPU "similar-not-identical" mode for high counts.
- **INV-648** — *Sub-emitter chain with depth limit and signed parent lineage* — common bug source (runaway chains) becomes structural impossibility past depth 4.
- **INV-649** — *Camera-velocity-aware weather culling* — spawn margin scales with camera motion, eliminating the visible weather pop creators usually patch by hand.

## Open follow-ups

- Whether v0.1 ships a visual VFX editor (Tier C Brief 182, provisional yes for v0.1).
- 3D decal projection at v0.4 — defer.
- VFX streaming for very-long sessions (memory budget concerns) — defer to Tier G Brief 222.

## Sources

- Brief 131 — seven-axis structural claim
- Brief 134 — substrate-native benchmark battery
- Brief 143 — differentiable action learning recipe
- Brief 144 — drift detector threshold calibration
- Brief 149 — v0.1 scope finalization
- Brief 152 — game loop and tick model namespace
- Brief 153 — ECS substrate binding
- Round 2 Brief 022 — image engine deep dive
- Unity Shuriken / VFX Graph documentation
- Unreal Niagara documentation
- Godot GPUParticles2D / GPUParticles3D documentation
- Phaser ParticleEmitter documentation
- Vlambeer "Art of Screenshake" GDC talk (juice and VFX layering)
