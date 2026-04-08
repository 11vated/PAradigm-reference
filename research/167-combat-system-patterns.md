# 167 — Combat system patterns

## Question

What canonical combat system patterns does GSPL ship in `combat.*` so that any genre — real-time, turn-based, ATB, action, tactics, asymmetric — can adopt damage formulas, hitboxes, hitstop, juice, status effects, and combat resolution by composition rather than from scratch, and what are the bounds, signed primitives, and v0.1 reach?

## Why it matters (blast radius)

Combat is the dominant interaction surface in most games and is the densest source of frame-perfect bugs, balance regressions, and replay non-determinism. Without typed combat primitives, every creator reinvents hitbox vs hurtbox queries, damage formulas, hitstop, and status effects — and the substrate cannot reason about damage attribution, replay validity, or competitive fairness. Brief 168 (enemies) consumes combat primitives, Brief 169 (loot) is fed by them, Brief 186 (balance) reads them, Brief 199 (shooter genre) and Brief 206 (fighting genre) compose them densely, and Tier F multiplayer (Briefs 209-216) requires combat events to be deterministically signed for rollback netcode.

## What we know from the spec

- Brief 153 — ECS substrate; combat entities, hitboxes, hurtboxes are typed components
- Brief 154 — input action layer; combat verbs (Brief 164's attack family) fire combat events
- Brief 156 — physics; hitbox queries use the physics broadphase
- Brief 157 — collision/triggers; hit detection uses contact handlers
- Brief 161 — animation; hitboxes are bound to animation frames with cancel windows
- Brief 164 — mechanic vocabulary; the attack/defend families terminate in combat events
- Brief 209 — networking; combat events must be deterministic for rollback netcode

## Findings

1. **Six combat resolution modes.** Surveying fighting games (Street Fighter, Tekken, Guilty Strive), action games (Devil May Cry, Bayonetta, Hades, Hollow Knight), turn-based RPGs (Final Fantasy, Persona), tactics (Fire Emblem, XCOM), shooters (Halo, Doom Eternal), and ATB hybrids (FF7R) yields **six canonical combat resolution modes**: `realtime_action`, `turn_based`, `atb` (active time battle), `tactics_grid`, `asymmetric` (Dead by Daylight, Evolve), `auto_resolve` (auto-battler, idle). Each is a `combat.mode` enum value selecting which subset of `combat.*` primitives are used.

2. **Eight irreducible combat primitives.** `combat.hitbox`, `combat.hurtbox`, `combat.damage_formula`, `combat.damage_event`, `combat.status_effect`, `combat.resource_pool`, `combat.hitstop`, `combat.knockback`. These eight cover every shipped combat system; the resolution mode (Finding 1) determines *when* they fire, not *which* exist.

3. **`combat.hitbox`.** A signed offensive volume tied to an animation frame range. Parameters: `hitbox_id`, `shape: enum{box, sphere, capsule, polygon}`, `local_transform`, `active_frame_range: (u32, u32)`, `damage_formula_ref`, `hit_layer: u8`, `multi_hit: bool`, `max_hits_per_target`, `priority: i8`, `cancel_window_into: set<mechanic_ref>`, `vfx_on_hit: vfx_ref`, `audio_on_hit: audio_ref`. Hitboxes are bound to Brief 161 animation clip events; the substrate guarantees frame-perfect activation/deactivation.

4. **`combat.hurtbox`.** The defensive volume. Parameters: `hurtbox_id`, `shape`, `local_transform`, `defense_layer: u8`, `armor: u32`, `vulnerability_multiplier: f32 ∈ [0.0, 10.0]`, `invulnerable_during: optional<state_ref>`, `parry_window: optional<(u32, u32)>`, `block_window: optional<(u32, u32)>`. Hit/hurt layers form a configurable matrix (player melee can hit enemy body but not enemy parry hurtbox, etc.) — defaults to a 16×16 matrix per Brief 156 collision layer count.

5. **`combat.damage_formula`.** A typed signed expression. The substrate ships **eight default formulas**: `flat`, `additive` (atk - def), `multiplicative` (atk * (atk / (atk + def))), `percent_max_hp`, `percent_current_hp`, `pokemon` (the canonical level/atk/def/effectiveness/STAB formula), `dnd_dice` (XdY+Z with crit), `souls` (motion-value × weapon × scaling). Each is parameterized; creators can fork or write a `custom` formula via the typed expression DSL. Formulas are *deterministic* — random rolls use a sub-seeded PRNG (Brief 160) keyed on (combatant_id, hit_id, tick) so replays are stable.

6. **`combat.damage_event`.** The resolved hit. Parameters: `attacker_ref`, `target_ref`, `hitbox_ref`, `hurtbox_ref`, `final_damage: i32`, `damage_type: DamageTypeId`, `crit: bool`, `block_state: enum{none, partial, full, parry}`, `tick`, `lineage`. Damage events are signed and per-tick Merkle-batched (Brief 153); they form the substrate-level audit trail for combat. Anti-cheat (Brief 213) verifies multiplayer damage events against the formula and the inputs.

7. **`combat.status_effect`.** Buffs/debuffs/DoTs/CC. Parameters: `effect_id`, `kind: enum{buff, debuff, dot, hot, cc}`, `magnitude: f32`, `duration_ticks`, `tick_interval`, `stack_policy: enum{refresh, stack, max_one, replace_lowest}`, `cleanse_categories: set<CategoryId>`, `expiry_event: optional<gseed_ref>`, `vfx_attached: vfx_ref`, `cc_kind: enum{stun, root, silence, fear, charm, slow}`. Status effects are typed ECS components on the target; tick draining/expiry is handled by the fixed-update scheduler from Brief 152.

8. **`combat.resource_pool`.** HP, MP, stamina, shield, armor, focus, etc. Parameters: `pool_id`, `current: u32`, `max: u32`, `regen_per_tick: f32`, `regen_delay_after_damage_ticks: u32`, `overheal_policy`, `min_clamp`, `damage_categories_affecting: set<DamageTypeId>`. The substrate ships ~6 default pool types but creators can declare any pool id. Pool depletion can fire `expiry_event` gseeds (e.g., on HP=0, fire `mechanic.die`).

9. **`combat.hitstop`.** Frame freezing on impact. Parameters: `duration_ticks: u8 ∈ [0, 30]`, `applies_to: enum{attacker, target, both, all}`, `scaled_by_damage_pct: bool`, `chromatic_aberration: bool`, `screen_freeze: bool`. Hitstop is the single biggest contributor to "game feel" per Steve Swink and the Devil May Cry/Bayonetta combat designers; the substrate makes it a first-class signed primitive.

10. **`combat.knockback`.** Impulse on hit. Parameters: `magnitude: f32`, `direction_mode: enum{relative_to_attacker, fixed, away_from_hitbox_center, custom}`, `vertical_component: f32`, `clamps_to_velocity_cap: bool`, `affects_grounded: bool`. Knockback fires through Brief 156 physics as a typed impulse; in turn-based games it's a tile pushback resolved discretely.

11. **Mode bindings.** Each `combat.mode` defines which primitives fire when:
    - `realtime_action`: hitboxes active per anim frame, damage events on contact, hitstop+knockback applied immediately
    - `turn_based`: hitboxes/hurtboxes are abstract slots; damage formula evaluated on action commit; hitstop/knockback are visual-only
    - `atb`: like turn_based but with a tick gauge; damage events fire on gauge full
    - `tactics_grid`: hitboxes are grid cells; damage formula respects flanking/elevation/cover modifiers
    - `asymmetric`: two role classes with different hurtbox/hitbox layer matrices; example primitive present at v0.3
    - `auto_resolve`: combat round = single damage_event per attacker per round, no animation gating

12. **Combo and cancel system.** Cancel windows on hitboxes (Finding 3, `cancel_window_into`) form the combo graph. The substrate represents combos as a typed DAG: nodes are mechanics (Brief 164 attack family), edges are cancel windows. Editor (Brief 181) renders this graph for fighting game designers; the parser checks for unreachable nodes and infinite loops.

13. **Damage type matrix.** ~12 default damage types (physical, slash, pierce, blunt, fire, ice, lightning, poison, holy, dark, true, healing). Resistance/weakness lives on hurtboxes as a typed table. Pokémon-style 18-type type chart is a creator template, not the default.

14. **Replay determinism.** Combat must be bit-for-bit replayable. Achieved by: (a) signed input recording (Brief 154), (b) sub-seeded RNG per damage roll, (c) per-tick Merkle batching of damage events, (d) animation events on fixed-tick boundaries (Brief 161). Brief 097's anti-hallucination test suite includes a combat-determinism battery.

15. **Hitstop in netcode.** Hitstop is local-visual-only in rollback netcode; it does not freeze the simulation. Mitigation: hitstop is a render-layer effect with a separate `combat.hitstop.simulation` flag for single-player games that want full pause.

16. **v0.1 reach.** All 8 primitives ship at v0.1. Modes shipped at v0.1: `realtime_action`, `turn_based`, `atb`, `tactics_grid`, `auto_resolve` (5/6). `asymmetric` defers to v0.3 multiplayer. Damage formulas: all 8 ship. Status effects, resource pools, hitstop, knockback all ship.

## Risks identified

1. **Hitbox/hurtbox layer matrix complexity.** 16×16 matrices are confusing. Mitigation: editor (Brief 181) ships a visual matrix view; default matrices for the 6 modes ship as templates.

2. **Damage formula edge cases.** Floor/ceiling, division by zero, negative final damage. Mitigation: substrate clamps final damage to [-resource_pool.max, +resource_pool.max] and never divides by zero; formulas validated at sign time.

3. **Replay drift via floating-point in formulas.** All damage math is in fixed-point per Brief 020; the typed expression DSL forbids `f32` arithmetic outside explicit `quantize_to_fixed` operations.

4. **Combo system explodes.** Devil May Cry's combo graph has thousands of edges. Mitigation: editor warns past 500 nodes; the runtime BT shallow-cache (Brief 159) helps performance.

5. **Status stacking is the canonical bug source.** Mitigation: 4 explicit stack policies (Finding 7); creator must pick one per effect at sign time.

6. **Attacker attribution in chains.** "Player A casts a curse on enemy B, B kills enemy C — who gets credit?" Mitigation: damage events carry full lineage; attribution is a query-time decision per Brief 186 balance tooling.

## Recommendation

Ship the 8-primitive `combat.*` vocabulary with the 6 resolution modes, the 8 default damage formulas, the 12-entry damage type matrix, and the 4 stack policies. Wire combat events into the per-tick Merkle batch from day one for replay/anti-cheat parity. Hold `asymmetric` mode behind v0.3; everything else ships at v0.1. Surface combo DAG, layer matrix, and hitbox preview through the Brief 181 editor.

## Confidence

**4.5/5.** Combat system primitives are the most well-studied area in game design — 30+ years of fighting game frame data, action game design talks, and tactics RPG postmortems converge tightly on this decomposition. The only soft spot is `asymmetric` mode (only ~6 shipped titles use it) which is why it defers to v0.3.

## Spec impact

- Add `combat.*` namespace with 8 primitive sub-namespaces and `combat.damage_event` event type
- Add the 6 mode enum and the 8 damage formula library
- Add the 12-entry damage type matrix
- Cross-link to Brief 153 (ECS), Brief 154 (input/actions), Brief 156 (physics impulses), Brief 157 (collision dispatch), Brief 161 (animation cancel windows), Brief 168 (enemy AI consumer), Brief 186 (balance), Brief 209 (rollback netcode)
- Mark `combat.mode.asymmetric` deferred to v0.3

## New inventions

- **INV-670** Eight-primitive canonical `combat.*` substrate vocabulary spanning six combat resolution modes
- **INV-671** Eight pre-shipped damage formula library (flat / additive / multiplicative / pct-max / pct-current / pokemon / dnd-dice / souls) as signed gseed templates
- **INV-672** `combat.damage_event` per-tick Merkle-batched signed event as substrate-level combat audit trail
- **INV-673** Combo-as-typed-DAG with cancel-window edges and editor visualization
- **INV-674** Hitstop-as-render-layer-only flag for rollback-netcode compatibility

## Open follow-ups

- Specific damage formula presets per genre (Brief 230 takes this)
- Hit-spark VFX defaults (Brief 162 already specifies; this brief consumes)
- Voice barks on combat events (Brief 175 audio takes this)
- Frame data exporter for fighting game creators (Brief 181 editor follow-up)

## Sources

1. *Game Feel*, Steve Swink, ch. on impact and feedback — hitstop and game feel framing
2. Devil May Cry combat design talk, Hideaki Itsuno, GDC 2007 — combo cancel discipline
3. Bayonetta combat design retrospective, PlatinumGames, 2010 — hitstop magnitudes
4. Street Fighter V frame data documentation, Capcom — hitbox/hurtbox/cancel windows
5. Hades combat design talk, Supergiant GDC 2020 — boon/status effect system
6. Hollow Knight combat retrospective, Team Cherry — soul/damage/heal pool architecture
7. Final Fantasy formula reference, gamefaqs/wiki — additive/multiplicative formula reference
8. Pokémon damage formula breakdown, Bulbapedia — type matrix and STAB
9. XCOM 2 design talk, Firaxis GDC 2016 — flanking/cover tactics combat
10. Doom Eternal combat design talk, id Software GDC 2020 — resource pool ecology
11. Brief 020 (this repo) — fixed-point determinism
12. Brief 097 (this repo) — combat determinism test battery
13. Brief 156 (this repo) — physics impulses
14. Brief 161 (this repo) — animation cancel windows
