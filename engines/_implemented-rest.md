# Implemented Engines (Compact Specs)

The four flagship engines (Sprite, Character, Music, FullGame) have full standalone specs in this directory. This file collects compact specs for the remaining 11 implemented engines: Geometry3D, Animation, Procedural, Narrative, UI, Physics, Visual2D, Audio, Ecosystem, Game, ALife. Each follows the canonical engine template but at reduced length. Anything that diverges from the standard template is called out explicitly.

---

## Geometry3D

**Overview.** Pure 3D mesh generation. SDF (signed distance field) modeling with marching cubes extraction. 3,084 LOC, 6 stages. Output: glTF mesh.

**Genes.** `topology` (categorical: organic|hard_surface|crystalline|plant|architectural), `field_resolution` (int 32..256), `field_complexity` (scalar [0,1]), `symmetry` (categorical: none|bilateral|radial_n|spherical), `surface_roughness` (scalar), `material_hint` (categorical), `bounding_box` (vector(3)).

**Pipeline.** `extract → field (SDF assembly) → march (marching cubes) → simplify (mesh decimation to target tri count) → uv_unwrap → export (glTF)`.

**Determinism.** SDF samples on a fixed-resolution lattice (no adaptive sampling). Marching cubes uses canonical edge indexing. Mesh vertices canonicalized to 7 decimal digits.

**Fitness hints.** `geometry`, `style`, `novelty`. MAP-Elites: `mesh_density`, `symmetry`.

**References.** Lorensen & Cline (1987), Inigo Quilez SDF articles.

---

## Animation

**Overview.** Generates animation clips for skeletal rigs. 2,891 LOC, 5 stages. Output: glTF animation file (clips, curves, sampler bindings).

**Genes.** `style` (categorical: realistic|anticipated|exaggerated|stiff|fluid), `clip_set` (array), `loop_kind` (categorical), `keyframe_density` (scalar), `easing_curves` (array<categorical>), `target_skeleton_hint` (categorical: humanoid|quadruped|...).

**Pipeline.** `extract → keyframe (generate keyframes from style) → curve (fit easing curves) → bind (bind to skeleton) → export (glTF animation channel set)`.

**Determinism.** Curves evaluated at fixed sub-step rate. Keyframe quantization to 1/120 second.

**Fitness hints.** `animation`, `coherence`, `style`. Descriptors: `motion_smoothness`, `loop_quality`.

---

## Procedural

**Overview.** Generates layered procedural content (terrain, dungeons, biomes, materials). 2,772 LOC, 7 stages. Output: a layered asset bundle (heightmap PNG + biome map + asset placement JSON).

**Genes.** `topology` (categorical: open_world|dungeon|maze|cave|island|sky_archipelago), `noise_layers` (array<struct>), `biomes` (array<categorical>), `feature_density` (scalar), `seed_anchor` (scalar — used as proc-gen master seed within the engine), `playable_size` (vector(2)).

**Pipeline.** `extract → base_field (perlin/simplex/worley) → biomes (region assignment) → erode (hydraulic + thermal erosion) → populate (POI placement) → tile (tilemap conversion) → export`.

**Determinism.** Noise functions use deterministic seed derivation; erosion runs fixed iteration count.

**Fitness hints.** `geometry`, `coherence`, `novelty`. Descriptors: `terrain_roughness`, `biome_diversity`.

---

## Narrative

**Overview.** Generates structured stories with characters, plots, scenes, and beats. 2,654 LOC, 4 stages. Output: a structured story document (JSON tree + Markdown rendering).

**Genes.** `genre` (categorical), `tone` (vector(4)), `protagonist_seed` (seed_ref to a character), `antagonist_seed` (seed_ref), `arc_template` (categorical: hero_journey|tragedy|comedy|mystery|romance|coming_of_age|three_act|five_act), `length` (scalar — words), `setting_hint` (categorical).

**Pipeline.** `extract → arc (instantiate arc template) → populate (assign characters/places to arc beats) → render (compose Markdown + JSON tree)`.

**Determinism.** Story grammar derivations are deterministic given the seeded RNG. No LLM in the engine — that's confined to Layer 6.

**Fitness hints.** `coherence`, `style`, `novelty`. Descriptors: `arc_complexity`, `character_count`.

---

## UI

**Overview.** Generates UI layouts (web/app screens). 2,512 LOC, 6 stages. Output: HTML/CSS bundle (and optionally a React component tree).

**Genes.** `screen_template` (categorical: dashboard|landing|form|gallery|reader|player|chat|map), `density` (scalar), `palette` (array<vector(3)>), `typography_pair` (categorical: serif_sans|sans_sans|mono_sans|display_pair), `motion` (categorical: none|subtle|playful), `accessibility_target` (categorical: AA|AAA), `breakpoints` (array<int>).

**Pipeline.** `extract → grid (layout grid) → component (component placement) → style (apply palette + typography) → motion (animation hooks) → export (HTML/CSS)`.

**Determinism.** DOM child ordering canonicalized. CSS rules emitted in fixed property order.

**Fitness hints.** `geometry` (layout balance), `texture` (palette), `coherence`, `style`. Descriptors: `density`, `palette_diversity`.

---

## Physics

**Overview.** Generates physics simulation parameters and (optionally) trajectories. 2,398 LOC, 5 stages. Output: simulation spec (parameters + initial conditions + recorded trajectories).

**Genes.** `world_kind` (categorical: rigid_body|soft_body|fluid|cloth|granular|verlet_rope), `gravity` (vector(3)), `materials` (array<struct>), `bodies` (array<struct>), `constraints` (array<struct>), `integration` (categorical: verlet|xpbd|implicit_euler), `step_dt` (scalar), `total_time` (scalar).

**Pipeline.** `extract → assemble (build the world) → simulate (run forward integration) → record (sample trajectories at fixed rate) → export (sim spec + trajectory log)`.

**Determinism.** Integration uses fixed dt and fixed iteration count. Verlet/XPBD use deterministic constraint ordering.

**Fitness hints.** `geometry`, `animation`, `coherence`. Descriptors: `interaction_complexity`, `energy_conservation_error`.

---

## Visual2D

**Overview.** Generates 2D images (illustrations, posters, abstract art) — distinct from sprites in that there's no rig and no animation. 2,317 LOC, 6 stages. Output: PNG / SVG.

**Genes.** `composition` (categorical: rule_of_thirds|golden_ratio|symmetric|chaotic|grid), `palette` (array<vector(3)>), `style_tag` (categorical: abstract|illustrative|geometric|surreal|minimal|maximal), `subject_seeds` (array<seed_ref>), `texture_grain` (scalar), `format` (categorical: square|portrait|landscape|wide).

**Pipeline.** `extract → layout → fill (subjects + backgrounds) → texture → render (rasterize) → export`.

**Determinism.** Same as Sprite — pixel-coordinate, OKLab color, fixed PNG encoding.

**Fitness hints.** `texture`, `coherence`, `style`, `novelty`. Descriptors: `palette_diversity`, `composition_score`.

---

## Audio

**Overview.** Generates audio (sound effects, ambiences, drones) — distinct from Music in that there's no harmonic structure or score. 2,201 LOC, 5 stages. Output: WAV.

**Genes.** `kind` (categorical: sfx|ambient|drone|impact|whoosh|ui_click|footstep|...), `length_seconds` (scalar), `spectrum` (vector(N)), `envelope` (struct), `fx_chain` (array<categorical>: filter|reverb|distortion|delay|chorus), `seed_anchor` (scalar).

**Pipeline.** `extract → synthesize (oscillator/noise generators) → envelope → fx → export (WAV)`.

**Determinism.** Fixed-point DSP throughout.

**Fitness hints.** `texture` (spectral content), `coherence`. Descriptors: `centroid_freq`, `spectral_flatness`.

---

## Ecosystem

**Overview.** Simulates an ecosystem of species over time and outputs population dynamics. 2,089 LOC, 6 stages. Output: state log (time series of species populations + interaction graph).

**Genes.** `species` (array<struct>: name, role (producer|herbivore|carnivore|scavenger|decomposer), traits), `interactions` (graph), `initial_populations` (vector), `simulation_steps` (int), `random_events` (array<struct>).

**Pipeline.** `extract → assemble → step (Lotka-Volterra-like update) × N → record → export`.

**Determinism.** Update rules deterministic; random events seeded.

**Fitness hints.** `coherence`, `novelty`. Descriptors: `species_count`, `extinction_rate`.

---

## Game

**Overview.** Generates *abstract* game mechanics (rule sets, win conditions, scoring) without producing a playable bundle. Useful as input to FullGame or as standalone design artifact. 1,976 LOC, 5 stages. Output: structured mechanic spec.

**Genes.** `mechanic_kind` (categorical), `objects` (array<struct>), `rules` (array<expression>), `win_condition` (expression), `scoring` (expression), `min_players` (int), `max_players` (int).

**Pipeline.** `extract → grammar (parse expressions) → balance (rule consistency check) → render (formatted spec) → export`.

**Determinism.** Pure expression evaluation; no random.

**Fitness hints.** `coherence`, `novelty`. Descriptors: `rule_count`, `decision_branching_factor`.

---

## ALife

**Overview.** Open-ended artificial life simulation. Generates initial state and rules; the resulting simulation evolves indefinitely. 1,803 LOC, 6 stages. Output: initial state + rule definitions + (optional) recorded snapshot of N steps.

**Genes.** `world_kind` (categorical: cellular_automaton|particle_world|grid_creatures|continuous_2d), `rules` (array<expression>), `initial_state` (struct), `step_count` (int), `recording_interval` (int).

**Pipeline.** `extract → assemble → step × N → snapshot → record → export`.

**Determinism.** Initial state and rules are exact; long simulations are deterministic on conformant hardware but accumulate floating-point error after many millions of steps. Documented as such in [`spec/07-determinism.md`](../spec/07-determinism.md).

**Fitness hints.** `novelty`, `coherence`. Descriptors: `entropy_growth_rate`, `pattern_complexity`.

---

For the 11 planned engines (Shader, Particle, Typography, Architecture, Vehicle, Furniture, Fashion, Robotics, Circuit, Food, Choreography), see [`engines/_planned.md`](_planned.md).
