# 022 — Sound family: Music + Audio engines

## Question
What is the seed schema, kernel pipeline, and proof model for the two engines that produce audible output: MusicEngine (composed music) and AudioEngine (sound effects, ambience, voice processing)?

## Why it matters
Audio is the asset class with the *highest* perceptual sensitivity and the *weakest* tooling among GSPL's competitors. Stable Audio, MusicGen, Suno produce undifferentiated waveforms with no structural handles. GSPL's gene-based audio is a real differentiator: every musical decision, from key to envelope, is a typed handle the user can breed.

## What we know from the spec
- `engines/music.md`, `engines/audio.md` exist as stubs.
- WaveGene and EnvelopeGene (Brief 020) are the audio-friendly gene types.
- audiowmark (Brief 009) handles watermarking.

## Findings — schemas

### MusicEngine

The MusicEngine produces *score-level* music: structural compositions that are then synthesized. The engine separates composition (proof-bearing) from synthesis (perceptual layer).

**Genes (typical 30-60):**
- `key.tonic` (CategoricalGene over 12 pitch classes)
- `key.mode` (CategoricalGene: major, minor, dorian, phrygian, lydian, mixolydian, locrian, custom)
- `tempo.bpm` (ScalarGene)
- `tempo.envelope` (EnvelopeGene over song duration for tempo automation)
- `time_signature` (CategoricalGene: 4/4, 3/4, 6/8, 5/4, 7/8, custom-IntPair)
- `structure.form` (CategoricalGene: AABA, verse-chorus-bridge, through-composed, sonata, custom)
- `structure.section_lengths` (SequenceGene of bar counts)
- `harmony.chord_progression` (SequenceGene<CategoricalGene> of chord roots+qualities, per section)
- `harmony.voice_leading_strictness` (ScalarGene)
- `melody.contour` (CurveGene per section, mapping bar position → pitch class offset)
- `melody.rhythm_density` (ScalarGene per section)
- `instrumentation.ensemble` (SwarmGene over instrument families)
- `instrumentation.dynamics_envelope` (EnvelopeGene per instrument)
- `texture.density_envelope` (EnvelopeGene over song duration)
- `mood.embedding` (EmbeddingGene anchored to a music-mood model)
- Plus the 8 Core genes.

### AudioEngine

The AudioEngine handles non-music audio: SFX (one-shots), ambience (loops + drones), voice (synthesized or processed). It is more parameter-driven and less compositional than MusicEngine.

**Genes (typical 12-30 per asset class):**
- `category` (CategoricalGene: sfx, ambience, voice, foley, riser, impact, drone)
- `duration` (ScalarGene in seconds)
- `synth.method` (CategoricalGene: subtractive, fm, granular, sample, hybrid)
- `synth.params` (DistributionGene over the chosen method's parameter space)
- `envelope.amplitude` (EnvelopeGene; ADSR variant)
- `envelope.pitch` (EnvelopeGene)
- `envelope.filter_cutoff` (EnvelopeGene)
- `effects.chain` (SequenceGene of effect type + params)
- `voice.text` (TextGene, only for voice category)
- `voice.timbre.embedding` (EmbeddingGene, only for voice category)
- Plus the 8 Core genes.

## Pipeline architecture

Two-stage pipeline shared by both engines:

1. **Seed → Score IR**: deterministic. For Music, the IR is a typed score graph (notes, chords, expression marks). For Audio, the IR is a typed parameter envelope graph. The Score IR is what the content hash and signature cover.
2. **Score IR → Waveform**: deterministic-given-fixed-synth, but the synth implementation is allowed to be platform-specific. To preserve verifiability, GSPL ships a *reference synth* that produces a canonical reference waveform whose hash is recorded in the seed metadata. Other synths may produce perceptually-equivalent waveforms with different hashes; this is allowed but flagged.

The 2-stage split lets the proof system live on the Score IR (deterministic, portable) while letting the synthesis stage take advantage of any audio engine, plugin, or DAW.

## Cross-engine bindings

- `Audio ← Music`: an AudioEngine seed may consume a MusicEngine seed when, e.g., synthesizing one instrument stem. The binding flows through Core (mood, energy, complexity, density).
- `Audio ← Character`: voice synthesis binds to a CharacterEngine seed via `voice.timbre` and `voice.pitch_range` (Brief 021).
- `Music ← Narrative`: emotional pacing of a music score binds to a NarrativeEngine seed via the tension envelope (Brief 023).

## Watermarking

- WaveformOutput watermarks via audiowmark (Brief 009).
- The watermark payload includes the content hash of the Score IR (not the waveform), so verification is robust to re-synthesis.

## Risks identified

- **Reference synth quality vs portability**: a high-quality reference synth is heavyweight; a portable reference synth sounds sterile. Mitigation: ship a *Tier 1* portable reference synth for proof, plus *Tier 2* "preferred" synths that producers actually use, with cross-references in metadata.
- **Score IR for non-Western music**: 12-tone equal temperament is baked into the schema by default. Mitigation: `key.tuning_system` is itself a CategoricalGene with custom-microtonal as an option.
- **Voice synthesis legal exposure**: voice cloning has known legal and ethical risks. Mitigation: the engine refuses to bind to a voice embedding without an explicit consent flag in metadata; this is enforced by the validator (Brief 014 invariant 8 extension).
- **EnvelopeGene proliferation**: many envelopes per song = large seeds. Mitigation: hierarchical envelopes; default curves with override; per-instrument inheritance.

## Recommendation

1. **Adopt the two-engine schemas as drafted.**
2. **Score IR is normative and proof-bearing**, waveform is not.
3. **Reference synth is mandatory**, additional synths optional.
4. **Watermark payload references the Score IR hash**, not the waveform hash.
5. **Voice synthesis requires explicit consent flag** in metadata; validator rejects voice seeds without it.
6. **`key.tuning_system` defaults to 12-TET** but allows custom microtonal.
7. **Hierarchical envelopes** are mandatory in the schema, not optional.

## Confidence
**3/5.** Music and audio are mature in their respective fields, but the *typed-gene* approach to compositional music is novel and untested. The 3/5 reflects the gap between knowing the math and knowing whether musicians will accept it as expressive enough.

## Spec impact

- `engines/music.md`, `engines/audio.md` — full schemas.
- `algorithms/score-ir.md`, `audio-ir.md` — IR definitions.
- `algorithms/reference-synth.md` — Tier 1 reference synth specification.
- `tests/audio-conformance.md` — perceptual + structural tests.
- New ADR: `adr/00NN-score-ir-as-proof-domain.md`.

## Open follow-ups

- Build a Tier 1 reference synth as a Phase 1 task. Constraints: portable, deterministic, perceptually acceptable. Likely a small additive/subtractive hybrid.
- Decide on whether to ship a soundfont-based fallback for the reference synth.
- Empirically validate that NarrativeEngine → MusicEngine binding via Core feels musical, not arbitrary.
- Decide on consent-flag UX for voice synthesis (Phase 2 with the studio).

## Sources

- Music21 (computational musicology library) — gives confidence the score IR direction is well-trodden.
- Suno, MusicGen, Stable Audio whitepapers (the "no structural handles" baseline).
- audiowmark documentation (Brief 009).
- Internal: Brief 020 (EnvelopeGene, EmbeddingGene), Brief 009 (audio watermarking).
