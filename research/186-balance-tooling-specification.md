# 186 — Balance tooling specification

## Question
What is the creator-facing balance tooling surface that runs simulations against typed `combat.*` (Brief 167), `economy.*` (Brief 166), `progression.*` (Brief 165), and `loot.*` (Brief 169) gseeds with monte-carlo aggregation, sensitivity analysis, and signed result fixtures?

## Why it matters (blast radius)
Balance is where games live or die — a 10% damage tweak can break an entire build path. Without sign-time validation through simulation, creators ship broken meta. Without monte-carlo aggregation, single-run results mislead. Without lineage on simulation results, balance changes can't be audited.

## What we know from the spec
- Brief 165 — progression composition with sign-time monotonic XP curves and acyclic skill DAG.
- Brief 166 — economy faucet/sink graphing.
- Brief 167 — combat damage formulas and resolution modes.
- Brief 168 — vector difficulty KPIs from enemy.encounter validation.
- Brief 169 — loot tables with sub-seeded PRNG.
- Brief 027 — reproducibility test harness.
- Brief 185 — playtest harness.

## Findings
1. **Tooling surface = stat tables + simulation runner + result inspector.** Stat tables expose typed `progression.*`, `combat.*`, `economy.*`, `loot.*` gseeds in editable grid form. The simulation runner spawns N parallel headless harness sessions (Brief 185 headless mode) with parameter sweeps. The result inspector renders aggregate metrics with confidence intervals.
2. **Stat-table editor.** A stat table is a typed view over a set of gseeds — for example, "all enemy.encounter difficulty knobs" or "all combat.damage_formula coefficients". Edits commit through the same modifier-surface contract as Brief 177. Bulk edits across rows are typed batch mutations.
3. **Simulation primitive.** A typed `balance.simulation` gseed declares: target scenario (typically a `level.scene` or a synthetic encounter), parameter sweep (typed param × range × step), iteration count (default 1000), random seed strategy (per-iteration sub-seed), and metric selectors (which telemetry to aggregate).
4. **Monte-carlo aggregation.** The runner produces typed `balance.result` gseeds containing per-metric mean, median, stddev, p5, p25, p50, p75, p95, p99, and a confidence interval at the requested level (default 95%). All numbers are deterministic given the seed strategy — re-running produces bit-identical aggregates.
5. **Sensitivity analysis.** A typed `balance.sensitivity_run` varies one parameter while holding others fixed, then ranks parameters by effect size on the metric of interest. Output is a typed `balance.sensitivity_report` gseed listing the top-N influential parameters.
6. **Signed result fixtures.** Every simulation run produces a signed result gseed. Repeating the run on a fresh substrate version is the regression check — if results drift, the substrate caught a behavior change.
7. **Faucet/sink validation.** Per Brief 166's economy graphing, the balance tool can run an N-day economy simulation against the current `economy.*` configuration and surface flow imbalances. Sign-time validator reuses the same auto-graphing.
8. **Loot drop validation.** Per Brief 169, the tool can run M loot rolls against a `loot.table` and verify the empirical drop frequencies match the declared probabilities within a chi-squared confidence band. Failures surface as typed errors at sign time.
9. **Encounter difficulty curve check.** Per Brief 168's vector difficulty KPIs, the tool runs an enemy encounter against canonical player loadouts and surfaces the resulting difficulty vector. Encounter authors get immediate feedback on whether they hit the intended difficulty cell.
10. **Power curve check.** Per Brief 165, the tool runs a progression curve against a typical play session and verifies XP growth is monotonic and matches the declared pacing target. Out-of-band growth surfaces as a warning.
11. **Multi-axis comparison.** The result inspector overlays multiple runs for diff comparison — "before tweak vs after tweak" is a one-click view, not a manual export-and-diff workflow.
12. **Counterfactual replay.** Combine with Brief 052 lineage time machine: a recorded playtest session can be replayed with a parameter changed (via fork) to ask "what if armor was 10% higher?". The harness re-runs from the fork point and produces a new signed result.

## Risks identified
- **Simulation runtime cost.** N=1000 iterations × parameter sweep × scenario duration can be hours. Mitigation: distribute runs across cores; cache results keyed on parameter hash; expose a "quick" preset (N=100) for iterative tweaks.
- **Monte-carlo seed contamination.** Using the same seed across iterations would produce false convergence. Mitigation: per-iteration sub-seeds derived from a master seed (Brief 169 PRNG keying pattern).
- **Sensitivity analysis combinatorial explosion.** N parameters × M values × O scenarios scales fast. Mitigation: surface a variance-decomposition mode (Sobol-style) that ranks parameters by main effect cheaply.
- **Statistical misinterpretation by creators.** Confidence intervals are easy to misread. Mitigation: result UI labels intervals plainly ("95% chance the true value is within X-Y"); avoids p-value language.
- **Drift between balance simulation and actual gameplay.** Simulation models can diverge from human player behavior. Mitigation: results are advisory, not normative; the tool surfaces a "real player data" overlay when telemetry from playtest sessions is available.

## Recommendation
Specify the balance tooling as stat-table editor + simulation runner + result inspector, all over the existing modifier-surface contract. Ship monte-carlo aggregation, sensitivity analysis, faucet/sink/loot/encounter/progression validators, and signed result fixtures at v0.1. Defer real-player-telemetry overlay to v0.2 with telemetry runtime. Defer Sobol-style variance decomposition to v0.2 as a power tool.

## Confidence
**4 / 5.** Balance simulation has thinner direct precedent than other editor surfaces (most studios build internal tooling), but the underlying primitives — monte-carlo runs, sensitivity analysis, parameter sweeps — are well-understood. The novelty is the substrate-level signed result fixture and the unification with Briefs 165/166/167/168/169 sign-time validators. Lower than 4.5 because the per-domain validator coverage will reveal gaps in Phase 1.

## Spec impact
- New spec section: **Balance tooling surface specification**.
- Adds `balance.simulation`, `balance.result`, `balance.sensitivity_run`, `balance.sensitivity_report` typed primitives.
- Cross-references Briefs 165, 166, 167, 168, 169, 185.

## New inventions
- **INV-764** — Stat-table editor over typed gseed views: bulk-editable stat grids over any namespace, committing through the standard modifier-surface contract.
- **INV-765** — Monte-carlo simulation primitive with deterministic per-iteration sub-seeds: aggregates produced are bit-identical on re-run, making balance results signable as fixtures.
- **INV-766** — Sensitivity-ranking sub-primitive: vary-one-hold-all-others over a metric of interest, ranked by effect size, with a Sobol-style variance decomposition mode deferred as a power tool.
- **INV-767** — Counterfactual replay binding: lineage-forked playtest sessions answer "what if X was different" with re-runs from the fork point producing signed result fixtures.
- **INV-768** — Cross-namespace balance validators: faucet/sink, loot frequency, encounter difficulty, and progression curve validators reuse the sign-time gates from Briefs 165-169 inside an iteration loop.

## Open follow-ups
- Real-player telemetry overlay (deferred to v0.2 with telemetry runtime).
- Sobol-style variance decomposition (deferred to v0.2).
- Distributed simulation across federation peers (deferred to v0.4).
- ML-driven parameter optimization (deferred to v0.5 with neurosymbolic surfaces).
- Tournament-style auto-balancing (deferred — requires Round 8 agent surfaces).

## Sources
1. Brief 027 — Reproducibility test harness.
2. Brief 052 — Lineage-aware time machine.
3. Brief 165 — Progression system patterns.
4. Brief 166 — Economy and currency patterns.
5. Brief 167 — Combat system patterns.
6. Brief 168 — Enemy and creature taxonomies.
7. Brief 169 — Loot drop and reward systems.
8. Brief 185 — Playtest harness specification.
9. Sobol method — Saltelli et al., Variance-based sensitivity analysis (2008).
