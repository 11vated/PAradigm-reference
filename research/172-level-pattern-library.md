# 172 — Level pattern library

## Question

What canonical level patterns does GSPL ship in `level.*` so that any genre can compose platformer rooms, dungeon templates, racetrack layouts, RTS map archetypes, puzzle grids, narrative scenes, and arena types from typed signed primitives, with parameter bounds, biome bindings, and v0.1 reach?

## Why it matters (blast radius)

Levels are the *spatial content unit* most games ship at scale. Without typed level primitives, every game reinvents room metrics, encounter placement, lighting setup, and traversal flow, breaking cross-game tooling for level analytics, balance, and procedural generation. Brief 173 (procgen) generates levels into these patterns, Brief 177 (scene editor) edits them, Brief 168 (encounters) instantiates inside them, Brief 170 (quests) reference them as locations, Brief 197-208 (genre families) compose them, and Brief 224 (game feel) tunes them.

## What we know from the spec

- Brief 153 — ECS substrate; levels are typed scene gseeds containing entities
- Brief 155 — camera; levels declare default camera modes and bounds
- Brief 156/157 — physics/collision; levels carry collider geometry
- Brief 158 — save/load; level state can be saved per Brief 158's pointer-or-full save kinds
- Brief 173 — procedural generation; populates the patterns this brief defines
- Brief 177 — scene editor; the authoring surface

## Findings

1. **`level.scene` as the root primitive.** A level is a typed signed gseed `level.scene` with: `scene_id`, `dimensions: (f32, f32, f32)`, `tilemap_ref: optional<tilemap_ref>`, `entities: set<entity_ref>`, `camera_default: camera_mode_ref`, `lighting_setup_ref`, `audio_environment_ref`, `physics_world_ref`, `loading_strategy: enum{single, streaming, sub_scene}`, `tags: set<TagId>`, `signing_authority`. Scene = ECS world (Brief 153) plus spatial metadata. Forking a scene preserves lineage.

2. **Twelve canonical pattern families.** Surveying Mario, Celeste, Hollow Knight, Dark Souls, Spelunky, Hades, Diablo, Doom, Quake, Counter-Strike, StarCraft, Civilization, Stardew Valley, Persona, and visual novels yields **12 canonical level pattern families**: `level.pattern.platformer_room`, `level.pattern.metroidvania_room`, `level.pattern.dungeon_chamber`, `level.pattern.dungeon_corridor`, `level.pattern.open_area`, `level.pattern.arena`, `level.pattern.racetrack`, `level.pattern.rts_map`, `level.pattern.puzzle_grid`, `level.pattern.narrative_scene`, `level.pattern.hub`, `level.pattern.transition`. Each is a parameterized template with default metrics, gates, encounters, and props.

3. **`level.pattern.platformer_room`.** Parameters: `width_tiles: u16 ∈ [16, 256]`, `height_tiles: u16 ∈ [9, 64]`, `gravity_dir: enum{down, up, variable}`, `entry_points: set<edge_marker>`, `exit_points: set<edge_marker>`, `mechanic_focus: set<mechanic_ref>` (Brief 164.move.*), `difficulty_band: u8 ∈ [1, 10]`. Default ships with 8 named sub-templates: `tutorial`, `simple_jumps`, `wall_jumps`, `dash_corridor`, `vertical_climb`, `enemy_gauntlet`, `puzzle_room`, `boss_arena_2d`.

4. **`level.pattern.metroidvania_room`.** Like platformer room but with: `gating_abilities: set<ability_ref>`, `secret_count: u8`, `lore_objects: set<object_ref>`, `connections_to: set<scene_ref>`. Hollow Knight/Symphony of the Night class. Substrate-level reachability validation runs at sign time: every gated path must be reachable from start under at least one ability set.

5. **`level.pattern.dungeon_chamber` and `dungeon_corridor`.** The Diablo/roguelike unit. Chamber parameters: `chamber_kind: enum{combat, treasure, puzzle, shop, rest, boss, secret}`, `entry_count: u8`, `exit_count: u8`, `encounter_ref`, `theme_ref`. Corridor parameters: `length_tiles`, `width_tiles`, `straightness: f32`, `enemy_density: f32`. Chambers connect via corridors in a typed graph (`level.dungeon.graph`) which Brief 173 procgen populates.

6. **`level.pattern.open_area`.** Open-world chunks (Skyrim, Witcher 3, BotW). Parameters: `area_size: (f32, f32)`, `biome_ref: brief_086_ref`, `points_of_interest: set<poi_ref>`, `streaming_radius: f32`, `density_curve_ref`. The substrate's streaming loader (Brief 153) handles entity unload/reload at the radius.

7. **`level.pattern.arena`.** A bounded combat space (Hades chambers, Doom Eternal arenas, Devil May Cry rooms). Parameters: `bounds: aabb`, `wave_set_ref: encounter_ref` (Brief 168), `cover_density: f32`, `cover_archetypes: set<cover_ref>`, `arena_shape: enum{rectangular, circular, multi_tier, asymmetric}`, `escape_blocked_until: predicate`. The substrate ships ~12 named arena templates including Doom-style and Hades-style defaults.

8. **`level.pattern.racetrack`.** Parameters: `track_spline: spline_ref`, `lap_count`, `width_curve_along_spline: curve_ref`, `surface_type_per_segment: ordered_set<surface_id>`, `checkpoint_count`, `track_kind: enum{closed_circuit, point_to_point, rally, drift}`. Procedural racetracks (Brief 173) operate on this primitive.

9. **`level.pattern.rts_map`.** Parameters: `playable_area: aabb`, `start_locations: ordered_set<spawn_point>`, `resource_nodes: set<resource_ref>`, `chokepoints: set<chokepoint_marker>`, `expansion_sites: set<expansion_marker>`, `pathing_grid_ref`. Standard symmetric/asymmetric multiplayer RTS map. v0.3+ multiplayer hooks; v0.1 single-player skirmish supported.

10. **`level.pattern.puzzle_grid`.** Parameters: `grid_dims: (u16, u16)`, `cell_kind_palette: set<cell_kind_id>`, `initial_state: grid_state`, `solution_state: optional<grid_state>`, `solver_validation: bool`. Used by sokoban, match-3, hidden-object, tile-laying. Substrate-level *solvability* check optionally runs at sign time using a constraint solver.

11. **`level.pattern.narrative_scene`.** Parameters: `participants: set<entity_ref>`, `staging_marks: set<mark_ref>`, `dialogue_graph_ref` (Brief 171), `cutscene_ref: optional<cutscene_ref>` (Brief 176), `interactivity_kind: enum{cutscene_only, hybrid, free_explore}`, `exit_condition: predicate`. Visual novel and walking sim core unit.

12. **`level.pattern.hub`.** A safe central scene from which other scenes branch (Hades House of Hades, Hollow Knight Dirtmouth, Persona Velvet Room). Parameters: `connected_scenes: set<(scene_ref, exit_marker)>`, `hub_services: set<service_ref>` (vendor, save, upgrade, social), `default_spawn_point`. The substrate validates that every connected scene has a return edge.

13. **`level.pattern.transition`.** A small intermediate scene for loading/cinematic continuity (Mario world map, Souls bonfire teleport, FFXIV inn). Parameters: `from_scene_ref`, `to_scene_ref`, `transition_kind: enum{fade, cinematic, walk_through, instant, loading_screen}`, `transition_duration_ticks`. Often invisible to players but essential for streaming.

14. **Pattern composition.** A real game scene combines patterns: a Hades chamber is `arena + transition`, a Hollow Knight room is `platformer_room + metroidvania_room`, a Witcher quest scene is `open_area + narrative_scene`. The substrate's `level.composition` gseed binds N patterns into one scene with explicit overlap semantics.

15. **Theme and biome binding.** Each scene/pattern can declare a `theme_ref` (visual style, palette) and `biome_ref` (Brief 086 ecological binding). Themes drive automatic prop selection, lighting presets, audio environment, and particle defaults. Biomes drive procgen generation (Brief 173) parameter sets.

16. **Validation.** Every level scene validates at sign time: (a) every entry point reaches every exit point under at least one player ability set; (b) collision geometry is closed (no holes leak players out of bounds); (c) camera bounds (Brief 155) are within scene dimensions; (d) entity references resolve; (e) dependent assets (textures, audio, prefabs) are present in the project. Validation failures are warnings or errors per severity.

17. **v0.1 reach.** All 12 pattern families ship at v0.1 schemas. Sub-templates: `platformer_room` (8/8), `metroidvania_room` (4/4), `dungeon_chamber` (7/7), `arena` (12/12 — but 3D-default arenas defer 3D-specific parameters to v0.4), `racetrack` (4/4 — runtime gated to v0.4 for 3D), `rts_map` (4/4 — runtime gated to v0.3 multiplayer), `puzzle_grid` (full), `narrative_scene` (full), `hub` (full), `transition` (full). 2D variants of every pattern ship runtime at v0.1; 3D-specific runtimes gate per Brief 156 physics 3D deferrals.

## Risks identified

1. **Pattern overfitting.** A 12-family taxonomy may not cover unusual genres (idle games, deck-builders, walking sims-only games). Mitigation: `level.pattern.minimal` escape hatch with no spatial metadata; deck-builders and idle games can use it.

2. **Reachability validation is expensive.** A metroidvania with 100 rooms and 20 abilities has 2^20 reachability combinations. Mitigation: validation caches per ability set; uses BDD-style compact representation; runs incrementally on edits.

3. **Solvability check on puzzles is undecidable in general.** Mitigation: solver gives up after a fixed budget and emits a warning; creator can override.

4. **Streaming radius vs determinism.** Two clients with different streaming distances see different entities. Mitigation: streaming is *load* but not *spawn*; entity existence is per-tick deterministic, only memory residency varies.

5. **Theme/biome mismatch with assets.** A creator binds a "tundra" biome theme to a tropical asset pack. Mitigation: warning at sign time if theme tags and asset tags conflict.

6. **Hub circular references.** Hub A → Hub B → Hub A. Mitigation: legitimate; the substrate just tracks the connection graph and ensures both have spawn markers for both directions.

## Recommendation

Ship the `level.*` namespace with `level.scene` root, 12 canonical pattern families, sign-time reachability/closure/asset/camera/entity validation, and theme/biome binding. Wire procgen (Brief 173) and scene editor (Brief 177) to read the typed pattern library at v0.1. Hold 3D-specific runtimes per Brief 156 deferrals; everything 2D ships fully at v0.1.

## Confidence

**4/5.** Pattern decomposition is grounded in 30+ years of level design talks and academic level analysis (Hocking, Pearce, Schell). Held back from 5 by the validation complexity (esp. metroidvania reachability) which will need empirical sizing in Round 8.

## Spec impact

- Add `level.*` namespace with scene root and 12 pattern sub-namespaces
- Add `level.composition` gseed for multi-pattern scenes
- Add `level.dungeon.graph` typed gseed for chamber/corridor connectivity
- Add sign-time validation rules (reachability, closure, asset, camera, entity refs)
- Cross-link to Brief 086 (biome refs), Brief 153 (entities), Brief 155 (camera bounds), Brief 156 (physics world), Brief 157 (collision), Brief 161 (animation), Brief 168 (encounter consumer), Brief 170 (quest location refs), Brief 173 (procgen producer), Brief 175 (audio environment), Brief 177 (editor), Brief 220 (LocalKey scene names)
- Mark 3D-runtime patterns deferred per Brief 156

## New inventions

- **INV-695** Twelve-family canonical `level.pattern.*` substrate vocabulary
- **INV-696** Sign-time metroidvania reachability validation across all ability sets via cached BDD-style representation
- **INV-697** `level.composition` typed gseed for multi-pattern scene overlay with explicit overlap semantics
- **INV-698** Theme/biome binding driving automatic prop/lighting/audio/particle defaults
- **INV-699** Sign-time level validation (reachability + closure + camera bounds + entity refs + asset presence) as substrate-level integrity gate

## Open follow-ups

- Specific level metrics per genre (Brief 230 cross-genre matrix)
- 3D-specific level patterns and runtime (deferred to v0.4)
- LOD streaming cost model (Brief 222 perf budget)
- Per-pattern editor tooling (Brief 177)

## Sources

1. *Level Up! The Guide to Great Video Game Design*, Scott Rogers, ch. on level design
2. *The Art of Game Design*, Jesse Schell, ch. on space
3. Clint Hocking GDC talks on level pacing and intentional play
4. Mark Brown's *Boss Keys* video series on metroidvania design
5. Spelunky procedural level design talk, Derek Yu, GDC 2016
6. Hades chamber design talk, Supergiant GDC 2020
7. Doom Eternal arena design talk, id Software GDC 2020
8. Dark Souls level interconnection retrospective, FromSoftware
9. Brief 086 (this repo) — biome library
10. Brief 153 (this repo) — ECS substrate
11. Brief 173 (this repo, next) — procgen
