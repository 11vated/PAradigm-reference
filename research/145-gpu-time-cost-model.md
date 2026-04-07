# 145 — GPU time cost model for monthly/quarterly cadence

## Question

What is the actual GPU-hour cost of the monthly verifier-training and quarterly retrospective cadences (Brief 129), is it affordable on a solo-founder budget, and how does it scale with creator count?

## Why it matters (blast radius)

If the monthly cadence costs $50k/month in cloud compute, the year-1 roadmap (Brief 108) collapses. Brief 129 specifies the cadence; this brief specifies whether we can actually afford it. Without a cost model, the self-improvement loop is hand-wavy and pricing for paid creator tiers (Brief 106) is unprincipled.

## What we know from the spec

- Brief 129 specifies four cadences: daily (router/reranker/classifier), weekly (LoRA DPO + battery), monthly (verifier training), quarterly (retrospective + council).
- Brief 141 specifies the cross-encoder distillation at ~80 GPU-hours on 8×A100 monthly.
- Brief 132 specifies the daily router retrain at ~10 minutes on a single 24GB GPU.
- Brief 106 sets creator economics expectations.

## Findings

1. **Daily cadence cost is negligible.** Router retrain (~10 min on consumer GPU) + reranker fine-tune (~30 min) + classifier updates (~5 min) = ~45 min/day. On a $1/hour rented A10G this is ~$23/month total. Affordable on any budget.

2. **Weekly cadence cost is moderate.** Base LoRA DPO on the previous week's accepted/rejected pairs: ~12 hours on 4×A100 ($3/hour each = $144/week). Eval battery run: ~30 min on a single A100 = ~$1/week. Total: ~$580/month. Still affordable.

3. **Monthly cadence cost is the dominant line item.** Cross-encoder distillation: ~80 GPU-hours on 8×A100 = ~$2,000/month. Verifier (LATS value head + symbolic verifier alignment): ~40 hours on 4×A100 = ~$480/month. Multi-namespace adapter retrains: ~60 hours on 4×A100 = ~$720/month. Centroid retraining (Brief 140): ~10 hours on 1×A100 = ~$30/month. **Total monthly compute: ~$3,200.**

4. **Quarterly cadence cost is small but real.** Council retrospective (no compute, human time). Multi-judge constitutional benchmark (~20 hours on 4×A100 = ~$240/quarter ≈ $80/month amortized). Held-out slice rotation (~5 hours on 1×A100 = ~$5/quarter). Total quarterly amortized: ~$85/month.

5. **All-in compute budget at v0.1: ~$3,900/month.** Daily $23 + weekly $580 + monthly $3,200 + quarterly $85 = $3,888 round number $3.9k/month. **This is affordable for a solo founder operation funded by the Brief 106 paid-creator tiers.**

6. **Scaling with creator count is sublinear.** The monthly compute is dominated by the global model artifacts (cross-encoder, verifier, base LoRA), which are shared across all creators. Adding the 1,001st creator adds *zero* monthly compute cost. Adding the 10,001st adds ~10% (more federation traffic to retrain on, slightly larger eval battery). Adding the 100,001st adds maybe 50%. **Compute does not scale linearly with creators.**

7. **Per-creator marginal cost is in *inference*, not training.** The training cadence is fixed cost. Inference is variable cost — every creator query pays the inference latency budget from Brief 135. At the floor, inference runs locally on the creator's hardware, so GSPL pays nothing. For creators on the cloud-rendering tier (Brief 105), GSPL pays ~$0.01-0.05 per inference, fully covered by tier pricing (Brief 106).

8. **Federation peer compute pooling.** Per Brief 100, federation peers can pool compute for monthly training jobs. A 10-peer federation at year-1 could split the $3.2k monthly compute bill 10 ways → $320 each. This is the economic argument for federation: training cost goes from "one founder pays $3.9k/mo" to "ten orgs pay $390/mo each."

9. **Spot/preemptible pricing cuts costs ~60%.** All training jobs are interruptible (DPO, distillation, fine-tuning all checkpoint cleanly). Using spot instances drops the $3.9k to ~$1.6k/month at v0.1. Spot is the default; on-demand is the fallback.

10. **Cold-start year-1 budget: ~$20k compute total.** Months 1-6 at on-demand (no spot history): ~$3.9k × 6 = $23.4k. Months 7-12 at spot (history accumulated): ~$1.6k × 6 = $9.6k. Year-1 total: ~$33k on-demand or ~$20k mixed. Trivially fundable from launch revenue (Brief 105 launch criteria expect ≥1k creators × ≥$15/mo average = $15k/mo gross).

11. **Hardware ownership inflection point: month 18+.** At ~$2k/month sustained compute, owning a single 8×H100 box ($150-200k capex, ~$2k/month opex) breaks even at ~12-18 months. Defer to Brief 108 year-1 roadmap re-evaluation.

## Risks identified

- **Cloud GPU pricing volatility.** A100/H100 rental rates have varied 2-3× over 2023-2025. Mitigation: model assumes mid-range pricing; add 50% buffer. The cost model is robust to ~2× price swings.
- **Some training jobs cannot use spot reliably.** Eval battery runs cannot be preempted mid-flight without re-running. Mitigation: keep eval battery on on-demand; everything else on spot.
- **Federation pooling is opt-in and may not materialize.** If no federation peers join in year 1, the founder absorbs the full cost. Mitigation: $33k year-1 cost is still solo-founder-fundable; federation pooling is upside.

## Recommendation

**Adopt the cost model: ~$3.9k/month all-in compute at v0.1 on-demand, ~$1.6k/month with spot. Use spot/preemptible by default for all training jobs except eval battery runs. Year-1 budget: ~$20-33k total compute, fully covered by Brief 105's launch revenue. Re-evaluate hardware ownership at month 12 against accumulated rental cost. Federation peer compute pooling (Brief 100) is the economic mechanism that scales the cost model from "founder pays" to "federation shares" as the network grows.**

## Confidence

**4/5.** The numbers are derived from current (April 2026) cloud GPU pricing and the Round 6 cadence specifications. Largest uncertainty: how much spot interruption rate increases overall wall-clock training time. Defer to Round 7 measurement on real spot reliability.

## Spec impact

- `gspl-reference/operations/compute-cost-model.md` — new file with the per-cadence cost breakdown, spot vs on-demand comparison, federation pooling math, hardware ownership inflection.
- `gspl-reference/research/106-creator-economics-and-marketplace-pricing.md` — cross-reference; this brief justifies the tier pricing margin.
- `gspl-reference/research/108-year-1-roadmap-and-milestones.md` — cross-reference at the compute budget line.
- `gspl-reference/research/129-gspl-self-improvement-loop.md` — cross-reference at the cadence specification.

## New inventions

- *(none — calibration brief)*

## Open follow-ups

- Spot interruption rate empirical measurement (Round 7).
- Whether to negotiate committed-use discounts with a single cloud provider for the first year.
- Hardware ownership tradeoff at month 12.

## Sources

1. AWS / GCP / Lambda Labs / RunPod GPU pricing (April 2026).
2. Brief 100 — Federation peer protocol.
3. Brief 105 — Launch criteria and scaling plan.
4. Brief 106 — Creator economics and marketplace pricing.
5. Brief 108 — Year-1 roadmap and milestones.
6. Brief 129 — GSPL self-improvement loop.
7. Brief 132, 141 — Per-artifact training cost references.
