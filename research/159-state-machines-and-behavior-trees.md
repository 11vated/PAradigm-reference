# 159 — State machines and behavior trees

## Question

How does GSPL equip the universal behavior-authoring primitives — finite state machines, hierarchical state machines, behavior trees, GOAP — as typed substrate namespaces where every state, transition, and BT node is a signed gseed with replay-deterministic execution and lineage from decision to outcome?

## Why it matters (blast radius)

State machines and behavior trees are the dominant patterns for game logic — character controllers (FSM), NPC AI (BT or HFSM), boss fight choreography (HFSM), quest progression (FSM), UI mode dispatch (FSM), tutorial sequencing (FSM). Without typed substrate primitives, every game reinvents the dispatch logic and accumulates per-game bugs at state boundaries. Tier B briefs (164-176) all assume creators have a coherent way to express "do this until that, then do the other thing." Brief 159 specifies it.

## What we know from the spec

- Brief 153 — ECS components include `ai.state` placeholder; Brief 159 fills it.
- Brief 152 — fixed tick scheduling; state evaluations run on the fixed tick.
- Brief 131 — seven-axis claim; states and transitions are signed.
- Brief 128 — four-layer action space; state-machine and BT node libraries are level-3 (composed action) primitives.

## Findings

1. **Three behavior-authoring primitives ship at v0.1: FSM, HFSM, BT.** GOAP (goal-oriented action planning) ships substrate hooks but no first-class authoring at v0.1 — defer GOAP UI to Round 8. The three v0.1 primitives cover ~95% of v0.1 starter-genre needs.

2. **A finite state machine is a signed gseed in `behavior.fsm`.** Schema: `(name, states[], initial_state, transitions[], on_enter_actions, on_exit_actions, on_tick_actions)`. States and transitions are sub-gseeds; transitions carry `(from, to, condition_expression, priority)`.

3. **A hierarchical state machine wraps FSMs.** A state can itself contain a child FSM (a "super-state"). Entering a super-state activates its initial child; exiting deactivates the entire child tree. This is the consensus HFSM pattern from Harel Statecharts and is well-known in game AI literature.

4. **A behavior tree is a signed gseed in `behavior.bt`.** Schema: `(name, root_node, blackboard_schema)`. Nodes are sub-gseeds with one of seven canonical types: `selector`, `sequence`, `parallel`, `inverter`, `condition`, `action`, `decorator`. Each carries its own typed parameters. Per-tick evaluation returns one of `success`, `failure`, `running`.

5. **Conditions and action-leafs reference ECS components.** Conditions like "is enemy in range" are signed `behavior.condition` gseeds that read the ECS state. Action leafs like "move to position" are signed `behavior.action` gseeds that mutate ECS state via the same dispatch surface as Brief 128's primitive tools. This makes behavior authoring composable with the substrate's action space, not parallel to it.

6. **Blackboards are signed and per-instance.** A blackboard is a typed key-value gseed that a BT instance reads and writes. Schema is declared on the BT definition; instances carry signed blackboards. Blackboard mutations are diff-tracked for replay (same Merkle batching as ECS in Brief 153).

7. **State transitions and BT decisions are lineage-tracked.** When an FSM transitions or a BT picks a branch, the resulting decision is a signed gseed with parent lineage to the conditions that caused it. Creators debugging "why did the boss go into rage mode?" traverse the lineage to the conditions that fired. Brief 131 Lineage axis at the behavior boundary.

8. **The visual editor is Tier C Brief 181, not this brief.** This brief specifies the data substrate; the editor is a separate brief. Both feed the same signed gseed schema so visual edits and code edits are interchangeable.

9. **Animation integration via `behavior.animation_link`.** A state can declare an animation it plays on enter and a transition out of an animation event (e.g., "exit attack state on attack-end animation event"). The link is signed and read by the animation runtime (Brief 161). This is the structural way animation and state stay in sync without per-game glue code.

10. **Determinism comes from fixed-tick evaluation.** All state evaluations and BT ticks run on the fixed update phase (Brief 152). Within a tick, the topological sort orders behavior systems after input and physics but before animation and rendering. Same input + same state = same transitions every replay.

11. **Performance.** v0.1 budgets behavior evaluation at 1ms per fixed tick for 100 active behavior instances on the hardware floor. BT evaluation is shallow-cached: nodes that returned `running` last tick start their evaluation from the resumed point, not the root.

12. **Reusable behavior libraries — typed and shareable.** Common patterns ship as canonical signed BTs: `patrol_then_chase`, `flee_when_low_health`, `cover_seek_and_fire`, `distance_keeper`, `circle_strafe`, `ambush_from_hiding`, `coordinate_with_allies`. Creators import these as starting points and customize via overrides. Federation propagation via Brief 147.

13. **GOAP substrate hooks (deferred UI).** The substrate reserves the `behavior.goap` namespace for v0.2+: a goal carries `(name, precondition_set, satisfaction_check)`; an action carries `(name, preconditions, effects, cost)`; a planner finds an action sequence at runtime. v0.1 signs the schemas but doesn't ship the planner UI; programmers can use it directly via the action space.

14. **Differentiable behavior selection.** Per Brief 143, accepted-outcome BT and FSM patterns become positive training signals; rolled-back patterns become negative. Genre-default behavior libraries get promoted via the same mechanism as control schemes (Brief 154) and camera defaults (Brief 155).

## Risks identified

- **BT evaluation can be expensive for deep trees.** Mitigation: shallow-cache resumed `running` nodes; depth ceiling of 32 with warning at 24; profiler in Brief 217 surfaces hot paths.
- **HFSM can lead to "state explosion" if not authored carefully.** Mitigation: scene-compile warns when an HFSM has more than 50 transitions or more than 20 leaf states; soft cap, not enforced.
- **Mixing FSM and BT in the same character is a common confusion.** Mitigation: a single ECS entity has either a `behavior.fsm` or `behavior.bt` component, not both. Creators wanting hybrid patterns nest one inside the other (BT action node that runs an FSM, or FSM state that runs a BT) — explicit composition, not implicit mix.
- **GOAP substrate without UI may invite half-implementations.** Mitigation: the schema is reserved but inert at v0.1; creators using it accept it's a programmer-only path until v0.2+.

## Recommendation

**GSPL ships `behavior.fsm`, `behavior.hfsm`, and `behavior.bt` namespaces at v0.1 with signed states/transitions/nodes, blackboards as typed gseeds with diff tracking, condition and action leafs that read/write ECS via the action space, lineage from decision to outcome, animation integration via signed `behavior.animation_link`, fixed-tick deterministic evaluation, shallow-cache for resumed BT nodes, ~7 canonical reusable behavior libraries shipped as starter templates, GOAP substrate hooks reserved but UI deferred, and federation-promoted genre-default behavior libraries via the Differentiable axis.**

## Confidence

**4/5.** FSM, HFSM, and BT are decades-old proven patterns from game AI literature (Damian Isla "Halo 3 BT" GDC, Pixelberry "Choices" FSM patterns, Harel Statecharts). Composing them on the substrate's signed action space is the only novel piece and follows directly from Brief 128.

## Spec impact

- `gspl-reference/namespaces/behavior.md` — new namespace: `behavior.fsm`, `behavior.hfsm`, `behavior.bt`, `behavior.condition`, `behavior.action`, `behavior.blackboard`, `behavior.animation_link`, `behavior.goap` (reserved)
- `gspl-reference/research/152-game-loop-tick-model-namespace.md` — behavior phase is between input/physics and animation/render
- `gspl-reference/research/153-ecs-substrate-binding.md` — `behavior.fsm` and `behavior.bt` ECS components
- `gspl-reference/research/128-gspl-tool-use-and-modifier-surface.md` — behavior leaves are level-3 composed actions
- `gspl-reference/research/161-animation-runtime-namespace.md` (next-next brief) — `behavior.animation_link` integration point
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — behavior battery: 100 active behaviors at 60 Hz, FSM transition correctness, BT shallow-cache correctness
- Tier C Brief 181 — visual editor reads/writes the same gseed schema

## New inventions

- **INV-630** — *Three-primitive behavior substrate* (FSM/HFSM/BT) with a single shared schema for conditions and actions reading from ECS and writing through the action space.
- **INV-631** — *Signed `behavior.animation_link`* — animation plays and animation events trigger transitions through a typed link, not per-game glue code, eliminating an entire class of state/animation desync bug.
- **INV-632** — *BT shallow-cache* on resumed `running` nodes — cuts behavior evaluation cost dramatically for the common case where most nodes don't change between ticks.
- **INV-633** — *Seven canonical reusable behavior libraries* shipped as signed templates and competing for genre-default promotion via Brief 143's Differentiable axis.
- **INV-634** — *GOAP substrate reservation* — the namespace and schemas exist at v0.1 even though the planner UI is v0.2+, preventing creator-built parallel implementations from forking the substrate.

## Open follow-ups

- Whether the substrate ships utility-AI (weighted-evaluator) as a fourth primitive at v0.1 or v0.2 (provisional v0.2, after creator feedback on FSM/BT coverage).
- Whether visual BT editor ships at v0.1 or v0.2 (Tier C Brief 181 covers; provisional v0.1 ship, simplified UI).
- Whether multi-character coordination (squad-level BT) needs a fifth primitive (defer to Round 8).

## Sources

- Brief 128 — GSPL tool-use and modifier-surface intelligence
- Brief 131 — seven-axis structural claim
- Brief 134 — substrate-native benchmark battery
- Brief 143 — differentiable action learning recipe
- Brief 147 — federation-wide adapter review protocol
- Brief 152 — game loop and tick model namespace
- Brief 153 — ECS substrate binding
- Damian Isla, "Handling Complexity in the Halo 2 AI" (canonical BT for game AI)
- David Harel, "Statecharts: A Visual Formalism for Complex Systems" (HFSM)
- Jeff Orkin, "Three States and a Plan: The AI of F.E.A.R." (GOAP reference)
- Bobby Anguelov, "Behavior Trees: A Practical Approach"
