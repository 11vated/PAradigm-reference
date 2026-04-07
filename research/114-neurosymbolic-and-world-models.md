# 114 — Neurosymbolic integration and world models: Dreamer, Genie, V-JEPA, AlphaProof, LeanDojo

## Question

Which parts of GSPL's reasoning stack should be symbolic, which should be neural, which should be bound world-model style, and where does the binding happen?

## Why it matters (blast radius)

GSPL's substrate already is half-symbolic: CODATA physics constants, dimensional analysis, chemistry equations, math axioms, dimensional checking, power-system operator algebra. Neural reasoning on top of a symbolic substrate is a classical neurosymbolic architecture and it is the single most under-exploited lever in AI today. Every closed-lab LLM hallucinates physics because it does not have a solver to call; GSPL has the solver.

The question is how to bind the two without the latency and brittleness classical neurosymbolic systems suffered from.

## What we know from the spec

- Brief 082 (physics constants and laws) commits to dimensional checking as substrate-enforced.
- Brief 081 (chemistry primitives) commits to reaction kinetics as substrate primitives.
- Brief 086B (mathematics) commits to math as a single differentiable substrate.
- Brief 092 (power systems) commits to a six-operator interaction algebra that is literally symbolic.
- Brief 091 (knowledge graph) is content-addressed but is not a "world model" in the Dreamer sense — yet.
- INV-312, INV-326, INV-361 all live in the symbolic region already.

## Findings

### 1. The classical neurosymbolic failure mode

1990s–2010s neurosymbolic systems (Logic Tensor Networks, Neural Theorem Provers, Neural Symbolic Machines) failed on two fronts: the symbolic layer was too rigid to express real-world messiness, and the binding layer (neural-to-symbolic) was too slow and too narrow. [1]

What changed in 2024–2026: LLMs are now strong enough to *call* a symbolic solver reliably, and the solver results are small enough to fold back into the LLM's context without blowing the budget. The binding is "tool call + response" instead of "differentiable gradient flow."

### 2. AlphaProof and AlphaGeometry

DeepMind's AlphaProof (2024) won silver at the International Mathematical Olympiad by combining a neural network (Gemini-based) that proposes proof steps with Lean 4 as the symbolic verifier. Every step the neural network proposes gets checked by Lean; failed steps are discarded; the neural network learns from the verifier's signal. [2]

AlphaGeometry (2024) does the same for geometry with a custom symbolic deduction engine. Published result: IMO gold-medal-level geometry performance from a model much smaller than frontier LLMs. [3]

**The meta-lesson:** a symbolic verifier + neural proposer is strictly stronger than either alone on verifiable tasks, and the binding is mechanically trivial (tool call + feedback loop). This is the single most under-used architectural pattern in production LLM systems.

### 3. LeanDojo and the Lean proof assistant ecosystem

LeanDojo (Yang et al., 2023) provides infrastructure for LLM-Lean interaction and is now the standard research platform. miniF2F and ProofNet are the benchmarks. Published results show small models reaching >40% proof rate on undergraduate-level math with retrieval-augmented Lean interaction. [4]

**Implication for GSPL:** GSPL's math substrate (Brief 086B) already commits to a symbolic layer. Exposing Lean as a tool for the reasoning kernel is nearly free engineering once the substrate integration is in place.

### 4. LLM + solver hybrids for planning and optimization

- **Logic-LM (Pan et al., 2023):** LLM translates natural-language problem → first-order logic → Prolog/Z3 solver → answer. Beats GPT-4 chain-of-thought on logic benchmarks by 20+ points. [5]
- **Chameleon (Lu et al., 2023):** LLM dispatches to a toolbox of calculators, image tools, knowledge bases. General pattern. [6]
- **PAL (Program-aided Language Models):** LLM generates Python code that does the reasoning; the Python interpreter is the "solver." Beats chain-of-thought on math reasoning. [7]
- **Toolformer (Schick et al., 2023):** LLM learns to insert tool-call tokens during generation. [8]

**Common pattern:** the LLM's job is *translation*, not computation. Neural is for fuzzy surface; symbolic is for hard constraints. The binding is the tool-call layer.

### 5. Dreamer-class world models

Dreamer (Hafner et al., 2019–2024) and its successors (DreamerV3, DreamerV4) learn a compressed latent world model and plan by imagining rollouts in the latent space. The world model is a recurrent state-space model trained to predict observations and rewards. Planning is search in latent space. [9]

Dreamer is the canonical world-model architecture in RL. It does not directly apply to language, but the *idea* — a compressed latent that supports imagined rollouts — parallels what a substrate-grounded reasoning kernel does. GSPL's "imagined rollout" is a graph walk; GSPL's "latent" is the content-addressed node embedding.

### 6. V-JEPA and joint embedding predictive architectures

Meta's JEPA line (V-JEPA, I-JEPA, V-JEPA 2) learns a predictive latent without generative decoding. Applied to video, V-JEPA learns physics intuitions (objects persist, supports hold things, gravity points down) from passive video without labels. [10]

The JEPA insight is deep: you do not need to reconstruct to understand. A substrate representation that predicts in latent space is often enough. For GSPL this means the substrate's node embeddings (content-addressed) can be trained to *predict graph neighborhoods* — and doing so gives the reasoning kernel a latent "intuition" about which nodes compose well.

### 7. Genie: interactive generative world models

DeepMind's Genie (2024) and Genie-2 (2024) learn to generate playable 2D and 3D worlds from video data. The model is an interactive latent world model: given a state and a user input, it predicts the next state. [11]

Genie's relevance to GSPL: the substrate's physics, biology, and power-system primitives are *exactly* the kind of structured world knowledge a world model would need. A Genie-style latent wrapped around the substrate would be a generative world model where the physics are grounded by the substrate rather than learned from video. This is a research direction, not a v1 commitment.

### 8. Sora and the generative-as-world-model thesis

OpenAI's Sora (2024–2025) was explicitly framed as "general-purpose simulators of the physical world," not just video generators. The thesis is controversial — Sora demonstrably lacks persistent object physics at long horizons. [12]

The GSPL position: a pure generative world model will always lack the precision a symbolic substrate provides. The right architecture is a generative model that *calls* the substrate for physics, not a generative model that *replaces* physics with learned latents.

### 9. Symbolic distillation

Trauble et al. (2023) and others showed you can distill a trained neural model's behavior into a symbolic program with minimal performance loss on well-structured tasks. This is the opposite direction from classical neurosymbolic: start neural, end symbolic. [13]

For GSPL this matters because some pieces of the reasoning kernel can be distilled from neural to symbolic over time, getting faster and more auditable. The substrate's symbolic layer is the distillation target.

### 10. Confidence propagation and round-trip verification

A neurosymbolic system that calls a solver gets back a symbolic answer with (usually) high confidence. The problem: the neural layer has to decide how to fold that confidence into its final natural-language response. Published work on confidence propagation is thin. [14]

**GSPL's advantage:** every substrate value carries a confidence score by construction (INV-348). The solver's confidence plugs into the same confidence type. No custom fusion logic needed.

## Inventions to absorb

Tier W hooks for Brief 130:

- **Symbolic substrate as first-class reasoning tool.** The reasoning kernel calls chemistry, physics, math, and operator-algebra substrate primitives like any other tool (Brief 117 + Brief 128).
- **Lean (or equivalent) proof assistant integration for math namespace.** Follows the AlphaProof pattern.
- **LLM-as-translator, substrate-as-computer.** The neural reasoning kernel translates fuzzy creator intent into substrate calls; the substrate does the hard computation; the neural layer narrates the answer.
- **Confidence propagation is unified.** Substrate confidence (INV-348), solver confidence, and neural confidence all share the same type. No custom fusion logic.
- **JEPA-style substrate embeddings.** Node embeddings are trained to predict graph neighborhoods; this gives the reasoning kernel a "composition intuition" even before it queries the graph explicitly.
- **World-model wrapper as v2 research direction.** Genie-style generative world model that calls the substrate for physics rather than learning its own. Not v1.
- **Symbolic distillation as a continuous pressure.** Parts of the reasoning kernel that stabilize get distilled into symbolic substrate primitives over time.

## Risks identified

- **Symbolic solvers are slow.** Mitigation: fast solvers for common cases (dimensional checks are O(1)); offload hard solvers (Lean proofs) asynchronously; cache proof gseeds.
- **Natural language → symbolic translation is error-prone.** Mitigation: round-trip verification — solver's answer gets re-verified against the substrate before emission.
- **Users don't know when the solver ran.** Mitigation: the composition graph viewer (Brief 103) shows every solver call as a node with provenance.
- **World-model wrapper is a research risk.** Mitigation: explicitly deferred to v2.
- **Distillation can regress behavior.** Mitigation: distilled primitives are versioned gseeds with reversible promotion.

## Recommendation

1. **Neurosymbolic architecture is GSPL's primary reasoning topology.** Neural kernel translates; substrate computes. This is not a feature; it is the load-bearing beam.
2. **Substrate primitives are first-class tools** (Brief 117, 128). Chemistry, physics, math, power-system operators, dimensional checking, cultural attribution — all are callable by the reasoning kernel.
3. **Lean proof assistant integration** for the math namespace (Brief 086B). Published AlphaProof/LeanDojo pattern is the template.
4. **Confidence is one type across neural, symbolic, and substrate layers.** Brief 348 already committed to this.
5. **JEPA-style predictive embeddings** on substrate graph nodes. Gives the kernel composition intuition.
6. **World-model wrapper deferred to v2.** Genie-style generative wrapper is a research direction, not a v1 commitment.
7. **Symbolic distillation is a continuous pressure,** not a launch feature. Stabilized reasoning becomes symbolic substrate over time.

Feeds Brief 130 (neurosymbolic substrate binding) directly. Cross-references Brief 126 (reasoning kernel) and Brief 128 (tool-use).

## Confidence

**4.5/5.** The AlphaProof / Logic-LM / PAL pattern is well-published and production-ready. The GSPL-specific wins (substrate primitives as tools, confidence propagation without fusion) work because the substrate already commits to the right primitives in Round 4. The world-model wrapper is the only 3/5 piece, and it's explicitly deferred.

## Spec impact

- Brief 086B (math substrate) needs Lean integration recipe.
- Brief 117 / Brief 128 need substrate primitives added to the first-class tool list.
- Brief 130 owns the full binding.

## Open follow-ups

- Solver latency budgets across substrate namespaces.
- Whether to ship with Lean or a lighter verifier at launch.
- JEPA-training recipe for substrate node embeddings.
- v2 world-model wrapper exploration scoping.

## Sources

1. Garcez & Lamb, "Neurosymbolic AI: The 3rd Wave," 2020.
2. DeepMind, "AI achieves silver-medal standard solving International Mathematical Olympiad problems," Jul 2024.
3. Trinh et al., "Solving olympiad geometry without human demonstrations," Nature, 2024.
4. Yang et al., "LeanDojo," NeurIPS 2023. arXiv:2306.15626.
5. Pan et al., "Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning," 2023. arXiv:2305.12295.
6. Lu et al., "Chameleon: Plug-and-Play Compositional Reasoning," 2023.
7. Gao et al., "PAL: Program-aided Language Models," 2022.
8. Schick et al., "Toolformer: Language Models Can Teach Themselves to Use Tools," 2023.
9. Hafner et al., "Mastering Diverse Domains through World Models (DreamerV3)," 2023.
10. Bardes et al., "V-JEPA 2," Meta, 2024.
11. DeepMind, "Genie: Generative Interactive Environments," 2024.
12. OpenAI, "Video generation models as world simulators (Sora technical report)," 2024.
13. Trauble et al., "Discrete Latent Bottleneck for Symbolic Distillation," 2023.
14. Various, 2023–2025.
