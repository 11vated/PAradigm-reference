# 154 — Input abstraction namespace

## Question

How does GSPL equip the universal input layer — keyboard, gamepad, touch, motion, voice — as a typed substrate namespace with rebinding, accessibility, and signed input recordings that drive deterministic replay and Tier F (multiplayer) rollback netcode?

## Why it matters (blast radius)

Input is the only place where the outside world enters the deterministic substrate. If input isn't signed and replayable, every downstream system that depends on determinism (physics, AI, networking, save/load, replay, debugging) loses its guarantees. If input isn't device-abstracted, creators write per-platform branches and lose portability. If input isn't rebinding-first and accessibility-first, the substrate fails the constitutional grounding floor (Brief 097) at the input boundary.

## What we know from the spec

- Brief 152 establishes the tick scheduler; input must arrive on the fixed tick boundary, not asynchronously.
- Brief 153 establishes ECS; an `input` component holds per-tick input state for actor entities.
- Brief 131 — seven-axis claim; input recordings must be Signed and Lineage-tracked.
- Brief 097 — anti-hallucination/grounding floor; accessibility is non-patchable.
- Brief 149 — v0.1 includes input but not voice or motion (those are v0.2+).

## Findings

1. **Input is captured as signed actions, not raw events.** Raw device events (key codes, mouse coords, gamepad button bitfields) are *immediately* mapped through a signed binding gseed into named actions (`jump`, `move_x`, `aim`, `interact`). Only actions enter the ECS world; raw events stay at the device boundary. This is the Unreal Enhanced Input / Unity Input System / Godot Action pattern, signed.

2. **Five canonical action types ship at v0.1.** `digital` (binary on/off), `analog_1d` (-1..1 axis), `analog_2d` (vec2 stick), `delta` (mouse-look style relative motion), and `gesture` (touch sequence completion: tap, double-tap, swipe, pinch, hold). Voice is `transcript` and motion is `pose`, both deferred to v0.2 per Brief 149.

3. **Bindings are signed gseeds in `input.binding`.** A binding is `(action_name, device_type, source, modifier_chain, deadzone, sensitivity)`. Multiple bindings per action are normal (gamepad-A *and* keyboard-Space both fire `jump`). Bindings are creator-editable at runtime; rebind UIs read and write the same gseed format that the engine uses.

4. **Input arrives on the fixed tick boundary, polled, not pushed.** The variable-update polls device state and queues raw events. The fixed tick scheduler (Brief 152) drains the queue at the start of each fixed tick, applies bindings, writes the resulting action set into the ECS `input` component for the local-player actor, and signs it as `input.tick.snapshot`. Asynchronous events are *never* applied mid-tick; they wait for the next tick boundary.

5. **Per-tick input snapshot is the rollback-netcode primitive.** `input.tick.snapshot` carries `(player_id, tick_number, action_set, hash)`. This is exactly the recording format Tier F Brief 209 needs for GGPO-style rollback netcode. v0.1 ships the recording format even though multiplayer doesn't ship until v0.3 — the structural choice that makes adding multiplayer "free" later.

6. **Input recording = ordered sequence of `input.tick.snapshot` gseeds.** A replay file is just a tick-ordered sequence of input snapshots plus the initial scene gseed. Re-running the same scene with the same inputs produces bit-identical results because Brief 152 guaranteed deterministic ticks. This collapses "replay system" into "input recording playback" — no separate machinery.

7. **Accessibility is structural, not optional.** Every binding gseed carries an `accessibility` block with: rebindable (default true), hold-vs-toggle (default toggle), repeat-rate-tunable, alternative-input-supported (e.g., dwell-click for switch users), required-precision (low/med/high). The first-ten-minutes onboarding (Brief 104) and the Tier C UI editor (Brief 184) refuse to ship a scene that fails the accessibility check — surfaced as a signed `input.accessibility.violation` gseed.

8. **Device hot-plug is signed, not silent.** Connecting/disconnecting a gamepad mid-session emits `input.device.connected` and `input.device.disconnected` gseeds. The scene can react (pause, show prompts) or ignore. Default behavior at v0.1: pause on disconnect of the active player device, show "reconnect or rebind" overlay. This is the constitutional courtesy — the substrate never silently loses input.

9. **Local multi-player (couch coop) is supported at v0.1; networked multi-player at v0.3.** Each local player gets a distinct `player_id` and a distinct `input` component on their actor. Devices are bound to players via a signed `input.player.bind` gseed. v0.1 supports up to 4 local players (the constraint isn't input — it's the renderer split-screen path, defer to renderer brief).

10. **Touch is first-class, not "mouse with extra steps".** The `gesture` action type and the touch primitives (single, multi, pinch, rotate, swipe, long-press) are typed and signed at the binding layer. Mobile/touch is v0.4 default per Brief 149's scope; v0.1 ships the substrate but no mobile build target. HTML5 builds (v0.1 export) get touch support for free since the binding layer treats it as a device, not a platform.

11. **Voice and motion bindings exist but are gated behind v0.2.** The `transcript` and `pose` action types reserve namespace slots; v0.1 input.binding gseeds may not target them. This is per Brief 149's scope cuts (audio/voice = v0.2). The reservation prevents creators from inventing parallel voice systems that v0.2 would have to break.

12. **Input lineage explains why an action fired.** When an action fires, the resulting `input.tick.snapshot` carries the binding gseed reference. A creator debugging "why did jump fire here?" can traverse the lineage to the binding to the device event. This is the seven-axis Lineage property at the input boundary.

13. **Differentiable input — accepted control schemes propagate.** Control schemes (full sets of bindings) are signed `input.scheme` gseeds. Creator-tuned schemes that get high acceptance scores in the Brief 134 canonical battery and the Brief 144 drift detector get promoted as default scheme suggestions for new projects in the same genre. This is the seventh-axis (Differentiable) at the input layer.

## Risks identified

- **Polling input on the fixed tick can introduce up to one-tick latency vs raw event handling.** Mitigation: at 60 Hz that's 16.6ms — well within human perception threshold for action games. Twitch genres (fighting, bullet-hell) can opt into 120 Hz fixed-tick (Brief 152 allows up to 240 Hz).
- **Touch gesture recognition is hard to make deterministic across devices.** Mitigation: gesture detection runs on tick boundaries against quantized touch position grids (defined per device DPI class), not against raw float coords. Gestures are signed only after recognition succeeds, never speculatively.
- **Accessibility checks can be over-restrictive and frustrate creators.** Mitigation: violations are warnings by default; only the constitutional accessibility floor (e.g., must be rebindable) is hard-blocking. Creators can opt-in to stricter checks per project.
- **Per-tick action set diff is noisy when player holds a button.** Mitigation: the snapshot is the *current* action set, not a diff; the rollback-netcode hash is over the full set. Storage cost is bounded by `tick_count × action_count × 1 bit`, ~7.5 KB/min at 60 Hz with 16 actions, trivial.
- **Hot-plug pause-default may be wrong for keyboard-only single-player games.** Mitigation: per-scene override; default is "pause if active player loses primary device," not "pause on any disconnect."

## Recommendation

**GSPL ships an `input` namespace at v0.1 with action-not-event capture, five canonical action types (digital/analog_1d/analog_2d/delta/gesture, plus reserved transcript/pose for v0.2), signed binding gseeds with structural accessibility blocks, fixed-tick-boundary draining of the device event queue, signed per-tick `input.tick.snapshot` as the rollback-netcode primitive, replay-as-input-recording-playback, signed device hot-plug events, up to 4 local players with per-player binding, touch as first-class through HTML5 export, voice/motion namespace slots reserved but gated, and creator control schemes that compete via the Brief 144 drift detector to become genre-default suggestions.**

## Confidence

**4/5.** The action-not-event pattern is the consensus of Unreal Enhanced Input, Unity New Input System, Godot Actions, and Steam Input — all proven at scale. Tick-boundary draining is the rollback-netcode pattern. Accessibility-as-structural is the only somewhat-novel choice; it's defensive and honest about the constitutional floor.

## Spec impact

- `gspl-reference/namespaces/input.md` — new namespace: `input.binding`, `input.scheme`, `input.tick.snapshot`, `input.device.connected`, `input.device.disconnected`, `input.player.bind`, `input.accessibility.violation`
- `gspl-reference/research/152-game-loop-tick-model-namespace.md` — cross-reference; input drains at fixed-tick start
- `gspl-reference/research/153-ecs-substrate-binding.md` — cross-reference; `input` component on actor entities
- `gspl-reference/research/097-anti-hallucination-test-suite.md` — cross-reference; accessibility is constitutional
- `gspl-reference/research/104-first-ten-minutes-onboarding.md` — cross-reference; rebinding intro is part of onboarding
- Tier C Brief 184 (UI/HUD layout editor) inherits accessibility check
- Tier F Brief 209 (networking model) inherits the rollback-netcode recording format

## New inventions

- **INV-604** — *Action-not-event signed input capture* — bindings are first-class signed gseeds; raw device events never enter the ECS world; the boundary is structural.
- **INV-605** — *Per-tick input snapshot as the universal rollback-netcode primitive*, shipped at v0.1 even though Tier F multiplayer is v0.3, so the recording format never changes.
- **INV-606** — *Replay = input recording playback* — no separate replay system; `(initial_scene_gseed, ordered input.tick.snapshots)` is the replay format.
- **INV-607** — *Accessibility-as-structural binding metadata* — every binding gseed carries an accessibility block; constitutional violations are signed, surfaced, and refused at scene compile.
- **INV-608** — *Genre-default control scheme promotion* — creator schemes compete via the Brief 144 drift detector and the highest-scoring become default suggestions for new projects in the same genre, the Differentiable axis at the input layer.

## Open follow-ups

- Exact deadzone defaults per gamepad family (defer to Tier G Brief 219 asset import for device-DB import).
- Whether the substrate ships built-in support for adaptive triggers (PS5) and haptics at v0.1 — provisional yes for haptics, no for adaptive triggers (Round 8).
- Whether the rebind UI is a stock Studio component or per-project (provisional: stock, with project override).

## Sources

- Brief 097 — anti-hallucination test suite and grounding gates
- Brief 104 — first-ten-minutes onboarding
- Brief 131 — seven-axis structural claim
- Brief 134 — substrate-native benchmark battery
- Brief 144 — drift detector threshold calibration
- Brief 149 — v0.1 scope finalization
- Brief 152 — game loop and tick model namespace
- Brief 153 — ECS substrate binding
- Unreal Enhanced Input documentation
- Unity Input System documentation
- Godot InputAction / InputMap documentation
- Steam Input controller abstraction
- GGPO rollback netcode input recording format
