# 125 — Copilot Workspace, Devin, SWE-agent, Augment teardown

## Question

What do the autonomous-loop coding systems (GitHub Copilot Workspace, Cognition Devin, SWE-agent, Augment Code) teach about long-horizon autonomy, agent-computer interfaces, and closed-loop engineering that GSPL must absorb?

## Why it matters (blast radius)

This is where the "AI software engineer" promise is being stress-tested in public. Every system here runs autonomously over minutes-to-hours horizons on real engineering tasks. Their failure modes and successful patterns are the best public signal on what GSPL's long-horizon agent must solve.

## What we know from the spec

- Brief 118 (multi-agent) commits to bounded returning sub-agents.
- Brief 115 (planning) commits to strategy-routed planner.
- Brief 117 (tool-use) commits to substrate-typed action space.
- Brief 119 (self-improvement) commits to tiered improvement loop.

## Findings

### 1. Copilot Workspace: spec → plan → implementation → PR

GitHub's Copilot Workspace (2024) is a structured pipeline: the user describes an issue, the system produces a spec, then a plan, then an implementation, then opens a PR. Each stage is editable. [1]

- **Strengths:** the stage-by-stage discipline is pedagogically clean; editable artifacts at every stage build trust; tight GitHub integration is a distribution lever.
- **Weaknesses:** the rigid pipeline doesn't match non-linear real work; each stage adds latency; the user often wants to skip to implementation.

**GSPL lesson:** stage-by-stage with editable artifacts is the right default for complex tasks. But stages must be collapsible so simple tasks skip to implementation.

### 2. Cognition Devin: long-horizon autonomous loop

Cognition's Devin (2024) runs as a full remote agent with a browser, shell, editor, and planner. It runs for hours on tasks. Public benchmarks show ~13% on SWE-bench initially, climbing with iteration. [2]

- **Strengths:** the long-horizon autonomous pattern is the endgame; the planner-executor-debugger-reviewer loop is the right shape.
- **Weaknesses:** failures are opaque; cost per task is high; most published runs required human intervention; the closed-source agent can't be audited.

**GSPL lesson:** long-horizon autonomy is possible but requires extreme discipline on budget, grounding, and rollback. Brief 101 (budget envelope) and Brief 105 (rollback) are load-bearing for this.

### 3. SWE-agent: the agent-computer interface insight

Yang et al. (2024) showed that a single agent with a carefully designed Agent-Computer Interface (commands like `open`, `edit`, `search`, `goto`, `submit`) beat multi-agent approaches on SWE-bench at the time. The ACI is the action space. [3]

**GSPL lesson:** this is the strongest public evidence for Brief 117's insight — a well-designed action space is worth more than multi-agent orchestration. GSPL's modifier-surface DSL IS the ACI.

### 4. The SWE-bench benchmark as a forcing function

SWE-bench Verified (2024) became the canonical benchmark for autonomous coding agents. Scores published by Anthropic, OpenAI, Google, Cognition, and others are the competitive yardstick. [4]

**GSPL lesson:** GSPL should track SWE-bench Verified as one of several benchmarks, but not optimize exclusively for it — the benchmark rewards fixing bugs in existing codebases, not the creator-first workloads GSPL targets.

### 5. Augment Code: long-context enterprise agent

Augment (2024) focuses on enterprise-scale codebases with a 100M+ token context system (retrieval-backed) and deep IDE integration. Its pitch is "works on huge legacy codebases where Cursor and Copilot break." [5]

**GSPL lesson:** the enterprise-scale long-context path is achievable with retrieval rather than context window. GSPL's Brief 120 substrate-native retrieval is the same lever.

### 6. Claude with Computer Use as an autonomous pattern

Anthropic's Claude Computer Use (2024) lets Claude control a desktop via screenshots. Public demos show it can operate real software autonomously. [6]

**GSPL lesson:** computer use is a last-resort external tool (Brief 117). For most creator tasks, substrate-native actions are faster and more reliable. Computer use is for the long tail.

### 7. The "pull request as contract" pattern

Copilot Workspace and Devin both treat the PR as the canonical artifact. The agent's work ends when the PR is opened; human review begins.

**GSPL lesson:** for coding workloads, PR-as-contract is the right handoff. But GSPL's substrate supports richer contracts: signed gseeds with lineage, which are strictly more auditable than PRs.

### 8. The "long horizon is about recovery, not execution"

Devin's public failures reveal the core insight: the hard part of long-horizon autonomy isn't executing steps — it's recovering from errors. A 100-step task has a ~0 chance of all steps succeeding; the agent must be able to detect and correct failures at every step.

**GSPL lesson:** Brief 115's evaluator-optimizer pattern is load-bearing for long horizons. Every step must be verifiable against the substrate. The grounding floor is the recovery signal.

### 9. SWE-bench's "repo knowledge" problem

SWE-bench's hardest tasks require understanding the repository's conventions and hidden dependencies. Agents that don't read enough of the repo fail; agents that read too much exhaust their budget.

**GSPL lesson:** substrate-native retrieval (Brief 120) with graph-walk on the repository's signed convention gseeds makes this tractable. GSPL creators sign their conventions; agents walk the graph to find them.

### 10. The "loop budget cap" as a safety lever

Every long-horizon agent has a loop budget cap — a hard limit on turns, tokens, or tool calls after which the agent stops. Without the cap, agents spin forever.

**GSPL lesson:** Brief 101's budget envelope is the cap. It must be enforced at every loop, every sub-agent, every tool call. No infinite loops.

### 11. "Stop conditions" as a research frontier

When should the agent stop? Declared success? Test pass? Human approval? This is an open research question. Devin uses learned stop classifiers; SWE-agent uses test pass; Copilot Workspace uses human review.

**GSPL lesson:** GSPL's stop conditions are multi-signal:
- Grounding floor satisfied.
- Constitutional commitments satisfied.
- Task-specific verifiable reward signal (if present).
- Budget envelope exhausted.
- Explicit creator approval (for sensitive tasks).

All five are first-class; any one can terminate the loop.

### 12. The "one PR per issue" discipline

Devin and Copilot Workspace both enforce one PR per task. This is the right default but fights real work where one issue touches multiple surfaces.

**GSPL lesson:** the unit of work is the signed gseed, not the PR. A single task can produce multiple gseeds that federate independently. This is more flexible than PR-per-task.

### 13. "Self-heal" and debugging loops

Devin, SWE-agent, and OpenHands all include debugging loops: if a command fails, the agent reads the error, reasons about it, and tries again. This is where most of the long-horizon value comes from.

**GSPL lesson:** the debugging loop is a named planner strategy (Brief 115): Reflexion with verified-error signal. GSPL should expose it as a first-class strategy.

### 14. The enterprise-grade observability layer

Augment Code and others ship extensive observability: every agent action is logged, every tool call has a trace, every decision has a rationale. Enterprise adoption requires this.

**GSPL lesson:** the signed lineage graph IS the observability layer. Every substrate mutation is already logged, traced, and rationalized. This is structural, not bolt-on.

### 15. What no system has solved

- **Cross-session memory that actually compounds.** All of these systems forget between tasks.
- **Fine-grained permission models for destructive actions.** Most ask for confirmation once, then run free.
- **Rollback across a multi-step trajectory.** Most systems can undo a single change; few can undo a 20-step trajectory cleanly.
- **Attribution of work to the agent's reasoning path.** No system reliably links "why did I do this" to "what did I do."

**GSPL lesson:** these four are all GSPL structural wins. Signed substrate = cross-session memory. Brief 033 = fine-grained permissions. Brief 105 = multi-step rollback. Signed lineage = why-to-what attribution.

## Inventions to absorb

Tier W hooks for Brief 126 and Brief 129:

- **Stage-by-stage with collapsible stages.** Simple tasks skip to implementation; complex tasks use the full pipeline.
- **Evaluator-optimizer as load-bearing for long horizons.** Brief 115.
- **Multi-signal stop conditions.** Grounding floor + constitutional + verifiable reward + budget + explicit approval.
- **Loop budget cap enforced at every level.** Brief 101.
- **Debugging loop as a named strategy.** Reflexion with verified-error signal.
- **Signed lineage as the observability layer.** Already structural.
- **Substrate mutation as the unit of work, not the PR.** Multiple independent gseeds per task.
- **Repo convention gseeds for the agent to walk.** Brief 120's substrate-native retrieval applies.
- **Computer use as last-resort external tool only.** Brief 117 stands.
- **Structural wins as the competitive lever:** cross-session memory, permissions, rollback, attribution.

## Risks identified

- **Long-horizon autonomy is hard to get right.** Mitigation: ship with short-horizon defaults; long-horizon is opt-in; failures degrade gracefully.
- **SWE-bench optimization is a trap.** Mitigation: track it but don't optimize exclusively; creator workflows are the primary target.
- **Evaluator-optimizer latency.** Mitigation: evaluator runs on a fast tier (Brief 110); optimizer only on failed steps.
- **Rollback across multi-step trajectories is complex.** Mitigation: Brief 105 defines the rollback primitive; every gseed is rollback-able; trajectory rollback is composed.

## Recommendation

1. **Stage-by-stage with collapsible stages** is the default for complex tasks.
2. **Evaluator-optimizer is the long-horizon backbone.** Brief 115's LATS or ReAct+CoV strategy, with the substrate grounding floor as the evaluator.
3. **Multi-signal stop conditions.** No single stop signal is authoritative.
4. **Loop budget cap is enforced at every level.** Brief 101.
5. **Debugging loop as a named strategy.** Named "debug-loop" in Brief 115.
6. **Unit of work is the signed gseed, not the PR.** Multiple gseeds per task are normal.
7. **Repo convention gseeds** drive agent context for codebase-aware tasks.
8. **Computer use is last-resort external.** Brief 117 stands.
9. **Track SWE-bench and LiveCodeBench as external anchors** without optimizing exclusively.
10. **Expose structural wins** (memory, permissions, rollback, attribution) as the creator-facing differentiation.

Feeds Brief 126 (reasoning kernel) and Brief 129 (self-improvement loop).

## Confidence

**4.5/5.** All five systems are well-documented in public. The long-horizon autonomy lessons are the clearest signal in this research round. The 3.5/5 piece is evaluator-optimizer latency at multi-step scale; needs empirical validation.

## Spec impact

- Brief 101 needs loop-level budget cap addendum.
- Brief 105 needs trajectory rollback addendum.
- Brief 115 needs the debug-loop strategy.
- Brief 126 owns the integration.
- Brief 129 needs the observability-as-lineage confirmation.

## Open follow-ups

- Evaluator-optimizer latency budget.
- Trajectory rollback implementation.
- SWE-bench Verified baseline measurement post-Brief 126.

## Sources

1. GitHub, "Copilot Workspace" documentation and blog, 2024.
2. Cognition Labs, "Introducing Devin," 2024.
3. Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," 2024. arXiv:2405.15793.
4. Jimenez et al., "SWE-bench," 2023; SWE-bench Verified, 2024.
5. Augment Code documentation and launch materials, 2024.
6. Anthropic, "Claude's Computer Use," Oct 2024.
