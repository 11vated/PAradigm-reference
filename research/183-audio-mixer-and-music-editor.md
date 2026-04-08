# 183 — Audio mixer and music editor

## Question
What is the creator-facing editor surface that authors `audio.mixer`, `audio.bus`, `audio.pattern.*` (Brief 175) and `audio.clip` gseeds with bus routing, real-time preview, dynamic music graph editing, and ducking rule authoring?

## Why it matters (blast radius)
Audio mixing is the highest-bandwidth creator surface where preview must equal runtime — the human ear catches sub-100ms differences. If the editor doesn't bind to the runtime mixer (Brief 163), creators tune in the editor and ship something different. If LUFS analysis isn't sign-time, creators ship hot-mastered audio that violates the substrate-level loudness gate.

## What we know from the spec
- Brief 163 — audio runtime namespace (mixing, busses, 3D positional, ducking, dynamic music).
- Brief 175 — sound design and music pattern library (6 audio.pattern families, EBU R128 -14 LUFS default, beat-callback primitive).
- Brief 152 — fixed-tick scheduler for beat callbacks.
- Brief 086C — music and audio measured library.
- Brief 050 — accessibility (subtitle and ducking-on-voice substrate-level defaults).
- Brief 177 — modifier-surface contract.

## Findings
1. **Mixer view = bus tree + module rack + meter strip.** The editor renders the `audio.mixer` gseed as a tree of `audio.bus` nodes. Each bus has a meter strip, gain fader, mute/solo, send slots, and an effect rack (typed module list: EQ / compressor / limiter / reverb / delay / filter / convolution / sidechain). All values commit as signed mutations on slider release (mouse-up batching from Brief 177).
2. **Routing as typed graph.** Bus routing is a typed DAG. Sign-time validation rejects cycles. Sends are typed edges with gain coefficients. Default routing matches Brief 163's substrate template: master ← music ← (layered_music_layers); master ← sfx ← (sfx_subgroups); master ← voice; master ← ambience.
3. **Real-time preview = runtime mixer.** The editor instantiates the runtime mixer in-process and routes the editor's audio output through it. There is no separate "editor approximation" — preview is runtime. Bus changes apply on the next tick boundary (Brief 152 fixed tick) without needing an editor restart.
4. **Music editor = horizontal timeline + vertical layer rack.** The dynamic music editor renders a `audio.pattern.layered_music` gseed as horizontal segments (intro / loop / outro / transition) with stacked layers (drums / bass / harmony / lead / atmosphere). Crossfades and stinger triggers are typed transitions between segments.
5. **Beat callback authoring.** Brief 175's beat callback primitive is exposed as a typed `audio.beat_event` keyframe on the music timeline, bound to a downstream typed action (e.g., trigger VFX, advance state machine, emit lineage event). This is the audio equivalent of Brief 179's animation event channel.
6. **Vertical and horizontal remixing.** Vertical remixing (layer add/remove on game state) is authored as typed predicates per layer ("active when player.in_combat == true"). Horizontal remixing (segment switching) is a typed FSM (Brief 159) over segments with predicate transitions. Both bind to the same expression DSL as Brief 180.
7. **Ducking rules.** Brief 175's substrate-default voice ducking is exposed as typed `audio.ducking_rule` gseeds: source bus, target bus, attenuation in dB, attack/release in ms, hold time. Multiple rules compose; sign-time validation rejects conflicting rules (e.g., two rules ducking the same target by mutually exclusive amounts).
8. **Sign-time LUFS analysis.** Per Brief 175, every clip and every bus signed at commit runs an EBU R128 LUFS analysis. The result is a typed `audio.loudness_metadata` field signed alongside the clip. Sign-time validator rejects clips/busses exceeding the master target (default -14 LUFS integrated, configurable per project). The editor surfaces the loudness number live in the meter strip during preview.
9. **Clip import.** Audio clips import via Brief 089 universal pipeline. The editor's "import audio" button compiles to a typed `audio.clip.import` mutation. Supported formats per Brief 219 (forthcoming): WAV, OGG, FLAC, MP3, OPUS. Output is a signed `audio.clip` gseed with format, sample rate, channel count, and LUFS metadata.
10. **3D positional audio.** Spatial audio settings (attenuation curve, doppler, spread, occlusion) are typed per-source overrides on the bus or per-instance at runtime. The editor exposes them as a typed control panel; v0.2 ships HRTF simulation (deferred from v0.1 because Brief 163 is v0.2-default).
11. **Subtitles and accessibility.** Per Brief 050 and Brief 175, every voice clip can carry a typed `localization.string_ref` for subtitle text. The editor surfaces missing-subtitle warnings as a sign-time check.
12. **Effect rack module library.** v0.1 ships eight effect modules: parametric EQ, RMS compressor, brick-wall limiter, FDN reverb, BBD delay, biquad filter, convolution reverb, sidechain compressor. All implemented over Brief 026 deterministic kernel for replay determinism.

## Risks identified
- **Real-time preview latency.** Audio in editor must be < 20ms latency or creators perceive lag. Mitigation: use the runtime mixer's lowest-latency callback path; document target hardware.
- **LUFS analysis cost on commit.** Re-analyzing every long clip on every edit is expensive. Mitigation: LUFS metadata is cached on the clip gseed; re-analysis only triggers on clip-content change, not on bus routing change.
- **Effect determinism across builds.** Floating-point math in DSP can drift. Mitigation: all effects use Brief 026's deterministic kernel; measured drift bounded per Brief 001.
- **Crossfade timing precision.** Sample-accurate crossfades require sub-tick scheduling. Mitigation: Brief 152's tick scheduler exposes a sub-tick audio scheduler at sample granularity, used only by the audio runtime.
- **HRTF cost.** Per-source HRTF on dozens of sources is expensive. Mitigation: HRTF is opt-in per bus, limited at v0.2 to a configurable max-active-source count.

## Recommendation
Specify the audio editor as a bus-tree + effect-rack + music-timeline surface with real-time preview that *is* the runtime mixer. Ship 8 effect modules at v0.1 over Brief 026's deterministic kernel. Enforce sign-time LUFS analysis with caching. Defer HRTF to v0.2 with the rest of the audio runtime per Brief 163.

## Confidence
**4.5 / 5.** Audio mixer editing has heavy precedent (Wwise, FMOD Studio, Reaper, Unity Audio Mixer, Unreal MetaSounds). The novelty is the runtime-equals-preview binding, the lineage-signed mutation contract, the sign-time LUFS gate, and the typed ducking-rule composition. Lower than 5 because real-time preview latency on commodity hardware is empirical.

## Spec impact
- New spec section: **Audio mixer and music editor surface specification**.
- Adds the eight v0.1 effect module typed primitives.
- Adds `audio.loudness_metadata` typed field and the LUFS gate contract.
- Adds `audio.ducking_rule` typed primitive.
- Adds `audio.beat_event` keyframe on music timelines.
- Cross-references Briefs 152, 163, 175, 050.

## New inventions
- **INV-749** — Bus-tree + effect-rack + music-timeline unified audio editor: one surface for static mixing and dynamic music, both committing as typed mutations.
- **INV-750** — Runtime-equals-preview audio binding via in-process mixer instantiation: the editor's audio output goes through the runtime mixer, eliminating preview/runtime divergence.
- **INV-751** — Cached sign-time LUFS analysis with content-hash invalidation: loudness analysis runs on clip-content change only, not on every commit, while still enforcing the master loudness gate.
- **INV-752** — Typed ducking rule composition with sign-time conflict detection: multiple ducking rules compose; conflicts produce typed errors at sign time.
- **INV-753** — Eight v0.1 deterministic effect modules over Brief 026 kernel: parametric EQ, RMS compressor, brick-wall limiter, FDN reverb, BBD delay, biquad filter, convolution reverb, sidechain compressor — all replay-deterministic by construction.

## Open follow-ups
- HRTF spatial audio runtime (deferred to v0.2 with Brief 163).
- MIDI input for music authoring (deferred to v0.2).
- DAW interop (Reaper, Logic, FL Studio) — deferred to v0.3.
- Adaptive music ML (mood-driven generative scoring) — deferred to v0.5 with Brief 130 neurosymbolic surfaces.
- Multi-creator simultaneous mixing (deferred to v0.3).

## Sources
1. Brief 001 — GPU determinism (audio CPU determinism analog).
2. Brief 026 — Deterministic kernel implementation.
3. Brief 050 — Accessibility and i18n.
4. Brief 086C — Music and audio measured library.
5. Brief 089 — Universal anything-to-gseed pipeline.
6. Brief 152 — Game loop and tick model.
7. Brief 159 — State machines.
8. Brief 163 — Audio runtime namespace.
9. Brief 175 — Sound design and music pattern library.
10. Brief 177 — Scene editor modifier surface.
11. Wwise documentation (audiokinetic.com).
12. FMOD Studio documentation.
13. EBU R128 loudness recommendation.
