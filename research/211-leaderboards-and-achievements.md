# 211 — Leaderboards and achievements

## Question
What is the typed leaderboard and achievement surface that enables substrate gseeds to support persistent rankings, daily/weekly leaderboards, achievements with unlock conditions, and replay-verified scores across the federation, without locking creators into a centralized service?

## Why it matters (blast radius)
Leaderboards and achievements drive retention in single-player and multiplayer alike. The substrate's signed-replay determinism (Brief 185, 196) makes verifiable leaderboards structurally possible: a posted score can include the replay gseed and any node can verify it. Without typed primitives, every creator reinvents this and the verification story collapses.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 185 — playtest harness with deterministic replay.
- Brief 196 — cross-engine parity.
- Brief 210 — account and identity surface.

## Findings
1. **Leaderboard as typed gseed.** `leaderboard.def` declares: typed score field reference, sort order (ascending / descending), scope (global / friends / regional / daily / weekly / all-time), maximum entries, replay attachment requirement (boolean).
2. **Score submission as typed mutation.** Player completes a run; substrate emits typed `leaderboard.submit` mutation containing: identity reference, score value, replay gseed reference (if required), submission timestamp. Mutation is signed per Brief 152.
3. **Replay-verified scores.** When `replay attachment required` is true, the leaderboard server replays the gseed through the substrate kernel and confirms the resulting score matches the submitted value. Mismatched submissions are rejected. This is the killer feature — verifiable leaderboards.
4. **Achievement as typed gseed.** `achievement.def` declares: typed unlock condition (referencing substrate state via Brief 180's expression DSL), display name, description, icon asset reference, hidden flag, lineage-recording requirement.
5. **Achievement unlock as typed mutation.** When unlock condition holds, substrate runtime emits typed `achievement.unlock` mutation appended to player identity's achievement list. Mutation is signed.
6. **Federation pattern.** Leaderboard and achievement state lives in a substrate federation node (per Brief 210). Creators run their own; players from any federated node can see leaderboards if the creator opts in. No centralized substrate-hosted leaderboard service.
7. **Daily/weekly resets.** `leaderboard.def` typed reset schedule (none / daily / weekly / monthly / per-version). Reset rotates the leaderboard, archiving prior periods to substrate-history.
8. **Anti-cheat via replay verification.** Replay-required leaderboards are structurally cheat-resistant: any score with a verifiable replay is provably legitimate. Scores without replays (e.g., simpler arcade leaderboards) are creator-trust-based.
9. **Achievement validation contract.** Sign-time gates: achievement unlock conditions reference resolved substrate state, achievement icons exist, hidden achievements have descriptions visible only post-unlock.
10. **Steam / console achievement integration.** Substrate's achievement system mirrors to Steam / Xbox / PSN achievements via creator-implemented adapters. Substrate provides the typed bridge; creators handle platform-specific submission.

## Risks identified
- **Replay verification cost.** Verifying replays costs server CPU. Mitigation: typed verification budget per leaderboard; sampling-based verification for high-volume leaderboards (verify 10% of submissions, ban verified-cheaters).
- **Replay storage cost.** Replay gseeds can be large. Mitigation: zstd compression per Brief 005; reference-only retention for non-top scores.
- **Federation discovery.** Players don't know which nodes host leaderboards. Mitigation: substrate ships leaderboard discovery via federation directory in Brief 210.
- **Cross-version compatibility.** Substrate updates can break old replays. Mitigation: leaderboards are typed with substrate-version pinning; legacy versions get separate leaderboard scopes.
- **Hidden cheat surface.** Non-replay leaderboards are cheatable. Mitigation: documented as creator-trust-based; recommend replay-required for competitive scopes.

## Recommendation
Specify the leaderboard and achievement surface as typed `leaderboard.def` + `achievement.def` gseeds with typed unlock conditions referencing substrate state, replay-verified score submission as the cheat-resistance primitive, federated hosting via Brief 210, daily/weekly/monthly reset schedules, and substrate-version pinning. Default leaderboards in v0.1 ship as replay-required for competitive scopes; non-verified leaderboards are documented as creator-trust-based.

## Confidence
**4.5 / 5.** Leaderboards and achievements are well-precedented; the novelty is replay-verified scores as a substrate primitive enabled by Brief 185's deterministic replay. Lower than 5 because verification cost at scale needs Phase-1 measurement.

## Spec impact
- New spec section: **Leaderboards and achievements specification**.
- Adds typed `leaderboard.def`, `leaderboard.submit`, `achievement.def`, `achievement.unlock` gseed kinds.
- Adds replay-verified score submission contract.
- Adds the substrate-version pinning model for leaderboards.
- Cross-references Briefs 005, 152, 180, 185, 196, 210.

## New inventions
- **INV-893** — Typed `leaderboard.def` with replay-verified score submission contract: leaderboards are first-class typed gseeds with structural cheat resistance via Brief 185 deterministic replay.
- **INV-894** — Typed `achievement.def` with unlock conditions referencing substrate state via expression DSL: achievements are declarative typed predicates over typed game state, not opaque scripts.
- **INV-895** — Federated leaderboard hosting via Brief 210 identity nodes: leaderboards live with creators, no centralized substrate service.
- **INV-896** — Sampling-based replay verification for high-volume leaderboards: typed budget caps verification cost while maintaining cheat resistance.
- **INV-897** — Substrate-version pinned leaderboards: substrate updates that change replay semantics don't invalidate leaderboards; old versions get separate scopes.
- **INV-898** — Steam / console achievement adapter pattern via creator-implemented bridges: substrate provides the typed bridge contract, creators handle platform submission.

## Open follow-ups
- Phase-1 verification cost measurement at scale.
- Tournament bracket primitives — deferred to v0.3.
- Speedrun-specific leaderboard features (categories, glitches) — deferred to v0.3.
- Cross-platform unified leaderboards (Steam + console + federation) — deferred to v0.4.

## Sources
1. Brief 005 — zstd deterministic encoding.
2. Brief 152 — Substrate signing and lineage.
3. Brief 180 — Dialogue and quest editor (expression DSL).
4. Brief 185 — Playtest harness.
5. Brief 196 — Cross-engine parity test suite.
6. Brief 210 — Account and identity surface.
7. speedrun.com replay verification practices.
8. Steam achievements documentation (partner.steamgames.com).
