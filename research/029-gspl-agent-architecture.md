# 029 — GSPL Agent end-to-end architecture

## Question
What is the end-to-end architecture of the GSPL Agent — the LLM-driven intelligence layer that turns natural-language intent into seeds, breeding plans, and finished artifacts — and how does it interact with the kernel, the studio, and the user?

## Why it matters
The agent is the user's primary interface to GSPL. A casual user never edits a `.gseed` file; they speak intent and the agent translates. If the agent is unreliable, hallucinatory, or inconsistent, the entire stack underneath is invisible. Brief 011 already established mechanical reliability backstops; this brief defines the *architecture* the agent fits into.

## What we know from the spec
- `architecture/agent.md` exists as a stub.
- Brief 011 fixed the four-layer reliability stack (mechanical, semantic, operational, model hygiene).
- Brief 033 will cover concept-to-seed latency budgets.

## Findings — the architecture

### Top-level shape

The GSPL Agent is a **planner + executor** loop with eight specialized sub-agents, a memory system, and a strict tool surface. It does not write seed bytes directly — it emits *proposals* that are executed by the kernel through a small, audited tool surface.

```
              ┌──────────────────────────────────────┐
              │            User intent                │
              └──────────────────┬───────────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────────┐
              │   Intent normalizer (Brief 032)      │
              └──────────────────┬───────────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────────┐
              │            Planner agent              │
              │  (Tree of Thoughts → plan tree)       │
              └──────────────────┬───────────────────┘
                                 │
            ┌────────┬───────────┼───────────┬────────┐
            ▼        ▼           ▼           ▼        ▼
        Schema   Composer    Breeder     Validator  Critic
        agent    agent       agent       agent      agent
            ▼        ▼           ▼           ▼        ▼
              ┌──────────────────────────────────────┐
              │       Tool surface (Brief 030)       │
              │  emit_seed, mutate, crossover,       │
              │  validate, render_preview, score     │
              └──────────────────┬───────────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────────┐
              │              Kernel                   │
              └──────────────────┬───────────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────────┐
              │       Memory + exemplar archive       │
              │              (Brief 031)              │
              └──────────────────────────────────────┘
```

### The eight sub-agents

(Detailed in Brief 030. Listed here for completeness.)

1. **Planner**: turns intent into a plan tree using Tree of Thoughts, picks engines, picks composition patterns.
2. **Schema**: knows every engine's gene schema and produces typed gene proposals.
3. **Composer**: applies cross-engine composition patterns (Brief 028) to build multi-engine seeds.
4. **Breeder**: proposes breeding operators and parents from the archive.
5. **Validator**: runs the seed validator (Brief 014) and converts errors into repair plans.
6. **Critic**: scores candidates against learned and rule-based critics.
7. **Researcher**: searches the exemplar archive and the user's history for relevant priors.
8. **Explainer**: generates user-facing explanations of what was produced and why.

### The tool surface

The agent calls a *small, total, deterministic* tool surface:

- `emit_seed(engine, genes) → seed_id | error` — produces a fresh seed; validator runs automatically.
- `mutate(seed_id, operator, params) → seed_id | error` — applies a typed mutation operator.
- `crossover(parent1, parent2, operator, params) → seed_id | error` — applies a typed crossover operator.
- `validate(seed_id) → Valid | Invalid(reason, invariant_id, gene_path)`.
- `render_preview(seed_id, mode) → preview_id` — produces a small thumbnail/audio clip/text summary.
- `score(seed_id, critic) → score_table` — runs critics and returns ranked metrics.
- `archive_query(intent, k) → seed_id[]` — returns top-k similar seeds from the exemplar archive.
- `lineage_query(seed_id) → ancestry` — returns ancestry up to a depth limit.

The agent **never** writes raw bytes, **never** calls a network endpoint outside this surface, and **never** generates JSON the validator hasn't approved. Every state change goes through the tool surface and is logged.

### Planner loop

The planner runs a **Tree of Thoughts** with three tunable hyperparameters:

- **Branching factor** (default 3): how many alternative plans the planner generates per step.
- **Depth** (default 4): how many planning steps before committing.
- **Beam width** (default 2): how many candidate plans survive each round.

At each step the planner produces N candidates, the critic scores them, the top K survive. The final plan is a sequence of tool calls. No tool is executed until the plan is complete and the explainer summarizes it for the user (or for autonomous mode, the safety check passes).

### Modes

- **Interactive**: every plan step is shown to the user; the user can edit, approve, or reject.
- **Autonomous**: plans execute end-to-end with no user intervention; reserved for Phase 2 with strict guardrails.
- **Coach**: the agent watches the user manually compose and offers suggestions without executing.

## Risks identified

- **Hallucinated gene names**: the agent invents a gene name that doesn't exist in the schema. Mitigation: Schema agent has the full catalog and rejects unknowns at proposal time. (Layer 1 of Brief 011.)
- **Plan-tree explosion**: ToT with branching 3 depth 4 = 81 candidates per round. Mitigation: critic prunes to beam width 2.
- **Critic bias**: the critic favors safe, average outputs; novelty dies. Mitigation: novelty is one of the critic dimensions (Brief 040).
- **Tool-call loops**: a buggy plan retries the same operation. Mitigation: retry budget per tool, hard cap on plan steps.
- **Explainer hallucinations**: the explainer fabricates reasons. Mitigation: explanations are constrained to the actual tool calls executed; no free-form post hoc rationalization.

## Recommendation

1. **Adopt the planner+executor architecture with eight sub-agents.**
2. **The tool surface is the only way the agent affects state.** Codify in `architecture/agent.md` and enforce in code.
3. **Tree of Thoughts at branching 3 / depth 4 / beam 2** as v1 defaults; tune empirically.
4. **Three modes (interactive, autonomous, coach)** with autonomous gated behind Phase 2 guardrails.
5. **Every tool call is logged with its parent plan ID** for replayability and debugging.
6. **Explainer is constrained** to the executed tool calls; no free-form rationalization.
7. **Sub-agents share the same model by default** but each can override (e.g., Critic may use a smaller, cheaper model).

## Confidence
**3/5.** Planner+executor with ToT is a well-understood architecture (LangGraph, AutoGen, OpenAI's function calling). The 3/5 reflects (a) the unproven assumption that this maps cleanly onto seed editing and (b) the cost-quality tradeoff at GSPL's compute budget.

## Spec impact

- `architecture/agent.md` — full architecture document.
- `architecture/agent-tool-surface.md` — the eight tools, their signatures, and their semantics.
- `algorithms/planner-tot.md` — the ToT pseudocode.
- New ADR: `adr/00NN-agent-architecture-v1.md`.

## Open follow-ups

- Decide on the exact model used by the planner (likely a frontier model with function calling).
- Build the tool surface as a single Rust crate with deterministic behavior.
- Define the autonomous-mode safety guardrails (Phase 2).
- Empirically tune ToT hyperparameters once the agent is running.

## Sources

- Yao et al., *Tree of Thoughts: Deliberate Problem Solving with Large Language Models*.
- Internal: Brief 011 (reliability backstops), Brief 014 (validator), Brief 028 (composition patterns).
