# 030 — Eight sub-agents: roles, contracts, handoffs

## Question
What are the precise roles, input/output contracts, and handoff protocols of the eight specialized sub-agents in the GSPL Agent (Brief 029)?

## Why it matters
"Eight sub-agents" is an organizing principle, not an implementation. Without clear contracts between them, the agent collapses into a soup where every sub-agent tries to do everything. Defining roles and handoffs is the difference between a maintainable system and a tangle of prompts.

## What we know from the spec
- Brief 029 named the eight sub-agents and the planner+executor architecture.
- Brief 011 defined the four-layer reliability backstop.

## Findings — sub-agent contracts

Each sub-agent is defined by: **role**, **input**, **output**, **tool access**, **stop conditions**, **failure mode**.

### 1. Planner

- **Role:** Translate normalized intent into a plan tree.
- **Input:** Normalized intent (Brief 032), user context (history, preferences, current archive snapshot).
- **Output:** A typed plan tree where leaves are tool-call specifications and internal nodes are composition patterns from Brief 028.
- **Tool access:** None. Planner does not execute; it only proposes.
- **Stop conditions:** Plan complete (depth or quality threshold reached) OR explicit user interrupt OR cost ceiling.
- **Failure mode:** Returns `Cannot plan: <reason>` to the user. Never executes a partial plan.

### 2. Schema

- **Role:** Be the canonical authority on every engine's gene schema; turn vague gene mentions into typed gene proposals.
- **Input:** Engine name + a list of gene name hints (possibly fuzzy or natural-language).
- **Output:** A typed gene proposal compatible with the engine's schema, with each gene's type, value, range, and tags filled in.
- **Tool access:** None. Pure transformation.
- **Stop conditions:** All hint genes resolved or marked as unresolvable.
- **Failure mode:** Returns the resolved subset plus an unresolved list with reasons. The Planner decides whether to retry, ask the user, or drop the unresolved hints.

### 3. Composer

- **Role:** Apply cross-engine composition patterns (Brief 028) to build multi-engine seeds. Knows which patterns apply to which engine pairs.
- **Input:** A set of seed proposals from the Schema agent and a target composition (e.g., "character with theme music").
- **Output:** A composition tree of typed seeds with binding edges and chosen composition patterns.
- **Tool access:** None.
- **Stop conditions:** Composition tree complete OR pattern preconditions unsatisfiable.
- **Failure mode:** Returns the partial tree with the unsatisfiable patterns flagged.

### 4. Breeder

- **Role:** Propose breeding operators and parents. Selects from the user's archive or recent generations.
- **Input:** A target intent (e.g., "make this more whimsical") plus the current candidate.
- **Output:** A list of `(parent_seed_ids, operator, params)` tuples ranked by expected fitness.
- **Tool access:** `archive_query`, `lineage_query`. Read-only.
- **Stop conditions:** Top-N proposals generated OR archive empty.
- **Failure mode:** Returns an empty proposal list with a reason. Planner decides whether to fall back to mutation-only.

### 5. Validator

- **Role:** Run the seed validator (Brief 014) and convert errors into repair plans.
- **Input:** A seed (proposal or already-emitted).
- **Output:** Either `Valid` or a typed repair plan with one entry per failed invariant: `(invariant_id, gene_path, suggested_fix)`.
- **Tool access:** `validate`. Pure (no state mutation).
- **Stop conditions:** Validation complete.
- **Failure mode:** N/A — Validator always succeeds in producing a valid/invalid verdict.

### 6. Critic

- **Role:** Score candidates against critic models and rule-based metrics.
- **Input:** A seed and a critic suite specification.
- **Output:** A score table: `{critic_name → score}` with overall ranking.
- **Tool access:** `score`. Pure.
- **Stop conditions:** All requested critics evaluated.
- **Failure mode:** Returns partial scores with the failed critics flagged.

### 7. Researcher

- **Role:** Find relevant priors in the exemplar archive and the user's history.
- **Input:** An intent string or a seed.
- **Output:** A ranked list of `(seed_id, similarity_score, reason)`.
- **Tool access:** `archive_query`, `lineage_query`. Read-only.
- **Stop conditions:** Top-K returned OR query exhausted.
- **Failure mode:** Returns an empty list with a reason.

### 8. Explainer

- **Role:** Generate user-facing explanations of what was produced and why.
- **Input:** The final plan tree and the executed tool-call log.
- **Output:** A short, structured explanation with: (a) what was created, (b) which patterns were applied, (c) which alternatives were considered and rejected.
- **Tool access:** None. Pure summarization with strict templates.
- **Stop conditions:** Explanation complete.
- **Failure mode:** Returns a minimal "produced N seeds for engine E" summary if the full explainer fails.

## Handoff protocol

The Planner is the only sub-agent that can call other sub-agents. The handoff is a typed message with a `request_id`, a `from_agent`, a `to_agent`, an `input` payload, and a `deadline`. The receiving sub-agent must return a response with the same `request_id` before the deadline or it is treated as failed.

**Concurrency:**
- Planner can dispatch multiple sub-agents in parallel when their inputs don't depend on each other (e.g., Schema + Researcher).
- Executor sub-agents (the kernel-facing path) are serialized — the kernel is not multi-tenant from the agent's perspective.

**Memory sharing:**
- Sub-agents do not share working state. All state lives in the plan tree and the kernel-side seed archive.
- The Planner is the only sub-agent that holds the plan tree.

## Risks identified

- **Sub-agent boundaries blur over time** as features ship. Mitigation: a small architectural document per sub-agent; quarterly review for boundary creep.
- **Planner becomes a god object**. Mitigation: the Planner's only job is ToT planning and dispatch; no domain knowledge lives in it.
- **Handoff overhead costs latency**. Mitigation: parallel dispatch where dependencies allow; sub-agents are cheap (each is a focused prompt with a small tool surface).
- **Failure cascades**: a Validator failure forces a re-plan, which forces re-Schema, which forces re-Compose. Mitigation: caching at each sub-agent's output, keyed by input hash.

## Recommendation

1. **Adopt the eight-sub-agent decomposition with the contracts above.**
2. **The Planner is the only sub-agent that can call others.** All others are pure functions.
3. **Each sub-agent has a stable named-prompt template** stored in the agent crate, versioned independently.
4. **Handoffs are typed messages** with request IDs and deadlines.
5. **Caching at each sub-agent boundary** by input hash.
6. **Quarterly architectural review** to catch boundary creep.
7. **Each sub-agent gets a single-page contract document** in `architecture/agents/`.

## Confidence
**4/5.** The decomposition follows clean separation-of-concerns principles and matches established multi-agent patterns. The 4/5 reflects the unmeasured handoff latency cost in practice.

## Spec impact

- `architecture/agent.md` — link to per-sub-agent contracts.
- `architecture/agents/planner.md` … `explainer.md` — eight files.
- `algorithms/sub-agent-handoff.md` — handoff message schema.
- New ADR: `adr/00NN-eight-sub-agent-decomposition.md`.

## Open follow-ups

- Pin the prompt templates per sub-agent (Phase 1 task).
- Decide which sub-agents share a model and which use specialized models.
- Build the handoff message routing layer.
- Empirically measure handoff latency and tune.

## Sources

- Wu et al., *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*.
- LangGraph documentation.
- Internal: Brief 029 (agent architecture), Brief 011 (reliability backstops).
