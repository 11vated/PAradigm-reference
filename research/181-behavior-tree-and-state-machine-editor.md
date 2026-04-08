# 181 — Behavior tree and state machine editor

## Question
What is the creator-facing editor surface that authors `ai.behavior_tree` and `ai.fsm` (Brief 159) gseeds with debugger integration, breakpoint stepping, and signed lineage on every node edit?

## Why it matters (blast radius)
Behavior trees and state machines are the primary AI authoring surface (Brief 160 archetypes compose them). If the editor cannot debug a live tree against a running game tick, creators cannot diagnose AI behavior. If breakpoints are not first-class lineage events, debug sessions can't be replayed. If the editor surface is separate from Brief 180's dialogue/quest editor, creators learn three node-graph tools.

## What we know from the spec
- Brief 159 — typed FSM, behavior tree node library, GOAP primitives.
- Brief 160 — game AI primitives namespace and 24 archetype templates.
- Brief 152 — fixed-tick scheduler.
- Brief 180 — unified node-graph editor with per-flavor palettes.
- Brief 052 — lineage time machine.

## Findings
1. **Inherits Brief 180's unified node-graph chrome.** This is the third flavor on the same canvas (after dialogue and quest), with a BT/FSM-specific palette. All node-graph editor invariants from Brief 180 (autocomplete, expression DSL, sign-time validation, locale-aware metadata) apply unchanged.
2. **BT node palette.** Per Brief 159: composite (sequence / selector / parallel / random / priority), decorator (inverter / repeater / cooldown / time-limit / blackboard-condition), leaf (action / condition), service (background tick during a subtree). Each is a typed primitive with documented tick semantics.
3. **FSM node palette.** Typed states with entry/update/exit actions, typed transitions with predicate guards, optional substate machines (hierarchical FSM). Brief 159's GOAP primitives appear as a special leaf type that compiles to a planner invocation at runtime.
4. **Blackboard editor.** Both BT and FSM share a typed `ai.blackboard` schema editor — declare keys with types and default values, with sign-time validation that every node referencing a key uses a compatible type.
5. **Live debugger.** When a game is running (in the playtest harness, Brief 185), the editor can attach to a live `ai.behavior_tree.runtime` instance and highlight the currently executing node, the tick path that produced it, and the blackboard state. This is the BT equivalent of Brief 179's animation preview — the editor shows the runtime's actual state, not an approximation.
6. **Breakpoints.** The creator can set a typed `ai.breakpoint` on any node. When the runtime hits the node, the playtest harness pauses at the next tick boundary (Brief 152) and the editor shows the full tree state. Resume / step-into / step-over / continue mirror standard debugger semantics.
7. **Signed debug session.** Every breakpoint hit emits a signed `ai.debug_event` to the lineage. A debug session can be replayed deterministically because the lineage carries the full tick history (Brief 052) and the inputs (Brief 154's signed input recording).
8. **Tree validation.** Sign-time validators per Brief 159: every leaf has a defined action, every condition references a blackboard key that exists, every transition predicate type-checks, every cooldown decorator has a non-negative duration, the tree has no orphan subtrees.
9. **Performance budget.** A typed `ai.budget` per tree declares a max-tick-time-per-instance (default 1ms in Brief 160's archetype templates). Sign-time validation flags trees that obviously exceed the budget (e.g., a sequence with N > 100 leaves). Runtime measurement happens in the playtest harness.
10. **GOAP planner inspection.** When a GOAP leaf fires, the debugger surfaces the goal, the world state precondition vector, the candidate actions considered, and the chosen plan. This makes GOAP debuggable for the first time at substrate level.
11. **Sub-tree referencing.** A BT can reference another BT as a sub-tree, allowing reuse. Sign-time validation rejects circular references. The editor renders sub-tree nodes with a click-to-zoom-in to navigate.
12. **State machine visual layout.** FSM states auto-layout via a force-directed layout algorithm on commit, with manual pin overrides as editor_metadata. Same pattern as Brief 180.

## Risks identified
- **Live attach across federation peers.** Debugging a remote running game is non-trivial. Mitigation: v0.1 supports local-only attach; remote attach deferred to v0.3 with multiplayer.
- **Breakpoint storms in tight loops.** A breakpoint inside a service node ticking every frame would be useless. Mitigation: breakpoints have a typed `hit_condition` predicate (e.g., "only when blackboard.target == player") so they fire selectively.
- **GOAP planner non-determinism.** If the planner's tie-breaking depends on hashmap iteration order, replay could diverge. Mitigation: planner uses a sorted-by-typed-key data structure with documented tie-breaking, signed at the planner gseed level.
- **Tree depth blowup.** Deeply nested BTs with sub-tree refs are hard to read. Mitigation: editor enforces a depth-of-render cap (default 5 levels) with collapse/expand chrome; sign-time depth cap of 16 levels (matching Unreal's BT depth cap).
- **Performance budget false positives.** Static analysis can't catch all O(n^2) BT shapes. Mitigation: sign-time check is heuristic and produces a warning, not a rejection; runtime measurement in the playtest harness is the ground truth.

## Recommendation
Specify the BT/FSM editor as the third flavor of Brief 180's unified node-graph surface, sharing all chrome and conventions. Ship live debugger attach with signed breakpoints, GOAP planner inspection, and the typed blackboard editor at v0.1. Enforce sign-time tree validation (orphan-free, type-safe blackboard, finite cooldowns). Defer remote-peer debug attach to v0.3.

## Confidence
**4.5 / 5.** Behavior tree editing is well-understood (Unreal BT editor, Behavior Designer for Unity, Panda BT, NodeCanvas, Behave). The novelty is the lineage-signed debug events, the GOAP planner inspector, and the unified-node-graph reuse from Brief 180. Lower than 5 because live-attach latency and the GOAP determinism contract need Phase-1 measurement.

## Spec impact
- New spec section: **Behavior tree and FSM editor surface specification**.
- Adds the `ai.breakpoint` typed primitive with hit conditions.
- Adds the `ai.debug_event` lineage entry.
- Adds the `ai.budget` typed primitive declaring per-tree tick-time targets.
- Cross-references Brief 159, Brief 160, Brief 180 for the unified node-graph chrome.

## New inventions
- **INV-739** — Lineage-signed AI debug events: every breakpoint hit, step, and resume emits a signed event so debug sessions are replayable across the substrate.
- **INV-740** — GOAP planner introspection at substrate level: the planner exposes goal, precondition vector, candidate actions, and chosen plan as typed inspection data — making GOAP debuggable for the first time at substrate level.
- **INV-741** — Per-tree typed performance budget with sign-time heuristic + runtime measurement: trees declare an upper-bound tick time, validated heuristically at sign and measured precisely in the playtest harness.
- **INV-742** — Hit-conditioned breakpoints as typed predicates: breakpoints carry a creator-authored guard expression so high-frequency nodes are debuggable without storming.
- **INV-743** — Sub-tree referencing with depth-cap and circular-ref rejection: BTs compose via signed references with sign-time topology validation.

## Open follow-ups
- Remote-peer BT debugger attach (deferred to v0.3).
- Visual diff between two BT versions (deferred to v0.2 — useful but not v0.1-blocking).
- BT-to-utility-AI conversion tooling (deferred to v0.2).
- Auto-generation of BTs from natural language (deferred — this is a Round 8 agent-authoring topic).

## Sources
1. Brief 052 — Lineage-aware time machine.
2. Brief 152 — Game loop and tick model.
3. Brief 154 — Input abstraction (signed input recording).
4. Brief 159 — State machines and behavior trees.
5. Brief 160 — Game AI primitives namespace.
6. Brief 180 — Dialogue and quest editor (unified node-graph chrome).
7. Brief 185 — Playtest harness (forthcoming).
8. Unreal Engine Behavior Tree documentation (docs.unrealengine.com/5/en-US/behavior-trees-in-unreal-engine).
9. Behavior Designer for Unity documentation.
