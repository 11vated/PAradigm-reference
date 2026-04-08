# 155 — Camera namespace

## Question

How does GSPL equip the universal camera primitive — 2D and 3D, fixed/follow/orbit/free, plus a cinematic camera language — as a typed substrate namespace where the camera itself is a signed gseed and the camera "shot" is composable across scenes?

## Why it matters (blast radius)

The camera is the player's window. Get it wrong and the game is unplayable regardless of how good the systems beneath it are. Every genre has a canonical camera idiom (platformer follow-with-leadout, top-down RPG smart-zoom, FPS first-person, racing chase, RTS edge-pan, fighting framing-keep-both-fighters-visible, cinematic Cinemachine-style virtual cameras). If the substrate doesn't equip the full set as composable signed primitives, creators rebuild them per-game and lose lineage, replay, and rollback at the camera boundary.

## What we know from the spec

- Brief 152 — fixed/variable tick split; camera lives on variable-update with interpolation against fixed-tick state.
- Brief 153 — ECS; camera is an entity with a `camera` component.
- Brief 131 — seven-axis claim; camera "shots" are signed.
- Round 2 Brief 025 — renderer determinism contract; camera projection is part of it.

## Findings

1. **Camera is an ECS entity with a `camera` component.** Not a global. Multiple cameras coexist; one is `active` per viewport at a time. The active camera is selected by a signed `camera.activate` gseed; transitions are signed.

2. **Eight canonical camera modes ship at v0.1.** `fixed_2d`, `follow_2d`, `pan_2d`, `screen_2d`, `fixed_3d`, `follow_3d`, `orbit_3d`, `first_person_3d`. v0.1's 2D-first scope (Brief 149) means the four 2D modes are the primary surface; the 3D modes ship the substrate but the v0.1 export pipeline only reaches them via 3D-capable engines (Godot 3D, Unity, Unreal — Brief 188-190).

3. **Camera state = `(position, rotation, projection, fov_or_size, near, far, target, follow_offset, lookahead, dampening)`.** All as typed fields on the `camera` component. Projection is `orthographic` (2D + isometric) or `perspective` (3D); switching is a signed mutation, not free.

4. **Cinematic shots = signed `camera.shot` gseeds.** A shot declares `(shot_id, mode, target_entity, position, rotation, fov, easing, duration, blend_in, blend_out)`. A scene plays a shot by emitting a signed `camera.shot.play` event. Shots compose into shot lists; shot lists compose into sequences. This is the Cinemachine pattern, signed and made portable.

5. **Camera follow uses lookahead and dampening, not hard tracking.** The default 2D follow camera uses Brackeys/HotlineMiami-style lookahead in the velocity direction with critically-damped spring approach (damping = 0.15 default). The 3D orbit camera uses spherical coordinates with damped angular velocity. Both are well-known patterns; v0.1 ships them as defaults so creators don't reinvent.

6. **Camera bounds = signed regions.** A `camera.bounds` gseed declares a 2D AABB or 3D AABB inside which the camera position is clamped. Crossing room boundaries triggers a signed `camera.bounds.transition` event with a default ease. This is the Metroidvania room-snap pattern, equipped as substrate.

7. **Zoom is parametric, not hardcoded.** A `camera.zoom` gseed declares a zoom curve as a function of one or more entity references — e.g., "zoom out so all four players fit on screen with margin" (Smash Bros camera) or "zoom in proportional to player health below 30%" (Hotline Miami juice). The camera asks the parameters for current zoom each variable-update; result is signed per-frame for replay.

8. **Camera shake is a typed effect, not a script hack.** `camera.shake` is a signed gseed with `(amplitude, frequency, duration, falloff, axes)`. Multiple shakes additively combine; the camera namespace handles bookkeeping. This is the Riot/Vlambeer juice pattern, equipped.

9. **Split-screen and multi-viewport.** A scene can host up to 4 viewports at v0.1, each with its own active camera. Viewport layout (vertical/horizontal/quad/PiP) is a signed `camera.viewport.layout` gseed. The renderer and the input layer (Brief 154) cooperate to give each viewport its own player.

10. **Cinematic camera language: a tiny DSL.** Creators describe shots like `shot.dolly(target=player, from=back_3m, to=back_5m, over=2s, ease=cubic_in_out).then.shake(0.3, 1s)`. The DSL compiles to signed `camera.shot` gseeds. This is the same cognitive load as a video editing timeline, not a scripting language.

11. **Camera replay-determinism is structural.** Camera state is a signed function of (active camera entity, camera component values, target entity transform, time). Given identical inputs from input recording (Brief 154) and identical fixed-tick state (Brief 152), the camera produces identical pixels every replay. The variable-update interpolation uses the deterministic accumulator from Brief 152 so even high-refresh-rate displays replay identically.

12. **Camera-as-modifier-surface.** Per Brief 128's four-layer action space, the camera namespace exposes `camera.set_target`, `camera.shot.play`, `camera.shake`, `camera.zoom.adjust`, `camera.transition` as primitive tools. Creator-tunable shot libraries become genre-default suggestions via the same Differentiable promotion pattern as input schemes (Brief 154 finding 13).

13. **v0.1 reach.** Eight modes, eight canonical shot templates per mode, one DSL, signed bounds and shake and zoom, four-viewport split-screen, cinematic shot lists. 3D modes ship in the substrate but only the 2D modes are surfaced in the first-ten-minutes onboarding (Brief 104). 3D-default cinematic patterns expand at v0.4.

## Risks identified

- **Cinematic shot DSL may diverge from creator mental models from After Effects/Premiere/Cinemachine.** Mitigation: name DSL ops after the editing-room vocabulary (`dolly`, `pan`, `tilt`, `zoom`, `truck`, `pedestal`) and ship a side-by-side cheat sheet.
- **Damping defaults are taste-dependent and may feel wrong on some genres.** Mitigation: ship per-genre default damping presets via the Brief 144 drift detector promotion path.
- **Camera bounds + cinematic shots can conflict (a shot wants to leave the room).** Mitigation: shot.play optionally suspends bounds; the suspension is a signed scope on the shot gseed.
- **3D orbit camera collision (camera clipping into walls) is non-trivial.** Mitigation: v0.1 ships orbit with raycast-based clip-back; full IK-based camera collision deferred to Brief 156 physics integration and Round 8.
- **Multi-viewport input mapping can confuse couch coop.** Mitigation: Brief 154's per-player binding handles it; viewport ↔ player mapping is signed at the layout level.

## Recommendation

**GSPL ships a `camera` namespace at v0.1 with eight canonical modes (4×2D + 4×3D), ECS-component camera entities, signed cinematic shots and shot lists, lookahead/damped follow with sensible defaults, signed camera bounds and bounds-transition events, parametric zoom curves, additively-composable signed shake, up to 4 viewports for split-screen with per-viewport active cameras, a tiny editing-room-vocabulary cinematic DSL that compiles to signed gseeds, deterministic variable-update interpolation against fixed-tick state, and creator-tuned camera defaults that compete via the drift detector to become genre-default suggestions.**

## Confidence

**4/5.** The patterns are all well-known (Cinemachine, Metroidvania bounds, Brackeys lookahead, Hotline Miami zoom, Vlambeer shake). The only novel piece is signing the camera state per-frame for replay; this is required by Brief 131 and adds bounded cost (~one signature per viewport per frame, ~240 sigs/sec at 60 FPS, well within budget).

## Spec impact

- `gspl-reference/namespaces/camera.md` — new namespace
- `gspl-reference/research/152-game-loop-tick-model-namespace.md` — variable-update interpolation contract
- `gspl-reference/research/153-ecs-substrate-binding.md` — `camera` component definition
- `gspl-reference/research/128-gspl-tool-use-and-modifier-surface.md` — cross-reference; camera primitives expose to action space
- Tier C Brief 177 (scene editor) — camera component is a first-class scene element
- Tier D Brief 196 (cross-engine parity test) — camera state must reach all engines identically

## New inventions

- **INV-609** — *Cinematic shot as a signed composable gseed* — shots, shot lists, and sequences are first-class substrate primitives, not scripts.
- **INV-610** — *Editing-room-vocabulary camera DSL* — `dolly`, `pan`, `tilt`, `zoom`, `truck`, `pedestal`, `shake`, with parametric easing and signed compilation, lowering cognitive load for creators with video-editing background.
- **INV-611** — *Parametric zoom curve* over arbitrary entity-state functions, equipping Smash-Bros-style multi-target framing as a substrate primitive rather than a script.
- **INV-612** — *Signed camera bounds with transition events* — Metroidvania room-snap as substrate, replayable and lineage-tracked.
- **INV-613** — *Genre-default damping promotion* — creator-tuned camera defaults compete via the drift detector to become genre-default suggestions for new projects.

## Open follow-ups

- Exact 3D camera-collision algorithm at v0.4 (raycast clip-back at v0.1; defer richer solution to Round 8).
- Whether the cinematic DSL gets a visual timeline editor at v0.1 or v0.2 (provisional v0.2 per Tier C Brief 177 scope).
- Audio listener attachment to camera vs separate listener entity (defer to Brief 163 audio runtime).

## Sources

- Brief 128 — GSPL tool-use and modifier-surface intelligence
- Brief 131 — seven-axis structural claim
- Brief 144 — drift detector threshold calibration
- Brief 149 — v0.1 scope finalization
- Brief 152 — game loop and tick model namespace
- Brief 153 — ECS substrate binding
- Brief 154 — input abstraction namespace
- Round 2 Brief 025 — renderer determinism contract
- Unity Cinemachine documentation
- Brackeys lookahead / damped follow-camera tutorial pattern
- Vlambeer "Art of Screenshake" GDC talk (camera juice)
- Riot Games "League of Legends" camera shake postmortem
