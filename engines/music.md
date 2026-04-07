# Music Engine

## Overview

Generates a complete piece of music from genes describing scale, mode, tempo, instrumentation, mood, and structure. 3,381 LOC, 5 stages. Output is a synthesized WAV (via DSP), a MIDI file, and a structural manifest. Uses theory-driven harmonic progression and voice-leading rules rather than ML-based composition, which makes it deterministic and editable.

## Gene Schema

| Gene | Type | Range | Required | Description |
|---|---|---|---|---|
| `scale` | categorical | enum {ionian, dorian, phrygian, lydian, mixolydian, aeolian, locrian, harmonic_minor, melodic_minor, pentatonic, blues, chromatic, custom} | yes | Tonal scale |
| `key` | categorical | enum {C, C#, D, D#, E, F, F#, G, G#, A, A#, B} | yes | Tonic |
| `tempo` | scalar | [40, 240] BPM | yes | Beat tempo |
| `time_signature` | categorical | enum {3/4, 4/4, 5/4, 6/8, 7/8, 12/8} | yes | Meter |
| `instrument_set` | array<categorical> | from instrument library | yes | Voices |
| `mood` | vector(4) | each [0, 1] | yes | Energy, valence, tension, complexity |
| `genre` | categorical | enum {orchestral, rock, jazz, electronic, folk, ambient, hybrid} | yes | Style template |
| `structure` | categorical | enum {AABA, ABAB, verse_chorus, through_composed, theme_variations} | yes | Song form |
| `harmonic_density` | scalar | [0.1, 0.95] | yes | Chord complexity |
| `length_seconds` | scalar | [10, 600] | yes | Total length |

## Stage Pipeline

```
1. extract        : Seed                  -> MusicWorking
2. parameterize   : MusicWorking          -> KeySignature + StructureMap
3. morphogenesis  : KeySignature          -> HarmonicProgression
4. populate       : HarmonicProgression   -> MultiVoiceScore
5. render         : MultiVoiceScore       -> MusicArtifact
```

(The Music engine elides the `pose`/`compose` stages and combines them into `populate` and `render`. The 5-stage shape is unusual — see anti-patterns.)

## Stage Details

### Stage 2 — `parameterize`

Compute the key signature from `key` + `scale`, derive the song structure from `structure` + `length_seconds`, and assign chord-region durations.

### Stage 3 — `morphogenesis`

Generate the harmonic progression. For each chord region, choose chord roots and qualities consistent with the scale and the mood. Uses functional harmony rules: tonic → predominant → dominant → tonic, with substitutions weighted by `harmonic_density` and `genre`.

### Stage 4 — `populate`

Compose melodies for each instrument under voice-leading rules (no parallel fifths, smooth voice motion, consistent register). Each instrument is assigned a role (lead, harmony, bass, percussion) based on the instrument set and genre template.

### Stage 5 — `render`

Synthesize WAV via DSP (oscillators + envelopes + effects) and emit MIDI in parallel. The DSP path uses fixed-point arithmetic internally to avoid floating-point drift across machines.

## Render Hints

```ts
{ viewportMode: 'audio', supportsAnimation: false, thumbnailSize: { width: 512, height: 128 } }  // waveform thumb
```

## Export Hints

`['wav', 'mid', 'mp3', 'flac', 'ogg', 'json_score']`. Recommended: `wav` + `mid` together.

## Fitness Hints

Meaningful axes: animation (rhythmic motion), coherence, style, novelty.
Default MAP-Elites descriptors: `tempo`, `harmonic_density`.

## Determinism Notes

- DSP synthesis uses 32-bit fixed-point (Q15) internally; converted to PCM16 at the boundary.
- WAV byte output is canonicalized: header values fixed, no PAD chunks, no junk metadata.
- MIDI deltas are integer ticks at fixed PPQN.

## Validation Rules

- `length_seconds` ≥ 10.
- Instrument set non-empty.
- Tempo in [40, 240].
- All chord regions resolve to playable voicings under the chosen instrument set.

## Anti-Patterns

- **Don't add stages for "vocals" or "lyrics."** Use the `narrative_to_music` functor or compose with the Narrative engine separately.
- **Don't expose ML-trained models inside the engine.** Determinism would break.

## References

- Lerdahl & Jackendoff, *A Generative Theory of Tonal Music* (1983)
- Sound on Sound: voice-leading practical guides
- Music21 library (used as a reference for chord vocabulary)
