# 185 — Playtest harness specification

## Question
What is the playtest harness that runs a `level.scene` against typed inputs (Brief 154), records signed sessions, captures telemetry, and replays deterministically — and how does it bind every prior editor (177-184) to live debug?

## Why it matters (blast radius)
The playtest harness is where every editor's "preview = runtime" promise is empirically validated. If sessions aren't recorded with full lineage, regression testing collapses. If replay isn't deterministic, the seven-axis claim is false at the highest-stakes surface. If the harness is separate from the debugger surfaces of Briefs 177-184, creators have to context-switch to debug.

## What we know from the spec
- Brief 027 — reproducibility test harness.
- Brief 052 — lineage time machine.
- Brief 152 — fixed-tick scheduler.
- Brief 154 — input abstraction with signed input recordings for replay.
- Brief 158 — save/load and partial save chunks.
- Brief 056 — observability, telemetry, privacy.
- Briefs 177-184 — editor live-debug binding points.

## Findings
1. **Harness = isolated runtime + recorder + replayer + telemetry sink.** The harness instantiates the substrate's runtime in an isolated process, fed by the editor's current scene gseed. It owns its own tick clock, input pipe, and audio/video output. It does not share state with any editor.
2. **Session recording.** A typed `playtest.session` gseed records: starting scene gseed hash, full input stream (Brief 154 signed input recording), all signed lineage events emitted during play, telemetry counters (Brief 056), and termination state. The session is signed at end-of-play.
3. **Replay determinism.** Loading a session into the harness reproduces the exact tick-by-tick state. The harness verifies replay determinism by hashing entity-state-per-tick and comparing against a stored verifier. Mismatch fails the replay loudly with the offending tick number — Brief 027's test harness is the implementation backbone.
4. **Live editor binding.** Each editor (177-184) can attach to a running harness session. Brief 181's BT debugger, Brief 179's animation timeline, Brief 183's audio mixer, Brief 184's UI layout, and Brief 177's scene tree all read live state from the harness's runtime. Attach is read-only by default; "live edit" mode applies edits to the harness as well as the gseed, with sign-time validation.
5. **Pause / step / scrub.** The harness exposes tick controls: pause, step (one tick), step-frame (one variable-rate frame), scrub (rewind via lineage). Pause / step are O(1); scrub uses Brief 052's time machine.
6. **Telemetry capture.** The harness captures typed `telemetry.event` records (FPS, tick time, entity count, draw calls, audio active sources, AI tick budget, memory) at a configurable rate (default once per second). All telemetry is opt-in per Brief 056 and stored in the session gseed.
7. **Recorded session as test fixture.** A signed session is a typed test fixture. The QA layer (Brief 229 forthcoming) runs sessions against the current substrate build to detect regressions. Sessions become unit tests by construction.
8. **Crash capture.** If the runtime crashes during a session, the harness captures the lineage up to the crash, the input that triggered it, and the substrate version. The result is a typed `playtest.crash_repro` gseed that the substrate's bug tracker can ingest directly.
9. **Multi-resolution rendering.** The harness can render at the editor's chosen target resolution and at the substrate's reference resolution simultaneously, comparing the two for visual divergence. This catches editor / runtime visual drift.
10. **Headless mode.** The harness can run without a window (headless) for CI / batch / regression test runs. Headless mode skips rendering by default but executes all logic ticks.
11. **Network isolation.** The harness blocks all outbound network calls by default. Multiplayer testing requires explicit opt-in and routes through a typed `playtest.virtual_lobby` (Brief 211 forthcoming).
12. **Speed control.** Tick rate can be slowed (0.1x default minimum, useful for debugging) or sped up (10x default maximum, useful for soak testing). Audio is muted when not at 1x to avoid pitch artifacts.

## Risks identified
- **Replay non-determinism from external state.** Anything reading from outside the substrate (filesystem, clock, network) breaks replay. Mitigation: harness intercepts and stubs all external reads with deterministic sources — wallclock becomes tick-derived, filesystem becomes a snapshot, network is denied.
- **Session size on long playtests.** A 30-minute session can produce gigabytes. Mitigation: lineage events are zstd-compressed (Brief 005); telemetry rate is capped; binary blobs (screenshots) are stored once and referenced.
- **Editor-attach feedback loops.** Live editing during a session can cause re-entrancy. Mitigation: edits are queued at the next tick boundary, never mid-tick; the harness's tick scheduler is the only mutator.
- **Crash repro reproducibility.** Crashes that depend on hardware state (GPU memory pressure) might not reproduce. Mitigation: the harness records a hardware fingerprint with the crash; reproduction requires a similar fingerprint or the crash is downgraded to "not deterministic" status.
- **Telemetry PII risk.** Telemetry could leak player data. Mitigation: per Brief 056, all telemetry events have a typed PII classification; collection is opt-in and the harness refuses to store PII-classified events without a creator's explicit acknowledgement.

## Recommendation
Specify the playtest harness as an isolated runtime with full session recording, deterministic replay verifier, live editor attach to all Briefs 177-184 surfaces, headless and speed-controlled modes, and tick-boundary-only mutation. Make every recorded session a regression test fixture by default. Defer multiplayer harness mode to v0.3.

## Confidence
**4.5 / 5.** Playtest harness patterns are well-precedented (Unreal Insights, Unity Profiler + Play Mode, Godot remote inspector, browser devtools). The novelty is the lineage-signed session as a first-class test fixture, the editor-attach unification across all editor surfaces, and the deterministic replay verifier as a hard sign-time gate. Lower than 5 because external-state stubbing coverage is empirical.

## Spec impact
- New spec section: **Playtest harness specification**.
- Adds `playtest.session`, `playtest.crash_repro`, `playtest.virtual_lobby` typed primitives.
- Adds the editor-attach contract between harness and Briefs 177-184.
- Cross-references Briefs 027, 052, 056, 152, 154, 158.

## New inventions
- **INV-759** — Lineage-signed playtest session as first-class test fixture: every session is a signed gseed and a regression test by construction.
- **INV-760** — Universal editor-attach to harness across all editor surfaces (177-184): one harness, many concurrent editor inspectors, all reading live runtime state.
- **INV-761** — Deterministic replay verifier as sign-time gate: replay hashes entity state per tick and fails loudly on the offending tick if state diverges.
- **INV-762** — External-state stubbing: wallclock, filesystem, network are intercepted and replaced with deterministic substitutes during harness runs.
- **INV-763** — Crash repro gseed with hardware fingerprint: substrate crashes produce typed bug-trackable gseeds with the lineage tail and the hardware context.

## Open follow-ups
- Multiplayer harness mode (deferred to v0.3 with Brief 211).
- GPU debugging integration (RenderDoc / NSight) — deferred to v0.2.
- Performance flame graph in editor (deferred to v0.2).
- Distributed soak testing across federation peers (deferred to v0.4).
- Adversarial fuzz testing of input streams (deferred to v0.3).

## Sources
1. Brief 005 — zstd deterministic encoding.
2. Brief 027 — Reproducibility test harness.
3. Brief 052 — Lineage-aware time machine.
4. Brief 056 — Observability, telemetry, privacy.
5. Brief 152 — Game loop and tick model.
6. Brief 154 — Input abstraction.
7. Brief 158 — Save / load and serialization.
8. Briefs 177-184 — editor surfaces.
9. Unreal Insights documentation.
10. Unity Profiler documentation.
