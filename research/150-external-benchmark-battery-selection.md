# 150 — External benchmark battery selection

## Question

Which external benchmarks (SWE-bench Verified, LiveCodeBench, BFCL, MMLU-Pro, ARC-AGI, etc.) does v0.1 commit to running, and what are the target scores that justify the seven-axis competitive claim?

## Why it matters (blast radius)

The substrate-native canonical battery (Brief 134) measures the moat. External benchmarks measure parity. Without competitive scores on the benchmarks creators and the press already know, the seven-axis claim sounds like marketing. We need to declare which benchmarks v0.1 runs, what the targets are, and how the results are reported alongside the substrate-native scores. Picking the wrong external suite either embarrasses (we lose) or proves nothing (we win irrelevant benchmarks).

## What we know from the spec

- Brief 134 specifies the substrate-native canonical battery as the primary eval.
- Brief 122 selected Qwen3 family backbones, which have well-documented scores on most published benchmarks.
- No prior brief commits to a specific external suite.

## Findings

1. **Five external benchmarks cover the high-leverage axes.**
   - **SWE-bench Verified** — long-horizon code task completion. The gold standard for coding agents.
   - **LiveCodeBench** — held-out competitive programming problems. Measures coding ability without contamination.
   - **BFCL (Berkeley Function Calling Leaderboard)** — tool use accuracy. Direct measure of the action-space layer.
   - **MMLU-Pro** — broad knowledge with harder distractors than original MMLU. Measures backbone quality.
   - **ARC-AGI** — abstract reasoning. Measures generalization beyond training distribution.

2. **Each benchmark maps to one or more structural axes.**
   - SWE-bench Verified → Differentiable + Lineage-tracked (long-horizon multi-step)
   - LiveCodeBench → Typed + Confidence-bearing (constrained generation)
   - BFCL → Typed (grammar-enforced tool calls)
   - MMLU-Pro → Graph-structured (federation knowledge retrieval)
   - ARC-AGI → Confidence-bearing + Rollback-able (abstract planning with backtracking)

3. **v0.1 target scores (must clear or beat at launch):**

   | Benchmark | Backbone-only baseline | GSPL v0.1 target | Frontier ceiling (April 2026) |
   |---|---|---|---|
   | SWE-bench Verified | ~35% (Qwen3-14B) | ≥48% | ~71% (Claude Opus 4.6) |
   | LiveCodeBench | ~45% | ≥52% | ~67% |
   | BFCL avg | ~80% | ≥90% | ~93% |
   | MMLU-Pro | ~62% | ≥66% | ~78% |
   | ARC-AGI public | ~12% | ≥18% | ~55% |

   The targets are *substrate uplifts*: GSPL must provably add value over the bare backbone on every benchmark. We do not target the frontier ceiling at v0.1 — the floor hardware budget makes that impossible — but we target *measurable substrate uplift*.

4. **Substrate uplift is the primary v0.1 narrative.** "Qwen3-14B + GSPL > Qwen3-14B alone on every external benchmark" is a verifiable, defensible claim. It does NOT claim "GSPL beats Claude Opus 4.6"; it claims "GSPL makes any backbone better, and the better the backbone, the better the result." This claim scales naturally with v0.2's bigger backbones.

5. **BFCL is the most diagnostic for GSPL.** BFCL directly measures function-calling correctness, which is the typed-axis layer. A 10-point uplift on BFCL is the strongest single-benchmark validation of the seven-axis claim.

6. **SWE-bench Verified is the most marketable.** Press, creators, and investors recognize SWE-bench. A measurable substrate uplift on SWE-bench Verified is the press headline.

7. **ARC-AGI is the most ambitious and the most controversial.** ARC-AGI is hard for every system. A modest uplift (12% → 18%) is honest and impressive. We do NOT chase a leaderboard position; we report the uplift.

8. **MMLU-Pro tests the federation-graph retrieval claim.** MMLU-Pro questions often have grounded answers in the federation graph (Brief 091). The substrate uplift here measures whether GraphRAG-via-substrate is actually working.

9. **LiveCodeBench tests typed code generation.** Held-out problems with strict test cases. The xgrammar grammar enforcement (Brief 142) and constitutional fence (Round 4) should produce a measurable uplift.

10. **Reporting protocol: alongside, not instead of, the canonical battery.** Every release ships *both* the substrate-native canonical battery scores AND the external benchmark scores. The release notes lead with the canonical battery (the moat) and follow with external benchmarks (the parity). This is the dual-reporting commitment.

11. **Re-running cadence: monthly external benchmark sweep.** External benchmarks run monthly as part of the Brief 129 monthly cadence. Daily/weekly runs are prohibitively expensive; monthly catches regressions in time for the next release cycle.

12. **Contamination protection.** Per Brief 134, the held-out 20% of canonical battery rotates quarterly. External benchmarks have their own contamination protection (LiveCodeBench updates monthly; SWE-bench Verified is a fixed gold set; ARC-AGI public has held-out private).

## Risks identified

- **External benchmark contamination.** If the backbone has been pretrained on benchmark data, the baseline overstates. Mitigation: report uplift over the *same* contaminated baseline; relative claim is robust.
- **External benchmarks change over time.** SWE-bench versions evolve; LiveCodeBench updates monthly. Mitigation: pin a specific version per release; report the version number.
- **Missing benchmark for the rollback axis.** No external benchmark directly measures rollback-ability. Mitigation: this is part of the canonical battery's rollback family (Brief 134) and is acknowledged as substrate-native-only.

## Recommendation

**Adopt the five-benchmark external suite (SWE-bench Verified, LiveCodeBench, BFCL, MMLU-Pro, ARC-AGI) as the v0.1 external evaluation commitment. Target measurable substrate uplift on every benchmark over the bare backbone baseline, NOT frontier ceiling parity. Report results alongside the canonical battery (Brief 134) at every release with the canonical battery leading. Re-run monthly under Brief 129 cadence. Pin benchmark versions per release. The headline metric for press is SWE-bench Verified uplift; the headline metric for engineers is BFCL uplift. The v0.1 target scores in finding 3 are the floor; exceeding them is upside.**

## Confidence

**4/5.** The benchmark selection is grounded in current 2026 industry practice. The target scores are conservative substrate uplifts based on Qwen3-14B baselines and reasonable expectations of GSPL value-add. Largest uncertainty: actual uplift magnitude pre-launch — the first measurement happens in Round 7.

## Spec impact

- `gspl-reference/eval/external-benchmark-suite.md` — new file with the five benchmarks, target scores, dual-reporting protocol, monthly cadence, version pinning.
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — cross-reference; canonical battery and external suite are complementary.
- `gspl-reference/research/129-gspl-self-improvement-loop.md` — cross-reference; external sweep is monthly.

## New inventions

- **INV-590** — *Substrate-uplift reporting* over bare-backbone baseline as the v0.1 external benchmark posture, paired with dual-reporting (canonical battery first, external benchmarks second).

## Open follow-ups

- Whether to add HumanEval / MBPP as additional code benchmarks (probably no — LiveCodeBench is more contamination-resistant).
- Whether to add agent-specific benchmarks (AgentBench, GAIA) — defer to v0.2.
- Whether to publish the external sweep results as a public dashboard for creator transparency.

## Sources

1. Jimenez et al., *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*, ICLR 2024.
2. Princeton NLP, *SWE-bench Verified*, OpenAI 2024.
3. Jain et al., *LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code*, 2024.
4. UC Berkeley, *Berkeley Function Calling Leaderboard (BFCL)*, 2024.
5. Wang et al., *MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark*, 2024.
6. Chollet, *On the Measure of Intelligence (ARC)*, 2019; *ARC-AGI*, 2024.
7. Brief 122 — Qwen Code architecture teardown (Qwen3 baseline scores).
8. Brief 134 — Substrate-native benchmark battery.
