# 197 — 2D platformer genre recipe

## Question
What is the typed genre composition recipe that produces a complete, signed 2D platformer gseed bundle from substrate primitives, validated against the canonical platformer feel-loop and ready for export to any of the eight v0.1 engine targets?

## Why it matters (blast radius)
2D platformers are the highest-volume indie genre and the canonical first-game for new creators. A typed recipe that compiles substrate primitives into a working platformer in minutes proves the substrate is *composable*, not just *capable*. Without recipes, creators face a blank-page problem and the substrate's expressiveness is invisible.

## What we know from the spec
- Briefs 152-163 — Tier A substrate primitives.
- Briefs 164-176 — Tier B content inventories.
- Briefs 177-187 — Tier C authoring surfaces.
- Briefs 188-196 — Tier D export pipelines.
- Brief 172 — scene patterns (`level.scene` 2D pattern family).
- Brief 173 — tilemap autotile.
- Brief 156 — physics integration.
- Brief 159 — state machines and behavior trees.

## Findings
1. **Recipe as typed gseed.** A genre recipe is a signed `recipe.gseed` declaring the namespace primitives it composes, the parameter slots it exposes to creators, and the validation contract that defines "is this still a platformer?"
2. **Required primitives.** Platformer recipe imports: `tilemap.layer` (one or more), `physics.body` (player + enemies + props), `animation.clip` (idle/walk/jump/fall/land/hurt/die), `input.action` (left/right/jump/crouch/interact), `audio.bus` (music + SFX), `vfx.system` (jump dust, landing dust, hit flash), `ui.element` (HUD: health/score/lives), `state.machine` (player FSM), `level.scene` (one starter level), `save.snapshot` (checkpoint), `camera.rig` (follow with deadzone), `vfx.system` (parallax background module).
3. **Player FSM canonical states.** Recipe ships a typed FSM with: Grounded, Jumping, Falling, Coyote-jump (typed timer), Wall-slide (optional), Wall-jump (optional), Crouch (optional), Hurt, Dead. Each state has typed transition conditions referencing `input.action` and `physics.body.contact_state`.
4. **Feel-loop parameters.** The "platformer feel" reduces to ~12 typed numeric parameters: jump height, jump apex time, fall multiplier, max horizontal speed, ground acceleration, air acceleration, ground friction, air friction, coyote-time window, jump-buffer window, terminal velocity, gravity. The recipe exposes all twelve as creator-tunable typed fields with documented sensible defaults (drawn from Celeste / Hollow Knight / Super Meat Boy published numbers).
5. **Coyote-time and jump-buffer.** Both are typed timer fields on the player FSM. Coyote-time fires the Jump transition during a brief grace period after leaving the ground; jump-buffer fires the Jump transition during a brief grace period after the input is pressed but before grounding. Defaults: 100ms coyote, 150ms buffer.
6. **Tilemap collision contract.** Recipe declares the tilemap layer's collision-tile set. Brief 173's 47-tile autotile + collision bitmask drives both visual rendering and physics body collider generation. Sign-time validator gates that the collision tileset is non-empty.
7. **Camera follow rig.** Camera-rig is a typed `camera.rig` instance with 2D follow + deadzone + look-ahead based on player velocity sign. Look-ahead and deadzone are exposed as creator-tunable parameters with platformer-canonical defaults.
8. **Validation contract — "is this still a platformer?"** Sign-time validator gates: (a) at least one player FSM with Grounded + Jumping + Falling states, (b) at least one tilemap layer with collision tiles, (c) at least one input.action with `jump` semantic tag, (d) gravity > 0 and < 30 m/s², (e) jump height between 0.5 and 5 player heights. Any violation downgrades the gseed from "platformer" to "2d-game" and surfaces the missing requirement.
9. **Recipe instantiation.** A creator instantiates the recipe by selecting parameter values; the recipe emits a complete signed gseed bundle ready for export. Default parameters produce a playable Celeste-clone within 30 seconds of instantiation.
10. **Sub-recipes.** The platformer recipe ships sub-recipes for: classic Mario (no wall-jump, fixed gravity), Celeste-style (dash + wall-jump), Metroidvania (room-based scenes + ability gating), and Super Meat Boy (high-speed + spike instakill). Sub-recipes override default parameters and FSM states; creators can fork further.
11. **Asset pack binding.** Recipe references Brief 088A seed armory packs by typed pack id (e.g., `seed-armory:pack:platformer-prototype-v1`). Default pack provides programmer-art tiles + sprites; creators swap to their own pack.
12. **Engine export readiness.** Recipe gseeds export to all eight Tier D engines without modification. The recipe's primitives are all in the substrate's runtime baseline; no engine-specific extensions are required.

## Risks identified
- **Recipe vs creator freedom tension.** Recipes risk being too prescriptive and steering creators toward homogeneous output. Mitigation: every recipe parameter is a *default*, not a *constraint*; the validation contract gates only the structural genre identity, not the creative choices.
- **Feel-loop parameter sensitivity.** Twelve parameters interact non-linearly; bad combinations produce unfun games. Mitigation: ship validated parameter presets from real published games; document the safe ranges per parameter.
- **Sub-recipe explosion.** Every sub-genre risks becoming a full recipe. Mitigation: cap sub-recipes at five per parent recipe in v0.1; deeper specialization is creator forking, not substrate-shipped.
- **Asset pack dependency.** Default pack is required at recipe instantiation. Mitigation: bundled programmer-art pack in `seed-armory:default` is always available; creators see an immediate playable result.
- **Validator strictness.** Too-strict validators reject legitimate platformer variations (e.g., zero-gravity puzzle platformer). Mitigation: validator surfaces a downgrade rather than a hard reject; "this is not a platformer per the canonical definition but is still a valid 2d-game gseed."

## Recommendation
Specify the 2D platformer recipe as a signed typed gseed composing substrate primitives (tilemap + physics + animation + input + audio + vfx + ui + state machine + level scene + save + camera) with twelve typed feel-loop parameters, a canonical FSM, four sub-recipes (Mario / Celeste / Metroidvania / Super Meat Boy), and a sign-time validation contract that gates structural genre identity. Default parameters produce a playable game within 30 seconds of instantiation.

## Confidence
**4.5 / 5.** Platformer mechanics are well-published and the parameter ranges are documented across decades of game-design literature. The novelty is the typed-recipe-as-gseed pattern with composition validation. Lower than 5 because the "30 seconds to playable" claim needs Phase-1 measurement.

## Spec impact
- New spec section: **2D platformer genre recipe specification**.
- Adds the `recipe.gseed` typed kind with composition manifest, parameter slots, and validation contract.
- Adds the platformer canonical FSM template.
- Adds the twelve feel-loop parameter definitions with sensible-default values from published games.
- Cross-references Briefs 088A, 152-163, 172, 173, 177-187.

## New inventions
- **INV-819** — Typed `recipe.gseed` kind composing substrate primitives with declared parameter slots, sign-time validation contract, and signed lineage: genre recipes are first-class substrate artifacts, not engine boilerplate.
- **INV-820** — Twelve-parameter platformer feel-loop with documented default presets from published games (Celeste / Hollow Knight / Super Meat Boy): the canonical platformer feel is reducible to a small typed parameter set.
- **INV-821** — Sign-time genre validation contract with "downgrade" semantics: non-conforming gseeds are downgraded to a more general kind rather than rejected, preserving creator freedom.
- **INV-822** — Sub-recipe parameter-override pattern: sub-recipes override parent defaults and FSM states without forking the parent, enabling cap-bounded recipe specialization.
- **INV-823** — Recipe-driven asset-pack binding via typed pack id: recipes reference Brief 088A seed armory packs declaratively, swappable by creator with no recipe-level changes.

## Open follow-ups
- Phase-1 measurement of "30 seconds to playable" claim across the eight engine targets.
- Recipe parameter telemetry (creators commonly tweak which?) — deferred to v0.2.
- Recipe versioning and migration when substrate primitives change — covered by Brief 152 lineage but needs recipe-specific guidance — deferred to v0.2.
- More sub-recipes (e.g., Sonic-style speed platformer, puzzle platformer) — deferred to v0.3.

## Sources
1. Brief 088A — Seed armory.
2. Brief 152 — Substrate signing and lineage.
3. Brief 156 — Physics integration.
4. Brief 159 — State machines and behavior trees.
5. Brief 172 — Scene patterns.
6. Brief 173 — Tilemap autotile.
7. Celeste source code (released by Maddy Thorson, github.com/NoelFB/Celeste).
8. "Math for Game Programmers" GDC 2014 — coyote time, jump buffering.
9. "Building a Better Jump" — Kyle Pittman, GDC.
10. Hollow Knight postmortem — Team Cherry.
