# 152 — Game loop and tick model namespace

## Question

How does GSPL equip the universal game-loop and tick-model primitives — fixed vs variable timestep, frame budgeting, deterministic scheduling, pause/resume/serialize — as a typed substrate namespace that every Round 7 tier A-H can sit on?

## Why it matters (blast radius)

The game loop is the heartbeat every other system composes against. If the tick model isn't signed, typed, and rollback-able from day one, every downstream system (physics, AI, animation, particles, networking) inherits the wrong properties: non-determinism, replay divergence, save-state corruption, frame-budget bleed. Round 6.5 Brief 149 froze v0.1 on 2D creative workflows; Brief 152 is the first brief that gives those workflows a *runtime heartbeat*, so every subsequent Tier A brief (153-163) inherits a coherent scheduling and frame-lifecycle contract.

## What we know from the spec

- Round 2 Brief 020 defines the determinism contract per engine.
- Round 2 Brief 025 defines the renderer determinism contract.
- Round 2 Brief 026 defines the deterministic kernel implementation.
- Brief 131 establishes the Rollback-able axis — any tick must be rewindable.
- Brief 149 freezes v0.1 scope, which includes deterministic mode for sprite/image workflows.
- Round 4 measured-world primitives assume a fixed-Δt integrator exists to drive them.

## Findings

1. **Three canonical tick models ship, not one.** Fixed timestep (deterministic, required for physics/networking/replay), variable timestep (smooth rendering, required for camera/UI), and hybrid fixed-update-with-interpolation (the Glenn Fiedler "Fix Your Timestep" pattern). All three are typed namespace members; creators select per-scene via a signed `tick.mode` gseed.

2. **The fixed step is the default; variable is opt-in per system.** Physics, networking, AI decisions, save-state capture all run on the fixed tick. Rendering, input polling, UI, and camera-smoothing run on the variable tick with accumulator-based interpolation. This mirrors Unity's `FixedUpdate`/`Update`/`LateUpdate` and Unreal's `Tick`/`AsyncPhysicsTick` split but signs the boundary between them.

3. **Default fixed step is 60 Hz (16.666ms); hard range 20-240 Hz.** 60 Hz matches the default of Godot, Unity, Unreal, Phaser, and the hardware display rate on the majority of v0.1 target machines. A creator can override per-scene within 20-240 Hz; below 20 introduces perceptible latency, above 240 explodes compute without meaningful benefit for 2D.

4. **Frame budget is signed per scene.** Each scene declares a frame budget gseed (`frame.budget`) with per-phase targets: input (0.5ms), fixed-update (5ms), variable-update (3ms), render (6ms), reserved (2ms) = 16.666ms at 60 Hz. The budget is *enforced*, not advisory — a phase that exceeds its target emits a signed `frame.budget.breach` gseed that feeds the drift detector (Brief 144).

5. **Deterministic scheduling uses a single-source-of-truth PRNG per tick.** Each fixed tick is seeded from a signed rolling seed derived from `(scene_seed, tick_number, namespace)`. Any system that needs randomness asks the tick scheduler for a sub-seed; no system holds a private RNG. This gives bit-identical replay across runs and across machines.

6. **Pause is a first-class state, not a side effect.** Pause sets `tick.mode` to `paused`; all fixed-update phases halt; variable-update continues (for UI animation, menus). Resume replays the exact tick index from save without drift. "Background pause" (app loses focus) is an implicit signed pause gseed.

7. **Serialize/resume are derived from tick-level lineage.** Because every fixed tick is a signed gseed carrying the scheduler state, save/load (Brief 158) is just "pick a tick and start from there." This is the structural reason the Rollback-able axis extends to game loops: every tick is a checkpoint by construction.

8. **Time dilation and slow-motion are typed modifiers, not hacks.** A `tick.time_scale` gseed multiplies Δt for the fixed integrator (e.g., 0.1 for bullet-time, 2.0 for fast-forward, -1.0 for reverse-replay). Systems that must not slow down (UI, audio-ducking envelopes) read `tick.real_delta` instead. The distinction is declared in system metadata, not inferred.

9. **Multi-world and multi-scene tick isolation.** A scene can host sub-worlds (e.g., a mini-game inside a room, a dream sequence, a physics sandbox preview) that run on independent tick schedulers. Each sub-world is a child gseed with its own `tick.mode`, `tick.hz`, `frame.budget`, and PRNG seed, but shares the parent's wall-clock.

10. **Frame-skip and frame-drop policies are explicit.** Under load, the scheduler can either: (a) *catch up* — run multiple fixed-updates per render frame until the accumulator drains, (b) *drop* — skip fixed-updates and resync the accumulator, (c) *freeze* — slow the wall-clock to keep all ticks. Default is (a) with a max-catch-up of 5 ticks per frame (the Glenn Fiedler recommendation); creators can override per scene. Each policy is a signed `tick.overload_policy` gseed value.

11. **Fixed-update ordering is topologically sorted from system dependencies.** Each system declares what it reads and writes (e.g., physics writes transforms; AI reads transforms; animation reads transforms and writes visual-only). The scheduler topologically sorts the system DAG once per scene-load and reuses the order for every tick. Cyclic dependencies are refused at scene-compile time with a signed `tick.cycle.detected` error gseed.

12. **Networking hooks are built into the tick, not bolted on.** Even at v0.1 (Tier F deferred), every fixed tick records `(tick_number, input_hash, state_hash)`. A creator who later adds multiplayer via Tier F Brief 209 gets rollback-netcode-ready ticks for free because the recording format never changes.

13. **The tick scheduler itself is a gseed.** Not a hard-coded engine component — creators can subclass the default scheduler with a signed custom scheduler (for e.g. energy-saving mobile builds, deterministic-replay-only mode, time-travel debugging mode). Custom schedulers must pass the canonical tick battery (Brief 134) to be publishable to federation.

## Risks identified

- **60 Hz default may not match high-refresh-rate displays (144, 240 Hz).** Mitigation: variable-update runs at display rate; fixed-update stays at 60 Hz; interpolation fills the gap. Tested in the parity test suite per Brief 196.
- **Topological sort may not fit certain creator patterns (chained post-processing).** Mitigation: ordered "phases" inside a tick let creators declare sub-phase ordering explicitly; the sort resolves within a phase.
- **Time-scale + fixed-step interaction can desync audio.** Mitigation: audio runtime (Brief 163) reads `tick.real_delta` by default; creators opt into scaled audio per-source with a signed flag.
- **Multi-world PRNG seeding can collide if creators reuse scene seeds.** Mitigation: sub-world seeds derived from `hash(parent_seed, child_name)` so siblings diverge deterministically.
- **Catch-up policy can cause "spiral of death" on sustained overload.** Mitigation: the 5-tick ceiling is hard; past that, the scheduler switches to drop-mode and emits a signed `tick.overload.spiral` gseed to telemetry.

## Recommendation

**GSPL ships a `tick` namespace at v0.1 with three canonical modes (fixed / variable / hybrid), 60 Hz default fixed rate with 20-240 Hz range, signed per-scene frame budgets with per-phase targets summing to 16.666ms, deterministic PRNG rooted in `(scene_seed, tick_number, namespace)`, topologically-sorted fixed-update ordering, pause-as-first-class-state, explicit overload policies (catch-up default, max 5 ticks), signed per-tick recording of `(tick_number, input_hash, state_hash)`, and multi-world/sub-world tick isolation. The tick scheduler itself is a subclassable signed gseed. Every subsequent Tier A brief sits on top of this namespace.**

## Confidence

**4/5.** The design is a synthesis of well-proven patterns (Glenn Fiedler timestep, Unity's FixedUpdate split, GGPO rollback netcode recording, Godot's physics-tick/process-tick split) composed under the seven-axis discipline. The 5th confidence point is withheld until the canonical tick battery (Brief 134) empirically validates the 5-tick catch-up ceiling on the v0.1 hardware floor (Brief 135).

## Spec impact

- `gspl-reference/namespaces/tick.md` — new namespace definition with all gseed types (mode, hz, frame.budget, time_scale, overload_policy, scheduler)
- `gspl-reference/research/020-determinism-contract-per-engine.md` — cross-reference; tick namespace is the scheduling primitive determinism sits on
- `gspl-reference/research/025-renderer-determinism-contract.md` — cross-reference; variable-update contract aligns with renderer determinism
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — add tick battery test family (tick ordering, overload policy, time-scale correctness, sub-world isolation)
- `gspl-reference/research/144-drift-detector-threshold-calibration.md` — `frame.budget.breach` and `tick.overload.spiral` gseeds feed drift metrics

## New inventions

- **INV-594** — *Three-mode canonical tick namespace* (fixed / variable / hybrid) where mode is a signed typed gseed, not an engine flag, letting creators compose mixed-mode scenes (e.g., fixed physics world inside a variable-time UI shell).
- **INV-595** — *Per-phase signed frame budget* with enforced per-phase targets summing to the total frame time, enabling the drift detector to see budget breaches as first-class events.
- **INV-596** — *Topologically-compiled tick order with phase annotations* — the DAG resolves at scene-compile and is signed into the scene gseed, so every creator's identical scene ticks identically on every machine.
- **INV-597** — *Sub-world tick isolation with deterministically-derived PRNG sub-seeds*, enabling mini-games and dream sequences as composable signed sub-scenes without seed collision.
- **INV-598** — *Rollback-netcode-ready tick recording from v0.1* — `(tick_number, input_hash, state_hash)` captured on every fixed tick even when no networking exists, so Tier F (briefs 209-216) adds multiplayer without changing the recording format.

## Open follow-ups

- Whether the tick scheduler should support opportunistic GPU offload of fixed-update phases (defer to Round 8 implementation).
- Whether negative time-scale (reverse-replay) is ship-ready at v0.1 or should wait for the time-machine UI (Round 2 Brief 052); provisional answer is v0.1 supports the data path but the UI ships at v0.2.
- Exact per-phase budget split for mobile targets (defer to Tier G Brief 222 performance budget enforcement).

## Sources

- Round 2 Brief 020 — determinism contract per engine
- Round 2 Brief 025 — renderer determinism contract
- Round 2 Brief 026 — deterministic kernel implementation
- Round 2 Brief 052 — lineage-aware time machine
- Brief 131 — seven-axis structural claim (Rollback-able)
- Brief 134 — substrate-native benchmark battery
- Brief 135 — hardware budget v0.1
- Brief 144 — drift detector threshold calibration
- Brief 149 — v0.1 scope finalization
- Glenn Fiedler, "Fix Your Timestep!" — canonical variable/fixed pattern
- GGPO / rollback netcode recording format (referenced for Tier F compatibility)
- Godot physics-process vs process tick split
- Unity FixedUpdate / Update / LateUpdate documentation
