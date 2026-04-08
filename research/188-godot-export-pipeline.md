# 188 — Godot export pipeline

## Question
What is the export pipeline that produces a complete, runnable Godot 4.x project from a signed GSPL gseed bundle, with parity-tested 2D and 3D output, GDScript scene files, and resource serialization?

## Why it matters (blast radius)
Godot is the reference engine for Round 7's export discipline (Round 7 plan). If parity is not achieved here first, parity for the other 7 engines becomes a moving target. Creators choose engines based on what their game looks like *after* export — if Godot output drifts from preview, the substrate's "preview = runtime" promise stops at the export boundary.

## What we know from the spec
- Brief 020 — determinism contract per engine.
- Brief 028 — per-engine spec format.
- Brief 065 — game engines deep dive (Unity, Unreal, Godot).
- Brief 089 — universal anything-to-gseed pipeline (the inverse direction).
- Briefs 152-176 — every Tier A and B namespace that needs an export mapping.
- Round 7 plan — Godot is the reference engine; first-class parity; 2D and 3D.

## Findings
1. **Pipeline = typed exporter graph.** A typed `export.target` gseed declares the target engine (godot_4_3 here), the target version range, and the output directory. The exporter graph maps each substrate namespace to a per-engine emitter. Each emitter is a typed function from `(gseed, export_context) -> file_set`.
2. **Scene mapping.** `level.scene` (Brief 172) → Godot `.tscn` text scene file. The scene tree maps to Godot's SceneTree; entities (Brief 153) become Node3D / Node2D / Control nodes per their archetype. Components map to typed Node properties or attached Node children.
3. **Tilemap mapping.** `tilemap.layer` (Brief 173) → Godot `TileMap` node + `TileSet` resource. Brief 173's 47-tile and 16-tile autotile maps to Godot's terrain tile system. Procgen-generated tiles export as static cell data with the procgen seed recorded as scene metadata for future re-roll.
4. **Animation mapping.** `animation.clip` (Brief 161) → Godot `Animation` resource. `animation.blend_tree` → `AnimationTree` node + `AnimationNodeBlendTree`. Skeletal data → `Skeleton2D` / `Skeleton3D`. IK chains → `SkeletonModification2D` / `SkeletonModification3D` per Godot's IK family.
5. **Audio mapping.** `audio.bus` (Brief 175) → Godot `AudioBusLayout` resource. `audio.clip` → `AudioStreamWAV` / `AudioStreamOGGVorbis`. Mixer routing maps to AudioServer.bus_layout. Effects map to Godot's `AudioEffect*` family where equivalents exist; otherwise the substrate's deterministic effect kernel ships as a `.gdextension` plugin.
6. **UI mapping.** `ui.element` (Brief 174) → Godot `Control` node tree. The 5 layout primitives map directly: flow → HBoxContainer/VBoxContainer; grid → GridContainer; stack → BoxContainer; absolute → manual offsets; constraint → AnchorPreset + custom layout.
7. **VFX mapping.** `vfx.system` (Brief 162) → Godot `GPUParticles2D` / `GPUParticles3D` for GPU emitters; `CPUParticles2D/3D` for CPU emitters. Module stack maps to ParticleProcessMaterial properties. The deterministic seed becomes the particles `seed` property.
8. **Behavior tree / FSM mapping.** Brief 159's BT/FSM has no native Godot equivalent. The pipeline emits a typed `bt.gd` GDScript file implementing Brief 159's tick semantics, plus the BT data as a JSON resource. Same for FSM via Godot's `StateMachine` AnimationNode for trivial cases, GDScript for complex.
9. **Save / load mapping.** `save.snapshot` (Brief 158) → Godot's `ConfigFile` or `FileAccess` calls in a generated `save_manager.gd`. Partial save chunks map to per-chunk files.
10. **Input mapping.** `input.action` (Brief 154) → Godot `InputMap` actions. Per-binding mappings (keyboard / gamepad / touch) export to Godot's input event types.
11. **Physics mapping.** Brief 156 2D physics → Godot 4 Box2D-class CharacterBody2D / RigidBody2D / StaticBody2D + CollisionShape2D. 3D physics → equivalent 3D nodes. Collision tags / masks (Brief 157) export to Godot's collision_layer / collision_mask bitmasks.
12. **Camera mapping.** `camera.rig` (Brief 155) → Godot `Camera2D` / `Camera3D` with `RemoteTransform` for follow, `PhantomCamera`-class for cinematic shots. `camera.shot` → typed cinematic data on a generated controller.
13. **Determinism preservation.** Brief 020's per-engine determinism contract is enforced via deterministic kernel emission (Brief 026). Floating-point math goes through fixed-point or strictly-rounded paths via the substrate's `det_kernel.gd` ext. Random number generation uses sub-seeded PRNGs ported to GDScript.
14. **Asset bundle.** All textures, audio, meshes, and fonts export to Godot's import directory with `.import` metadata files generated to match the substrate's import settings (Brief 089).
15. **Project file.** A `project.godot` is generated with substrate-derived settings: rendering backend (forward+/mobile/compatibility per target), input map, autoload list (det_kernel, save_manager, lineage_recorder), main scene, target resolution.
16. **Lineage stub.** A typed `lineage_recorder.gd` autoload captures runtime mutations into a JCS-canonical file at exit, allowing post-export replay verification against the source gseed.

## Risks identified
- **Engine version drift.** Godot 4.3, 4.4, 4.5 have minor scene format differences. Mitigation: target version range in `export.target`; emitter graph branches per minor version.
- **Effect / shader gap.** Some substrate audio effects (e.g., FDN reverb) lack Godot equivalents. Mitigation: ship `det_kernel.gdextension` C++ plugin with the substrate's deterministic implementations.
- **GDScript performance.** Hot loops in GDScript are slow. Mitigation: critical paths (BT tick, FSM update, AI pathfinding) emit as `.gdextension` C++ where the substrate has a kernel implementation; pure GDScript fallback for non-critical paths.
- **Tile autotile mismatch.** Godot's terrain system has different bitmask conventions than Brief 173. Mitigation: emitter translates Brief 173's 47-tile bitmask to Godot's terrain set at export, with sign-time validation that no tile is dropped.
- **Editor round-trip.** Creators may want to edit the exported Godot project and round-trip back. Mitigation: not supported at v0.1; round-trip deferred to v0.3 because it requires AST parsing of GDScript.

## Recommendation
Specify the Godot exporter as a typed emitter graph mapping every substrate namespace to a Godot 4.3+ resource or generated GDScript module, with `det_kernel.gdextension` shipping the deterministic kernels Godot lacks. Ship 2D and 3D parity from v0.1 (Godot's 2D/3D parity is structurally cleaner than Unity's). Defer GDScript round-trip to v0.3.

## Confidence
**4.5 / 5.** Godot's open-source scene format and well-documented APIs make this the highest-confidence exporter. The novelty is the deterministic kernel as a gdextension plugin and the lineage_recorder autoload. Lower than 5 because real performance under heavy substrate scenes needs Phase-1 measurement.

## Spec impact
- New spec section: **Godot export pipeline specification**.
- Adds `export.target` typed primitive.
- Adds `det_kernel.gdextension` as a substrate-shipped Godot plugin.
- Adds the per-namespace emitter mapping table.

## New inventions
- **INV-774** — Typed export emitter graph: every namespace has a typed function `(gseed, context) → file_set` that emits engine-native artifacts, composable into a full export.
- **INV-775** — `det_kernel.gdextension` shipping substrate kernels Godot lacks: deterministic floating-point math, audio effects, BT/FSM tick, sub-seeded PRNG — all as one C++ plugin.
- **INV-776** — Lineage recorder autoload per export: every exported game ships with a lineage capture stub so post-export replay verification is automatic.
- **INV-777** — 47-tile to Godot terrain bitmask translator with sign-time tile-loss check: ensures Brief 173 autotile output survives engine translation.
- **INV-778** — `procgen.seed_record` preserved as scene metadata: exported games can re-roll procgen regions deterministically using the original seed.

## Open follow-ups
- Godot round-trip (creator edits in Godot, re-imports to substrate) — deferred to v0.3.
- Mobile target presets (Android / iOS export configs) — deferred to v0.4.
- Console targets via Godot 4 console exporters — deferred to v0.5.
- HTML5 via Godot's web export (separate path from Brief 193) — deferred to v0.2.

## Sources
1. Brief 020 — Determinism contract per engine.
2. Brief 026 — Deterministic kernel implementation.
3. Brief 028 — Per-engine spec format.
4. Brief 065 — Game engines deep dive.
5. Brief 089 — Universal anything-to-gseed pipeline.
6. Briefs 152-176 — Tier A and B namespaces.
7. Godot 4 documentation (docs.godotengine.org/en/stable/).
8. Godot scene file format (`.tscn`) reference.
9. Godot GDExtension documentation.
