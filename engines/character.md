# Character Engine

## Overview

Produces a 3D humanoid (or non-humanoid) character with morphology, personality, animation rig, archetype-driven rendering, and metadata. 3,615 LOC, 7 stages. Output is a glTF mesh with skeleton, skinning weights, animation clips, and a JSON personality manifest. The Character engine is the canonical "complex multi-faceted" engine and is the primary input to most cross-domain functors.

## Gene Schema

| Gene | Type | Range | Required | Description |
|---|---|---|---|---|
| `archetype` | categorical | enum {warrior, mage, rogue, ranger, paladin, monk, bard, druid, custom} | yes | Base identity |
| `species` | categorical | enum {human, elf, dwarf, halfling, orc, beast, construct, custom} | yes | Body morph |
| `body_morph` | vector(8) | each [0, 1] | yes | Height, build, proportions |
| `personality` | vector(6) | each [-1, 1] | yes | Aggression, warmth, complexity, curiosity, melancholy, confidence |
| `outfit` | struct | per-archetype slots | yes | Clothing/armor selection |
| `palette` | array<vector(3)> | 4..12 OKLab colors | yes | Skin/hair/clothes colors |
| `signature_pose` | categorical | enum from animation library | yes | Default rest pose |
| `voice_signature` | vector(4) | each [0, 1] | no | Pitch, timbre, breathiness, accent (for music functor) |

## Stage Pipeline

```
1. extract        : Seed                     -> CharWorking
2. morphogenesis  : CharWorking              -> Skeleton + base mesh
3. personality    : Skeleton                 -> AnimatedRig
4. archetype      : AnimatedRig              -> EquippedCharacter
5. texture        : EquippedCharacter        -> ShadedCharacter
6. compose        : ShadedCharacter          -> CharacterBundle
7. export         : CharacterBundle          -> CharacterArtifact
```

## Stage Details

### Stage 2 — `morphogenesis`

Generate base humanoid (or species-specific) skeleton and skin mesh from `body_morph` parameters. Heights/limb lengths/torso width are interpolated from per-species reference rigs. Skinning weights are computed from a heat-diffusion solver.

### Stage 3 — `personality`

Project the 6-dim personality vector onto an animation pose space. The signature pose is biased: high-aggression characters lean forward with weapon raised; high-warmth characters stand open and relaxed. The "personality" of the rig manifests as resting micro-poses and idle animation cadence.

### Stage 4 — `archetype`

Apply outfit and equipment from the archetype's slot table. Warrior → armor + weapon; mage → robe + staff; rogue → leathers + dagger. Slots are filled deterministically from the outfit struct.

### Stage 5 — `texture`

Apply skin tone, hair color, fabric textures, metal materials. Uses OKLab to ensure shading consistency. Metal materials use PBR (roughness/metalness) parameters derived from archetype defaults.

### Stage 6 — `compose`

Bundle the mesh, skeleton, animations, materials, and personality manifest into a single glTF binary.

### Stage 7 — `export`

Wrap as `.glb` (binary glTF) plus a sidecar `personality.json`.

## Render Hints

```ts
{ viewportMode: '3d', defaultCamera: { position: [0, 1.6, 3], target: [0, 1.0, 0] }, supportsAnimation: true }
```

## Export Hints

`['glb', 'gltf', 'fbx', 'usd', 'godot_character', 'unity_character']`. Recommended: `glb`.

## Fitness Hints

Meaningful axes: geometry, texture, animation, coherence, style, novelty (all 6).
Default MAP-Elites descriptors: `strength`, `agility` (both derived from body_morph + personality).

## Determinism Notes

- Mesh vertices canonicalized to 7 decimal digits before glTF export.
- Skinning weight solver uses fixed iteration count and tie-breaking by vertex index.
- All animation curves are evaluated at fixed sub-step rate (60 Hz) for consistent frame timing.

## Validation Rules

- All required genes present.
- `body_morph` dimensions match the species' parameter count.
- `outfit` slots match the archetype's slot schema.
- `palette` size 4..12.

## Anti-Patterns

- Never modify the skeleton in `archetype` (it's frozen after `morphogenesis`).
- Don't compose two archetypes; use the `character_to_fullgame` functor for multi-character scenes.

## References

- Pinocchio: Automatic Rigging and Animation of 3D Characters (Baran & Popović, 2007)
- glTF 2.0 spec
- OpenPBR Surface specification
