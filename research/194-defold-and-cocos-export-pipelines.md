# 194 — Defold and Cocos export pipelines

## Question
What are the export pipelines that produce complete Defold and Cocos Creator projects from a signed GSPL gseed bundle, with Lua / TypeScript output, mobile-first 2D performance, and the lightweight runtime profile that distinguishes these engines from heavier alternatives?

## Why it matters (blast radius)
Defold (King-owned, free, BSD-licensed) and Cocos Creator (largest mobile 2D engine globally, especially in Asia) are the two leading mobile-2D engines. Together they cover the mobile creator population that Unity and GameMaker don't reach idiomatically. Skipping them concedes the mobile-2D market.

## What we know from the spec
- Brief 188 — Godot export pipeline (reference exporter).
- Brief 191 — Phaser export pipeline.
- Brief 192 — GameMaker export pipeline.
- Brief 020 — determinism contract per engine.
- Brief 065 — game engines deep dive.
- Briefs 152-176.

## Findings (Defold)
1. **Project format.** Defold projects are a `game.project` ini + `.collection` (scenes) + `.go` (entities) + `.script` / `.gui_script` (Lua) + `.atlas` / `.tileset` / `.font` resources, all in a Git-friendly text format. The exporter generates the full tree.
2. **Scene → Collection mapping.** `level.scene` → Defold `.collection` file. Substrate entities become Game Objects (`.go`) referenced from the collection.
3. **Entity → GameObject mapping.** Brief 153 entities → Defold Game Objects with attached components (Sprite / Tilemap / Sound / Collision / Script). Substrate components map to Defold component types where they exist; otherwise substrate-provided Lua scripts.
4. **Script generation.** Substrate logic emits as Defold Lua scripts (`.script`) using Defold's message-passing API. BT / FSM ship as `substrate_bt.lua` / `substrate_fsm.lua` libraries.
5. **Audio mapping.** `audio.bus` → Defold sound groups (limited routing). Substrate's deterministic audio kernel ships as a Defold native extension (`substrate_audio.ext`) for the eight effects from Brief 183.
6. **UI mapping.** `ui.element` → Defold GUI nodes (`.gui` files + `.gui_script`). The 5 layout primitives map to Defold GUI's anchor + adjust system.
7. **VFX mapping.** `vfx.system` → Defold particle FX (`.particlefx`). Module stack maps to particle emitter properties. Deterministic seed via substrate PRNG library.
8. **Physics mapping.** Brief 156 2D physics → Defold's Box2D wrapper. Substrate determinism kernel as Defold native extension for replay-critical entities.

## Findings (Cocos Creator)
9. **Project format.** Cocos Creator 3.x projects are TypeScript-first with `assets/` (scenes / prefabs / scripts) + `package.json` + `tsconfig.json` + `cc.config.json`. Scenes are `.scene` JSON files.
10. **Scene mapping.** `level.scene` → Cocos `.scene` file (cc.Scene). Entities → cc.Node hierarchy with attached cc.Component instances.
11. **Component mapping.** Substrate components → Cocos Components (TypeScript classes extending cc.Component). Same script generation pattern as Brief 189 Unity but in TypeScript.
12. **Audio / UI / VFX / Physics.** Audio → cc.AudioSource + AudioClip. UI → cc.UITransform + Layout. VFX → cc.ParticleSystem2D / cc.ParticleSystem (3D). Physics → cc.PhysicsSystem2D (Box2D-class) or cc.PhysicsSystem (Bullet-class). Substrate determinism kernels via Cocos native extensions where supported.
13. **Cocos has stronger 3D than Defold.** Cocos Creator 3.x supports both 2D and 3D natively. The exporter routes 2D scenes to Defold or Cocos based on creator preference; 3D scenes route only to Cocos (Defold's 3D is minimal).

## Findings (shared)
14. **Sign-time engine selection.** A typed `export.target.engine` field selects Defold vs Cocos. Both share the substrate web/mobile runtime modules where possible (BT/FSM/save/lineage), with engine-specific physics/audio extensions.
15. **Mobile-first defaults.** Both exporters default to mobile target platforms (Android / iOS). Touch input (`input.action` touch bindings) is the default control scheme. Performance budgets default to mobile profiles (60 FPS at 720p, 30 FPS at 1080p).
16. **Lua vs TypeScript.** Defold uses Lua (5.1 dialect with LuaJIT compatibility); Cocos uses TypeScript. Substrate's logic generation has dual emitters per language. Generated code is hand-readable in both targets.
17. **Lightweight runtime budget.** Both engines target small executable sizes (<10 MB for Defold, <30 MB for Cocos). Substrate runtime libraries respect these budgets — no kitchen-sink imports.

## Risks identified
- **Lua / TypeScript dual maintenance burden.** Substrate runtime modules must be maintained in two languages plus the canonical TypeScript from Brief 191. Mitigation: a code-generation pipeline produces Lua and TypeScript variants from a canonical AST; substrate authors maintain one source.
- **Defold native extension cost.** Native extensions require platform-specific builds (Windows / Mac / Linux / Android / iOS). Mitigation: substrate ships pre-built extension binaries for all five platforms per release.
- **Cocos Creator version churn.** Cocos Creator 2 → 3 was a major break. Target Cocos Creator 3.8+ as v0.1 floor; refuse export to 2.x.
- **3D physics determinism on mobile.** Cocos Bullet wrapper is non-deterministic. Mitigation: same as Brief 189 — substrate physics kernel native extension for replay-critical entities.
- **Defold 3D limitations.** Defold 3D is intentionally minimal. Mitigation: export validator routes 3D scenes to Cocos only; Defold target rejects 3D scenes with a typed error pointing at Cocos as alternative.

## Recommendation
Specify Defold and Cocos export pipelines as paired engine targets sharing substrate runtime via a canonical-AST-driven code-generator producing Lua (Defold) and TypeScript (Cocos) variants. Default both to mobile target platforms with mobile performance budgets. Route 3D scenes to Cocos only. Ship substrate native extensions for both engines with pre-built binaries for all five host platforms.

## Confidence
**4 / 5.** Both engines have well-documented project formats and clear creator workflows. The novelty is the canonical-AST code-gen producing Lua + TypeScript from one source, and the substrate native extension distribution. Lower than 4.5 because Defold native extension build / signing on iOS is the highest-risk technical surface — Phase-1 needs to validate pre-built distribution works under Apple's notarization rules.

## Spec impact
- New spec section: **Defold and Cocos export pipeline specification**.
- Adds the `export.target.engine` typed field (defold / cocos_creator).
- Adds the canonical-AST code-gen pipeline producing Lua + TypeScript.
- Adds substrate native extension distribution specification.
- Cross-references Briefs 188, 191, 192.

## New inventions
- **INV-803** — Canonical-AST code-generator producing Lua (Defold) + TypeScript (Cocos) from one substrate source: substrate runtime modules maintained once, emitted twice.
- **INV-804** — Substrate native extension distribution with pre-built binaries for all five host platforms: creators don't compile substrate runtime themselves.
- **INV-805** — Sign-time engine routing based on scene 2D/3D and creator preference: 3D scenes routed to Cocos, 2D scenes routable to either.
- **INV-806** — Mobile-first performance budget defaults: 60 FPS @ 720p / 30 FPS @ 1080p budgets baked into the export target for both engines.
- **INV-807** — Defold collection / Cocos scene unified scene mapping with engine-specific game-object/cc-node emitters: shared scene tree contract across both 2D mobile engines.

## Open follow-ups
- Defold round-trip (deferred to v0.3).
- Cocos Creator 3.8 vs latest tracking (incremental).
- Cocos Native (C++) export path for non-web targets (deferred to v0.4).
- Defold WebAssembly target unification with Brief 193 (deferred to v0.4).
- Console targets via Defold's licensed platforms (deferred to v0.5).

## Sources
1. Brief 020 — Determinism contract per engine.
2. Brief 065 — Game engines deep dive.
3. Brief 156 — Physics integration.
4. Brief 159 — State machines and behavior trees.
5. Brief 183 — Audio mixer and music editor.
6. Brief 188 — Godot export pipeline.
7. Brief 191 — Phaser export pipeline.
8. Brief 192 — GameMaker export pipeline.
9. Defold documentation (defold.com/manuals/).
10. Cocos Creator 3.x documentation (docs.cocos.com/creator/manual/en/).
