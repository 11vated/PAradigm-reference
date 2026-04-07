# 149 — v0.1 scope finalization and feature cuts

## Question

Given the locked architecture (Rounds 1-6), the calibration briefs (132-148), and the budgets (Brief 135 hardware, Brief 145 compute), what is the **exact, non-negotiable** v0.1 scope, and what gets cut to v0.2+?

## Why it matters (blast radius)

Round 7 starts with this scope. Every feature in scope must ship; every feature out of scope must NOT ship. Without a frozen scope, Round 7 drifts, dates slip, and the launch criteria in Brief 105 are violated. This is the most consequential decision brief in Round 6.5 because it controls every subsequent build commitment.

## What we know from the spec

- Brief 108 specifies the year-1 roadmap with v0.1 launch as month 0.
- Brief 105 specifies the launch criteria (1k creators, ship-readiness gates).
- Briefs 126-131 specify the intelligence layer in five-layer detail.
- Briefs 132-148 calibrate the implementation parameters.
- Brief 131 specifies the v0.1 → v0.5 release arc with v0.1 as "launch."

## Findings

### v0.1 IN-SCOPE — substrate (Round 1-2 baseline)

1. **Deterministic GPU + CPU kernels.** WGSL portable subset; CPU fallback path (Brief 075). Single-precision floating point with documented determinism contract per engine.
2. **gseed format v1.** Content-addressed, JCS-canonicalized, signed (RFC 6979 ECDSA p256). zstd-compressed on disk.
3. **Modifier-surface DSL.** Read / write / modify / compose / diff with operator chains canonicalized for shape-equivalence.
4. **Lineage tracking.** Every gseed has parent edges; rollback works to any ancestor.
5. **HM-with-refinements type system.** Strict mode at v0.1.
6. **Three engines at v0.1: image, sprite, character.** Other engines (sound, sim, vehicles, built-world, etc.) defer to v0.2-v0.3.
7. **Local-first storage with optional cloud sync.**
8. **C2PA provenance + watermark on every signed export.**

### v0.1 IN-SCOPE — substrate content (Round 4 baseline)

9. **Foundation kernel** with the 13 non-patchable constitutional commitments.
10. **1,000-seed canonical armory** (Brief 095) covering image, sprite, character at full coverage; partial coverage of math, code, science namespaces.
11. **Federated knowledge graph at ~250k nodes** initial (Brief 140). Federation peer protocol live but with the founder as the only seeded peer.
12. **Universal anything-to-gseed pipeline** (Brief 089) for image and text inputs; defer audio/video to v0.2.
13. **Visual phenomena coverage atlas** (Brief 087) at v0.1 baseline.
14. **Character canon at full v0.1 coverage** (Brief 088).

### v0.1 IN-SCOPE — operations (Round 5 baseline)

15. **Studio IDE** (Brief 048) with composition graph viewer (Brief 103), reference transparency UI, signed-rollback one-click.
16. **First-ten-minutes onboarding** (Brief 104).
17. **Launch criteria gates** (Brief 105): 1k creator capacity, signed launch readiness checklist.
18. **Creator economics tier 1** (Brief 106): free tier + one paid tier ($15/month). Tier 2/3 defer to v0.2-v0.3.
19. **Governance council** (Brief 107) seated with 5 founding members; quarterly review cadence active.
20. **Telemetry + observability** (Brief 056) with privacy-preserving defaults.
21. **Grounding floor and anti-hallucination test suite** (Brief 097) enforced on every signed claim.

### v0.1 IN-SCOPE — intelligence (Round 6 + 6.5)

22. **Five-layer reasoning kernel** (Brief 126) with backbone Qwen3-14B-Thinking at the floor (Brief 135).
23. **Vision tower** Qwen2.5-VL-3B (Brief 137) for image-namespace grounding.
24. **Router classifier** (Brief 132) with cold-start corpus and daily retrain cadence.
25. **Cross-encoder reranker** (Brief 141) distilled from Qwen3-Reranker-7B at ModernBERT-base size.
26. **Five planner strategies** (Brief 126): ReAct, ToT, LATS, Reflexion, Self-Refine. LATS uses the composed value function from Brief 133.
27. **Four-layer action space** (Brief 128) with primitive + substrate + meta + external tools, signed tool calls, xgrammar grammar enforcement (Brief 142).
28. **Four-tier memory** (Brief 127) with sleep-cycle compaction (Brief 138).
29. **Three-part composed confidence type** on every artifact (Brief 130).
30. **Constitutional fence** enforced at every generation step.
31. **Multi-signal stop condition** active (Brief 126).
32. **Trajectory rollback** to any signed state (Brief 105).
33. **Daily cadence** (router, reranker, classifier updates) per Brief 129.
34. **Weekly cadence** (LoRA DPO, eval battery) per Brief 129 + Brief 134.
35. **Monthly cadence** (verifier training, reranker distillation, centroid retraining) per Brief 129.
36. **Quarterly cadence** (council retrospective, multi-judge constitutional benchmark) per Brief 129 + Brief 107.
37. **Continuous drift detector** with auto-rollback (Brief 144).
38. **Differentiable action learning at collection-only.** Data flows; adapter at identity. Learning enables in v0.2 (Brief 143).
39. **Procedural promotion threshold** active with creator-consent prompts (Brief 139).
40. **Federation-shared adapter review** with cross-peer local re-run (Brief 147).
41. **Canonical eval battery** (Brief 134) at three cadences (per-PR fast, weekly full, monthly full+held-out).
42. **Deep Research workflow** as v0.1 plugin (Brief 136) — the headline workflow.

### v0.1 OUT-OF-SCOPE — explicitly cut

- **Audio engine and audio-namespace gseeds.** Defer to v0.2.
- **Video engine and animation pipeline.** Defer to v0.2.
- **Multi-agent topologies (CrewAI/AutoGen-style multi-turn agents).** Bounded sub-agents only at v0.1 (Brief 126); namespace-routed MoE multi-agent defers to v0.3 (Brief 131).
- **Differentiable action learning enabled (vs collection-only).** Defer to v0.2.
- **JEPA predictive embeddings.** Defer to v0.4 (Brief 146).
- **World model `simulate` primitive tool.** Defer to v0.5 (Brief 148).
- **Long-context (128k+).** v0.1 floor is 32k, mid is 128k as upside (Brief 135). Long-context default defers to v0.2.
- **A22B backbone as default.** v0.1 default is Qwen3-14B (Brief 135). A22B is v0.2+ on mid/ceiling tiers.
- **Federation peer pool > 1.** Founder is the only seeded peer at launch; first external peer onboards within 30 days post-launch.
- **Creator tiers 2 and 3.** Paid tier 1 only at v0.1; tiers 2/3 defer to v0.2-v0.3.
- **Mobile clients.** Desktop only at v0.1.
- **Real-time multiplayer / collaborative editing.** Single-creator sessions only.
- **All sim-family engines** (Brief 025): physics, particles, rigid body, soft body. Defer to v0.2.
- **Vehicles, built-world, lifestyle full coverage.** Skeleton coverage only at v0.1; full coverage defers to v0.2.
- **Hand-drawn / cartoon / retro / hand-drawn engine variants** (Brief 024). Defer.
- **AMD ROCm / Intel Arc first-class support.** NVIDIA + Apple Silicon at v0.1; AMD/Intel defer to v0.2.
- **Self-improving language for the core kernel itself** (only artifacts above the kernel learn at v0.1).

### Scope statistics

- **42 in-scope features** spanning substrate, content, operations, intelligence.
- **17 explicit cuts** to v0.2+.
- **Total briefs informing v0.1 scope: 78** (Round 1: 12; Round 2: 28 of 58; Round 3: 4 of 7; Round 4: 12 of 17; Round 5: 14 of 14; Round 6: 6 of 23 [reasoning kernel + memory + tools + improvement loop + binding + differentiable]; Round 6.5: 17 of 20).
- **Total inventions implemented at v0.1: ~140** of 246 (the rest are v0.2+).

## Risks identified

- **42 features is a lot for v0.1.** Mitigation: each in-scope feature is *spec-complete* in the briefs; Round 7 implements rather than designs. The remaining design surface is small.
- **Cuts may be re-litigated later.** Mitigation: this scope is a signed gseed (`scope-v0.1://canonical`) — changes require council review, not unilateral decision.
- **Some cuts are visible to creators (audio, video, multiplayer).** Mitigation: Brief 151 explicitly lists what is and is not in v0.1; messaging is honest.

## Recommendation

**Lock the v0.1 scope at the 42 in-scope features and 17 explicit cuts above. Sign the scope manifest as `scope-v0.1://canonical/v1`. Round 7 implements every in-scope feature; no in-scope feature is dropped without a council review. Cuts cannot be added back to v0.1 without a council review. Brief 151 communicates the scope honestly to creators with explicit "what's coming in v0.2+" language. v0.2 plan opens at month +3 per Brief 131 release arc.**

## Confidence

**5/5.** This is a decision brief, not a research brief. Every line item is grounded in a prior brief. The recommendation is to commit; the evidence supporting commitment is overwhelming.

## Spec impact

- `gspl-reference/scope/v0.1-canonical-manifest.md` — new signed manifest with all 42 in-scope features and 17 cuts. This is the contract Round 7 implements.
- Every brief listed above gets a `v0.1-scope: in` or `v0.1-scope: out` annotation.

## New inventions

- *(none — decision brief)*

## Open follow-ups

- v0.2 scope planning opens at month +3.
- Specific feature-cut messaging (Brief 151).
- Whether the scope manifest itself becomes a federation-published gseed (almost certainly yes).

## Sources

- Briefs 001-148 (every brief contributing to the scope decision).
- Brief 105 — Launch criteria and scaling plan.
- Brief 108 — Year-1 roadmap and milestones.
- Brief 131 — GSPL as a differentiable reasoning substrate (release arc).
- Brief 135 — Hardware budget for v0.1.
- Brief 145 — GPU time cost model.
