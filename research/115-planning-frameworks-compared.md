# 115 — Planning frameworks compared: ReAct, Reflexion, ToT, GoT, LATS, CoV, Self-Consistency, Plan-and-Solve

## Question

Which planning frameworks should GSPL absorb as first-class primitives in its reasoning kernel, and which should it treat as special cases of a more general substrate-native planner?

## Why it matters (blast radius)

The agent's planning scaffold determines whether long tasks converge or spin. Every published framework has a niche where it dominates and a niche where it flounders. A naive pick locks GSPL into one niche. A principled composition gives GSPL the best of all of them.

## What we know from the spec

- Brief 029 (planner agent architecture) commits to a planner/critic pair without naming a framework.
- Brief 031 (refinement loop policy) commits to iterative refinement.
- Brief 040 (refinement loop with critics + RL) commits to RL on critic signal.

## Findings

### 1. ReAct: reason + act interleaving

Yao et al. (2022). The foundational pattern: interleave reasoning steps with tool calls. Model emits `Thought:` then `Action:` then `Observation:` in a loop. [1]

- **Strengths:** simple, robust, works with any tool-calling model, widely adopted, good for grounded tasks where observations anchor reasoning.
- **Weaknesses:** single-path — no backtracking, no search. Long horizons drift. No mechanism for self-critique between steps.

### 2. Reflexion: episodic self-critique with memory

Shinn et al. (2023). After a task attempt, the model writes a natural-language critique of its own trajectory and stores it in an episodic memory. The next attempt reads the critique. [2]

- **Strengths:** improves over multiple attempts; works well when the task can be retried; the critique is cheap and the memory is lightweight.
- **Weaknesses:** needs retriability; brittle when the critique is wrong (no verifier on the critique itself); struggles with tasks that cannot be sampled multiple times.

### 3. Self-Refine: single-session iterative refinement

Madaan et al. (2023). Generate, critique, refine, critique, refine... until stopping criterion. Single-session, no external memory. [3]

- **Strengths:** cheapest reflection variant; works on creative tasks where there is no verifier.
- **Weaknesses:** converges to local optima; can make the output *worse* if the critic is miscalibrated.

### 4. Tree of Thoughts (ToT)

Yao et al. (2023). The model expands a tree of thought branches, evaluates each with a value function, and performs BFS/DFS search. Dominates single-path CoT on Game of 24, crosswords, creative writing tasks. [4]

- **Strengths:** explicit search structure; good when the value function is reliable; strong on reasoning with clear branching.
- **Weaknesses:** value function is rarely reliable for open-ended tasks; expensive in tokens; the tree can explode.

### 5. Graph of Thoughts (GoT)

Besta et al. (2023). Generalizes ToT from tree to DAG, allowing thought-merging and back-references. [5]

- **Strengths:** richer than trees; can represent plans that revisit earlier ideas.
- **Weaknesses:** harder to implement correctly; the merging step is fragile; gains over ToT are task-dependent.

### 6. LATS: Language Agent Tree Search

Zhou et al. (2023). Combines MCTS with ReAct-style action emission. Each node in the search tree is a partial trajectory; rollouts extend trajectories; a learned value function guides search; backpropagation updates value estimates. [6]

- **Strengths:** the most principled search-based planning scaffold published; strong on code and reasoning benchmarks; MCTS is well-understood.
- **Weaknesses:** expensive; value function training is hard; overkill for short tasks.

### 7. Chain-of-Verification (CoV)

Dhuliawala et al. (2023). After generating an answer, the model generates verification questions, answers each, and uses the answers to revise. [7]

- **Strengths:** reliable correction of factual errors; works well on retrieval-grounded tasks.
- **Weaknesses:** does not help on creative or open-ended tasks; adds 2–4× token cost.

### 8. Self-Consistency

Wang et al. (2022). Sample multiple reasoning chains, majority-vote the final answers. [8]

- **Strengths:** simple, strong on verifiable tasks, no training required.
- **Weaknesses:** only works when the answer space has a clear "vote" semantic (math answers, yes/no); useless for creative or code output.

### 9. Plan-and-Solve, Skeleton-of-Thought, Algorithm of Thoughts

A cluster of "think about the plan first, then execute" frameworks. Plan-and-Solve (Wang 2023), Skeleton-of-Thought (Ning 2023), Algorithm of Thoughts (Sel 2023). All three decompose tasks before executing. [9][10][11]

- **Strengths:** consistent small wins across benchmarks; improves long-horizon task coherence.
- **Weaknesses:** the plan itself can be wrong and lock the execution into the wrong frame.

### 10. Least-to-Most

Zhou et al. (2022). Decompose hard task into simpler subtasks, solve subtasks in order, each subtask has prior subtasks' answers as context. [12]

- **Strengths:** strong on compositional generalization; simple to implement.
- **Weaknesses:** task decomposition is itself a hard problem; can cascade errors.

### 11. Meta-finding: no single framework dominates

Across all 2023–2025 comparative studies, the result is consistent: **no single planning framework dominates**. The best performer is task-class-conditional. ReAct + CoV wins at grounded factual; ToT/LATS wins at verifiable reasoning; Reflexion wins at retriable multi-attempt; Self-Refine wins at creative refinement; Self-Consistency wins at math. [13]

**The meta-framework is: route planning strategy by task namespace.** This matches Brief 109 (adaptive reasoning budget by namespace) and Brief 110 (MoE routing by namespace).

### 12. What GSPL has that none of these frameworks assume

Every published planning framework assumes the model reasons in a vacuum. GSPL assumes the model reasons on top of a signed, lineage-bearing knowledge graph with:

- **Per-step grounding signal** (every thought is audited against the graph).
- **Per-step cost envelope** (Brief 101 budgets every step).
- **Signed intermediate artifacts** (every thought can become a reusable gseed).
- **Constitutional constraints** (the 13 commitments prune invalid branches).
- **Confidence type** (INV-348) unified across all reasoning outputs.

This means GSPL's planner can compose any of the above frameworks with substrate-aware primitives the framework authors did not have access to.

## Inventions to absorb

Tier W hooks for Brief 126:

- **Namespace-conditional planning strategy routing.** The default planner is ReAct + CoV. For verifiable reasoning (math, code, physics) it switches to LATS. For retriable multi-attempt it switches to Reflexion with a signed episodic memory. For creative it switches to Self-Refine with diversity regularization.
- **Every thought is a candidate gseed.** Successful reasoning traces become reusable signed gseeds (Brief 109).
- **The graph prunes invalid branches at zero cost.** In ToT / LATS search, branches that violate grounding or constitutional commitments are pruned before evaluation. This is free because the graph already has the signals.
- **Constitutional critics as search value function.** The 13 commitments become part of the MCTS value estimate for LATS.
- **Reflexion with signed critique gseeds.** Episodic memory is the signed federation graph, not a local scratchpad.
- **CoV verification uses the graph.** Verification questions are graph queries; the answer is the graph's answer, not a second LLM call.
- **Adaptive budget envelope** routes search intensity by task and by subscription tier (Brief 106).

## Risks identified

- **Framework proliferation becomes framework sprawl.** Mitigation: one router, named strategies, finite set. No ad-hoc framework mixing.
- **Namespace routing misclassifies tasks.** Mitigation: router trained on substrate-native task examples; fallback is ReAct + CoV (safe default).
- **LATS is expensive.** Mitigation: only used on verifiable namespaces; budget envelope capped.
- **Reflexion requires retriable tasks.** Mitigation: only used when the task is retriable; otherwise falls back to CoV.
- **Self-Refine regresses quality.** Mitigation: critic confidence threshold gates refinement; quality metric from Brief 096 is the guard.

## Recommendation

The GSPL reasoning kernel (Brief 126) ships with **one configurable planner and five named strategies**:

1. **Default: ReAct + CoV.** Safe, grounded, good for the majority of tasks.
2. **Verifiable-reasoning: LATS with substrate-aware value function.** Math, code, physics, chemistry, power-system balance.
3. **Retriable multi-attempt: Reflexion with signed critique memory.** Task retries with signed critique gseeds.
4. **Creative: Self-Refine with diversity regularization.** Writing, design, narrative.
5. **Math-answer: Self-Consistency + solver.** Math word problems with verifiable numeric answers.

Strategy is selected by the router (task namespace + budget tier). Fallback to ReAct + CoV on router uncertainty.

Every strategy honors:
- Per-step grounding audit (Brief 109).
- Per-step cost envelope (Brief 101).
- Constitutional commitment checks (Brief 113).
- Signed intermediate artifacts (Brief 109 lineage).

Feeds Brief 126 (reasoning kernel) directly.

## Confidence

**4.5/5.** Every framework cited is well-published. The strategy-routing meta-pattern is principled and tracks the field's convergent findings. The one 3.5/5 piece is the custom value function for LATS — training it requires data we don't have pre-launch; mitigation is to start with the graph + constitutional score as a hand-crafted value and learn it iteratively.

## Spec impact

- Brief 029 (planner agent architecture) needs the strategy-router addendum.
- Brief 030 (critic ensemble) needs the "graph + constitutional = critic" addendum.
- Brief 126 owns the final integration.

## Open follow-ups

- Router training data (substrate-native task/strategy pairs).
- LATS value function training recipe.
- When to upgrade ReAct + CoV to v2 (post-launch).

## Sources

1. Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," 2022. arXiv:2210.03629.
2. Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning," 2023. arXiv:2303.11366.
3. Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback," 2023. arXiv:2303.17651.
4. Yao et al., "Tree of Thoughts," 2023. arXiv:2305.10601.
5. Besta et al., "Graph of Thoughts," 2023. arXiv:2308.09687.
6. Zhou et al., "Language Agent Tree Search," 2023. arXiv:2310.04406.
7. Dhuliawala et al., "Chain-of-Verification Reduces Hallucination in Large Language Models," 2023. arXiv:2309.11495.
8. Wang et al., "Self-Consistency Improves Chain of Thought Reasoning in Language Models," 2022. arXiv:2203.11171.
9. Wang et al., "Plan-and-Solve Prompting," 2023.
10. Ning et al., "Skeleton-of-Thought," 2023.
11. Sel et al., "Algorithm of Thoughts," 2023.
12. Zhou et al., "Least-to-Most Prompting Enables Complex Reasoning in Large Language Models," 2022.
13. Various comparative studies, 2024–2025.
