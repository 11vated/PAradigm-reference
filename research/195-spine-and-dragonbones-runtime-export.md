# 195 — Spine and DragonBones runtime export

## Question
What is the export pipeline that produces Spine and DragonBones runtime data from substrate `animation.skeleton` (Brief 161) and `animation.clip` gseeds, with parity-tested skeletal animation data interchange across the eight target engines?

## Why it matters (blast radius)
Spine and DragonBones are the two dominant 2D skeletal animation formats. Every major engine has runtime libraries for both. Producing parity-tested Spine/DragonBones output means substrate skeletal animations work in any engine that has a Spine or DragonBones runtime — including engines beyond the eight in Tier D. This brief turns substrate skeletal animation into a universal interchange artifact.

## What we know from the spec
- Brief 161 — animation runtime namespace (skeletal, blend trees, IK, root motion, retargeting).
- Brief 179 — animation editor specification.
- Brief 188 — Godot export pipeline.
- Brief 189 — Unity export pipeline.
- Brief 190 — Unreal export pipeline.
- Brief 191 — Phaser export pipeline.
- Brief 192 — GameMaker export pipeline.
- Brief 194 — Defold and Cocos.

## Findings
1. **Spine runtime data format.** Spine exports as `.json` (skeleton data) + `.atlas` (texture atlas with regions) + `.png` (atlas images). The JSON describes bones, slots, attachments, animations, transform constraints, IK constraints, path constraints. The substrate's `animation.skeleton` schema maps structurally to Spine's skeleton schema.
2. **DragonBones runtime data format.** DragonBones exports as `_ske.json` (skeleton) + `_tex.json` (atlas) + `_tex.png`. The schema is similar to Spine with naming differences (slot → display, attachment → display, etc.).
3. **Substrate → Spine mapping.** Brief 161 bones → Spine bones (1:1 with name + parent + length + rotation/translation/scale). Brief 161 slots / attachments → Spine slots / region attachments. Animation timelines → Spine timelines per channel type. IK chains → Spine IK constraints (Spine supports 1-bone, 2-bone, and N-bone IK).
4. **Substrate → DragonBones mapping.** Same structure as Spine with field renaming. Substrate ships dual emitters that share the same canonical AST.
5. **Atlas packing.** Substrate atlas (Brief 161 / 179) re-packs to Spine `.atlas` format on export. Frame names preserved per Brief 179's frame-name stability contract.
6. **IK solver semantics.** Spine IK uses analytic 2-bone for 2-bone chains and CCD for longer chains. Substrate's FABRIK IK does not match Spine's CCD bit-for-bit. Mitigation: at export, the substrate IK solver chooses the closest Spine equivalent and writes it; the substrate runtime IK solver remains the source of truth for replay determinism inside substrate exports, while Spine-runtime exports use Spine's solver.
7. **Mesh deformation.** Spine and DragonBones support mesh deformation with weighted vertices. Substrate's animation runtime supports mesh deformation as a typed channel; the exporter writes Spine mesh attachments with vertex weights.
8. **Cross-engine consumption.** Once exported as Spine `.json`, the data can be consumed by official Spine runtimes for Godot / Unity / Unreal / Phaser / GameMaker / Cocos / Defold / HTML5. The substrate exporter does not need to re-emit per-engine — engines load Spine data via their native Spine runtime libraries. This dramatically reduces export complexity for skeletal animation.
9. **Round-trip semantics.** A `.json` Spine file can be re-imported via Brief 089's universal pipeline back into a substrate `animation.skeleton` gseed. Round-trip is bit-stable when no editing happens between export and re-import.
10. **Substrate-native extensions to Spine.** Some substrate features (e.g., Brief 161's blend tree, Brief 161 retargeting) have no Spine equivalent. Mitigation: blend trees and retargeting metadata ride alongside the Spine `.json` as a substrate-specific sidecar `.substrate.json` file that substrate runtimes load and Spine runtimes ignore.
11. **Versioning.** Spine 4.0+ is the v0.1 floor; older Spine versions deferred. DragonBones 5.7+ is the v0.1 floor. Both have stable JSON schemas at these versions.
12. **Licensing.** Spine is commercial (Esoteric Software); the substrate's exporter writes data in Spine's documented JSON format without using Spine's tooling — no license dependency on Esoteric Software for the data interchange. Creators wishing to *edit* exported Spine files in Spine's editor need their own Spine license. DragonBones is open-source MIT.

## Risks identified
- **Spine schema evolution.** Spine's JSON schema has changed across major versions (3.x → 4.0). Mitigation: target Spine 4.0+ schema; CI runs against multiple Spine versions when 4.x progresses.
- **IK solver divergence.** As noted in #6, Spine's CCD doesn't match substrate FABRIK. Mitigation: document the divergence; substrate exports default to using Spine's solver in Spine-runtime contexts and substrate's solver in substrate-runtime contexts; replay verifier marks Spine-runtime IK as "external solver" and skips bit-comparison.
- **Atlas constraints.** Spine atlases have packing constraints (POT sizes, padding rules) that substrate atlases may not satisfy. Mitigation: export-time re-pack with Spine-compatible settings; sign-time validation that resulting atlas fits Spine's constraints.
- **Sidecar file fragmentation.** Substrate-specific extensions in `.substrate.json` are easy to lose. Mitigation: bundle Spine + sidecar in a single `.substrate.skel` archive (zstd-compressed tar) for substrate-runtime contexts; emit raw Spine files only when targeting external Spine runtimes.
- **DragonBones popularity decline.** DragonBones is less actively maintained than Spine. Mitigation: support but don't prioritize; deprecate if upstream stops shipping.

## Recommendation
Specify Spine and DragonBones export as a single dual-format emitter producing `.json` skeleton data + `.atlas` + atlas images, with substrate-specific extensions in a sidecar `.substrate.json`. Use Spine 4.0+ and DragonBones 5.7+ as v0.1 floors. Default skeletal animation in any engine target to Spine-runtime consumption — engines load via their native Spine runtimes rather than re-exporting per-engine. Document IK solver divergence honestly.

## Confidence
**4.5 / 5.** Spine and DragonBones formats are well-documented, and the 1:1 structural mapping with Brief 161 is mostly mechanical. The novelty is the substrate-extension sidecar pattern, the dual emitter from one canonical AST, and the cross-engine consumption strategy that bypasses per-engine re-emission. Lower than 5 because IK divergence may produce visible runtime differences that need Phase-1 measurement.

## Spec impact
- New spec section: **Spine and DragonBones runtime export specification**.
- Adds `.substrate.skel` archive format and `.substrate.json` sidecar specification.
- Adds documentation of substrate-FABRIK vs Spine-CCD divergence with the export-time solver-selection contract.
- Cross-references Briefs 089, 161, 179, 188-194.

## New inventions
- **INV-808** — Substrate-extension sidecar `.substrate.json` riding alongside Spine `.json`: substrate features Spine lacks (blend trees, retargeting, custom timelines) preserved without breaking Spine compatibility.
- **INV-809** — Cross-engine Spine consumption strategy: skeletal animation exports as Spine data once, consumed by every engine via its native Spine runtime, eliminating per-engine re-emission.
- **INV-810** — `.substrate.skel` zstd-compressed bundle of Spine + sidecar: single-file distribution for substrate-runtime contexts.
- **INV-811** — Dual-format emitter (Spine + DragonBones) from one canonical animation AST: maintain once, emit twice.
- **INV-812** — Documented IK solver divergence with export-time solver selection: substrate-FABRIK in substrate runtimes, Spine-CCD in Spine runtimes, with replay verifier flagging external-solver scenes.

## Open follow-ups
- Spine 4.x minor version tracking (incremental).
- 3D Spine equivalent (Spine is 2D-only; 3D skeletal interchange is glTF; covered by Brief 219 asset import).
- DragonBones decline contingency planning (deprecate if upstream stops shipping).
- Spine editor round-trip (creator edits in Spine, re-imports to substrate) — deferred to v0.3.
- Mesh deformation parity test against Spine reference (Phase 1 measurement).

## Sources
1. Brief 089 — Universal anything-to-gseed pipeline.
2. Brief 161 — Animation runtime namespace.
3. Brief 179 — Animation editor specification.
4. Briefs 188-194 — engine export pipelines.
5. Spine User Guide (esotericsoftware.com/spine-user-guide).
6. Spine JSON format reference (esotericsoftware.com/spine-json-format).
7. DragonBones documentation (dragonbones.com).
