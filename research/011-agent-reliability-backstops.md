# 011 — Agent reliability — LLM-to-DSL pipeline error budgets and backstops

## Question
What is the realistic reliability envelope for the GSPL Agent (the LLM that translates natural-language prompts into GSPL DSL programs), and what backstops does the spec need so that user-facing failures stay within an acceptable error budget for a solo-founder operation?

## Why it matters (blast radius)
The GSPL Agent is the user's primary entry point. If it produces broken DSL programs more than a few percent of the time, every user's first impression is "this is unreliable." If the failures are silent (programs that parse but produce wrong output), the product loses trust. Worse, a solo founder cannot afford a 24/7 on-call rotation to triage agent failures, so the system has to fail well on its own. This brief gates `agent/architecture.md` and `agent/reliability.md`.

## What we know from the spec
- `agent/architecture.md` describes a 5-stage LLM pipeline: intent extraction → program sketch → DSL synthesis → type-check & repair → kernel dispatch.
- `agent/reliability.md` is largely empty pending this brief.
- The spec does not yet quantify acceptable failure rates.

## Findings

1. **Constrained DSL generation is dramatically more reliable than free-form code generation in a general-purpose language.** The published Anka DSL benchmark [1] reports that Claude 3.5 Haiku achieves 99.9% parse success and 95.8% overall task accuracy on a 100-problem benchmark in a DSL the model had never been trained on, and notes a 40-percentage-point accuracy advantage over Python on multi-step pipeline tasks (100% vs 60%). The mechanism: the constrained surface eliminates entire classes of errors (state management, ambiguous syntax, multiple valid approaches that the model picks the wrong one of).

2. **Type-constrained decoding reduces compilation errors by ~75% compared to ~9% for syntax-only constraints.** [2, 3] Specifically, type-constrained sampling resolves 50.3% more compilation errors than vanilla LLM decoding [3]. This is the strongest mechanical lever the spec has: forcing the LLM's token output through a real-time type checker during generation, not just after.

3. **Grammar-guided / constrained-decoding tooling is mature** [4, 5, 6, 7]: libraries exist (outlines, lm-format-enforcer, JSON-mode in major API providers, llguidance, xgrammar) that can take a context-free grammar or a set of structural constraints and force the LLM to produce only well-formed outputs. The performance overhead is real but bounded — typically 1.5×-3× slowdown vs unconstrained generation.

4. **Error classes for an LLM → DSL pipeline, in order of severity:**
   - **Parse failures** — DSL doesn't parse. Most common, easiest to fix (constrained decoding eliminates ~all of these).
   - **Type errors** — DSL parses but doesn't type-check. Eliminated almost entirely by type-constrained decoding plus a repair pass.
   - **Refinement / runtime assertion failures** — DSL parses, type-checks, but violates a runtime invariant (out-of-range parameter, etc.). Caught at the kernel boundary per Brief 006.
   - **Semantic mismatches** — DSL is valid but doesn't match user intent. The hardest class. Cannot be eliminated mechanically; must be caught by a preview / approval step.
   - **Hallucinated identifiers** — references to nonexistent functions or types. Type-constrained decoding catches these as type errors; without it, they parse but fail to compile.
   - **Specification gaming** — DSL produces output that satisfies the literal request but misses an implicit constraint. Same severity as semantic mismatch.

5. **Repair passes** (re-prompting the LLM with the type-checker's error message and asking for a fix) [3] can recover from a substantial fraction of type errors that slip past constrained decoding, at the cost of additional latency and tokens. Two-pass repair is the standard pattern; three-pass has diminishing returns.

6. **The "preview before commit" pattern** is the dominant backstop for semantic-mismatch errors. The user sees a render preview before committing the seed to the exemplar archive. This is not perfect (users miss subtle mismatches) but it is the only known general fix.

7. **Test-time compute scaling** (generating multiple candidate programs and ranking them) [1, 5] provides another reliability lever — generate N candidates, type-check all, pick the best by a combination of type score, refinement score, and a learned ranker. Cost scales linearly with N.

## Risks identified

- **Constrained decoding is not supported by all LLM APIs.** The spec must pick an LLM (or a small set) where constrained decoding is available, or build a client-side enforcement layer (more brittle and slower).
- **Type-constrained decoding requires the type checker to be fast enough to run inside the generation loop.** Brief 006's HM Algorithm J is fast enough; refinement-checking via Z3 is not.
- **Latency budget**: a multi-pass agent (constrained generation + type check + repair + preview render) can blow out user-perceived latency. The spec needs to set explicit latency budgets per stage.
- **Cost budget**: two-pass repair plus N-best sampling multiplies token cost by 4×-10× per request. A solo founder must price for this.
- **Model drift** — switching the underlying LLM (or the provider switching it underneath us) can change reliability numbers overnight. The reliability conformance suite must be re-run on every model bump.
- **Silent semantic-mismatch failures** are the residual category that no mechanical backstop fully addresses. The brief recommends explicit user-visible preview as the only sane mitigation.
- **Solo-founder on-call**: the spec must assume no human is in the loop at 3am. Every failure must either retry safely or fall back to a "tell the user, log the issue, do not damage state" path.

## Recommendation

**Adopt a layered reliability architecture with explicit error budgets and hard backstops:**

### Layer 1 — Mechanical correctness (must catch ~99%)

1. **Constrained decoding via a context-free grammar of the GSPL DSL surface.** Pick a tooling stack (outlines / xgrammar / llguidance) at Phase 1 and pin it.
2. **Type-constrained decoding using the v1 HM type checker** from Brief 006. The type checker runs inside the generation loop; tokens that would lead to ill-typed programs are masked from the LLM's output distribution.
3. **One-pass type-error repair**: if any error escapes layers 1 and 2, re-prompt the LLM with the type error message and ask for a fix. Cap repair at one round.

### Layer 2 — Semantic checks (catch the remainder before user-visible commit)

4. **Refinement / runtime assertion checks at the kernel boundary** per Brief 006. Programs that fail here are caught before any output reaches the user.
5. **Render-and-preview**: every generated program runs through the kernel pipeline at low fidelity and the user sees the result before committing the seed.
6. **N-best sampling with type-and-refinement ranking**: generate N=3 candidates by default, type-check all, rank by (type validity, refinement validity, internal heuristic), present the best plus a "show alternatives" affordance.

### Layer 3 — Solo-founder operational backstops

7. **No silent failures.** Every failure path either succeeds with a retry, fails with a user-actionable message, or logs and surfaces an "agent failed, here's why" event. No swallowed errors.
8. **No state damage on failure.** Agent failures must never corrupt the exemplar archive, the seed registry, or any user content.
9. **Per-request budget caps** (latency, tokens, repair attempts). If a request exceeds its budget, it fails clean.
10. **Reliability conformance suite**: a standing suite of N=200+ representative prompts with expected behavior. CI runs it on every model bump; release blocks if reliability drops below thresholds.
11. **Error budgets** (initial targets, to be recalibrated against the conformance suite):
    - Parse failures reaching the user: < 0.1%
    - Type errors reaching the user: < 0.5%
    - Runtime/refinement failures reaching the user: < 1.0%
    - Semantic mismatches caught only at the preview step: < 5%
    - Semantic mismatches reaching commit: < 1%
    - Total user-visible failures: < 2% (excluding preview-level catches)

### Layer 4 — Model and provider hygiene

12. **Pin the LLM model and provider version**, treat bumps as release events with conformance suite re-runs.
13. **Maintain a fallback model** — if the primary fails or returns empty, retry against a secondary model with the same prompt and constraints.
14. **Treat the LLM as an untrusted oracle** — no agent output is trusted until it has passed Layer 1 and Layer 2.

## Confidence
**3/5.** The mechanical reliability levers (constrained decoding, type-constrained decoding, repair) are real and well-published. The published Anka 99.9% parse / 95.8% accuracy numbers are encouraging but were measured on a specific benchmark with a specific model on a specific DSL — they will not transfer 1:1 to GSPL. The 3/5 reflects the genuine uncertainty about (a) whether GSPL's actual reliability hits these numbers without significant tuning and (b) whether the latency/cost budget allows the full layered architecture above. Phase 1 must measure on the real conformance suite before the spec commits to specific error-budget thresholds.

## Spec impact

- **`agent/architecture.md`** — fold in the Layer 1-4 architecture and the explicit pipeline stages.
- **`agent/reliability.md` — REWRITE** with the error budgets, the conformance suite requirement, and the operational backstops.
- **`agent/grammar.md`** — new file specifying the GSPL DSL grammar in a constrained-decoding-compatible form (BNF or similar).
- **`agent/budgets.md`** — new file with the per-request latency, token, and repair-attempt caps.
- **`infrastructure/library-canon.md`** — pin the constrained-decoding library and the LLM model/provider.
- **`infrastructure/ci.md`** — add the reliability conformance suite as a release gate.
- New ADR: **`adr/00NN-agent-reliability-architecture.md`** — record the layered architecture decision.
- New ADR: **`adr/00NN-llm-provider-pin.md`** — record the LLM pin and the bump process.

## Open follow-ups

- Pick the LLM model/provider for v1. This is a real decision that needs separate evaluation; the brief recommends running a small bake-off on a 50-prompt seed of the conformance suite before committing.
- Pick the constrained-decoding library. Survey outlines, xgrammar, llguidance, and any provider-native equivalents.
- Build the 200-prompt reliability conformance suite. Phase 1 task. This is the load-bearing piece of work.
- Decide on the cost model: how many tokens per request is acceptable for a free-tier user vs a paid user?
- Decide whether the agent runs server-side (centralized cost, easier conformance) or supports a client-side mode (privacy, harder reliability tracking). This is a product decision flagged but deferred.

## Sources

1. Anka: A Domain-Specific Language for Reliable LLM Code Generation (arXiv 2512.23214). https://arxiv.org/html/2512.23214
2. Type-Constrained Code Generation with LLMs (OpenReview). https://openreview.net/pdf/fcec8d95bee1e22da4297bbe39c40960fe62ec27.pdf
3. Type-Guided Constrained Decoding: How to Stop LLMs from Hallucinating Code. https://dev.to/delimitter_8b9077911a3848/type-guided-constrained-decoding-how-to-stop-llms-from-hallucinating-code-5hbc
4. Constrained Decoding: Grammar-Guided Generation for Structured LLM Output. https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output
5. Reasoning with constrained LLM generation (CRANE). https://arxiv.org/pdf/2502.09061
6. Awesome-LLM-Constrained-Decoding (curated bibliography). https://github.com/Saibo-creator/Awesome-LLM-Constrained-Decoding
7. From Text to DSL: Evaluating Grammar-Based Model Generation. https://hal.science/hal-05291305v1/document
8. LLM-Hardened DSLs for Probabilistic Code Generation in High-Assurance Systems (Dean Mai). https://deanm.ai/blog/2025/5/24/toward-data-driven-multi-model-enterprise-ai-7e545-sw6c2
