# 175 — Sound design and music pattern library

## Question

What canonical sound design and music patterns does GSPL ship in `audio.pattern.*` so that any genre can adopt stingers, layered tracks, vertical/horizontal remixing, Wwise/FMOD-class typed surfaces, voice barks, ambience beds, and music-driven gameplay by composition rather than from scratch, and how do they sit on top of Brief 163's audio runtime primitives?

## Why it matters (blast radius)

Audio is the most consistently underrated part of game design and the most frame-perfect-bug-prone subsystem after combat. Without typed audio patterns, every game reinvents music transitions, voice barks, ambience layering, and dynamic mixing, breaking cross-game tooling for localization, accessibility, and authoring. Brief 163 (audio runtime), Brief 167 (combat audio events), Brief 168 (enemy voice sets), Brief 171 (dialogue voice clips), Brief 174 (UI sound), Brief 183 (audio mixer editor), and Brief 220 (localized voice) all consume `audio.pattern.*`.

## What we know from the spec

- Brief 163 — audio runtime namespace; the substrate primitives this brief composes (clip / bus / source / mixer / music_graph)
- Brief 086C — music and audio measured-world library
- Brief 153 — ECS substrate; audio sources are typed components on entities
- Brief 097 — anti-hallucination test suite covering audio determinism
- Brief 220 — i18n; voice clips are locale-keyed
- Brief 149 — v0.1 frozen scope: audio runtime is v0.2-default with substrate hooks at v0.1

## Findings

1. **Six canonical pattern families.** Surveying *Game Audio Implementation* (Stevens & Raybould), Wwise/FMOD documentation, and shipped game audio postmortems (Hellblade, Doom Eternal, Hades, Hollow Knight, Stardew Valley, Outer Wilds) yields **6 canonical audio pattern families**: `audio.pattern.stinger`, `audio.pattern.ambience_bed`, `audio.pattern.voice_bark`, `audio.pattern.layered_music`, `audio.pattern.dynamic_mix`, `audio.pattern.event_signature`. Each is a typed signed gseed composing Brief 163 primitives.

2. **`audio.pattern.stinger`.** A short, signed audio cue tied to an event. Parameters: `stinger_id`, `clips: ordered_set<clip_ref>` (one per locale + variation), `trigger_event_kind: EventKindId`, `bus_ref: bus_ref` (Brief 163), `volume: f32`, `pitch_jitter: f32 ∈ [0.0, 0.25]`, `cooldown_ticks: u32`, `concurrency_cap: u8`, `priority: i8`. Substrate randomly selects a variation using sub-seeded PRNG (Brief 160) keyed on `(event_id, tick)`. Stingers fire on level-up, item pickup, achievement, hit confirm, etc.

3. **`audio.pattern.ambience_bed`.** Looping background ambience with layered variation. Parameters: `bed_id`, `base_layer: clip_ref`, `optional_layers: set<(clip_ref, gating_predicate, fade_in_ticks, fade_out_ticks)>`, `bus_ref`, `wind_modulation_ref: optional<lfo_ref>`, `random_one_shots: optional<one_shot_set>`, `time_of_day_modulation: optional<curve_ref>`. Beds compose 1-8 layers; gating predicates read ECS state (player position, weather, time of day) to fade layers in/out. Substrate enforces seamless looping.

4. **`audio.pattern.voice_bark`.** Short voiced reactions. Parameters: `bark_id`, `clip_set_per_locale: map<LocaleId, set<clip_ref>>`, `speaker_ref: speaker_ref` (Brief 171), `trigger_predicate`, `cooldown_ticks`, `priority`, `subtitle_text: LocalKey`. Barks are the most common combat audio (enemy yells, ally callouts) and the most localization-heavy. Substrate ships subtitle integration (Brief 050 accessibility) by default.

5. **`audio.pattern.layered_music`.** Vertical layering: stems that fade in/out based on game state. Parameters: `track_id`, `stems: ordered_set<(clip_ref, gating_predicate, base_volume)>`, `master_bus_ref`, `loop_points`, `tempo_bpm`, `time_signature`. Substrate uses Brief 163's music graph primitive; fades are quantized to beat boundaries when `quantize_to_beat: bool=true`.

6. **`audio.pattern.dynamic_mix`.** Horizontal remixing: switching between music sections based on game state. Parameters: `mix_id`, `sections: set<(section_id, clip_ref, transition_rules)>`, `current_section_predicate`, `transition_kind: enum{cut, crossfade, beat_quantized, bar_quantized, phrase_quantized, stinger_bridge}`. Used by Hades (Hadestown sections), Doom Eternal (combat layers), Outer Wilds (instrument-stacking).

7. **`audio.pattern.event_signature`.** A reusable group of audio events triggered together. Parameters: `signature_id`, `events: ordered_set<(event_kind, delay_ticks, randomization)>`, `cooldown`, `bus_routing`. Used for "explosion = boom + shockwave + debris + far_thunder + ringing" composition. Reduces creator-side reinvention.

8. **Music-as-gameplay primitive.** Rhythm games and music-reactive titles need beat callbacks. Substrate ships `audio.pattern.beat_callback`: `track_ref`, `subdivision: enum{whole, half, quarter, eighth, sixteenth, triplet}`, `callback_event: gseed_ref`. Beat callbacks fire on the fixed-tick scheduler (Brief 152), not the audio thread, so gameplay reactions are tick-deterministic. Brief 208 rhythm genre depends on this.

9. **Spatial audio patterns.** Brief 163 ships positional sources; this brief layers patterns: `audio.pattern.distance_falloff_curve` (linear/log/inverse-square presets), `audio.pattern.occlusion_model` (raycast-based / portal-based / disabled), `audio.pattern.directional_emit` (cone/spotlight). These are *patterns* not *primitives* — they parameterize how the runtime renders spatial sources.

10. **Loudness and mastering.** Substrate ships LUFS metering hooks per Brief 163's EBU R128 -14 LUFS target. `audio.pattern.master_chain` parameters: `chain_id`, `dynamic_range_compressor`, `limiter`, `lufs_target`, `peak_ceiling_dbfs`. Substrate enforces -14 LUFS by default; creators can override for genre conventions (e.g., -16 for narrative games, -10 for arcade).

11. **Voice routing.** Voice clips (dialogue, barks) automatically route to the `voice` bus from Brief 163's seven default buses. The voice bus has duck rules — when voice is active, music and SFX duck by default `-6 dB` over `100 ms`. Creator can adjust per-bus via `audio.pattern.duck_rule`.

12. **Audio accessibility.** Substrate supports: `audio.pattern.subtitle` for any voice/bark gseed, `audio.pattern.visualizer` for music-driven visual cues (deaf-accessible rhythm games), `audio.pattern.haptic_pairing` for controller rumble synced to audio events, `audio.pattern.mono_mix` flag for hearing-impaired stereo collapse.

13. **Localization rules.** Voice clips have a per-locale set; subtitle text is a LocalKey. Substrate refuses to sign a voiced gseed without at least source-locale clip and source-locale subtitle. Missing target-locale clips fall back to source with a runtime warning (or strict-locale error per Brief 220's enforcement mode).

14. **Replay determinism.** Audio events are signed and per-tick (Brief 163's documented sample-level non-determinism applies only to sub-tick precision). Replays produce identical event triggers; sample-exact playback may differ across hardware but the *gseed-level* event log is bit-identical.

15. **Performance budget.** Brief 163 caps active sources at 32; this brief's patterns must respect that cap via priority + voice stealing. `audio.pattern.priority_class` enum: `critical, high, normal, low, ambient`. Stealing always ejects lowest-priority oldest source first.

16. **v0.1 reach.** Per Brief 149, audio runtime is v0.2-default. The `audio.pattern.*` schemas all ship at v0.1 (so creators can author audio metadata into v0.1 projects); the runtime that *plays* them is gated to v0.2. Subtitles, beat callbacks, and accessibility features ship at v0.1 even without audio output, so deaf-accessible gameplay primitives are available from day one. Voice barks and dialogue voice integration ship runtime at v0.2.

## Risks identified

1. **Voice acting cost.** A creator wanting full voice across 10 locales for 10,000 lines is six-figure budget. Mitigation: substrate supports voice on a per-line opt-in; AI-synthesized voice is a v0.4+ option per Brief 092 character canon work.

2. **Music transition determinism with sample-precise quantization.** Different audio drivers have different latency. Mitigation: quantization happens at the gseed event level, not the sample level; per Brief 163, sub-tick precision is documented non-deterministic.

3. **Loudness wars in mod content.** Player-modded audio could blow out mixes. Mitigation: substrate runs LUFS analysis at sign time on creator audio gseeds; warnings emitted for tracks exceeding the project's LUFS target.

4. **Subtitle overflow in long localizations.** German subtitles 2× English don't fit the same UI. Mitigation: subtitle widget (Brief 174) defaults to multi-line + auto-shrink; sign-time warning past 4 lines.

5. **Bark spam in horde games.** 100 enemies all yelling. Mitigation: priority + cooldown + concurrency cap; substrate's bark priority system steals lowest-priority barks first.

6. **Beat callback latency.** A beat callback that fires on the next tick may lag the actual beat by up to one tick (16.67 ms at 60 Hz). Mitigation: callback dispatch uses lookahead — schedule the callback `lookahead_ticks` before the beat for sub-tick accuracy at dispatch time.

## Recommendation

Ship the 6-pattern `audio.pattern.*` library on top of Brief 163's audio runtime primitives. Schemas ship at v0.1; runtime gated to v0.2 per Brief 149. Subtitles, beat callbacks, and accessibility patterns ship runtime at v0.1 even without full audio output. Wire to Brief 174 UI subtitle widget, Brief 183 audio editor, Brief 171 dialogue speaker linkage, and Brief 167 combat event triggers from day one. Default to -14 LUFS mastering with creator override.

## Confidence

**4/5.** Audio patterns are well-grounded in Wwise/FMOD documentation, *Game Audio Implementation* textbook, and 30+ years of game audio postmortems. Held back from 5 by the v0.1-vs-v0.2 schema-without-runtime split, which is novel and may need adjustment after Brief 220 i18n integration testing.

## Spec impact

- Add `audio.pattern.*` namespace with 6 pattern primitives
- Add `audio.pattern.beat_callback`, `subtitle`, `visualizer`, `haptic_pairing`, `mono_mix`, `master_chain`, `duck_rule`, `priority_class`
- Cross-link to Brief 050 (a11y), Brief 086C (music library), Brief 097 (audio determinism), Brief 152 (tick scheduler), Brief 153 (ECS source components), Brief 160 (sub-seeded PRNG for variations), Brief 163 (runtime primitives), Brief 167 (combat trigger), Brief 168 (enemy voice sets), Brief 171 (dialogue speaker), Brief 174 (subtitle widget), Brief 183 (mixer editor), Brief 208 (rhythm genre), Brief 220 (i18n)
- Mark audio runtime gated to v0.2 per Brief 149; pattern *schemas* ship at v0.1

## New inventions

- **INV-710** Six-pattern canonical `audio.pattern.*` library composing Brief 163 runtime primitives
- **INV-711** Beat callback primitive scheduled on Brief 152's fixed-tick scheduler with lookahead for sub-tick accuracy at dispatch time
- **INV-712** Sign-time LUFS analysis as substrate-level loudness gate enforcing project mastering targets
- **INV-713** Schema-at-v0.1 / runtime-at-v0.2 split allowing creators to author audio metadata into v0.1 projects without runtime support
- **INV-714** Substrate-default voice ducking, subtitle integration, and haptic pairing as accessibility-first audio primitives

## Open follow-ups

- AI-synthesized voice integration (v0.4+, Brief 092 follow-up)
- Spatial audio HRTF presets per platform (Brief 219 asset import)
- Dolby Atmos / surround configuration (deferred to v0.5)
- Adaptive music ML hooks (Brief 228 emergent narrative follow-up)

## Sources

1. *Game Audio Implementation*, Stevens & Raybould, 2015
2. Wwise documentation — bus/event/state architecture
3. FMOD documentation — event/parameter/snapshot architecture
4. Hellblade: Senua's Sacrifice audio retrospective, Ninja Theory GDC 2018
5. Doom Eternal music & sound talk, id Software GDC 2020
6. Hades dynamic music talk, Supergiant GDC 2020
7. Outer Wilds music-as-gameplay talk, Mobius GDC 2019
8. EBU R128 specification — loudness measurement
9. Brief 050 (this repo) — accessibility
10. Brief 086C (this repo) — music & audio library
11. Brief 163 (this repo) — audio runtime namespace
12. Brief 220 (this repo, planned) — i18n / locale keys
