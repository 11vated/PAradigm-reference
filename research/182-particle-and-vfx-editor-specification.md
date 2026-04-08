# 182 — Particle and VFX editor specification

## Question
What is the creator-facing editor surface that authors `vfx.system`, `vfx.emitter`, and `vfx.module` (Brief 162) gseeds with curve editing, GPU/CPU toggle, deterministic seed input, and live preview?

## Why it matters (blast radius)
VFX is the densest tunable surface — a single emitter has 30+ parameters. If the editor doesn't make those parameters scrubbable with live preview, creators iterate by trial and error. If GPU and CPU paths produce different visuals, creators have to author twice. If the deterministic seed isn't a first-class control, the substrate's replay guarantee silently breaks for VFX.

## What we know from the spec
- Brief 162 — particle and VFX runtime, emitters, simulators, GPU/CPU paths, deterministic mode, typed VFX gseeds.
- Brief 152 — fixed-tick scheduler.
- Brief 156 — physics integration (used by physics-affected particles).
- Brief 161 — animation runtime (referenced for spawning particles on animation events).
- Brief 177, 178, 179 — modifier-surface inheritance.

## Findings
1. **Editor surface = curve editor + module stack + preview viewport.** The editor renders an emitter as a vertical stack of typed `vfx.module` rows (spawn / shape / velocity / size / color / rotation / drag / gravity / collision / sub-emitter / trail / mesh / lighting / sound). Each row hosts curves and constants. Curves use the same widget as Brief 179's animation editor (linear / bezier / catmull-rom).
2. **Module add/remove as typed mutation.** Adding a module compiles to `vfx.emitter.add_module`. Removing one is a single signed mutation. Module reorder is a typed mutation; sign-time validation enforces dependency rules (e.g., a `trail` module requires a `shape` module upstream).
3. **Curve editing inheritance.** Curves are typed channels identical to Brief 179. Editing curves emits one mutation per drag (mouse-up batched). Same seven curve types ship at v0.1.
4. **Live preview.** The viewport runs the runtime simulator at the editor's preview rate. Pause / step / restart / loop controls map to substrate-level tick controls. The preview camera is editor-runtime ephemeral, not signed.
5. **Deterministic seed input.** Every emitter has a typed `vfx.seed` field. Set it to a fixed value and the simulator produces bit-identical particle motion every replay (per Brief 162's deterministic mode). The editor exposes a "randomize seed" button and a "lock seed" toggle.
6. **GPU vs CPU toggle.** A typed `vfx.simulator_target` field on the emitter selects GPU (default for visual-only emitters) or CPU (default when physics collision or trigger interactions are enabled). The editor surfaces a "preview matches runtime" indicator: green when both paths produce visually identical output, yellow with a typed warning when they diverge (e.g., when CPU-only modules are stacked on a GPU emitter).
7. **Sub-emitter graph.** Sub-emitters render as a tree below the parent emitter. Spawn-on-collide / spawn-on-death / spawn-per-tick are typed sub-emitter triggers. Sign-time validation rejects circular sub-emitter chains.
8. **Mesh particle support.** A particle can be sprite, billboard mesh, or full mesh. Mesh references are typed asset refs validated at sign time.
9. **Force field and collision.** Force fields (Brief 084 particles-and-fields) and collision targets (Brief 157) are referenced via typed handles. Sign-time validation rejects refs to nonexistent fields.
10. **Texture sheet animation.** Particle textures can be flipbook sheets with typed frame-count, frames-per-second, and start-frame randomization parameters. Same atlas frame-name stability contract as Brief 179.
11. **Performance budget.** A typed `vfx.budget` per system declares max-active-particles, max-spawn-rate, and a CPU/GPU time target. Sign-time heuristic check; runtime measurement in the playtest harness (Brief 185).
12. **Light probe and lighting integration.** Particles can opt into scene lighting via a typed `vfx.lighting_mode` enum (unlit / flat / per-vertex / per-particle). v0.1 ships unlit + flat for 2D; per-vertex and per-particle deferred to v0.4 with 3D physics.
13. **Sound binding.** A particle event can emit a sound cue via a typed `audio.event_ref` — first-class binding to Brief 175 audio patterns, not bolted on.

## Risks identified
- **GPU/CPU divergence under stress.** GPU floating-point reproducibility across vendors is bounded (per Brief 001). Mitigation: deterministic mode forces CPU path; GPU path is for non-replay visual emitters; the editor's "preview matches runtime" indicator surfaces divergence proactively.
- **Curve interpolation precision drift.** Different curve evaluators on GPU and CPU could produce slightly different values. Mitigation: both paths use the same fixed-point evaluator from Brief 026 (deterministic kernel implementation).
- **Sub-emitter spawn explosions.** A poorly tuned chain can create N^2 particles. Mitigation: sign-time depth cap of 4 sub-emitter levels; runtime hard cap on total active particles per `vfx.system`, with overflow particles silently dropped (logged at sign-time test).
- **Mesh particle memory cost.** Large meshes per particle blow VRAM. Mitigation: editor warns at sign time if mesh vertex count × max active particles exceeds a configurable budget.
- **Curve editor performance.** Editing 30+ curves simultaneously on a complex emitter can be slow. Mitigation: per-module collapse, with curves rendering only for the expanded module.

## Recommendation
Specify the VFX editor as a module-stack + curve-editor + viewport surface inheriting Briefs 177/179's modifier-surface and curve contracts. Ship the deterministic seed control as a first-class field. Default to CPU path when collision is enabled and GPU otherwise, with a divergence indicator. Defer per-particle 3D lighting to v0.4. Expose `vfx.budget` as a typed sign-time + runtime check.

## Confidence
**4.5 / 5.** Particle editor patterns are converged across Unity Particle System / Unreal Niagara / Godot GPUParticles / Cascade / Effekseer. The novelty is the deterministic-seed-as-first-class-field, the GPU/CPU divergence indicator, and the lineage-signed module stack. Lower than 5 because the GPU/CPU divergence detector heuristic needs Phase-1 calibration.

## Spec impact
- New spec section: **Particle and VFX editor surface specification**.
- Adds `vfx.simulator_target` typed enum.
- Adds `vfx.seed`, `vfx.budget`, `vfx.lighting_mode` typed fields.
- Cross-references Briefs 162, 179, 177, 026.

## New inventions
- **INV-744** — Module-stack VFX editor with typed module dependency rules: modules compose top-down with sign-time validation that upstream dependencies are present.
- **INV-745** — Deterministic seed as first-class emitter field: every emitter exposes a creator-authored seed; setting it locks the emitter to bit-identical replay across the substrate.
- **INV-746** — GPU/CPU divergence indicator at edit time: the editor surfaces a typed warning when the chosen simulator target produces visuals that differ from the alternate path.
- **INV-747** — Sub-emitter typed depth cap with runtime overflow drop: depth-of-4 cap at sign time, runtime active-particle ceiling per system with logged overflow.
- **INV-748** — Atlas frame-name stability for texture sheet animation: same contract as Brief 179, so atlas re-pack does not invalidate flipbook references.

## Open follow-ups
- Per-particle 3D lighting and shadow casting (deferred to v0.4).
- Niagara-style data interface bindings (deferred to v0.2 as advanced authoring).
- Voxel and mesh-particle volumetric effects (deferred to v0.4).
- Auto-LOD for particle systems on distance (deferred to v0.4).

## Sources
1. Brief 001 — GPU determinism cross-vendor.
2. Brief 026 — Deterministic kernel implementation.
3. Brief 084 — Particles and fields.
4. Brief 152 — Game loop and tick model.
5. Brief 156 — Physics integration.
6. Brief 157 — Collision and trigger primitives.
7. Brief 162 — Particle and VFX runtime.
8. Brief 175 — Sound design and music pattern library.
9. Brief 177 — Scene editor modifier surface.
10. Brief 179 — Animation editor specification.
11. Unreal Engine Niagara documentation.
12. Unity Particle System Manual.
