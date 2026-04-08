# 221 — Asset pipeline and import tooling

## Question
What is the typed asset pipeline and import tooling that ingests external creator assets (PNG / WAV / OGG / GLTF / FBX / Tiled / LDtk / Aseprite / Blender / Spine / DragonBones / Tiled-tilemap / OGMO) and emits typed substrate gseeds, with content hashing, deduplication, and dependency tracking — bridging the substrate's typed surface to the creator's existing tool ecosystem?

## Why it matters (blast radius)
Creators don't draw sprites in the substrate — they use Aseprite, Photoshop, Krita, Blender. They don't compose music in the substrate — they use Ableton, FL Studio, Reaper. The substrate is the assembly point, not the asset creation surface. Without typed import, every asset format becomes a creator integration burden. With it, the substrate ingests the creator's existing tool output as typed gseeds with full provenance.

## What we know from the spec
- Brief 089 — universal anything-to-gseed conversion (substrate-foundational).
- Brief 152 — substrate signing and lineage.
- Brief 187 — mod and plugin surface.
- Brief 217 — CLI and headless toolchain.

## Findings
1. **`gspl import` subcommand.** CLI subcommand `gspl import <file>` detects file format and ingests into a typed gseed. `gspl import --watch <dir>` runs in watch mode for continuous ingestion during creator workflows.
2. **Format detection.** Detection by file magic bytes + extension. Substrate ships built-in importers for: PNG / JPG / WebP (image gseeds), WAV / OGG / FLAC / MP3 (audio gseeds), GLTF / GLB (3D mesh gseeds), FBX (3D mesh + skeletal gseeds), Aseprite (sprite + animation gseeds), Tiled `.tmx` / `.tsx` (tilemap gseeds), LDtk (level + tilemap gseeds), Spine `.json` / `.skel` (skeletal animation gseeds), DragonBones (skeletal animation gseeds), Blender `.blend` (via Blender CLI bridge), OGMO (level gseeds), font formats `.ttf` / `.otf` / `.woff` (font gseeds).
3. **Content-addressed storage.** Imported assets are stored content-addressed by typed BLAKE3 hash. Identical files imported multiple times deduplicate to one storage entry. Lineage records the original filename and import timestamp.
4. **Typed metadata extraction.** Importers extract typed metadata: image dimensions and color space, audio sample rate and channel count, mesh vertex count and material list, animation frame count and rig structure. Metadata is part of the gseed schema.
5. **Re-import detection.** Watch mode detects file changes and re-imports automatically. Lineage records the re-import as a typed `asset.update` mutation referencing the prior gseed. Existing references re-resolve.
6. **Dependency graph.** Imported assets and the gseeds that reference them form a typed dependency graph. `gspl deps <gseed>` queries the graph; orphan assets (referenced by nothing) are flagged.
7. **Source-of-truth tracking.** Every imported gseed records the source filepath, source format, source tool version (where detectable), and the importer version. Provenance is queryable.
8. **Importer plugin API.** Brief 187 mods can register typed `importer.plugin` capability declaring: file extensions handled, magic-byte signatures, output gseed kinds. Creators extend the importer set without forking substrate.
9. **Color space handling.** Image importers detect color space (sRGB / linear / Display-P3) and store typed color space in the image gseed. Substrate runtime handles color space conversion at render time.
10. **Texture compression.** Optional `gspl import --compress` runs platform-specific texture compression (BC7 / ASTC / ETC2) and stores compressed variants alongside the source. Engine export pipelines select the appropriate variant per target.
11. **Audio normalization.** Audio importers can optionally normalize loudness (typed `import.loudness_target` field, default -16 LUFS) and emit a normalized variant alongside the source.
12. **Asset bundles.** Multiple imports can be bundled into a typed `asset.bundle.gseed` for distribution as a single signed unit. Bundles compose for asset packs / DLC distribution.
13. **Validation contract.** Sign-time gates: file format detected, importer plugin registered, content hash computed, metadata extracted, source provenance recorded.

## Risks identified
- **Format coverage.** 13+ formats is a maintenance burden. Mitigation: built-in importers cover the dominant formats; rare formats use plugin importers via Brief 187.
- **Re-import drift.** Watch mode re-imports can break references if metadata changes incompatibly. Mitigation: typed metadata-compatibility check on re-import; incompatible changes require explicit creator confirmation.
- **Texture compression cost.** Compression is CPU-intensive. Mitigation: compression is opt-in per import; CI pipelines compress; local watch mode skips by default.
- **Source tool dependency.** Blender / Aseprite imports need the source tool installed for some metadata. Mitigation: importer falls back to standalone parsing where possible; documents which features need the source tool.

## Recommendation
Specify the asset pipeline as a `gspl import` subcommand handling 13 built-in formats with content-addressed storage, typed metadata extraction, watch mode, dependency graph queries, source provenance, importer plugin API, color space handling, optional texture compression and audio normalization, and typed asset bundles.

## Confidence
**4 / 5.** Asset import patterns are well-precedented (Unity / Unreal / Godot importers). The novelty is the substrate's content-addressed deduplication and full provenance lineage. Lower than 4.5 because Blender `.blend` parsing without Blender installed needs Phase-1 measurement.

## Spec impact
- New spec section: **Asset pipeline and import tooling specification**.
- Adds the `gspl import` subcommand contract.
- Adds the 13 built-in importer list with format requirements.
- Adds the `importer.plugin` Brief 187 capability.
- Adds the `asset.bundle.gseed` typed kind.
- Cross-references Briefs 089, 152, 187, 217.

## New inventions
- **INV-968** — `gspl import` subcommand with 13 built-in format importers covering the dominant creator tool ecosystem: substrate ingests existing creator output without forcing tool migration.
- **INV-969** — Content-addressed storage of imported assets via BLAKE3 hash with automatic deduplication: identical assets exist exactly once regardless of import path.
- **INV-970** — Typed metadata extraction per importer with full schema integration: imported assets carry their structural metadata as substrate-typed fields.
- **INV-971** — Watch-mode re-import with typed `asset.update` mutation preserving lineage: creator workflows (paint in Aseprite, save, see the substrate update) work continuously.
- **INV-972** — Dependency graph queryable via `gspl deps`: orphan assets and reference chains are first-class queries.
- **INV-973** — Importer plugin API via Brief 187 capability for creator-supplied formats: substrate import surface is extensible without forking.
- **INV-974** — Source provenance tracking on every imported gseed (filepath / format / tool version / importer version): asset provenance is fully auditable.
- **INV-975** — Optional texture compression and audio normalization variants stored alongside source: engine export targets select appropriate variant without re-import.
- **INV-976** — Typed `asset.bundle.gseed` for signed multi-asset distribution: asset packs and DLC are first-class substrate primitives.

## Open follow-ups
- USD (Universal Scene Description) importer — deferred to v0.3.
- Substance Painter / Designer importer — deferred to v0.4.
- Phase-1 Blender bridge implementation.
- Asset hot-reload protocol for live engine targets — Phase 1.
- Audio middleware (Wwise / FMOD) project import — deferred to v0.4.

## Sources
1. Brief 089 — Universal anything-to-gseed conversion.
2. Brief 152 — Substrate signing and lineage.
3. Brief 187 — Mod and plugin surface.
4. Aseprite file format documentation.
5. Tiled `.tmx` format specification.
6. LDtk JSON schema.
7. Spine runtime documentation.
8. GLTF 2.0 specification (Khronos).
9. BLAKE3 hash specification.
10. Unity asset import pipeline documentation.
11. Godot resource importer documentation.
