# 117 — Tool-use and action-space design: MCP, Computer Use, function calling, Toolformer, Gorilla, constrained grammars

## Question

What is the best action-space and tool-use discipline for GSPL's agent, given that every tool call must be a signed lineage-bearing gseed and every tool must honor the grounding floor?

## Why it matters (blast radius)

Tool-use is where reasoning meets the world. A sloppy action space leaks capabilities, confuses grounding, and breaks lineage. A well-designed action space turns every tool call into an auditable, reusable, forkable substrate event.

## What we know from the spec

- Brief 023 (modifier-surface DSL) commits to a differentiable modifier surface — this is already an action space, not just a function-call API.
- Brief 033 (agent permission model) commits to capability-bounded tool use.
- Brief 091's knowledge graph tracks tool calls as first-class citizens (implicitly).

## Findings

### 1. The four layers of tool-use

Any production tool-use system has to solve four problems:

- **Discovery:** how the agent learns what tools exist.
- **Selection:** how the agent chooses which tool to call.
- **Invocation:** the mechanical act of calling (format, types, errors).
- **Integration:** how the result feeds the next reasoning step.

Published systems differ mostly on layer 3 (invocation) and layer 4 (integration); layer 1 (discovery) and 2 (selection) are less studied. [1]

### 2. Function calling (OpenAI, Anthropic, Gemini, Qwen, open-source)

The dominant modern pattern: tools are JSON-schema-described functions; the model emits a JSON tool call; the runtime executes and returns a JSON result; the model continues. Every frontier lab ships this. [2]

- **Strengths:** standardized, works across models, easy to implement, good for structured operations.
- **Weaknesses:** JSON is lossy (no structural types, no differentiability); schemas grow unwieldy; no lineage; no grounding.

### 3. MCP: Model Context Protocol

Anthropic's Model Context Protocol (2024) standardizes how tools are discovered, authenticated, and invoked across LLM runtimes. MCP servers expose tools; MCP clients (LLM apps) consume them. [3]

- **Strengths:** the first serious attempt at a *standard* tool interface; growing ecosystem; discoverability-first design.
- **Weaknesses:** tools are still opaque to the model beyond JSON descriptions; no substrate-native extensions; no lineage.

### 4. Computer Use (Claude)

Anthropic's Computer Use (2024) lets Claude control a computer via screenshots + mouse/keyboard primitives. The action space is low-level and the observation space is visual. [4]

- **Strengths:** universal (any software becomes usable); emergent capability for UI-bound tasks.
- **Weaknesses:** slow (each step is a screenshot + OCR + decision); error-prone; hard to audit; state tracking is brittle.

### 5. Toolformer and self-teaching

Schick et al. (2023). Model is trained to insert tool-call tokens during generation; during training, tools are called and the results replace the tool-call tokens if they improve downstream prediction. [5]

- **Strengths:** tool use is baked into the model distribution; no separate tool loop.
- **Weaknesses:** training requires tool access during pretraining; limited to small tool sets; hasn't scaled to frontier.

### 6. Gorilla and tool retrieval

Patil et al. (2023). Fine-tuned LLM that can call 1600+ APIs by retrieving tool documentation at query time. Shows that tool use scales with retrieval, not context window. [6]

- **Strengths:** scales to large tool libraries; retrieval is free plumbing.
- **Weaknesses:** retrieval quality gates everything; no grounding of the result.

### 7. Structured output grammars: Outlines, Guidance, xgrammar, Lark

The "constrain the output at decode time" approach. Rather than hoping the model emits valid JSON, force it to by masking invalid tokens during sampling. [7][8]

- **Strengths:** 100% schema-valid output by construction; zero retries; fast.
- **Weaknesses:** some grammars are expensive to compile; aggressive masking can hurt quality on edge cases.

This is critical for GSPL: every tool call is a structured artifact, and structured output grammars are how you get reliability without retries.

### 8. The action-space-as-DSL pattern

A few systems (CodeAct, Voyager's Minecraft agent, SWE-agent) expose actions as a programming language rather than a function-call JSON API. The agent writes code; the code is executed; the result is observable state. [9][10][11]

- **Strengths:** fully expressive, supports loops/conditions/composition; the model can script multi-step tool use in one emission.
- **Weaknesses:** code can break; sandboxing is hard; errors are harder to recover from than a single function-call error.

### 9. The modifier-surface insight (GSPL-specific)

GSPL's Brief 023 already commits to a modifier-surface DSL: the substrate exposes differentiable knobs that creators (and agents) pull. This is *already* a programming language action space, but with two properties that generic code doesn't have:

- **Differentiability.** Every modifier has a gradient. An agent can learn to adjust modifiers by backprop, not just by trial and error.
- **Substrate-native typing.** Every modifier is typed by its namespace (a chemistry modifier is different from a culture modifier). Type errors are caught at substrate level, not at runtime.

No published tool-use system has a differentiable, substrate-typed action space. This is a GSPL-native lever.

### 10. Lineage-tracked tool calls

Every published tool-use system treats a tool call as a transient event. GSPL treats every tool call as a signed event. The tool call is a gseed in a lineage-only namespace (e.g., `tool-call://`, matching the Round 5 lineage-only pattern). This has three wins:

- **Auditability:** every call is reviewable forever, not just until the session ends.
- **Reusability:** a successful call sequence can be replayed, forked, or edited.
- **Grounding:** the call's result is cited in every downstream reasoning step.

### 11. The four-layer GSPL action space

- **Primitive tools:** graph queries, chemistry solver, physics solver, Lean proof (Brief 114), dimensional checker, identity metric calculator (Brief 096), confidence normalizer.
- **Substrate tools:** modifier-surface DSL pulls on any namespace. The agent writes modifier-surface expressions, not function calls.
- **Meta tools:** fork a gseed, sign a new one, tombstone, request consultancy review (Brief 099), query the constitutional commitments.
- **External tools:** web search (Brief 090), partner archive fetches (Brief 098), file I/O in the creator's namespace.

All four layers speak the same lineage-tracked signed-call protocol.

## Inventions to absorb

Tier W hooks for Brief 128:

- **Every tool call is a signed gseed.** Lineage-only namespace; no new substrate primitive.
- **Structured output grammars** enforce valid tool calls at decode time. xgrammar-class; no retries.
- **Action space is the modifier-surface DSL**, extended with primitive/substrate/meta/external tools. The substrate DSL is the base action type; everything else is a call into it.
- **Differentiable action space.** Every modifier has a gradient; the agent can learn via backprop.
- **Substrate-typed actions.** Type-checked at substrate level before execution.
- **MCP compatibility layer** so creators' existing MCP servers Just Work.
- **Computer-use as last-resort external tool.** Only when no substrate-native tool exists; sandboxed via Brief 045 (anti-piracy / leak resilience) principles.

## Risks identified

- **Grammar compilation is slow for complex schemas.** Mitigation: pre-compile all substrate DSL grammars at startup; warm cache.
- **Agents over-call tools.** Mitigation: tool-call budget included in Brief 101 envelope.
- **Tool calls can leak private data.** Mitigation: capability-bounded tool access from Brief 033; private namespaces are off-limits to external tools.
- **The modifier surface is a lot to learn.** Mitigation: progressive disclosure in the studio (Brief 103); the agent learns it first, then teaches it to the creator.
- **MCP ecosystem has variable quality.** Mitigation: MCP tools are external by default and subject to grounding audit.

## Recommendation

1. **Action space is the Brief 023 modifier-surface DSL**, extended to cover primitives, substrate operations, meta operations, and external tools.
2. **Every tool call is a signed gseed** in a lineage-only namespace. No new substrate primitive.
3. **xgrammar-class structured output grammars** enforce valid calls at decode time.
4. **MCP compatibility layer** for creator-facing external tools.
5. **Differentiable substrate actions** are a first-class learning surface (feeds Brief 129 self-improvement).
6. **Computer-use is last-resort external**, sandboxed.
7. **Tool-call budget is a line in the query envelope** (Brief 101).

Feeds Brief 128 (tool-use and modifier-surface intelligence).

## Confidence

**4.5/5.** Every published tool-use technique cited is mature. The GSPL-specific lever (modifier-surface DSL as the action space, with differentiability) is novel but mechanically straightforward because Brief 023 already commits to the surface.

## Spec impact

- Brief 023 (modifier-surface DSL) needs the "agent is a first-class caller" addendum.
- Brief 033 (agent permission model) needs the capability-bounded external tool rule.
- Brief 128 owns the integration.

## Open follow-ups

- MCP compatibility layer implementation details.
- Differentiable action learning recipe.
- Substrate DSL grammar compilation optimization.

## Sources

1. Qin et al., "Tool Learning with Foundation Models," 2023.
2. OpenAI / Anthropic / Google function-calling documentation, 2024–2025.
3. Anthropic, "Model Context Protocol," 2024.
4. Anthropic, "Claude's Computer Use," Oct 2024.
5. Schick et al., "Toolformer: Language Models Can Teach Themselves to Use Tools," 2023.
6. Patil et al., "Gorilla: Large Language Model Connected with Massive APIs," 2023. arXiv:2305.15334.
7. Willard & Louf, "Efficient Guided Generation for Large Language Models (Outlines)," 2023.
8. Dong et al., "xgrammar: Flexible and Efficient Structured Generation," 2024.
9. Wang et al., "CodeAct: Executable Code Actions Elicit Better LLM Agents," 2024.
10. Wang et al., "Voyager: An Open-Ended Embodied Agent with Large Language Models," 2023.
11. Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," 2024.
