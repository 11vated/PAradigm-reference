# 170 — Quest and mission patterns

## Question

What canonical quest and mission primitives does GSPL ship in `quest.*` so that any genre can adopt fetch, escort, kill, defend, explore, collect, branching, time-limited, and faction missions by composition rather than from scratch, with quest-as-signed-gseed, deterministic state, and v0.1 reach?

## Why it matters (blast radius)

Quests are the *content unit* most games ship at scale — Witcher 3 has 200+, Skyrim has 300+, MMOs have thousands. Without typed quest primitives, every game reinvents quest state machines, objective tracking, branching logic, and reward delivery, breaking cross-game tooling for localization, balance, and authoring. Brief 165 (progression narrative gates), Brief 169 (loot direct grants), Brief 171 (dialogue triggers and consequences), Brief 174 (HUD quest tracker), Brief 180 (quest editor), Brief 204 (narrative genre family), and Brief 214 (live-ops seasonal content) all consume `quest.*`.

## What we know from the spec

- Brief 153 — ECS substrate; quest state lives in player-side and world-side typed components
- Brief 158 — save/load; quest state is critical save content
- Brief 159 — FSM/HFSM/BT; quest state machines compose Brief 159 primitives
- Brief 165 — progression narrative gates; quests gate progression
- Brief 169 — loot direct grants; quest rewards
- Brief 171 — dialogue is the most common quest trigger and resolution
- Brief 220 — i18n; quest text is the most localized content category

## Findings

1. **`quest.definition` as the root primitive.** A quest is a signed gseed in `quest.definition` with: `quest_id`, `display_name: LocalKey`, `description: LocalKey`, `category: enum{main, side, faction, daily, weekly, hidden, repeatable, world_event}`, `prerequisites: set<predicate>`, `objectives: ordered_set<objective_ref>`, `reward_set: set<grant_ref>`, `failure_conditions: set<predicate>`, `time_limit_ticks: optional<u64>`, `branches: optional<branch_graph>`, `signing_authority`. Quests are typed gseeds with full lineage; forking a quest preserves parent reference.

2. **Eight canonical objective types.** Surveying Witcher 3, Skyrim, Mass Effect, Disco Elysium, FFXIV, WoW, GTA V, and Stardew Valley yields **8 irreducible objective primitives**: `quest.objective.kill`, `quest.objective.fetch`, `quest.objective.escort`, `quest.objective.defend`, `quest.objective.explore`, `quest.objective.collect`, `quest.objective.interact`, `quest.objective.dialogue`. Each is a typed gseed with parameters specific to the kind. Compound objectives (kill 5 wolves *and* deliver pelts to vendor) are composed by the quest's `objectives` ordered set with explicit AND/OR/SEQUENCE wiring in the quest definition.

3. **`quest.objective.kill`.** Parameters: `target_predicate: enemy_query`, `count: u32`, `count_formula: optional<expr>`, `valid_attackers: set<entity_ref>`, `count_only_killing_blow: bool`, `time_limit_ticks`, `progress_event_ref`. Listens to `combat.damage_event` (Brief 167) where target dies and applies the predicate.

4. **`quest.objective.fetch`.** Parameters: `item_predicate: item_query`, `quantity`, `delivery_target: optional<entity_ref>`, `consumed_on_delivery: bool`, `must_be_in_inventory: bool`. Two-phase: collect → deliver. Listens to `loot.grant` and `mechanic.interact.give` (Brief 164).

5. **`quest.objective.escort`.** Parameters: `escortee: entity_ref`, `destination: location_ref`, `path_constraint: optional<path_ref>`, `escortee_health_threshold: f32`, `max_distance_from_player: f32`, `escortee_ai_archetype: ref`. The most failure-prone objective type historically; substrate ships defaults that mitigate (e.g., escortee invulnerable when off-screen, teleport-to-player if too far).

6. **`quest.objective.defend`.** Parameters: `defended_entity_or_zone: ref`, `wave_count: u32`, `wave_composition: encounter_ref` (Brief 168), `success_condition: predicate`, `time_to_survive_ticks`. Wave composition reuses the encounter primitive directly.

7. **`quest.objective.explore`.** Parameters: `target_zone: zone_ref`, `discover_radius: f32`, `must_remain_for_ticks: u32`, `marker_visible: bool`. Triggered by player position trigger volumes (Brief 157).

8. **`quest.objective.collect`.** Parameters: `target_set: set<collectible_ref>`, `min_count`, `max_count`, `partial_credit: bool`, `time_limit_ticks`. Differs from fetch in that targets are world-distributed collectibles (e.g., feathers, audio logs) rather than enemy/container drops.

9. **`quest.objective.interact`.** Generic catch-all. Parameters: `target_predicate: entity_query`, `interact_verb: mechanic_ref` (Brief 164.interact.*), `count: u32`, `unique_targets: bool`. Used for "talk to 5 villagers", "open 3 chests", "press 4 levers".

10. **`quest.objective.dialogue`.** Parameters: `dialogue_node_ref` (Brief 171), `must_select_choice: optional<choice_ref>`, `must_reach_node: optional<node_ref>`, `count: u32`. Listens to dialogue traversal events from Brief 171.

11. **Quest state machine.** Every quest is a typed FSM (Brief 159) with default states `inactive → available → active → completed | failed | abandoned`. Custom states can be added per quest. Transitions are gated by predicates over ECS components and quest objective progress. State changes are signed events (`quest.state_change`) in the per-tick Merkle batch (Brief 153).

12. **Branching.** A quest's `branches` field is a typed DAG: nodes are story states, edges are choice predicates from `quest.objective.dialogue`. The DAG is validated at sign time (no orphans, no cycles, all leaves are terminal states). Branching enables Witcher-style consequence trees and Disco-style choice gardens.

13. **Time-limited and repeatable.** Time limits are tick-counted from `state=active`; the substrate fires `quest.failure` when the limit elapses. Repeatable quests reset their objective progress on completion; the substrate caps repeat count or makes it infinite per the `category` field.

14. **Quest text and localization.** All player-visible strings are `LocalKey` references resolved by Brief 220's i18n pipeline. Quest descriptions can have parametric substitution (`"Kill {count} {enemy_name}"`) with type-checked params. Substrate refuses to sign a quest gseed with unresolved or untyped parameters.

15. **Tracking and HUD.** Each `quest.objective` exposes a typed progress component readable by the HUD (Brief 174). Tracker shows objective name, progress count, optional waypoint marker. Players can pin one quest as primary or none. The substrate ships the typed progress projector at v0.1; the HUD widget is creator-customizable.

16. **Faction quests.** A faction is a typed gseed in `social.faction` (defined here as a sub-namespace, not a separate primitive) with `faction_id`, `reputation_per_player`, `reputation_thresholds`, `relations: set<faction_relation>`. Quests can require/grant faction reputation; `quest.definition.prerequisites` can include "faction X reputation ≥ Y" predicates.

17. **Replay and save.** Quest state is signed and saved verbatim. Branching paths are determined by player choices, which are signed input events (Brief 154). Replays from save are bit-for-bit reproducible.

18. **Multiplayer note.** Shared quests in v0.3+ multiplayer require the server to be the authority on objective progress (Brief 210); v0.1 is single-player so this is a hook. The substrate ships the schema for `quest.shared_progress` at v0.1.

19. **v0.1 reach.** All 8 objective types ship at v0.1. Quest state machine, branching, time limits, factions, localization integration, and HUD tracker all ship. Shared quests defer to v0.3.

## Risks identified

1. **Escort objectives are universally hated.** Built-in mitigations (Finding 5) exist but creators may still ship bad escorts. Mitigation: editor (Brief 180) flags escort objectives with a warning and links to design guidelines.

2. **Branching complexity explodes.** Witcher 3 quests have hundreds of nodes. Mitigation: editor renders the DAG visually (Brief 180); sign-time check warns past 100 nodes per quest.

3. **Localization of parametric strings.** Languages with grammatical case/gender break naive substitution. Mitigation: Brief 220's i18n supports ICU MessageFormat with case/gender; quest substitution uses ICU.

4. **Repeatable quests + economy = farming.** Daily quests with currency rewards are an inflation risk. Mitigation: balance tooling (Brief 186) flags unbounded repeatable rewards as a faucet.

5. **Quest collisions in shared world.** "Kill the chief" can't be completed twice. Mitigation: quest definitions with `category=world_event` fire only once globally; per-player quests use entity instancing.

6. **Time-limited quests in pause-heavy games.** A real-time time limit feels unfair if the game is heavily paused. Mitigation: time limits respect Brief 152 pause-as-first-class state — the timer ticks only in unpaused state by default; per-quest override available.

## Recommendation

Ship the `quest.*` namespace with `quest.definition` root, 8 canonical objective primitives, FSM-based state machine, DAG-based branching, time-limit and faction-reputation predicates, and ICU-MessageFormat localization. Wire to dialogue (Brief 171), enemy encounters (Brief 168), and loot grants (Brief 169) as the canonical quest content sources. Hold shared multiplayer quest progress to v0.3.

## Confidence

**4/5.** Quest primitives are well-grounded in 25+ years of RPG/MMO design and academic narrative game research. Held back from 5 by the branching DAG validation rules, which are novel and may need adjustment after Round 8 implementation feedback.

## Spec impact

- Add `quest.*` namespace with `definition`, `objective.*` (8 sub-types), `state_change` event
- Add `social.faction` sub-namespace
- Add ICU MessageFormat as the canonical parametric string format
- Cross-link to Brief 153 (state component), Brief 158 (save), Brief 159 (FSM), Brief 165 (narrative gate consumer), Brief 167 (kill objective trigger), Brief 168 (defend wave composition), Brief 169 (reward grants), Brief 171 (dialogue), Brief 174 (HUD tracker), Brief 180 (editor), Brief 220 (i18n)
- Mark shared multiplayer quest progress deferred to v0.3

## New inventions

- **INV-685** `quest.definition` as a typed signed gseed with categorized lifecycle and lineage-tracked branching
- **INV-686** Eight canonical objective primitives composing into compound quests via AND/OR/SEQUENCE wiring
- **INV-687** Quest state machine as a Brief 159 FSM with signed `quest.state_change` events in per-tick Merkle batch
- **INV-688** Branching as a sign-time-validated DAG with editor visualization
- **INV-689** Substrate-default escort mitigations (off-screen invulnerability, teleport-to-player) reducing the most failure-prone objective class

## Open follow-ups

- World event coordination across federation peers (deferred to v0.5)
- Quest graph visualization in editor (Brief 180)
- Voice acting attachment to quest dialogue (Brief 175)
- Specific recommended quest density per genre (Brief 230)

## Sources

1. *The Game Narrative Toolbox*, Heussner et al., 2015 — quest structure framework
2. Witcher 3 quest design talk, CDPR GDC 2016 — branching at scale
3. Skyrim Radiant Quest System talk, Bethesda GDC 2012 — quest generation
4. Mass Effect choice system retrospective, BioWare GDC 2014
5. Disco Elysium narrative system talk, ZA/UM, 2019 — heavy branching
6. FFXIV quest tooling talk, Square Enix GDC 2018 — MMO scale quest authoring
7. *Hamlet on the Holodeck*, Janet Murray — branching narrative theory
8. Ink scripting language docs, inkle — typed branching reference
9. ICU MessageFormat specification — i18n parametric strings
10. Brief 159 (this repo) — FSM substrate
11. Brief 220 (this repo, planned) — i18n pipeline
12. Brief 171 (this repo, next) — dialogue substrate
