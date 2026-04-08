# 206 — 3D first-person and third-person genre recipe

## Question
What is the typed genre composition recipe that produces a complete signed 3D first-person or third-person gseed bundle (Doom-clone / Quake-clone / Tomb-Raider / Dark-Souls / Minecraft-class) from substrate primitives, with 3D camera, character controller, weapon systems, and 3D level scenes?

## Why it matters (blast radius)
3D character-action games are the dominant AAA genre and the canonical proving ground for 3D substrate primitives end-to-end. A working recipe demonstrates the substrate's 3D camera, character controller, animation runtime, and skeletal systems compose into creator-instantiable 3D games — and it stress-tests the cross-engine 3D parity story (Brief 196).

## What we know from the spec
- Brief 156 — physics integration (3D).
- Brief 161 — animation runtime (skeletal).
- Brief 162 — VFX module stack.
- Brief 195 — Spine / DragonBones (note: 2D-only — 3D uses different path).
- Briefs 197-205 — recipe template precedent.

## Findings
1. **Recipe inherits frame.**
2. **Required primitives.** `level.scene` (3D pattern family from Brief 172), `physics.body` (3D character + props), `animation.skeleton` + `animation.clip` (humanoid rig), `character.controller` (typed FPS/TPS controller), `camera.rig` (FPS / over-shoulder / orbit modes), `input.action` (look + move + interact + attack), `audio.bus` (3D positional), `vfx.system` (muzzle flash / impact / blood), `ui.element` (HUD), `weapon.def` (typed weapon), `state.machine` (player state), `save.snapshot`.
3. **Character controller as typed primitive.** `character.controller` declares: capsule height/radius, walk speed, run speed, jump height, crouch height, slope limit, step height. Substrate provides the controller implementation (not the engine's). This guarantees cross-engine parity.
4. **Camera modes.** First-person (camera at head bone), third-person over-shoulder (camera offset behind character), third-person orbit (camera circles character with mouse). Sub-recipes select.
5. **Weapon system.** `weapon.def` declares: type (hitscan / projectile / melee), damage, range, fire rate, ammo, reload time, recoil curve, hit response. Hitscan uses typed `physics.raycast` mutation; projectile uses `physics.body` spawn.
6. **Animation rig.** Default humanoid rig (Brief 161) with idle / walk / run / jump / land / aim / fire / reload / hurt / death animations. Sub-recipes can override.
7. **3D physics.** Brief 156 3D physics with substrate deterministic kernel default. Replay-bit-deterministic across the eight engine targets per Brief 196.
8. **Sub-recipes.** Doom-clone (FPS, hitscan + projectile, fast movement, no ironsights), Quake-clone (FPS, projectile-heavy, advanced movement like rocket jump), Souls-like (TPS over-shoulder, stamina-based combat, lock-on target), Tomb-Raider-style (TPS orbit, climbing + puzzles), Minecraft-style (FPS or TPS, voxel world from Brief 207).
9. **Lock-on target system.** Souls-like sub-recipe ships typed `target.lock` mutation with eligible-target selector and camera-follow override. Toggles via input.action.
10. **Validation contract.** Sign-time gates: 3D level scene (rejects 2D), `character.controller` present, `camera.rig` with valid mode, at least one `weapon.def` (or weapon-less sub-recipe explicitly opt out), substrate physics kernel selected (not engine native).

## Risks identified
- **3D parity is harder than 2D.** Brief 196 parity suite must include 3D fixtures across all eight engines (where 3D is supported — not Phaser, GameMaker; HTML5 via Three.js). Mitigation: sub-recipes default to engines that support 3D well.
- **Character controller fidelity.** Substrate-provided controller may not match creator expectations against engine-native controllers. Mitigation: typed parameters expose creator tuning; document the cross-engine parity guarantee as the trade-off.
- **Animation rig variation.** Humanoid rig assumptions break for non-humanoid characters. Mitigation: sub-recipes can substitute alternative rigs; default ships humanoid.
- **Asset volume.** 3D needs more art than 2D. Mitigation: default Brief 088A pack provides programmer-art humanoid rig + box weapons.

## Recommendation
Specify the 3D first/third-person recipe as a `recipe.gseed` with typed `character.controller` (substrate-provided, not engine-native), three camera modes, typed `weapon.def` system, humanoid animation rig default, substrate 3D physics kernel default, and five sub-recipes. Default sub-recipe (Doom-clone) produces a playable 3D FPS in under 2 minutes.

## Confidence
**4 / 5.** 3D character-action mechanics are well-precedented; the novelty is the substrate-provided character controller for cross-engine parity. Lower than 4.5 because 3D parity across engines (Brief 196) needs extensive Phase-1 measurement to validate the substrate-controller decision.

## Spec impact
- New spec section: **3D first-person and third-person genre recipe specification**.
- Adds typed `character.controller`, `weapon.def`, `target.lock` gseed kinds.
- Adds the substrate-provided-controller cross-engine parity contract.
- Cross-references Briefs 156, 161, 172, 196, 197.

## New inventions
- **INV-864** — Substrate-provided typed `character.controller` cross-engine parity primitive: character movement is identical across all engines because substrate ships the controller, not engines.
- **INV-865** — Three-mode camera rig (FPS / over-shoulder / orbit) as typed substrate primitive: camera behavior is structured choice, not per-game implementation.
- **INV-866** — Typed `weapon.def` with hitscan / projectile / melee variants: weapons are first-class typed gseeds with declarative behavior.
- **INV-867** — Typed `target.lock` mutation with eligible-target selector: Souls-style lock-on is a substrate primitive, not per-game scripting.
- **INV-868** — Sub-recipe-driven engine target filtering: 3D sub-recipes declare which engines they're compatible with, surfacing at sign-time when targeting incompatible engines (e.g., Phaser).

## Open follow-ups
- VR/AR camera mode (deferred to v0.5 with WebXR).
- Ragdoll on death — deferred to v0.3.
- Vehicle controllers — deferred to v0.4.
- Non-humanoid character rigs as sub-recipe options — Phase 1.

## Sources
1. Brief 156 — Physics integration.
2. Brief 161 — Animation runtime.
3. Brief 172 — Scene patterns.
4. Brief 196 — Cross-engine parity test suite.
5. Brief 197 — 2D platformer recipe.
6. Doom 3 source code (id Software, GPL).
7. Dark Souls combat design talks — From Software / GDC.
8. Quake movement physics analysis (community-documented).
