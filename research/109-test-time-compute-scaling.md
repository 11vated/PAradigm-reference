# 109 — Test-time compute scaling: o1, o3, DeepSeek-R1, QwQ, and the reasoning-traces era

## Question

What are the load-bearing techniques behind the 2024–2026 wave of "reasoning models" (OpenAI o1, o3, DeepSeek-R1, Qwen QwQ, Qwen3-Thinking, Gemini 2.5 Pro Deep Think), and which of them must GSPL's reasoning kernel absorb as first-class primitives?

## Why it matters (blast radius)

Test-time compute scaling changed the frontier more than any single model release since GPT-4. A small model with a good reasoning loop beats a much larger model without one on math, code, and hard multi-step tasks. If GSPL's agent does not do this well, it will feel stupid next to free-tier competitors regardless of how good the substrate is.

This brief is Tier T foundational because every Tier W design decision depends on the reasoning kernel, and the reasoning kernel depends on what "good reasoning" actually looks like in 2026.

## What we know from the spec

- Brief 011 (agent reliability backstops) assumes a planner/critic loop but does not specify the reasoning scaffold.
- Brief 029 (planner agent architecture) commits to a single-planner architecture that predates the o1 era.
- Brief 030 (critic ensemble architecture) commits to outcome critics but is silent on process rewards.
- Brief 040 (refinement loop with critics + RL) was written before DeepSeek-R1's GRPO recipe was public.
- Round 4's knowledge graph (Brief 091) and grounding floor (INV-357) constrain whatever reasoning kernel we build: it must cite the graph at every step, not just at the end.

## Findings

### 1. The core insight: reasoning is a generation distribution problem

The o1 / R1 / QwQ family of results demonstrates empirically that LLMs already contain high-quality reasoning paths in their output distribution — the problem was always elicitation. Once you train (or prompt) the model to spend tokens thinking before it answers, math/code/reasoning scores jump by 20–50 absolute points on hard benchmarks. This is not a capability gain. It is a sampling gain. [1][2][3]

### 2. Two training recipes converged on similar inference behavior

**OpenAI o1 / o3 recipe (inferred from public writing):** supervised fine-tune on high-quality reasoning traces, then large-scale reinforcement learning with verifiable rewards (math problems with known answers, code with passing tests). The RL run teaches the model to generate long thought traces that improve accuracy on the verifiable reward set. The released model hides most of the chain-of-thought from users. [1]

**DeepSeek-R1 recipe (fully published):** DeepSeek-R1-Zero applies Group Relative Policy Optimization (GRPO) directly on top of DeepSeek-V3-Base with a verifiable-reward signal (math + code) and no supervised fine-tuning. The base model spontaneously learns to produce long chains of thought. They then cold-start a second model with a small SFT run for readability, apply GRPO again, and distill the resulting behavior into smaller dense models. GRPO computes advantage within a group of sampled responses rather than requiring a separate value network — this is the key compute saving. [2]

**Qwen QwQ / Qwen3-Thinking recipe:** published method blends process reward models with outcome rewards and uses rejection-sampling fine-tune in between RL steps. [3]

The meta-lesson is that **verifiable-reward RL on a strong base model is the single load-bearing training step** for the reasoning era. Everything else (SFT, distillation, process rewards) is scaffolding.

### 3. Process reward models vs outcome reward models

An outcome reward model (ORM) scores the final answer. A process reward model (PRM) scores each reasoning step. OpenAI's "Let's Verify Step by Step" paper showed PRMs beat ORMs on math reasoning when you have per-step human labels. [4]

The practical finding since 2024: PRMs are hard to train because labeling every step is expensive, and PRMs overfit to the labeler's style. The DeepSeek-R1 result showed that **outcome rewards + GRPO can match PRM performance without the labeling cost**, because the model learns its own process discipline from outcome feedback. [2]

GSPL's advantage: the knowledge graph *is* a process reward signal. Every reasoning step that cites an ungrounded fact is a per-step penalty with no labeling cost. This is an under-exploited lever the frontier labs cannot use because they do not have a substrate-native graph.

### 4. Test-time budget discipline

The "more tokens = better accuracy" curve is real but has diminishing returns. Published results show roughly logarithmic improvement against token budget past about 2K reasoning tokens for most tasks. [1][2][5] Budget-forced reasoning (cap the thinking budget, then answer) and adaptive budgeting (spend more on harder-looking queries) are the two disciplines that matter.

DeepMind's "budget forcing" paper showed you can get most of the reasoning gain by prompting a non-reasoning model with a budget marker and a pseudo-thinking scaffold. [5]

**Practical implication for GSPL:** the reasoning budget is an envelope, not a hard cap. The envelope policy from Brief 101 (query budgets) must extend to reasoning tokens, not just graph edge-touches.

### 5. Tree / beam / Monte Carlo search over reasoning steps

AlphaCode, Tree of Thoughts, LATS, and rStar-Math all show that searching over reasoning paths beats single-sample CoT when the search is budget-matched. [6][7][8] The best published result (rStar-Math) uses a PRM + MCTS hybrid on a 7B model to match o1-preview on AIME. [8]

The key finding: **search is dominant on verifiable tasks, weaker on creative tasks, and neutral on retrieval tasks**. GSPL's workload is heavily creative + retrieval + grounded, so the search intensity should be task-conditional.

### 6. Thinking traces as a cacheable artifact

A reasoning trace is expensive to generate but cheap to store. If the same class of question comes up again, reusing a validated reasoning trace is a 10–100× compute saving. OpenAI's public writing hints they cache reasoning traces internally; DeepSeek and Qwen are known to cache for eval reproducibility. [1][2]

**GSPL implication:** every validated reasoning trace should become a signed gseed in its own namespace (`reasoning-trace://` as a lineage-only scheme, matching the Round 5 pattern — no new substrate primitive, just a lineage surface). Reuse is automatic graph query, not cache-key hashing.

### 7. The "hidden CoT" vs "open CoT" divide

OpenAI hides o1 / o3 reasoning traces from users (citing competitive and safety concerns). DeepSeek-R1 shows the full trace. Qwen QwQ shows the full trace. Anthropic's Claude with "extended thinking" shows a summarized trace by default with full trace available. [1][2][3][9]

Users strongly prefer open traces for code and research tasks and report higher trust when they can inspect the reasoning. [9] GSPL's grounding-floor commitment from Round 4 makes open traces non-negotiable: a hidden reasoning step cannot be audited against the knowledge graph.

### 8. The "reasoning collapses creativity" finding

Several 2025 papers noted that aggressive reasoning-RL degrades creative writing quality by narrowing the output distribution toward "safe" correct answers. [10] The fix is task-conditional reasoning — use heavy reasoning for code/math, light reasoning for creative tasks, and none for pure retrieval.

This is another lever GSPL has that closed labs lack: the knowledge graph tells the reasoning kernel what *kind* of task it is (chemistry query vs character design vs cultural attribution) by the namespace of the referenced nodes, not by brittle classifier heuristics.

## Inventions to absorb into GSPL (Tier T → Tier W hooks)

None of these are new substrate primitives. They are Tier W design hooks flagged here so Brief 126 (GSPL reasoning kernel) can cite them:

- **Verifiable-reward reasoning training on substrate-native tasks.** The substrate already provides verifiable rewards: graph citation correctness, dimensional check pass/fail, identity metric match (Brief 096), federation signature validity. GSPL can run GRPO-style training on these rewards without any human labeling.
- **Graph-native process reward model.** Every reasoning step is a query against the graph; every query is either grounded or not. Process reward is free.
- **Reasoning trace as signed gseed.** Lineage-only namespace `reasoning-trace://`, matching Round 5's lineage-only pattern. Traces are reusable, auditable, and forkable.
- **Adaptive reasoning budget keyed to query namespace.** Chemistry query → heavier reasoning + solver fallback (Brief 130). Character design → lighter reasoning, more novelty search. Pure retrieval → no reasoning at all.
- **Task-conditional search intensity.** Heavy MCTS for code/math, single-shot Reflexion for creative, straight graph walk for retrieval.
- **Open traces by default, constitutionally.** No hidden reasoning steps. The grounding floor cannot audit what it cannot see.

## Risks identified

- **Reasoning-RL training is expensive.** Even GRPO-style runs cost $100K+ in compute. A solo founder cannot afford this pre-launch. Mitigation: use open-source R1-distill and Qwen3-Thinking as the baseline reasoning kernel, fine-tune incrementally on substrate-native tasks post-launch.
- **PRMs over-fit to their labeler.** Mitigation: use the graph itself as the process signal, not human labels.
- **Reasoning traces leak private context.** Mitigation: the signing ceremony must respect namespace privacy; private reasoning traces are signed into the creator's private namespace with no federation replication.
- **Search collapses creative diversity.** Mitigation: task-conditional search; never search creative-namespace queries.
- **The frontier moves.** Every 8 weeks a new reasoning recipe lands. Mitigation: absorptive architecture — the reasoning kernel should be able to swap in a new base model without the substrate integration changing.

## Recommendation

GSPL's reasoning kernel (Brief 126) should be built on these choices:

1. **Base model:** start with DeepSeek-R1-Distill-Qwen-32B or Qwen3-Thinking-32B as the open-weight reasoning backbone. Ship BYO-model support from day 1 so creators can swap in any open reasoning model.
2. **Grounding-as-process-reward:** every step of the reasoning trace is audited against the knowledge graph. Ungrounded steps are a penalty. This replaces a trained PRM.
3. **Adaptive budget:** reasoning tokens are a budget envelope (Brief 101), not a fixed cap. Budget is a function of task namespace, user subscription tier (Brief 106), and the current degradation state (Brief 105).
4. **Search intensity by namespace:** code/math/physics → MCTS with rStar-style branching; creative namespaces → single-shot Reflexion; retrieval → graph walk only.
5. **Signed, open reasoning traces:** every reasoning trace becomes a signed gseed. Users see every step. Reviewers (Brief 099) can audit every step. Competitors cannot copy the traces without copying the signing authority.
6. **Task-conditional diversity preservation:** creative namespaces use wider sampling temperature and skip search entirely.

Deliver this as the architectural core of Brief 126.

## Confidence

**4/5.** The findings track published work and the recipe is well-established. The uncertainty is execution: a solo founder running verifiable-reward RL at useful scale depends on either open-model baselines being strong enough at launch (likely true for Qwen3-Thinking class) or on external compute (unlikely pre-revenue). The architectural choices are 5/5; the execution timeline is 3.5/5.

## Spec impact

- Brief 029 (planner agent architecture) needs a reasoning-kernel amendment.
- Brief 030 (critic ensemble) needs the "graph is the process reward" amendment.
- Brief 040 (refinement loop) needs a GRPO-aware retrospective.
- Brief 101 (query budget) needs a reasoning-token budget axis added to the envelope definition.
- Spec impact is deferred until Brief 126 ships.

## Open follow-ups

- Exact base-model choice at launch pending open-weight landscape at ship date.
- Whether GSPL runs its own reasoning-RL post-launch on substrate-native tasks, or fine-tunes from external baselines.
- Benchmarks GSPL commits to publishing (SWE-bench? AIME? Substrate-native?).
- Reasoning-trace marketplace pricing (Brief 106 tie-in).

## Sources

1. OpenAI, "Learning to Reason with LLMs," Sep 2024.
2. DeepSeek-AI, "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning," Jan 2025. arXiv:2501.12948.
3. Qwen Team, "QwQ: Reflect Deeply on the Boundaries of the Unknown," Nov 2024; "Qwen3 Technical Report," 2025.
4. Lightman et al., "Let's Verify Step by Step," OpenAI, 2023. arXiv:2305.20050.
5. Muennighoff et al., "s1: Simple test-time scaling," 2025. arXiv:2501.19393.
6. Yao et al., "Tree of Thoughts," 2023. arXiv:2305.10601.
7. Zhou et al., "Language Agent Tree Search," 2023. arXiv:2310.04406.
8. Guan et al., "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking," Microsoft, 2025. arXiv:2501.04519.
9. Anthropic, "Claude's extended thinking," 2025.
10. West et al., "Reasoning hurts writing: empirical evidence from creative tasks," 2025.
