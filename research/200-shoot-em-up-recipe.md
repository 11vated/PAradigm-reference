# 200 — Shoot 'em up genre recipe

## Question
What is the typed genre composition recipe that produces a complete signed shoot 'em up gseed bundle (vertical / horizontal / bullet-hell / twin-stick classes) from substrate primitives, with deterministic bullet patterns, scoring, and wave progression?

## Why it matters (blast radius)
Shmups are the canonical proving ground for high-volume entity systems and deterministic bullet patterns. A working recipe demonstrates the substrate handles thousands of simultaneous entities with replay-bit-determinism — the highest-stress test for the runtime kernel short of an MMO.

## What we know from the spec
- Brief 020 — determinism contract.
- Brief 162 — VFX module stack.
- Brief 156 — physics integration.
- Brief 173 — tilemap (scrolling background).
- Briefs 197-199 — recipe template precedent.

## Findings
1. **Recipe inherits Brief 197 frame.**
2. **Required primitives.** `physics.body` (player + bullets + enemies), `vfx.system` (explosions), `bullet.pattern` (typed pattern definition), `wave.schedule` (typed enemy spawn timeline), `audio.bus`, `ui.element` (score / lives / power), `state.machine` (player state), `level.scene` (one stage), `save.snapshot` (high score), `camera.rig` (auto-scroll).
3. **Bullet pattern as typed primitive.** `bullet.pattern` is a typed gseed declaring: spawn point, direction function (constant / spread / aimed / arc / spiral / homing), velocity profile, lifetime, hitbox region, sub-emitter rules. Compositional — patterns can spawn sub-patterns. Deterministic per Brief 020.
4. **Wave schedule.** `wave.schedule` is a typed timeline of (timestamp, enemy archetype, spawn position, count, formation). Replay-bit-deterministic.
5. **Player state FSM.** Idle → Move → Hit → Invulnerable → Move (with grace period). Power-up state tracked as a typed `power.level` field with discrete tiers.
6. **Hitbox-vs-hurtbox separation.** Player has a small typed hurtbox distinct from their visual sprite (canonical shmup feel). Bullets have hitboxes. Validator gates that hurtbox area < sprite area.
7. **Auto-scroll camera.** Camera-rig in auto-scroll mode with typed scroll velocity. Vertical / horizontal sub-recipes select the axis.
8. **Sub-recipes.** Vertical (1942-class), horizontal (Gradius-class), bullet-hell (Touhou-class with high pattern density), twin-stick (Geometry Wars-class with analog aim and no auto-scroll).
9. **Validation contract.** Sign-time gates: at least one `bullet.pattern`, at least one `wave.schedule`, hurtbox area < sprite area, auto-scroll enabled (except twin-stick), per-frame entity budget declared (default 2000 simultaneous bullets).
10. **Performance budget as typed field.** Recipe declares max simultaneous entities and the substrate runtime gates spawning when the budget is exceeded. Enforces the brief's "deterministic at scale" promise.

## Risks identified
- **Entity budget breach.** Bullet-hell sub-recipe may exceed substrate budget on weak hardware. Mitigation: typed budget surfaces a warning at sign-time; runtime degrades gracefully by suppressing newest bullets.
- **Bullet pattern composition complexity.** Sub-pattern spawning chains can recurse unboundedly. Mitigation: typed depth cap (default 4); deeper nesting is a sign-time error.
- **Determinism across engines.** Brief 196 parity suite must include a bullet-hell fixture to validate the 8-engine parity claim under high entity load.
- **Hitbox tuning.** Shmup feel depends on precise hitbox/hurtbox calibration. Mitigation: ship validated presets from Cave / Touhou published numbers.

## Recommendation
Specify the shmup recipe as a `recipe.gseed` with typed `bullet.pattern` and `wave.schedule` primitives, hitbox/hurtbox separation gate, four sub-recipes (vertical / horizontal / bullet-hell / twin-stick), and a typed entity budget declared at sign-time. Default sub-recipe instantiation produces a playable single-stage game.

## Confidence
**4 / 5.** Shmup mechanics are well-published; the novelty is the typed `bullet.pattern` primitive and the entity-budget-as-typed-field pattern. Lower than 4.5 because high-entity determinism across engines needs Phase-1 measurement with the parity suite.

## Spec impact
- New spec section: **Shoot 'em up genre recipe specification**.
- Adds typed `bullet.pattern` and `wave.schedule` gseed kinds (or as recipe-extension types).
- Adds the hitbox/hurtbox validation gate.
- Cross-references Briefs 020, 156, 162, 197.

## New inventions
- **INV-834** — Typed `bullet.pattern` primitive with composable sub-pattern spawning, depth cap, and deterministic sub-seeding: bullet patterns are first-class typed gseeds, not opaque scripts.
- **INV-835** — Typed `wave.schedule` enemy spawn timeline as deterministic gseed: enemy waves are replayable bit-for-bit across runs.
- **INV-836** — Hitbox/hurtbox separation gate at sign-time: substrate enforces canonical shmup feel by gating that hurtbox area is structurally smaller than sprite visual area.
- **INV-837** — Per-recipe entity budget as typed field with sign-time and runtime enforcement: high-entity recipes declare their budget; substrate runtime degrades gracefully when exceeded.
- **INV-838** — Bullet-pattern composition depth cap as typed substrate primitive: prevents unbounded recursion in pattern definitions while exposing the cap as a creator-tunable parameter.

## Open follow-ups
- Bullet-hell parity fixture in Brief 196 — Phase 1.
- Replay-based scoring leaderboards — deferred to v0.4 with Brief 209.
- Procedural pattern generation — deferred to v0.4.

## Sources
1. Brief 020 — Determinism contract.
2. Brief 162 — VFX module stack.
3. Brief 196 — Cross-engine parity test suite.
4. Brief 197 — 2D platformer recipe.
5. Touhou Project pattern analysis (community-documented).
6. Cave shmup design talks.
7. Geometry Wars postmortem.
