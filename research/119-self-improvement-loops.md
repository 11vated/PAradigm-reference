# 119 — Self-improvement loops: STaR, Quiet-STaR, V-STaR, SPIN, rStar-Math, self-rewarding, weak-to-strong

## Question

What self-improvement loop does GSPL run on its own substrate data, and how does the constitutional layer prevent drift?

## Why it matters (blast radius)

Self-improvement is where platforms compound. A system that gets measurably better every week from its own usage dominates a system that requires a new base model to improve. GSPL has two native improvement signals no closed lab has: the knowledge graph (ground-truth for reasoning steps) and the federation (signed creator actions). The question is how to turn these into training signal safely.

## What we know from the spec

- Brief 040 (refinement loop with critics + RL) commits to an RL loop.
- Brief 113 (constitutional AI / alignment) commits to iterative IPO on AI-judged pairs.
- Brief 109 commits to verifiable-reward training from substrate tasks.

## Findings

### 1. STaR: Self-Taught Reasoner

Zelikman et al. (2022). Generate rationales for problems, keep the rationales that produce correct answers, fine-tune on those. Bootstrap reasoning from a base model's own outputs. [1]

Strong result: small models get large reasoning gains from their own correct-rationale outputs, no human labels needed.

### 2. Quiet-STaR

Zelikman et al. (2024). STaR applied to arbitrary tokens, not just reasoning: the model learns to "think before each token" with silent thought tokens, rewarded by downstream prediction improvement. [2]

### 3. V-STaR (Verification STaR)

Hosseini et al. (2024). Trains both a generator and a verifier from STaR-style self-generated data. The verifier then gates which self-generated examples make it into training. Cleaner bootstrap. [3]

### 4. SPIN: Self-Play Fine-Tuning

Chen et al. (2024). Iterative fine-tuning where the model plays against its own previous checkpoint — the earlier checkpoint generates "negative" examples, the new checkpoint learns to beat them. Related to DPO but with self-generated negatives. [4]

### 5. rStar-Math

Microsoft (2025). Combines MCTS + process reward models + self-evolved training data. A small model matches o1-preview on AIME through iterated self-generated training traces. The loop: generate traces via MCTS, filter by verifier, train, repeat. [5]

### 6. Self-Rewarding Language Models

Yuan et al. (2024). The model acts as both generator and judge, and the judging ability improves alongside the generation ability. Demonstrated compounding improvements across iterations. [6]

### 7. Weak-to-Strong Generalization

OpenAI (2023). A weaker teacher can supervise a stronger student and still produce reliable improvement. Matters for GSPL because we can bootstrap a strong model from a weaker judge + substrate ground truth. [7]

### 8. Iterative DPO / Online DPO

Round 113 already covered this. Every iteration is a small DPO run on fresh self-generated pairs. The federation provides fresh pairs continuously.

### 9. The drift failure mode

Every self-improvement loop faces drift: the model optimizes for its own judgment, which rewards patterns the judgment already liked. Over iterations the model narrows and loses diversity. Published mitigations:

- **External grounding signal** (the substrate graph in GSPL's case).
- **Held-out constitutional benchmark** (Brief 113).
- **Diverse judges** (multiple critics, not one).
- **Periodic reset to base model** for comparison.
- **Rollback discipline** (Brief 105).

### 10. The unique GSPL signal

No closed lab has these:

- **Graph-verified reasoning traces** are free positive examples.
- **Constitutional-violated outputs** are free negative examples.
- **Signed creator overrides** are free high-quality preference labels.
- **Signed forks** are free "this was useful" signals.
- **Refusals + overrides** are free alignment boundary labels.

A continuous improvement loop that consumes these signals and produces a new fine-tune adapter every cycle is a GSPL-native compounding lever no competitor can replicate.

### 11. Safe self-improvement requires constitutional fencing

The loop MUST:
- Never change the 13 constitutional commitments (Brief 107's non-amendable core).
- Never reduce grounding floor coverage.
- Never degrade refusal quality on constitutional categories.
- Pass a held-out benchmark before each checkpoint promotion.
- Be rollback-able at any step (Brief 105).

The loop MAY:
- Improve reasoning efficiency.
- Improve tool-use selection.
- Improve tone and clarity.
- Improve strategy routing decisions (Brief 115).
- Improve namespace-expert specialization.

### 12. Substrate-native improvement cycle shape

- **Daily:** harvest signed reasoning traces, signed overrides, signed forks. Update the cheapest layers (router, planner strategy selector, retrieval reranker).
- **Weekly:** iterative DPO pass on the week's preference data. LoRA adapter, rollback-able.
- **Monthly:** full verifier training on graph-audited traces. Promote if held-out benchmark passes.
- **Quarterly:** aligned with Brief 108's retrospective. Reset adapters if drift is detected; consult the council (Brief 107) on any constitutional concerns.

## Inventions to absorb

Tier W hooks for Brief 129:

- **Substrate as the only source of ground truth.** No outcome labels; only graph audits.
- **Signed federation actions as preference data.** Overrides, forks, and refusals are all free labels.
- **Constitutional fence on every improvement step.** The non-amendable core is the hard stop.
- **Held-out benchmarks per namespace.** Each substrate namespace has its own benchmark derived from the Foundation Kernel (Brief 095).
- **Rollback-by-default.** Every checkpoint is a signed gseed; promoting is explicit; rolling back is one operation (Brief 105).
- **LoRA adapters at every tier.** Weekly, monthly, quarterly adapters; full fine-tune is rare.
- **Daily → weekly → monthly → quarterly cadence.** Matches Brief 108 retrospective.
- **Consultancy review for any improvement touching sensitive namespaces.** Brief 099.
- **Public improvement log.** Every promotion is a signed public gseed (`improvement-log://`, lineage-only).

## Risks identified

- **Reward hacking on graph audit.** Mitigation: held-out audit, multi-judge ensemble, periodic human spot-check.
- **Diversity collapse.** Mitigation: creative-namespace checkpoints use separate diversity-preserving objectives (KTO with diversity regularization).
- **Consultancy bottleneck.** Mitigation: consultancy review is only for sensitive-namespace adapters; most adapters ship without it.
- **Rollback complexity.** Mitigation: every adapter is a signed gseed; rollback is a one-click operation in the governance UI.
- **Silent drift.** Mitigation: weekly regression on the constitutional benchmark; alarm + auto-rollback on regression.

## Recommendation

1. **Self-improvement is tiered by cadence.** Daily (retrieval/routing), weekly (LoRA DPO), monthly (verifier training), quarterly (retrospective).
2. **Substrate is the only ground truth.** No human outcome labels; graph audits + federation actions are sufficient.
3. **Constitutional fence is load-bearing.** Every promotion passes the held-out constitutional benchmark.
4. **Rollback-by-default.** Every adapter is signed; rollback is trivial.
5. **Consultancy review only for sensitive adapters.** Brief 099 budget is preserved.
6. **Public improvement log.** Every promotion is a signed public gseed.
7. **Council review at quarterly cadence.** Brief 107.

Feeds Brief 129 directly.

## Confidence

**4/5.** The individual techniques (STaR, iterative DPO, weak-to-strong) are well-published. The substrate-native improvement loop is novel but mechanically straightforward because the substrate produces the signal. Execution confidence is moderate because continuous improvement is operationally demanding for a solo founder — mitigation is strict rollback discipline and LoRA-only by default.

## Spec impact

- Brief 040 needs the substrate-as-signal amendment.
- Brief 105 needs the adapter rollback protocol.
- Brief 129 owns the integration.

## Open follow-ups

- Weekly/monthly adapter training budget (GPU-time cost model).
- Constitutional benchmark construction details.
- Public improvement log format.

## Sources

1. Zelikman et al., "STaR: Bootstrapping Reasoning with Reasoning," 2022.
2. Zelikman et al., "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking," 2024.
3. Hosseini et al., "V-STaR: Training Verifiers for Self-Taught Reasoners," 2024.
4. Chen et al., "Self-Play Fine-Tuning Converts Weak Language Models to Strong Language Models," 2024. arXiv:2401.01335.
5. Guan et al., "rStar-Math," Microsoft, 2025. arXiv:2501.04519.
6. Yuan et al., "Self-Rewarding Language Models," 2024. arXiv:2401.10020.
7. Burns et al., "Weak-to-Strong Generalization," OpenAI, 2023.
