# 205 — Simulation and management genre recipe

## Question
What is the typed genre composition recipe that produces a complete signed simulation or management game gseed bundle (Stardew Valley / Factorio / RollerCoaster Tycoon / Two Point Hospital / Animal Crossing class) from substrate primitives, with economy loops, time progression, agent simulation, and persistent world state?

## Why it matters (blast radius)
Simulation and management games are the largest single revenue category outside live-service multiplayer (Factorio sold 4M+ copies, Stardew sold 30M+). They are the canonical proving ground for typed economy systems and persistent world state at scale — the substrate's economic-loop and large-state-graph stress test.

## What we know from the spec
- Brief 159 — state machines / behavior trees.
- Brief 158 — save snapshot model.
- Brief 175 — procgen library.
- Briefs 197-204 — recipe template precedent.

## Findings
1. **Recipe inherits frame.**
2. **Required primitives.** `entity.archetype` (player + NPCs + buildings + resources), `behavior.tree` (NPC schedules), `inventory.container` (resources), `item.def`, `economy.flow` (typed input → process → output recipe), `time.calendar` (typed in-game clock), `world.tile` (the persistent grid), `save.snapshot` (heavy use), `quest.graph` (optional progression goals), `ui.element` (build menu / inventory / map / journal), `audio.bus`, `vfx.system`.
3. **Time calendar.** `time.calendar` is a typed gseed declaring: tick rate (real-seconds per game-minute), day length, season length, year length, day-night cycle, weather schedule. Defaults: 1 real second = 1 game minute, 24-minute day, 28-day season, 4 seasons.
4. **Economy flow primitive.** `economy.flow` declares: typed input items, processing time, typed output items, machine type (manual / automated / building). Validator gates that flows form valid graphs (no impossible recipes). Inspired by Factorio's recipe graph but generalized.
5. **NPC schedules.** NPCs have typed `daily.schedule` fields binding time ranges to BT subtrees. NPCs deterministically follow their schedule, mutated by quest events. Stardew NPC schedule fidelity.
6. **World tile state.** Persistent world is `world.tile[]` with each tile having typed terrain, building, growth state, owner. Save.snapshot chunks tiles by spatial region per Brief 158.
7. **Building placement.** Player builds via typed `world.tile.place_building` mutation; building referenced from `building.def` library. Sign-time validates buildings have valid economy flows where applicable.
8. **Sub-recipes.** Stardew-style (farming + dialogue, layered with Brief 204), Factorio-style (heavy economy graph + automation), RollerCoaster-Tycoon-style (entertainment economy + visitor agent simulation), Two-Point-Hospital-style (service economy + staff scheduling), Animal-Crossing-style (slow social sim + collection).
9. **Save bloat handling.** Long-term play balloons save state. Mitigation: per-region chunk save (Brief 158), with archived chunks compressed to summary form for unvisited regions.
10. **Validation contract.** Sign-time gates: `time.calendar` present, at least one `economy.flow` OR `quest.graph` (sims need economic loop or progression loop), at least one `world.tile`-based persistent state, save chunking declared.

## Risks identified
- **Save bloat.** Long-term saves can hit MB scale. Mitigation: per-region chunking; sign-time warning when un-chunked save state exceeds threshold.
- **Economy graph cycles.** Recipes can form impossible cycles. Mitigation: validator detects cycles in `economy.flow` graph and surfaces as typed errors.
- **NPC schedule pathing cost.** Many NPCs deterministically pathfinding through a grid is expensive. Mitigation: substrate provides cached path lookups for repeated NPC routes.
- **Tick rate vs frame rate.** Sims often tick at fixed rate independent of render frame rate. Mitigation: substrate provides typed `tick.rate` field with fixed-timestep tick loop separate from render loop.

## Recommendation
Specify the simulation and management recipe as a `recipe.gseed` with typed `time.calendar`, `economy.flow`, `world.tile`, and `daily.schedule` primitives, fixed-timestep tick loop separate from render, per-region save chunking, economy graph cycle validation, and five sub-recipes. Default sub-recipe (Stardew-style, layered with Brief 204) produces a playable farming sim.

## Confidence
**4 / 5.** Sim mechanics are well-precedented; the novelty is the typed `economy.flow` primitive and the time.calendar substrate field. Lower than 4.5 because long-term save bloat and NPC schedule pathing cost need Phase-1 measurement.

## Spec impact
- New spec section: **Simulation and management genre recipe specification**.
- Adds typed `time.calendar`, `economy.flow`, `world.tile`, `daily.schedule`, `building.def` gseed kinds.
- Adds the fixed-timestep tick loop separate from render contract.
- Cross-references Briefs 158, 159, 175, 197, 204.

## New inventions
- **INV-859** — Typed `economy.flow` recipe-graph primitive with cycle detection: economy systems are first-class typed gseeds with structural validity gates.
- **INV-860** — Typed `time.calendar` with creator-tunable tick / day / season / year fields: in-game time is a substrate primitive, not per-game implementation.
- **INV-861** — Typed `daily.schedule` binding time ranges to BT subtrees: NPC behavior over time is structured composition, not opaque scripts.
- **INV-862** — Per-region save chunking with archived-summary compression for unvisited regions: long-term sim saves stay bounded as a substrate-provided pattern.
- **INV-863** — Fixed-timestep tick loop separate from render frame rate: substrate enforces structural separation enabling deterministic sim regardless of frame rate.

## Open follow-ups
- Multiplayer sim (Stardew co-op, Factorio multiplayer) — deferred to v0.3 with Brief 209.
- Dynamic economy balancing — deferred to v0.4.
- Procedural NPC generation — deferred to v0.4.
- Historical state queries (rewind sim N days) — deferred to v0.4.

## Sources
1. Brief 158 — Save snapshot model.
2. Brief 159 — State machines and behavior trees.
3. Brief 175 — Procgen library.
4. Brief 197 — 2D platformer recipe.
5. Brief 204 — Narrative recipe.
6. Stardew Valley postmortem — ConcernedApe.
7. Factorio Friday Facts blog (factorio.com/blog).
8. RollerCoaster Tycoon source code analysis.
