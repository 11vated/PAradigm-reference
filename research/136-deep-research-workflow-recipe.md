# 136 — Deep Research workflow recipe

## Question

What is the end-to-end recipe for the Deep Research workflow Brief 119 specified as a v0.1-eligible plugin — specifically, how does it use the substrate's signed lineage and confidence type to deliver something a research-grade analyst would trust over Gemini Deep Research or Perplexity Pro?

## Why it matters (blast radius)

Deep Research is the most visible high-value workflow Gemini and Perplexity have shipped. If GSPL ships v0.1 with a Deep Research workflow that produces *signed*, *grounded*, *rollback-able*, *confidence-bearing* reports, every other vendor's deep-research tool becomes a black-box demo by comparison. This is the single highest-leverage creator-facing differentiator at launch and a load-bearing entry in Brief 151's communication strategy. If we get it wrong, we cede the most marketable workflow to incumbents.

## What we know from the spec

- Brief 119 (Round 6) lists Deep Research as a v0.1 plugin candidate.
- Brief 120 (Round 6) consolidates the RAG evolution into the federation graph + reranker combination GSPL uses by default.
- Brief 097 (Round 5) defines the grounding floor every claim must clear.
- Brief 091 (Round 4) defines the federated knowledge graph that is the substrate for any retrieval.
- No brief has yet specified the Deep Research workflow as an end-to-end recipe.

## Findings

1. **Deep Research is a five-stage signed pipeline.**
   1. *Intent capture* — user request → router classifies to `research` namespace → planner selects ToT or LATS based on breadth requirement.
   2. *Outline generation* — model produces a hierarchical outline; each outline node carries a *confidence prior* derived from prior knowledge density in the federation graph for that subtopic.
   3. *Evidence gathering* — for each outline node, parallel federation graph walks + ColBERT retrieval + (if grounded enough) external web search via the Brief 099 consultancy network or sanctioned web sources.
   4. *Synthesis* — model writes each outline node, with every claim carrying a parent edge to its evidence source, a three-part confidence score, and a constitutional fence check.
   5. *Sign-and-ship* — the entire report is canonicalized, signed, and stored as a `research-report://` gseed with full lineage.

2. **The confidence-bearing axis is the primary differentiator.** Every claim in the final report carries a visible confidence pill (high / medium / low / disputed). High = grounded by ≥2 independent sources; medium = grounded by 1 source; low = inferred from synthesis; disputed = at least one source contradicts. Gemini and Perplexity show citations but no confidence; GSPL shows both.

3. **Disagreement is rendered explicitly, not hidden.** When two sources contradict, the report includes a "disputed" footnote with both sources and lets the reader decide. This is operationally what the substrate already does (the federated knowledge graph carries multi-source nodes); we just expose it in the report UI.

4. **Web search is bounded by the consultancy network.** GSPL's sanctioned web-search tool only fetches from sources the Brief 099 consultancy network has signed for the relevant namespace, OR from a small fixed set of grounding sources (arXiv, PubMed, government data). This avoids the SEO-spam pollution that plagues Perplexity.

5. **The full report is rollback-able.** Brief 105's rollback primitive applies to research reports as it does to any signed gseed. If a source is later retracted, the report is auto-flagged and the user can either accept the retraction or replay the workflow with the source removed.

6. **Deep Research consumes more tokens than any other v0.1 workflow.** A 5-section report at the floor hardware (32k context) means the kernel must operate in a *streaming* mode: synthesis section by section, with prior sections summarized into working memory. This is identical to the Brief 127 sleep-cycle compaction protocol applied at workflow granularity.

7. **Latency target: 8 minutes for a 5-section report at the floor.** This is competitive with Gemini Deep Research (≈10 min) and Perplexity Pro (≈3 min for shallower reports). The signed/grounded/rollback-able properties are the value delta.

8. **Deep Research is a signed skill gseed.** It lives at `skill://gspl/deep-research/v0.1` per Brief 127's procedural-memory specification. Creators can fork it, parameterize it, and republish forks under their own identity.

9. **Output formats: signed markdown, signed PDF, signed JSON-LD.** The signed JSON-LD is the canonical form; markdown and PDF are deterministic renderings. The signature covers the canonical form, so all three render to verifiable artifacts.

## Risks identified

- **Web search policy is brittle.** Sanctioned-source allowlist is narrow at v0.1. Mitigation: explicit allowlist tied to the consultancy network; federation peers can extend it via signed PRs to the source registry.
- **8-minute latency is optimistic at the floor.** Mitigation: ship a "fast mode" (3 outline nodes, no LATS) that completes in 3 min and a "thorough mode" (10+ outline nodes, full LATS) that completes in 15 min on the floor.
- **Confidence calibration on synthesis claims is the hardest open problem.** Mitigation: borrow Brief 132's calibration methodology; the synthesis-claim confidence head trains on the same accepted/rolled-back signal.

## Recommendation

**Ship Deep Research as v0.1 plugin `skill://gspl/deep-research/v0.1` implementing the five-stage signed pipeline (intent → outline → gather → synthesize → sign-and-ship). Default mode targets 8-minute latency for a 5-section report on the floor hardware. Fast mode (3 sections, no LATS, ~3 min) and thorough mode (10+ sections, full LATS, ~15 min) ship alongside. Web search is bounded by the consultancy-signed source allowlist plus arXiv/PubMed/government baselines. Output as signed JSON-LD canonical with deterministic markdown and PDF renderings. Confidence pills (high/medium/low/disputed) are mandatory on every claim and are derived from the three-part composed confidence type. Deep Research is the headline workflow in the Brief 151 launch communication.**

## Confidence

**4/5.** The pipeline is straightforward composition of existing primitives. The unknowns are: (a) the empirical 8-min latency claim (needs Round 7 measurement), and (b) the exact source allowlist size (consultancy-network-dependent, see Brief 099).

## Spec impact

- `gspl-reference/skills/deep-research-v0.1.md` — new file with the full pipeline spec, three modes, output formats, and confidence pill UI binding.
- `gspl-reference/research/099-lived-experience-consultancy-network.md` — cross-reference at the source-allowlist construction protocol.
- `gspl-reference/research/119-self-improvement-loops.md` — cross-reference at the v0.1 plugin candidate line.
- `gspl-reference/research/151-creator-facing-communication.md` — Deep Research is the headline workflow.

## New inventions

- **INV-564** — *Confidence-pilled research report* with explicit high/medium/low/disputed labels rendered next to every claim, derived from the three-part composed confidence type.
- **INV-565** — *Sanctioned-source allowlist tied to consultancy network.* Web search in Deep Research only fetches from sources the relevant-namespace consultancy network has signed for, plus a small fixed grounding-source set. SEO-spam-resistant by construction.
- **INV-566** — *Rollback-on-retraction.* When any cited source is later retracted, the report is auto-flagged and the user can replay the workflow with the source removed, producing a new signed child report.

## Open follow-ups

- Exact source allowlist size (Brief 099 dependency).
- Whether to ship a "team research" multi-creator variant in v0.1 or v0.2 (defer to Brief 149).
- Confidence pill UX details (defer to Brief 103 composition graph viewer).

## Sources

1. Brief 091 — Federated knowledge graph.
2. Brief 097 — Anti-hallucination test suite and grounding gates.
3. Brief 099 — Lived-experience consultancy network.
4. Brief 119 — Self-improvement loops.
5. Brief 120 — RAG evolution.
6. Brief 127 — GSPL memory and context.
7. Google, *Gemini Deep Research overview*, 2024.
8. Perplexity, *Pro Search documentation*, 2024.
