# 086C — Music theory, audio, and acoustics library

## Question
What music, audio, and acoustic data — instruments, scales, modes, rhythms, timbres, sound effects, environmental audio — must GSPL ship at v1 so that any sound a creator invokes is grounded in measured acoustics and culturally-accurate music theory?

## Why it matters
Half of "feeling like reality" is sound. A campfire crackles. A sword sings as it cuts. A dragon's roar shakes the ribcage. A character speaks in a voice that fits her face. A scene's emotional tone is set by an underscore that follows the laws of harmony. If GSPL ships the visual world without the auditory world, half of every scene is missing. If it ships **measured instrument samples, full music theory, environmental acoustics, and synthesis primitives** as signed substrate gseeds, sound becomes a first-class creative material.

## What we know from the spec
- Brief 082: physics (acoustics, wave equation).
- Brief 083: materials (acoustic absorption coefficients).
- Brief 084: particles (combustion sound coupling).
- Brief 085: biology (vocal tract anatomy).

## Findings — what GSPL ships at v1

### 1. Music theory primitives
- **Pitch systems:** 12-TET, just intonation, Pythagorean, meantone, well-temperament, microtonal (24-TET, 31-TET, Bohlen-Pierce), Indian classical (22 śruti), Arabic maqam (24 quarter-tones), gamelan slendro/pelog, Chinese pentatonic 五声.
- **Scales and modes:** all church modes (Ionian → Locrian), melodic and harmonic minor variants, jazz modes, blues, pentatonic, hexatonic, octatonic, whole tone, chromatic, exotic (Hijaz, Phrygian dominant, Hungarian minor, Iwato, Ryūkyū, etc.) — total 100+ named scales.
- **Chord theory:** triads, sevenths, extensions, alterations, polychords, slash chords, voicings (close, drop-2, drop-3, spread).
- **Rhythm:** meter (simple, compound, complex, additive, polyrhythm, polymeter), groove templates (swing, shuffle, clave 2-3/3-2, son, bossa, samba, reggae, dembow, amapiano, hip-hop pocket, drum-and-bass, garage).
- **Form:** sonata, rondo, AABA, 12-bar blues, verse-chorus, through-composed, theme and variations.
- **Counterpoint and voice leading rules.**
- **Harmonic function** (tonic/subdominant/dominant, modal interchange, secondary dominants, Neapolitan, augmented sixth chords).

**Source:** Hindemith, Schoenberg, Persichetti, Rameau (public domain), MuseScore, Hooktheory open data.

### 2. Instrument library — measured samples
- **Western orchestral:** strings (violin, viola, cello, bass), woodwinds (flute, piccolo, oboe, English horn, clarinet, bass clarinet, bassoon, contrabassoon, saxophones), brass (horn, trumpet, trombone, tuba), percussion (timpani, snare, bass drum, cymbals, tam-tam, glockenspiel, vibraphone, marimba, xylophone, celesta, tubular bells, harp, piano, harpsichord, organ).
- **World instruments:** sitar, tabla, tanpura, shakuhachi, koto, shamisen, guzheng, erhu, pipa, oud, qanun, ney, duduk, balalaika, accordion, bagpipes, mbira, kalimba, djembe, talking drum, didgeridoo, hang drum, taiko, gamelan ensemble, steel pan.
- **Modern/electronic:** electric guitar (clean/crunch/lead), bass, drum kit, synth (analog/FM/wavetable/granular), 808s, breakbeats, vocal chops.
- Each instrument shipped as **velocity-layered, round-robin, articulation-tagged sample sets** at 24-bit/96k, plus **physical model** alternative for differentiable use.

**Source:** Philharmonia Orchestra Sound Samples (open), University of Iowa Musical Instrument Samples, VSCO2 Community Edition, Sonatina Symphonic Orchestra, Salamander Grand Piano, Karoryfer.

### 3. Vocal and speech
- **Singing voice models** for soprano, mezzo, alto, tenor, baritone, bass.
- **Phoneme library** for major languages (consumes Brief 086D linguistics).
- **Vocal tract physical model** (Pink Trombone-grade) for synthesis.
- **Choir samples** and stack synthesis.
- **Speech synthesis primitives** for placeholder VO during preview (real VO via Brief 091 federation TTS).

### 4. Environmental and effect sounds (SFX library)
- **Foley:** footsteps on 30 surface materials (consumes Brief 083), cloth movement, object handling.
- **Ambiences:** forest (temperate/tropical/boreal), savanna, jungle, ocean (calm/storm/under), urban (city/suburb/industrial), interior (room tone, HVAC), wind (light/strong/howling), rain (drizzle/heavy/storm), fire (campfire/inferno/crackling).
- **Mechanical:** doors, latches, machinery, vehicles (cars, trains, planes, ships).
- **Combat:** swords, guns (period-accurate from flintlock to modern), explosions, impacts.
- **Creature vocalizations** for top 50 species (links to Brief 085 biology).
- **Magical/sci-fi templates** built on synth primitives.

**Source:** BBC Sound Effects (open library, ~33,000 sounds), freesound.org curated subset, Sonniss GameAudioGDC packs, Soundly free tier.

### 5. Acoustics and room simulation
- **Reverb impulse responses** for 200+ canonical spaces (cathedrals, concert halls, recording studios, theatres, caves, forests, parking garages, stairwells, bathrooms, bedrooms, opera houses).
- **Convolution and algorithmic reverb** primitives.
- **Geometric acoustics solver** (image source, ray tracing for sound) consuming material acoustic coefficients (Brief 083) — sound reflection emerges from physics.
- **HRTF database** (CIPIC, ARI, KEMAR) for binaural rendering.
- **Ambisonics** (1st through 7th order) for spatial audio.
- **Doppler, occlusion, diffraction, distance attenuation** as substrate primitives.

**Source:** OpenAIR Reverb Library, EchoThief impulse response database, CIPIC HRTF, ARI HRTF, IEM Plug-in Suite reference.

### 6. Audio DSP primitives
- **Filters:** low/high/band pass, shelf, parametric EQ, comb, all-pass.
- **Dynamics:** compressor, limiter, gate, expander, transient shaper.
- **Time/pitch:** time stretch (PSOLA, phase vocoder), pitch shift, formant shift.
- **Saturation/distortion:** tube, tape, transistor, bit crusher, wave folder.
- **Modulation:** chorus, flanger, phaser, tremolo, ring modulation.
- **Spectral:** STFT, mel, MFCC, CQT, chromagram, spectral gate.
- **Synthesis:** subtractive, FM, AM, additive, wavetable, granular, physical modeling (Karplus-Strong, waveguide), spectral.

### 7. Music generation and analysis
- **Melodic templates** (motifs, phrases, period structures).
- **Harmonic progressions** library (canonical I-V-vi-IV, ii-V-I, modal vamps, Coltrane changes, etc.).
- **Rhythm patterns** by genre.
- **Audio analysis:** beat tracking, key detection, chord recognition, tempo/meter inference.
- **MIDI and DAW interop** primitives.

## Findings — audio gseed structure

```
audio://instrument/violin/forte-staccato@v1.0
audio://scale/dorian/c@v1.0
audio://chord/maj7@v1.0
audio://groove/clave-2-3@v1.0
audio://reverb/notre-dame@v1.0
audio://ambience/temperate-forest-dawn@v1.0
audio://hrtf/CIPIC/subject-003@v1.0
audio://synth/wavetable/saw-stack@v1.0
```

A "campfire on a beach at night" composes ambience://beach-night, foley://campfire, particle audio coupling from Brief 084's combustion fire, and reverb computed from the open beach geometry — all coherent and signed.

## Inventions

### INV-328: Coherent visual+audio material binding
Material gseeds (Brief 083) carry both optical and acoustic properties. The substrate guarantees that the same wood-floor material reflects light at GGX(α=0.2) and reflects sound at NRC=0.10 simultaneously, with no possibility of drift. Novel because no creative tool binds visual and acoustic material identity at substrate level.

### INV-329: Geometric-acoustic rendering from scene geometry
The same scene geometry that drives the visual renderer drives a geometric acoustic solver (image source + ray tracing) consuming material acoustic coefficients. Reverb emerges from physics, not from a preset. Novel as a substrate-level coupled visual-acoustic renderer.

## Phase 1 deliverables

- **Music theory primitives** (scales, chords, rhythms, forms) at v1.
- **30 Western orchestral + 30 world instruments** as sampled and physically-modeled gseeds at v1.
- **5,000 SFX** in the foundation library at v1.
- **200 reverb IRs** at v1.
- **Geometric acoustic solver** wired to scene geometry at v1.
- **Full DSP primitive set** at v1.
- **HRTF + ambisonics** for spatial audio at v1.

## Risks

- **Sample library size.** Mitigation: lossless compression + lazy load from federation.
- **Sample licensing.** Mitigation: ship only CC0/CC-BY/permissive sources.
- **Real-time geometric acoustics on T1.** Mitigation: coarse mode for preview, full mode for render.

## Recommendation

1. **Lock the v1 sample library** to permissively-licensed sources only.
2. **Sign all gseeds** under GSPL Foundation Identity.
3. **Wire material acoustics** as a substrate contract (consumes INV-315).
4. **Engage Philharmonia, Iowa, VSCO2, BBC** as upstream partners.

## Confidence
**4.5/5.** Open audio ecosystem is mature.

## Spec impact

- `inventory/audio.md` — new doc.
- `inventory/music-theory.md` — new doc.
- New ADR: `adr/00NN-coupled-visual-acoustic-rendering.md`.

## Open follow-ups

- Sample library curation and licensing audit.
- Geometric acoustic solver performance benchmarks.
- World instrument coverage gap analysis.

## Sources

- Philharmonia Orchestra Sound Samples.
- University of Iowa Musical Instrument Samples.
- VSCO2 Community Edition.
- Sonatina Symphonic Orchestra.
- Salamander Grand Piano.
- BBC Sound Effects Archive.
- freesound.org.
- OpenAIR Reverb Library.
- EchoThief impulse response database.
- CIPIC HRTF, ARI HRTF.
- IEM Plug-in Suite.
- MuseScore, Hooktheory.
- *The Audio Programming Book* (Boulanger/Lazzarini).
- *Designing Sound* (Farnell).
- *The Theory and Technique of Electronic Music* (Puckette).
- Internal: Briefs 082, 083, 084, 085, 086D.
