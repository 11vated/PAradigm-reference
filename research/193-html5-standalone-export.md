# 193 — HTML5 standalone export (Three.js + WebGPU)

## Question
What is the engine-free HTML5 standalone export pipeline that produces a zero-install browser-runnable game from a signed GSPL gseed bundle, using Three.js for 3D, raw Canvas / WebGL2 for 2D, and WebGPU when available?

## Why it matters (blast radius)
Per the v0.1 reach table, HTML5 is the v0.1 web target. Phaser (Brief 191) covers framework-shaped games; this brief covers the engine-free demo path that creators use to share work without anyone installing anything. Zero-install is the lowest-friction creator-to-player surface in existence — every other engine path has a setup cost.

## What we know from the spec
- Brief 188 — Godot export pipeline (reference exporter).
- Brief 191 — Phaser export pipeline (framework web target).
- Brief 075 — GSPL without a real GPU.
- Brief 020 — determinism contract per engine.
- Brief 002 — WGSL portable subset.
- Briefs 152-176.

## Findings
1. **Emitter graph inheritance.** Inherits Brief 188's emitter graph. HTML5-specific target declares: target browser baseline (ES2020 default), 2D-only / 3D / mixed mode, render backend (Canvas2D / WebGL2 / Three.js / WebGPU), and bundling strategy (defaults to Vite same as Brief 191).
2. **Render backend selection.** Sign-time selects render backend per scene: 2D scenes default to Canvas2D for simple, WebGL2 for complex; 3D scenes default to Three.js (currently r160+) over WebGL2 with WebGPU fall-forward where available (Brief 002 WGSL portable subset).
3. **Project format.** Output is a flat directory: `index.html`, `main.ts` (entry), `src/` (TypeScript modules), `assets/`, `package.json`, `vite.config.ts`. Optional pre-bundled `dist/` produced by the export step.
4. **Scene mapping.** `level.scene` (Brief 172) → either Three.js Scene (3D) or substrate-provided 2D scene class. Each substrate scene exports as one TypeScript module.
5. **Entity / component mapping.** Brief 153 entities → Three.js Object3D (3D) or substrate `Entity2D` class (2D). Components → Object3D userData properties or substrate component classes.
6. **Tilemap mapping (2D).** `tilemap.layer` → substrate-provided `TilemapRenderer.ts` rendering against WebGL2 batched quads. 47-tile autotile resolved at export.
7. **3D mesh / animation mapping.** Brief 161 skeletal data → Three.js `SkinnedMesh` + `Skeleton` + `AnimationMixer`. Brief 161 IK chains → substrate `IKSolver.ts` running FABRIK / CCD on Three.js bones (Three.js has no native IK).
8. **Material / shader mapping.** Substrate materials → Three.js `MeshStandardMaterial` (PBR) for 3D, custom shader chunks for substrate-specific effects. WGSL portable subset (Brief 002) compiles to GLSL via Three.js shader chunks for WebGL2 fallback, native WGSL for WebGPU.
9. **Audio mapping.** `audio.bus` → Web Audio AudioContext + GainNode tree. Same `substrate-audio.worklet.ts` as Brief 191 for deterministic effects.
10. **UI mapping.** `ui.element` → DOM elements (default for accessibility per Brief 184) or substrate-provided canvas-rendered UI for HUD elements that overlay the game canvas. Canvas UI bypasses Brief 184's WCAG sign-time check and is rejected for non-game-specific element kinds.
11. **VFX mapping.** `vfx.system` → Three.js `Points` / `InstancedMesh` for 3D, substrate `Particle2D` class for 2D. Same deterministic seed contract as Brief 191 + Brief 162.
12. **Behavior tree / FSM / save / input / physics.** Same substrate web runtime modules as Brief 191. The runtime modules are shared between Phaser and HTML5 exports — only the rendering layer differs.
13. **Camera mapping.** Three.js PerspectiveCamera / OrthographicCamera for 3D; substrate-provided 2D camera class for 2D. `camera.rig` and `camera.shot` execute via substrate's camera controller.
14. **3D physics.** Brief 156 3D physics → substrate's deterministic 3D kernel ported to TypeScript / WASM. v0.4 default; v0.1 ships hooks only.
15. **WebGPU progressive enhancement.** When `navigator.gpu` is available, the exporter uses WebGPU through Three.js's WebGPURenderer (or directly for substrate-specific shaders). Otherwise WebGL2 fallback. The selection is runtime, not export-time.
16. **Asset delivery.** Assets compress with substrate's universal pipeline (Brief 089) outputs (KTX2 textures, OGG audio, draco-compressed meshes). The exporter generates lazy-load chunks per scene.
17. **Lineage stub.** Same `substrate-lineage.ts` as Brief 191.
18. **PWA option.** Optional service worker generation for offline play. Off by default at v0.1; opt-in flag in `export.target`.

## Risks identified
- **WebGPU adoption.** WebGPU is not yet universally supported (Safari shipping in 17.4+ behind a flag). Mitigation: WebGL2 fallback is always present; WebGPU is an opt-in performance path, not a requirement.
- **Three.js API churn.** Three.js has frequent API breaks (r150 → r160 dropped several APIs). Mitigation: pin minimum to r160 LTS-equivalent; test against current release.
- **Asset bundle size.** 3D assets blow browser load times. Mitigation: lazy-load chunks per scene; document size budgets in the generated README.
- **iOS Safari quirks.** Safari has historical WebAudio / WebGL quirks. Mitigation: substrate ships a per-browser polyfill set; target iOS 16+ only.
- **WGSL compatibility on older browsers.** WGSL not supported on WebGL2-only browsers. Mitigation: GLSL fallback for all substrate shaders generated by the WGSL → GLSL transpiler from Brief 002.

## Recommendation
Specify the HTML5 standalone exporter as Brief 188's emitter graph specialized for engine-free browser delivery, with Three.js for 3D, Canvas2D / WebGL2 for 2D, WebGPU progressive enhancement, shared substrate web runtime modules with Brief 191, and DOM-default UI for accessibility. Defer 3D physics and PWA to v0.4 / v0.2 respectively.

## Confidence
**4 / 5.** Three.js + WebGL2 + WebGPU stacks are well-precedented; the novelty is the substrate web runtime modules being shared with Phaser export, the WGSL portable subset compiling to both backends, and the sign-time backend selection. Lower than 4.5 because WebGPU support and the WGSL→GLSL transpiler need Phase-1 cross-browser validation.

## Spec impact
- New spec section: **HTML5 standalone export pipeline specification**.
- Adds HTML5-specific `export.target` parameters (render backend, browser baseline, PWA flag).
- Specifies the WGSL → GLSL transpiler as part of the substrate web runtime.
- Cross-references Briefs 002, 075, 188, 191.

## New inventions
- **INV-798** — Sign-time render backend selection per scene with progressive WebGPU enhancement: Canvas2D / WebGL2 / Three.js / WebGPU chosen based on scene complexity, with WebGPU runtime opt-in.
- **INV-799** — WGSL → GLSL transpiler at export for cross-backend shader portability: substrate shaders compile to both WebGPU and WebGL2 from one canonical source.
- **INV-800** — Shared substrate web runtime modules across HTML5 and Phaser exports: physics, audio, BT/FSM, save, lineage, input modules implemented once, reused twice.
- **INV-801** — Lazy-load asset chunking per scene: substrate exporter slices the asset bundle by scene reachability for browser-friendly initial load.
- **INV-802** — Engine-free 3D HTML5 export via Three.js with substrate IK / animation runtime overlay: Three.js becomes the rendering backend; substrate provides the runtime semantics it lacks.

## Open follow-ups
- 3D physics (deferred to v0.4).
- PWA / service worker template (deferred to v0.2).
- Mobile-touch optimized HTML5 export profile (deferred to v0.4).
- WebXR (VR/AR) support (deferred to v0.5).
- WebRTC multiplayer transport (deferred to v0.3 with Brief 209).

## Sources
1. Brief 002 — WGSL portable subset.
2. Brief 020 — Determinism contract per engine.
3. Brief 075 — GSPL without a real GPU.
4. Brief 089 — Universal anything-to-gseed pipeline.
5. Brief 188 — Godot export pipeline.
6. Brief 191 — Phaser export pipeline.
7. Three.js documentation (threejs.org/docs/).
8. WebGPU specification (gpuweb.github.io/gpuweb/).
9. KTX2 specification (khronos.org/ktx/).
10. Draco mesh compression (google.github.io/draco/).
