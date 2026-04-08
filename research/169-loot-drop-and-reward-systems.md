# 169 — Loot, drop, and reward systems

## Question

What canonical loot, drop, and reward primitives does GSPL ship in `loot.*` so that any genre can adopt drop tables, weighted RNG, pity timers, bad-luck protection, crafting reagents, set bonuses, and reward grants by composition rather than from scratch, with deterministic replay, signed flow attribution, and v0.1 reach?

## Why it matters (blast radius)

Loot is the closed-loop reward system that converts encounter outcomes (Brief 168) into progression fuel (Brief 165) and economy inputs (Brief 166). It is the densest source of pseudo-RNG bugs, replay non-determinism, and balance regressions. Without typed loot primitives, every game reinvents drop tables and pity timers, breaking cross-game balance tooling and replay fidelity. Brief 168 (enemies) feeds it, Brief 167 (combat) triggers it, Brief 165 (collection / progression) consumes it, Brief 166 (economy faucets) attributes from it, Brief 186 (balance) reads it, and Tier E genre recipes for ARPG/MMO/loot-shooter/roguelike (Briefs 198, 199, 203) compose densely from it.

## What we know from the spec

- Brief 153 — ECS substrate; loot grants are signed mutations
- Brief 158 — save/load; inventory state and pity counters are saved
- Brief 165 — progression and collection primitives consume loot
- Brief 166 — economy faucets attribute through loot
- Brief 167 — combat damage events trigger loot rolls on death
- Brief 168 — enemies declare default loot table refs
- Brief 160 — sub-seeded PRNG for deterministic randomness

## Findings

1. **Six canonical loot primitives.** Surveying Diablo 2/3/4, Path of Exile, Borderlands 3, Destiny 2, Hades, Hollow Knight, Stardew Valley, Monster Hunter, and World of Warcraft yields **six irreducible primitives**: `loot.table`, `loot.entry`, `loot.roll`, `loot.pity`, `loot.grant`, `loot.set_bonus`. Every shipped loot system reduces to these six composed.

2. **`loot.table`.** A weighted bag of possible drops. Parameters: `table_id`, `entries: ordered_set<EntryRef>`, `roll_count: u8 ∈ [0, 32]`, `roll_count_formula: optional<expr>`, `unique_roll: bool`, `magic_find_modifier: f32`, `parent_table: optional<table_ref>`, `signing_authority`. Tables can be hierarchical (a "boss_loot" table can reference a "common_loot" sub-table); inheritance is signed. Roll count can be a formula referencing combat context (e.g., "killing blow was a critical → +1 roll").

3. **`loot.entry`.** A possible drop within a table. Parameters: `entry_id`, `payload: enum{item_ref, currency_ref, xp, status, recipe, blueprint, lore_unlock}`, `weight: u32`, `quantity: range<u32>`, `quantity_formula: optional<expr>`, `condition_predicate: optional<predicate>`, `attribution_tag: AttributionTagId`, `tier: enum{common, uncommon, rare, epic, legendary, mythic, unique}`. Entries are typed by payload kind; the same primitive supports item drops, currency drops, XP grants, recipe unlocks, and lore reveals.

4. **`loot.roll`.** The signed deterministic sampling event. Parameters: `roll_id`, `table_ref`, `tick`, `seed: u64` (sub-seeded from Brief 160 via `(scene_seed, tick, killer_id, victim_id)`), `magic_find: f32`, `result: ordered_set<entry_ref>`, `pity_state_before`, `pity_state_after`, `lineage`. Rolls are signed events in the per-tick Merkle batch (Brief 153); the substrate guarantees that two clients given the same inputs produce identical rolls. This is the substrate-level *replay-fair RNG* guarantee.

5. **`loot.pity`.** Bad-luck protection state. Parameters: `pity_id`, `tracked_entries: set<entry_ref>`, `threshold: u32`, `current_count_per_player: u32`, `reset_on_drop: bool`, `weight_boost_per_failed_roll: f32`, `guaranteed_at_threshold: bool`. Pity is a typed component on the player entity, persists across sessions, and is exposed to balance tooling. The substrate ships pity per-rare-or-higher entry by default; creators can opt out per-table.

6. **`loot.grant`.** The actual hand-off of loot to the player. Parameters: `grant_id`, `recipient: entity_ref`, `payload`, `quantity`, `source: roll_ref | direct_grant`, `cause_event: gseed_ref`, `tick`, `lineage`. Grants are signed events; they fire `economy.flow` events (Brief 166) for currency payloads, mutate inventory components for item payloads, and update collection/progression for unlock payloads. Anti-cheat reads grants for verification.

7. **`loot.set_bonus`.** Equipment-set conditional buffs. Parameters: `set_id`, `member_items: set<item_ref>`, `tiered_bonuses: ordered_map<u8, bonus_ref>` (e.g., 2-piece, 4-piece, 6-piece bonuses), `stack_with_other_sets: bool`, `unique_per_player: bool`. Set bonuses are read by the equipment system at equip time and apply as Brief 167 status effects.

8. **Drop attribution.** Every loot.entry carries an `attribution_tag` (e.g., `boss_kill`, `chest_open`, `quest_reward`, `world_drop`, `crafting_byproduct`). Tags feed into Brief 166 economy faucet attribution and Brief 186 balance tooling. Designers can ask "what fraction of legendary drops came from world chests vs boss kills?" without instrumentation.

9. **Eight default rarity tiers.** `common (50%) / uncommon (30%) / rare (12%) / epic (5%) / legendary (2.5%) / mythic (0.5%) / unique (special-cased) / cursed (special-cased)`. Tier weights are templates, not enforced — creators set their own weights per table. Tier names are localization keys (Brief 220) and have default colors (Brief 174 UI).

10. **Magic find / luck stat.** Optional player-side modifier. Parameters on `loot.table`: `magic_find_modifier` is multiplied by player's `magic_find` stat to skew weights toward higher-rarity entries. Implementation uses the canonical "shifted weight" approach (Diablo 2-style) which is replay-deterministic.

11. **Replay determinism.** Loot rolls *must* be bit-for-bit replayable. Achieved by: (a) sub-seeded PRNG keyed on (scene, tick, killer, victim) — never on wall clock; (b) integer arithmetic for weight calculations; (c) signed roll events in the per-tick Merkle batch. Two creators replaying the same recording get the same drops.

12. **Inventory integration.** Loot grants flow into inventory components on the recipient entity. Inventory itself is *not* a loot primitive — it's a generic ECS component (`inventory.bag`, `inventory.equipment`, `inventory.bank`) defined as part of Brief 153's typed component library. Inventory size, slot rules, weight, and stack limits are per-game configuration, not substrate primitives.

13. **Crafting reagents.** Loot entries with `payload=item_ref` for ingredient-class items feed Brief 164's `mechanic.craft.*` family. Creators don't need a separate "reagent" loot primitive; ingredient-ness is a tag on the item gseed itself.

14. **Lore drops.** Loot entries with `payload=lore_unlock` write to a typed `progression.collection` of type `lore_codex` (Brief 165). Examples: Witcher journal entries on bestiary scan, Dark Souls item descriptions, Hollow Knight lore tablets. The substrate guarantees that lore drops respect Brief 165's `discovered/collected/mastered` state machine.

15. **Reward grants outside loot tables.** Quest rewards, milestone rewards, and login rewards are *direct grants*, not rolled — they use `loot.grant` with `source=direct_grant`. The same signing/attribution flows. The substrate intentionally unifies "rolled drops" and "guaranteed rewards" under one primitive so balance tooling has one query path.

16. **v0.1 reach.** All 6 primitives ship at v0.1. The 8 rarity tiers ship as templates. Pity timers ship. Set bonuses ship. Magic find ships. Federation-shared loot tables (where two games share a community drop pool) defer to v0.5; in v0.1-v0.4, every loot table is per-game.

## Risks identified

1. **Pity timer is gameable.** A player who learns the threshold can farm to threshold then risk a roll. Mitigation: pity is a *minimum guarantee*, not a *maximum*; creators can hide the threshold from the UI but the substrate exposes the typed state for accessibility/tooling.

2. **Hierarchical tables get confusing.** A 4-deep table inheritance graph with weight modifiers per level is hard to balance. Mitigation: editor (Brief 181) renders the *flattened* effective weights; sign-time check warns past 3 levels of inheritance.

3. **Magic find creates degenerate strategies.** Stack magic find → never play balanced builds. Mitigation: substrate-level cap at `magic_find_modifier ≤ 5.0`; balance tooling flags any item granting >100% magic find.

4. **Replay drift via floating-point weight calc.** Mitigation: all weight calc is in `u64` integer arithmetic; floats only at the typed-API surface, immediately quantized.

5. **Set bonuses interact with stack policies.** Two 6-piece sets with conflicting bonuses. Mitigation: `unique_per_player: bool` flag plus Brief 167's status effect stack policies handle the runtime.

6. **Inventory not being a substrate primitive bites later.** A creator wanting a complex inventory (Resident Evil 4 grid, Path of Exile inventory) may want substrate-level support. Mitigation: typed `inventory.*` component library in Brief 153 ECS; this brief just declines to specify inventory rules at the loot level.

## Recommendation

Ship the 6-primitive `loot.*` vocabulary with the 8 default rarity tiers, signed roll events with sub-seeded PRNG, pity by default for rare+, attribution tags, hierarchical tables with sign-time validation, and unified direct/rolled grant primitive. Wire balance tooling to read the typed table graph from day one. Defer federation-shared loot tables to v0.5.

## Confidence

**4.5/5.** Loot primitives are extremely well-studied: 25+ years of ARPG design, GDC talks on Diablo/Borderlands/Destiny tuning, and academic papers on loot economy convergence make this decomposition tight. The only soft spot is federation-shared tables, which is an open research question deferred to v0.5.

## Spec impact

- Add `loot.*` namespace with 6 primitive sub-namespaces and `loot.roll`/`loot.grant` event types
- Add the 8 default rarity tiers as templates
- Add the sub-seeded PRNG keying rule `(scene, tick, killer, victim)` to Brief 160's PRNG namespace
- Cross-link to Brief 153 (inventory components), Brief 158 (save), Brief 160 (PRNG), Brief 165 (collection/lore consumer), Brief 166 (economy faucet attribution), Brief 167 (combat damage event trigger), Brief 168 (enemy default tables), Brief 186 (balance), Brief 213 (anti-cheat reads grants)
- Mark federation-shared loot tables deferred to v0.5

## New inventions

- **INV-680** Six-primitive canonical `loot.*` substrate vocabulary with unified rolled/direct grant model
- **INV-681** Sub-seeded PRNG keyed on `(scene, tick, killer, victim)` as substrate-level replay-fair RNG guarantee for loot rolls
- **INV-682** Pity-as-typed-component with persisted bad-luck protection state and balance tool exposure
- **INV-683** Drop attribution tags as substrate primitive feeding economy faucet attribution
- **INV-684** Hierarchical loot table inheritance with sign-time depth validation and editor-side flattening preview

## Open follow-ups

- Federation-shared loot pools (deferred to v0.5)
- Inventory component library spec (Brief 153 follow-up appendix)
- Crafting recipe gseed schema (Brief 164 follow-up appendix; consumer of loot reagents)
- Localization rules for rarity tier names (Brief 220 i18n)
- Genre-specific drop rate templates (Brief 230 cross-genre matrix)

## Sources

1. Diablo 2 LoD itemization design retrospective, Blizzard
2. Diablo 3 loot 2.0 redesign talk, Blizzard GDC 2014
3. Path of Exile itemization talk, Chris Wilson GGG GDC 2018
4. Borderlands 3 loot system talk, Gearbox GDC 2020
5. Destiny 2 loot economy postmortem, Bungie GDC 2019
6. Hades boon roll design talk, Supergiant GDC 2020
7. Hollow Knight charm system retrospective, Team Cherry
8. World of Warcraft raid loot tuning interviews, Blizzard
9. Monster Hunter Rise reward system, Capcom design talks
10. *Game Mechanics: Advanced Game Design*, Adams & Dormans, ch. on randomness and rewards
11. Brief 020 (this repo) — fixed-point/integer determinism
12. Brief 160 (this repo) — sub-seeded PRNG primitives
13. Brief 097 (this repo) — anti-hallucination test suite (loot determinism battery)
