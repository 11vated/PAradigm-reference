# 128 — GSPL tool-use and modifier-surface intelligence (Tier W integration)

## Question

How does GSPL extend the Brief 023 modifier-surface DSL into a complete action space that makes every tool call a signed, lineage-tracked, substrate-typed, differentiable operation?

## Why it matters (blast radius)

The action space is where the model touches the world. If it's sloppy, every tool call becomes a hallucination vector; if it's structured, every tool call becomes a reusable, auditable, forkable asset. The difference compounds over months.

## What we know from prior briefs

- **023:** modifier-surface DSL exists as a differentiable, substrate-typed interface.
- **033:** capability-bounded tool access.
- **117:** action-space insights from MCP, Computer Use, Toolformer, Gorilla, xgrammar, CodeAct.
- **118:** multi-agent hand-offs carry signed lineage.
- **121:** Claude Code tool roster and edit-as-diff primitive.
- **123:** parallel tool calling as default.
- **124:** ambient context and preview-with-veto.

## Architecture

### The four action layers

1. **Primitive tools** — deterministic, substrate-native computations.
2. **Substrate tools** — modifier-surface DSL calls on any namespace.
3. **Meta tools** — substrate operations (fork, sign, tombstone, consultancy request).
4. **External tools** — web, file I/O, MCP servers, computer-use (last resort).

All four layers speak the same lineage-tracked signed-call protocol.

### Primitive tool catalog

| Tool | Purpose | Used by strategy |
|---|---|---|
| `graph.query` | SPARQL-like queries on the federation graph | all |
| `graph.walk` | multi-hop traversal with typed edges | ReAct+CoV, LATS |
| `lean.prove` | Lean 4 proof attempt (Brief 114) | LATS, math-answer |
| `solver.chemistry` | chemistry solver (ChemPy/RDKit wrapper) | LATS |
| `solver.physics` | physics solver (SymPy/SciPy wrapper) | LATS |
| `dim.check` | dimensional analysis on a quantity | LATS, math-answer |
| `confidence.normalize` | unified confidence type (INV-348) | all |
| `ground.audit` | grounding floor check on a claim | all |
| `constitution.check` | 13-commitment check on an output | all |
| `identity.metric` | Brief 096 identity metric on an artifact | Self-Refine, procedural promotion |

### Substrate tool (modifier-surface DSL)

The DSL (Brief 023) is the unified interface to:

- **Read:** fetch a gseed by content address, by namespace path, by lineage query.
- **Write:** sign and publish a new gseed; fork an existing one; tombstone one.
- **Modify:** apply a modifier expression to a gseed, producing a new signed gseed with lineage edge.
- **Compose:** combine multiple gseeds via a typed composition expression.
- **Diff:** produce a typed diff between two gseeds (edit-as-diff, INV-493).

All operations are differentiable where the underlying type supports gradients.

### Meta tool catalog

| Tool | Purpose |
|---|---|
| `meta.fork` | create a signed fork with lineage edge |
| `meta.sign` | sign a pending gseed into the creator's namespace |
| `meta.tombstone` | tombstone a gseed with lineage preservation (Brief 102) |
| `meta.consultancy_request` | file a review request with the consultancy network (Brief 099) |
| `meta.council_query` | read the constitutional commitments or council rulings (Brief 107) |
| `meta.rollback` | roll back to a prior gseed (Brief 105) |
| `meta.federation_publish` | publish to federation (Brief 100) |
| `meta.federation_subscribe` | subscribe to a federation feed |

### External tool catalog

| Tool | Purpose |
|---|---|
| `web.search` | Brief 090 web search grounding |
| `web.fetch` | fetch a URL with contextual annotation |
| `file.read` | read a creator-namespace file |
| `file.write` | write a creator-namespace file |
| `file.edit` | apply a diff to a creator-namespace file |
| `shell.run` | run a shell command (sandboxed by default) |
| `mcp.call` | call any MCP-exposed tool (Brief 117 compatibility layer) |
| `computer.action` | last-resort computer-use primitive (Brief 117) |

### Signed call protocol

Every tool call is a signed gseed in `tool-call://<creator>/<session>/<turn>/<call-id>`.

Each call carries:
- **Inputs:** typed, substrate-grounded.
- **Caller:** signed by the agent's identity (creator's namespace).
- **Capability bound:** the permission grant that authorized this call (Brief 033).
- **Result:** the output, also signed.
- **Lineage:** edges to inputs and to the reasoning trace that produced it.

### Structured output grammars

xgrammar-class grammars are pre-compiled at startup for:
- Every primitive tool's input schema.
- The modifier-surface DSL.
- Every meta tool.
- Function-call schemas for all registered external tools and MCP servers.

The model cannot emit an invalid tool call; invalid outputs are masked at decode time.

### Parallel dispatch

Before execution, a dependency analyzer inspects the emitted tool calls and partitions them into parallel batches. Calls with no dependencies run concurrently; dependent calls serialize.

### Preview-with-veto

For sensitive namespaces and modifying tools, the studio shows a preview before execution:
- **Read-only tools:** no preview.
- **Meta tools:** preview.
- **Substrate modify:** preview.
- **External write (file.write, shell.run, web.submit):** preview.
- **Computer use:** always preview.

Per-tool and per-namespace overrides are allowed; overrides are themselves signed gseeds.

### Differentiable action learning

Because modifier-surface calls are differentiable (Brief 023), the agent can:
- Compute gradients on the outcome with respect to modifier parameters.
- Learn to adjust modifiers via backprop during training (Brief 119 self-improvement).
- Use the gradient as an exploration signal at inference time.

This is unique to GSPL. No published agent has a differentiable action space.

## Inventions (INV-515 through INV-526)

- **INV-515:** four-layer action space (primitive/substrate/meta/external) on a unified signed-call protocol.
- **INV-516:** primitive tool catalog with Lean, chemistry, physics, dimensional, confidence, grounding, constitutional, identity-metric.
- **INV-517:** meta tool catalog with fork, sign, tombstone, consultancy, council, rollback, federation.
- **INV-518:** tool-call://<creator>/<session>/<turn>/<call-id> namespace.
- **INV-519:** capability grant carried on every signed tool call.
- **INV-520:** pre-compiled xgrammar-class grammars for every tool schema.
- **INV-521:** dependency-analyzed parallel dispatch for tool batches.
- **INV-522:** tier-based preview-with-veto with per-tool/per-namespace overrides.
- **INV-523:** signed override grants as substrate entities.
- **INV-524:** differentiable modifier-surface calls as a learning signal (Brief 119 feed).
- **INV-525:** MCP compatibility layer that wraps external MCP tools as signed calls.
- **INV-526:** computer-use as last-resort external tool with mandatory preview and sandbox.

## What makes this unsurpassable

1. **Differentiable action space.** No published system has this.
2. **Substrate-typed actions.** Type errors caught at substrate level, not runtime.
3. **Every call is a signed gseed.** Perfect auditability and reusability.
4. **Pre-compiled grammars prevent invalid calls.** No retries for format errors.
5. **Parallel dispatch with dependency analysis.** Latency wins for free.
6. **Capability grants on every call.** Fine-grained security.
7. **Preview-with-veto is signed.** Overrides are auditable.
8. **MCP compatibility.** Creators can bring their tools; GSPL extends them.

## Risks identified

- **Grammar compilation at startup is slow.** Mitigation: warm cache; incremental compilation; compile on first use for rarely-called tools.
- **Signed tool calls bloat the substrate.** Mitigation: lineage-only namespace with aggressive retention (Brief 102); unsigned calls for hot-path ephemeral operations.
- **Capability grants add friction.** Mitigation: creator-level defaults; project-level overrides; session-level overrides.
- **Parallel dispatch race conditions.** Mitigation: dependency analyzer is conservative; ambiguous cases serialize.
- **Differentiable learning is training-data-hungry.** Mitigation: start without it; add when Brief 119 has enough substrate data.

## Recommendation

1. **Ship the four-layer action space in v0.2** of Brief 126's reasoning kernel.
2. **Primitive tool catalog in v0.1** — these are immediately useful and have no substrate dependency.
3. **Substrate tool (modifier DSL) in v0.2** — depends on Brief 023 maturity.
4. **Meta tool catalog in v0.2.**
5. **External tools + MCP compatibility in v0.1** — table stakes.
6. **Differentiable action learning deferred to v0.4** — post-launch optimization.
7. **Pre-compiled grammars in v0.1** for primitive and external tools; extend coverage in later tiers.

## Confidence

**4.5/5.** Every layer is grounded in prior briefs. The differentiable action space is 3.5/5 because it depends on modifier-surface DSL maturity and training data. The rest is straightforward integration.

## Spec impact

- Brief 023 (modifier-surface DSL) needs the "agent is a first-class caller" addendum.
- Brief 033 (permissions) needs signed capability grants.
- Brief 105 (rollback) needs the rollback tool exposure.
- Brief 102 (retention) needs the tool-call namespace policy.
- Brief 117 this brief extends.
- Brief 128 this brief completes.

## Open follow-ups

- Differentiable action learning recipe.
- MCP compatibility layer implementation.
- Grammar compilation performance budget.

## Sources

Briefs 023, 033, 117, 118, 121, 123, 124, and their cited sources.
