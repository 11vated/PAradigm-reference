# 198 — Top-down action RPG genre recipe

## Question
What is the typed genre composition recipe that produces a complete signed top-down action RPG gseed bundle (Zelda / Hyper Light Drifter / Hades-lite class) from substrate primitives, with combat, inventory, dialogue, and progression loops, ready for export to any v0.1 engine target?

## Why it matters (blast radius)
Top-down action RPGs are the second-most-built indie genre after platformers and the canonical proving ground for combat + inventory + dialogue + progression simultaneously. A working recipe demonstrates that the substrate composes the four major game-design loops together, not just one at a time.

## What we know from the spec
- Brief 197 — 2D platformer recipe (template precedent).
- Briefs 152-163 — Tier A primitives.
- Briefs 164-176 — Tier B inventories.
- Brief 159 — state machines / behavior trees.
- Brief 174 — UI / HUD pattern library.
- Brief 180 — dialogue and quest editor.

## Findings
1. **Recipe inherits Brief 197 frame.** Same `recipe.gseed` kind, composition manifest, parameter slots, validation contract pattern.
2. **Required primitives.** Inherits platformer set, plus: `dialogue.tree`, `quest.graph`, `inventory.container`, `item.def`, `stats.sheet`, `progression.curve`, `behavior.tree` (enemy AI), `audio.bus` (with combat mix layer).
3. **Combat loop.** Typed combat FSM: Idle → Wind-up → Active → Recovery → Idle. Each state has typed frames, hitbox windows, cancel windows. Defaults drawn from Hyper Light Drifter + Hades published frame data. Hitbox is a typed `physics.body.region` with damage/knockback/status payloads.
4. **Top-down movement.** 8-direction or analog movement with typed acceleration / max-speed / friction. No gravity (top-down sets gravity = 0 in the validator).
5. **Camera rig.** Top-down camera with deadzone + smooth follow; no platformer look-ahead. Optional cinematic shot triggers from `quest.graph` events.
6. **Inventory system.** `inventory.container` with typed slot count + typed accept-filter (e.g., "weapons only", "consumables only"). Items are signed `item.def` gseeds with typed effects bound to substrate primitives (heal → stats.sheet.health delta).
7. **Stats and progression.** Player has a `stats.sheet` (HP/MP/STR/DEX/INT defaults; creator-configurable). XP gain → `progression.curve` lookup → level up → stat increase. All typed.
8. **Dialogue and quest binding.** NPCs are entities with attached `dialogue.tree` and optional `quest.graph` references. Dialogue triggers via interact action; quest state mutates via dialogue callbacks. Both editor-equals-runtime per Brief 180.
9. **Enemy AI.** Default enemies use Brief 159 behavior trees with patrol → chase → attack → flee patterns. Three difficulty presets: pushover / standard / hardcore.
10. **Validation contract.** Sign-time gates: at least one player entity with `stats.sheet` + combat FSM, at least one enemy with `behavior.tree`, gravity = 0, at least one `dialogue.tree` OR `quest.graph` (RPGs require at least one social/narrative loop), at least one `inventory.container`.
11. **Sub-recipes.** Zelda-like (puzzle dungeons, key/door progression), Hyper Light Drifter (precision combat, no levels), Hades-lite (room-cleared roguelite), Stardew-lite (farming + dialogue, no combat — downgrades to "social-rpg" sub-class).
12. **Asset pack binding.** References `seed-armory:pack:topdown-rpg-prototype-v1` by default.

## Risks identified
- **Loop interaction complexity.** Combat + inventory + dialogue + progression interacting create emergent bugs. Mitigation: validation contract gates the structural composition; per-loop tests in playtest harness (Brief 185).
- **Dialogue tree authoring overhead.** Creators may not write dialogue. Mitigation: default sub-recipes ship with placeholder dialogue trees; "no NPCs" sub-recipe drops the dialogue requirement.
- **Stats sheet flexibility.** Creators want to redefine stat names. Mitigation: stat names are typed string labels with no engine-side semantics; creators rename freely.
- **Combat frame data sensitivity.** Frame timings are critical to combat feel. Mitigation: ship validated frame presets from real games; document the safe ranges.
- **Inventory UI complexity.** Inventory UIs are notoriously hard. Mitigation: recipe ships a default inventory UI as a `ui.element` template with the standard grid layout from Brief 174.

## Recommendation
Specify the top-down action RPG recipe as a `recipe.gseed` composing substrate primitives plus dialogue/quest/inventory/stats/progression, with a typed combat FSM, four sub-recipes (Zelda / Hyper Light Drifter / Hades-lite / Stardew-lite), and a sign-time validation contract gating combat-AI-dialogue/quest-inventory composition. Default sub-recipe instantiation produces a playable game within 60 seconds.

## Confidence
**4 / 5.** Action RPG mechanics are well-published. The novelty is the four-loop composition validation. Lower than 4.5 because combat frame data sensitivity and dialogue authoring overhead are creator-facing risks needing Phase-1 measurement.

## Spec impact
- New spec section: **Top-down action RPG genre recipe specification**.
- Adds the typed combat FSM template.
- Adds the four sub-recipes.
- Cross-references Briefs 159, 174, 180, 197.

## New inventions
- **INV-824** — Typed combat FSM (Idle/Wind-up/Active/Recovery) with hitbox window slots and cancel windows: combat feel reduces to a small typed state machine with frame-data parameters.
- **INV-825** — Four-loop composition validation contract (combat + inventory + dialogue/quest + progression): action RPG identity is the structural co-presence of all four loops.
- **INV-826** — Stat-sheet typed-label flexibility: substrate enforces stat structure but not stat names, enabling creator-defined attribute systems.
- **INV-827** — Difficulty presets as typed enemy-BT parameter sets: pushover/standard/hardcore are typed parameter overlays on the enemy behavior tree, not separate trees.
- **INV-828** — "Social RPG" downgrade for combat-less variants (Stardew-lite): the validation contract gracefully downgrades to a sub-genre when one loop is dropped.

## Open follow-ups
- Phase-1 measurement of "60 seconds to playable" claim.
- More sub-recipes (e.g., bullet-hell-action-RPG) — deferred to v0.3.
- Procedural quest generation as recipe extension — deferred to v0.4.
- Inventory crafting sub-system — deferred to v0.3.

## Sources
1. Brief 159 — State machines and behavior trees.
2. Brief 174 — UI / HUD pattern library.
3. Brief 180 — Dialogue and quest editor.
4. Brief 197 — 2D platformer genre recipe.
5. Hyper Light Drifter postmortem — Heart Machine.
6. Hades GDC talk — Supergiant Games.
7. "Designing Action RPG Combat" — GDC.
