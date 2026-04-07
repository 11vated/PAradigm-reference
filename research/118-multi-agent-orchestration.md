# 118 — Multi-agent orchestration: AutoGen, CrewAI, LangGraph, MetaGPT, AgentVerse, Swarm, SWE-agent

## Question

When does GSPL benefit from multi-agent orchestration, when does it hurt, and how does multi-agent discipline preserve the grounding floor when many agents operate on shared substrate?

## Why it matters (blast radius)

Multi-agent systems are fashionable but fragile. Done right, they parallelize work and specialize capabilities. Done wrong, they amplify hallucinations, break lineage, and dilute the grounding floor. GSPL cannot ship with multi-agent as a default — but the right pattern is a huge productivity win for hard creator tasks.

## What we know from the spec

- Brief 029 (planner agent) commits to a single-agent architecture by default.
- Brief 110 (MoE) suggests an MoE-shaped orchestration layer is natural for GSPL.
- The claude-code-guide and Brief 125 (Copilot/Devin/SWE-agent) reference multi-agent patterns.

## Findings

### 1. AutoGen

Microsoft Research (2023). Conversation-centric: agents talk to each other in a shared message log. Supports hierarchies of agents, tool-calling, human-in-the-loop. [1]

- **Strengths:** flexible; the message log is easy to reason about and debug.
- **Weaknesses:** conversations can loop; token cost explodes; no principled way to bound the conversation length.

### 2. CrewAI

(2024). Role-based: agents have named roles, goals, backstories, and tools. A "crew" is an explicit orchestration of roles executing tasks in sequence or parallel. [2]

- **Strengths:** the role metaphor is legible to non-technical users; templating is straightforward.
- **Weaknesses:** role-playing can degrade grounding (agents "stay in character" even when accuracy demands breaking character); brittle on long tasks.

### 3. LangGraph

LangChain (2024). Graph-based orchestration: nodes are agents or tools, edges are conditional transitions. The graph is explicit; state is shared. [3]

- **Strengths:** the explicit graph is the right abstraction for complex multi-step workflows; good debugging; supports cycles and branching.
- **Weaknesses:** verbose to define; the graph-as-code pattern has a learning curve.

### 4. MetaGPT

Hong et al. (2023). Simulates a software company: product manager agent writes requirements, architect agent designs, engineer agents code, QA agent tests. Waterfall metaphor. [4]

- **Strengths:** strong results on software engineering benchmarks when the task fits the waterfall shape.
- **Weaknesses:** waterfall is rigid; tasks that don't fit (exploration, iteration) suffer; the role specialization feels forced.

### 5. AgentVerse and Camel

Multi-agent playgrounds that focus on emergent collaboration between role-defined agents. Useful for research; not production-ready for solo-founder scale. [5][6]

### 6. OpenAI Swarm

(2024). Lightweight orchestration: agents can "hand off" to other agents via function calls. Minimal framework — the emphasis is that most multi-agent can be expressed as routed function calls. [7]

- **Strengths:** minimalism is right; the hand-off primitive captures most of what's needed.
- **Weaknesses:** explicitly an experimental pattern, not production.

### 7. SWE-agent and agent-computer interfaces

Yang et al. (2024). Single-agent with a carefully-designed agent-computer interface (ACI) — commands like `open`, `edit`, `goto`, `search`, `submit`. Beat multi-agent SWE-bench results at the time. [8]

**Meta-lesson:** one agent with a well-designed action space often beats multiple agents with poor action spaces. Multi-agent is sometimes a *symptom* of a bad action space.

### 8. Devin and the black-box autonomous pattern

Cognition's Devin (2024) packages a multi-agent system behind a single task interface. The internals are opaque but the public pattern is: planner → executor → debugger → reviewer, with long-horizon task tracking. [9]

### 9. Anthropic's agent patterns document

Anthropic's 2024 "Building Effective Agents" post distilled industry experience into canonical patterns: workflow (deterministic chaining), routing, parallelization, orchestrator-workers, evaluator-optimizer. The strongest recommendation: **use the simplest pattern that works; multi-agent is a last resort.** [10]

### 10. When multi-agent wins

Empirically, multi-agent beats single-agent when:
- Tasks are decomposable with clean boundaries (MetaGPT's waterfall fits).
- Sub-tasks require very different tools or contexts (research vs implementation vs review).
- Long horizons exceed a single context budget and work must be parallelized.
- Verification benefits from independent perspectives (debate-style critique).

Multi-agent **loses** when:
- Tasks are not decomposable and force artificial boundaries.
- Sub-agents duplicate reasoning (same context, same tools, wasted tokens).
- Shared state becomes a contention bottleneck.
- Debugging is impossible across agents.

### 11. Grounding floor under multi-agent

This is the GSPL-specific concern. If agent A cites the graph, and agent B reads A's output without re-citing, hallucinations propagate. The fix is **every hand-off carries its lineage.** When agent A hands off to agent B, B receives not just A's text but A's signed provenance trace. B can re-audit A's citations against the graph before acting on them.

No published multi-agent framework does this, because none of them have a signed substrate underneath.

### 12. The MoE orchestration analogy (Brief 110)

GSPL's agent orchestration is architecturally an MoE router: the router dispatches tasks to namespace experts (chemistry expert, culture expert, code expert, etc.) with a shared grounding floor always active. This is a multi-agent system, but the "agents" are routed at the model-orchestration layer, not the framework layer. The benefits of multi-agent (specialization) come with the discipline of MoE (load balancing, shared expert, auditable routing).

## Inventions to absorb

Tier W hooks for Brief 126 and Brief 128:

- **Default to single-agent.** Multi-agent is opt-in, scoped to tasks that publicly benefit (long code refactors, cross-namespace research, debate-style verification).
- **Multi-agent = namespace-routed MoE** (Brief 110). The router + fine-grained expert agents + shared grounding floor IS the multi-agent system.
- **Every hand-off carries signed lineage.** Agent B re-audits agent A's citations before acting. No unverified hand-offs.
- **Bounded conversation length by envelope.** Brief 101's budget envelope caps multi-agent conversations; no infinite loops.
- **Simplest pattern that works.** Follow Anthropic's ordering: workflow → routing → parallelization → orchestrator-workers → evaluator-optimizer. Multi-agent is the last step, not the first.
- **Evaluator-optimizer as first-class pattern for verifiable tasks.** One agent generates, another evaluates against the substrate graph, generator revises. This is the multi-agent version of Reflexion (Brief 115).
- **No role-play degradation.** Agents don't "stay in character" if staying in character hurts grounding. Character is a tone layer (Brief 113), not a reasoning layer.

## Risks identified

- **Multi-agent loops.** Mitigation: hard budget cap; turn counter; automatic degrade to single-agent if budget exceeded.
- **Shared state contention.** Mitigation: substrate's content-addressed graph handles concurrent writes via Brief 100's fork-and-reconcile.
- **Hand-off lineage bloat.** Mitigation: lineage is signed but compressed; only the provenance root is carried, not the full chain.
- **Users can't debug multi-agent.** Mitigation: Brief 103's composition graph viewer shows every agent-step as a node; the viewer works across agents.
- **The temptation to add agents as a fix for bad action-space design.** Mitigation: every multi-agent proposal has to prove the single-agent failure first.

## Recommendation

1. **Default is single-agent.** GSPL's reasoning kernel is one model running the Brief 115 planner strategies.
2. **Multi-agent is namespace-routed MoE orchestration.** Brief 110's router + fine-grained expert pattern is the multi-agent system GSPL ships.
3. **Canonical patterns in priority order:** workflow, routing, parallelization, orchestrator-workers, evaluator-optimizer. No ad-hoc agents.
4. **Every hand-off carries signed lineage.** Receiving agents re-audit citations before acting.
5. **Bounded by envelope.** Brief 101 caps the budget; no runaway loops.
6. **Debuggable in the composition graph viewer.** Brief 103 shows every agent-step.
7. **Evaluator-optimizer pattern is the default for verifiable tasks.** Generator + substrate critic + revise loop.
8. **No role-play.** Character is a tone layer, not a reasoning constraint.

Feeds Brief 126 (reasoning kernel) and Brief 128 (tool-use).

## Confidence

**4/5.** The single-agent-first discipline is well-supported by 2024–2025 industry experience. The multi-agent-as-MoE mapping is novel and 3.5/5 — principled but unproven at scale in production.

## Spec impact

- Brief 029 needs the multi-agent opt-in rules.
- Brief 034 (agent observability) needs multi-agent trace support.
- Brief 126 owns the integration.

## Open follow-ups

- Exact budget caps for multi-agent conversations.
- Router training for namespace dispatch.
- Evaluator-optimizer recipe for each substrate namespace.

## Sources

1. Wu et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation," Microsoft, 2023. arXiv:2308.08155.
2. CrewAI documentation, 2024.
3. LangGraph documentation, LangChain, 2024.
4. Hong et al., "MetaGPT: Meta Programming for Multi-Agent Collaborative Framework," 2023. arXiv:2308.00352.
5. Chen et al., "AgentVerse," 2023.
6. Li et al., "CAMEL: Communicative Agents for Mind Exploration of Large Language Model Society," 2023.
7. OpenAI, "Swarm," 2024.
8. Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," 2024. arXiv:2405.15793.
9. Cognition Labs, "Introducing Devin," 2024.
10. Anthropic, "Building Effective Agents," Dec 2024.
