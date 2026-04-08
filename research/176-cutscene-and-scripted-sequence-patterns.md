# 176 — Cutscene and scripted sequence patterns

## Question

What canonical cutscene and scripted-sequence primitives does GSPL ship in `cutscene.*` so that any genre can adopt in-engine cutscenes, prerendered cutscenes, interactive QTE sequences, cinematic camera moves, dialogue-driven scenes, and signed scene gseeds by composition rather than from scratch, with replay determinism, skip behavior, and v0.1 reach?

## Why it matters (blast radius)

Cutscenes are how games deliver authored story moments — almost every genre uses some form of scripted sequence (Mario boss intros, Hades narrator, Witcher cinematic dialogues, Final Fantasy summons, walking-sim closing scenes). Without typed cutscene primitives, every game reinvents timeline coordination, camera blends, character animation triggers, dialogue gating, and skip behavior, breaking cross-game tooling for accessibility (skip, subtitles, motion reduction), replay, and authoring. Brief 155 (camera), Brief 161 (animation), Brief 162 (VFX), Brief 163/175 (audio), Brief 171 (dialogue), Brief 174 (UI), and Brief 197-208 (genre families) all consume `cutscene.*`.

## What we know from the spec

- Brief 152 — tick scheduler; cutscenes are tick-driven timelines
- Brief 153 — ECS substrate; cutscenes mutate scene state via signed events
- Brief 155 — camera; cutscenes drive cinematic camera shots
- Brief 158 — save/load; mid-cutscene saves and replay
- Brief 161 — animation; cutscenes trigger animation clips
- Brief 162 — VFX; cutscenes spawn VFX
- Brief 163/175 — audio; cutscenes orchestrate music and dialogue voice
- Brief 171 — dialogue; many cutscenes are dialogue-driven
- Brief 050 — accessibility; cutscenes need skip, subtitles, motion-reduction

## Findings

1. **`cutscene.timeline` as the root primitive.** A cutscene is a typed signed gseed `cutscene.timeline` containing: `cutscene_id`, `duration_ticks: u64`, `tracks: ordered_set<track_ref>`, `entry_points: set<(tick, label)>`, `exit_behavior: enum{return_to_gameplay, transition_to_scene, end_game, return_to_main_menu}`, `skip_policy: SkipPolicy`, `accessibility_props: AccessibilityProps`, `signing_authority`. A cutscene is a *timeline*, not a state machine — it advances by tick rather than by transition.

2. **Five canonical cutscene kinds.** Surveying Final Fantasy, Metal Gear Solid, Witcher 3, God of War, Hades, Hollow Knight, Last of Us, Persona 5, and short narrative games yields **5 irreducible cutscene kinds**: `cutscene.kind.in_engine_realtime`, `cutscene.kind.in_engine_offline_baked`, `cutscene.kind.prerendered_video`, `cutscene.kind.interactive_qte`, `cutscene.kind.dialogue_driven`. Each is a `kind` field on the timeline.

3. **`in_engine_realtime`.** The most common kind. Cutscene runs against the live ECS world; existing entities animate per timeline tracks, camera moves to cinematic shots, dialogue plays. Player input is gated. Determinism guaranteed because all mutations are tick-aligned signed events. Witcher-class cinematic conversations, Hades narrator interludes, Hollow Knight dream sequences.

4. **`in_engine_offline_baked`.** Same as realtime but the cutscene's per-tick state was *pre-recorded* into a typed gseed during authoring (or by a prior playthrough). Replays the recorded ticks rather than re-simulating. Used for performance-heavy cutscenes or for cross-platform parity.

5. **`prerendered_video`.** A video clip from disk. Parameters: `video_clip_ref`, `audio_clip_ref` (optional, often baked into video), `subtitle_track_ref`, `letterbox_aspect`, `playback_speed`. Substrate ships H.264 + AV1 video decoder support per Round 4 brief 089's universal pipeline; deterministic decode for replay.

6. **`interactive_qte`.** A timeline with player input windows. Parameters extending `cutscene.timeline`: `qte_events: ordered_set<QTE>` where each QTE has `tick_window: range<u64>`, `expected_action: action_ref` (Brief 154), `success_branch: timeline_label`, `failure_branch: timeline_label`. Used by God of War, Heavy Rain, Resident Evil 4. Player choices are signed input events; replays preserve them.

7. **`dialogue_driven`.** A cutscene whose timeline is mostly dialogue (Brief 171) with camera moves between speakers. Parameters: `dialogue_graph_ref`, `auto_advance_on_dialogue_complete`, `camera_shot_per_speaker_map`, `optional_letterbox`. The most common cutscene kind for narrative games.

8. **Track types.** A cutscene timeline has typed tracks. Eleven canonical track types: `cutscene.track.camera`, `track.animation`, `track.entity_transform`, `track.dialogue`, `track.audio`, `track.vfx`, `track.lighting`, `track.ui_overlay`, `track.event_emit`, `track.input_gate`, `track.tick_speed`. Each track holds keyframes or events; the substrate's timeline solver applies them in deterministic per-tick order.

9. **Camera shot integration.** `cutscene.track.camera` references signed camera shot gseeds from Brief 155. Each camera keyframe is a `(tick, shot_ref, blend_curve)`. The substrate's camera blend solver interpolates between shots deterministically. Camera DSL primitives (dolly, pan, tilt, zoom) from Brief 155 compose into shots.

10. **Animation track.** `cutscene.track.animation` references entity + animation clip + start tick. Multiple animations can play simultaneously on different entities. Substrate respects Brief 161's animation runtime constraints (4 additive layers max, signed cancel windows).

11. **Skip policy.** `SkipPolicy` parameters: `skippable: enum{always, after_first_view, never, by_section}`, `skip_action: action_ref`, `skip_confirm_required: bool`, `unskippable_sections: set<tick_range>` (for legally-required content like credits or intro logos). Substrate enforces accessibility-by-default: every cutscene is skippable unless explicitly marked otherwise, and motion-sensitive players can request `motion_reduction_mode` which substitutes a static-shot variant.

12. **Save and resume.** Mid-cutscene saves are supported. The save snapshots `(cutscene_id, current_tick, qte_state, dialogue_state)`. Resuming a save mid-cutscene replays from the current tick. Optional `cutscene.preroll_ticks` parameter rewinds N ticks for context on resume.

13. **Subtitles and accessibility.** Every cutscene must declare its subtitle source: either embedded subtitle tracks (for prerendered video), or aggregated from dialogue (for dialogue-driven). Subtitles are Brief 174 UI elements rendered through Brief 220 i18n. Audio descriptions for blind accessibility ship at v0.2+ via Brief 175 voice barks scheduled on the timeline.

14. **Triggers and gates.** Cutscenes are triggered by `cutscene.trigger` typed gseeds: `trigger_kind: enum{volume_enter, item_pickup, dialogue_choice, quest_state_change, scene_load, manual}`, `cutscene_ref`, `cooldown_ticks`, `gating_predicate`, `one_shot: bool`. Triggers are signed events.

15. **Replay determinism.** Cutscenes are tick-driven and signed; replays produce identical timelines. QTE outcomes follow signed player input events. Prerendered video plays from a deterministic decoder seek; differing video decoders may produce different *pixels*, but the *gseed-level* timeline state is bit-identical.

16. **Cross-engine export.** Cutscene gseeds export to all 8 target engines per Tier D (Briefs 188-196). In-engine realtime cutscenes export as native engine timeline assets (Godot AnimationPlayer, Unity Timeline, Unreal Sequencer). Prerendered video exports as a video file plus a typed timeline wrapper. Substrate's parity test (Brief 196) verifies cutscene playback parity.

17. **Performance budget.** A cutscene can spawn many entities, animations, VFX, and audio sources at once. Substrate enforces Brief 222's per-tick budget; cutscenes pre-declare their peak entity/audio/VFX counts at sign time so loaders can preallocate.

18. **v0.1 reach.** All 5 cutscene kinds ship schemas at v0.1. `in_engine_realtime` and `dialogue_driven` ship full runtime at v0.1. `interactive_qte` ships at v0.1. `in_engine_offline_baked` ships at v0.2. `prerendered_video` ships at v0.2 alongside the audio runtime. All track types ship schemas at v0.1; tracks dependent on v0.2+ runtimes (audio, voice) have their playback gated. Subtitles ship at v0.1 via Brief 174.

## Risks identified

1. **Cutscene determinism vs streaming.** Streaming-load cutscenes can have hitches that desync from audio. Mitigation: cutscenes preload their dependencies at trigger time; substrate's loader (Brief 153) supports timeline-aware preloading.

2. **Skip mid-section breaks state.** A cutscene that mutates ECS state will leave the world inconsistent if skipped mid-way. Mitigation: skipping always advances the timeline to its `exit_state` (a typed snapshot of expected end-state ECS mutations); the substrate diffs current vs exit and applies missing mutations atomically.

3. **Prerendered video file size.** Prerendered cutscenes can balloon distribution size. Mitigation: substrate ships AV1 encode by default for new content; H.264 for compatibility. Per-cutscene compression budget enforced.

4. **QTE accessibility.** QTEs are inherently exclusionary for some players. Mitigation: substrate ships per-cutscene `qte.accessibility_mode: enum{normal, easier_window, auto_pass}` with the `auto_pass` mode bypassing all QTEs for accessibility.

5. **Mid-cutscene saves are surprising.** Players may expect "no saves during cutscene" behavior. Mitigation: substrate default is `save_during_cutscene: false`; creators opt in per-cutscene.

6. **Unskippable content abuse.** Some publishers historically force unskippable logos. Mitigation: substrate logs and exposes `unskippable_sections` to the accessibility check (Brief 221) which warns if total unskippable duration exceeds 5 seconds.

## Recommendation

Ship `cutscene.*` with `cutscene.timeline` root, 5 cutscene kinds, 11 track types, signed camera shot integration, accessibility-first skip and motion reduction, mid-cutscene save with exit_state diff, and trigger primitive. v0.1 ships in-engine realtime + dialogue-driven + QTE; v0.2 ships baked + prerendered video. Wire to Brief 155/161/162/171/174 from day one.

## Confidence

**4/5.** Cutscene primitives are well-grounded in 30+ years of cinematic game design and the published timeline architectures of Unity Timeline, Unreal Sequencer, and Godot AnimationPlayer. Held back from 5 by the mid-cutscene save + skip exit_state diff approach which is novel and may need adjustment after Round 8 implementation.

## Spec impact

- Add `cutscene.*` namespace with `timeline`, `track.*` (11 sub-types), `trigger`, `qte`
- Add `cutscene.kind` enum with 5 values
- Add accessibility-first skip and motion-reduction defaults
- Cross-link to Brief 050 (a11y), Brief 089 (universal pipeline for video import), Brief 152 (tick scheduler), Brief 153 (ECS), Brief 154 (input for QTE), Brief 155 (camera shots), Brief 158 (mid-cutscene save), Brief 161 (animation), Brief 162 (VFX), Brief 163/175 (audio), Brief 171 (dialogue-driven), Brief 174 (subtitle UI), Brief 188-196 (export pipeline parity), Brief 220 (i18n subtitles), Brief 221 (accessibility check), Brief 222 (perf budget pre-declare)
- Mark `in_engine_offline_baked` and `prerendered_video` runtime gated to v0.2

## New inventions

- **INV-715** `cutscene.timeline` as typed signed tick-driven gseed with 11-track type system and 5 cutscene kinds
- **INV-716** Skip-with-exit-state-diff atomic mutation primitive ensuring world consistency on mid-cutscene skip
- **INV-717** Accessibility-first cutscene defaults (always-skippable + motion-reduction-variant + auto-pass-QTE) as substrate-level commitment
- **INV-718** Mid-cutscene save with optional preroll resume for context restoration
- **INV-719** Sign-time pre-declared peak entity/audio/VFX budget enabling substrate-side preallocation per cutscene

## Open follow-ups

- Audio description voice tracks for blind accessibility (deferred to v0.2 audio runtime)
- Cinematic camera DSL extensions beyond Brief 155 (Round 8 reference appendix)
- Real-time motion-capture import for cutscene authoring (deferred to v0.4)
- Cross-engine cutscene parity test details (Brief 196)

## Sources

1. Unity Timeline architecture documentation
2. Unreal Sequencer documentation and GDC talks
3. Godot AnimationPlayer documentation
4. *The Cinematic Mode of Engagement*, academic paper on cutscene theory
5. God of War (2018) cinematic camera talk, Sony Santa Monica GDC 2019
6. Last of Us Part II cinematic talk, Naughty Dog GDC 2020
7. Final Fantasy XV cutscene system retrospective, Square Enix
8. Hades narrator-interlude design, Supergiant GDC 2020
9. Heavy Rain QTE postmortem, Quantic Dream
10. Brief 050 (this repo) — accessibility commitments
11. Brief 155 (this repo) — camera shots and cinematic DSL
12. Brief 171 (this repo) — dialogue substrate
13. Brief 220 (this repo, planned) — i18n for subtitles
