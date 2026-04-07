# 144 — Drift detector threshold calibration

## Question

What metrics, thresholds, and rollback triggers should the continuous drift detector (Brief 129) use to catch a regressing weekly LoRA, monthly verifier, or daily router *before* a creator notices?

## Why it matters (blast radius)

Brief 129 promises continuous drift detection with auto-rollback. Without concrete thresholds, the detector either fires too eagerly (constant rollbacks, churn-induced creator distrust) or too rarely (regressions ship to creators, brand damage). This is the safety net under every self-improvement cycle. It must be empirically grounded and conservative by default.

## What we know from the spec

- Brief 129 specifies a continuous drift detector with auto-rollback.
- Brief 134 specifies the canonical eval battery with eight families, each with its own pass criterion.
- No prior brief calibrates the actual thresholds.

## Findings

1. **Drift is measured against the held-out 20% slice from the canonical battery (Brief 134).** Each new model artifact (router, reranker, verifier, action adapter, base LoRA) is evaluated on the held-out slice immediately on promotion. The held-out slice is by construction *not* in the training data, so a regression there is real, not overfitting noise.

2. **Three metric classes per artifact: quality, calibration, latency.**
   - *Quality:* the artifact-specific primary metric (macro-F1 for router, BEIR nDCG@10 for reranker, Spearman ρ for verifier value head, etc.).
   - *Calibration:* expected calibration error (ECE) on the artifact's confidence outputs.
   - *Latency:* p99 latency on the floor hardware.

3. **Promotion threshold formula: `must_match_or_beat_previous_version_within_2σ`.** Where σ is the historical standard deviation of the metric across the previous 8 versions of that artifact. This adapts the threshold to the natural noise floor of each metric — a noisy metric gets a wider band, a stable metric gets a tighter one.

4. **Hard floors override the relative formula.** Each artifact has an absolute floor:
   - Router: macro-F1 ≥0.85, ECE ≤0.05, p99 ≤80ms.
   - Reranker: BEIR avg ≥95% of teacher, federation nDCG@10 ≥0.85, p99 ≤200ms.
   - Verifier: Spearman ρ ≥0.7, p99 ≤200ms.
   - Action adapter: Spearman ρ ≥0.7, zero new fence violations.
   - Base LoRA: canonical battery 8/8 families pass, p99 inference latency ≤previous-version × 1.05.

   A new artifact must clear *both* the relative formula *and* the hard floor. Failure on either triggers auto-rollback.

5. **Detection cadence: per-promotion + continuous.** Per-promotion check is the gating event. Continuous detection runs every hour during normal kernel operation: a small (~50 example) probe set is run, and if accuracy drops more than 5 points relative to the post-promotion measurement, an alert fires and the system enters "graceful degradation" mode (next inference falls back to the previous artifact version while the alert is investigated).

6. **The continuous probe set is creator-local and signed.** It is sampled from the creator's recent successful interactions, anonymized, and stored in `drift-probe://<creator>/v1`. Each creator has their own probes, so drift is detected against the creator's actual usage pattern.

7. **Two failure modes: silent drift and catastrophic drift.** Silent drift is a small, slow degradation across many metrics — caught by the relative formula. Catastrophic drift is a single hard-floor violation — caught immediately. Both trigger rollback; only catastrophic enters degradation mode immediately.

8. **Rollback is to the last *promoted* version, not the last *trained* version.** Some training runs never promote (because they fail the gate); rollback skips them and goes to the most recent gated-and-promoted artifact.

9. **Rollback events are signed and visible.** Every auto-rollback creates a `rollback-event://<artifact>/<from-version>/<to-version>` gseed visible in the council review (Brief 107) and in the improvement log (`improvement-log://`).

10. **Rate limit on rollbacks per artifact: 1 per 24 hours.** If two rollbacks fire on the same artifact within 24 hours, the artifact is *frozen*: no further promotions until a council review (Brief 107). This prevents oscillation and forces human attention on persistent regression sources.

11. **Calibration tables for each metric** (initial v0.1 thresholds, all tunable post-launch):

    | Artifact | Primary | Floor | Relative band |
    |---|---|---|---|
    | Router | macro-F1 | 0.85 | within 2σ |
    | Router | ECE | 0.05 | absolute floor only |
    | Reranker | BEIR avg | 95% teacher | within 1σ |
    | Verifier | Spearman ρ | 0.70 | within 2σ |
    | Action adapter | Spearman ρ | 0.70 | within 2σ |
    | Base LoRA | battery families | 8/8 pass | absolute floor only |
    | Eval battery | per-family pass | 100% | absolute floor only |

## Risks identified

- **σ is undefined for the first ~8 versions.** Mitigation: until 8 versions exist, fall back to absolute floors only; the relative formula activates from version 9 onward.
- **Continuous probe set drift.** As creators' usage patterns shift, the probe set may stop being representative. Mitigation: probe set is re-sampled monthly from the most recent month's interactions, with a 6-month rolling window.
- **Council review queue saturation.** If many artifacts get frozen, council can't review fast enough. Mitigation: rate limit rollbacks at 1/24h per artifact (this brief); if council queue exceeds 5 frozen artifacts, the freeze policy escalates from "frozen" to "creator-opt-in" so blast radius is creator-controlled.

## Recommendation

**Implement the drift detector with three-metric-class evaluation (quality / calibration / latency) per artifact, using `within_2σ_of_previous_8_versions` as the relative formula plus per-artifact absolute floors. Detection runs at promotion gate + every hour on a creator-local probe set sampled from recent interactions. Auto-rollback to last promoted version on either-failure. Two failures within 24h freeze the artifact pending council review. Rollback events are signed gseeds and visible in `improvement-log://`. Calibration table from finding 11 ships as default v0.1 config; all thresholds are tunable via signed config gseeds.**

## Confidence

**4/5.** The thresholds are conservative defaults grounded in the eval battery design. They will need empirical tuning post-launch but the framework is sound. Unknown: how often the relative formula vs the absolute floors will be the binding constraint in practice.

## Spec impact

- `gspl-reference/intelligence/drift-detection.md` — new file with the metric classes, threshold formulas, calibration table, rollback rules, freeze protocol.
- `gspl-reference/research/129-gspl-self-improvement-loop.md` — cross-reference at the continuous drift detector line.
- `gspl-reference/research/107-governance-and-constitutional-amendment-process.md` — cross-reference at the council review queue.

## New inventions

- **INV-579** — *Two-channel drift detection (per-promotion + continuous hourly).* A regression is caught either at the moment of promotion or within an hour of going live, never later.
- **INV-580** — *Creator-local probe set for drift detection.* Each creator's probes are sampled from their own recent successful interactions, so drift is measured against the creator's actual usage rather than a generic benchmark.
- **INV-581** — *Freeze-after-two-rollbacks protocol.* A persistently regressing artifact is frozen and escalated to council, preventing oscillation and forcing human attention.

## Open follow-ups

- Empirical tuning of the 2σ window post-launch.
- Whether to publish anonymized aggregate drift events as a public dashboard for creator transparency.
- How to handle drift in artifacts that have very low version cadence (e.g., quarterly verifier).

## Sources

1. Brief 107 — Governance and constitutional amendment process.
2. Brief 129 — GSPL self-improvement loop.
3. Brief 134 — Substrate-native benchmark battery.
4. Lipton et al., *Detecting and Correcting for Label Shift*, ICML 2018 (drift detection patterns).
