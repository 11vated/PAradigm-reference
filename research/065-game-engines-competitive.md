# 065 — Game engines: Unity, Unreal, Godot

## Question
GSPL is a generative substrate, not a game engine — but it ships sprites, animations, audio, music, dialog, and (eventually) 3D meshes that *go into* games. How does GSPL relate to Unity, Unreal, and Godot? Is it a competitor, a complement, or both? What is the integration story, and what is the differentiation against engine-internal AI features?

## Why it matters
Game engines are the dominant target for sprite/asset generation. If GSPL doesn't have a clean export and round-trip story to all three, it cuts itself off from its largest user base. At the same time, all three engines are racing to add their own AI features (Unity Muse, Unreal MetaHuman + plugin marketplace, Godot Anima/AI plugins). GSPL has to be the best generation substrate that *feeds* engines, not the worst engine that competes with them.

## What we know from the spec
- Brief 014: cross-engine breeding via naturality square.
- Brief 002: shipped engines include sprite, animation, audio, music, dialog.
- Brief 048: studio architecture is engine-agnostic.
- Brief 044: marketplace can list engine-targeted asset packs.

## Findings — engine profiles

### Unity
**Operator:** Unity Technologies; commercial; large free tier.
**Strengths:**
- Largest install base for indie and mobile games.
- C# scripting; mature 2D and 3D pipelines.
- Asset Store with millions of assets.
- Strong cross-platform deploy (mobile, console, web, desktop, XR).
- Unity Muse: AI features for behavior, animation, sprite generation (subscription).
- Unity Sentis: ONNX runtime for in-game ML inference.

**Weaknesses:**
- Recent pricing controversies eroded trust.
- Closed engine source (with conditional Unity Reference exception).
- Muse is hosted-only, subscription-gated.
- Asset Store quality varies wildly; provenance is weak.

### Unreal Engine
**Operator:** Epic Games; free with revenue share above $1M/year.
**Strengths:**
- Best-in-class 3D rendering; Lumen, Nanite, Chaos.
- Blueprint visual scripting + C++.
- MetaHuman Creator: photoreal humans.
- Marketplace with high-quality (often expensive) assets.
- Source-available (custom Epic license).
- Strong AAA and film usage.

**Weaknesses:**
- Steeper learning curve; heavier hardware requirements.
- Marketplace less indie-friendly than Unity.
- AI features are scattered across MetaHuman, NeRF tools, and plugin marketplace.
- 5% revenue share above $1M.

### Godot
**Operator:** community-led non-profit; MIT licensed.
**Strengths:**
- Fully open source, no royalties, no licensing.
- Lightweight; runs on modest hardware.
- GDScript + C# + C++ support.
- Strong 2D pipeline; 3D pipeline maturing fast.
- Active community and rapid iteration.

**Weaknesses:**
- Asset ecosystem smaller than Unity/Unreal.
- 3D quality trails Unreal significantly.
- AI features are entirely community-plugin-driven; no first-party AI.
- Console deployment is harder (community ports).

## Engine-internal AI: the competitive context

| Engine AI feature | Quality | Sovereignty | GSPL alternative |
|---|---|---|---|
| Unity Muse Sprite | mid | hosted | GSPL sprite engine — better, local, signed, lineage |
| Unity Muse Animate | mid | hosted | GSPL animation engine — better, local, signed |
| Unity Muse Behavior | early | hosted | GSPL agent + critic loop |
| Unity Muse Texture | mid | hosted | GSPL texture variant of image engine |
| Unreal MetaHuman | high | local + cloud hybrid | GSPL doesn't compete; complementary |
| Unreal NeRF tools | early | local | GSPL has 3D engine roadmap (Brief 003) |
| Godot AI plugins | varies | varies | GSPL plug-in via export pipeline |

GSPL's positioning vs engine-internal AI is straightforward: **GSPL beats them on sovereignty, lineage, provenance, evolution, and federation, and matches or exceeds on quality.**

## Integration model

GSPL is a *substrate*, not an engine. The integration model is *export-first*:

### Sprite engine → all three engines
- **Unity:** export as 2D sprite atlas + JSON metadata; ship a Unity package that imports gseed lineage as a custom asset type. Provenance survives the import (c2pa metadata stored as a sub-asset).
- **Unreal:** export as Paper2D sprite + Datasmith reference. Provenance via custom asset wrapper.
- **Godot:** export as SpriteFrames resource + lineage sidecar. Tightest integration because Godot is open and we can ship a first-party plugin.

### Animation engine → all three
- **Unity:** export as Mecanim animation clips + state machine.
- **Unreal:** export as Animation Sequences + State Machine for AnimBP.
- **Godot:** export as AnimationPlayer or AnimationTree resources.

### Audio/music/dialog → all three
- Export as WAV/OGG/FLAC + lineage sidecar; standard import.

### 3D mesh (v2)
- Export as glTF 2.0 + lineage sidecar. Universal across all three engines.

### Round-trip
- The reverse direction (engine → GSPL) is harder. v1 supports importing existing sprites/animations as starting points for evolution; round-trip lineage preservation is v2.

## Engine-specific plugins

GSPL ships engine plugins for each:
- **Unity:** "GSPL Lineage Browser" — view and import seeds with their lineage.
- **Unreal:** "GSPL Asset Bridge" — Datasmith-style sync.
- **Godot:** "GSPL Native" — first-party plugin with bidirectional sync.

These plugins are signed by the GSPL release key (Brief 042) and distributed through each engine's plugin marketplace plus the GSPL marketplace.

## Differentiation vs Unity Muse, MetaHuman, etc.

| Capability | Unity Muse | Unreal MetaHuman | GSPL |
|---|---|---|---|
| Local execution | ❌ | partial | ✅ |
| Open weights | ❌ | ❌ | ✅ |
| Lineage tracking | ❌ | ❌ | ✅ |
| Provenance | ❌ | partial | ✅ |
| Cross-engine | ❌ | ❌ | ✅ |
| Multi-modal in single project | partial | partial | ✅ |
| Marketplace with royalties | Asset Store | Marketplace | GSPL marketplace + engine marketplaces |
| Federation | ❌ | ❌ | ✅ |
| Sovereignty | ❌ | ❌ | ✅ |
| Evolution operators | ❌ | ❌ | ✅ |
| Subscription required | ✅ | partial | ❌ |

## What GSPL absorbs

### From Unity
- **Asset import patterns** for sprite atlases and animation clips.
- **Asset Store taxonomy** as a starting point for marketplace categories.
- **Cross-platform deploy targets** as the export matrix.

### From Unreal
- **MetaHuman quality bar** for character generation (long-term aspiration).
- **Datasmith bridging** as the model for live sync between GSPL and an external editor.
- **Source-available philosophy** as a middle ground between fully open and fully closed.

### From Godot
- **Open-source community model** as the cultural anchor.
- **GDScript simplicity** as the model for the studio scripting layer (if any).
- **Resource-based asset model** as the integration target for the tightest integration.

## What GSPL doesn't try to do

- **Become a game engine.** No physics simulation, no scene graph, no scripting, no game loop.
- **Replace MetaHuman.** Photoreal human creation is a separate problem with different tooling needs; GSPL's strength is stylized and procedural.
- **Compete with engine asset stores.** GSPL's marketplace is *complementary* — engine asset stores list final assets; GSPL's marketplace lists *seeds* (which can generate many assets).

## Risks identified

- **Unity Muse improves rapidly.** Mitigation: GSPL's structural advantages (lineage, sovereignty, federation) survive even if Muse closes the quality gap.
- **Engine plugin maintenance burden.** Mitigation: shared core in Rust + thin per-engine bindings; community contribution model for plugins.
- **Engine IP terms restrict plugin distribution.** Mitigation: legal review per engine; Unity and Unreal both allow plugin marketplaces.
- **Engine update breakage.** Each major engine update can break plugins. Mitigation: CI matrix tested against each engine LTS.
- **Round-trip lineage loss.** When users edit imported assets in the engine, GSPL lineage is broken. Mitigation: clear "fork point" in lineage when round-tripping; v2 bidirectional sync.

## Recommendation

1. **Position GSPL as the substrate for game engines, not a competitor.** Public messaging focuses on integration, not replacement.
2. **First-party plugins for Unity, Unreal, Godot at v1.** Sprite + animation + audio export.
3. **3D / mesh export at v2** via glTF.
4. **Round-trip and bidirectional sync at v2.**
5. **Plugin distribution via engine marketplaces and GSPL marketplace.**
6. **Quarterly engine compatibility CI.**
7. **Marketing language**: "Generate in GSPL, ship in your engine."
8. **Strategic partnership outreach** with Godot Foundation (cleanest cultural fit).

## Confidence
**4/5.** The integration model is conventional and well-understood; the positioning is defensible. The 4/5 reflects honest uncertainty about engine plugin maintenance overhead.

## Spec impact

- `architecture/engine-integration.md` — full export and plugin matrix.
- `marketing/competitive-game-engines.md` — public positioning.
- `protocols/glTF-export.md` — 3D export format.
- New ADR: `adr/00NN-substrate-not-engine.md`.

## Open follow-ups

- Build first-party plugins for Unity, Unreal, Godot.
- Set up engine compatibility CI.
- Engage Godot Foundation about partnership.
- Plan v2 bidirectional sync architecture.
- Define round-trip fork-point UX.

## Sources

- Unity, Unreal Engine, Godot official documentation.
- Unity Muse and Sentis documentation.
- Unreal MetaHuman documentation.
- Godot plugin development guide.
- Internal: Briefs 002, 003, 014, 044, 048.
