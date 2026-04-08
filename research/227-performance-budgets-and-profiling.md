# 227 — Performance budgets and profiling

## Question
What is the typed performance budget and profiling surface that enables substrate creators to declare per-target frame budgets, memory budgets, draw call budgets, asset size budgets — and have substrate sign-time gates fail builds that exceed budgets, plus a runtime profiler that pinpoints which gseed mutations cost what — across the eight engine targets?

## Why it matters (blast radius)
"Optimize at the end" is the dominant indie failure mode. Without typed budgets, perf regressions accumulate invisibly until ship. With typed budgets enforced at sign-time, perf is a first-class structural property tracked alongside correctness. Substrate's deterministic kernel makes profiling reproducible (re-run a replay = re-run the profile).

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 185 — playtest harness with replay verifier.
- Brief 196 — cross-engine parity test suite.
- Brief 220 — debugger and time-travel inspector.
- Brief 222 — testing framework and CI integration.

## Findings
1. **Typed `perf.budget.def` gseed.** Each performance budget is a typed gseed declaring: target engine, target hardware tier (low / mid / high), frame budget (ms), CPU budget per system, GPU budget per pass, memory budget (RAM / VRAM), draw call budget per scene, texture memory budget, audio voices budget, network bandwidth budget. Budgets compose: per-scene + per-recipe + per-game.
2. **Hardware tier definitions.** Substrate ships typed hardware tiers (e.g., low = Steam Deck / iPhone SE 2020 baseline; mid = mid-range PC / iPhone 13; high = current-gen console / RTX 4070). Creators target one or more tiers.
3. **Sign-time budget gates.** `gspl validate --budgets` runs static budget checks: total asset size, draw call estimate from scenes, particle count budgets, texture memory sums. Failures block sign with creator-actionable hints.
4. **Runtime profiler.** Substrate runtime ships typed profiler hooks: per-frame timeline, per-system CPU time, per-pass GPU time (where engine target supports), per-mutation cost, allocation tracking. Profiler runs during playtest and writes typed `profile.trace.gseed` for inspection.
5. **Profile trace as gseed.** Profile traces are typed signed gseeds. Lineage records the substrate version, engine target, hardware tier, replay reference. Profiles are diffable across versions to detect regressions.
6. **`gspl profile` subcommand.** CLI subcommand opens a profile trace in an interactive viewer (TUI by default; `--gui` for graphical). Renders flame graphs, per-frame timelines, allocation hot spots.
7. **Replay-driven profiling.** Because substrate is deterministic, profiling a replay is reproducible: run the same replay twice on the same hardware, get the same profile. Eliminates the dominant "I can't reproduce the slow case" debugging failure mode.
8. **Per-mutation cost.** Substrate runtime measures cost per typed mutation kind. Profile reports show "level.entity.spawn averaged 1.2ms across 200 invocations." Expensive mutations are visible.
9. **Allocation tracking.** Substrate runtime tracks gseed allocation rate. Excessive allocation (a frequent perf killer) is sign-time flagged when budget exceeded.
10. **Comparison mode.** `gspl profile diff <old> <new>` compares two profiles against the same replay. Highlights regressions and improvements per-mutation. Drives perf-aware code review.
11. **CI integration.** CI templates from Brief 222 include a perf gate: run a fixed playtest replay, compare profile to baseline, fail if regression exceeds typed threshold (default 10%).
12. **Hardware tier downgrade.** Sign-time gate can produce a "downgrade" report rather than rejection: budget exceeded for tier high, but acceptable for tier mid. Creators choose: optimize, or drop the tier.
13. **Validation contract.** Sign-time gates: every shippable build declares at least one `perf.budget.def`, declared hardware tier matches an engine-supported tier, profile baseline gseed referenced for CI comparison.

## Risks identified
- **Hardware tier definition drift.** Hardware ages; tiers need updates. Mitigation: substrate ships tier definitions as versioned gseeds; creators pin substrate version.
- **Profiler overhead.** Profiling adds runtime cost. Mitigation: profiler hooks compiled out of release builds by default; opt-in flag for ship-with-profiler.
- **Per-engine GPU profiling variance.** GPU profile APIs vary across the eight engine targets. Mitigation: substrate ships best-effort GPU timing per target; documents limitations per target.
- **Budget-induced over-engineering.** Creators may over-budget every gseed. Mitigation: substrate ships sensible defaults; budgets are opt-in beyond defaults.
- **Replay determinism + non-determinism boundary.** Network multiplayer profiles may include non-deterministic effects. Mitigation: profile traces marked deterministic vs non-deterministic; non-deterministic profiles documented as approximate.

## Recommendation
Specify performance budgets as typed `perf.budget.def` gseed with sign-time `gspl validate --budgets` gate, runtime substrate profiler emitting typed `profile.trace.gseed` traces, replay-deterministic profiling, `gspl profile` interactive viewer, profile diff comparison, and CI perf-regression gates. Substrate makes perf a first-class structural property.

## Confidence
**4 / 5.** Profiler patterns and budget gating are well-precedented (Tracy, Optick, Unity Profile Analyzer). The novelty is the deterministic-replay-driven profiling and the sign-time budget gates with downgrade semantics. Lower than 4.5 because per-engine-target GPU timing fidelity needs Phase-1 measurement.

## Spec impact
- New spec section: **Performance budgets and profiling specification**.
- Adds typed `perf.budget.def`, `hardware.tier`, `profile.trace.gseed` gseed kinds.
- Adds the `gspl validate --budgets` gate set.
- Adds the `gspl profile` subcommand.
- Adds CI perf-regression integration.
- Cross-references Briefs 152, 185, 196, 220, 222.

## New inventions
- **INV-1025** — Typed `perf.budget.def` with per-tier multi-dimensional budgets (frame / CPU / GPU / memory / draw call / asset size): performance is first-class typed declaration.
- **INV-1026** — Substrate-shipped versioned `hardware.tier` definitions: target hardware is structured creator choice with substrate-maintained reference points.
- **INV-1027** — Sign-time `gspl validate --budgets` gate with downgrade semantics: builds that exceed budgets either fail or downgrade declared tier — perf is sign-gated.
- **INV-1028** — Typed `profile.trace.gseed` as signed lineage-tracked artifact: profile data is a substrate primitive, diffable across versions.
- **INV-1029** — Replay-deterministic profiling reproducible across runs: substrate's deterministic kernel makes profiles flake-free.
- **INV-1030** — Per-mutation cost measurement: expensive mutations are visible at the typed mutation kind level, not opaque function calls.
- **INV-1031** — `gspl profile diff` comparing two traces against the same replay: perf regressions are review-detectable per-mutation.
- **INV-1032** — CI perf-regression gate with typed threshold: perf regressions block PRs structurally.
- **INV-1033** — Substrate runtime allocation tracking with budget gating: allocation-rate perf killers are sign-time visible.

## Open follow-ups
- Per-engine-target GPU timing fidelity measurement — Phase 1.
- Mobile thermal throttling profiles — deferred to v0.2.
- Network bandwidth profiling integration with Brief 209 — Phase 1.
- Memory leak detection over long playtests — deferred to v0.3.
- Auto-optimization hints from profile data — deferred to v0.4.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 185 — Playtest harness with replay verifier.
3. Brief 196 — Cross-engine parity test suite.
4. Tracy profiler documentation.
5. Optick profiler documentation.
6. Unity Profile Analyzer documentation.
7. Unreal Insights documentation.
8. Chrome DevTools Performance panel.
9. Steam Deck performance tier documentation.
