# 160 — Game AI primitives namespace

## Question

How does GSPL equip the runtime game-AI primitives — pathfinding (A*, navmesh, flow fields), steering (Reynolds boids), perception (vision/hearing cones), group behavior (formation, flocking), and utility AI scoring — as typed substrate primitives that compose under the behavior layer (Brief 159) and inherit signed determinism from the tick model (Brief 152)?

## Why it matters (blast radius)

Runtime game AI is the layer below behavior trees: the *capabilities* a BT or FSM action calls into. "Move to target" needs pathfinding. "Detect player" needs perception. "Follow leader" needs steering. Without typed substrate primitives, every game reinvents A*, every game writes its own perception cone math, every game implements flocking from scratch and gets it slightly wrong. Brief 160 equips the consensus algorithms once, signed and deterministic, so behavior authoring becomes pure composition.

## What we know from the spec

- Brief 159 — behavior trees and FSMs are the layer above; their action leafs call into Brief 160 primitives.
- Brief 156 — physics queries (raycast/shapecast/overlap) underlie perception.
- Brief 152 — fixed tick scheduling for determinism.
- Brief 153 — ECS components for AI state.
- Brief 131 — seven-axis claim; AI state is signed and lineage-tracked.

## Findings

1. **Five canonical AI primitive families ship at v0.1.** Pathfinding, steering, perception, group behavior, utility scoring. Each is a sub-namespace under `ai.*`. All are deterministic on the fixed tick.

2. **Pathfinding: three algorithms ship.** `ai.path.astar` (grid + arbitrary graph), `ai.path.navmesh` (Recast/Detour-class triangle navmesh, 3D-default but works in 2D), `ai.path.flow_field` (Dijkstra-based goal field for many-vs-one chase, RTS-friendly). Selection is per-scene; some scenes use multiple (a navmesh for the world, a flow field for swarm enemies, a grid A* for puzzle entities).

3. **Pathfinding inputs are signed gseeds.** A path query is `ai.path.query` carrying `(start, goal, agent_radius, max_cost, layers, expansion_budget)`. Result is `ai.path.result` carrying `(success, waypoints[], cost, partial_path)`. Queries can be `sync` (block the tick, ≤2ms budget) or `async` (split across N ticks via incremental search).

4. **Steering: ten Reynolds primitives ship.** `seek`, `flee`, `arrive`, `pursue`, `evade`, `wander`, `path_follow`, `obstacle_avoid`, `wall_avoid`, `separation`. Each takes the agent's current state and target parameters and returns a desired velocity vector. Composing steering forces is `weighted_sum` or `prioritized_dither`. This is the canonical Craig Reynolds steering pipeline.

5. **Perception: four sense models ship.** `vision_cone` (FOV angle + range, blocked by physics raycast), `hearing` (radius + decay), `proximity` (sphere overlap), `awareness` (combined model with memory). Each returns signed `ai.perception.detection` gseeds carrying `(perceiver, perceived, sense, confidence, last_seen_position, last_seen_tick)`.

6. **Awareness — the memory primitive.** Per-perceiver memory of detections. An agent who saw the player 3 seconds ago has a "last known position" and a "search box" derived from elapsed time and player movement bounds. This is the consensus stealth-game perception pattern (Splinter Cell, Thief, Hitman) equipped as substrate.

7. **Group behavior: four primitives.** `formation` (positioned slots relative to a leader), `flocking` (Reynolds boid composition), `coordinate` (shared blackboard for group decisions like "two attack, two flank"), `squad_link` (explicit signed group membership with leader/follower roles).

8. **Utility AI: scoring + selection.** `ai.utility.score` is a signed function over the agent's perceived state returning a real-valued score per action option. `ai.utility.select` picks the highest-scoring action with optional softmax randomization. Utility AI is shipped as a flat substrate primitive that BTs and FSMs can call into for "what should I do right now?" decisions when discrete state isn't enough.

9. **AI runs in three update phases.** `perception` phase (early in fixed tick, after physics), `decision` phase (calls into BTs/FSMs from Brief 159 which call into pathfinding/utility), `action` phase (steering writes to physics velocity, animation links fire). Phase ordering is part of Brief 152's topologically-sorted DAG.

10. **Determinism is preserved by sub-seeded RNGs.** Wander, dither, and softmax all use sub-seeded PRNGs from Brief 152's tick seed root. Same scene + same input + same tick = same AI decisions every replay.

11. **Performance budget.** v0.1 budgets the AI namespace at 4ms per fixed tick on the hardware floor for: 100 perceivers running awareness, 50 active path queries (async-amortized), 200 steering composers, 10 squad coordinations. Beyond this, the drift detector emits `ai.budget.breach`.

12. **AI navmesh authoring.** v0.1 ships substrate primitives but defers visual navmesh editing to Tier C Brief 177 (scene editor) and to Tier B Brief 173 (procedural generation) — navmeshes auto-generate from tilemaps and from 3D scene geometry on save. Hand-painted navmesh regions are creator overrides.

13. **Anti-frustration AI patterns ship as named primitives.** `ai.fairness.rubber_band` (rubber-banding for racing AI), `ai.fairness.miss_first_shot` (NPC misses on first encounter to give player reaction time), `ai.fairness.dramatic_pause` (boss telegraphs by waiting), `ai.fairness.assist` (off-screen aim assist for shooters). These are explicit, signed, opt-in. Players who want the "honest" experience can opt out of fairness primitives via accessibility settings.

14. **Differentiable AI parameters.** Agent behavior parameters (perception ranges, steering weights, utility curve shapes) tuned by creators and accepted via Brief 144 drift detector become genre-default suggestions for new projects of the same archetype. Per-genre AI starter packs propagate via federation.

## Risks identified

- **Navmesh generation from arbitrary 3D geometry is non-trivial and error-prone.** Mitigation: ship Recast/Detour as the canonical generator (well-validated); creators can override per region.
- **A* on large grids can dominate the AI budget.** Mitigation: hierarchical pathfinding (HPA*) for grids ≥ 256² ships at v0.2; v0.1 documents the ceiling.
- **Boid composition can produce visible artifacts at scale (>500 boids).** Mitigation: spatial hashing for neighbor query; optimization brief in Tier G Brief 222.
- **Anti-frustration "fairness" primitives can feel patronizing if undisclosed.** Mitigation: every fairness primitive that fires emits a signed gseed; creators can surface "AI assist active" UI as needed; constitutional courtesy.
- **Utility AI score functions can be hard to author by hand.** Mitigation: ship 12 starter scoring templates; visual editor for curve composition in Tier C.

## Recommendation

**GSPL ships an `ai` namespace at v0.1 with five primitive families: pathfinding (A*, navmesh, flow_field), steering (10 Reynolds primitives), perception (4 sense models with awareness/memory), group behavior (formation, flocking, coordinate, squad_link), and utility AI (scoring + selection). All primitives run on the fixed tick in three phases (perception/decision/action), use sub-seeded PRNGs for determinism, return signed gseeds for queries and detections, budget at 4ms for 100 perceivers + 50 paths + 200 steerings + 10 squads on the hardware floor, ship four named anti-frustration "fairness" primitives as opt-in, and propagate creator-tuned parameters via the Differentiable axis.**

## Confidence

**4/5.** All five families are decades-old proven patterns (Reynolds boids, Recast/Detour navmesh, hierarchical pathfinding, utility AI from Mat Buckland and Dave Mark). The novel composition is binding them all under one signed namespace with deterministic sub-seeded PRNGs. The 5th confidence point waits on the Brief 134 canonical battery measuring 100-perceiver awareness on the hardware floor.

## Spec impact

- `gspl-reference/namespaces/ai.md` — new namespace: `ai.path.*`, `ai.steer.*`, `ai.perception.*`, `ai.group.*`, `ai.utility.*`, `ai.fairness.*`
- `gspl-reference/research/152-game-loop-tick-model-namespace.md` — perception/decision/action phase ordering
- `gspl-reference/research/153-ecs-substrate-binding.md` — `ai.perceiver`, `ai.steering`, `ai.path.agent` components
- `gspl-reference/research/156-physics-integration-2d-and-3d.md` — perception uses physics raycast/shapecast
- `gspl-reference/research/159-state-machines-and-behavior-trees.md` — BT/FSM action leafs call into ai.* primitives
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — AI battery: 100 perceivers + 50 paths + 200 steerings at 60Hz
- Tier B Brief 168 (enemy taxonomies) — uses `ai.fairness.*` primitives
- Tier B Brief 173 (procedural generation) — emits navmesh data alongside tilemap data

## New inventions

- **INV-635** — *Five-family unified AI primitive namespace* with consistent phase ordering and signed query/result gseeds, eliminating per-game reinventions of A*, perception, steering, flocking, and utility scoring.
- **INV-636** — *`ai.awareness` perception with memory* equipped as substrate — last-known-position + time-decay + search-box generation for stealth-game patterns at zero per-game implementation cost.
- **INV-637** — *Sub-seeded PRNGs for AI randomness* preserving fixed-tick determinism while enabling wander, dither, and softmax selection.
- **INV-638** — *Four named anti-frustration `ai.fairness.*` primitives* (rubber_band, miss_first_shot, dramatic_pause, assist) shipped as explicit, signed, opt-in substrate primitives — surfacing what other engines hide in per-game scripts.
- **INV-639** — *Async path query budget split* — incremental A*/navmesh search across N ticks, surfacing path completion as a signed event rather than blocking the tick.

## Open follow-ups

- Hierarchical pathfinding (HPA*) ship date — v0.1 vs v0.2 (provisional v0.2; v0.1 documents the grid-size ceiling).
- Whether learned policy primitives (RL-trained agents) ship at v0.1 — provisional no; defer to Round 8 with the Brief 143 LoRA path.
- LLM-driven NPC dialogue/decision integration — its own Round 8 tier per Round 7 plan; Brief 160 stays mechanical.

## Sources

- Brief 131 — seven-axis structural claim
- Brief 134 — substrate-native benchmark battery
- Brief 143 — differentiable action learning recipe
- Brief 144 — drift detector threshold calibration
- Brief 152 — game loop and tick model namespace
- Brief 153 — ECS substrate binding
- Brief 156 — physics integration 2D and 3D
- Brief 159 — state machines and behavior trees
- Craig Reynolds, "Steering Behaviors For Autonomous Characters"
- Mat Buckland, "Programming Game AI by Example"
- Dave Mark, "Behavioral Mathematics for Game AI" (utility AI canonical reference)
- Mikko Mononen, Recast and Detour (navmesh generator + runtime)
- Adi Botea et al., Hierarchical Path-Finding (HPA*)
- Damian Isla, "Halo 3 AI: Building a Better Battle"
