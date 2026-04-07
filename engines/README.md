# Domain Engines

Each of Paradigm's 26 domain engines implements the [`DomainEngine`](../architecture/engine-pattern.md) interface and follows the staged-pipeline pattern. Engines are siblings — none calls another. Cross-domain composition happens through [functor bridges](../architecture/cross-domain-composition.md), not nested calls.

## The 26 Domains

**Implemented (15):**

| Domain | LOC | Stages | Output | Spec |
|---|---|---|---|---|
| Sprite | 3,673 | 8 | PNG atlas + metadata | [sprite.md](sprite.md) |
| Character | 3,615 | 7 | glTF mesh + animations | [character.md](character.md) |
| Music | 3,381 | 5 | WAV + MIDI | [music.md](music.md) |
| FullGame | 3,329 | 8 | HTML5 zip | [fullgame.md](fullgame.md) |
| Geometry3D | 3,084 | 6 | glTF mesh | [geometry3d.md](geometry3d.md) |
| Animation | 2,891 | 5 | glTF animation | [animation.md](animation.md) |
| Procedural | 2,772 | 7 | layered assets | [procedural.md](procedural.md) |
| Narrative | 2,654 | 4 | structured story | [narrative.md](narrative.md) |
| UI | 2,512 | 6 | HTML/CSS bundle | [ui.md](ui.md) |
| Physics | 2,398 | 5 | sim params + trajectories | [physics.md](physics.md) |
| Visual2D | 2,317 | 6 | PNG / SVG | [visual2d.md](visual2d.md) |
| Audio | 2,201 | 5 | WAV | [audio.md](audio.md) |
| Ecosystem | 2,089 | 6 | population state log | [ecosystem.md](ecosystem.md) |
| Game | 1,976 | 5 | mechanic spec | [game.md](game.md) |
| ALife | 1,803 | 6 | initial state + rules | [alife.md](alife.md) |

**Planned (11):**

| Domain | Output | Spec |
|---|---|---|
| Shader | WGSL/GLSL source | [shader.md](shader.md) |
| Particle | particle system spec | [particle.md](particle.md) |
| Typography | font + glyph spec | [typography.md](typography.md) |
| Architecture | building / room glTF | [architecture.md](architecture.md) |
| Vehicle | vehicle glTF + dynamics | [vehicle.md](vehicle.md) |
| Furniture | parametric furniture model | [furniture.md](furniture.md) |
| Fashion | garment mesh + texture | [fashion.md](fashion.md) |
| Robotics | URDF + control policy | [robotics.md](robotics.md) |
| Circuit | KiCad schematic + PCB | [circuit.md](circuit.md) |
| Food | recipe + nutrition + image | [food.md](food.md) |
| Choreography | motion sequence | [choreography.md](choreography.md) |

## How to Read an Engine Spec

Every engine spec follows the same template:

1. **Overview** — what the engine does in one paragraph.
2. **Gene Schema** — the named genes the engine reads, with types and ranges.
3. **Stage Pipeline** — the ordered list of stages, with input/output types.
4. **Stage Details** — pseudocode for each stage.
5. **Render Hints** — how the studio should preview the artifact.
6. **Export Hints** — supported export formats.
7. **Fitness Hints** — which QualityVector axes are meaningful.
8. **Determinism Notes** — engine-specific determinism budget.
9. **Validation Rules** — what `validate(seed)` checks.
10. **Anti-Patterns** — engine-specific things to avoid.
11. **References** — papers, libraries, prior art.

## Adding a New Engine

See [`architecture/engine-pattern.md`](../architecture/engine-pattern.md) §Adding a New Engine for the 10-step process. The minimal work for a simple domain is 1–3 days; a complex domain takes 1–3 weeks.

## Engine Tiers

For prioritization purposes, engines are grouped into tiers based on user demand and platform leverage:

- **Tier 1 (must-have for MVP):** Sprite, Character, Music, FullGame, Geometry3D, Animation
- **Tier 2 (high value):** Visual2D, Audio, UI, Narrative, Procedural
- **Tier 3 (specialized):** Physics, Game, Ecosystem, ALife
- **Tier 4 (planned expansion):** the 11 unimplemented domains

The MVP build order is documented in [`roadmap/build-order.md`](../roadmap/build-order.md).
