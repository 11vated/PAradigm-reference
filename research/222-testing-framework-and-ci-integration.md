# 222 — Testing framework and CI integration

## Question
What is the typed testing framework and CI integration that enables substrate creators to write unit tests, integration tests, parity tests, golden replay tests, and property-based tests for gseeds and recipes — running locally via the CLI and in CI pipelines (GitHub Actions, GitLab CI, CircleCI, Buildkite) with structured failure reports?

## Why it matters (blast radius)
Substrate is signed and deterministic (Brief 152). Determinism makes testing trivially reliable: a passing test now is a passing test forever (modulo substrate version bumps). Without a typed testing framework, creators reinvent the wheel and don't exploit determinism. With one, the substrate becomes self-testing — every gseed is a testable artifact, every recipe has a test surface, every CI run is reproducible.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 185 — playtest harness with replay verifier.
- Brief 196 — cross-engine parity test suite.
- Brief 217 — CLI and headless toolchain.

## Findings
1. **`gspl test` subcommand.** CLI subcommand `gspl test` discovers and runs tests in the project. Reports pass/fail counts, durations, and structured failure details. Exits with typed exit codes for CI consumption.
2. **Test as typed gseed.** Tests are typed `test.def` gseeds declaring: name, kind (unit / integration / parity / golden / property), setup gseeds, exercise mutation sequence, expected outcome, teardown.
3. **Five test kinds.**
   - **Unit:** asserts on substrate state after a typed mutation sequence on a setup state.
   - **Integration:** asserts on multi-recipe composed state after a recipe execution sequence.
   - **Parity:** runs a fixture across N engine targets and asserts parity per Brief 196 tolerance bands.
   - **Golden replay:** runs a recorded replay and asserts the final state matches a stored golden state. Detects regressions in deterministic substrate behavior.
   - **Property:** generates random typed inputs (within typed schema bounds) and asserts substrate invariants hold across all generated cases.
4. **Determinism advantage.** Because substrate is deterministic, tests are flake-free by construction. A test that passes locally passes in CI passes in 5 years (assuming substrate version pinned).
5. **Property-based testing.** Substrate schemas drive automatic input generation. Property tests like "for any valid level.scene with N entities, validation gates always converge" exercise the full input space.
6. **Snapshot testing.** Golden replays act as snapshot tests. `gspl test --update-snapshots` regenerates goldens after intentional changes; CI runs without the flag to detect regressions.
7. **Parallel execution.** Tests run in parallel by default. Substrate determinism + isolated process model means no test interaction. `gspl test --parallel <N>` controls worker count.
8. **CI templates.** Substrate ships first-class CI templates for: GitHub Actions (`.github/workflows/gspl.yml`), GitLab CI (`.gitlab-ci.yml`), CircleCI (`.circleci/config.yml`), Buildkite (`.buildkite/pipeline.yml`). Templates run validate / test / parity / export-smoke-test on every PR.
9. **Coverage reporting.** `gspl test --coverage` reports typed coverage: which substrate primitives are exercised, which recipes are exercised, which validation gates fire. Exported as JSON for tooling integration.
10. **Mutation testing (advanced).** `gspl test --mutate` perturbs typed parameter values within schema bounds and re-runs tests, reporting which mutations are caught by tests. Identifies under-tested gseeds.
11. **Test result format.** Default output is human-readable; `--junit` emits JUnit XML for CI dashboards; `--json` emits structured JSON for programmatic consumption.
12. **Validation contract.** Sign-time gates: test gseeds reference resolvable setup states, expected outcomes typed against substrate schemas, parity tests reference declared engine targets, property tests declare typed input bounds.

## Risks identified
- **Test discovery overhead.** Large projects with many test gseeds slow discovery. Mitigation: typed test index gseed cached per project; only rebuilt on test gseed changes.
- **Property test runtime.** Random input generation can produce slow-to-validate inputs. Mitigation: typed time budget per property test; default 10 seconds; failures shrunk to minimal counterexample.
- **Golden replay drift.** Goldens become stale after intentional substrate changes. Mitigation: substrate version pinned per golden; substrate version bumps require explicit golden regeneration acknowledged by creator.
- **CI cost on parity tests.** Running 60 fixtures × 8 engines on every PR is expensive. Mitigation: typed `test.budget` field per CI run; fast/slow tiers; full parity matrix runs on main branch only.

## Recommendation
Specify the testing framework as a `gspl test` subcommand running typed `test.def` gseeds across five test kinds (unit / integration / parity / golden / property), with parallel execution, coverage reporting, mutation testing, JUnit/JSON output, and first-class CI templates for the four major platforms. Substrate determinism eliminates test flake by construction.

## Confidence
**4.5 / 5.** Test framework patterns are well-precedented. The novelty is the substrate determinism guarantee eliminating flake and enabling property-based testing over typed schemas with automatic input generation. Lower than 5 because mutation testing performance under large projects needs Phase-1 measurement.

## Spec impact
- New spec section: **Testing framework and CI integration specification**.
- Adds the `gspl test` subcommand contract.
- Adds the typed `test.def` gseed kind with five test kinds.
- Adds the four CI template specifications.
- Adds the typed coverage report schema.
- Cross-references Briefs 152, 185, 196, 217.

## New inventions
- **INV-977** — `gspl test` subcommand with typed `test.def` gseeds across five test kinds: testing is a first-class substrate primitive, not creator tooling.
- **INV-978** — Determinism-driven flake-free testing by construction: substrate's signed deterministic kernel makes test flake structurally impossible.
- **INV-979** — Property-based testing with substrate-schema-driven input generation: typed schemas are themselves test input generators.
- **INV-980** — Golden replay snapshot testing with substrate-version-pinned goldens: regression detection is exact and version-aware.
- **INV-981** — Typed test coverage reporting (primitives / recipes / gates exercised): coverage is structural, not line-based.
- **INV-982** — Mutation testing via typed schema-bound parameter perturbation: under-tested gseeds are auto-identified.
- **INV-983** — Parallel test execution by default with isolated process model: substrate determinism makes parallel test isolation trivial.
- **INV-984** — First-class CI templates for GitHub Actions / GitLab CI / CircleCI / Buildkite: substrate creators get CI integration with zero configuration.

## Open follow-ups
- Visual regression testing for rendered output — deferred to v0.2.
- Test sharding across CI workers — Phase 1.
- Test result history queries — deferred to v0.3.
- Phase-1 mutation testing performance measurement.
- Differential testing between substrate versions — deferred to v0.3.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 185 — Playtest harness with replay verifier.
3. Brief 196 — Cross-engine parity test suite.
4. Brief 217 — CLI and headless toolchain.
5. QuickCheck (Haskell property-based testing).
6. Hypothesis (Python property-based testing).
7. Jest snapshot testing.
8. Stryker mutation testing framework.
9. JUnit XML format specification.
