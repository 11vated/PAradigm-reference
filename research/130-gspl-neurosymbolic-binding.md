# 130 — GSPL neurosymbolic substrate binding (Tier W integration)

## Question

How does GSPL bind the reasoning kernel to symbolic solvers, formal verifiers, and graph-structured world models so that neural reasoning and symbolic guarantees compose natively at the substrate level?

## Why it matters (blast radius)

Every closed frontier lab is building neurosymbolic capabilities bolted onto their models. GSPL's substrate is a signed, typed, content-addressed graph — which is exactly the structure neurosymbolic systems have been trying to reconstruct from raw text for a decade. The binding is where GSPL's structural advantage compounds into raw capability.

## What we know from prior briefs

- **114:** neurosymbolic as primary reasoning topology; substrate primitives as first-class tools; Lean integration for math; unified confidence; JEPA-style predictive embeddings.
- **115:** LATS with substrate-aware value function for verifiable reasoning.
- **117:** primitive tool catalog includes Lean, chemistry, physics, dimensional checker, confidence normalizer, grounding audit, constitutional check.
- **091:** federated knowledge graph is content-addressed with typed edges.
- **100:** 11-edge ontology.
- **096:** identity metric for drift and quality.

## Architecture

### The three symbolic surfaces

1. **Formal verification surface.** Lean 4 proofs for math, type-theoretic correctness for code, dimensional analysis for physics.
2. **Solver surface.** SymPy/SciPy/Z3/ChemPy for computational tasks with deterministic answers.
3. **Graph surface.** The federation graph itself — signed gseeds, typed edges, lineage, constitutional constraints. Every query is a graph query.

### The neural surface

- **Backbone (Brief 110):** Qwen3-MoE-A22B or equivalent.
- **Reasoning kernel (Brief 126):** five planner strategies.
- **Confidence type (INV-348):** unified across all outputs.

### The binding protocol

Neural and symbolic compose through four mechanisms:

#### Mechanism 1: Symbolic tools as primitive actions

Every symbolic surface is exposed as a primitive tool (Brief 128):
- `lean.prove` — submit a goal, get a proof term or failure.
- `solver.chemistry` — submit a reaction query, get a balanced result.
- `solver.physics` — submit a system, get a solution.
- `dim.check` — submit a quantity, get dimensional validity.
- `graph.query` — submit a SPARQL-like query, get typed results.

The neural kernel emits calls; the symbolic backends execute; results return as signed gseeds with full lineage.

#### Mechanism 2: Symbolic verifiers as LATS value functions

Brief 115's LATS strategy uses a value function to prune the search tree. For verifiable-reasoning namespaces, the value function IS the symbolic verifier:

- Math: Lean 4 proof progress.
- Code: test pass rate + type-check pass.
- Physics: dimensional consistency + conservation law checks.
- Chemistry: reaction balance + stoichiometry.

The value function returns a scalar + a certificate. Branches that produce certificates are gold; branches that produce failures are pruned.

#### Mechanism 3: Graph walks as neural retrieval

Brief 127's multi-backend retrieval fusion includes graph-walk as one backend. The walk uses the 11-edge ontology (Brief 100) to propagate relevance: starting from a query embedding, walk typed edges, accumulate relevance scores, return top-K gseeds.

The neural side picks the query. The symbolic side (graph structure) filters and propagates. The result is neurally ranked, symbolically constrained.

#### Mechanism 4: Constitutional commitments as symbolic constraints

The 13 constitutional commitments (Brief 113) are symbolic constraints at generation time:
- Every generated output is checked against each commitment.
- Commitments are declarative — "this output must not misattribute creator work" — and the check is a symbolic function.
- Failure yields a symbolic error (not a neural "this seems off"), which the kernel acts on.

Brief 113's inference-time constitutional pass IS this mechanism.

### The confidence type binding

INV-348's unified confidence type carries:
- **Neural confidence:** from the model's output distribution.
- **Symbolic confidence:** from verifier results (proof pass, test pass, check pass).
- **Graph confidence:** from grounding floor audit.
- **Composite:** a typed product of the three.

Every output carries all three; downstream consumers can filter by any of them. This is unique to GSPL.

### The JEPA-style predictive embedding (optional v2)

Brief 114 recommended JEPA-style predictive embeddings as a world model primitive. In v2, GSPL can train a small predictive model over substrate trajectories:
- Input: the first N turns of a creator session.
- Target: predict the embedding of the Nth+1 turn's gseeds.
- Loss: contrastive with hard negatives.

This gives the kernel a "what might come next" signal for speculative retrieval and pre-computation. It's a v2 lever, not v1.

### The world-model deferral

Full world models (Dreamer, Genie, Sora) are deferred to v2+. The rationale: GSPL's substrate IS a world model at a higher level of abstraction — the relevant "state" is the graph, not pixels. Brief 131 will formalize this.

### Binding to the reasoning kernel (Brief 126)

1. **Router selects strategy based on task namespace.**
2. **For verifiable namespaces,** the LATS strategy is dispatched with the appropriate symbolic verifier as value function.
3. **For all namespaces,** the grounding floor check uses graph-walk retrieval.
4. **Every output passes the constitutional check** before emission.
5. **Every signed output carries the three-part confidence type.**

## Inventions (INV-538 through INV-547)

- **INV-538:** symbolic surfaces as primitive tools with signed-call protocol.
- **INV-539:** LATS value function = symbolic verifier for verifiable namespaces.
- **INV-540:** graph-walk retrieval as neural-ranked, symbolically-constrained backend.
- **INV-541:** constitutional commitments as symbolic constraints at generation time.
- **INV-542:** three-part unified confidence type (neural + symbolic + graph).
- **INV-543:** typed product composition of confidence components.
- **INV-544:** JEPA-style predictive substrate embedding (v2).
- **INV-545:** substrate as world model at gseed-level abstraction (not pixel-level).
- **INV-546:** verifier certificate as first-class signed gseed (on proof/test/check pass).
- **INV-547:** symbolic failure as typed error, acted on by the kernel.

## What makes this unsurpassable

1. **Native substrate = native graph surface.** No other system has a signed, typed graph as its memory layer.
2. **Lean + solvers + graph + constitution as one composable stack.** No other system composes all four.
3. **Three-part confidence type.** No other system unifies neural, symbolic, and grounding confidence.
4. **LATS value function IS the symbolic verifier.** Free pruning from free verification.
5. **Constitutional commitments as declarative symbolic constraints.** No other system has non-amendable declarative constraints at generation time.
6. **World model at gseed abstraction.** Free because the substrate is already there.

## Risks identified

- **Lean and solver setup is heavy.** Mitigation: ship as separate tool servers; primitive tools call them via MCP; creators can install or skip.
- **Verifier timeouts.** Mitigation: budget envelope (Brief 101) caps verifier time; timeout = failure (prune the branch).
- **Graph walks at scale can be expensive.** Mitigation: pre-computed walk indexes for hot namespaces; Brief 101 budget cap.
- **Constitutional check latency.** Mitigation: check is cached per-output fingerprint; only re-runs on substantive changes.
- **Three-part confidence is complex to communicate to creators.** Mitigation: surface the composite by default; expose components on-demand in the studio.

## Recommendation

1. **Primitive symbolic tools ship in v0.1** of the kernel — Lean, solvers, dimensional, grounding, constitutional check.
2. **Graph walk as retrieval backend in v0.1** — it's just another Brief 127 backend.
3. **LATS with symbolic value function in v0.2** — after the primitive tool set is stable.
4. **Three-part confidence type in v0.1** — the type already exists in INV-348; this brief formalizes the binding.
5. **Constitutional check at generation time in v0.1** — load-bearing; already committed in Brief 113.
6. **JEPA predictive embedding deferred to v0.4.**
7. **World model formalization in Brief 131.**

## Confidence

**4.5/5.** Every binding is mechanical composition of existing substrate primitives with open-source symbolic backends. The 3.5/5 piece is LATS value function training for namespaces without a natural verifier — mitigation is to start with hand-crafted values and learn iteratively.

## Spec impact

- Brief 114 this brief operationalizes.
- Brief 115 (LATS) confirms value function = symbolic verifier.
- Brief 091 confirms graph-walk retrieval backend.
- Brief 113 confirms constitutional-check-as-symbolic-constraint.
- Brief 130 this brief completes.

## Open follow-ups

- Solver integration recipes per namespace.
- LATS value function fallback for no-verifier namespaces.
- JEPA predictive embedding dataset construction.
- World model formalization (Brief 131).

## Sources

Briefs 091, 096, 100, 113, 114, 115, 117, 126, 127, 128 and their cited sources.
