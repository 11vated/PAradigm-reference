# 156 — Physics integration: 2D and 3D

## Question

How does GSPL equip 2D and 3D physics — Box2D-class and Bullet-class typed wrappers, deterministic mode, collision tagging, constraint primitives — as a substrate namespace where physics state is signed per fixed tick and rollback-able to any prior tick?

## Why it matters (blast radius)

Physics is the largest source of non-determinism in game engines (floating-point order-of-operations differences, accumulated error, incremental solver state). Without a determinism contract at the physics layer, every multiplayer game, every replay, every save/load loses correctness. Physics is also the largest blocker to multi-engine export — Box2D, Chipmunk, Rapier, Bullet, PhysX, Havok all produce different results for the same input. Brief 156 must specify a substrate physics interface that is *engine-portable* and *deterministic-in-substrate-mode* even when underlying engines aren't.

## What we know from the spec

- Brief 152 — fixed tick at 60 Hz default; physics runs on the fixed tick.
- Brief 153 — ECS components: `transform`, `velocity`, `collider.2d`, plus `collider.3d`, `rigidbody.2d`, `rigidbody.3d`.
- Brief 131 — seven-axis claim; physics state must be signed and rollback-able.
- Brief 149 — v0.1 ships 2D physics first-class; 3D physics ships substrate hooks but only Godot/Unreal exports get full 3D until v0.4.
- Round 2 Brief 026 — deterministic kernel implementation; physics inherits the constraint.

## Findings

1. **Two physics substrates ship: `physics.2d` and `physics.3d`, with a shared abstract interface.** Both expose: bodies, colliders, joints, queries, contact events, simulation step. Bodies live in the ECS as components; the physics namespace owns the simulation. The abstract interface is the substrate's portable surface; underlying solvers are pluggable.

2. **Default 2D solver: Rapier 2D, with Box2D as alternate.** Rapier (Rust) is deterministic by construction across machines if `f32` mode is enforced and the same compile flags ship to every target. Box2D is the more familiar fallback for creators who explicitly want Box2D semantics. Selection is a signed scene-level `physics.2d.solver` gseed.

3. **Default 3D solver: Rapier 3D, with PhysX 5 as engine-export alternate.** Rapier 3D for substrate-determinism mode; PhysX for Unity/Unreal-export when the creator opts out of substrate determinism for performance. The substrate ships Rapier 3D as the canonical reference.

4. **Determinism mode is signed per scene.** A scene's `physics.determinism` gseed has one of three values: `strict` (Rapier f32 with fixed step, no engine-export hand-off; identical results across all platforms), `engine_native` (uses target engine's solver, may diverge), `none` (faster, no determinism guarantees; for prototyping only). Strict mode is required for multiplayer and replay; default for v0.1 demo projects is `strict`.

5. **Collider primitives.** v0.1 ships: `box`, `circle`, `capsule`, `polygon` (convex, ≤8 vertices), `compound` (set of primitives), `tilemap` (auto-generated from tilemap data) for 2D; `box`, `sphere`, `capsule`, `convex_hull` (≤32 vertices), `compound`, `heightfield`, `mesh` (concave; static only) for 3D. Each is a signed gseed in `physics.collider.*`.

6. **Bodies have three types: `static`, `kinematic`, `dynamic`.** Static bodies never move (terrain, walls). Kinematic bodies move under script control and push dynamic bodies but ignore forces (player characters, platforms, doors). Dynamic bodies obey forces and collisions (props, enemies, projectiles). This is the consensus across Box2D, Rapier, PhysX, Bullet.

7. **Collision layers and masks are typed bitfields with named layers.** A scene declares up to 32 named layers (`world`, `player`, `enemy`, `projectile`, `pickup`, `trigger`, `decoration`, ...). Each collider has a `layer` (one) and a `mask` (set of layers it collides with). Names are creator-defined per scene; defaults ship for the v0.1 6 starter genre templates (Brief 197-208).

8. **Joints and constraints.** v0.1 ships: `pin` (revolute), `slider` (prismatic), `distance`, `weld`, `motor` (active force), `spring` for 2D; same six plus `cone_twist`, `6dof` for 3D. Each is a signed `physics.joint.*` gseed. Joints reference body entity IDs from the ECS.

9. **Contact events are signed and queryable.** When two colliders touch, the physics step emits a `physics.contact.begin`, `physics.contact.stay` (each tick of contact), and `physics.contact.end` gseed. Each carries `(entity_a, entity_b, normal, point, impulse)`. ECS systems can subscribe via `physics.query.contacts`. This is the structural way creators wire up "did the player touch the spike?" without per-game tag soup.

10. **Queries: raycast, shapecast, overlap.** All return signed result gseeds. Queries run synchronously on the fixed tick; results are bit-identical across replays in strict mode. v0.1 supports broadphase + narrowphase queries for both 2D and 3D.

11. **Per-tick physics state is signed via the same Merkle batching as ECS (Brief 153 finding 11).** Body transforms, velocities, joint states, and contact set are hashed into a `physics.tick.root` signed gseed. Rollback to any tick uses ECS rollback (Brief 153 finding 6) plus a physics-specific solver-state restore (the small bit of internal solver state Rapier exposes for warm-starting).

12. **Substrate-deterministic mode disables platform-specific FP optimizations.** No fast-math, no FMA, no SSE4.1+ specialization without uniform compile flag. The Rapier authors explicitly support this mode. Cost: ~20% slower than native solver, validated against the Rapier benchmark suite. Acceptable for v0.1's hardware floor (Brief 135) at typical entity counts.

13. **Contact tagging via lineage, not strings.** Brief 157 (collision and trigger primitives) details this; the gist is that contact handlers don't grep for tag strings; they query the ECS for components on the contact entities, and lineage-track the contact to the systems that responded.

14. **3D physics ships substrate but is gated at the export pipeline.** The `physics.3d` namespace exists at v0.1 with full Rapier 3D backing, but the export pipeline (Tier D) only reaches it via Godot 3D, Unity 3D, and Unreal at v0.1. Phaser/GameMaker/HTML5 2D-only exports refuse `physics.3d` components at compile-time. v0.4 expands 3D-default exports.

## Risks identified

- **Rapier f32 strict mode is ~20% slower than native.** Mitigation: 20% headroom on the v0.1 hardware floor (Brief 135) is enough for the 2D-first scope; 3D strict-mode for low entity counts only.
- **Cross-engine physics export will produce *visually different* simulations even from identical signed inputs if creators export with `engine_native`.** Mitigation: the export pipeline (Brief 188-196) emits a signed warning when a scene uses `engine_native` and the target engine differs from the substrate solver; creators must explicitly accept the divergence.
- **Tilemap auto-collision can fail for custom tile shapes.** Mitigation: ship a per-tile collider override (`physics.tilemap.tile_override`); creators can hand-author edge cases.
- **Joint stability is solver-dependent and can drift over long sessions.** Mitigation: signed `physics.joint.divergence` gseed when joint position error exceeds threshold; surfaces in the debugger.
- **Mesh colliders for concave 3D geometry are static-only at v0.1.** Mitigation: explicit and documented; dynamic concave is a v0.4 expansion via convex decomposition.

## Recommendation

**GSPL ships `physics.2d` and `physics.3d` namespaces at v0.1 with Rapier 2D / Rapier 3D as the canonical determinism-strict solvers, Box2D and PhysX as engine-export alternates, three body types (static/kinematic/dynamic), six 2D collider primitives + seven 3D, six joint types per dimension (plus two 3D-only), 32 named collision layers per scene, signed contact events with begin/stay/end, signed raycast/shapecast/overlap queries, per-tick Merkle-batched physics state root, three determinism modes (strict / engine_native / none) with strict as v0.1 default for demos, ECS-component bodies, and explicit export-pipeline gating of `physics.3d` at v0.1 to Godot/Unity/Unreal targets only.**

## Confidence

**4/5.** Rapier's f32 strict-determinism mode is documented and validated. Layers, joints, contact events are the consensus pattern. The 5th confidence point is withheld until the Tier A canonical battery (Brief 134) measures actual cross-platform replay divergence on the v0.1 hardware floor with 1000 dynamic 2D bodies.

## Spec impact

- `gspl-reference/namespaces/physics.2d.md` — new namespace
- `gspl-reference/namespaces/physics.3d.md` — new namespace
- `gspl-reference/research/152-game-loop-tick-model-namespace.md` — physics step is the first phase of fixed-update
- `gspl-reference/research/153-ecs-substrate-binding.md` — `rigidbody.*` and `collider.*` components
- `gspl-reference/research/157-collision-and-trigger-primitives.md` (next brief) — extends the contact event surface
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — physics test family: 1000-body 2D divergence test, 100-body 3D divergence test, joint stability over 60s
- Tier D Briefs 188-196 — export pipeline gating

## New inventions

- **INV-614** — *Three-mode physics determinism* (strict / engine_native / none) as a signed scene gseed, with strict as default for v0.1 demos and the export pipeline emitting signed divergence warnings on engine_native.
- **INV-615** — *Per-tick Merkle-batched physics state root*, mirroring Brief 153's ECS pattern, so physics inherits frame-exact rollback at one signature per tick instead of one per body.
- **INV-616** — *Substrate-portable 2D/3D physics interface* — same component types, same query API, same joint types (modulo dimension), so creators write physics code once and the substrate routes to Rapier-2D, Rapier-3D, Box2D, or PhysX as configured.
- **INV-617** — *Tilemap auto-collision with per-tile override*, equipping platformer/dungeon-crawler tile worlds without forcing creators to hand-author colliders.
- **INV-618** — *Compile-time export gating of `physics.3d`* — 2D-only export targets refuse 3D physics components at compile, surfacing the gap to the creator before they hit a runtime crash on a target.

## Open follow-ups

- Whether continuous collision detection (CCD) is on by default for fast-moving bodies (provisional yes for projectiles, no for default dynamic; revisit per Brief 134 measurements).
- Whether v0.1 exposes destructible bodies (provisional no; defer to Round 8 with substrate-level Voronoi fracture).
- Soft-body and cloth — explicit v0.5 deferral per Brief 149 (sim integration).
- Vehicle physics (raycast vehicle, articulated vehicle) — defer to Tier E Brief 205 racing family.

## Sources

- Brief 131 — seven-axis structural claim
- Brief 134 — substrate-native benchmark battery
- Brief 135 — hardware budget v0.1
- Brief 149 — v0.1 scope finalization
- Brief 152 — game loop and tick model namespace
- Brief 153 — ECS substrate binding
- Round 2 Brief 026 — deterministic kernel implementation
- Rapier physics documentation (f32 determinism mode)
- Box2D documentation
- Bullet/Bullet3 documentation
- PhysX 5 documentation
- Erin Catto, "Iterative Dynamics with Temporal Coherence" (constraint solver reference)
- Glenn Fiedler, "Networked Physics" (deterministic lockstep + rollback)
