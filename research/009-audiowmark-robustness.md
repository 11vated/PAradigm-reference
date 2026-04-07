# 009 — audiowmark robustness and licensing

## Question
Is `audiowmark` (Stefan Westerfeld's open-source audio watermarking library) suitable as the Paradigm audio watermark, what robustness can it provide for the spec's compression scenarios, and what licensing constraints does it impose?

## Why it matters (blast radius)
Every Paradigm export of audio (music, voice, sound design) needs a perceptually invisible watermark that survives common audio re-encodes (MP3, AAC, Ogg) so that the provenance signal persists when the C2PA manifest is stripped. If `audiowmark` is unsuitable on robustness, performance, or licensing grounds, the spec must either implement audio watermarking from scratch (large project) or drop the audio modality at v1. This brief gates `compliance/watermark-audio.md`.

## What we know from the spec
- `compliance/watermark-audio.md` mandates an audio watermark on every exported audio asset.
- The spec assumes the watermark survives MP3/AAC/Ogg at typical streaming bitrates (≥128 kbps).
- The spec assumes the watermark payload is ~64-128 bits.

## Findings

1. **`audiowmark` is mature, actively maintained open-source software (github.com/swesterfeld/audiowmark) and the de-facto open-source audio watermarking reference.** [1, 2] It implements a spread-spectrum watermark using a patchwork algorithm in the audio spectrum.

2. **License: GPLv3 or later.** [1, 2] **This is the critical finding.** GPLv3 is a copyleft license that is incompatible with the Apache-2.0 spec license if `audiowmark` is linked into the Paradigm engine binary as a library. Use as a separate process (called via subprocess, with audio files crossing the process boundary) is the established workaround for combining GPL tools with non-GPL applications, but it constrains the integration architecture.

3. **Payload: 128-bit message embedded in the audio spectrum.** [1] This comfortably covers the spec's 64-128 bit budget.

4. **Robustness to lossy compression: documented to survive MP3 and Ogg encoding at 128 kbps or higher with the default watermark strength.** [1] At lower bitrates (e.g., 64 kbps) or after multiple re-encoding cycles, a higher watermark strength (e.g., strength 15 instead of the default) is required, at the cost of audibility.

5. **AAC support is not explicitly named in the README** but the patchwork-spectrum approach is codec-agnostic in principle; survival rates against AAC at typical bitrates are likely comparable to MP3 but require empirical confirmation.

6. **The strength/audibility tradeoff is exposed as a tunable parameter.** [1] This is a feature, not a bug — Paradigm can pick a strength based on the per-asset perceptual budget and the desired robustness profile.

7. **Other audio watermarking options surveyed:**
   - **Patchwork-Audio-Watermarking** [3]: an academic / educational implementation, not production-ready.
   - **Deep-learning audio watermarking** [4, 5]: best published robustness but introduces ML model dependencies, GPU requirements, and proprietary training data — incompatible with the spec's boring-tech rule.
   - **Commercial audio watermarking SDKs** (Verance, Civolution, etc.): proprietary, expensive, and add a vendor relationship to the critical path. Out of scope for v1.
   - **Roll our own**: spread-spectrum or echo-hiding implementations are documented in the literature, but writing one from scratch and validating its robustness is a multi-month project that is not on the critical path for a solo founder.

8. **AudioMarkBench** [6] is an academic benchmark that measures audio watermark robustness against a standard attack suite. `audiowmark` is included; the benchmark provides comparative numbers that the spec can reference.

## Risks identified

- **GPLv3 incompatibility with Apache-2.0** is the dominant risk. Linking `audiowmark` into the engine binary would force the entire Paradigm engine to be GPLv3, which conflicts with the spec license and the boring-tech ADR. The subprocess workaround is well-established but adds operational complexity (process spawning, audio file IPC, error handling across the process boundary).
- **No published numbers for AAC survival at 64 kbps or below.** Phase 1 must measure.
- **Multi-stage re-encoding** (Paradigm → MP3 → YouTube AAC → mobile playback) compounds attacks; default strength may be insufficient.
- **The library is maintained by a single developer.** Bus factor risk. The license at least permits forking.
- **No Rust binding.** Calling `audiowmark` from Rust requires either subprocess invocation, an FFI binding to a C++ library (which is what `audiowmark` is), or a from-scratch reimplementation of the algorithm in Rust.

## Recommendation

**Adopt `audiowmark` for v1 with the subprocess integration model:**

1. **Integration model: subprocess.** The Paradigm engine spawns `audiowmark` as a child process for embedding and extraction. Audio buffers cross the process boundary as WAV files in a working directory or via pipes. This sidesteps the GPLv3-vs-Apache-2.0 license incompatibility.
2. **Document the GPLv3 status of `audiowmark` in `infrastructure/library-canon.md`** with the explicit note that it is invoked as a separate process and not linked into the engine binary, so the GPL does not propagate.
3. **Default watermark strength: the library default**, with a `--robust` mode that uses strength 15 for assets that need to survive multi-stage re-encoding or low-bitrate compression.
4. **Payload: 128 bits**, identical structure to the image watermark from Brief 008 — a content-hash pointer plus a per-export nonce.
5. **Document the robustness envelope explicitly:**
   - MP3/Ogg ≥ 128 kbps single encode: ≥ 99% recovery (default strength)
   - MP3/Ogg 64-127 kbps single encode: 90-99% recovery (`--robust`)
   - MP3/Ogg < 64 kbps: not guaranteed
   - AAC ≥ 128 kbps: provisionally ≥ 95% recovery, pending Phase 1 measurement
   - 2+ rounds of lossy re-encoding at default strength: not guaranteed
   - 2+ rounds at `--robust` strength: 80-95% recovery, scenario-dependent
6. **Phase 1 task: build an audio watermark robustness benchmark** with a representative corpus and the same standard attacks (MP3/AAC/Ogg at multiple bitrates, multi-stage re-encoding, resampling, light noise addition).
7. **Reserve a v2 brief for a Rust-native audio watermark** (either an FFI binding to `audiowmark`, an in-tree reimplementation, or a deep-learning replacement), to be revisited if the subprocess model becomes a bottleneck.
8. **Adversarial removal attacks are out of scope for v1**, identical posture to the image watermark.

## Confidence
**4/5.** `audiowmark` is real, mature, and the only credible open-source option. The robustness numbers above are consistent with the README and AudioMarkBench. The 4/5 (rather than 5/5) reflects the AAC measurement gap and the unverified multi-stage re-encoding numbers.

## Spec impact

- **`compliance/watermark-audio.md` — REWRITE** to specify `audiowmark`, the subprocess integration model, the strength default and `--robust` flag, the 128-bit payload structure, and the explicit robustness envelope.
- **`compliance/watermark-audio.md`** — add the explicit "probabilistic, not a guarantee" disclaimer (mirroring Brief 008).
- **`infrastructure/library-canon.md`** — list `audiowmark` with its GPLv3 status and the subprocess-only constraint.
- **`runtime/export-pipeline.md`** — add the audio watermark step with the subprocess invocation rules and a latency budget marked provisional pending Phase 1 measurement.
- New ADR: **`adr/00NN-audiowmark-via-subprocess.md`** — record the GPL-via-subprocess decision and the rationale.

## Open follow-ups

- Build the audio watermark robustness benchmark. Phase 1 task.
- Measure subprocess invocation overhead vs in-process call overhead — if the export latency budget is tight, the subprocess model might be the bottleneck.
- Track AudioMarkBench updates.
- Reserve a v2 evaluation of FFI-bound or in-tree audio watermark replacements.
- Decide whether the Paradigm distribution bundles a prebuilt `audiowmark` binary or expects users to install it separately.

## Sources

1. audiowmark on GitHub. https://github.com/swesterfeld/audiowmark
2. audiowmark project page on uplex.de. https://uplex.de/audiowmark/
3. Patchwork-Audio-Watermarking (academic). https://github.com/thnagahawaththa/Patchwork-Audio-Watermarking
4. Audio Compression Impact on Neural Watermarks. https://www.scoredetect.com/blog/posts/audio-compression-impact-neural-watermarks
5. Deep Learning Audio Watermarking Key Metrics. https://www.scoredetect.com/blog/posts/deep-learning-audio-watermarking-key-metrics
6. AudioMarkBench: Benchmarking Robustness of Audio Watermarking. https://arxiv.org/html/2406.06979v1
7. An Audio Watermark Designed for Efficient and Robust Synchronization (Nadeau & Sharma, TIFS 2017). https://hajim.rochester.edu/ece/sites/gsharma/papers/NadeauAnalogPlaybkAudioWMSynchTIFS2017.pdf
