# Sprite Engine

## Overview

The Sprite engine produces 2D character and object sprites with palette-coherent shading, multi-frame animation, and a frame atlas. It is the largest implemented engine in the codebase (3,673 LOC, 8 stages) and serves as the canonical reference for the engine pattern. Output is a PNG atlas plus a JSON manifest describing frame layout, hitboxes, and animation timing.

## Gene Schema

| Gene Name | Type | Range / Constraint | Required | Description |
|---|---|---|---|---|
| `body_template` | categorical | enum {humanoid, quadruped, avian, serpentine, insectoid, custom} | yes | Base topology |
| `size` | categorical | enum {16x16, 32x32, 48x48, 64x64, 128x128} | yes | Sprite cell size |
| `palette` | array<scalar> | 4..16 OKLab colors | yes | Color palette |
| `silhouette_complexity` | scalar | [0, 1] | yes | Outline detail |
| `outline_color` | vector(3) | each [0, 1] in OKLab | no | Outline color |
| `animation_set` | array<categorical> | from {idle, walk, run, jump, attack, defend, die, cast, dash, climb, swim, fall} | yes | Animations to generate |
| `joint_proportions` | vector(N) | each [0.5, 2.0] | no | Per-joint scaling |
| `weapon_attachment` | categorical | enum {none, sword, bow, staff, shield, dual_wield} | no | Equipment |
| `eye_style` | categorical | enum {dot, oval, slit, glowing, none} | yes | Eye rendering |
| `mouth_style` | categorical | enum {none, line, fanged, smile, frown} | no | Mouth rendering |

## Stage Pipeline

```
1. extract        : Seed                       -> SpriteWorking
2. morphogenesis  : SpriteWorking              -> BodyParts
3. parameterize   : BodyParts                  -> ParameterizedRig
4. texture        : ParameterizedRig           -> ColoredRig
5. pose           : ColoredRig                 -> AnimationFrames
6. compose        : AnimationFrames            -> Atlas
7. render         : Atlas                      -> RasterAtlas
8. export         : RasterAtlas                -> SpriteArtifact
```

## Stage Details

### Stage 1 — `extract`

```
fn extract(seed):
    return SpriteWorking {
        body_template:         seed.genes["body_template"].value,
        size:                  parse_size(seed.genes["size"].value),
        palette:               seed.genes["palette"].value,         // OKLab[]
        silhouette_complexity: seed.genes["silhouette_complexity"].value,
        outline_color:         seed.genes["outline_color"]?.value ?? oklab(0.1, 0.0, 0.0),
        animation_set:         seed.genes["animation_set"].value,
        joint_proportions:     seed.genes["joint_proportions"]?.value ?? [],
        weapon_attachment:     seed.genes["weapon_attachment"]?.value ?? "none",
        eye_style:             seed.genes["eye_style"].value,
        mouth_style:           seed.genes["mouth_style"]?.value ?? "none",
    }
```

### Stage 2 — `morphogenesis`

Compose body parts from the body_template field. Templates are parameterized: `humanoid` produces head/torso/arms/legs at proportions specified by `joint_proportions`. The output is a list of part shapes in pixel coordinates relative to the sprite's bounding box.

```
fn morphogenesis(working, seed, rng):
    template = lookup_body_template(working.body_template)
    parts = []
    for part in template.parts:
        scale = working.joint_proportions[part.joint_index] ?? 1.0
        shape = generate_part_shape(part, scale, working.silhouette_complexity, rng)
        parts.push(BodyPart { name: part.name, shape, joint: part.joint, z: part.z_index })
    return BodyParts { parts, bounding_box: union(parts.map(p => p.shape.bbox)) }
```

### Stage 3 — `parameterize`

Compute joint positions, eye positions, weapon attachment points, mouth position. These are derived from the body parts and are used by later stages.

```
fn parameterize(parts, seed, rng):
    joints = compute_joint_positions(parts)
    eyes   = compute_eye_positions(parts, working.eye_style)
    mouth  = compute_mouth_position(parts, working.mouth_style)
    weapon = compute_weapon_attachment(parts, working.weapon_attachment)
    return ParameterizedRig { parts, joints, eyes, mouth, weapon }
```

### Stage 4 — `texture`

Generate the per-pixel palette using OKLab color science. Each part is shaded with a base color from the palette, with optional dithered shadows and highlights. The OKLab color space is used because it has perceptually uniform lightness, so shadows and highlights look natural across the full palette.

```
fn texture(rig, seed, rng):
    colored = []
    for part in rig.parts:
        base_color = pick_base_color(part, working.palette, rng)
        shadow = oklab_darken(base_color, 0.15)
        highlight = oklab_lighten(base_color, 0.10)
        pixel_grid = rasterize_part_with_shading(part, base_color, shadow, highlight)
        colored.push(ColoredPart { part, pixel_grid })
    return ColoredRig { rig, colored, outline: working.outline_color }
```

### Stage 5 — `pose`

Compute frames for each animation in the animation_set. Each animation has a number of frames and a timing curve. For each frame, joint positions are interpolated and parts are transformed to match the pose.

```
fn pose(colored_rig, seed, rng):
    all_frames = {}
    for anim_name in working.animation_set:
        anim_template = lookup_animation_template(anim_name)
        frames = []
        for t in anim_template.timing_curve:
            joint_state = interpolate_joints(colored_rig.rig.joints, anim_template.keyframes, t)
            frame = transform_parts_by_joints(colored_rig, joint_state)
            frames.push(frame)
        all_frames[anim_name] = frames
    return AnimationFrames { all_frames }
```

### Stage 6 — `compose`

Combine all frames into a sprite atlas. Frames are packed into a grid layout that minimizes wasted pixels. The frame map records each frame's (animation, frame_index) → atlas (x, y).

```
fn compose(animation_frames, seed, rng):
    flat = flatten_frames(animation_frames)
    layout = pack_atlas(flat, working.size)
    return Atlas { layout, frame_map: build_frame_map(layout) }
```

### Stage 7 — `render`

Rasterize the atlas to a flat pixel grid with alpha. Each frame's pixels are blitted into the atlas grid at its packed position.

```
fn render(atlas, seed, rng):
    raster = blank_image(atlas.layout.width, atlas.layout.height)
    for frame in atlas.layout.frames:
        blit(raster, frame.pixel_grid, frame.x, frame.y)
    return RasterAtlas { raster, frame_map: atlas.frame_map }
```

### Stage 8 — `export`

Encode as PNG with metadata. The JSON manifest is built from the frame map and includes per-animation timing.

```
fn export(raster_atlas, seed, rng):
    png_bytes = encode_png(raster_atlas.raster)
    metadata = {
        format_version: "1",
        sprite_size: working.size,
        animations: build_animation_metadata(raster_atlas.frame_map, working.animation_set),
        hitboxes: compute_hitboxes(raster_atlas.frame_map),
    }
    return SpriteArtifact {
        png: png_bytes,
        metadata: metadata,
        manifest: json_encode(metadata),
    }
```

## Render Hints

```ts
const renderHints: RenderHints = {
  viewportMode: '2d',
  defaultCamera: null,
  thumbnailSize: { width: 256, height: 256 },
  supportsAnimation: true,
};
```

## Export Hints

```ts
const exportHints: ExportHints = {
  formats: ['png', 'png+json', 'godot_sprite', 'unity_sprite', 'aseprite', 'spine', 'dragonbones'],
  recommendedFormat: 'png+json',
  containerOptions: {
    atlas_padding: 2,
    power_of_two: false,
  },
};
```

## Fitness Hints

```ts
const fitnessHints: FitnessHints = {
  meaningfulAxes: ['geometry', 'texture', 'animation', 'coherence', 'style'],
  defaultDescriptors: ['silhouette_complexity', 'palette_diversity'],
};
```

(novelty axis is meaningful but secondary; sprite novelty is dominated by silhouette and palette which are already descriptors.)

## Determinism Notes

- **Strictness:** exact bytes (per [`spec/07-determinism.md`](../spec/07-determinism.md)).
- All coordinates are integer pixel positions.
- Color computations use OKLab in IEEE-754 binary64 with a fixed-precision rounding pass at the end so two implementations produce bit-identical RGB.
- Atlas packing uses a deterministic shelf-pack algorithm; ties broken by frame name lexicographic order.
- PNG encoding uses fixed compression level (6) and fixed filter strategy (sub) — different libraries with these settings produce identical bytes.

## Validation Rules

`validate(seed)` checks:

- `body_template` is one of the enum values.
- `size` is one of the enum values.
- `palette` has 4..16 entries; each is a valid OKLab triple with L in [0, 1] and a, b in [-0.5, 0.5].
- `animation_set` has 1..12 entries from the enum.
- `joint_proportions` length matches the joint count for the chosen body_template.
- The atlas predicted from `(animation_set, size)` fits within 4096×4096 (engine maximum).

## Anti-Patterns

- **Don't combine two body templates in morphogenesis.** If you want a humanoid+avian creature, use cross-domain composition (e.g., a `monster` engine), not multi-template fusion in this engine.
- **Don't add per-frame procedural effects in `pose`.** Pose is structural; effects belong in a separate `effects` stage if needed (and currently they're not — the engine is intentionally minimal).
- **Don't bypass the palette.** All colors must come from the palette gene; the engine never invents arbitrary RGB values.

## References

- Björn Ottosson, *A perceptual color space for image processing* (OKLab, 2020)
- Aseprite documentation for sprite atlas conventions
- libspine + DragonBones rigging conventions for export compatibility
