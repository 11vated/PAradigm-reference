# 203 — Tactics and strategy genre recipe

## Question
What is the typed genre composition recipe that produces a complete signed turn-based tactics or real-time strategy gseed bundle (Fire Emblem / XCOM / Into the Breach / Advance Wars / RTS-class) from substrate primitives, with grid-based movement, action-point economies, and AI opponents?

## Why it matters (blast radius)
Tactics and strategy games are the canonical proving ground for typed AI decision-making at scale, grid-based deterministic movement, and action-economy enforcement. A working recipe demonstrates the substrate's BT/FSM library (Brief 159) and GOAP planner (Brief 181) compose into believable AI opponents from typed primitives.

## What we know from the spec
- Brief 159 — state machines / behavior trees / GOAP.
- Brief 173 — tilemap (grid).
- Brief 181 — BT/FSM editor with GOAP introspection.
- Brief 198 — top-down RPG recipe (combat FSM precedent).
- Briefs 197-202 — recipe template precedent.

## Findings
1. **Recipe inherits frame.**
2. **Required primitives.** `tilemap.layer` (battle grid), `entity.archetype` (units), `stats.sheet` (HP, attack, defense, movement, range), `behavior.tree` or GOAP planner (enemy AI), `state.machine` (turn FSM), `inventory.container` (unit equipment, optional), `ui.element` (action menu, unit info, grid overlay), `audio.bus`, `vfx.system`.
3. **Grid movement.** Units move on `tilemap.layer` cells. Movement is a typed `unit.move` mutation with cost = path length × movement-point cost. A* pathfinding ships as substrate-provided. Sign-time validates the grid is non-empty.
4. **Action economy.** Each unit has typed action points per turn (default 2: move + action). Recipe declares the action-economy schema; validator gates that units have at least one declared action.
5. **Turn FSM.** Player-turn-start → Player-actions → Player-turn-end → Enemy-turn-start → Enemy-actions → Enemy-turn-end → Player-turn-start. Multi-faction support via typed `faction.id` field.
6. **Enemy AI: BT or GOAP.** Sub-recipes select. Simple sub-recipes (Advance Wars) use BT with priority list (attack-weakest, capture-objective, retreat). Complex sub-recipes (XCOM) use GOAP with typed action library (move-to-cover, shoot, overwatch, grenade, retreat).
7. **Fog of war.** Optional typed field on unit `vision.range`. Cells outside any allied unit's vision render dimmed. Determinism: visibility recomputes on every turn-end mutation.
8. **Sub-recipes.** Fire-Emblem-style (grid + unit roster + permadeath optional), XCOM-style (cover system + percentage hit chance + GOAP enemies), Into-the-Breach-style (deterministic puzzle-tactics with full enemy intent telegraphing), Advance-Wars-style (fog + production + capture), Real-time-strategy (Brief 209 multiplayer for full RTS; single-player skirmish in v0.1).
9. **Deterministic hit chance.** XCOM-style hit rolls draw from sub-seeded PRNG per Brief 162; replays reproduce identical roll sequences. Critical for community trust ("RNG screwed me, prove it").
10. **Validation contract.** Sign-time gates: at least one tilemap layer, at least one unit archetype with stats.sheet, action economy declared, turn FSM present, at least one AI behavior (BT or GOAP), faction count ≥ 2.

## Risks identified
- **GOAP planner cost.** GOAP can be expensive at scale. Mitigation: per-tree typed performance budget per Brief 181; substrate-provided GOAP solver caps planning depth.
- **Pathfinding cost.** A* on large grids is expensive. Mitigation: substrate provides JPS+ optimization for grid pathfinding; budget per turn typed and surfaced.
- **Hit-chance UI complexity.** Showing percentage chances honestly is hard (RNG bias, anti-frustration features). Mitigation: substrate provides typed hit-chance display with creator opt-in for cosmetic anti-frustration; lineage records the actual roll regardless.
- **Multi-faction balancing.** Not the substrate's job; document in recipe open follow-ups.
- **RTS in single-player.** Real-time strategy is much harder than turn-based. Mitigation: v0.1 ships only single-player skirmish RTS; full RTS lands in v0.3 with multiplayer.

## Recommendation
Specify the tactics and strategy recipe as a `recipe.gseed` with grid movement primitives, typed action economy, turn FSM with multi-faction support, BT or GOAP enemy AI selection, optional fog-of-war and cover systems, deterministic hit-chance with lineage recording, and five sub-recipes. Default sub-recipe instantiation (Advance-Wars-style) produces a playable single-player tactics game.

## Confidence
**4 / 5.** Tactics mechanics are well-precedented; the novelty is the typed action economy and the GOAP/BT sub-recipe selection pattern. Lower than 4.5 because GOAP planner cost and hit-chance UI need Phase-1 validation.

## Spec impact
- New spec section: **Tactics and strategy genre recipe specification**.
- Adds typed `unit.move` mutation, action-economy schema, faction.id field.
- Adds A* / JPS+ pathfinding as substrate-provided.
- Adds the GOAP/BT sub-recipe AI selection pattern.
- Cross-references Briefs 159, 162, 173, 181, 197.

## New inventions
- **INV-849** — Typed action economy schema with sign-time validation: action points per turn are a typed substrate field with creator-tunable defaults.
- **INV-850** — A* / JPS+ grid pathfinding as substrate-shipped primitive with typed per-turn cost budget: pathfinding is not creator code.
- **INV-851** — GOAP-vs-BT sub-recipe selection pattern: AI complexity scales with sub-recipe choice; substrate provides both engines and creators select.
- **INV-852** — Deterministic hit-chance with lineage-recorded roll sequence: RNG-based mechanics produce verifiable post-hoc explanations of every roll.
- **INV-853** — Multi-faction typed `faction.id` field with turn FSM faction iteration: substrate enforces structural multi-faction support, not per-recipe code.

## Open follow-ups
- RTS multiplayer (Brief 209) — v0.3.
- Procedural map generation for tactics — deferred to v0.3.
- Permadeath replay verification (Fire Emblem Ironman mode) — Phase 1.
- Anti-frustration RNG bias documentation — deferred to v0.2.

## Sources
1. Brief 159 — State machines and behavior trees.
2. Brief 162 — VFX with deterministic seeds.
3. Brief 173 — Tilemap autotile.
4. Brief 181 — BT/FSM editor.
5. Brief 197 — 2D platformer recipe.
6. XCOM postmortem — Firaxis.
7. Into the Breach design talks — Subset Games.
8. Fire Emblem GDC talks.
9. JPS+ pathfinding paper — Daniel Harabor.
