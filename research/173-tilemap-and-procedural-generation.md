# 173 — Tilemap and procedural generation

## Question

What canonical tilemap and procedural generation primitives does GSPL ship in `tilemap.*` and `procgen.*` so that any genre can adopt 47-tile autotile bitmasks, Wave Function Collapse, BSP, drunkard's walk, cellular automata, Perlin/Simplex noise, Wang tiles, herringbone, dungeon graphs, and biome generation by composition rather than from scratch, with deterministic seeds, signed outputs, and v0.1 reach?

## Why it matters (blast radius)

Procedural generation is the multiplier that turns a small content pool into thousands of hours of unique experiences (Spelunky, Dead Cells, Hades, Minecraft, Noita, Dwarf Fortress). Without typed procgen primitives, every game reinvents WFC, autotiling, dungeon layout, and noise sampling, breaking deterministic replay, cross-game seed sharing, and the substrate's promise that *the same input always produces the same output*. Brief 172 (level patterns) is the consumer of procgen output, Brief 178 (tilemap editor) is the authoring surface, Brief 197-208 (genre families) compose procgen recipes, and Brief 227 (replay/roguelike) depends on seed determinism for daily challenges and shareable runs.

## What we know from the spec

- Brief 153 — ECS substrate; tilemaps are typed components
- Brief 156/157 — physics/collision; tile collision shapes are derived from tilemaps
- Brief 160 — sub-seeded PRNG; procgen consumes it for all randomness
- Brief 172 — level patterns; the primary consumer of procgen output
- Brief 020 — determinism contract; procgen must be bit-for-bit reproducible

## Findings

1. **`tilemap.layer` as the root tilemap primitive.** A tilemap layer is a typed signed gseed: `layer_id`, `dims: (u16, u16)`, `tile_size: (u16, u16)`, `tile_palette_ref: tileset_ref`, `cells: dense_or_sparse_grid<TileId>`, `collision_mode: enum{none, per_tile, merged_polygon}`, `auto_tile_rule_ref: optional<rule_ref>`, `parallax: f32 ∈ [0.0, 4.0]`, `z_order: i16`, `signing_authority`. Multiple layers per scene; each independently editable and serializable.

2. **Tile palette and tile gseeds.** A `tilemap.tileset` is a typed gseed referencing an atlas image, with per-tile metadata: `tile_id`, `atlas_uv`, `tags: set<TagId>`, `collision_shape_ref`, `friction: f32`, `surface_type: SurfaceTypeId`, `audio_footstep_ref`, `vfx_on_step_ref`, `damage_on_contact: optional<damage_ref>`. Tiles are signed; tile mutations during gameplay are signed events.

3. **Autotile rules: 47-tile and 16-tile bitmasks.** The substrate ships **two canonical autotile rule sets**: the 16-tile (4-bit edge) bitmask used for simple terrain, and the 47-tile (8-bit corner-aware) bitmask used for full Tiled/RPG-Maker compatibility. Each is a typed `tilemap.autotile_rule` gseed mapping neighborhood bitmask → tile id. The substrate also supports custom rule sets for arbitrary Wang tile counts (2, 4, 8, 47, 256). Editor (Brief 178) ships pre-baked rule presets.

4. **`tilemap.collision`.** Tilemap collision is generated at sign time per the layer's `collision_mode`: `none` (decorative only), `per_tile` (every solid tile gets its tile collision shape), `merged_polygon` (run-length-merged into convex polygons for physics performance — uses a deterministic merging algorithm). Merged mode is the default for v0.1 to keep collider counts under Brief 156's per-scene physics body cap.

5. **Eight canonical procgen algorithms.** Surveying Spelunky, Dead Cells, Hades, Minecraft, Dwarf Fortress, Noita, Caves of Qud, Brogue, Diablo, and academic literature (Shaker et al., *Procedural Content Generation in Games*) yields **8 canonical procgen primitives**: `procgen.wfc` (Wave Function Collapse), `procgen.bsp` (binary space partition), `procgen.drunkards_walk`, `procgen.cellular_automata`, `procgen.perlin_noise`, `procgen.simplex_noise`, `procgen.wang_tiles`, `procgen.dungeon_graph`. Plus three composition primitives: `procgen.layered`, `procgen.constraint_solver`, `procgen.template_stitch`.

6. **`procgen.wfc`.** Wave Function Collapse. Parameters: `input_pattern: tilemap_ref` (the example to learn from), `output_dims`, `pattern_size: u8 ∈ [1, 5]`, `periodic: bool`, `symmetries: set<symmetry_id>`, `weights: optional<map<tile_id, f32>>`, `backtrack_limit: u32`, `seed: u64`. Substrate uses Maxim Gumin's reference algorithm (canonical implementation) for determinism. Output is a `tilemap.layer` gseed signed with the seed and input as lineage.

7. **`procgen.bsp`.** Binary space partition. Parameters: `area: aabb`, `min_room_size: (u16, u16)`, `max_room_size: (u16, u16)`, `split_ratio_range: range<f32>`, `corridor_width: u8`, `room_density: f32 ∈ [0.0, 1.0]`, `seed`. Output is a `procgen.dungeon_graph` of rooms and corridors. Used by classic roguelikes.

8. **`procgen.drunkards_walk`.** Random walk cave generation. Parameters: `start: (u16, u16)`, `steps: u32`, `direction_bias: vector_2d`, `multiple_walkers: u8`, `wall_thickness: u8`, `seed`. Used for organic caves (Brogue, dwarf-fortress style).

9. **`procgen.cellular_automata`.** CA generation. Parameters: `dims`, `initial_density: f32`, `birth_rule: set<u8>`, `survive_rule: set<u8>`, `iterations: u8`, `wrap_edges: bool`, `seed`. Game-of-Life style; canonical for cave systems.

10. **`procgen.perlin_noise` / `procgen.simplex_noise`.** Continuous noise. Parameters: `dims`, `octaves: u8`, `persistence: f32`, `lacunarity: f32`, `frequency: f32`, `amplitude: f32`, `seed`, `quantize_to: enum{f32, u8, tile_threshold_palette}`. Substrate uses Ken Perlin's reference Perlin and Stefan Gustavson's reference Simplex implementations for determinism. Used for terrain heightmaps (Minecraft), biome distribution, weather.

11. **`procgen.wang_tiles`.** Edge-color-matched tile sets. Parameters: `wang_set: wang_set_ref`, `dims`, `seed`. Used for non-repeating textures (terrain, road systems, dungeon corridors). The substrate ships 2-color, 4-color, and 8-color reference Wang tile sets.

12. **`procgen.dungeon_graph`.** A typed graph of chambers (Brief 172.dungeon_chamber) and corridors. Parameters: `chambers: set<chamber_ref>`, `connections: set<edge>`, `entry_chamber`, `exit_chamber`, `min_path_length`, `max_branching_factor`, `seed`. Output of BSP, Spelunky-style room stitching, or hand-built. Consumed by Brief 172 dungeon scenes.

13. **`procgen.layered`.** Composition primitive: layer multiple procgen passes with deterministic ordering. Parameters: `layers: ordered_set<(generator_ref, blend_mode)>`. Example: Minecraft = simplex(terrain) + cellular(caves) + simplex(biomes) + wfc(structures). Substrate guarantees layer composition is deterministic regardless of execution thread.

14. **`procgen.constraint_solver`.** Generic constraint generation. Parameters: `variables`, `domains`, `constraints`, `seed`, `solver_kind: enum{backtrack, AC3, sat, smt}`. Used for puzzles (Brief 172.puzzle_grid solvability), shop layouts, and quest objective placement. Substrate ships with a backtracking solver at v0.1; SAT/SMT solvers gated to v0.4.

15. **`procgen.template_stitch`.** Spelunky-style: hand-built room templates stitched into a grid. Parameters: `template_set: set<template_ref>`, `grid_dims`, `compatibility_rules`, `seed`. The most controllable procgen approach — used when designers want guarantees about room quality.

16. **Determinism guarantees.** Every procgen algorithm uses sub-seeded PRNGs from Brief 160 keyed on `(scene_seed, generator_id, layer_index)`. All arithmetic is in fixed-point (Brief 020) where possible; floating-point Perlin/Simplex use the canonical reference implementations whose IEEE 754 behavior is bit-stable across the engines GSPL targets. Two creators with the same seed get identical output.

17. **Seed sharing primitive.** A `procgen.seed_record` typed gseed captures `(seed, generator_chain, parameters)` so a player can copy/paste a seed string and another player gets the exact same generation. This is the substrate-level *daily challenge* and *Spelunky seed share* primitive.

18. **Signed lineage.** Every procgen output gseed (a tilemap, a dungeon graph, a heightmap) records the generators and parameters as lineage. A creator can fork a generated map, hand-edit a portion, and the substrate tracks both the procedural lineage and the manual edits.

19. **v0.1 reach.** Tilemap layer + tileset + 47-tile + 16-tile autotile + per-tile and merged collision: all ship at v0.1. Procgen primitives at v0.1: WFC (full), BSP (full), drunkard's walk (full), CA (full), Perlin (full), Simplex (full), Wang tiles (2/4/8 color), dungeon graph (full), layered composition (full), template stitch (full). Constraint solver: backtracking ships, SAT/SMT defer to v0.4. 3D voxel/marching cubes generation defers to v0.4.

## Risks identified

1. **WFC backtracking can fail.** Hard inputs may exceed the backtrack limit. Mitigation: substrate provides a fallback to template stitch if WFC fails after limit; warning logged.

2. **Floating-point determinism in Perlin/Simplex.** Different SIMD/FMA paths can produce different results. Mitigation: substrate ships scalar reference implementations only at v0.1; SIMD acceleration gated behind a determinism re-validation in Brief 020's harness.

3. **Procgen + multiplayer.** Two clients must generate identical output. Mitigation: server-authoritative seed sharing in v0.3+; client just receives the seed and regenerates.

4. **Procgen output that's unfair.** A procgen dungeon with no key, no exit, or impossible jumps. Mitigation: every procgen output goes through Brief 172's reachability validation before being accepted; failed outputs are regenerated with the next sub-seed.

5. **Seed format collision across versions.** Generator parameters change between substrate versions, breaking old seeds. Mitigation: seed records carry a substrate version tag; old seeds replay against the version they were generated under via Brief 158's schema-versioned migration.

6. **Performance.** WFC on a large grid is expensive. Mitigation: per-scene generation budget from Brief 222 perf budget brief; chunked generation with explicit yield points to the tick scheduler.

## Recommendation

Ship `tilemap.*` with layer + tileset + 47/16-tile autotile + collision-merging at v0.1. Ship `procgen.*` with the 8 generation primitives + 3 composition primitives + seed record + lineage tracking. Wire to Brief 172 level patterns at v0.1 with reachability validation as the acceptance gate. Defer SAT/SMT solvers and 3D voxel generation to v0.4. Default to scalar reference implementations for floating-point noise to guarantee determinism.

## Confidence

**4.5/5.** Procgen primitives are well-grounded in 50+ years of academic and industry work — Maxim Gumin's WFC, Ken Perlin's noise, Brogue/Spelunky/Dead Cells postmortems, and the *PCG in Games* textbook converge tightly. Held back from 5 by SIMD-determinism concerns which need empirical validation in Round 8.

## Spec impact

- Add `tilemap.*` namespace with `layer`, `tileset`, `autotile_rule` sub-types
- Add `procgen.*` namespace with 8 algorithm primitives + 3 composition primitives + `seed_record`
- Add canonical 47-tile and 16-tile autotile reference rule sets
- Specify scalar reference implementations for Perlin/Simplex; gate SIMD per Brief 020
- Cross-link to Brief 020 (determinism contract), Brief 153 (ECS storage), Brief 156/157 (collision derivation), Brief 160 (sub-seeded PRNG), Brief 172 (level pattern consumer), Brief 178 (tilemap editor), Brief 220 (tile name LocalKeys), Brief 222 (perf budget), Brief 227 (seed sharing for daily challenges)
- Mark SAT/SMT constraint solvers and 3D voxel generation deferred to v0.4

## New inventions

- **INV-700** Eight-primitive canonical `procgen.*` substrate vocabulary plus three composition primitives
- **INV-701** Canonical 47-tile and 16-tile autotile rule sets as substrate-shipped signed gseeds
- **INV-702** `procgen.seed_record` typed gseed for shareable daily-challenge / Spelunky-style seed strings with version tagging
- **INV-703** Procgen lineage tracking enabling fork-and-hand-edit on generated content with both procedural and manual provenance preserved
- **INV-704** Substrate-default acceptance gate: every procgen output passes Brief 172 reachability validation or is regenerated

## Open follow-ups

- SIMD Perlin/Simplex re-validation against scalar reference (Round 8)
- 3D voxel and marching-cubes generation (deferred to v0.4)
- Procgen-aware editor preview with stable chunk visualization (Brief 178)
- Specific recommended generators per genre (Brief 230 cross-genre matrix)

## Sources

1. Maxim Gumin, *Wave Function Collapse* reference repository and paper, 2016
2. Ken Perlin, *Improving Noise* paper, SIGGRAPH 2002
3. Stefan Gustavson, simplex noise reference implementation
4. Spelunky procedural design talk, Derek Yu, GDC 2016
5. Dead Cells procgen architecture talk, Motion Twin GDC 2018
6. Brogue dungeon generation retrospective, Brian Walker
7. *Procedural Content Generation in Games*, Shaker, Togelius, Nelson, 2016 (Springer textbook)
8. Minecraft world generation talks, Mojang
9. Dwarf Fortress world gen retrospective, Bay 12 Games
10. Tiled and Godot autotile bitmask reference documentation
11. Brief 020 (this repo) — determinism contract
12. Brief 160 (this repo) — sub-seeded PRNG
13. Brief 172 (this repo) — level patterns consuming procgen output
