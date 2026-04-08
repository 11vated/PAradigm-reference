# 165 — Progression system patterns

## Question

What canonical progression patterns does GSPL ship as signed gseed templates in `progression.*` so that any genre can adopt XP/level, skill tree, gear score, mastery, prestige, milestone, narrative-gate, or hybrid progression by composition rather than from scratch, and what are the parameter bounds, lineage rules, and v0.1 reach for each?

## Why it matters (blast radius)

Progression is the *meta-loop* that turns moment-to-moment mechanics (Brief 164) into a multi-hour player arc. Without typed progression primitives, every creator reinvents XP curves, level caps, skill prerequisites, and milestone unlocks — and two RPGs cannot share progression analytics, balance tooling, or signed difficulty audits because their progression isn't introspectable. Tier C balance tooling (Brief 186), Tier H pacing (Brief 225), Tier H replay loops (Brief 227), and Tier F live-ops (Brief 214) all assume a typed `progression.*` namespace exists. Get this wrong and the substrate cannot reason about pacing, fairness, or content gating.

## What we know from the spec

- Brief 164 — mechanic vocabulary; mechanics are the *atoms* progression unlocks
- Brief 153 — ECS substrate; progression state lives in typed components on the player entity
- Brief 158 — save/load; progression state is the bulk of any save
- Brief 159 — FSM/BT; progression often gates BT branches
- Brief 092 — character power systems; progression is how characters grow into those systems
- Brief 149 — v0.1 scope: 9/13 Tier B briefs ship at v0.1, with a 2D + sprite + image + character creator focus

## Findings

1. **Eight canonical progression primitives.** Surveying RPGs (Skyrim, Witcher 3, Disco Elysium, Final Fantasy XIV, Path of Exile), action games (Hades, Hollow Knight, Dead Cells), shooters (Destiny 2, Borderlands), and casual games (Stardew Valley, Animal Crossing) yields **8 reusable progression primitives** that compose into every shipped progression system: `progression.xp_level`, `progression.skill_tree`, `progression.gear_score`, `progression.mastery`, `progression.prestige`, `progression.milestone`, `progression.narrative_gate`, `progression.collection`. Each is a signed gseed template with parameter bounds; creators compose multiple primitives into the *progression graph* of their game.

2. **`progression.xp_level`.** The classic linear primitive. Parameters: `xp_curve: enum{linear, polynomial, exponential, custom_table}`, `curve_params`, `level_cap: u16 ∈ [1, 9999]`, `xp_sources: set<source_id>`, `level_up_handler: gseed_ref`, `rollover_xp: bool`. Default curves: D&D-style (cumulative xp), JRPG-style (per-level xp), MMO-style (exponential). Signed XP source IDs let balance tooling answer "what fraction of level 30 came from quests vs combat?".

3. **`progression.skill_tree`.** The branching unlock graph. Parameters: `nodes: set<SkillNode>`, `edges: set<Prereq>`, `currency: ProgressionCurrency`, `respec_policy: enum{none, paid, free, time_locked}`, `point_sources: set<source_id>`, `mutual_exclusion_groups: set<group_id>`. Skill nodes are typed gseeds referencing the mechanics (Brief 164) they unlock or modify. The tree is a DAG, validated at sign time (no cycles, no orphans, all prereqs reachable from a root node).

4. **`progression.gear_score`.** The Diablo/Destiny model. Parameters: `slots: set<EquipmentSlot>`, `score_formula: enum{sum, max, weighted, custom}`, `tier_thresholds: ordered_set<u32>`, `gear_pool_ref: loot_table`, `set_bonuses: set<SetBonus>`. Gear score is itself a derived signed component on the player entity, recomputed on equip/unequip mutations.

5. **`progression.mastery`.** The "use it to level it" model (Skyrim, RuneScape, FF14 jobs). Parameters: `tracked_actions: set<mechanic_id>`, `xp_per_action: f32`, `mastery_levels: u16 ∈ [1, 200]`, `passive_bonuses_per_level: set<bonus_ref>`, `cross_skill_bleed: f32 ∈ [0.0, 1.0]`. Mastery binds directly to Brief 164 mechanics — every action verb can have a mastery counter attached.

6. **`progression.prestige`.** The NG+/post-cap loop. Parameters: `prestige_levels: u16 ∈ [0, 99]`, `reset_scope: enum{full, partial, cosmetic_only}`, `carryover_set: set<carryover_ref>`, `prestige_bonuses: set<bonus_ref>`, `prestige_unlocks: set<unlock_ref>`. Prestige is the v0.5 sim-loop's most important primitive but ships at v0.1 as the New Game Plus pattern for narrative games.

7. **`progression.milestone`.** Discrete one-time unlocks (Animal Crossing, Stardew). Parameters: `milestones: set<Milestone>` where each Milestone has `condition: predicate`, `reward: gseed_ref`, `repeatable: bool`, `hidden: bool`. Predicate is a typed expression over ECS components (e.g., "harvested 100 carrots") evaluated at tick boundary. Cheap, signed, and the most common pattern for casual games.

8. **`progression.narrative_gate`.** Story-locked progression (Witcher, Mass Effect, Disco Elysium). Parameters: `gates: set<Gate>` where each Gate has `unlocks_after: quest_ref`, `unlocks_content: content_ref`, `bypassable_by: optional<predicate>`. Narrative gates bind directly to Brief 170 quest gseeds.

9. **`progression.collection`.** Pokédex-class enumeration (Pokémon, Witcher bestiary, Dead Cells weapon log). Parameters: `collection_id: CollectionId`, `entries: set<EntryRef>`, `entry_state_per_player: enum{discovered, collected, mastered}`, `completion_rewards: ordered_map<percentage, reward_ref>`. Each entry is a signed gseed; the player's collection state is itself a signed component.

10. **Composition rules.** A real game uses 2-5 of these primitives simultaneously. Witcher 3 uses `xp_level + skill_tree + gear_score + narrative_gate + collection`. Stardew uses `mastery + milestone + collection + narrative_gate`. Hades uses `xp_level + gear_score + prestige + collection + skill_tree(mirror)`. The substrate's `progression.composition` typed gseed binds N primitives into one *progression graph* with cross-referenced gates (e.g., "skill node X requires level 20 AND quest Y completed").

11. **Pacing introspection.** Because every primitive is signed and typed, balance tooling (Brief 186) can answer questions like "given the current XP curve and average mission XP, what tick range is the player in level 15 on average?". This is the entire reason progression must be typed-not-coded: it lets the substrate auto-graph pacing without instrumentation.

12. **Lineage and forking.** Creators fork progression templates the same way they fork mechanics. A creator who wants Hollow Knight's "no XP, only items" model forks `progression.skill_tree` with `currency=charm_slots`, `point_sources={}`, `respec_policy=free`. The parent reference stays in the lineage; the substrate verifies the fork's bounds.

13. **Bounds and validation.** Level caps clamped to [1, 9999]; XP curves required to be monotonic (validated at sign time); skill tree DAG-acyclic (validated at sign time); milestone predicates must compile against the ECS schema (validated at sign time). Out-of-bounds or invalid templates fail to sign.

14. **Save integration.** Progression state is a typed component bundle on the player entity, saved verbatim by Brief 158's save system. Save migration on schema change (e.g., creator adds a new skill node) is handled by the schema-versioned migration path from Brief 158, with auto-respec on incompatible deltas.

15. **Multiplayer notes.** In v0.3+ multiplayer, progression state is per-player and authoritative on the server (Brief 210); client-side prediction is OFF for progression mutations to prevent rollback ghosts. v0.1 is single-player, so this is a hook only.

16. **v0.1 reach.** All 8 primitives ship at v0.1. The v0.1 limitations are: prestige defers its multiplayer/leaderboard hooks to v0.3, collection's federation share defers to v0.3, narrative_gate's voice-acted unlock notification defers to v0.2 audio. The *typed progression graph itself* ships in full at v0.1.

## Risks identified

1. **Over-typing locks creators in.** A creator who wants a wholly novel progression model may find the 8 primitives constraining. Mitigation: `progression.custom` escape hatch with a typed predicate-action contract; using it requires explicit lineage from `progression.composition.unmodeled` so the substrate can flag it for analytics tooling later.

2. **Cross-primitive interaction is the hard part.** Witcher-style "skill point cost = current level × 1.5" requires reading from xp_level inside skill_tree's currency calculation. Mitigation: the `progression.composition` gseed exposes a typed expression DSL specifically for cross-primitive references, evaluated at sign time, not at runtime.

3. **XP curves drift in balance.** Creators tweak curves repeatedly during development, invalidating prior playthrough saves. Mitigation: progression curves are versioned via Brief 158's schema migration; old saves get a deterministic re-projection onto the new curve.

4. **Skill trees get huge.** Path of Exile's tree has 1,300+ nodes. Mitigation: no hard cap, but the editor (Brief 181) warns past 500 nodes; signed compression for very large trees per Brief 016.

5. **Mastery + cross-skill bleed is hard to balance.** Allowing 10% of mastery xp to spill into adjacent skills creates feedback loops. Mitigation: bleed factor capped at 0.25; balance tooling required to flag if any single mastery exceeds a threshold gain rate.

## Recommendation

Ship the 8-primitive progression vocabulary in `progression.*` with the schemas, bounds, and composition rules above. Mandate that every game ships *at least one* progression primitive, even narrative-only games (which use `progression.milestone + progression.narrative_gate`). Wire balance tooling to read the typed graph directly. Surface the catalog through `progression.find()` to authoring tools (Brief 181) and reuse Brief 164's editor palette pattern.

## Confidence

**4/5.** The 8-primitive decomposition is well-grounded in published RPG/action/sim postmortems and the comparative analysis of shipped titles. Held back from 5 because the `progression.composition` cross-primitive expression DSL is novel and will need a Round 8 implementation pass to confirm it's expressive enough for the long tail of unusual progression designs.

## Spec impact

- Add `progression.*` namespace with 8 primitive sub-namespaces
- Add the 8 typed gseed schemas with parameter bounds
- Add the `progression.composition` gseed for cross-primitive binding
- Cross-link to Brief 158 (save migration), Brief 164 (mechanic refs), Brief 170 (quest narrative gates), Brief 186 (balance tooling consumer)
- Mark the multiplayer-deferred fields in prestige and collection per Finding 16

## New inventions

- **INV-660** Eight-primitive canonical `progression.*` substrate vocabulary
- **INV-661** `progression.composition` typed gseed for cross-primitive binding via signed expression DSL
- **INV-662** Compile-time progression validation: monotonic XP curves, acyclic skill DAG, ECS-compilable milestone predicates
- **INV-663** Auto-pacing introspection from typed progression graph (no instrumentation required)
- **INV-664** Schema-versioned progression migration with deterministic curve re-projection on rebalance

## Open follow-ups

- Long-tail balance presets per genre (Brief 186 takes this)
- Voice-acted unlock notifications (Brief 175 / Brief 220 take this)
- Multiplayer leaderboard integration (Brief 211 takes this)
- Specific recommended XP curves per genre family (Brief 230 cross-genre matrix takes this)

## Sources

1. *Game Mechanics: Advanced Game Design*, Adams & Dormans, ch. on internal economies and progression
2. Path of Exile passive tree retrospective, GGG, GDC 2019 — large skill DAG architecture
3. Hades progression talk, GDC 2020 — heat system + mirror of night composition
4. Stardew Valley postmortem, GDC 2017 — mastery + milestone hybrid
5. Disco Elysium narrative-gate model, ZA/UM design notes, 2019
6. Destiny 2 gear-score tuning, Bungie GDC talk, 2018
7. Witcher 3 design retrospective, CDPR, 2018 — multi-primitive composition
8. *A Theory of Fun*, Raph Koster — pacing-as-mastery framing
9. RuneScape 25-year postmortem, Jagex GDC 2020 — mastery model long-term tuning
10. Brief 092 (this repo) — character power systems
11. Brief 164 (this repo) — mechanic vocabulary that progression unlocks
