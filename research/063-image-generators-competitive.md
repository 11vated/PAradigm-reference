# 063 — Image generators: Stable Diffusion, Flux, Midjourney

## Question
How does GSPL compare against the dominant image-generation systems — Stable Diffusion (and its forks), Black Forest Labs' Flux, and Midjourney — and where exactly does GSPL outperform, match, or trail them? What does GSPL need to absorb from each, and what is structurally impossible for them to copy from GSPL?

## Why it matters
Image generation is the most mature, most contested, and most commercially saturated AI-creation space. If GSPL cannot articulate a defensible differentiation against these three categories — open diffusion (SD/SDXL/SD3), state-of-the-art open weights (Flux), and best-in-class hosted (Midjourney) — it will be perceived as "another generator." The competitive matrix has to be honest, axis-by-axis, with no flinching.

## What we know from the spec
- Brief 003: shipped models include SD-class image engines.
- Brief 008: c2pa provenance.
- Brief 009: watermarks.
- Brief 029-034: agent and modifier surfaces.
- Brief 048: studio architecture.
- Brief 052: lineage time machine.
- Briefs 036-041: novelty, DQD, POET, evolution operators.

## Findings — competitor profiles

### Stable Diffusion family (SD 1.5, SDXL, SD3, SDXL-Turbo, SD3.5)
**Operator:** Stability AI; weights public.
**Architecture:** Latent diffusion model with VAE encoder/decoder, U-Net or DiT backbone, CLIP/T5 text encoder.
**Strengths:**
- Fully open weights and code; runs locally on consumer GPUs.
- Vast ecosystem: ControlNet, LoRA, IP-Adapter, custom checkpoints, dreambooth.
- ComfyUI and Automatic1111 expose every knob; the power-user community is enormous.
- Strong fine-tunability; thousands of community models on Civitai.
- Cheap to run; quantized variants run on 6-8GB VRAM.

**Weaknesses:**
- Aesthetic ceiling lower than Midjourney/Flux for generic "make it pretty" prompts.
- Anatomy and text rendering historically weak (improved in SD3 but still trails Flux).
- No first-class lineage; ComfyUI graphs are workflow-as-pipeline, not history-as-graph.
- Provenance and watermarking are bolted on, not constitutional.
- Identity/sovereignty story is essentially "you ran it locally" — no signed identity, no marketplace primitives.
- Quality varies wildly by checkpoint and sampler; UX punishes novices.

### Flux (Black Forest Labs)
**Operator:** Black Forest Labs (founders ex-Stability).
**Architecture:** Rectified flow + DiT (12B params for Flux.1 dev/pro).
**Strengths:**
- State-of-the-art aesthetic quality among open-weight models as of v1.
- Excellent text rendering and prompt adherence — best-in-class for open weights.
- Schnell variant runs in 1-4 steps.
- Open weights (Schnell, Dev) under permissive-ish licenses.
- Strong commercial backing.

**Weaknesses:**
- Fewer ControlNets and adapters than SD ecosystem (catching up).
- Pro model is API-only and gated.
- 12B params demands 16-24GB VRAM for full quality; quantized is fine but quality drops.
- No first-class lineage, no provenance, no marketplace, no critique loop.
- Single-shot generation philosophy — no built-in iteration or evolution.

### Midjourney
**Operator:** Midjourney Inc; closed-weights, hosted-only.
**Architecture:** Proprietary; rumored DiT + heavy aesthetic post-training and human-preference RLHF.
**Strengths:**
- Best-in-class aesthetic quality for "make it look amazing" out of the box.
- Dominant brand, large paying community.
- Discord and web UI tuned for fast iteration; the "/imagine, vary, upscale" loop is efficient.
- Best-in-class style control and consistency (style references, character references, mood boards).
- No setup; works on any device with a browser.

**Weaknesses:**
- Closed model; no local execution; no fine-tuning by users.
- No offline use; no sovereignty.
- Subscription pricing creates ongoing cost dependence.
- IP terms are murky and have changed multiple times.
- No lineage history exposed to users beyond the chat scrollback.
- No interoperability with other tools beyond image export.
- Cannot ship for commercial pipelines that need on-device inference.

## Axis-by-axis comparison

| Axis | SD | Flux | MJ | GSPL |
|---|---|---|---|---|
| Local execution | ✅ | ✅ | ❌ | ✅ |
| Open weights | ✅ | ✅ (mostly) | ❌ | ✅ |
| Aesthetic ceiling | 6/10 | 9/10 | 10/10 | 7/10 v1 → 9/10 v1.5 |
| Prompt adherence | 7/10 | 9/10 | 8/10 | 7/10 (uses same backbones) |
| Text rendering | 6/10 | 9/10 | 8/10 | inherits from engine |
| Controllability | 9/10 | 7/10 | 7/10 | 9/10 (modifier surfaces) |
| First-class lineage | ❌ | ❌ | ❌ | ✅ |
| Provenance (c2pa) | ❌ | ❌ | ❌ | ✅ |
| Watermarks | ❌ | ❌ | partial | ✅ |
| Signed identity | ❌ | ❌ | ❌ | ✅ |
| Marketplace primitives | community | ❌ | ❌ | ✅ |
| Critique loop | ❌ | ❌ | ❌ | ✅ |
| Evolution operators | ❌ | ❌ | partial (vary) | ✅ (10 native) |
| Time machine | ❌ | ❌ | ❌ | ✅ |
| Federation | ❌ | ❌ | ❌ | ✅ |
| Offline | ✅ | ✅ | ❌ | ✅ |
| Sovereignty | partial | partial | ❌ | ✅ |
| Multi-engine composition | ❌ | ❌ | ❌ | ✅ |
| Cross-modal | ComfyUI hacks | ❌ | ❌ | ✅ (sprites/audio/etc.) |
| Determinism | ✅ (seed) | ✅ (seed) | partial | ✅ (seed + lineage) |
| User onboarding | 3/10 | 4/10 | 9/10 | 7/10 target |

**GSPL wins on:** sovereignty, lineage, provenance, signed identity, marketplace primitives, evolution operators, time machine, federation, multi-engine composition, cross-modal, controllability. Eleven axes that are constitutional, not iterations.

**GSPL trails on:** raw aesthetic ceiling at v1 (uses SD/Flux as backbones), prompt adherence (same reason), Midjourney's onboarding polish.

**GSPL ties on:** local execution (with SD/Flux), determinism, openness.

## What GSPL absorbs from each

### From SD ecosystem
- **ControlNet pattern** for spatial conditioning. GSPL exposes ControlNet-style constraints as modifier surfaces (Brief 049).
- **LoRA fine-tuning** as a first-class engine feature. Users can train and ship LoRAs as gseed artifacts with their own provenance and lineage.
- **Sampler diversity** as user-selectable dials.
- **Civitai-style checkpoint sharing** model — but with signed identity and provenance instead of an ad-supported central host.

### From Flux
- **Rectified flow + DiT** as the v1.5 image engine target (when weights and licensing permit). GSPL's image engine is pluggable specifically so the best backbone of the moment can be the default.
- **Few-step generation** for the live preview loop (Schnell-style).
- **Aesthetic-aligned post-training** as a recipe for the GSPL model card requirements.

### From Midjourney
- **Aesthetic post-training and preference RLHF** as a quality strategy. Even open backbones can be re-tuned for aesthetic consistency.
- **Style reference** and **character reference** as first-class modifier surfaces.
- **Onboarding feel** — a great first generation in under 60 seconds with no setup. The "first wow moment ≤5 min" target (Brief 051) is directly inspired.

## What is structurally impossible for them to copy

### Lineage as native data structure
Adding lineage to SD/Flux/MJ requires either re-architecting the entire generation pipeline or bolting on a workflow recorder (which is what ComfyUI is, and it's not lineage). GSPL's lineage is integral to the seed format, not a UI feature.

### Federation without a central operator
SD has a community, but Civitai is a centralized host. MJ is a single company. Flux is a single company. None can become *federated* without abandoning their business model.

### Multi-engine composition
Stable Diffusion only generates images. To do sprites, audio, or 3D, the user has to leave the tool and use a different system. GSPL's substrate explicitly supports cross-engine breeding (Brief 041's naturality-square operator) — a competitor would have to rebuild their core to match this.

### Evolution operators on the substrate
A competitor *could* add a "vary" button (and MJ has). But ten native evolution operators with bandit selection over operator history (Brief 041) requires the substrate to expose the math. A diffusion-only system has no place to plug in a FIM-weighted mutation.

### Sovereignty and identity
A hosted service cannot become user-sovereign without ceasing to be hosted. GSPL's three-tier key storage (Brief 042), signed identity (Brief 042), and anonymous publication (Brief 047) are constitutional commitments that competitors cannot adopt without rewriting their business.

## Gaps GSPL must close

### Aesthetic quality at v1
GSPL ships SD/Flux as image engines. v1 quality on standard prompts will trail MJ. Mitigations:
- Ship the best open-weight model available at each release.
- Expose preference RLHF as an in-studio feature ("tune this model on the variants you liked").
- Critique ensemble (Brief 040) actively reranks variants for aesthetic quality.
- Shipped style packs that are expert-tuned.

### Prompt adherence
Same root cause; same mitigations. Plus: the planner agent (Brief 029) rewrites prompts before they hit the engine, which improves adherence beyond what the bare model offers.

### Onboarding polish
Brief 051's first-wow-moment target. The studio must feel as easy as MJ for the first generation — even though it has more under the hood.

## Risks identified

- **Backbone dependence:** GSPL's aesthetic ceiling is a function of the backbones it can ship. Mitigation: rapid model registry updates (Brief 055).
- **Open-weight licensing volatility:** Flux's license has changed; future models may be more restrictive. Mitigation: track multiple backbones; never depend on a single provider.
- **MJ-style polish gap:** large UX investment required. Mitigation: brief 049 + brief 051 prioritize this.
- **Community split:** SD users have huge investment in ComfyUI workflows. Mitigation: ship a ComfyUI workflow importer (Brief 030 modifier surfaces are a good target).
- **Hosted competitor going local:** MJ could ship a desktop version. Probability: low (their moat is the cloud-tuned model and aesthetic post-training). Mitigation: GSPL's lineage and provenance are still uncopyable.

## Recommendation

1. **Position GSPL as "the platform, not the model."** The image backbone is interchangeable; what GSPL offers is what surrounds it.
2. **Ship Flux Schnell as v1 default image engine** (license permitting) for aesthetic floor.
3. **Ship SDXL + community ControlNets** as the controllability floor.
4. **Implement preference RLHF as in-studio feature** for users to tune their own aesthetic.
5. **Ship a ComfyUI workflow importer** to capture the SD power-user audience.
6. **First-wow-moment ≤60 seconds** target for the image generation first-run.
7. **Aesthetic style packs** curated and signed by GSPL (model card publication).
8. **Marketing language**: "Midjourney's quality, Flux's openness, Stable Diffusion's flexibility — all on your machine, with lineage and provenance."

## Confidence
**4/5.** The competitive picture is clear; the differentiation is real and structural. The 4/5 reflects honest uncertainty about how fast the open-weight aesthetic ceiling rises and whether MJ will pivot.

## Spec impact

- `architecture/image-engine.md` — pluggable backbone, ControlNet, LoRA support.
- `marketing/competitive-image.md` — public competitive positioning.
- New ADR: `adr/00NN-pluggable-image-backbones.md`.
- Update Brief 003 image engine plan to prioritize Flux Schnell.

## Open follow-ups

- Track Flux licensing changes monthly.
- Build the ComfyUI workflow importer.
- Curate v1 style packs.
- Plan in-studio preference RLHF.
- Quarterly aesthetic benchmark vs MJ/Flux/SD on a fixed prompt set.

## Sources

- Stable Diffusion technical reports (Stability AI).
- Flux technical card (Black Forest Labs).
- Midjourney public statements and user research.
- ComfyUI and Automatic1111 ecosystem.
- Civitai marketplace observation.
- Internal: Briefs 003, 008, 009, 029-034, 040, 041, 048, 049, 051, 055.
