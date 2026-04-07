# Planned Engines (Compact Specs)

The 11 engines listed here are not yet implemented. Each entry gives the canonical name, output type, anticipated gene schema highlights, anticipated pipeline shape, and any notable references. They follow the same `DomainEngine` pattern as the implemented engines and slot in alongside them via the engine registry.

The build order for these is documented in [`roadmap/build-order.md`](../roadmap/build-order.md).

---

## Shader

**Output.** WGSL/GLSL source plus a parameter manifest. **Genes.** `kind` (categorical: surface|post|compute), `inputs` (array<struct>), `outputs` (array<struct>), `body_template` (categorical), `params` (vector). **Pipeline.** `extract → ast → typecheck → emit (WGSL) → emit (GLSL) → export`. **References.** WGSL spec, glslangValidator. Used as a sub-component by Visual2D and Geometry3D engines.

## Particle

**Output.** Particle system spec (emitter parameters, force fields, ranges, color gradients). **Genes.** `emitter_shape`, `rate`, `lifetime`, `velocity_curve`, `color_gradient`, `forces` (array). **Pipeline.** `extract → emitter → forces → render (preview frames) → export`. **References.** Niagara/VFX Graph design patterns.

## Typography

**Output.** Font (TTF/OTF) plus per-glyph metadata. **Genes.** `glyph_template`, `weight`, `slant`, `serif_kind`, `proportions`. **Pipeline.** `extract → glyph_morph → metric_layout → kern → export (TTF)`. **References.** OpenType spec, MetaFont.

## Architecture

**Output.** Building/room glTF (interior + exterior). **Genes.** `building_kind` (categorical: house|temple|tower|warehouse|cabin), `style` (categorical: gothic|modernist|art_deco|brutalist|...), `room_graph`, `material_palette`, `footprint`. **Pipeline.** `extract → footprint → walls → openings → roof → materials → export`. **References.** Wonderdraft, CityEngine procedural rules.

## Vehicle

**Output.** Vehicle glTF + dynamics parameters. **Genes.** `vehicle_kind` (categorical: car|truck|aircraft|boat|spacecraft|hover), `chassis_morph`, `engine_class`, `wheel_count`, `aerodynamics`. **Pipeline.** `extract → chassis → drivetrain → bodywork → texture → dynamics_params → export`.

## Furniture

**Output.** Parametric furniture model (chair, table, shelf). **Genes.** `furniture_kind`, `dimensions`, `material`, `joint_kind`, `style`. **Pipeline.** `extract → frame → surfaces → joinery → finish → export`. **References.** Sketchup parametric components.

## Fashion

**Output.** Garment mesh + texture (compatible with Character engine output). **Genes.** `garment_kind` (shirt|pants|dress|jacket|...), `silhouette`, `fabric`, `pattern`, `target_body_morph`. **Pipeline.** `extract → pattern → drape → seam → texture → export`. **References.** Marvelous Designer cloth simulation, CLO 3D.

## Robotics

**Output.** URDF (robot model) + control policy stub. **Genes.** `robot_kind` (arm|biped|wheeled|drone|quadruped), `joint_count`, `link_lengths`, `actuators`, `sensors`. **Pipeline.** `extract → links → joints → sensors → control_template → export (URDF)`. **References.** ROS URDF spec, MuJoCo.

## Circuit

**Output.** KiCad schematic + PCB layout. **Genes.** `circuit_kind` (analog|digital|mixed), `node_graph`, `component_palette`, `pcb_size`. **Pipeline.** `extract → netlist → place → route → drc → export (KiCad files)`. **References.** KiCad schematic format, FreeRouting.

## Food

**Output.** Recipe (ingredients + steps + nutrition) + a procedurally generated visual. **Genes.** `cuisine`, `dietary_constraints`, `ingredient_palette`, `complexity`, `course`. **Pipeline.** `extract → ingredients → steps → nutrition_calc → render_image → export`. **References.** USDA FoodData Central.

## Choreography

**Output.** Motion sequence compatible with the Animation engine. **Genes.** `dance_style`, `tempo` (or `music_seed_ref`), `steps_count`, `formation`. **Pipeline.** `extract → phrase → motion → sync_to_music → export (motion clip)`.

---

Each of these engines, once implemented, will get a full spec file replacing this entry. The compact form here is the canonical pre-implementation contract — it pins the gene schema and pipeline shape so that downstream tooling (functor bridges, intelligence layer templates, marketplace categories) can be designed in parallel with the engine itself.
