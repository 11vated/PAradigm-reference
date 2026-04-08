# 168 — Enemy and creature taxonomies

## Question

What canonical enemy and creature taxonomies does GSPL ship in `enemy.*` and `creature.*` so that any genre can compose hostile, neutral, and ambient agents from typed role/archetype/tier primitives, with signed AI archetype bindings, telegraph contracts, and difficulty curves, by composition rather than from scratch?

## Why it matters (blast radius)

Enemies are the second-largest content category after the player character, and they sit at the intersection of combat (Brief 167), AI (Brief 160), animation (Brief 161), loot (Brief 169), level pattern (Brief 172), and progression (Brief 165). Without a typed enemy taxonomy, every creator reinvents "tank" and "DPS" with mismatched parameter shapes, breaking cross-game balance tooling and the substrate's promise of typed encounter design. The taxonomy is the lexicon balance tooling, encounter editors, and Tier E genre recipes use to talk about *what fights what*.

## What we know from the spec

- Brief 092 — character power systems and movesets, which the *creature side* decomposes from
- Brief 160 — AI primitives namespace (pathfinding/steering/perception/group/utility/fairness)
- Brief 159 — FSM/HFSM/BT, the substrate behavior trees enemies use
- Brief 161 — animation runtime; enemies have canonical animation sets
- Brief 167 — combat primitives that enemies bind to
- Brief 169 — loot tables that enemies feed
- Brief 086 / 086A — biology and cosmology libraries from Round 4 supply ecological context

## Findings

1. **Two namespaces, one taxonomy.** `enemy.*` is the *role/encounter* axis (how the player fights it); `creature.*` is the *biology/ecology* axis (what it is in the world). A goblin warrior is `enemy.role.bruiser × creature.species.goblin`. The split lets bestiary entries (Brief 169 collection) be biology-keyed while encounter design (Brief 172) is role-keyed. Both are signed gseeds, joined by reference.

2. **Eight enemy roles.** Surveying MMORPG combat tuning (WoW, FFXIV), action RPGs (Souls, Hades, Dead Cells), tactics RPGs (XCOM, Fire Emblem), shooters (Halo, Doom, Destiny), and horde/swarm games (Vampire Survivors, Risk of Rain) yields **8 canonical enemy roles**: `tank`, `bruiser`, `dps_ranged`, `dps_melee`, `support_healer`, `support_buffer`, `swarmer`, `controller`. Plus three structural tiers: `elite`, `mini_boss`, `boss` (orthogonal to role; any role can be elevated). Total combinations: 8 × 4 tiers (including base) = 32 named role-tier slots.

3. **`enemy.role.<name>` schema.** Each role gseed has parameters: `role_id`, `target_kpi: TargetKPI`, `default_resource_pool_template`, `default_movement_template`, `default_attack_pattern: AttackPatternId`, `default_telegraph_window_ticks`, `aggro_priority_formula`, `recommended_party_position`. KPIs are designer-facing targets (e.g., "tank should soak 30% of incoming raid damage"); balance tooling reads the typed KPI to flag misbalanced fights.

4. **`enemy.tier.<name>`.** Tier modifiers: `base` (1×), `elite` (2-3× HP, +1 ability, distinct telegraph), `mini_boss` (5-10× HP, multi-phase BT, dedicated arena cue), `boss` (20-100× HP, full HFSM with phases, scripted intro, signed encounter gseed). Tiers compose multiplicatively with role; the `enemy.composition` typed gseed binds role × tier × creature.

5. **Telegraph contract.** Every enemy attack must declare a typed telegraph: `telegraph.kind: enum{visual_flash, audio_cue, animation_windup, vfx_emit, area_indicator}`, `telegraph.lead_ticks`, `telegraph.cancellable: bool`, `telegraph.fairness_floor: u32` (the minimum lead time per tier). The substrate's `combat.damage_event` refuses to fire if its origin attack hasn't passed its telegraph window. This is the substrate-level *anti-cheap-shot* guarantee, and it's what makes Brief 160's `ai.fairness.*` family enforceable.

6. **Twelve canonical creature archetypes.** Surveying D&D 5e Monster Manual, Pokémon, Witcher bestiary, Final Fantasy bestiary, and Bloodborne yields **12 creature archetype families**: `humanoid`, `beast`, `undead`, `aberration`, `construct`, `elemental`, `fey`, `fiend`, `celestial`, `dragon`, `ooze`, `plant`. Each maps to default Brief 086 biology library entries, default movement and animation styles, and default loot tables (Brief 169).

7. **`creature.species.<name>` schema.** Parameters: `species_id`, `archetype: ArchetypeId`, `biology_ref: brief_086_ref`, `default_size: SizeClass`, `default_animation_set: clip_set_ref`, `default_voice_set: audio_set_ref`, `habitat: set<biome_id>`, `diet: enum{carnivore, herbivore, omnivore, none, magical}`, `social: enum{solitary, pair, small_pack, large_pack, swarm, hive}`, `intelligence: enum{none, instinct, animal, sentient, sapient, genius}`, `relations: set<creature_relation>`. Creatures are biology-first; their *role* in any encounter is layered on by `enemy.composition`.

8. **Five default size classes.** `tiny` (rat, slime), `small` (goblin, faerie), `medium` (human, wolf), `large` (ogre, bear), `huge` (giant, dragon). Bound to default hurtbox sizes (Brief 167) and animation rig templates (Brief 161). Sixth class `gargantuan` (kaiju, world-boss) ships at v0.4 with 3D-default.

9. **Difficulty curves.** Difficulty is *not* a property of an enemy; it's a property of an `encounter`. The substrate ships `enemy.encounter` as a typed gseed with: `enemy_loadout: set<(species_ref, role_ref, tier_ref, count)>`, `arena_ref`, `pacing_curve: enum{flat, ramping, wave, peak_valley}`, `recommended_player_level_band`, `target_clear_time_ticks`. Balance tooling (Brief 186) simulates encounters against the player's current loadout to compute a difficulty number deterministically.

10. **AI archetype bindings.** Each enemy gseed declares which AI primitives it uses from Brief 160: pathfinding mode, perception model, steering primitives, group behavior. The substrate ships ~24 named AI archetype templates (`berserker`, `kiter`, `sniper`, `flanker`, `pack_hunter`, `ambusher`, `patroller`, `guard`, `caster`, `summoner`, `medic`, `defender`, `runner`, `bomber`, `sleeper`, `scavenger`, `territorial`, `mimic`, `chaser`, `spawner`, `fortress`, `swarm_unit`, `passive`, `hostile_neutral`). Each is a parameterized FSM or BT from Brief 159.

11. **Anti-frustration enforcement.** Brief 160's `ai.fairness.*` (rubber_band, miss_first_shot, dramatic_pause, assist) compose into enemy gseeds via opt-in flags: `enemy.composition.fairness: set<fairness_flag>`. Default `boss` tier ships with `dramatic_pause + miss_first_shot` enabled; default `swarmer` ships with no fairness (swarms are intentionally unfair).

12. **Bestiary integration.** Each `creature.species` gseed automatically populates a Brief 169 collection entry with: discovered → seen once, scanned → analyzed by player ability, defeated → killed, mastered → killed N times. This couples the encounter system to the collection progression primitive (Brief 165) for free.

13. **Spawning and population.** `enemy.spawner` typed gseed: `spawn_set`, `density_per_area`, `respawn_policy: enum{none, on_zone_reset, on_timer, infinite_horde}`, `cap_concurrent`, `arena_predicate`. Spawners respect the per-tick budget from Brief 152; horde games (Vampire Survivors-class) declare a high cap (1000+ entities) with the auto-LOD primitive that culls off-screen entities.

14. **Encounter validation.** At sign time, encounters validate: (a) total expected DPS doesn't exceed player healing/i-frame budget; (b) crowd-control durations don't stack to perma-lock; (c) telegraph fairness floors are respected; (d) loadout composition includes at least one role appropriate for the player's archetype. Violations are warnings, not errors — the creator can override with explicit acknowledgement.

15. **Procedural enemy generation.** v0.4+ supports `enemy.procedural` gseed where role/tier/AI archetype are sampled from a constrained distribution at level-load time using a sub-seeded PRNG (Brief 160). Used by roguelikes (Hades, Dead Cells, Risk of Rain). v0.1 ships the schema; the runtime sampler is gated.

16. **v0.1 reach.** Roles: 8/8 ship. Tiers: 4/4 ship. Creature archetypes: 12/12 ship. Size classes: 5/6 ship (gargantuan defers to v0.4). AI archetype templates: ~20/24 ship (the 4 deferred are large-scale group archetypes that need 3D pathfinding). Encounter primitive ships fully. Procedural enemy generator schema ships, runtime gated to v0.4.

## Risks identified

1. **Role/tier explosion.** 32 named slots × 12 archetypes × 5 sizes = 1,920 combinations. Mitigation: not all combinations need pre-built templates; the substrate ships ~80 hand-curated templates (the 9 v0.1 genres' canonical enemies) and creators compose the rest.

2. **Telegraph contract breaks "hard" enemies.** Some genres (bullet hell, fighting games) intentionally minimize telegraphs. Mitigation: `telegraph.fairness_floor` is creator-overridable per encounter with an explicit "intentional difficulty" signed acknowledgment.

3. **Bestiary collection vs spoiler.** Some games hide enemy stats until scanned; collection gseed exposes everything. Mitigation: per-entry `visibility_state_per_player` field on Brief 165 collection primitive controls reveal.

4. **Procedural enemies break replay.** Mitigation: sub-seeded PRNG keyed on (encounter_id, tick) makes runs deterministic; v0.1 ships schema-only.

5. **Creature relations cycle.** "Goblins fear orcs, orcs fear ogres, ogres fear goblins" creates loops. Mitigation: relations are *attitudes*, not predicates; cycles are valid (rock-paper-scissors social graphs are fine).

6. **Difficulty number is gameable.** A balance tool that outputs a single difficulty number invites min-max creators to optimize *for* the number. Mitigation: balance tool outputs a vector of KPIs (clear time, deaths per attempt, damage taken, resource consumption) — not a scalar.

## Recommendation

Ship the dual `enemy.*`/`creature.*` taxonomy with 8 roles × 4 tiers (32 slots), 12 creature archetypes, 5 size classes, 24 AI archetype templates, signed telegraph contract, and `enemy.encounter` typed gseed. Hold gargantuan size, 3D-pathfinding-bound AI archetypes, and the procedural enemy runtime to v0.4. Wire encounter validation into the sign-time gate from v0.1 with override-with-acknowledgement.

## Confidence

**4/5.** Roles, tiers, and archetypes are well-grounded in published RPG and action game design. Held back from 5 by the procedural enemy generation schema, which is largely untested across the surveyed catalog (only ~5 shipped titles use it well) and may need a Round 8 revision pass.

## Spec impact

- Add `enemy.*` and `creature.*` namespaces with role, tier, archetype, species, encounter, spawner sub-namespaces
- Add the typed telegraph contract to `combat.damage_event`'s preconditions
- Add the 24 AI archetype templates to Brief 160's primitive library
- Cross-link to Brief 092 (movesets), Brief 160 (AI primitives), Brief 165 (bestiary collection), Brief 167 (combat resource pools and damage), Brief 169 (default loot tables), Brief 172 (encounter placement), Brief 186 (balance KPI vector)
- Mark gargantuan size, 4 AI archetypes, and procedural enemy runtime deferred per Finding 16

## New inventions

- **INV-675** Dual `enemy.*`/`creature.*` namespace split: role/tier vs biology/archetype as orthogonal signed axes
- **INV-676** Substrate-level signed telegraph contract enforced at `combat.damage_event` precondition
- **INV-677** 24 named AI archetype templates as parameterized FSM/BT gseeds composing Brief 160 primitives
- **INV-678** `enemy.encounter` typed gseed with sign-time validation (DPS budget, CC stack, telegraph floor, role coverage)
- **INV-679** Vector-not-scalar difficulty KPI output to deter difficulty-number gaming

## Open follow-ups

- 80 hand-curated v0.1 enemy templates (Round 8 reference appendix)
- Cross-creature ecology rules (Round 4 brief 086 may extend)
- Boss encounter scripting DSL (Brief 176 cutscene takes this)
- Procedural enemy runtime details (deferred to v0.4 round)

## Sources

1. D&D 5e Monster Manual + DMG encounter-building rules — role/tier/CR framework
2. Final Fantasy XIV raid design talks, Square Enix GDC 2017+ — KPI-driven role tuning
3. Hades enemy design talk, Supergiant GDC 2020 — telegraph and fairness defaults
4. XCOM 2 enemy AI architecture talk, Firaxis GDC 2016 — AI archetype templates
5. Halo combat encounter design retrospective, Bungie — encounter pacing curves
6. Dark Souls enemy placement design, FromSoftware (interview compilations)
7. Vampire Survivors swarm/horde architecture, Poncle, 2022
8. Witcher 3 bestiary system, CDPR
9. Pokémon species-as-data design, GameFreak retrospectives
10. Brief 092 (this repo) — character power systems
11. Brief 160 (this repo) — AI primitives (fairness family)
12. Brief 167 (this repo) — combat hitbox/hurtbox/damage event
13. Brief 086 (this repo) — biology library
