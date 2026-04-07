# 139 — Procedural promotion threshold tuning

## Question

When does a successful workflow trace get promoted from episodic memory into a signed procedural-memory skill gseed (Brief 127), and what is the threshold function?

## Why it matters (blast radius)

Procedural memory is the substrate's compounding asset. Every promoted skill becomes a creator's reusable, shareable, signed capability — and through Brief 100's federation, eventually a community-shareable capability. Promote too eagerly and procedural memory fills with noise; promote too cautiously and creators never benefit from their own learning. The threshold is what makes the substrate self-improving at the *creator* tier rather than only at the global LoRA tier.

## What we know from the spec

- Brief 127 specifies procedural memory as signed skill gseeds at `skill://<creator>/<name>/<version>`.
- Brief 119 (Round 6) specifies the four-cadence self-improvement loop, in which procedural promotion is the *creator-driven* analog of the daily/weekly/monthly model updates.
- Brief 052 (Round 2) ships the lineage-aware time machine that gives every skill a rollback path.

## Findings

1. **Promotion is a four-signal threshold, not a single number.** The four signals are: (a) *repetition count* — how many times the same workflow shape has been executed by this creator; (b) *acceptance ratio* — fraction of those executions the creator did not roll back; (c) *grounding ratio* — fraction of resulting claims that cleared the Brief 097 grounding floor; (d) *constitutional pass rate* — fraction that cleared the Round 4 constitutional fence. All four must clear individual minima; the composite promotes.

2. **Default minima:** repetition ≥3, acceptance ≥0.8, grounding ≥0.85, constitutional 1.0 (no exceptions). These are conservative; the daily LoRA cadence (Brief 132) tunes them per-creator over time.

3. **Repetition count is "shape-equivalent," not "byte-equivalent."** Two workflows are shape-equivalent if their modifier-surface DSL operator chains are isomorphic (same operators, same dependency edges, possibly different parameter values). This means a creator who runs "generate sprite, recolor, resize" three times with three different sprites still gets a promotion candidate.

4. **Promotion requires creator consent.** Per Brief 105, no signed gseed is created on a creator's identity without explicit consent. The threshold-clearing event triggers a "promote this workflow as a skill?" prompt in Studio (Brief 048). The creator can name it, parameterize it, or dismiss it. Dismissed candidates are *not* re-prompted for the same shape for 30 days.

5. **Auto-promotion is opt-in per creator.** A creator can enable "auto-promote workflows that clear all four minima" in their preferences. Auto-promoted skills are still signed and rollback-able. This is the high-velocity power-user mode.

6. **The promoted skill carries its provenance.** The new skill gseed's lineage points to every contributing trace. If any contributing trace is later rolled back (e.g., a constitutional violation surfaces post-hoc), the skill is auto-flagged for re-review.

7. **Federation publishing has a higher bar.** A creator-private skill needs only the four minima. A federation-published skill (Brief 100) additionally requires: repetition ≥10, drawn from ≥2 distinct namespaces (cross-namespace stability), and creator-signed acknowledgement of public release. This higher bar is what protects the federation graph from noise.

8. **Threshold parameters are themselves signed.** The default minima live in `config://gspl/promotion-thresholds/v1`. Adjustments are signed config updates with rollback. Creators who tune their local thresholds produce a signed override gseed.

9. **Negative promotions exist.** If a workflow shape repeatedly fails (acceptance <0.3 over 5+ executions), the kernel produces a "anti-skill" gseed: a signed warning attached to the workflow shape that the router uses to *avoid* re-executing the same shape. This is operationally cheap and enormously valuable.

10. **Cross-creator promotion paths are mediated.** A creator cannot directly promote another creator's traces. But Brief 100's federation peer protocol allows a creator to *fork* a peer's promoted skill (with attribution) into their own namespace. This is the substrate-native version of "starring a repo."

## Risks identified

- **Repetition threshold is gameable.** A creator could artificially run the same workflow 3 times to trigger promotion. Mitigation: this is fine — the resulting skill is signed by that creator and only meaningful to them; federation publishing has a higher bar.
- **Shape-equivalence definition is fuzzy.** Two operators with the same name but different semantic intent could be wrongly treated as equivalent. Mitigation: shape equivalence is computed on the canonicalized DSL chain, which carries operator versions and types.
- **Studio prompts get annoying.** A creator who runs many similar workflows could see frequent promotion prompts. Mitigation: 30-day dismissal cooldown per shape; prompt frequency is itself capped at 1/hour.

## Recommendation

**Implement procedural promotion as a four-signal threshold (repetition ≥3, acceptance ≥0.8, grounding ≥0.85, constitutional 1.0) with shape-equivalence on canonical DSL chains. Promotion requires explicit creator consent via Studio prompt; opt-in auto-promotion mode for power users. Federation publishing requires higher minima (repetition ≥10, ≥2 namespaces, explicit release acknowledgement). Negative-promotion (anti-skill) gseeds catch repeatedly failing workflow shapes. Threshold parameters are signed config gseeds with rollback. Daily LoRA cadence tunes per-creator threshold offsets after 30 days of telemetry.**

## Confidence

**4/5.** The four-signal model is conservative and falls naturally out of the substrate. The unknowns are: (a) how aggressively to tune per-creator after telemetry, and (b) whether the 30-day dismissal cooldown is the right number. Both are decidable in Round 7.

## Spec impact

- `gspl-reference/intelligence/procedural-promotion.md` — new file documenting the four-signal threshold, shape-equivalence definition, federation higher-bar, anti-skill mechanism.
- `gspl-reference/research/127-gspl-memory-and-context.md` — cross-reference at the procedural memory section.
- `gspl-reference/research/100-federation-peer-protocol-details.md` — cross-reference at the cross-creator forking line.

## New inventions

- **INV-570** — *Four-signal procedural promotion threshold.* Repetition + acceptance + grounding + constitutional, all gating, with shape-equivalence on the canonicalized DSL chain.
- **INV-571** — *Anti-skill negative-promotion gseed.* A signed warning attached to a repeatedly-failing workflow shape that the router uses to avoid re-execution. Failure as a first-class learning signal.
- **INV-572** — *Federation higher-bar publishing minima.* Cross-creator skill publishing requires more evidence than private promotion, protecting the federation graph from noise without blocking creator-local productivity.

## Open follow-ups

- Per-creator threshold offset tuning (Round 7 telemetry).
- Cross-namespace stability metric exact formula (placeholder is "≥2 namespaces").
- Studio prompt UX details (defer to Brief 103).

## Sources

1. Brief 052 — Lineage-aware time machine.
2. Brief 100 — Federation peer protocol.
3. Brief 105 — Launch criteria and scaling plan (rollback primitive).
4. Brief 127 — GSPL memory and context.
5. Brief 119 — Self-improvement loops.
