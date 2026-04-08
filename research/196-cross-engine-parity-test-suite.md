# 196 — Cross-engine parity test suite

## Question
What is the cross-engine parity test suite that validates an identical signed gseed bundle renders, simulates, and behaves identically across all eight v0.1 export targets (Godot, Unity, Unreal, Phaser, GameMaker, HTML5, Defold, Cocos) within published tolerance bands, and what are the typed pass/fail contracts that gate a substrate release?

## Why it matters (blast radius)
Briefs 188-195 specify *how* to export to each engine. This brief specifies *how we know the exports are correct*. Without an enforced parity test suite, the eight pipelines drift independently, creator promises decay, and "write once, ship anywhere" becomes marketing. The parity suite is the structural guarantee behind every other export brief and is the single highest-leverage quality investment in the round.

## What we know from the spec
- Brief 020 — determinism contract per engine.
- Brief 075 — GSPL without a real GPU (golden-image tolerance bands).
- Briefs 188-195 — eight engine export pipelines.
- Brief 185 — playtest harness (deterministic replay verifier).
- Brief 152 — substrate signing and lineage.

## Findings
1. **Parity fixture corpus.** The suite ships a curated corpus of ~60 signed gseed bundles ("parity fixtures") covering: empty scene; single sprite; tilemap with autotile; skeletal animation; particle VFX; physics sandbox; audio mixer with all eight effects; UI screen with WCAG-tested elements; behavior-tree NPC; FSM state graph; dialogue with locale variants; save/load round-trip; replay-deterministic gameplay loop; mod-loaded scene; and one composite fixture per Tier E genre family. Each fixture is signed and pinned to a content hash.
2. **Per-fixture per-engine matrix.** Every fixture exports to all eight engines and produces: (a) golden frame captures at fixed deterministic timestamps, (b) audio waveform captures at the same timestamps, (c) physics state dumps, (d) replay-determinism logs, (e) save-snapshot binary blobs, (f) UI element geometry dumps, (g) particle position dumps, (h) signed lineage ledgers. The matrix is 60 × 8 = 480 cells; each cell produces ~8 artifacts per run.
3. **Tolerance bands per artifact kind.** Per Brief 075: rendered frames compare with SSIM ≥ 0.97 against the substrate reference; audio compares with 0.5 dB RMS tolerance per frame and ±10ms phase tolerance; physics positions compare with 0.001 unit tolerance; particle positions with 0.01 unit tolerance; UI geometry with 0.5 px tolerance; save blobs with bit-exact equality after deterministic-decode; replay logs with bit-exact equality. Tolerance bands are typed fields, not magic constants.
4. **Reference produces ground truth.** The substrate's headless reference renderer (Brief 075) produces the ground-truth frames, audio, physics state, and so on. Each engine target's output is compared against the reference, not pairwise. This avoids combinatorial blowup (8² = 64 pairwise comparisons) and creates a single authoritative source.
5. **Headless engine harness.** Each engine runs in headless mode in CI: Godot `--headless`, Unity batch mode, Unreal `-nullrhi -nosound`, Phaser via Playwright + headless Chromium, GameMaker via the YYC compiler + GMS test runner, HTML5 via Playwright, Defold via `dmengine --headless`, Cocos via `cc-runtime --headless`. Each harness loads the export target, executes the fixture's deterministic playback, and captures all artifact kinds.
6. **Capture at deterministic timestamps.** Captures happen at fixed fixture timestamps (0ms, 100ms, 1s, 5s, 30s) that match the substrate reference's capture timestamps. Each fixture declares its own capture schedule as a typed field.
7. **CI infrastructure.** Parity runs on a GitHub Actions matrix with one runner per engine. Linux runners cover Godot/Phaser/HTML5/Defold/Cocos; macOS for Unity (URP), Unreal, and additional GameMaker validation; Windows for GameMaker primary and as Unity/Unreal redundancy. Total matrix: 60 fixtures × 8 engines × 3 host OSes (where applicable) ≈ 800 runs per CI invocation.
8. **Run cadence.** Full parity suite runs (a) on every substrate release candidate, (b) nightly on `main`, (c) on every PR touching `export/` paths, (d) weekly against latest engine versions to catch upstream breakage. Reduced "smoke" subset runs on every PR.
9. **Failure classification.** Each parity failure is typed: `tolerance_exceeded`, `harness_crash`, `export_failure`, `engine_version_drift`, `external_solver_divergence` (e.g., Spine IK from Brief 195), `external_renderer_divergence` (e.g., Unreal Niagara module quirks), `unsupported_pattern` (sign-time gates correctly rejected). Only `tolerance_exceeded` and `harness_crash` block release; the others surface as warnings or expected divergences with linked-issue references.
10. **External-solver waiver mechanism.** When divergence comes from an external solver (Spine IK, Unity PhysX without substrate kernel, Niagara minor variance), the failure is logged with an explicit waiver tag in the parity report, and the cell shows "external" rather than "fail." Waivers are typed and require a signed justification from a substrate maintainer; un-waived divergence is a release blocker.
11. **Golden-frame storage.** Reference frames and audio captures live in a content-addressed blob store (Brief 005 zstd; Brief 152 signing). Comparison uses the cached reference; first-time fixture additions require maintainer approval to seed the golden artifact.
12. **Replay determinism cross-check.** Each fixture also runs Brief 185's replay verifier on each engine target's replay log. Replay-bit-equality across multiple runs of the same engine is the strictest gate; any non-determinism within a single engine target is a release blocker regardless of cross-engine state.
13. **Performance bands as soft gates.** Frame time, memory, and load-time per fixture per engine are captured. Performance regressions of >20% versus the prior release are warnings; >50% are release-blocking unless waived. Tracked over time as a parity-perf timeline.
14. **Parity report artifact.** Each CI run produces a signed parity report gseed: typed matrix of (fixture, engine, artifact, status, tolerance, waiver). The report is committed to `parity-history/` and queryable by future CI runs to detect regressions across releases. Reports are first-class substrate artifacts.
15. **Coverage for Tier C-only features.** Editor features from Tier C (177-187) that don't appear in runtime exports (e.g., the timeline scrubber UI from 179) are tested by Brief 185's harness, not the parity suite. The parity suite only tests artifacts that ship to creators.

## Risks identified
- **CI cost.** 800 runs per invocation across multiple OSes is expensive. Mitigation: per-PR smoke subset (≤50 runs); full matrix only nightly + on release. Cache reference artifacts aggressively.
- **Engine version churn.** Engines update independently; fixtures may break when an upstream renderer changes a default. Mitigation: pin engine versions in CI per substrate release; weekly upstream-version run with separate report; version bumps require parity re-baseline.
- **Tolerance band tuning.** Bands may be too strict (false positives) or too loose (real bugs slip through). Mitigation: tolerance bands are typed fields with substrate-version pinning; tightening a band is a release-note item; loosening requires maintainer signoff.
- **Headless mode quirks.** Some engines behave subtly differently in headless mode (e.g., Unreal with `-nullrhi`). Mitigation: per-engine headless-quirk database documented in `parity-quirks.md`; quirks are typed as expected divergences with waivers.
- **Reference renderer drift.** The substrate reference renderer is itself code that can change. Mitigation: substrate releases are signed and the parity report records the reference renderer version per fixture run; parity history includes reference-version metadata.
- **Cross-OS reproducibility.** Floating-point determinism across Linux/macOS/Windows can drift even with substrate's deterministic kernels. Mitigation: substrate ships its own soft-float library for replay-critical paths (already in Brief 020 contract); cross-OS bands are slightly looser than same-OS bands.

## Recommendation
Specify the cross-engine parity test suite as a typed (fixture × engine × artifact) matrix with per-artifact-kind tolerance bands, headless engine harnesses producing golden captures at fixed deterministic timestamps, comparison against the substrate reference renderer, typed failure classification with external-solver waivers, signed parity report gseeds committed to `parity-history/`, and full-matrix runs on every release candidate plus a smoke subset on every PR. This brief is the structural guarantee behind every export pipeline.

## Confidence
**4 / 5.** The parity suite architecture is straightforward (matrix CI + tolerance comparison), but the empirical risk is real: engine quirks, headless-mode oddities, cross-OS float drift, and tolerance-band tuning all need Phase-1 measurement. Lower than 4.5 because the brief makes promises that only running the full matrix can validate. This is intentional — the brief is the contract; Phase-1 is the proof.

## Spec impact
- New spec section: **Cross-engine parity test suite specification**.
- Adds typed `parity.fixture`, `parity.tolerance`, `parity.report`, `parity.waiver` gseed kinds.
- Adds the headless harness contract per engine.
- Adds the parity-history directory and report retention policy.
- Cross-references Briefs 020, 075, 152, 185, 188-195.

## New inventions
- **INV-813** — Typed (fixture × engine × artifact × tolerance × status × waiver) parity matrix as a signed gseed: parity reports are first-class substrate artifacts queryable across releases.
- **INV-814** — Per-artifact-kind tolerance bands as typed fields with substrate-version pinning: SSIM/RMS/positional/bit-exact bands are not magic constants but versioned contracts.
- **INV-815** — Substrate reference renderer as single ground truth with engine targets compared 1-vs-reference: avoids combinatorial pairwise blowup, creates a single authoritative source per artifact kind.
- **INV-816** — Typed external-solver waiver mechanism: divergence from third-party solvers (Spine IK, PhysX, Niagara) is explicitly typed and signed by a maintainer, distinguishing "expected difference" from "regression."
- **INV-817** — Parity-history directory as queryable substrate state: parity reports accumulate over releases enabling regression detection across the substrate's lifetime.
- **INV-818** — Headless engine harness contract: each engine target ships a substrate-maintained headless invocation recipe with documented quirks, enabling reproducible CI captures across host OSes.

## Open follow-ups
- Phase-1 tolerance band calibration against real fixtures (the empirical gap above).
- Console-target parity (deferred — no console exports in v0.1).
- Performance-band hard gates (currently soft) — promote to hard gates in v0.2 once historical baseline exists.
- Visual diff viewer for parity reports (creator-facing) — deferred to Studio v0.2.
- Mobile-runtime parity on real devices (vs. headless emulators) — deferred to v0.3.

## Sources
1. Brief 005 — zstd deterministic encoding.
2. Brief 020 — Determinism contract per engine.
3. Brief 075 — GSPL without a real GPU.
4. Brief 152 — Substrate signing and lineage.
5. Brief 185 — Playtest harness.
6. Briefs 188-195 — engine export pipelines.
7. SSIM specification (Wang et al. 2004).
8. GitHub Actions matrix documentation.
9. Playwright headless browser documentation.
