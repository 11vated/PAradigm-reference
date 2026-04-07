# 113 — Constitutional AI, RLAIF, DPO, IPO, KTO, and the post-RLHF alignment recipe

## Question

What alignment training recipe will keep GSPL's reasoning kernel honest to its grounding floor, its constitutional commitments, and its refusal envelope — without relying on RLHF with human labelers that a solo founder cannot afford?

## Why it matters (blast radius)

The 13 constitutional commitments from Round 4 and the grounding floor (INV-357) are the differentiating property of the whole platform. If the alignment recipe drifts — if the model starts hallucinating, refusing inconsistently, leaking copyrighted output, or eroding credit — the substrate promise collapses and so does trust. The wrong recipe can quietly degrade over time through naive fine-tuning.

Traditional RLHF requires tens of thousands of human preference labels. A solo founder cannot pay for that. The Round 6 question is: what post-RLHF recipes get us aligned without that cost, and which of them preserve the grounding floor?

## What we know from the spec

- Brief 011 (agent reliability backstops) assumes a critic loop but does not specify alignment training.
- Brief 030 (critic ensemble) specifies outcome critics, not constitutional critics.
- Round 4's 13 constitutional commitments are load-bearing and non-patchable.
- Round 5's consultancy network (Brief 099) provides a pool of lived-experience review but is budget-limited.

## Findings

### 1. RLHF is expensive and doesn't scale for small teams

Classic RLHF (InstructGPT, Llama 2 Chat): collect 30K–200K human preference comparisons, train a reward model, PPO against it. Total cost is in the millions of dollars and months of labeler operations. Not feasible for GSPL pre-launch. [1]

### 2. Constitutional AI (Anthropic)

Constitutional AI (Bai et al., 2022) replaces the "human preference" step with a "constitution": a list of principles the model uses to critique its own outputs. The recipe has two stages:

- **SL-CAI:** supervised fine-tune on model-generated critiques. The model writes a response, critiques it against the constitution, and rewrites. The rewritten pair is training data.
- **RL-CAI:** train a preference model on AI-labeled pairs ("which response better follows the constitution?") and run RL against it. This is RLAIF — Reinforcement Learning from AI Feedback. [2]

The output: a model aligned to the written constitution with minimal human labeling, and — crucially — with an auditable alignment target. You can read the constitution. This is exactly the property GSPL needs.

### 3. DPO: Direct Preference Optimization

Rafailov et al. (2023) showed that PPO-against-reward-model can be replaced with a closed-form loss on preference pairs, eliminating the need for a separately trained reward model. DPO is now the default for small-lab alignment. [3]

DPO strengths: simple, stable, low compute. Weaknesses: sensitive to the quality of preference pairs; can over-concentrate on the preferred distribution and lose diversity.

### 4. IPO (Identity Preference Optimization)

Azar et al. (2023) showed DPO can overfit when the preference labels are noisy. IPO regularizes by penalizing the log-ratio directly, preventing runaway exploitation of small preference margins. [4] IPO is the safer default for AI-labeled preferences (which are noisier than human).

### 5. KTO (Kahneman-Tversky Optimization)

Ethayarajh et al. (2024) replaced preference pairs with single-sided labels ("was this output good or bad?"), grounding the loss in prospect theory. KTO is more label-efficient when you can't afford to generate pairs. [5]

### 6. Rejection sampling fine-tune (RFT)

Generate many responses per prompt, pick the best by a critic (or a verifier for verifiable tasks), fine-tune on the winners. Simple, stable, widely used at Meta (Llama 2/3), Google, and in open-source (OpenChat, Zephyr). RFT pairs well with verifiable-reward tasks (Brief 109). [6]

### 7. Iterative and online DPO

The 2024–2025 consensus: run DPO in rounds. Train, sample, re-label with the new model or a judge, DPO again. Iterative DPO (Snorkel-Mistral, Zephyr, Nous) consistently beats single-shot DPO. Online DPO (Guo et al. 2024) makes this continuous. [7]

### 8. Process reward vs outcome reward in alignment

Same lesson as Brief 109: per-step process rewards beat single-outcome rewards on multi-step tasks but are labeling-expensive. The GSPL advantage reappears: the knowledge graph is a free process reward signal, and the 13 constitutional commitments are free constitutional checks. GSPL can train a constitutional process critic without paying for a single human label.

### 9. Weak-to-strong generalization

OpenAI's 2023 paper showed that a weak model can supervise a strong model and produce reliable alignment signal, at a cost to peak capability. For GSPL, this means the initial alignment pass can use a weaker judge model to bootstrap a stronger model. [8]

### 10. Character training (Claude)

Anthropic has published on character training: an additional post-DPO pass that shapes not just "is this helpful" but "does this sound like Claude." This pass is what makes Claude's tone consistent across millions of conversations. GSPL needs the analog: a character training pass that shapes the reasoning kernel to sound like **the grounding-floor voice** — humble about uncertainty, always-cites-sources, refuses-gracefully. [9]

### 11. Refusal quality is a learned skill, not a trained one

A poorly aligned model either refuses too much (useless) or too little (unsafe). The best published refusal recipe combines: (a) DPO on refusal-vs-compliance pairs, (b) a small constitutional self-critique loop at inference, (c) a refusal taxonomy the user can inspect. Brief 103's refusal explanation surface depends on the model actually producing *good* refusals, which requires trained refusal quality. [2][9]

### 12. Online / continuous alignment

Once deployed, models drift. OpenAI, Anthropic, and Meta all run continuous retraining cycles that incorporate user feedback signals. For GSPL, the "user feedback signal" is the federation: when users override a refusal, edit a reasoning trace, or fork a seed, those actions become alignment signal. This is a GSPL-native continuous alignment loop no closed lab can replicate because no closed lab has a signed substrate of creator actions. [10]

## Inventions to absorb

Tier W hooks for Brief 126 and Brief 129:

- **Constitutional AI as baseline alignment recipe.** The 13 constitutional commitments from Round 4 ARE the constitution. SL-CAI + RL-CAI pipeline bootstraps alignment with minimal human labeling.
- **DPO → IPO progression** depending on label noise. Use IPO when labels come from AI judges; use DPO when they come from consultancy reviewers.
- **Iterative DPO as the continuous loop.** Train, sample, re-judge, train.
- **RFT for verifiable tasks.** Math, code, chemistry, physics all have verifiable rewards. RFT is the cheap win.
- **Graph-as-process-critic.** Every reasoning step is audited against the graph; the audit result is training signal. No human labeler needed.
- **Constitutional commitments as inference-time critics.** At inference, a lightweight pass checks each response against the 13 commitments before emission. This is a safety net even if training drifts.
- **Character training for the grounding-floor voice.** GSPL's agent sounds like itself; it humble-cites, it refuses-gracefully, it explains-its-reasoning.
- **Federation as continuous alignment source.** Every override, fork, and edit in the federation is alignment signal. Substrate-native, lineage-tracked, free.
- **Consultancy network (Brief 099) is the high-trust label source** for the small number of places AI labels aren't enough (sacred content, mental health depictions, marginalized representation).

## Risks identified

- **RLAIF can embed the judge model's biases.** Mitigation: judges are diverse (not just one model); consultancy review for high-risk domains.
- **DPO overfits on small preference sets.** Mitigation: IPO with regularization; iterative re-labeling.
- **Inference-time constitutional critics add latency.** Mitigation: the critic is small and runs in parallel with generation; shares a budget line with reasoning tokens.
- **Continuous alignment can drift.** Mitigation: periodic regression runs against a held-out constitutional benchmark; rollback protocol from Brief 105.
- **Character training can feel forced.** Mitigation: character is a lightweight post-training pass with human-in-the-loop verification for tone.
- **Consultancy budget is finite.** Mitigation: consultancy is used only for domains where AI labels are insufficient; the rest is bootstrapped from the constitution.

## Recommendation

1. **Baseline recipe:** SL-CAI + iterative IPO using the 13 constitutional commitments as the explicit constitution. This is the cheap honest win.
2. **Verifiable-task training:** RFT on math, code, chemistry, physics, dimensional checks, graph-citation correctness. Free training signal.
3. **Process critic:** the knowledge graph is the process critic. Every reasoning step that cites an ungrounded fact is a penalty.
4. **Inference-time constitutional pass:** a lightweight 13-commitment check runs on every response. Costs a few hundred tokens. Included in the reasoning budget.
5. **Character training:** a small post-training pass to shape the grounding-floor voice (humble, citing, graceful refusal). Uses consultancy reviewers for tone calibration.
6. **Federation as continuous alignment source:** every signed override, fork, and edit feeds the next iterative DPO round. No user action is wasted signal.
7. **Consultancy network for high-risk domains:** sacred content, mental health, marginalized representation get human-in-the-loop labels; compensation is budgeted from Brief 099.
8. **Rollback discipline:** every alignment checkpoint is signed and reversible. Brief 105's rollback protocol applies.

This recipe is what Brief 126 uses.

## Confidence

**4/5.** Every technique cited has published support. The GSPL-specific wins (graph as process critic, federation as continuous alignment source) are novel but mechanically straightforward — they work because the substrate already produces the signal. Execution confidence is 4/5; architecture confidence is 4.5/5.

## Spec impact

- Brief 011 needs the constitutional-AI alignment recipe.
- Brief 030 needs the "critics include constitutional critics" addendum.
- Brief 099 needs a line item reserving consultancy budget for alignment labeling.
- Brief 126 owns the full integration.

## Open follow-ups

- Exact baseline model for the iterative IPO loop.
- Pre-launch consultancy-label budget allocation.
- Alignment regression benchmark construction.
- Whether GSPL's constitution becomes a public artifact (recommended: yes).

## Sources

1. Ouyang et al., "Training language models to follow instructions with human feedback," OpenAI, 2022. arXiv:2203.02155.
2. Bai et al., "Constitutional AI: Harmlessness from AI Feedback," Anthropic, 2022. arXiv:2212.08073.
3. Rafailov et al., "Direct Preference Optimization," Stanford, 2023. arXiv:2305.18290.
4. Azar et al., "A General Theoretical Paradigm to Understand Learning from Human Preferences," DeepMind, 2023. arXiv:2310.12036.
5. Ethayarajh et al., "KTO: Model Alignment as Prospect Theoretic Optimization," 2024. arXiv:2402.01306.
6. Dong et al., "RAFT: Reward rAnked FineTuning," 2023.
7. Guo et al., "Direct Language Model Alignment from Online AI Feedback," 2024. arXiv:2402.04792.
8. Burns et al., "Weak-to-Strong Generalization," OpenAI, 2023.
9. Anthropic, "Claude's Character," 2024.
10. Various industry reports, 2024–2026.
