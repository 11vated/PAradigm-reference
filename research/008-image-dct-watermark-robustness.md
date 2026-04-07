# 008 — Image DCT watermark robustness

## Question
What is the realistic robustness envelope for a DCT-domain image watermark in the Paradigm export pipeline against the attacks Paradigm needs to survive (JPEG re-encoding, resize, crop, screenshot), and what failure modes must the spec acknowledge?

## Why it matters (blast radius)
The image watermark is the spec's "last line of defense" provenance signal — it survives in cases where C2PA metadata is stripped (e.g., social media re-uploads, screenshots, copy-paste). If the watermark's robustness envelope is overstated, users will trust the provenance signal in cases where it has been silently destroyed. If understated, the spec will recommend a heavier or more invasive watermark than necessary. This brief gates `compliance/watermark-image.md` and `runtime/export-pipeline.md`.

## What we know from the spec
- `compliance/watermark-image.md` mandates a perceptually invisible watermark on every exported raster image.
- The spec assumes the watermark survives "common social media re-encoding" but does not yet quantify that.
- The watermark payload is small (≤ 64 bits) and conveys a pointer to the canonical content hash, not the full hash.

## Findings

1. **DCT-domain watermarks are inherently strong against JPEG re-encoding because both DCT and JPEG operate on the same 8×8 frequency-coefficient grid.** [1, 2, 3] Embedding in the mid-frequency band (typically coefficients in zigzag positions ~6 to ~21 of an 8×8 block) places the watermark in coefficients that are preserved through JPEG quantization at most quality levels and that are below the perceptual threshold of the human visual system.

2. **Published modern DCT-watermark schemes report PSNR > 38 dB and BER < 0.01% under JPEG quality factor Q=50.** [3] This is a strong result for the JPEG-only attack: at Q=50 (a very aggressive social-media-like compression), the watermark survives essentially perfectly.

3. **Resize attacks degrade the watermark significantly because resizing remixes which pixels fall in each 8×8 block.** [2, 3] The DCT block grid no longer aligns with the original embedding grid, so the embedded coefficients are spread across new blocks. Bit-error rates jump from <0.1% to 1-10% under typical resize ratios (50%-200%), depending on the resampling kernel.

4. **Crop attacks are similar to resize: they shift the 8×8 block grid relative to the watermark embedding grid.** [3] Even a 1-pixel crop offset can substantially destroy a non-resynchronized DCT watermark. Crop-robust schemes use *synchronization templates* (a known reference pattern embedded alongside the watermark) so the decoder can re-align the grid; this adds complexity and reduces capacity.

5. **Combined attacks (JPEG + resize + crop, in that order) are the realistic threat model for social media uploads.** Published BER under combined attacks varies widely; the conservative published numbers are in the 1-10% BER range for well-engineered schemes, with some schemes failing entirely under aggressive combinations.

6. **Hybrid DWT-DCT-SVD schemes** [4, 5] (wavelet decomposition + DCT in subbands + singular-value perturbation) achieve substantially better robustness than pure DCT against geometric attacks, at the cost of higher implementation complexity and more invasive perceptual changes.

7. **Deep-learning watermarking** (mixed-frequency channel attention, learned encoder-decoder pairs) [6] achieves the best published robustness numbers but is incompatible with the spec's "boring tech / no ML in the kernel" rule and adds enormous dependency surface.

8. **Sufficient lossy compression, large crops, or substantial resizes WILL destroy a DCT watermark.** [3] This is acknowledged in the literature; no scheme survives every attack. The watermark is a *probabilistic* provenance signal, not a guarantee.

## Risks identified

- **Overconfidence in the watermark's robustness** is the spec's biggest risk here. Users will assume "if the watermark is missing, the image is not from Paradigm," which is false in the presence of moderate post-processing.
- **Synchronization template overhead** can push perceptual quality below the spec's PSNR floor if the payload is too large.
- **Repeated re-encoding** (Paradigm export → Twitter → screenshot → Reddit re-upload → Discord re-encode) compounds attacks. The realistic survival rate after 3-4 re-encodes is much lower than after 1.
- **Mobile screenshot attacks** are a separate adversary class — they involve display resampling, possible cropping by the screenshot tool, and re-encoding by the OS. DCT watermarks survive mobile screenshots with substantially degraded reliability.
- **Adversarial removal attacks** (deliberate watermark stripping by an attacker who knows the scheme) are out of scope for invisible-watermark v1 and should be flagged as such.

## Recommendation

**Adopt a mid-frequency DCT watermark with explicit, honest robustness claims:**

1. **Embedding band: zigzag positions 6 through 21 of each 8×8 luma block.** This is the standard mid-frequency band that survives JPEG and is below the perceptual threshold.
2. **Payload: 64 bits, error-corrected with a (127, 64, 10) BCH code or similar** — yielding ~64 bits of usable payload from ~127 embedded bits, with error correction up to ~5 bit errors. This is enough for a 64-bit content hash pointer and tolerates the published BER under JPEG attacks.
3. **Embed a synchronization template** (small, fixed reference pattern in the corners of the image) so the decoder can resynchronize after small crops. Template overhead is bounded at ≤ 5% of the perceptual budget.
4. **PSNR floor: 40 dB** for the watermarked image relative to the unwatermarked image. Below this, the watermark is rejected and the export fails or falls back to a louder watermark with explicit user opt-in.
5. **Document the explicit robustness envelope in the spec, with numbers, not adjectives:**
   - JPEG Q ≥ 50: ≥ 99% bit recovery (after BCH)
   - JPEG Q 30-49: 90-99% bit recovery
   - JPEG Q < 30: not guaranteed
   - Resize ratio 0.75x-1.5x with synchronization template: 90-99% bit recovery
   - Resize ratio outside 0.5x-2.0x: not guaranteed
   - Crop ≤ 5% of any edge: 90-99% bit recovery (with template)
   - Combined JPEG + resize + small crop: 85-95% bit recovery
   - Mobile screenshot: ~80% bit recovery, scheme-dependent
   - 2+ rounds of re-encoding: not guaranteed
6. **Be explicit in the spec that the watermark is a probabilistic provenance signal, not a guarantee.** The C2PA manifest is the authoritative provenance bearer; the watermark is a fallback for when the manifest is stripped.
7. **Adversarial removal attacks are out of scope for v1.** Document this and reserve a `compliance/watermark-adversarial.md` slot for a future brief.
8. **Defer hybrid DWT-DCT-SVD and ML watermarking to v2** unless the v1 numbers prove insufficient in real-world testing.

## Confidence
**3/5.** The published literature is mature and the robustness envelope above is consistent across multiple sources. The 3/5 reflects two real uncertainties: (a) Phase 1 must measure the actual BER on Paradigm-typical content using the Paradigm encoder, not just trust academic numbers from arbitrary test images; and (b) the synchronization-template overhead might force adjusting the payload size or the BCH parameters once we measure the perceptual budget on representative content.

## Spec impact

- **`compliance/watermark-image.md` — REWRITE** to specify the mid-frequency DCT band, the BCH payload, the synchronization template, the PSNR floor, and the explicit robustness envelope table.
- **`compliance/watermark-image.md`** — add the explicit "probabilistic, not a guarantee" disclaimer.
- **`runtime/export-pipeline.md`** — add the watermark step with its perceptual-quality and latency budget.
- **`compliance/watermark-adversarial.md`** — new placeholder file noting v2 scope.
- New ADR: **`adr/00NN-image-watermark-scheme.md`** — record the DCT + BCH + synchronization template choice.

## Open follow-ups

- Build a Phase 1 robustness test harness: a Paradigm-encoded test set, a corpus of attacks (JPEG at multiple Q levels, resize at multiple ratios, crop offsets, combined attacks, simulated mobile screenshot), and a BER measurement script. Phase 1 task.
- Audit existing Rust DCT/wavelet libraries (`rustdct`, `image`, `imageproc`) for fitness to embed the watermark or whether to write the embedder in-tree.
- Decide whether the spec wants per-asset payload variation or a single fixed-payload scheme.
- Reserve a v2 brief for adversarial-removal robustness.

## Sources

1. A Hybrid Robust Image Watermarking Method Based on DWT-DCT and SIFT for Copyright Protection. https://pmc.ncbi.nlm.nih.gov/articles/PMC8539292/
2. A DCT-based Robust Watermarking Scheme. https://bit.kuas.edu.tw/~jni/2018/vol3/JNI_2018_03-v3n4-0049.pdf
3. Improving the robustness of DCT-based image watermarking against JPEG compression. https://www.researchgate.net/publication/222642137
4. Robust Image Watermarking Based on Hybrid IWT-DCT-SVD. https://www.journal.cendekiajournal.com/ijaci/article/download/17/9
5. An Improved DCT based Image Watermarking Robust Against JPEG Compression and Other Attacks. https://www.academia.edu/59886273/
6. Deep Image Watermarking to JPEG Compression Based on Mixed-Frequency Channel Attention. https://pmc.ncbi.nlm.nih.gov/articles/PMC9303108/
