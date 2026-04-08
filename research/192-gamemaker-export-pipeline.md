# 192 — GameMaker export pipeline

## Question
What is the export pipeline that produces a complete GameMaker Studio 2 / GameMaker LTS project from a signed GSPL gseed bundle, with GML scripts, sprite-first asset organization, and 2D-only output for the indie game-jam creator population?

## Why it matters (blast radius)
GameMaker is the dominant tool for indie 2D games (Undertale, Hyper Light Drifter, Hotline Miami, Spelunky). Its creator population is large, sprite-centric, and engine-loyal. Exporting to GameMaker brings GSPL into the indie 2D space without forcing those creators to learn another engine.

## What we know from the spec
- Brief 188 — Godot export pipeline (reference exporter).
- Brief 191 — Phaser export pipeline (web 2D export).
- Brief 020 — determinism contract per engine.
- Brief 065 — game engines deep dive (GameMaker is referenced as the indie 2D standard).
- Briefs 152-176.

## Findings
1. **Emitter graph inheritance.** Inherits Brief 188's emitter graph. GameMaker-specific target declares: target version (GameMaker LTS 2022 or GameMaker Studio 2 2024+), output platform (Windows / HTML5 / Mobile), GML version, and asset compression settings.
2. **2D-only enforcement.** Same as Brief 191 — GameMaker is 2D. Sign-time gate rejects 3D scenes with an alternate-target hint.
3. **Project format.** GameMaker projects are a `.yyp` JSON descriptor + per-asset `.yy` files in a directory tree (`sprites/`, `objects/`, `rooms/`, `scripts/`, `sounds/`, `fonts/`, `tilesets/`, `shaders/`). The exporter generates the full tree.
4. **Scene → Room mapping.** `level.scene` (Brief 172) → GameMaker `Room` asset. Substrate entities become Room instances with object references; substrate components map to per-instance variables set in the room's creation code.
5. **Entity → Object mapping.** Brief 153 entities → GameMaker `Object` assets. Each substrate archetype generates one Object class with substrate-derived event handlers (Create / Step / Draw / Destroy / Collision). Components attach via Object instance variables.
6. **Sprite mapping.** Sprites from Brief 088A seed armory → GameMaker `Sprite` assets with frame-strip layout. Substrate's atlas is unpacked into individual sprite assets per GameMaker conventions.
7. **Tilemap mapping.** `tilemap.layer` (Brief 173) → GameMaker `Tileset` + Room tile layer. Brief 173's autotile is exported as static cell data (GameMaker has its own autotile but the bitmask conventions differ; substrate translates).
8. **Animation mapping.** `animation.clip` sprite-frame channels → GameMaker sprite frame strips with per-frame timing via image_speed and image_index. Skeletal animation requires GameMaker's Spine integration (Brief 195).
9. **Audio mapping.** `audio.bus` → GameMaker Audio Groups. Substrate's deterministic effect kernel ships as a substrate GML script library because GameMaker's audio effects are limited and platform-specific. The eight v0.1 effects implement in GML against `audio_emitter_*` APIs where possible.
10. **UI mapping.** `ui.element` (Brief 174) → GameMaker UI rendered via Draw GUI events on a controller object. Substrate provides `substrate_ui.gml` script library implementing the 5 layout primitives in GML.
11. **VFX mapping.** `vfx.system` → GameMaker Particle System. Module stack maps to particle type/emitter setup. Deterministic seed → substrate's PRNG library since GameMaker's `random_set_seed` is global and not deterministic across versions.
12. **Behavior tree / FSM.** No native equivalent. Substrate ships `substrate_bt.gml` and `substrate_fsm.gml` script libraries implementing Brief 159's tick semantics.
13. **Save / load.** `save.snapshot` → GameMaker `ds_map_*` + `buffer_save` for binary, or JSON files for text. Partial chunks → multi-file saves under `working_directory`.
14. **Input mapping.** `input.action` → GameMaker `keyboard_*`, `mouse_*`, `gamepad_*` API wrappers in a substrate `InputAdapter.gml` script.
15. **Physics mapping.** Brief 156 2D physics → GameMaker's built-in Box2D wrapper or substrate's deterministic kernel as a GML library. Default to substrate kernel for replay-critical entities.
16. **GML version compatibility.** GameMaker LTS uses GML 2022.x; latest uses GML 2024.x with new features. Exporter targets LTS GML for the broadest compatibility floor.
17. **Lineage stub.** Substrate `substrate_lineage.gml` script captures runtime mutations to a JSON file at game exit.

## Risks identified
- **GameMaker's licensing model.** GameMaker is commercial closed-source with per-platform export licenses. Mitigation: substrate generates open project files; creators handle their own GameMaker licensing — substrate has no obligation.
- **GML performance ceiling.** GML is interpreted; complex BTs and AI tick loops can be slow. Mitigation: critical paths use GameMaker's `function`-keyword optimized GML; document the perf ceiling for creators considering large entity counts.
- **GameMaker version churn.** GameMaker has had multiple format breaks (GMS 1 → 2 → 2024). Mitigation: target only GMS 2 LTS and GMS 2 latest; refuse export to GMS 1.
- **Audio effect gap.** GameMaker has very limited audio effects. Mitigation: substrate's GML effect library is a slow but accurate fallback; creators can opt out and accept reduced fidelity.
- **Tilemap autotile bitmask mismatch.** GameMaker's autotile differs from Brief 173. Mitigation: same as Phaser — export static cell data, ignore GameMaker autotile.

## Recommendation
Specify the GameMaker exporter as Brief 188's emitter graph specialized for GameMaker LTS 2022+ with `.yyp` project generation, sprite-first asset organization, GML script library shipping the substrate runtime modules, and 2D-only sign-time gating. Defer GameMaker round-trip and GML 2024 advanced features to v0.2.

## Confidence
**4 / 5.** GameMaker's project format is documented and the GML language is approachable. The novelty is the substrate GML runtime library shipping deterministic kernels in an interpreted language. Lower than 4.5 because GML performance under heavy substrate scenes is the main empirical question for Phase 1.

## Spec impact
- New spec section: **GameMaker export pipeline specification**.
- Adds GameMaker-specific `export.target` parameters.
- Adds substrate GML runtime library specification (`substrate_bt.gml`, `substrate_fsm.gml`, `substrate_physics.gml`, `substrate_ui.gml`, `substrate_audio.gml`, `substrate_lineage.gml`).
- Cross-references Briefs 188, 191.

## New inventions
- **INV-794** — Substrate GML runtime library: deterministic BT/FSM/physics/UI/audio/lineage modules implemented in GML for any GameMaker target.
- **INV-795** — `.yyp` project + per-asset `.yy` file emission with substrate-derived asset organization: projects are generated open and editable inside GameMaker IDE.
- **INV-796** — Sprite-first asset unpacking from substrate atlases to GameMaker sprite frame strips: substrate's packed atlases unpack idiomatically for GameMaker's sprite-centric workflow.
- **INV-797** — Critical-path GML optimization via `function` keyword with substrate-author comments: generated code follows GameMaker performance best practices.

## Open follow-ups
- GameMaker round-trip (deferred to v0.3).
- GML 2024 advanced features (deferred to v0.2).
- GameMaker mobile platform export (deferred to v0.4).
- Console exports via GameMaker's licensed platforms (deferred to v0.5).

## Sources
1. Brief 020 — Determinism contract per engine.
2. Brief 065 — Game engines deep dive.
3. Brief 156 — Physics integration.
4. Brief 159 — State machines and behavior trees.
5. Brief 188 — Godot export pipeline.
6. Brief 191 — Phaser export pipeline.
7. GameMaker LTS documentation (manual.gamemaker.io).
8. GML language reference.
9. GameMaker Studio 2 file format reference (community-documented).
