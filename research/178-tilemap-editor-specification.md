# 178 — Tilemap editor specification

## Question
What is the creator-facing tilemap editor surface that authors `tilemap.layer` and `tilemap.tileset` (Brief 173) gseeds with autotile preview, deterministic procgen overlays, and signed lineage on every brush stroke?

## Why it matters (blast radius)
Tilemaps are the densest-edit surface in 2D game creation — a single creator session can land thousands of cell mutations. If the editor commits per-cell, the lineage explodes; if it commits per-stroke without atomic semantics, undo is incoherent. Autotile preview must match what the runtime resolver produces, or creators see one thing in the editor and another at runtime — the worst possible class of bug for the seven-axis discipline.

## What we know from the spec
- Brief 173 — `tilemap.layer`, `tilemap.tileset`, 47-tile and 16-tile autotile bitmasks, 8 procgen primitives.
- Brief 172 — `level.scene` composition with tilemap as a child.
- Brief 177 — scene editor as modifier surface; tilemap editor inherits the same contract.
- Brief 052 — lineage rewind / replay.
- Brief 088A — canonical seed armory feeds tileset gseeds.

## Findings
1. **Brush stroke as atomic mutation.** A "stroke" is everything between mouse-down and mouse-up. The editor accumulates per-cell changes in a typed `tilemap.stroke_buffer` ephemeral and commits one signed `tilemap.layer.stroke` mutation on mouse-up. Sign-time validation runs once per stroke, not once per cell. (Inherits Brief 177's gizmo-batch contract.)
2. **Brush types.** v0.1 ships eight brush primitives: single-cell, rectangle, line, fill (4-connected), fill (8-connected), random-from-set, autotile-paint, eraser. Each is a typed function over the stroke buffer. Custom brushes are `tilemap.brush` gseeds composing these primitives.
3. **Autotile preview.** As the creator paints, the editor runs the same 47-tile or 16-tile autotile bitmask resolver Brief 173 specifies for runtime. There is no separate "editor approximation" — preview *is* runtime. This eliminates the editor/runtime divergence class of bugs.
4. **Layer model.** A `tilemap.layer` is one z-ordered grid. Multiple layers stack within a `tilemap.composition` typed gseed with explicit z-index, parallax factor (Brief 155), and opacity. Layer reorder is a typed mutation; toggle-visibility is editor-runtime ephemeral, not signed.
5. **Animated tiles.** A tileset entry can declare a typed `animation_cycle` (frames, durations, loop policy). The editor renders the cycle in the palette and on the canvas at the editor's preview rate, but the gseed stores only the cycle definition — runtime advances the cycle on the fixed tick (Brief 152).
6. **Collision painting.** Tilemap cells can carry typed `collision_tag` overlays painted with a separate brush. The collision overlay is a parallel layer with the same dimensions; the editor renders it as a colored mask. Collision shape per tile is declared on the tileset entry, not the layer cell.
7. **Procgen overlay.** The creator can drop a Brief 173 procgen primitive (WFC, BSP, drunkards-walk, etc.) onto a layer region. The procgen runs with a creator-supplied seed and writes its output as one signed batch mutation. The seed and the procgen primitive's gseed are recorded in the lineage so the same region can be re-rolled deterministically. (Brief 173 `procgen.seed_record`.)
8. **Hand-edit after procgen.** Once procgen has placed cells, the creator can paint over the result. The lineage tracks the procgen ancestor and the subsequent hand-edits independently — Brief 173's "fork-and-hand-edit" lineage is a first-class editor operation.
9. **Tileset import.** A tileset is imported via the universal anything-to-gseed pipeline (Brief 089). The editor's "import sprite sheet" button compiles to a typed `tileset.import` mutation that runs the pipeline and produces a signed `tilemap.tileset` gseed.
10. **Marquee selection and copy/paste.** Selecting a region produces a typed `tilemap.region` ephemeral. Copy serializes it to the OS clipboard as a JCS-canonical text fragment per Brief 003. Paste compiles to a stroke mutation. Cross-document paste is identical because the format is JCS.
11. **Layer-spanning operations.** "Replace tile X with tile Y across all layers" is one signed batch mutation; "flood-fill across layers" is rejected as ambiguous and the editor refuses it.
12. **Visualization aids.** Grid overlay, chunk boundaries (per Brief 158 partial save chunks), tile coordinates, and bitmask debug view are editor-runtime overlays — none persist to the gseed.

## Risks identified
- **Stroke buffer overflow.** A creator dragging across a 10k-cell region in one stroke would produce a single multi-megabyte mutation. Mitigation: stroke buffer caps at 4096 cell deltas; over the cap, the stroke auto-splits into chunked sub-strokes that still appear as one undo step in the editor but multiple mutations in the lineage.
- **Autotile divergence on import.** A third-party tileset may not conform to the 47/16-tile bitmask. Mitigation: import pipeline validates the tileset against the bitmask grammar and rejects malformed sets with a typed error pointing at the offending tile index.
- **Procgen seed reproducibility across editor versions.** If the editor's RNG implementation changes, old seeds could produce different output. Mitigation: procgen primitives are versioned (Brief 018), and the seed record carries the primitive version. The editor refuses to re-roll a stale-version seed without an explicit "upgrade" confirmation.
- **Animated tile preview cost in large maps.** Animating 10k tiles in the editor at 60fps is non-trivial. Mitigation: animation preview is opt-in per layer; off by default for layers above a configurable cell-count threshold.

## Recommendation
Specify the tilemap editor as a stroke-atomic surface inheriting Brief 177's modifier-surface contract. Ship 8 brush primitives at v0.1, autotile preview that *is* the runtime resolver, procgen overlay with lineage-tracked re-roll, and JCS clipboard interop. Defer 3D voxel painting to v0.4 (Brief 173 already defers voxel procgen). Cap stroke buffers at 4096 cell deltas with auto-chunking.

## Confidence
**4.5 / 5.** Tilemap editing is well-understood (Tiled, Aseprite, Godot's TileMap node, Unity's 2D Tilemap, LDtk all converge on similar primitives). The novelty is the stroke-atomic signing contract, the procgen-overlay-as-lineage-fork pattern, and the editor-equals-runtime autotile guarantee — each follows mechanically from prior briefs.

## Spec impact
- New spec section: **Tilemap editor surface specification**.
- Adds `tilemap.brush` typed gseed (composable brush primitive).
- Adds the stroke-buffer cap and auto-chunk policy to `tilemap.layer.stroke` mutation contract.
- Cross-references Brief 177 for the inherited modifier-surface contract.

## New inventions
- **INV-725** — Stroke-atomic tilemap mutation with 4096-cell auto-chunking: brush strokes commit as one signed mutation per stroke, with auto-split for oversized strokes that preserves single-undo semantics.
- **INV-726** — Editor-equals-runtime autotile resolver: the editor's autotile preview is literally the same code path the runtime uses, eliminating editor/runtime divergence.
- **INV-727** — Procgen-overlay-as-lineage-fork: dropping a procgen primitive onto a region records the primitive, the seed, and the version in the lineage so re-roll is deterministic and hand-edits are tracked as forks.
- **INV-728** — JCS-canonical tilemap clipboard format: copy/paste interop across documents and federation peers uses Brief 003's canonical form so cross-substrate paste is bit-equivalent.

## Open follow-ups
- 3D voxel painting (deferred to v0.4 with Brief 173).
- Hexagonal and isometric grid topology (specified in `tilemap.layer.topology` field; editor support deferred to v0.2).
- Real-time collaborative tilemap editing across peers (deferred to v0.3).
- Brush macros (record-and-replay a sequence of strokes) — deferred to v0.2.

## Sources
1. Brief 003 — JCS canonicalization.
2. Brief 018 — Versioning and compatibility.
3. Brief 089 — Universal anything-to-gseed pipeline.
4. Brief 152 — Game loop and tick model.
5. Brief 158 — Save / load partial chunks.
6. Brief 173 — Tilemap and procedural generation.
7. Brief 177 — Scene and level editor specification.
8. LDtk editor design notes (deepnight.net/tools/ldtk/).
9. Godot 4.x TileMap and TileSet documentation.
