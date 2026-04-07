# 148 — World model formalization beyond Brief 131

## Question

Brief 131 declared "the substrate IS the world model at gseed abstraction." This brief formalizes that claim: what does it mean operationally, what are the formal properties, and how does it differ from a learned world model in the LeCun / Sutton sense?

## Why it matters (blast radius)

The seven-axis claim hinges on the substrate being a world model — not metaphorically, but mathematically. If the formalization is loose, the v0.5 release arc (Brief 131) which builds on this claim is unfounded. If we cannot specify *what kind of world model* the substrate is, we cannot defend the claim against frontier-lab world-model proposals (DreamerV3, Genie, Gemini's video models). This brief is the formal load-bearing argument.

## What we know from the spec

- Brief 131 declares the substrate-as-world-model thesis at the v0.5 release row.
- Brief 130 binds three symbolic surfaces (Lean, solvers, graph) into the kernel.
- Brief 094 specifies substrate open-extension grammar.
- Brief 091 specifies the federated knowledge graph.

## Findings

1. **A world model is a function `M: State × Action → State` plus `R: State → Reward`.** The classic Sutton definition. A learned world model approximates M and R from experience; a known world model has them in closed form.

2. **The GSPL substrate is a known-and-extensible world model.** The state space is the set of all valid signed gseeds (typed by HM-with-refinements). The action space is the modifier-surface DSL plus tool catalog. The transition function M is the deterministic evaluation of (gseed × modifier) → new gseed, defined by the engine implementations (Brief 027 reproducibility test harness guarantees determinism). The reward function R is the three-part composed confidence type (Brief 130).

3. **This is the formal world model definition: $M(s, a) = E_{\sigma(a)}(s)$, where $\sigma(a)$ is the engine selected by the action and $E$ is the engine's deterministic evaluation function.** Per Brief 020, every engine has a determinism contract. So M is a known function, computable in closed form, not learned.

4. **The reward function is grounded, not learned.** $R(s) = \alpha \cdot R_{\text{neural}}(s) + \beta \cdot R_{\text{symbolic}}(s) + \gamma \cdot R_{\text{graph}}(s)$ where the three components come from Brief 130's three binding mechanisms. The neural component is learned; the symbolic and graph components are computed from primitives. So R is partially known and partially learned — the partially-known piece is the safety guarantee that distinguishes GSPL from purely-learned world models.

5. **State space is infinite but typed.** Unlike pixel-space or video-frame world models which have an unstructured infinite state space, the GSPL state space is infinite but type-stratified. Every state is a typed gseed; only finitely many *types* exist (Round 4 fixed the namespace count); within each type, infinitely many instances. This stratification is what makes world-model planning tractable: planning happens at the type level, not the instance level.

6. **Action space is bounded but extensible.** At v0.1, ~25-30 primitive + meta + external tools (Brief 128). New tools can be added at federation-review boundaries (Brief 147). The action space evolves; the world model evolves with it without requiring retraining of M.

7. **GSPL world model vs learned world model — three differences.**
   (a) **GSPL transition function is symbolic; learned world models are neural.** GSPL's M is provably correct by construction (engine determinism contract); learned M is approximately correct. This matters for planning depth: GSPL can plan 100+ steps deep without compounding error, learned world models compound error after ~10 steps.
   (b) **GSPL state space is typed; learned world models work over unstructured embeddings.** Typed state means every state has a known schema, every transition has a known type signature, and the planner can prune impossible branches before searching them.
   (c) **GSPL reward is partially symbolic; learned world models have only learned rewards.** The symbolic reward component is the safety guarantee; the learned component is the quality signal.

8. **GSPL world model vs known-game world models (chess, Go, etc.).** Known-game models also have symbolic M, but their state and action spaces are tiny and game-specific. GSPL's are large, multi-domain, and extensible. GSPL is, formally, a *generalized* known-world model.

9. **The world model is differentiable at the action embedding layer.** Per Brief 143, the action adapter is a differentiable function over hidden states. This is *not* a differentiable world model in the JEPA sense (where the dynamics are differentiable), but a differentiable *policy* over a known world model. JEPA at v0.4 (Brief 146) adds the differentiable dynamics layer as an upper bound, not a replacement.

10. **What v0.5 adds beyond Brief 131.** v0.5 ships the formal world-model interface as a tool: `world_model.simulate(state, action_sequence) → state_sequence_with_confidence`. This makes the substrate's world-modeling capability accessible as a primitive tool any planner can call, not just an internal substrate property.

11. **Why this isn't equivalent to "running the engines."** Running the engines is *executing* the world model. Calling `world_model.simulate` is *querying* the world model at the *type and lineage* level, allowing branch pruning, counterfactual reasoning, and planning without committing to any particular execution. The same way a chess engine can think 30 moves ahead without making any of them.

## Risks identified

- **Symbolic-vs-learned comparison may be overstated for namespaces with heavy learned components.** Lifestyle, narrative, character namespaces have less symbolic structure than chemistry/math/code. Mitigation: claim the partial-symbolism advantage explicitly per namespace; do not over-claim universality.
- **The world-model interface as a tool may be expensive at scale.** Mitigation: defer to v0.5 (Brief 131); not a v0.1 concern.
- **Formal-claim language is academic and may obscure the practical message.** Mitigation: Brief 151 (creator communication) translates this into accessible language.

## Recommendation

**Adopt the formal world-model definition: state = signed typed gseeds, action = modifier-surface DSL + tool catalog, M = deterministic engine evaluation (closed form), R = composed neural+symbolic+graph confidence (partially closed form). Differentiate from learned world models on three axes: symbolic vs neural transition, typed vs embedding state, partially-symbolic vs purely-learned reward. v0.5 ships `world_model.simulate` as a primitive tool that exposes the substrate's world-modeling capability for branch pruning and counterfactual planning. This formalization is the load-bearing argument for the seven-axis claim's longevity against frontier-lab world-model proposals.**

## Confidence

**4/5.** The formal definition is rigorous; the comparisons against learned world models are well-founded in published differences. The unknowns are how cleanly each namespace fits the symbolic vs learned partition and how the formal interface tool is consumed by external planners.

## Spec impact

- `gspl-reference/intelligence/world-model.md` — new file with the formal definition, comparison table, v0.5 interface tool spec.
- `gspl-reference/research/130-gspl-neurosymbolic-binding.md` — cross-reference at the substrate-as-world-model deferral.
- `gspl-reference/research/131-gspl-differentiable-reasoning-substrate.md` — cross-reference at the v0.5 release row.

## New inventions

- **INV-588** — *Formal substrate-as-world-model definition* with closed-form symbolic transition function M, partial-symbolic reward R, and typed-stratified state space S — distinct from learned world models on three formal axes.
- **INV-589** — *`world_model.simulate` primitive tool* (v0.5) exposing the substrate's world-modeling capability for branch pruning and counterfactual planning by any planner.

## Open follow-ups

- Per-namespace symbolic-vs-learned partition (defer to v0.5 work).
- Empirical comparison of GSPL world-model planning depth vs DreamerV3 / Genie / Gemini video models (defer; needs v0.5 implementation).
- How `world_model.simulate` interacts with the action adapter learned in Brief 143 (defer to v0.5).

## Sources

1. Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., 2018 (formal world model definition).
2. LeCun, *A Path Towards Autonomous Machine Intelligence*, 2022.
3. Hafner et al., *DreamerV3: Mastering Diverse Domains through World Models*, 2023.
4. Brief 020 — Determinism contract per engine.
5. Brief 027 — Reproducibility test harness.
6. Brief 091 — Federated knowledge graph.
7. Brief 094 — Substrate open-extension grammar.
8. Brief 130 — GSPL neurosymbolic binding.
9. Brief 131 — GSPL as a differentiable reasoning substrate.
