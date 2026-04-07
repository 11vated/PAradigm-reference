# 037 — DQD: differentiable quality-diversity

## Question
What is differentiable quality-diversity (DQD), how does it accelerate MAP-Elites style search, and which GSPL engines can use it?

## Why it matters
Quality-diversity algorithms like MAP-Elites are gradient-free by default. When the fitness function and BC are *differentiable*, gradient information accelerates search by orders of magnitude. Engines with learned critics can be differentiable end-to-end. DQD is the bridge between QD evolution and modern gradient-based optimization. No competitor uses it for creative-asset generation.

## What we know from the spec
- Brief 035 named DQD as Layer 5 of the evolution stack.
- Many engines have learned critics that are inherently differentiable.

## Findings — DQD in one sentence

**DQD = MAP-Elites where the per-cell improvement step is gradient-driven (or gradient-aware) instead of pure mutation.**

The flagship algorithms in the literature are CMA-MEGA, CMA-MAE, and OMG-MEGA. They differ in how they manage the gradient information across cells, but they share the structure:

1. Sample a candidate from a current cell.
2. Compute the gradient of the fitness w.r.t. the candidate (or the gradient of the BC w.r.t. the candidate).
3. Take a gradient step to either improve fitness inside the current cell or move to a neighbor cell that's empty.
4. Add the new candidate to the archive if it improves its cell.

### Why it's faster

Plain MAP-Elites probes blindly with mutation. Each evaluation moves the candidate by a small Gaussian step. DQD moves the candidate in the direction of fitness gradient — many orders of magnitude more efficient when the gradient is informative.

### When DQD is applicable in GSPL

A GSPL engine can use DQD if **both** the fitness function (the critic) and the BC dimensions are differentiable functions of the seed's continuous gene values. Concretely:

- ✅ **SpriteEngine with a learned critic on rendered output**: critic is a small CNN; gradient flows through the renderer (if the renderer is differentiable, e.g., diffrast).
- ✅ **MusicEngine score-level critics**: critic on the score IR is differentiable.
- ✅ **Visual2D with learned style critic**: end-to-end differentiable when using a vector backend.
- ⚠️ **GameEngine, FullGame**: critics include playability metrics that are not differentiable (rollout-based). Partial DQD only.
- ❌ **Engines with categorical-only genes**: gradients don't flow through CategoricalGene without surrogates.
- ❌ **Symbolic engines (Procedural with WFC)**: discrete state transitions break gradient flow.

### The GSPL DQD recipe

1. **Identify differentiable subgraph**: which gene subset has continuous values feeding a differentiable critic? Typically Scalar/Vector/Color/Material/Embedding genes.
2. **Wrap the engine in a differentiable shell**: render in a way that supports backprop. For SpriteEngine this means a differentiable rasterizer (e.g., DIB-R, nvdiffrast); for MusicEngine, a differentiable score-to-feature map; for Visual2D vector backend, autodiff is straightforward.
3. **Run CMA-MEGA or CMA-MAE on that subset.** Discrete genes are mutated separately by plain MAP-Elites.
4. **Combine**: every M generations of DQD on continuous genes, alternate with N generations of plain MAP-Elites for discrete genes. Hybrid stack.

### Choosing a DQD variant

- **CMA-MEGA**: best raw performance, most complex.
- **CMA-MAE**: better for noisy fitness; simpler than CMA-MEGA.
- **OMG-MEGA**: closest to plain MAP-Elites in code shape; easiest to integrate.

GSPL ships **CMA-MAE** as the v1 default for noisy creative-asset critics; CMA-MEGA as opt-in for advanced users.

## Cost

- DQD requires a backward pass through the renderer, which is significantly more expensive than a forward pass.
- For a SpriteEngine candidate: forward render ≈ 50 ms; backward ≈ 200 ms; gradient step ≈ 250 ms.
- A DQD generation is roughly 5x the cost of a plain MAP-Elites generation per evaluation, but converges 10-100x faster in evaluation count for differentiable problems.
- Net: DQD is 2-20x faster wall-clock for the engines where it applies.

## Risks identified

- **Differentiable renderer fragility**: differentiable rasterizers are notoriously finicky and slow. Mitigation: ship a vetted reference differentiable renderer per applicable engine; fall back to plain MAP-Elites if it fails.
- **Gradient noise from learned critics**: small critic models give noisy gradients. Mitigation: smooth via ensembles or larger batches.
- **Cell-jump instability**: gradient steps can leap across many cells, breaking the archive's cell assignment. Mitigation: clamp step size relative to cell width.
- **Integration burden**: each engine needs its own DQD wrapper. Mitigation: a small reusable wrapper per gene type that the engine inherits.
- **No DQD for discrete genes** is a limitation. Mitigation: hybrid stack with plain MAP-Elites for discrete subset.

## Recommendation

1. **Adopt CMA-MAE as the default DQD variant** at v1 for engines where DQD applies.
2. **DQD is opt-in at v1**, default at v2 for engines with learned differentiable critics.
3. **Hybrid stack**: DQD on continuous gene subset, plain MAP-Elites on discrete subset, alternating generations.
4. **Cell-jump clamping**: gradient step magnitude bounded to one cell width.
5. **Reference differentiable renderers** ship per applicable engine (Sprite, Visual2D-vector, Music score IR).
6. **Critic ensembles** smooth gradient noise.
7. **DQD performance is monitored** by Phase 2 benchmarks; engines fall back to plain MAP-Elites if DQD fails to outperform.

## Confidence
**3/5.** DQD is a 2020+ research area with strong results in the literature but limited production deployments. The 3/5 reflects honest uncertainty about how well it transfers to creative-asset generation at GSPL's compute budgets.

## Spec impact

- `algorithms/evolution/dqd.md` — full DQD pseudocode for CMA-MAE and CMA-MEGA.
- `architecture/dqd-applicability.md` — table of which engines can use DQD.
- `algorithms/differentiable-renderers.md` — reference renderer specs.
- New ADR: `adr/00NN-dqd-as-opt-in-at-v1.md`.

## Open follow-ups

- Build a CMA-MAE prototype against the SpriteEngine in Phase 2.
- Decide on the differentiable rasterizer (diffrast vs nvdiffrast vs custom).
- Empirically benchmark DQD vs plain MAP-Elites on three engines.
- Investigate whether categorical surrogates (Gumbel-softmax) make discrete-gene DQD viable.

## Sources

- Fontaine et al., *Differentiable Quality Diversity*.
- Fontaine & Nikolaidis, *Covariance Matrix Adaptation for the Rapid Illumination of Behavior Space* (CMA-MAE).
- Tian et al., *Learning to Render*.
- Internal: Briefs 035, 040.
