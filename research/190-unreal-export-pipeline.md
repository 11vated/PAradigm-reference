# 190 — Unreal export pipeline

## Question
What is the export pipeline that produces a complete Unreal Engine 5.x project from a signed GSPL gseed bundle, with Blueprint + C++ outputs, uasset resource serialization, Niagara/Chaos integration, and AAA-quality 3D-first parity?

## Why it matters (blast radius)
Unreal is the AAA path. Per Brief 072, "GSPL surpasses Unreal at AAA 3D rendering" requires that substrate gseeds at minimum *export to* Unreal at parity. If the export drops fidelity, the substrate's structural advantage becomes a step-backward at the most demanding visual surface.

## What we know from the spec
- Brief 072 — beating Unreal at AAA 3D rendering.
- Brief 188 — Godot export pipeline (the reference exporter).
- Brief 189 — Unity export pipeline.
- Brief 020 — determinism contract per engine.
- Brief 065 — game engines deep dive.
- Briefs 152-176.

## Findings
1. **Emitter graph inheritance.** Inherits Brief 188's typed `export.target` graph. Unreal-specific target declares: target UE version (5.3+), template (Blank / Top-Down / Third-Person / First-Person / 2D), Lumen / Nanite enablement, target platforms.
2. **Project format.** UE projects are a `.uproject` JSON descriptor + `Source/` (C++) + `Content/` (uasset binary) + `Config/` (ini). The exporter generates all four directories with substrate-derived contents.
3. **Scene mapping.** `level.scene` (Brief 172) → UE `.umap` Level asset (binary uasset). Entities (Brief 153) become Actors with attached ActorComponents. The substrate's archetype maps to UE Actor classes generated as C++ headers under `Source/SubstrateGen/`.
4. **Blueprint vs C++.** Pure-data gseeds export as Data Assets (UE's ScriptableObject analog) editable in the Blueprint editor. Logic-bearing gseeds emit as C++ classes with optional Blueprint exposure (`UFUNCTION(BlueprintCallable)` markers). Critical paths are C++; gameplay glue is Blueprint.
5. **Niagara mapping.** `vfx.system` (Brief 162) → UE Niagara System asset. Brief 162's module stack maps to Niagara emitter modules — the closest 1:1 match across the four engines because Niagara was the design inspiration. Deterministic seed → Niagara's Random module seed property.
6. **Chaos physics mapping.** Brief 156 3D physics → UE5 Chaos. Replay-critical entities use the substrate's deterministic physics kernel as a UE plugin (`SubstratePhysics.uplugin`); non-critical entities use Chaos defaults. Brief 156's 2D physics maps to Chaos 2D shapes within a 3D world (UE's typical 2D approach).
7. **Animation mapping.** `animation.clip` → UE Animation Sequence asset. `animation.blend_tree` → Animation Blueprint with state machines and blend nodes. Skeletal data → USkeleton + USkeletalMesh. IK → Control Rig nodes for FABRIK / CCD / Two Bone IK matching Brief 161's solvers.
8. **Audio mapping.** `audio.bus` (Brief 175) → UE Audio Mixer Submix tree. `audio.clip` → SoundWave asset. Effects → MetaSounds for the substrate's deterministic effect kernel; substrate ships a MetaSounds plugin (`SubstrateAudio.uplugin`) implementing the eight v0.1 effects from Brief 183.
9. **UI mapping.** `ui.element` (Brief 174) → UMG Widget Blueprint. The 5 layout primitives map to UMG containers: flow → HorizontalBox/VerticalBox; grid → UniformGridPanel; stack → BoxPanel; absolute → CanvasPanel; constraint → ScaleBox + Anchors.
10. **Lighting and materials.** Substrate materials emit as UE Material assets with appropriate Lumen / Nanite settings. Brief 072's "beating Unreal at AAA 3D rendering" applies post-export through substrate's material parameters set to drive Lumen quality, not bypass it.
11. **Behavior tree mapping.** `ai.behavior_tree` (Brief 159) → UE Behavior Tree asset + Blackboard asset. The mapping is structural — UE's BT system was the design inspiration. GOAP (Brief 159's GOAP primitives) ships as a substrate plugin since UE has no native GOAP.
12. **State machine mapping.** `ai.fsm` → AnimationStateMachine for animation FSMs, custom C++ state machine class for game logic FSMs.
13. **Save / load.** `save.snapshot` → SaveGame class via UE's SaveGameObject API. Partial chunks → multiple SaveGame slots.
14. **Input mapping.** `input.action` → UE Enhanced Input system (UE 5.1+). Action maps export to InputMappingContext + InputAction assets directly.
15. **Determinism preservation.** UE5 is non-deterministic by default (multi-threaded particle ticks, async load). Substrate ships a `SubstrateDeterministic.uplugin` that pins critical-path ticks to a single thread and overrides PRNG sources. Replay verification flags any tick where output diverges from the recorded session.
16. **Asset cooking.** UE's cook step is the binary serialization phase. The substrate exporter writes uasset files in the canonical UE 5.x format. Non-cookable substrate features fall back to runtime asset loading.
17. **Plugin packaging.** `SubstrateAudio.uplugin`, `SubstratePhysics.uplugin`, `SubstrateGOAP.uplugin`, `SubstrateDeterministic.uplugin` ship as a single substrate UE plugin bundle exposed to the Unreal Marketplace post-v0.1 (deferred).

## Risks identified
- **UE version churn.** UE 5.3 → 5.4 → 5.5 introduce API breaks. Mitigation: target LTS-style major versions (5.3, 5.5); CI runs against each supported version.
- **Chaos non-determinism.** Chaos has the same non-determinism issues as PhysX. Mitigation: substrate physics plugin same as Brief 189; replay-critical entities only.
- **uasset binary format complexity.** Writing uasset files correctly requires matching UE's serialization byte-for-byte. Mitigation: use UE's text-based asset format where possible (`-textsource`); fall back to in-process UE editor invocation for binary uasset generation if direct write fails — accepting a slower export pipeline.
- **C++ build dependency.** Generated C++ requires the creator to have UE's build tooling (Visual Studio / Xcode / clang). Mitigation: pure-Blueprint export mode for creators without C++ tooling, with the trade-off that critical-path performance is reduced.
- **Substrate plugin marketplace approval.** Submitting to UE Marketplace has Epic's review process. Mitigation: ship plugins as direct downloads from substrate repo first; marketplace deferred.

## Recommendation
Specify the Unreal exporter as Brief 188's emitter graph specialized for UE 5.3+, with Blueprint + C++ dual emission, Niagara mapping for VFX, Chaos with substrate physics override for determinism, Enhanced Input + UMG + UE BT/Blackboard for input/UI/AI, and a unified substrate plugin bundle. Default to text-format uasset where supported. Defer pure-Blueprint export and marketplace listing to v0.2.

## Confidence
**4 / 5.** UE's Niagara, BT, and Animation Blueprint match substrate primitives more closely than any other engine, making most of the export structural. The novelty is the substrate plugin bundle and the determinism override. Lower than 4.5 because uasset binary serialization is the highest-risk technical surface in the round; Phase 1 will measure whether direct write or in-process UE invocation is required.

## Spec impact
- New spec section: **Unreal export pipeline specification**.
- Adds UE-specific `export.target` parameters (UE version, template, Lumen/Nanite, target platforms).
- Adds the substrate UE plugin bundle specification.
- Cross-references Briefs 072, 020, 188.

## New inventions
- **INV-784** — Niagara emitter mapping with structural module-stack alignment: substrate VFX exports near-1:1 to UE's flagship VFX system.
- **INV-785** — Substrate UE plugin bundle (Audio, Physics, GOAP, Deterministic): one installable plugin equips a UE project with substrate runtime parity.
- **INV-786** — Blueprint + C++ dual emission with critical-path C++ + glue Blueprint: best-of-both for performance and creator authoring ergonomics.
- **INV-787** — Enhanced Input mapping for `input.action`: substrate input actions export to UE's modern input pipeline.
- **INV-788** — Determinism plugin pinning critical-path ticks to single thread with PRNG override: makes UE replay-deterministic for replay-critical entities.

## Open follow-ups
- Unreal round-trip (deferred to v0.3).
- UE Marketplace plugin submission (deferred to v0.2).
- Console exporters via UE's licensed platforms (deferred to v0.5).
- Lyra Starter Game integration template (deferred to v0.4).
- Pixel Streaming integration for browser delivery (deferred to v0.4).
- USD pipeline integration (deferred to v0.5 with Brief 094 vehicles + USD metadata).

## Sources
1. Brief 020 — Determinism contract per engine.
2. Brief 065 — Game engines deep dive.
3. Brief 072 — Beating Unreal at AAA 3D rendering.
4. Brief 156 — Physics integration.
5. Brief 159 — State machines and behavior trees.
6. Brief 161 — Animation runtime.
7. Brief 162 — Particle and VFX runtime.
8. Brief 188 — Godot export pipeline.
9. Brief 189 — Unity export pipeline.
10. Unreal Engine 5 documentation (docs.unrealengine.com/5.3/en-US/).
11. UE Niagara documentation.
12. UE Enhanced Input documentation.
13. UE Chaos Physics documentation.
