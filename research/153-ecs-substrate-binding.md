# 153 — Entity-component-system (ECS) substrate binding

## Question

How does GSPL bind the entity-component-system pattern — the dominant runtime data model for modern games — to the substrate such that entities are signed gseeds, components are typed, spawn/destroy is lineage-tracked, and any tick can be rolled back to any prior entity state?

## Why it matters (blast radius)

ECS is the de-facto runtime model for every non-trivial game engine: Unity DOTS, Unreal Mass, Bevy, flecs, EnTT, DefaultEcs. If GSPL ships a parallel "objects" model instead of binding ECS into the substrate, creators will either (a) reject GSPL because it doesn't match their mental model, or (b) build an ECS on top of GSPL and lose all seven structural axes inside the ECS boundary. Brief 153 must make ECS *native* so entities inherit Signed, Typed, Lineage, Graph, Confidence, Rollback-able, and Differentiable for free.

## What we know from the spec

- Brief 152 establishes the tick scheduler as the substrate on which ECS runs.
- Brief 131 establishes the seven-axis structural claim; ECS must inherit all seven.
- Round 2 Brief 024 defines lineage entry schema.
- Round 4 Brief 091 defines the federated knowledge graph; ECS data must be queryable against it.
- Brief 149 freezes v0.1; the creator surface is 2D-first, so ECS must handle sprite/character/particle entity types at v0.1 and defer 3D-heavy patterns to v0.3+.

## Findings

1. **Entity = signed typed gseed with a stable handle.** An entity is a gseed in the `ecs.entity` namespace carrying `(entity_id, archetype, component_set, parent, tick_created, signature)`. The `entity_id` is a 128-bit ULID signed at spawn; it never changes over the entity's lifetime. Component sets mutate; identity does not.

2. **Component = typed gseed in a per-component namespace.** Each component type lives in `ecs.component.<type>`. Example types shipped at v0.1: `transform`, `sprite`, `velocity`, `collider.2d`, `health`, `inventory`, `actor`, `input`, `ai.state`, `animator`, `particle.emitter`, `audio.source`, `script`. Adding a component to an entity emits a signed `ecs.component.attach` gseed carrying `(entity_id, component_type, component_data, tick_number)`.

3. **Archetype = signed set-of-component-types, not a class.** Archetypes are computed from the current component set; entities migrate between archetypes when components attach/detach. This matches the Bevy/flecs/DOTS archetype model, which is the performance-winning pattern for cache-friendly iteration. Archetypes themselves are signed gseeds in `ecs.archetype` so the schema of any entity is queryable and replayable.

4. **Spawn and destroy are lineage events.** `ecs.entity.spawn` and `ecs.entity.destroy` are signed gseeds with parent lineage to whatever scene, system, or composition rule caused them. Creators can answer "why does this entity exist?" by traversing the lineage graph to the originating signed cause (a script, a spawn rule, a save file, a network message).

5. **Systems = signed functions over archetype queries.** A system is a signed gseed in `ecs.system` declaring `(name, query, phase, read_set, write_set, priority)`. The query is the set of component types the system operates on; the read/write sets feed Brief 152's topological sort. Systems compose via query intersection; two systems reading the same components can run in parallel if their write sets are disjoint.

6. **Per-tick entity state is a diff, not a snapshot.** Storing a full world snapshot every tick at 60 Hz is prohibitive. Instead, the substrate records per-tick component mutations as signed diff gseeds (`ecs.tick.diff`). A full snapshot is taken every 600 ticks (10 seconds at 60 Hz) as a signed checkpoint; rollback to any tick is checkpoint + replay of intermediate diffs. This matches GGPO rollback and is the structural reason Brief 131's Rollback-able axis extends to every entity in every game.

7. **Hierarchies are first-class but shallow.** Parent-child relationships are a `transform.parent` component, not a separate scene-graph structure. Max depth default is 16; beyond that, the scene-compile emits a warning (not an error) because most creator patterns stay under depth 8. This mirrors Unity's prefab/hierarchy model but keeps everything in the flat ECS store.

8. **Prefabs = signed composition recipes over archetypes.** A prefab is a signed gseed in `ecs.prefab` carrying `(name, archetype, component_defaults, lineage)`. Spawning from a prefab is a one-call operation that creates a new entity with the prefab's archetype and default component values, signed as a child of the prefab gseed. Prefab updates propagate to instances via lineage replay (opt-in per-instance).

9. **Queries are declarative and cached.** `ecs.query` is a typed gseed like `With<transform, velocity>, Without<static>`. The scheduler caches query results per-tick and invalidates them only on archetype migrations. This matches Bevy's query caching and keeps the iteration cost at O(matching_entities) rather than O(total_entities).

10. **Component data is in a dense per-archetype store.** Memory layout matches the DOTS/Bevy/flecs consensus: struct-of-arrays per archetype, cache-friendly iteration, zero-cost for entities that don't have a given component. v0.1 ships with 32-byte alignment on all component types to match SIMD for future optimization.

11. **Signature verification is lazy for hot-path components.** Signing every component mutation on every tick at 60 Hz would crush the frame budget. Instead, signatures are *batched per-tick*: the full set of component mutations for tick N is Merkle-hashed into a single signed `ecs.tick.root` gseed. Individual mutations carry Merkle paths; a creator auditing a specific mutation verifies against the tick root. This reduces signing cost from per-mutation to per-tick (typical: 1 signature per tick, not 10,000).

12. **The scene is an ECS world; the world is a scene.** Not two concepts. A scene gseed *is* an ECS world snapshot at a given tick; saving a scene is snapshotting the world; loading a scene is instantiating the world from the snapshot. This collapses Unity's Scene vs GameObject duality into one signed primitive.

13. **v0.1 reach.** At v0.1 the ECS substrate supports ~10,000 entities per scene at 60 Hz on the hardware floor (Brief 135) with the v0.1 component set (~20 component types). v0.4 (3D-default) raises this to ~100,000 via archetype-aware SIMD iteration. Federation-wide federation of ECS worlds (e.g., shared persistent worlds) is Tier F territory (Briefs 209-212).

14. **Differentiable ECS — seventh-axis binding.** Component mutations from accepted creator workflows can be collected as training signal for the action LoRA (Brief 143). A signed mutation with an accepted-outcome parent lineage becomes a positive training example; a mutation with a rolled-back lineage becomes negative. ECS operations are thus *the* primary source of Brief 131's Differentiable axis at the action-space layer.

## Risks identified

- **Per-tick diff storage may exceed the memory budget for long sessions.** Mitigation: diffs older than 600 ticks (1 checkpoint-cycle) are compacted into the checkpoint and dropped; memory ceiling is `checkpoint_size × 2 + 600 × avg_diff_size`, bounded and predictable.
- **Merkle signature batching delays detection of corrupt mutations by one tick.** Mitigation: acceptable — the drift detector (Brief 144) runs on tick boundaries anyway.
- **Archetype migrations are O(entity_size) copies; pathological churn (add/remove component every tick) can dominate frame time.** Mitigation: emit `ecs.archetype.churn` gseed when migration rate per entity exceeds 1/sec; surface in the debugger (Brief 217) so creators can refactor to state machines.
- **Prefab lineage updates can cascade across thousands of instances.** Mitigation: cascading updates are opt-in, not default; creators choose per-prefab whether updates propagate.
- **ECS-vs-OO mental model mismatch for beginners.** Mitigation: the authoring surfaces (Tier C) hide archetype concepts behind friendly "entity + components" framing; power users can drop down to raw archetype views.

## Recommendation

**GSPL ships a native ECS substrate at v0.1 in the `ecs` namespace with signed entities, typed per-component-type namespaces, archetype-based storage, query-driven systems with topologically-sorted phases (from Brief 152), signed per-tick Merkle-batched mutation roots, diff+checkpoint rollback (600-tick checkpoint cadence), prefab composition as signed recipes, and ~10,000-entity-per-scene capacity on the v0.1 hardware floor. The scene *is* the ECS world. Every subsequent Tier A brief (154-163) declares its components and systems against this substrate.**

## Confidence

**4/5.** The design is the consensus pattern from Bevy, flecs, EnTT, DOTS, and Mass Entity with the seven-axis discipline layered on top; no speculative elements. The 5th point is withheld until the Tier A benchmark family (Brief 134 extension) validates the 10,000-entity target on the v0.1 hardware floor.

## Spec impact

- `gspl-reference/namespaces/ecs.md` — new namespace: `ecs.entity`, `ecs.component.*`, `ecs.archetype`, `ecs.system`, `ecs.prefab`, `ecs.query`, `ecs.tick.diff`, `ecs.tick.root`
- `gspl-reference/research/152-game-loop-tick-model-namespace.md` — cross-reference; ECS systems declare phases via Brief 152's topological sort
- `gspl-reference/research/143-differentiable-action-learning-recipe.md` — cross-reference; ECS mutations are a primary Differentiable-axis signal source
- `gspl-reference/research/158-save-load-and-serialization.md` (to be written) — inherits the diff+checkpoint mechanism
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — add ECS battery test family (10k entities, archetype churn, query cache correctness, diff+checkpoint rollback)

## New inventions

- **INV-599** — *Merkle-batched per-tick signature root for ECS* — one signature per tick instead of one per mutation, with verifiable per-mutation Merkle paths, making signed ECS at 60 Hz within the v0.1 frame budget.
- **INV-600** — *Diff+checkpoint rollback for game ECS* at a 600-tick (10s) checkpoint cadence, bounding memory while giving frame-exact rollback to any tick.
- **INV-601** — *Scene-as-ECS-world collapse* — one signed primitive rather than Unity's two-layer Scene+GameObject model, simplifying the mental model and making save/load trivially consistent.
- **INV-602** — *Prefab lineage replay* — prefab updates propagate to instances via signed lineage replay rather than shared state, giving creators explicit control over cascade vs isolation.
- **INV-603** — *ECS mutation lineage as Differentiable-axis training signal* — accepted-outcome mutations become InfoNCE positives, rolled-back mutations become negatives, turning ordinary gameplay into LoRA training data per Brief 143.

## Open follow-ups

- Whether v0.1 ships a visual ECS debugger (defer to Tier G Brief 217 in-Studio debugger).
- Whether federation-shared ECS worlds need a distinct consistency model beyond Brief 100 federation peer protocol (defer to Tier F Brief 212 persistent world hooks).
- Whether component inheritance/traits are needed or flat composition suffices (current answer: flat composition only, matching Bevy/flecs; revisit in Round 8 if creator feedback demands traits).

## Sources

- Brief 131 — seven-axis structural claim
- Brief 143 — differentiable action learning recipe
- Brief 149 — v0.1 scope finalization
- Brief 152 — game loop and tick model namespace
- Round 2 Brief 024 — lineage entry schema
- Round 4 Brief 091 — federated knowledge graph
- Bevy ECS documentation (archetype model, query caching)
- flecs ECS documentation (archetype iteration, query DSL)
- Unity DOTS/Mass Entity documentation
- EnTT documentation
- GGPO rollback netcode (diff+checkpoint pattern reference)
