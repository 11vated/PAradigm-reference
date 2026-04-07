# 064 — Video generators: Sora, Veo, Runway

## Question
How does GSPL compare against the dominant video-generation systems — OpenAI Sora, Google Veo, Runway Gen-3 — and what is GSPL's realistic v1 video story given that none of these are open weights and the underlying compute is enormous?

## Why it matters
Video generation is the next frontier and the most capital-intensive AI-creation modality. GSPL cannot compete on raw model quality at v1; the compute and training data of Sora/Veo are out of reach. But GSPL can win on the *workflow around* video — lineage, scene-by-scene composition, consistency control, and the inevitable open-weight catch-up. The question is what to ship at v1, what to defer to v1.5, and where the structural moats are.

## What we know from the spec
- Brief 003: video engine deferred from v1 in some plans.
- Brief 052: time machine and lineage.
- Briefs 029-034: agent and modifier surfaces.
- Brief 048: studio architecture supports any engine.
- Brief 037: DQD (relevant to video parameter exploration).

## Findings — competitor profiles

### OpenAI Sora
**Operator:** OpenAI; closed-weights, hosted-only, gated access.
**Architecture:** Diffusion transformer over latent video patches; multi-resolution training; long-context.
**Strengths:**
- Best-in-class prompt-to-video at long durations (60s+).
- Strong physical realism and temporal coherence.
- Storyboard mode, in-painting, video-to-video.
- Backed by enormous compute.

**Weaknesses:**
- Closed; no local execution.
- Subscription gated; very limited free tier.
- No fine-tuning by users.
- Limited control surfaces (no ControlNet equivalent).
- No lineage, no provenance, no marketplace.
- Generations are not reproducible across the same prompt.

### Google Veo (Veo 2/3)
**Operator:** Google DeepMind; closed-weights, integrated into Vertex AI and consumer products.
**Architecture:** Latent diffusion video model; large-scale training on YouTube-derived data.
**Strengths:**
- Best-in-class consistency and physical plausibility as of latest version.
- Tight integration with Google products.
- Strong audio-video joint generation.

**Weaknesses:**
- Closed; hosted only.
- Heavy gating and rate-limiting.
- Enterprise-priced.
- No user fine-tuning.
- No lineage, no provenance, no sovereignty.

### Runway Gen-3 / Gen-4
**Operator:** Runway; closed-weights, hosted.
**Architecture:** Proprietary diffusion video model; integrated editing suite.
**Strengths:**
- Most comprehensive video editor around an AI model.
- Motion brush, camera controls, video-to-video, in-painting, style transfer.
- Best UX for video creators among the three.
- Pioneer of the AI-video creator workflow.

**Weaknesses:**
- Closed; hosted; subscription.
- Quality trails Sora/Veo on physical realism.
- Compute-heavy; per-clip cost adds up.
- No lineage, no provenance, no sovereignty.

## Open-weight video state-of-the-art

GSPL's v1 video story depends on what's actually shippable. As of the substrate-research cutoff, the open-weight video landscape is:
- **Stable Video Diffusion (SVD):** Stability AI; ~14 frames at 1024x576; image-to-video.
- **AnimateDiff:** community-trained motion modules over SD; relatively short clips.
- **Open-Sora:** open-source replication effort; promising but not at Sora quality.
- **Mochi 1:** Genmo's open-weight text-to-video; competitive with mid-tier hosted.
- **HunyuanVideo / CogVideoX / LTX-Video:** Chinese-lab open releases catching up rapidly.
- **Wan 2.1+ family:** open releases with strong prompt adherence.

The open-weight ceiling is rising fast but trails closed models by ~12-18 months in quality.

## Axis-by-axis comparison

| Axis | Sora | Veo | Runway | GSPL v1 | GSPL v2 |
|---|---|---|---|---|---|
| Local execution | ❌ | ❌ | ❌ | ✅ | ✅ |
| Open weights | ❌ | ❌ | ❌ | ✅ | ✅ |
| Quality (physical realism) | 10/10 | 10/10 | 7/10 | 5/10 | 8/10 |
| Quality (aesthetic) | 9/10 | 9/10 | 8/10 | 6/10 | 8/10 |
| Long-form (>30s) | ✅ | ✅ | partial | ❌ | partial |
| Consistency across shots | partial | partial | partial | ✅ (lineage) | ✅ |
| Lineage | ❌ | ❌ | ❌ | ✅ | ✅ |
| Provenance | partial | ✅ (SynthID) | ❌ | ✅ | ✅ |
| Watermark | ✅ visible | ✅ SynthID | partial | ✅ | ✅ |
| Editor integration | partial | ❌ | ✅ | ✅ | ✅ |
| Cost per minute | $$$ | $$$$ | $$ | one-time hardware | one-time hardware |
| Sovereignty | ❌ | ❌ | ❌ | ✅ | ✅ |
| Multi-shot scene composition | partial | partial | ✅ | ✅ | ✅ |
| Storyboard-as-lineage | ❌ | ❌ | ❌ | ✅ | ✅ |
| Multi-engine (with sprite/audio) | ❌ | ❌ | ❌ | ✅ | ✅ |

## v1 video strategy

GSPL cannot match Sora/Veo on raw quality at v1. The strategy is:

### Option A: Don't ship video at v1
Defer video to v1.5 when an open-weight model good enough to be respectable is reliably available. Focus v1 on image, sprite, audio, 3D where GSPL can compete.

### Option B: Ship a video engine for short clips
Use Mochi/LTX/Hunyuan/Wan for short (4-10s) clips. Position as "video moments, not long-form film" — clips are first-class GSPL artifacts with lineage and provenance. Honest about quality.

### Option C: Image-first storyboarding with AI motion
Generate images for each shot in the storyboard (where GSPL is strong), then use a smaller motion model (SVD-style) to add motion. The lineage is the storyboard. Avoids competing head-on with Sora.

**Recommendation: Option C at v1, Option B at v1.5, full long-form at v2.**

This plays to GSPL's structural advantages (lineage, multi-shot composition, storyboarding) while avoiding the worst quality comparisons.

## What GSPL absorbs

### From Sora
- **Long-context video DiT** as a v2 target architecture.
- **Storyboard mode** as a workflow primitive — but GSPL's version is the lineage DAG.
- **In-painting** as a modifier surface.

### From Veo
- **SynthID-style content provenance** — already mandated by Brief 008/009 with c2pa.
- **Joint audio-video generation** as a v2 target.

### From Runway
- **Motion brush** and **camera controls** as modifier surfaces (Brief 049). These are exactly the kind of high-leverage controls GSPL's modifier surface system is designed for.
- **Video-to-video** as a first-class engine operation.
- **Editor integration** as the studio model — Runway is the closest competitor to GSPL's "tool, not just a model" positioning.

## What is structurally impossible for them to copy

### Lineage as scene graph
GSPL's storyboard *is* the lineage DAG. Adding lineage to a video generator requires it to track every shot decision, every variant, every modifier. None of the three competitors have this; building it is months of engineering on top of an already-mature product.

### Cross-modal composition
GSPL can compose video with sprite (Brief 014), audio, music, and dialog from a single project. None of the three competitors integrate beyond their own model.

### Sovereignty
Sora/Veo/Runway are all hosted. They cannot become local without abandoning their compute model.

### Open-weight strategy
Even when Sora 2 or Veo 4 lands, they will still be closed. GSPL ships open weights from day one, so the open-weight ecosystem catch-up directly accrues to GSPL.

## Gaps GSPL must close

### Quality
The fundamental gap. Mitigations: ship the best open-weight model at each release; fine-tune for consistency on user content; use the critique loop to rerank generations.

### Long-form
Not solvable at v1. Focus on short clips; defer long-form to v1.5+.

### Audio-video joint generation
Defer to v1.5/v2. v1 ships separate audio engine.

### Cost
Local generation is cheap *per clip* but expensive *per second of compute*. Mitigation: smaller models for previews; only run full quality on user-marked finals.

## Risks identified

- **Open-weight quality stalls.** Mitigation: Option A/B fallback; honest about positioning.
- **Sora/Veo go more permissive.** Probability: low (compute moat). Mitigation: GSPL's substrate advantages survive even if quality parity arrives.
- **Runway pivots to local.** Probability: low (their compute is on cloud GPUs). Mitigation: GSPL's federation and sovereignty are still uncopyable.
- **User expectations set by Sora.** Mitigation: clear positioning ("short clips with full lineage and editor"); demo videos showing what GSPL is good at.
- **Compute requirements:** even open-weight video needs ~12-24GB VRAM. Mitigation: cloud-execution mode (Brief 055 hybrid mode); CPU fallback for preview-only.
- **Watermark policy:** Sora/Veo embed visible watermarks in commercial output. Mitigation: GSPL's c2pa is invisible-but-verifiable, satisfying provenance without aesthetic damage.

## Recommendation

1. **v1 ships Option C: image-first storyboarding with motion engine.** Honest positioning.
2. **v1.5 ships short-form video engine** based on best open weights at the time (Mochi/LTX/Hunyuan/Wan as candidates).
3. **v2 targets long-form** when open weights and local compute permit.
4. **Motion brush, camera control, and video-to-video as modifier surfaces** at v1.5.
5. **Storyboard-as-lineage** is the headline GSPL video feature from day one.
6. **c2pa attestations on every video frame** (Brief 008).
7. **Cloud execution mode** for users with insufficient local GPU.
8. **Quarterly model registry update** for video backbones.
9. **Marketing language**: "Sora is the model. Runway is the editor. GSPL is the workflow with lineage that you own."

## Confidence
**3/5.** Video is the highest-uncertainty modality. The 3/5 reflects honest uncertainty about open-weight catch-up timeline and the right v1 scope.

## Spec impact

- `architecture/video-engine.md` — phased plan A/B/C.
- `marketing/competitive-video.md` — public positioning.
- `protocols/storyboard-lineage.md` — storyboard as DAG.
- New ADR: `adr/00NN-video-phased-rollout.md`.
- Update Brief 003 to defer video engine to v1.5.

## Open follow-ups

- Pick v1.5 video backbone after evaluating Mochi/LTX/Hunyuan/Wan.
- Build storyboard UX in collaboration with Brief 049.
- Design motion brush modifier surface.
- Plan cloud execution mode for video.
- Quarterly video benchmark vs Sora/Veo/Runway on fixed prompt set.

## Sources

- Sora technical report (OpenAI).
- Veo technical card (Google DeepMind).
- Runway Gen-3 documentation.
- Open-Sora, Mochi, LTX-Video, HunyuanVideo, Wan 2.1 research papers and model cards.
- SynthID documentation.
- Internal: Briefs 003, 008, 009, 029-034, 037, 048, 049, 052, 055.
