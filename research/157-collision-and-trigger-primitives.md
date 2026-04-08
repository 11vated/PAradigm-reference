# 157 — Collision and trigger primitives

## Question

How does GSPL equip the runtime collision and trigger surface — layers, masks, triggers, queries, raycasts, signed contact events — as substrate primitives that creators compose without writing per-game tag soup, and that lineage-track which system handled each contact?

## Why it matters (blast radius)

Collision and triggers are the primary glue between physics (Brief 156) and gameplay logic. Most game bugs and most multiplayer desyncs originate at collision boundaries: missed triggers, double-fired events, wrong contact response, tag-string typos. If GSPL ships only "raw physics contacts" creators reinvent dispatch logic per game and lose lineage at the contact boundary. Brief 157 makes contacts a *typed dispatch surface* with signed lineage from contact to response.

## What we know from the spec

- Brief 156 — physics ships signed contact events (begin/stay/end) and queries.
- Brief 153 — ECS components and systems with read/write declarations.
- Brief 152 — fixed tick scheduling for deterministic dispatch ordering.
- Brief 131 — seven-axis claim; contact responses are lineage-tracked.

## Findings

1. **Triggers are colliders with `is_trigger = true`.** A trigger detects overlap but never blocks motion. Default trigger types ship for the v0.1 starter genres: `damage_zone`, `pickup`, `goal`, `checkpoint`, `room_transition`, `dialogue`, `cutscene_start`. Each is a typed gseed in `physics.trigger.*` carrying its own data shape (e.g., `damage_zone` has `damage`, `damage_type`, `cooldown`).

2. **Contact dispatch is component-typed, not tag-string.** Instead of `if (other.tag == "Enemy")`, creators query `if other.has(components::enemy)`. The dispatch table is computed once at scene-compile from the components present on the colliding entities. This is the `B in A's mask AND A has component X AND B has component Y → call handler` pattern.

3. **Contact handlers are signed `physics.contact.handler` gseeds.** A handler declares `(name, query_a, query_b, phase, on_begin, on_stay, on_end)`. The phase determines whether the handler runs in `pre_solve` (can cancel the collision), `post_solve` (after impulses applied), or `narrow_phase` (between detection and response). Handlers are deterministic functions over the contact data and the entity components.

4. **Layer/mask is the broad-phase filter; component query is the narrow-phase dispatch.** Layers/masks (Brief 156 finding 7) prevent the physics solver from even considering certain pairs (cheap). Component queries on contact events filter further (precise). Together they replace tag-string runtime checks across the codebase.

5. **Queries are first-class signed primitives.** `physics.query.raycast`, `shapecast`, `overlap`, `closest_point`, `nearest_neighbor`. Each takes a signed query gseed and returns a signed result gseed. v0.1 supports both 2D and 3D variants. Queries are a key tool for AI perception (Brief 160), camera collision (Brief 155), and click-to-select UI.

6. **Continuous collision detection is per-body opt-in.** A `rigidbody.ccd` flag enables CCD for fast-moving small bodies (bullets, projectiles). Default off; opt-in costs ~2x narrow-phase. Mandatory for any body with the `projectile` component at v0.1.

7. **Contact response is signed lineage from event → handler → mutation.** When a contact handler mutates ECS state (e.g., deals damage), the resulting mutation gseed has parent lineage to the contact event gseed which has parent lineage to the physics step. This is the "why did this entity die?" debugging chain at zero extra cost — Brief 131's Lineage axis at the contact boundary.

8. **Trigger ordering is deterministic.** When two triggers fire on the same tick (e.g., a single dash through three damage zones), they fire in a deterministic order: `(handler_priority, entity_id_a, entity_id_b)`. The order is part of the signed `physics.tick.root` (Brief 156 finding 11) so replay is exact.

9. **Edge cases ship as named primitives, not workarounds.** Common bugs across engines that creators reinvent solutions for, equipped as substrate:
   - `physics.contact.dedupe` — fires `begin` once even if two colliders re-touch on the same tick after separation
   - `physics.contact.tunnel_check` — fast-mover trigger pass-through, equipped via swept-overlap query, not user code
   - `physics.contact.ground_check` — standard "is character grounded?" query as a typed primitive, not a per-game raycast
   - `physics.contact.coyote_time` — N-tick grace period after leaving ground for jump input, signed parameter

10. **Multi-collider compound bodies dispatch on the *body* by default.** A character with head/torso/legs colliders fires one `begin` per tick when any sub-collider enters a trigger. Per-collider dispatch is opt-in for hitbox systems (fighting games, Metroid-style boss weak points). The opt-in is a signed `physics.contact.per_collider` flag.

11. **Trigger volumes with state.** A `physics.trigger.zone` carries optional state: `entered_set` (the set of entity IDs currently inside), `enter_count`, `last_enter_tick`. Creators read these fields directly without maintaining their own bookkeeping. This eliminates an entire class of bug (forgetting to remove an entity from a tracked set when it dies).

12. **Differentiable contact handlers.** Per Brief 143, contact handlers that produce accepted-outcome lineage become positive examples in the action LoRA training set. Common handler patterns (e.g., "damage zone reduces health by configured amount") get promoted as default templates for new projects in the same genre.

13. **Performance budget.** On the v0.1 hardware floor, the contact dispatch system is budgeted at 1ms per fixed tick for 1000 dynamic 2D bodies in the canonical battery (Brief 134 extension). Beyond that envelope, the drift detector emits a `physics.dispatch.budget.breach` signal.

## Risks identified

- **Per-component dispatch table can grow large.** Mitigation: precompiled at scene-compile, not at runtime; lookup is O(1) hash on `(component_a_set, component_b_set, handler_query)`.
- **Trigger zone state can drift if entities are destroyed mid-contact.** Mitigation: ECS destroy emits `entity.destroyed` event; trigger zones subscribe and prune; signed.
- **Coyote time is taste-dependent (most platformers use 5-8 ticks at 60Hz).** Mitigation: ship per-genre default (6 ticks for platformer); creators override per scene.
- **Per-collider hitbox dispatch ×100 hitboxes can saturate the dispatch budget.** Mitigation: opt-in only, surfaced in debugger when crossed.

## Recommendation

**GSPL ships a `physics.contact` and `physics.query` and `physics.trigger` set of primitives at v0.1 with: triggers as colliders with `is_trigger`, eight starter trigger types with typed schemas, contact handlers as signed gseeds with phase placement (pre_solve / post_solve / narrow_phase), component-query dispatch instead of tag strings, layer/mask broad-phase filter + component-query narrow-phase dispatch, signed lineage from physics step → contact event → handler → state mutation, deterministic trigger ordering as part of the physics tick root, four named edge-case primitives (dedupe / tunnel_check / ground_check / coyote_time), per-body CCD opt-in, multi-collider compound body single-dispatch default, trigger zones with built-in entered_set state tracking, and differentiable handler promotion via Brief 143.**

## Confidence

**4/5.** The component-query dispatch pattern is the proven approach in Bevy, flecs, and modern ECS-physics integrations. Coyote time, ground check, and tunnel check as named primitives are uncommon in engines but well-known in creator culture (Maddy Thorson's Celeste postmortem notes); equipping them as substrate is a clean alignment.

## Spec impact

- `gspl-reference/namespaces/physics.contact.md` — new sub-namespace
- `gspl-reference/namespaces/physics.trigger.md` — new sub-namespace with typed starter trigger gseeds
- `gspl-reference/namespaces/physics.query.md` — new sub-namespace
- `gspl-reference/research/156-physics-integration-2d-and-3d.md` — cross-reference; this brief extends the contact event surface
- `gspl-reference/research/153-ecs-substrate-binding.md` — cross-reference; trigger zone uses ECS subscription
- `gspl-reference/research/143-differentiable-action-learning-recipe.md` — handler templates as training signal
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — contact dispatch test family

## New inventions

- **INV-619** — *Component-query contact dispatch* — replaces tag-string runtime checks with compile-time-resolved component-set dispatch tables, eliminating typo classes of bug and giving signed lineage on every dispatch.
- **INV-620** — *Four named edge-case primitives* (dedupe / tunnel_check / ground_check / coyote_time) equipped as substrate so creators stop reinventing and lose nothing in lineage when they use them.
- **INV-621** — *Trigger zones with built-in entered_set tracking* — bookkeeping creators usually maintain by hand, equipped and signed.
- **INV-622** — *Eight typed starter trigger gseeds* (damage_zone, pickup, goal, checkpoint, room_transition, dialogue, cutscene_start) covering ~80% of v0.1 starter-genre trigger needs without composition.
- **INV-623** — *Pre-solve / post-solve / narrow-phase handler placement* as a signed phase declaration on the contact handler gseed, giving creators precise control over when they cancel vs respond to a contact.

## Open follow-ups

- Whether trigger volumes can be parented to moving entities (provisional yes; verified at Tier C Brief 177 scene editor).
- Pull-request format for adding new starter trigger types (community contribution path defer to Round 8).
- Whether spatial hashing vs sweep-and-prune is the v0.1 broadphase default (provisional sweep-and-prune; revisit per Brief 134 measurements).

## Sources

- Brief 131 — seven-axis structural claim
- Brief 134 — substrate-native benchmark battery
- Brief 143 — differentiable action learning recipe
- Brief 152 — game loop and tick model namespace
- Brief 153 — ECS substrate binding
- Brief 156 — physics integration 2D and 3D
- Maddy Thorson, "Celeste & Towerfall Physics" GDC talk (coyote time, jump buffering, ground check primitives)
- Box2D / Rapier contact callback documentation
- Bevy ECS+Rapier integration patterns
- flecs trait-based dispatch reference
