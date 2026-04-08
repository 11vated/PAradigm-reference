# 163 — Audio runtime namespace

## Question

How does GSPL equip the runtime audio system — mixing, busses, 3D positional, ducking, dynamic music — as a typed substrate namespace where every sound, bus, and music transition is signed and rollback-able, and how does this reconcile with Brief 149's v0.2 scope cut for audio?

## Why it matters (blast radius)

Audio is the most-overlooked surface that has the largest emotional impact on the player. Bad audio kills game feel; good audio sells everything visual. Brief 149 cut the *creator-facing audio creation tools* (audio generation, voice synthesis) from v0.1 — but the runtime system that *plays* audio must ship at v0.1 because every starter-genre demo needs at least music + SFX. This brief specifies the runtime layer (which v0.1 ships) and reserves namespace slots for the v0.2 creation tools.

## What we know from the spec

- Round 4 Brief 086C — music and audio measured-world primitives.
- Brief 149 — v0.1 cuts audio *creation* (gen tools); audio *runtime* must ship.
- Brief 152 — fixed/variable tick split; audio reads `tick.real_delta` for wall-clock-locked playback (Brief 152 finding 8).
- Brief 153 — `audio.source` ECS component placeholder.
- Brief 131 — seven-axis claim; audio events are signed.

## Findings

1. **Runtime audio ships at v0.1; audio creation tools defer to v0.2.** This brief specifies the runtime: loading clips, playing them on busses, mixing, 3D positioning, ducking, dynamic music transitions, signed events. v0.2 adds: audio generation models, voice synthesis, music generation, mastering tools (Brief 175 covers their authoring surface).

2. **Five canonical primitives ship: clip, bus, source, mixer, music_graph.** A `audio.clip` is loaded sound data (signed gseed referencing a content file). A `audio.bus` is a mixing channel with volume, pitch, low/mid/high EQ, send-effects. A `audio.source` is an ECS component playing a clip on a bus from a position (or non-positional). A `audio.mixer` is the global signed routing graph. A `audio.music_graph` is the dynamic music state machine.

3. **Default bus layout ships per scene.** v0.1 starter-genre templates ship with: `master`, `music`, `sfx`, `ambience`, `ui`, `voice`, `dialogue`. Creators add buses as needed. The bus graph is a signed `audio.mixer` gseed.

4. **Audio runs on the wall-clock, not the fixed tick.** Per Brief 152 finding 8, audio is real-time: it doesn't pause when fixed-tick scaling slows down (slow-motion). Sources can opt into time-scale via a flag for hit-stop / freeze-frame effects. Audio events fire at sample-accurate timestamps and are signed at fixed-tick boundaries for replay matching.

5. **3D positional audio.** A `audio.source` with a position attribute attenuates by distance, pans by azimuth, applies low-pass filter for occlusion (queryable from physics). Listener is the active camera by default (Brief 155); creators can override via `audio.listener` ECS component.

6. **Ducking is a signed bus modifier.** When voice fires on the `voice` bus, the `music` and `ambience` buses duck by signed amounts. Duck rules are typed: `(trigger_bus, target_buses[], duck_db, attack_ms, release_ms)`. Ship-default ducking is wired into the v0.1 starter scenes.

7. **Dynamic music graph.** A signed `audio.music_graph` is a state machine of music sections (e.g., `exploration`, `combat`, `boss`, `ambient`). Transitions have signed `(from, to, conditions, beat_quantize, crossfade_ms)`. Beat-quantized transitions ensure musical phrases align even when the trigger fires mid-bar. This is the consensus Wwise/FMOD pattern.

8. **Vertical layering.** A music section has up to 8 stems (drums, bass, melody, harmony, percussion, lead, background, fx). Stems are independently muted/unmuted by gameplay state (e.g., add brass when player health drops). Each stem mute is a signed gseed event.

9. **Audio events are signed for replay.** When `play`, `stop`, `duck`, `transition`, or `volume_change` fires, a signed `audio.event` gseed records `(event_type, source_id, parameters, fixed_tick_number, sample_offset_in_tick)`. Replay re-fires the same events at the same offsets; same audio output every replay.

10. **Audio determinism caveats.** Per Brief 156-style honesty: bit-identical audio output across machines is not guaranteed because of audio driver buffer alignment, OS mixing, and hardware sample-rate variation. The substrate guarantees *event-level* determinism (same events fire at same logical times); the rendered samples may differ by buffer-alignment microseconds.

11. **Performance budget.** v0.1 budgets audio at 1ms variable on the hardware floor for: 32 simultaneous sources, 8 buses, 2 reverb sends, 1 active music_graph. Beyond, drift detector emits `audio.budget.breach`.

12. **Audio file format.** v0.1 supports OGG Vorbis (looping music), WAV (short SFX), and FLAC (lossless reference). Streaming for long music files (>30s) is automatic. Loaded clips are content-addressed and shared across sources.

13. **Loudness targets and integrated loudness measurement.** v0.1 ships an integrated-loudness measurement gseed (`audio.loudness.lufs`) per clip and a per-scene target loudness (default -14 LUFS for streaming-friendly builds). Clips outside ±2 LUFS of the target emit a signed warning. This is the BS.1770/EBU R128 standard, equipped as substrate so creators don't ship un-leveled audio.

14. **Voice and dialogue are runtime-supported, content-deferred.** The `voice` and `dialogue` buses exist; creators can ship pre-recorded voice files at v0.1 and they play on the right buses with ducking. Voice synthesis is v0.2.

## Risks identified

- **Audio bit-determinism is unachievable on consumer hardware.** Mitigation: substrate guarantees event-level determinism only; rendered audio is "close enough"; replay matches at the event layer; documented honestly per Brief 097 grounding floor.
- **Dynamic music transitions can sound jarring without beat quantization.** Mitigation: beat-quantize is on by default; creators opt-out per transition.
- **3D occlusion via physics raycast can be expensive at high source counts.** Mitigation: occlusion checks are throttled (every 4th tick by default); creators can override per source.
- **Audio file format choice locks creators into specific tooling.** Mitigation: import pipeline (Tier G Brief 219) accepts MP3/AAC/FLAC/WAV/OGG and normalizes to OGG/FLAC at import.
- **Loudness warnings can frustrate creators using existing assets.** Mitigation: warning, not block; per-scene override available.

## Recommendation

**GSPL ships an `audio` namespace at v0.1 with: five canonical primitives (clip / bus / source / mixer / music_graph), seven default buses (master / music / sfx / ambience / ui / voice / dialogue), wall-clock-driven playback with opt-in time-scale, 3D positional with physics-occlusion at throttled cadence, signed bus ducking with default voice→music wiring, dynamic music graph with beat-quantized transitions and 8-stem vertical layering, signed audio events for event-level replay determinism with documented sample-level non-determinism, OGG/WAV/FLAC support with auto-streaming for long clips, EBU R128 integrated loudness measurement and -14 LUFS default target with warnings, ~32 sources / 8 buses / 1 music graph capacity on the hardware floor, and namespace slots reserved for v0.2 audio creation tools.**

## Confidence

**4/5.** Bus + source + music_graph is the consensus Wwise/FMOD pattern. Beat-quantized transitions, vertical layering, and loudness targets are all standard practice. The only novel piece is signing audio events for replay; this is bounded by the event count, not the sample count, and fits in the budget.

## Spec impact

- `gspl-reference/namespaces/audio.md` — new namespace
- `gspl-reference/research/152-game-loop-tick-model-namespace.md` — wall-clock for audio, tick.real_delta usage
- `gspl-reference/research/153-ecs-substrate-binding.md` — `audio.source` and `audio.listener` components
- `gspl-reference/research/155-camera-namespace.md` — default audio listener attached to active camera
- `gspl-reference/research/086C-music-and-audio-primitives.md` — measured-world music primitives
- `gspl-reference/research/097-anti-hallucination-test-suite.md` — honesty about sample-level non-determinism
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — audio battery: 32 sources + 1 music_graph at 60Hz
- Tier B Brief 175 (sound design pattern library) — composes on this runtime
- Tier C Brief 183 (audio mixer editor) — visual editor reads/writes mixer gseeds
- Tier G Brief 219 (asset import pipeline) — audio format normalization
- v0.2 audio creation tools brief (out of Round 7 scope)

## New inventions

- **INV-650** — *Five-primitive audio runtime under one signed namespace* (clip/bus/source/mixer/music_graph) with seven default starter-genre buses and creator extensibility.
- **INV-651** — *Event-level replay determinism for audio* — signed audio events at fixed-tick boundaries with sample-offset annotations, replay-matching at the event layer while documenting honest sample-level divergence.
- **INV-652** — *Beat-quantized music transitions with 8-stem vertical layering* equipped as substrate primitive — creators describe musical state machines, the substrate handles the timing math.
- **INV-653** — *EBU R128 integrated loudness as a substrate metric* — clips outside ±2 LUFS of scene target emit signed warnings, eliminating an entire class of "shipped game has wildly inconsistent audio levels" creator failures.
- **INV-654** — *Throttled physics-occlusion for 3D positional audio* (every 4th tick default) — keeps audio in the budget at high source counts without losing the perceptual cue.

## Open follow-ups

- Whether v0.1 ships a real-time DSP effect chain (compressor, limiter, EQ on buses) — provisional yes for the 4 most common (compressor, limiter, EQ, reverb-send); defer richer chains to Tier C Brief 183.
- Voice chat (multiplayer) — defer to Tier F Brief 209 networking.
- HRTF spatialization — defer to v0.4 (3D-default).
- v0.2 audio creation tools brief — separate brief in Round 7.5 or Round 8.

## Sources

- Brief 097 — anti-hallucination test suite and grounding gates
- Brief 131 — seven-axis structural claim
- Brief 134 — substrate-native benchmark battery
- Brief 144 — drift detector threshold calibration
- Brief 149 — v0.1 scope finalization
- Brief 152 — game loop and tick model namespace
- Brief 153 — ECS substrate binding
- Brief 155 — camera namespace (audio listener default)
- Round 4 Brief 086C — music and audio measured-world primitives
- Wwise documentation (interactive music, RTPC, ducking)
- FMOD documentation (event system, parameter automation)
- Godot AudioStreamPlayer / AudioBus documentation
- ITU-R BS.1770 / EBU R128 loudness measurement standard
- Winifred Phillips, "A Composer's Guide to Game Music" (vertical layering reference)
