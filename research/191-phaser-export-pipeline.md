# 191 — Phaser export pipeline

## Question
What is the export pipeline that produces a complete, web-runnable Phaser 3.x project from a signed GSPL gseed bundle, with TypeScript scripts, 2D-only output, and zero-install browser delivery?

## Why it matters (blast radius)
Phaser is the leading open-source 2D web game framework with a massive creator ecosystem. Unlike Godot/Unity/Unreal which require installs, Phaser ships HTML5 from day one — making it the natural v0.1 web target alongside Brief 193's standalone HTML5. The two surfaces serve different creator needs: Phaser for game-shaped projects with the framework's batteries; raw HTML5 for engine-free demos.

## What we know from the spec
- Brief 188 — Godot export pipeline (reference exporter).
- Brief 189 — Unity export pipeline.
- Brief 020 — determinism contract per engine.
- Brief 065 — game engines deep dive (Phaser is referenced as the indie 2D web standard).
- Briefs 152-176.

## Findings
1. **Emitter graph inheritance.** Inherits Brief 188's typed `export.target` graph. Phaser-specific target declares: target Phaser version (3.70+), TypeScript or JavaScript output, asset bundling strategy (Webpack / Vite / esbuild / parcel — defaults to Vite), and target browser baseline (ES2020 default).
2. **2D-only enforcement.** Phaser is strictly 2D. The exporter validates the source `level.scene` is a 2D pattern family per Brief 172; 3D scenes are rejected with a typed error pointing at the unsupported pattern. This is a sign-time gate, not a runtime fall-through.
3. **Project format.** Output is a directory tree: `index.html`, `src/` (TypeScript modules), `assets/` (images, audio, JSON), `package.json`, `vite.config.ts` (or chosen bundler), `tsconfig.json`.
4. **Scene mapping.** `level.scene` (Brief 172) → Phaser `Scene` class. Each substrate scene becomes one TypeScript module exporting a Scene subclass. Scene init / preload / create / update lifecycle methods are populated from the scene gseed's typed structure.
5. **Entity / component mapping.** Brief 153 entities → Phaser GameObjects (`Sprite`, `Image`, `Text`, `TileSprite`, etc.). Components map to Phaser GameObject properties or to substrate-provided component classes attached via the `setData()` API for non-builtin component types.
6. **Tilemap mapping.** `tilemap.layer` (Brief 173) → Phaser `Tilemap` + `TilemapLayer`. Brief 173's 47-tile autotile is exported as static cell data; Phaser does not have an autotile runtime so tile resolution happens at export. Tileset → Phaser `Tileset` from a packed atlas.
7. **Animation mapping.** `animation.clip` (sprite-frame channels only — no skeletal in v0.1 Phaser export) → Phaser `Animation` instances created via `anims.create()`. Skeletal animation requires a Spine plugin (Brief 195) — exported as a Phaser-Spine bundle.
8. **Audio mapping.** `audio.bus` → flattened bus structure since Phaser's WebAudio binding is single-graph by default. Substrate's deterministic effect kernel ships as a substrate-provided Web Audio worklet (`substrate-audio.worklet.ts`). The eight v0.1 effects (Brief 183) implement against AudioWorklet for replay parity.
9. **UI mapping.** `ui.element` (Brief 174) → either Phaser DOM elements (when accessibility / WCAG matters) or Phaser GameObject-based UI. Default is DOM-based for accessibility per Brief 184's WCAG gate. The 5 layout primitives map to CSS flexbox / grid for DOM mode.
10. **VFX mapping.** `vfx.system` → Phaser Particle Emitter (the new 3.60+ emitter API). Brief 162's module stack maps to the emitter's typed config object. Deterministic seed → Phaser RandomDataGenerator with substrate's sub-seeded PRNG.
11. **Behavior tree / FSM.** No native Phaser equivalent. Emit as TypeScript classes implementing Brief 159's tick semantics. Substrate provides `substrate-bt.ts` and `substrate-fsm.ts` runtime modules included in the export.
12. **Save / load.** `save.snapshot` → IndexedDB via substrate's `substrate-save.ts` module providing the same partial-chunk semantics as Brief 158. localStorage fallback for tiny saves.
13. **Input mapping.** `input.action` → Phaser InputManager bindings. Keyboard, mouse, touch, gamepad APIs are wrapped in a substrate `InputAdapter.ts` that emits the same typed events as the substrate runtime.
14. **Physics mapping.** Brief 156 2D physics → Phaser's Arcade Physics (default) or Matter.js (advanced). Substrate's deterministic 2D physics kernel ships as `substrate-physics.ts` and is the default for replay-critical scenes; Arcade is the fallback for simpler games.
15. **Camera mapping.** `camera.rig` → Phaser Camera with substrate-provided controller for follow / orbit / cinematic. Camera shots are typed config objects executed by the controller.
16. **Lineage stub.** A `substrate-lineage.ts` module captures runtime mutations to a JSON blob for post-export replay verification.
17. **Bundle output.** The exporter runs the chosen bundler (default Vite) at export-time and produces a `dist/` directory ready to deploy. Optional skip-bundle mode emits source files only for creators who want their own build pipeline.

## Risks identified
- **Phaser API churn.** Phaser 3.60 → 3.80 introduced breaking changes (notably the new particle emitter). Mitigation: pin minimum target to 3.70 with version-specific emitter branches.
- **Audio determinism in WebAudio.** WebAudio implementations differ across browsers. Mitigation: substrate AudioWorklet runs the deterministic kernel in JS-only mode (not browser-native effects); accept slightly higher CPU cost for determinism.
- **IndexedDB quota limits.** Browsers cap IndexedDB. Mitigation: substrate save module surfaces quota errors as typed events; partial chunks compress with zstd-wasm (Brief 005).
- **3D rejection UX.** Creators may try to export 3D scenes and see only an error. Mitigation: error message points at the unsupported pattern family and suggests Brief 188 (Godot) or Brief 190 (Unreal) as alternatives.
- **Bundle size at scale.** Large asset packs blow browser load times. Mitigation: substrate provides asset chunking + lazy loading directives in the export config; CDN-hosting recommendations in the generated README.

## Recommendation
Specify the Phaser exporter as Brief 188's emitter graph specialized for Phaser 3.70+ with TypeScript output, 2D-only validation, Vite bundling default, deterministic physics + audio + PRNG via substrate runtime modules, and DOM-based UI for accessibility. Defer Spine integration to Brief 195's coverage.

## Confidence
**4.5 / 5.** Phaser is well-documented and structurally simple compared to Unity/Unreal. The novelty is the deterministic AudioWorklet and physics kernel running in pure JS. Lower than 5 because IndexedDB quota and AudioWorklet CPU cost need Phase-1 measurement.

## Spec impact
- New spec section: **Phaser export pipeline specification**.
- Adds Phaser-specific `export.target` parameters.
- Adds substrate-provided web runtime modules (`substrate-audio.worklet.ts`, `substrate-physics.ts`, `substrate-bt.ts`, `substrate-fsm.ts`, `substrate-save.ts`, `substrate-lineage.ts`, `InputAdapter.ts`).
- Cross-references Briefs 005, 020, 158, 174, 184, 188.

## New inventions
- **INV-789** — Sign-time 3D-rejection gate at export with alternate-target suggestion: 3D scenes rejected with a typed error pointing at supported alternatives.
- **INV-790** — Substrate web runtime modules bundle: a TypeScript bundle providing deterministic physics, audio, BT/FSM, save, lineage, and input adaptation for any web export.
- **INV-791** — AudioWorklet-based deterministic audio for browser exports: the eight v0.1 effects from Brief 183 run as a Web Audio worklet for replay parity in the browser.
- **INV-792** — IndexedDB partial-save chunk strategy with zstd-wasm compression: substrate's save model fits in browser quota constraints.
- **INV-793** — Default DOM-mode UI for browser exports for WCAG compliance: substrate UI exports to accessible DOM elements by default rather than canvas-rendered text.

## Open follow-ups
- Phaser round-trip (deferred to v0.3).
- Spine plugin integration (covered by Brief 195).
- Multi-build target for Phaser (Vite + Webpack + esbuild parity test) — deferred to v0.2.
- Service worker / PWA template for offline play (deferred to v0.2).
- WebGPU backend (Phaser ships WebGL by default) — deferred to v0.4.

## Sources
1. Brief 005 — zstd deterministic encoding.
2. Brief 020 — Determinism contract per engine.
3. Brief 152-176 — Tier A and B namespaces.
4. Brief 174 — UI and HUD pattern library.
5. Brief 184 — UI and HUD layout editor.
6. Brief 188 — Godot export pipeline.
7. Phaser 3.70+ documentation (phaser.io/docs).
8. Vite documentation (vitejs.dev).
9. AudioWorklet specification (w3.org/TR/webaudio/#audioworklet).
10. IndexedDB specification.
