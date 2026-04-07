# 072 — How GSPL beats Unreal at AAA 3D rendering

## Question
Brief 065 conceded that "Unreal wins" at AAA 3D rendering. That concession was premature. How does GSPL surpass Unreal — Lumen, Nanite, Chaos, virtualized geometry, real-time global illumination — using a substrate that is neural-first, differentiable, lineage-aware, and federated?

## Why it matters
3D rendering is the highest-prestige technical category in interactive media. If GSPL has a hole here, it's a permanent ceiling on its credibility for serious creators. The right answer is not "we export to Unreal" (that's table-stakes integration); the right answer is "GSPL renders natively in a way Unreal architecturally cannot."

## What we know from the spec
- Brief 002, 003: image and 3D engines.
- Brief 026: deterministic kernel.
- Brief 037: DQD (parameter exploration).
- Brief 040: critic ensemble.
- Brief 052: lineage time machine.
- Brief 054: three-tier rendering (deterministic / native fast / differentiable).
- Brief 071: differentiable simulation substrate.

## Findings — Unreal's structural limits

Unreal Engine 5 is a triumph of conventional rendering — Lumen for real-time global illumination, Nanite for virtualized micro-polygon geometry, Chaos for physics, MetaHuman for characters. But every one of these is locked into three architectural assumptions GSPL does not share:

1. **Rasterization-first with bolted-on neural and ray tracing.** Unreal's core pipeline is still triangle rasterization. Lumen is a hybrid; ray tracing is optional. Neural rendering is not native; it is a plugin path. The render graph cannot natively run a NeRF or a 3D Gaussian splat alongside meshes without engine surgery.
2. **Closed engine, source-available license.** Plugins are second-class. The render thread is owned by Epic. Substrate-level changes (like content-addressed scene caching) require an Epic-blessed engine fork.
3. **Single-machine rendering loop.** The frame is rendered locally. There is no first-class concept of borrowing render compute from a peer with cryptographic verification of what they rendered.

These are not features Epic can add without rewriting Unreal. GSPL inherits none of them.

## Findings — what GSPL ships that Unreal can't

### 1. Neural-first rendering substrate
The last five years of academic and industrial work have produced a new family of renderers that do not use triangles as the primitive: NeRF (Mildenhall et al. 2020) and its descendants (Mip-NeRF, Instant-NGP, Zip-NeRF), 3D Gaussian Splatting (Kerbl et al. 2023) and its real-time variants, neural radiance caches (Müller et al. 2021), and 4D radiance fields for video. These outperform rasterization on (a) photometric realism for captured scenes, (b) view synthesis quality, (c) memory efficiency for very high-detail scenes, and (d) integration with diffusion models.

GSPL ships these as **first-class engines on the substrate**, not as plugins. A scene in GSPL can be a mesh, a NeRF, a Gaussian splat, a procedural primitive, or a composition of all of them via cross-engine breeding (Brief 014, Brief 071 INV-202).

**Concrete win:** Capture a real-world environment with a phone in 5 minutes, drop the resulting Gaussian splat into a GSPL scene, light it with a procedural sun simulation, populate it with diffusion-generated characters, render at film quality. Unreal cannot do this without three plugins, two manual exports, and a technical artist.

### 2. Differentiable rendering for inverse problems
Differentiable rendering (Mitsuba 3, nvdiffrast, redner, drjit) lets you compute gradients of rendered pixels with respect to scene parameters — material properties, light positions, geometry, camera parameters. Combined with a target image and a perceptual loss, you can *invert* the rendering pipeline to recover scene properties from references.

GSPL's differentiable rendering tier (Brief 054) ships this as a native operation. "Match this reference photo's lighting" is a one-line gradient descent. "Make this scene look like this concept art" optimizes through the renderer.

**Concrete win:** A solo creator dials in lighting in seconds via reference matching. In Unreal, this is hours of manual tuning by a lighting artist.

### 3. Lineage-aware radiance caching (INV-203)
Unreal recomputes lighting on every frame change. Its hybrid Lumen system caches some indirect illumination but the cache is per-session and tied to the running engine.

GSPL caches radiance fields and light transport solutions in the lineage. Every irradiance probe, every neural cache, every Gaussian splat is a content-addressed lineage node. When the user changes a single light position, the lineage walker identifies which radiance contributions are still valid and reuses them; only the affected sub-graph re-solves. Across the federation, cached radiance solutions are shareable: if your scene matches a peer's cached lighting, GSPL pulls it.

**Concrete win:** Iterating on lighting in a complex scene is 10-100× faster than in Unreal because the radiance field is lineage-cached, not session-cached.

### 4. Compositional renderers via cross-engine breeding
GSPL's substrate (Brief 014, Brief 041 INV-103) lets renderers compose. A mesh renderer, a NeRF renderer, a 3D Gaussian splat renderer, and a procedural renderer can all contribute to a single frame, with the lineage tracking which pixels came from which sub-renderer. Unreal has one render path; everything else is layered atop or composited externally.

**Concrete win:** Stylized rendering (cel shading, painterly, watercolor) composed with photoreal lighting in the same frame. In Unreal this is a custom shader and a multi-pass setup; in GSPL it's a cross-engine composition.

### 5. Train-your-own neural shader on user content
GSPL's substrate exposes parameter spaces as differentiable manifolds (Brief 071). A neural shader (e.g., a small UNet that takes a G-buffer and outputs a stylized frame) can be trained in-studio on a few reference images. The lineage records the training run, the model weights, and the inference call.

**Concrete win:** "Make my game look like this concept artist's portfolio" is a 10-minute fine-tune. In Unreal it's a custom shader weeks of work.

### 6. Federated render compute (depends on Brief 075)
A frame can be rendered in parallel across federated peers. Cryptographic attestation guarantees correctness. Settlement flows through the marketplace. Unreal needs Pixel Streaming + a corporate render farm.

**Concrete win:** A solo indie can render film-quality animation by federating across friends, paying in marketplace credits. AAA-quality output without an AAA budget.

### 7. Lineage time machine for scene editing
Brief 052's time machine extends to scene state. Every camera angle, every light change, every prop move is a lineage node. Branch, what-if, replay all work natively. Unreal's "undo" is a stack; GSPL's is a graph.

**Concrete win:** "What did the scene look like three days ago when the lead said it was perfect?" is a one-click navigation. In Unreal it's a search through git history and a manual restore.

### 8. Provenance for rendered output (Brief 008, 058)
Every rendered frame is c2pa-attested back to the scene gseed and the engine version. For VFX, advertising, and any production where the audit trail matters, GSPL has it natively.

## What GSPL ships at each phase

### v1
- **Mesh rasterization engine** at Unreal Lumen-comparable quality via wgpu (Brief 054).
- **Diffusion-based 2D rendering** for stylized output.
- **Lineage-aware scene caching infrastructure**.
- **Critic-guided lighting search**.
- **Modest 3D quality** — honestly trailing Unreal raw quality, but with substrate advantages.

### v1.5
- **3D Gaussian splatting engine** for capture-based scenes.
- **NeRF/Instant-NGP engine** for view synthesis.
- **Differentiable rendering tier** for inverse problems.
- **Neural shader fine-tuning in studio**.
- **Cross-engine breeding** of mesh + NeRF + Gaussian splat.

### v2
- **Real-time path tracing** via wgpu's RT extensions where available.
- **Production neural radiance caching** matching Lumen quality.
- **Federated render compute** (depends on Brief 075).
- **Inverse-rendering scene capture** end-to-end.

### v3
- **End-to-end neural game rendering** — no triangles, just gseeds and learned renderers.

## Inventions

### INV-203: Lineage-aware radiance caching
Cache radiance solutions by content-addressed lineage hash. Federation-shareable. Dependency analysis identifies stale sub-graphs on parameter changes. Novel because no rendering system (game or offline) treats radiance as a federated content-addressed resource.

### INV-204: Compositional cross-renderer breeding
Multiple rendering engines (mesh, NeRF, splat, neural shader, procedural) contribute to a single frame via the substrate's naturality square (Brief 041 INV-103). The lineage tracks per-pixel provenance. Novel because all production renderers assume a single primary primitive type.

### INV-205: In-studio neural shader fine-tuning
The studio exposes a "train this look on these references" operation that fine-tunes a small neural renderer on user-supplied images. The result is a gseed-bound, signed neural shader. Novel because no game engine ships in-engine fine-tuning; Unreal Muse and Unity Sentis do inference only.

## What Unreal still does better at v1

Honest accounting:
- **Real-time AAA quality on consumer GPUs** for triangle-based scenes. Unreal wins at v1.
- **Nanite virtualized geometry** at hundreds of millions of polygons. GSPL doesn't replicate this for v2.
- **Chaos physics at production scale.** GSPL competes via Brief 071 but Unreal wins on sheer throughput.
- **MetaHuman pipeline.** GSPL competes via Brief 073.
- **AAA studio adoption and tutorials.** GSPL community starts at zero.

These are time and engineering investments, not architectural moats. GSPL closes them by leveraging the *correct* substrate for the *next* decade of rendering, where Unreal is leveraging the substrate from the *previous* decade.

## The strategic claim

Triangle rasterization is not the future of rendering. Neural rendering is. Every major research lab and rendering company has converged on this. GSPL is built around the new substrate from day one; Unreal is built around the old substrate and bolting the new on. **In the long run this is a structural advantage even more decisive than the lineage advantage.** GSPL doesn't have to beat Unreal at triangles; it has to beat them at neural-first rendering, which Unreal architecturally cannot do.

## Risks identified

- **Neural rendering is not yet at AAA real-time quality.** Mitigation: ship hybrid (mesh + neural) at v1; pure neural at v2-v3 as the field matures.
- **Open-weight neural renderers are research-grade.** Mitigation: GSPL contributes to and ships the best open implementations; engages researchers.
- **GPU memory for radiance caches is large.** Mitigation: federation, distillation, content-addressed sharing.
- **Unreal adopts neural rendering aggressively.** Probability: medium. Mitigation: Epic's plugin-path approach can't match substrate-native; the lineage and federation advantages survive even at quality parity.
- **Stylized vs photoreal split.** GSPL wins at stylized first, photoreal later. Mitigation: align v1 launch with the stylized creator audience.

## Recommendation

1. **Reverse the Brief 065 concession.** GSPL competes natively at AAA 3D rendering via neural-first substrate.
2. **Ship Gaussian splatting and NeRF as v1.5 engines.** Open-weight implementations exist.
3. **Implement INV-203 (lineage-aware radiance caching) as a headline performance demo.**
4. **Differentiable rendering tier at v1.5** with reference-matching as the killer demo.
5. **In-studio neural shader fine-tuning at v2** (INV-205).
6. **Engage NeRF, 3DGS, neural rendering research communities** as advisors.
7. **Position as "neural-first 3D"** in marketing — the framing nobody else owns.
8. **Marketing language**: "Unreal renders triangles. GSPL renders the future."

## Confidence
**4/5.** The neural rendering trajectory is well-established in research; open-weight implementations are advancing fast. The 4/5 reflects honest uncertainty about real-time AAA quality timing.

## Spec impact

- `architecture/rendering-substrate.md` — neural-first articulation.
- Update Brief 065 to remove the AAA rendering concession.
- New ADR: `adr/00NN-neural-first-rendering.md`.
- New ADR: `adr/00NN-lineage-aware-radiance-cache.md`.

## Open follow-ups

- Pick v1.5 NeRF/3DGS backbone implementations.
- Build INV-203 prototype.
- Engage Mildenhall, Kerbl, NVIDIA NeRF teams.
- Plan in-studio neural shader fine-tuning (INV-205).
- Quarterly benchmark vs Unreal Lumen on iteration time.

## Sources

- Mildenhall et al., "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis" (2020).
- Kerbl et al., "3D Gaussian Splatting for Real-Time Radiance Field Rendering" (2023).
- Müller et al., "Real-time Neural Radiance Caching for Path Tracing" (2021).
- Müller et al., "Instant Neural Graphics Primitives" (2022).
- Mitsuba 3 differentiable rendering documentation.
- nvdiffrast (Laine et al.).
- Epic Games Unreal Engine 5 documentation (Lumen, Nanite, Chaos).
- Internal: Briefs 002, 003, 014, 026, 037, 040, 041, 052, 054, 058, 065, 071, 075.
