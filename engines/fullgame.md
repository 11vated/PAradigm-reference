# FullGame Engine

## Overview

Generates a complete, self-contained, playable HTML5 game from genes describing theme, mechanics, level layouts, characters, and narrative. 3,329 LOC, 8 stages. Output is a single `.zip` containing `index.html`, `engine.js`, asset folders, and a manifest. The user can open it in a browser and play immediately.

## Gene Schema

| Gene | Type | Range | Required | Description |
|---|---|---|---|---|
| `theme` | categorical | enum {fantasy, sci_fi, horror, comedy, mystery, slice_of_life, abstract} | yes | Tone |
| `mechanics` | array<categorical> | from {platformer, shooter, puzzle, rpg, racing, sandbox, rhythm, deck_builder, idle, simulation} | yes | Core gameplay |
| `level_seeds` | array<seed_ref> | by hash | yes | Level layouts (each is a procedural seed) |
| `character_seeds` | array<seed_ref> | by hash | yes | Playable + NPCs |
| `narrative_seed` | seed_ref | by hash | no | Story arc |
| `difficulty_curve` | vector(5) | each [0, 1] | yes | Per-level difficulty |
| `art_style` | categorical | enum {pixel, vector, cel_shaded, low_poly, photoreal, hand_drawn} | yes | Visual style |
| `target_session_minutes` | scalar | [1, 480] | yes | Intended play length |

## Stage Pipeline

```
1. extract        : Seed                        -> GameWorking
2. morphogenesis  : GameWorking                 -> WorldLayout
3. populate       : WorldLayout                 -> PopulatedWorld
4. parameterize   : PopulatedWorld              -> BalancedWorld
5. simulate       : BalancedWorld               -> ValidatedWorld
6. compose        : ValidatedWorld              -> GameBundle
7. render         : GameBundle                  -> MinifiedBundle
8. export         : MinifiedBundle              -> FullGameArtifact
```

## Stage Details

### Stage 2 — `morphogenesis`

Generate world layout (level graph) from procedural rules driven by `theme` and `mechanics`. Each node is a level slot; each edge is a transition.

### Stage 3 — `populate`

Place characters, items, hazards into each level by referencing the `level_seeds` and `character_seeds`. Cross-domain references are resolved at this stage — the engine asks the kernel for the referenced seeds and grows them inline.

### Stage 4 — `parameterize`

Compute game balance numbers: HP, damage, cooldowns, drop rates. Driven by `difficulty_curve`.

### Stage 5 — `simulate`

Run a balance pass — play the game with a stub AI to verify completability. If the AI cannot complete a level within a budget, adjust parameters and re-run. This stage may iterate up to N times before declaring success or failure.

### Stage 6 — `compose`

Assemble the HTML5 bundle: `index.html`, `engine.js`, asset folders for sprites/audio/levels.

### Stage 7 — `render`

Minify JS, optimize assets, pack into a single deployable archive.

### Stage 8 — `export`

Emit `.zip` bytes plus a manifest describing controls, recommended browsers, and required APIs (e.g., gamepad, audio).

## Render Hints

```ts
{ viewportMode: 'game', supportsAnimation: true, thumbnailSize: { width: 640, height: 360 } }
```

The studio renders the bundle inside an iframe sandbox so the user can actually play the preview.

## Export Hints

`['html5_zip', 'godot_project', 'unity_project', 'phaser_project']`. Recommended: `html5_zip`.

## Fitness Hints

Meaningful axes: coherence, animation, style, novelty.
Default MAP-Elites descriptors: `mechanic_complexity`, `difficulty_curve_area_under_curve`.

## Determinism Notes

- Bundle bytes are deterministic. The *gameplay* may include physics/RNG that's also deterministic given a play seed, but the *bundle* itself is what's compared for byte-equality.
- Minification uses fixed `terser` settings.
- ZIP files use STORE compression (no compression) to avoid dictionary differences.

## Validation Rules

- At least one mechanic.
- At least one level_seed and one character_seed.
- All referenced seeds resolve in the kernel and are valid.
- The simulate stage successfully completes each level (within retries).

## Anti-Patterns

- **Don't bypass the simulate stage.** A bundle that ships without verified completability is broken-by-construction.
- **Don't inline level/character generation.** Use referenced seeds; this enforces the cross-domain composition pattern.

## References

- Phaser 3 documentation
- Procedural Content Generation in Games (Shaker, Togelius, Nelson, 2016)
