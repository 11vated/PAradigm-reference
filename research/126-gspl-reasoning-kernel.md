# 126 — GSPL reasoning kernel design (Tier W integration)

## Question

What is the GSPL reasoning kernel — the composed integration of test-time compute, MoE backbone, planning strategies, multi-agent discipline, and action-space that makes the creator-facing agent unsurpassable?

## Why it matters (blast radius)

This is the brain. Every finding from Briefs 109–125 lands here. A sloppy composition produces an agent that is the sum of its parts' weaknesses; a principled one produces an agent whose capabilities compound. The reasoning kernel is the single most load-bearing piece of the intelligence layer.

## What we know from prior briefs

- **109:** adaptive test-time compute with configurable thinking budget; open reasoning traces; substrate as free process reward.
- **110:** Qwen3-MoE-A22B or Llama 4 class as backbone; MLA in context buffer; expert offloading for local-first.
- **111:** YaRN-extended attention in v1, hybrid SSM+attention deferred to v2.
- **113:** SFT → DPO/IPO → RFT training recipe with constitutional critics.
- **114:** neurosymbolic topology with Lean and substrate primitives as first-class tools.
- **115:** five named planner strategies (ReAct+CoV, LATS, Reflexion, Self-Refine, Self-Consistency+solver) routed by namespace.
- **116:** memory is the substrate, not a separate store.
- **117:** modifier-surface DSL as the action space; signed tool calls.
- **118:** single-agent default; multi-agent as namespace-routed MoE.
- **119:** tiered self-improvement (daily/weekly/monthly/quarterly).
- **120:** substrate-native retrieval with multi-backend fusion.
- **121:** Claude Code discipline — CLI-first, tool-rich, plan mode, bounded sub-agents.
- **122:** Qwen backbones sufficient; thinking-mode flag; Hermes function-calling parse.
- **123:** parallel tool calling; open thinking traces; multi-modal native.
- **124:** ambient context; commit-per-change; preview-with-veto; live substrate stream.
- **125:** multi-signal stop conditions; evaluator-optimizer backbone; signed lineage as observability.

## Architecture

The reasoning kernel is a five-layer stack. Each layer composes the prior.

### Layer 0: Backbone tier (Brief 110)

- **Default:** Qwen3-MoE-A22B (open weights, Apache 2.0, MoE with fine-grained experts).
- **Alternates:** Llama 4 Scout, DeepSeek-V3, Mistral Large 2 — all interchangeable via Brief 122's backbone-agnostic interface.
- **Adapters:** LoRA adapters for each substrate namespace, trained weekly via Brief 113 and Brief 119.
- **Context:** YaRN-extended to 256K effective; expert offloading for laptop-class hardware.
- **Tokenizer:** extended with substrate special tokens (citation, modifier call, confidence, lineage markers).

### Layer 1: Test-time compute tier (Brief 109)

- **Configurable thinking budget** exposed as inference parameter: `think=low|medium|high|max`.
- **Open thinking traces** by default; creator can disable.
- **Process reward = substrate grounding audit.** Every reasoning step is auditable against the graph.
- **Cached thinking traces** become reusable signed gseeds for similar future queries.
- **Adaptive budget by namespace and tier** (Brief 106 subscription integration).

### Layer 2: Planner strategy tier (Brief 115)

Five named strategies, routed by a lightweight classifier trained on substrate-native task examples:

1. **Default: ReAct + Chain-of-Verification.** Safe, grounded, covers 70% of tasks.
2. **Verifiable reasoning: LATS with substrate-aware value function.** Math, code, physics, chemistry.
3. **Retriable multi-attempt: Reflexion with signed critique gseeds.** Tasks that benefit from retry.
4. **Creative: Self-Refine with diversity regularization.** Writing, design, narrative.
5. **Math-answer: Self-Consistency + solver (Brief 114).** Math word problems with verifiable numeric answers.

Router fallback is ReAct + CoV.

### Layer 3: Action space and tool-use (Brief 117)

- **Action space IS the modifier-surface DSL** (Brief 023) extended with four tool layers:
  - **Primitive:** graph queries, Lean proof, chemistry solver, physics solver, dimensional checker, confidence normalizer.
  - **Substrate:** modifier-surface DSL calls on any namespace.
  - **Meta:** fork, sign, tombstone, consultancy request, constitutional query.
  - **External:** web search (Brief 090), partner archive fetch (Brief 098), file I/O, MCP servers, computer-use (last resort).
- **Every tool call is a signed gseed** in a lineage-only namespace.
- **xgrammar-class structured output grammars** enforce valid tool calls at decode time.
- **Parallel tool calling** is the default when dependencies allow (Brief 123).
- **Edit-as-diff is a first-class primitive** (Brief 121, 124).
- **Commit-per-change discipline** maps signed gseeds to git commits one-to-one (Brief 124).

### Layer 4: Agent orchestration (Brief 118)

- **Single agent by default.**
- **Multi-agent as namespace-routed MoE** (Brief 110 analogy). The router dispatches tasks to namespace experts with a shared grounding floor.
- **Bounded returning sub-agents** for scoped parallel work (Brief 121 Task pattern).
- **Canonical patterns in priority order:** workflow → routing → parallelization → orchestrator-workers → evaluator-optimizer.
- **Every hand-off carries signed lineage;** receiving agents re-audit citations.
- **Bounded by envelope** (Brief 101).
- **No role-play degradation.**

### Layer 5: Stop and safety

- **Multi-signal stop conditions:** grounding floor satisfied + constitutional commitments satisfied + verifiable reward met + budget envelope exhausted + explicit approval.
- **Constitutional fence** (Brief 113): 13 commitments checked at every generated output before emission.
- **Grounding floor** (INV-357): every claim cites a signed substrate source or is explicitly marked as opinion.
- **Rollback at every level** (Brief 105): any signed gseed can be rolled back; trajectory rollback is composed from individual rollbacks.

## Creator-facing surface

- **CLI-first** (Brief 121).
- **Studio (Brief 103)** shows:
  - Live substrate mutation stream (Brief 124).
  - Live progress widget (Brief 121).
  - Ambient context indicator (Brief 124).
  - Plan Mode for non-trivial tasks (Brief 121).
  - Tool-call preview for sensitive tools (Brief 124).
- **Slash commands** as named workflows (Brief 121).
- **Signed project-convention gseeds** replace `.cursorrules`-class files (Brief 124).
- **Configurable per-namespace** via signed creator config gseeds.

## Inventions (tentative INV numbering: INV-482 through INV-505)

- **INV-482:** configurable thinking budget as first-class inference parameter with open traces.
- **INV-483:** cached thinking traces as reusable signed gseeds.
- **INV-484:** adaptive budget by namespace and subscription tier.
- **INV-485:** five named planner strategies with namespace-router dispatch.
- **INV-486:** substrate-aware LATS value function using grounding + constitutional signals.
- **INV-487:** Reflexion with signed critique gseeds in episodic namespace.
- **INV-488:** Self-Refine with Brief 096 identity-metric diversity regularization.
- **INV-489:** action space IS the modifier-surface DSL, extended across four tool layers.
- **INV-490:** every tool call is a signed gseed in lineage-only namespace.
- **INV-491:** xgrammar-class structured output grammars for tool calls.
- **INV-492:** parallel tool calling as default when dependencies allow.
- **INV-493:** edit-as-diff first-class primitive in modifier-surface DSL.
- **INV-494:** commit-per-change discipline with gseed↔git-commit one-to-one mapping.
- **INV-495:** namespace-routed MoE as the multi-agent pattern.
- **INV-496:** bounded returning sub-agents with signed lineage hand-off.
- **INV-497:** no-role-play discipline — character is a tone layer only.
- **INV-498:** multi-signal stop conditions with all five signals as first-class.
- **INV-499:** constitutional fence at every generated output.
- **INV-500:** rollback at every level, trajectory rollback composed from primitives.
- **INV-501:** ambient context pull from editor signals, namespace-scoped.
- **INV-502:** live substrate mutation stream as the studio trust surface.
- **INV-503:** slash commands as signed workflow gseeds.
- **INV-504:** signed project-convention gseeds replace stray config files.
- **INV-505:** tool-call preview with per-tool and per-namespace permission overrides.

## What makes this unsurpassable

The head-to-head advantages over Claude Code / Qwen / Gemini / Cursor / Devin:

1. **Substrate as free process reward.** No other system has a signed, typed, content-addressed ground truth to audit reasoning against at every step.
2. **Constitutional fence at every output.** No other system enforces non-amendable commitments as a generation-time constraint with auditable receipts.
3. **Multi-signal stop conditions.** Every other system uses one or two; GSPL uses five.
4. **Rollback at every level.** Every other system can undo a file edit; GSPL can undo a trajectory.
5. **Closed self-improvement loop.** Brief 119. Every creator's usage improves their adapter; no closed lab can match.
6. **Signed lineage as observability.** No other system has free observability from architecture.
7. **Namespace-routed MoE as multi-agent.** Every other system bolts multi-agent on; GSPL's is structural.
8. **Local-first posture.** Brief 053. Most frontier systems are cloud-only.
9. **Creator ownership.** Every signed gseed belongs to its creator; adapters belong to their trainer.
10. **Federation as continuous alignment signal.** Brief 113. No closed lab has this.

## Risks identified

- **Composition complexity.** Five layers are a lot to get right. Mitigation: each layer is individually shippable and testable; the reasoning kernel ships in tiers (v0.1 = layers 0+1+2; v0.2 adds 3; v0.3 adds 4+5).
- **Backbone quality drift.** Mitigation: multi-backbone discipline (Brief 122).
- **Router training data shortage at launch.** Mitigation: start with heuristic routing; train the classifier once there's enough substrate data.
- **LATS cost.** Mitigation: only for verifiable namespaces; budget-capped.
- **Parallel tool calling race conditions.** Mitigation: dependency analyzer runs before dispatch; ambiguous cases serialize.
- **Edit-as-diff conflicts in multi-turn tasks.** Mitigation: three-way merge on conflicts; creator veto on ambiguous merges.

## Recommendation

1. **Ship the reasoning kernel in three tiers** (v0.1 → v0.3).
2. **v0.1 ships layers 0+1+2** with Qwen3-Thinking backbone, configurable thinking budget, and five planner strategies with heuristic routing.
3. **v0.2 adds layer 3** — the full substrate-extended action space with signed tool calls.
4. **v0.3 adds layers 4+5** — multi-agent orchestration, multi-signal stop, full constitutional fence integration.
5. **Each tier ships with its own creator-visible feature set** so creators feel improvement every release.
6. **Brief 127 owns memory integration;** Brief 128 owns tool-use details; Brief 129 owns self-improvement; Brief 130 owns neurosymbolic; Brief 131 owns the differentiable-substrate synthesis.

## Confidence

**4.5/5.** Every component is grounded in prior briefs (109–125) and well-published research. The composition is principled and the tiering mitigates integration risk. The 3.5/5 piece is v0.3's multi-signal stop conditions at scale — this needs empirical validation against SWE-bench and substrate-native benchmarks.

## Spec impact

- Brief 029 (planner) supersedes with this kernel architecture.
- Brief 030 (critic) subsumes into Layer 5.
- Brief 040 (refinement + RL) subsumes into Brief 119's self-improvement loop.
- Brief 023 (modifier-surface DSL) is extended by Layer 3.
- Brief 033 (permissions) integrates with Layer 5's tool-call preview.
- Brief 103 (studio) integrates with the creator-facing surface.

## Open follow-ups

- v0.1 → v0.2 → v0.3 tier release schedule.
- Router classifier training recipe.
- LATS value function hand-crafted vs learned.
- Substrate-native benchmark battery for kernel evaluation.

## Sources

Briefs 109–125 and their cited sources.
