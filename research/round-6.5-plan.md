# Round 6.5 — Closing Round 6's open follow-ups (briefs 132-151)

## Charter

Round 6 ended with twenty open follow-ups in `round-6-synthesis.md`. Round 6.5 is a tightly-scoped mini-round that turns each one into a decided, evidence-backed recommendation **before** Round 7 commits to code. Round 7 should start with zero known unknowns at the intelligence-layer / ship-readiness boundary.

This is a closing round, not an expansion round. The substrate is locked. The architecture is locked. The seven-axis structural claim is locked. Round 6.5's job is to fill in the operational and empirical gaps that Round 6 deliberately deferred.

## Non-goals

- **No new substrate primitives.** Round 4 closed that.
- **No new constitutional commitments.** Round 4's 13 are the canonical set.
- **No new structural axes.** Round 6's seven (Signed, Typed, Lineage-tracked, Graph-structured, Confidence-bearing, Rollback-able, Differentiable) are the canonical set.
- **No new namespaces or URL schemes.** Round 6's `tool-call://`, `adapter://`, `improvement-log://` are the last additions.
- **No code.** Round 6.5 is research/decision; Round 7 is implementation.
- **No new inventions for inventions' sake.** Round 6.5 inventions only where a follow-up genuinely produces a novel mechanism. Otherwise it's a calibration brief, and that's fine.

## Scope

Twenty briefs, one per Round 6 follow-up, in the order they appear in the synthesis. Each brief is decisional: it produces a concrete recommendation Round 7 can act on without further research.

| # | Title | Round 6 follow-up | Tier |
|---|---|---|---|
| 132 | Router classifier training data | (1) | X-Calibration |
| 133 | LATS value function: handcrafted vs learned | (2) | X-Calibration |
| 134 | Substrate-native benchmark battery | (3) | Y-Empirical |
| 135 | Hardware budget for v0.1 context ceiling | (4) | Y-Empirical |
| 136 | Deep Research workflow recipe | (5) | Z-Recipe |
| 137 | Multi-modal backbone selection | (6) | X-Calibration |
| 138 | Compaction cadence calibration | (7) | X-Calibration |
| 139 | Procedural promotion threshold tuning | (8) | X-Calibration |
| 140 | ColBERT storage budget at federation scale | (9) | Y-Empirical |
| 141 | Cross-encoder distillation recipe | (10) | Z-Recipe |
| 142 | Grammar compilation performance budget | (11) | Y-Empirical |
| 143 | Differentiable action learning recipe | (12) | Z-Recipe |
| 144 | Drift detector threshold calibration | (13) | X-Calibration |
| 145 | GPU time cost model for monthly/quarterly cadence | (14) | Y-Empirical |
| 146 | JEPA predictive embedding dataset construction | (15) | Z-Recipe |
| 147 | Federation-wide adapter review protocol | (16) | W-Operational |
| 148 | World model formalization beyond Brief 131 | (17) | W-Operational |
| 149 | v0.1 scope finalization and feature cuts | (18) | W-Operational |
| 150 | External benchmark battery selection | (19) | Y-Empirical |
| 151 | Creator-facing communication of the seven axes | (20) | W-Operational |

### Tier legend

- **X-Calibration:** A tunable parameter or threshold that needs empirical bounding before it can be set.
- **Y-Empirical:** A measurement question — what is the actual cost / performance / size?
- **Z-Recipe:** A training or construction recipe that needs to be specified end-to-end.
- **W-Operational:** A protocol, scope, or communication decision.

## Brief template

Same as the canonical research brief template (Question / Why it matters / What we know / Findings / Risks / Recommendation / Confidence / Spec impact / Open follow-ups / Sources). Round 6.5 briefs are typically shorter (3-10 findings each) because each follow-up is narrow by construction.

## Inventions

Round 6.5 may add a small number of inventions where a follow-up genuinely produces a new mechanism. The expected total is **5-15 inventions** (INV-556 onward), most of them small (calibration tables, sampling protocols, threshold formulas), not architectural.

## End conditions

Round 6.5 is complete when:

1. All 20 follow-ups have a decided recommendation in their respective brief.
2. Each recommendation is evidence-backed at confidence ≥ 3/5.
3. `round-6.5-synthesis.md` exists with the consolidated calibration tables and the v0.1 build-ready statement.
4. The README is updated to reflect 151 total briefs and the Round 6.5 set.
5. Round 7 can be started without re-opening any of these twenty questions.

## Why a half-round, not a full Round 7

Round 7 is implementation. It needs the calibration table, the recipe sheet, and the scope-cut decision to be **already made** when it starts. Forcing those decisions inside Round 7 would couple research with code and slow both. A half-round of 20 narrow briefs is the cheapest way to fully de-risk the implementation start.

## Round 6.5 → Round 7 hand-off

When Round 6.5 closes, Round 7 inherits:

- A calibration table (one row per X-Calibration brief)
- An empirical cost table (one row per Y-Empirical brief)
- A recipe sheet (one document per Z-Recipe brief)
- A v0.1 scope manifest (Brief 149)
- A creator-facing message (Brief 151)
- A benchmark battery (Briefs 134 + 150)

These six artifacts plus the locked Round 1-6 architecture are sufficient for Round 7 to begin coding.
