# 189 — Unity export pipeline

## Question
What is the export pipeline that produces a complete Unity 2022 LTS+ project from a signed GSPL gseed bundle, with C# scripts, prefab/ScriptableObject resources, URP/HDRP awareness, and 2D/3D parity?

## Why it matters (blast radius)
Unity has the largest creator pool. Parity here unlocks the largest creator population. Unity's prefab + ScriptableObject + GameObject model is far more idiomatic for substrate composition than its raw C# surface — getting the mapping right means substrate gseeds round-trip cleanly.

## What we know from the spec
- Brief 188 — Godot export pipeline (the reference exporter; this brief inherits its emitter graph contract).
- Brief 020 — determinism contract per engine.
- Brief 065 — game engines deep dive.
- Brief 074 — GSPL multiplayer runtime (Unity hooks).
- Briefs 152-176.

## Findings
1. **Emitter graph inheritance.** Inherits Brief 188's typed `export.target` and emitter graph contract. The Unity-specific `export.target` declares: target Unity LTS version (2022.3+), render pipeline (URP / HDRP / built-in), 2D or 3D template root, and target platforms.
2. **Scene mapping.** `level.scene` (Brief 172) → Unity `.unity` scene file (YAML). The scene tree maps to Unity's GameObject hierarchy. Entities (Brief 153) become GameObjects with attached MonoBehaviour components mirroring Brief 153 component types.
3. **Prefab mapping.** Brief 177's signed prefabs → Unity Prefab assets. Prefab variants (Brief 177 INV-723) map to Unity's Prefab Variants directly — Unity's prefab variant model was the design inspiration, so the mapping is structural.
4. **ScriptableObject mapping.** Pure-data gseeds (e.g., `combat.damage_formula`, `loot.table`, `progression.skill_tree`, `ai.blackboard`) export as Unity ScriptableObjects. ScriptableObjects are Unity-idiomatic data containers and round-trip cleanly into the Inspector.
5. **C# script generation.** Logic-bearing gseeds (BT tick, FSM update, custom mechanics from Brief 164) emit as C# scripts under `Assets/Substrate/Generated/`. Scripts inherit from substrate-provided base classes shipped as a `.unitypackage`.
6. **Render pipeline branching.** The emitter detects URP vs HDRP vs built-in and emits appropriate shader files. Substrate VFX (Brief 162) maps to Unity Particle System for URP, VFX Graph (Niagara-class) for HDRP. Materials map to URP/Lit, HDRP/Lit, or Standard.
7. **Animation mapping.** `animation.clip` → Unity `.anim` AnimationClip asset. `animation.blend_tree` → Animator Controller with BlendTree assets. Skeletal data → Avatar + AvatarMask. IK chains via Animation Rigging package or substrate IK MonoBehaviour for v0.1 simplicity.
8. **Audio mapping.** `audio.bus` → Unity `AudioMixer` asset with mixer groups. `audio.clip` → Unity AudioClip asset. Effects → AudioMixer effects where equivalents exist; substrate's deterministic effect kernel ships as a Unity native plugin (`SubstrateAudio.dll`).
9. **UI mapping.** Default to Unity UI Toolkit (Unity 2022 LTS+) — UXML + USS. Brief 174's 5 layout primitives map to UI Toolkit's flexbox. Game-specific elements (healthbar, hotbar, inventory) emit as custom UI Toolkit Visual Elements with substrate-provided controllers.
10. **VFX mapping.** Brief 162 emitter → Unity Particle System (URP) or VFX Graph (HDRP). Module stack maps to ParticleSystem main/emission/shape/velocity/color modules. The deterministic seed becomes ParticleSystem.useAutoRandomSeed = false + randomSeed.
11. **Behavior tree / FSM.** No native Unity equivalent. Emit as C# scripts implementing Brief 159's tick semantics, with the BT/FSM data as ScriptableObjects. Authoring round-trip back to substrate is one-way at v0.1.
12. **Save / load.** `save.snapshot` → C# `SaveManager.cs` using `BinaryFormatter` substitute (substrate's deterministic serializer for replay parity). Partial chunks → per-chunk files in Application.persistentDataPath.
13. **Input mapping.** `input.action` → Unity Input System assets (`.inputactions`). Action maps and bindings translate directly. Legacy Input Manager only as fallback for older projects.
14. **Physics mapping.** Brief 156 2D → Unity Box2D (Rigidbody2D / BoxCollider2D / etc.). 3D → Unity PhysX (Rigidbody / Collider). Determinism: PhysX is non-deterministic on Unity 2022 LTS by default, so the substrate's deterministic 3D physics kernel ships as a Unity package overriding PhysX for replay-critical entities.
15. **Camera mapping.** `camera.rig` → Unity Cinemachine virtual cameras (the de-facto Unity camera system). `camera.shot` → CinemachineBrain blends.
16. **Multiplayer hooks.** Per Brief 074, the exporter ships substrate networking hooks as a Unity package. v0.1 ships hooks only; full multiplayer in v0.3.
17. **Asset import settings.** Generated `.meta` files preserve substrate import metadata so re-import does not lose data.

## Risks identified
- **PhysX non-determinism.** PhysX in Unity is not deterministic across hardware. Mitigation: substrate ships a deterministic 3D physics kernel as a Unity package; replay-critical entities use it; non-critical entities use PhysX.
- **Render pipeline asset divergence.** A substrate gseed exported to URP and HDRP needs different shaders. Mitigation: emitter branches per pipeline at export time; sign-time validator surfaces unsupported features per pipeline.
- **Unity version compatibility.** Unity API drifts per minor version. Mitigation: target the LTS version range only (2022.3 LTS as v0.1 floor; 2023 LTS at v0.2); refuse to export to non-LTS versions without an explicit override.
- **C# generation legibility.** Generated C# is hard to read; creators may want to hand-edit. Mitigation: emit clean, idiomatic C# with substrate-author comments; round-trip not supported at v0.1.
- **License surface for substrate native plugins.** Shipping `SubstrateAudio.dll` requires platform-specific binaries (Windows / Mac / Linux). Mitigation: build all three at substrate release; the Unity package contains all platforms.

## Recommendation
Specify the Unity exporter as Brief 188's emitter graph specialized for Unity 2022 LTS+, with URP/HDRP/built-in branching, prefab + ScriptableObject as the primary data containers, C# scripts for logic, Cinemachine for cameras, Input System for input, Unity UI Toolkit for UI, and substrate native plugin packages for deterministic effects and physics. Defer Unity round-trip and 2023 LTS support to v0.2.

## Confidence
**4 / 5.** Unity's surface area is enormous and the prefab / ScriptableObject / package model is well-understood. The novelty is the substrate native plugin shipping deterministic kernels and the URP/HDRP branching at export. Lower than 4.5 because PhysX non-determinism is the hardest engineering problem in this brief — the substrate physics override needs Phase-1 validation against a real Unity scene.

## Spec impact
- New spec section: **Unity export pipeline specification**.
- Adds Unity-specific `export.target` parameters (LTS version, render pipeline, target platforms).
- Adds `SubstrateAudio` and `SubstratePhysics` Unity native plugin specifications.
- Cross-references Briefs 020, 074, 188.

## New inventions
- **INV-779** — URP/HDRP/built-in render pipeline branching at export with sign-time feature compatibility check: emits per-pipeline assets and rejects unsupported features.
- **INV-780** — Substrate physics native plugin overriding PhysX for replay-critical entities: deterministic 3D physics within Unity by selectively replacing the engine's solver.
- **INV-781** — ScriptableObject mapping for pure-data gseeds: round-trip-clean Unity Inspector authoring of substrate data.
- **INV-782** — Cinemachine virtual camera mapping for `camera.rig` and `camera.shot`: substrate cameras export to Unity's de-facto camera system.
- **INV-783** — Unity Input System asset mapping for `input.action`: action maps export directly to Unity's modern input pipeline.

## Open follow-ups
- Unity round-trip (deferred to v0.2).
- Unity 2023 LTS / Unity 6 support (deferred to v0.2).
- Console exporters via Unity's licensed platforms (deferred to v0.5).
- DOTS / Entities mapping for Unity ECS (deferred to v0.4 — substrate ECS in Brief 153 doesn't 1:1 map to DOTS).
- WebGL via Unity's WebGL export (separate path from Brief 193) — deferred to v0.2.

## Sources
1. Brief 020 — Determinism contract per engine.
2. Brief 065 — Game engines deep dive.
3. Brief 074 — GSPL multiplayer runtime.
4. Brief 188 — Godot export pipeline.
5. Briefs 152-176 — Tier A and B namespaces.
6. Unity Manual 2022 LTS (docs.unity3d.com/2022.3/Documentation/Manual/).
7. Unity Cinemachine documentation.
8. Unity Input System documentation.
9. Unity UI Toolkit documentation.
10. NVIDIA PhysX determinism notes (developer.nvidia.com/physx-sdk).
