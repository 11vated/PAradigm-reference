# 137 — Multi-modal backbone selection

## Question

Which open-weight multi-modal backbone is the right v0.1 default for vision-bearing namespaces (image, sprite, character, vehicles, built-world, materials), and how does it compose with the Brief 122 Qwen3-MoE-A22B text-default?

## Why it matters (blast radius)

GSPL's substrate is *content*-rich: sprites, images, character canon, materials, the universal anything-to-gseed pipeline (Brief 089). Without a vision backbone, half of v0.1's namespaces are blind to their own gseeds. Picking wrong here either bloats the floor hardware (Brief 135 violation), or ships a vision model that hallucinates against the grounding floor (Brief 097 violation), or fragments the kernel into two backbones with incompatible adapters (Brief 129 violation).

## What we know from the spec

- Brief 110 (Round 6) surveyed open-weight backbones and noted multi-modal options were deferred.
- Brief 122 selected Qwen3-MoE-A22B as the text default (with Qwen3-14B as the v0.1 floor backbone, Brief 135).
- Brief 089 specifies the universal-conversion pipeline assumes the kernel can read images.
- Brief 087 ships a visual phenomena coverage atlas.

## Findings

1. **Three credible v0.1 candidates: Qwen2.5-VL, Llama-3.2-Vision, Pixtral.** All three are Apache-2-or-Llama-license, all three handle native image input at variable resolution, all three are available in multiple sizes.

2. **Qwen2.5-VL is the architecturally consistent choice.** It shares tokenizer, attention pattern, and adapter format with the Qwen3 text default selected in Brief 122. This means LoRA adapters trained on Qwen3 can compose with Qwen2.5-VL's vision tower without re-training, *provided* we use Qwen2.5-VL as a vision encoder feeding into the Qwen3 backbone rather than as a standalone model. This is the standard "vision adapter" pattern.

3. **Two sizes for two tiers.** Qwen2.5-VL-3B fits the floor (24GB VRAM) alongside Qwen3-14B with ~2GB headroom. Qwen2.5-VL-7B is the mid-tier choice (48GB VRAM). The 72B variant is v0.2+.

4. **Native resolution handling matters.** Qwen2.5-VL processes images at native aspect ratio (no aggressive downsampling), which is critical for sprite namespaces where pixel-grid integrity is the entire point. Llama-3.2-Vision downsamples more aggressively. This alone tips the decision toward Qwen2.5-VL.

5. **Vision tower as a primitive tool.** Per Brief 128, the vision encoder is exposed as a primitive tool `vision.embed(image) → embedding[1024]`. This decouples the backbone from the vision tower at the action-space layer — if we swap visions later, only the tool implementation changes, not the kernel.

6. **The grounding floor for image content is graph proximity.** Brief 097's grounding-floor mechanism applies: when the model produces an image-related claim, the claim must have a parent edge to the visual phenomena atlas (Brief 087) or to a creator's grounded seed. Vision encoder embeddings are used for the parent-edge nearest-neighbor lookup.

7. **No native vision generation in v0.1.** Qwen2.5-VL is encoder-only (image in, text out). Image *generation* in v0.1 still routes to the substrate's existing image engine (Brief 022). The vision backbone provides understanding and grounding, not generation. This is a deliberate scope cut for v0.1.

8. **Audio is deferred to v0.2.** Audio understanding (music, speech, sound design namespaces) needs a separate audio encoder. Brief 086C ships audio gseed schemas, but no audio encoder is in the v0.1 budget. Defer to Brief 149 scope finalization.

9. **Multi-modal floor budget.** Adding Qwen2.5-VL-3B to the Brief 135 floor map: ~3GB VRAM additional. Total memory map at the floor with vision: backbone 7GB + KV 3GB + vision 3GB + router 0.4GB + reranker 0.6GB + LoRA 1.5GB + verifier 0.5GB + activation 3GB + headroom 5GB = 24GB. Tight but feasible. Vision is on by default; battery mode disables it.

10. **License compatibility.** Qwen2.5-VL is Apache 2.0, identical to Qwen3. No license fragmentation across the v0.1 backbone family. Llama-3.2-Vision is Llama-license, slightly more restrictive on commercial federation.

## Risks identified

- **Vision tower drift relative to Qwen3.** Qwen2.5-VL was trained against Qwen2.5-text, not Qwen3. The cross-version adapter composition is empirically supported but not officially blessed. Mitigation: validate on the canonical eval battery's image-namespace family before committing; if drift is significant, pin Qwen2.5-VL with a small bridging adapter.
- **Vision hallucination on long-tail content.** Qwen2.5-VL hallucinates on out-of-distribution visual content (just like every VLM). Mitigation: the grounding floor (Brief 097) catches it — if a vision claim has no parent edge, it's flagged low-confidence.
- **3GB extra VRAM is real headroom loss.** Battery mode and 16GB VRAM users lose vision. Mitigation: ship a CPU-fallback vision encoder (Qwen2.5-VL-3B int8 on CPU runs at ~2 sec per image, acceptable for non-interactive paths).

## Recommendation

**Adopt Qwen2.5-VL-3B as the v0.1 vision backbone, mounted as the vision tower feeding the Qwen3-14B text backbone via the standard vision-adapter pattern. Mid tier uses Qwen2.5-VL-7B. Vision encoder is exposed as the primitive tool `vision.embed`. Vision is on by default at the floor; battery mode disables it; CPU-fallback path serves the no-VRAM-headroom case at higher latency. Image generation stays in the substrate's existing image engine — Qwen2.5-VL is encode-only at v0.1. Audio defers to v0.2. License: Apache 2.0 across the entire v0.1 backbone family.**

## Confidence

**4/5.** The architecture-consistency argument is strong. The unknowns are: (a) actual cross-version adapter quality (needs Round 7 measurement on the eval battery), and (b) whether the 3GB headroom holds across all v0.1 workflows under load.

## Spec impact

- `gspl-reference/intelligence/vision-backbone.md` — new file documenting the Qwen2.5-VL-3B floor selection, the vision-tower mounting pattern, the vision.embed primitive, and the CPU-fallback path.
- `gspl-reference/research/110-mixture-of-experts-architectures.md` — cross-reference at the open-weight backbone survey.
- `gspl-reference/research/135-hardware-budget-v0-1-context-ceiling.md` — update the floor memory map to include the +3GB vision allocation.
- `gspl-reference/research/128-gspl-tool-use-and-modifier-surface.md` — add `vision.embed` to the primitive tool catalog.

## New inventions

- **INV-567** — *Vision-tower-as-primitive-tool decoupling.* The vision encoder is exposed as a tool, not as a kernel-internal subsystem, so swapping vision backbones is a tool-implementation swap rather than a kernel rebuild.

## Open follow-ups

- Cross-version Qwen2.5→Qwen3 adapter quality (Round 7 measurement).
- Audio encoder selection for v0.2 (defer to Round 7+).
- Whether to ship a vision-generation-side adapter for Brief 089's universal pipeline (defer to Brief 149).

## Sources

1. Qwen team, *Qwen2.5-VL Technical Report*, 2024.
2. Meta, *Llama 3.2 Vision Models*, 2024.
3. Mistral, *Pixtral 12B*, 2024.
4. Brief 087 — Visual phenomena coverage atlas.
5. Brief 089 — Universal anything-to-gseed pipeline.
6. Brief 097 — Anti-hallucination test suite.
7. Brief 122 — Qwen Code architecture teardown.
8. Brief 135 — Hardware budget for v0.1.
