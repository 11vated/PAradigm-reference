# 019 — Fisher Information Matrix in seed space: theory and use

## Question
Can the Fisher Information Matrix (FIM) be defined over GSPL seed space, and if so, what does it tell us about gene importance, mutation step sizing, breeding stability, and the geometry of the search landscape?

## Why it matters
Mutation step sizes, crossover blends, and novelty thresholds are currently hand-tuned per gene type. If GSPL had a *principled, per-seed* notion of how sensitive an output is to each gene, every operator could be auto-calibrated. The FIM is the textbook tool for exactly this question in any parameterized model. No competitor in the creative-asset space uses information geometry. This is a differentiator if it works.

## What we know from the spec
- Nothing. This brief is partly an invention proposal embedded in research framing.
- The 17 gene types (Brief 013) define the parameter space.
- The output of an engine is a deterministic function of the seed plus a small random seed.

## Findings — adapting FIM to seed space

**Standard FIM definition:**
For a parameterized probabilistic model `p(x | θ)`, the Fisher Information is:
`I(θ)_ij = E[ ∂log p / ∂θ_i · ∂log p / ∂θ_j ]`

**Adaptation to GSPL:**
GSPL outputs are deterministic given (seed, rng_seed). To define a FIM-like object we need a probability distribution. Two viable framings:

1. **Distribution over rng_seeds** (treat the engine as `p(x | seed) = uniform over rng_seeds`). The FIM measures how sharply the output distribution shifts when a gene changes. This is well-defined, computable by sampling, and has a clean interpretation: "high-FIM genes are the genes whose tweaks cause the biggest output changes on average."

2. **Distribution induced by a perceptual model** (e.g., a CLIP-like embedding model on rendered output, treated as a Gaussian in feature space). The FIM measures how much the perceptual feature distribution moves per gene perturbation. Closer to what humans care about.

**Recommended formulation:** Hybrid. Compute the FIM at three levels:
- **Engine-internal**: log-likelihood under the rng_seed distribution. Cheap, exact.
- **Perceptual**: Gaussian centered at perceptual embedding of output. Moderately expensive, more useful.
- **Behavioral** (for game/sim engines): distribution over emergent metrics (lifetime, score, distance traveled). Most expensive, most semantic.

**What the FIM gives us:**

1. **Per-gene sensitivity** = the diagonal entries `I(θ)_ii`. Sets per-gene mutation step sizes automatically: σ_i ∝ 1/√I_ii. Genes with high information get small steps; sloppy genes get big steps.
2. **Sloppy directions** = small eigenvalues of the FIM. These are gene combinations that don't change the output. Mutating along sloppy directions is wasted compute. Mutating along *stiff* directions (large eigenvalues) is where evolution should focus.
3. **Natural gradient** for any optimization step: `Δθ = I⁻¹ · ∇L`. Replaces hand-tuned step sizes with a geometrically principled update.
4. **Breeding stability**: if two parents differ along a stiff direction, the child is less likely to be a coherent blend. The FIM lets the breeding operator weight crossover by the local geometry.
5. **Novelty distance**: a Mahalanobis-like distance `(s₁ - s₂)ᵀ I (s₁ - s₂)` is more meaningful than naive Euclidean for archive-population diversity.
6. **Compression hint**: sloppy directions can be safely quantized harder in serialization without perceptual loss.

**Computability:**
- Diagonal-only FIM: O(num_genes × num_samples) — cheap, recomputable per seed in seconds.
- Block-diagonal FIM (per gene type): O(genes_per_type² × num_samples) — moderate.
- Full FIM: O(num_genes² × num_samples) — expensive but possible with tens of seconds budget.
- Krylov/Hutchinson trace estimators give sub-quadratic approximations for any of the above.

**Storage:**
- A computed FIM is *metadata*, not part of the seed's content hash. Caching the FIM in a separate sidecar `.fim` file is fine; recomputing is also fine.

## Risks identified

- **FIM is local**: the geometry near the current seed may not generalize to distant seeds. Use is per-seed, not global.
- **Numerical conditioning**: nearly-singular FIMs (very sloppy directions) cause instability in `I⁻¹`. Mitigation: add a small ridge `I + λI` before inversion; tune λ per engine.
- **Compute budget for the perceptual variant** is real. Mitigation: only compute perceptual FIM on demand (e.g., for interactive breeding sessions, not for every evolutionary step).
- **Behavioral FIM depends on the engine implementing a metric stack.** Make this opt-in; engines that don't ship metrics fall back to engine-internal FIM.
- **Premature optimization**: it's possible that hand-tuned per-gene-type step sizes (Brief 013) are good enough and the FIM doesn't pay for its compute cost. Mitigation: A/B test FIM-driven mutation against hand-tuned mutation in Phase 2.

## Recommendation

1. **Adopt the FIM as a normative *optional* mechanism.** Engines that compute it gain auto-tuned mutation; engines that don't fall back to hand-tuned defaults.
2. **Spec a uniform FIM API** in `algorithms/fisher-information.md`: `compute_fim(seed, mode={"engine", "perceptual", "behavioral"}, sparsity={"diagonal", "block", "full"}) → FIM`.
3. **Default mode is "engine" with "diagonal" sparsity**, computable in seconds. Higher modes are opt-in.
4. **FIM is metadata, not content-hashed.** Cached in `.fim` sidecar.
5. **Mutation operators consume the FIM if available**: σ_i ← global_σ / √I_ii (with floor and ceiling).
6. **Novelty distance uses FIM-weighted Mahalanobis** when FIM is available.
7. **A/B test in Phase 2** before promoting FIM-driven mutation to default.
8. **Reserve a `FisherInfo` section ID** in the .gseed format for future inline storage if A/B results justify it.

## Confidence
**3/5.** The math is standard and the sloppy/stiff distinction is empirically ubiquitous in physics and biology models (Sethna et al.). The 3/5 reflects (a) the absence of any prior application to creative-asset evolution and (b) the unproven cost-benefit at GSPL's compute budgets.

## Spec impact

- `algorithms/fisher-information.md` — new file with theory and pseudocode.
- `spec/02-gene-system.md` — note that mutation operators may consume FIM if available.
- `spec/06-gseed-format.md` — reserve `FisherInfo` section ID.
- `evolution/operators.md` — describe FIM-aware mutation as a recognized variant.
- New ADR: `adr/00NN-information-geometry-as-optional-layer.md`.

## Open follow-ups

- Implement the engine-internal diagonal FIM for one engine (recommended: SpriteEngine) as a Phase 1 prototype.
- A/B test FIM mutation vs hand-tuned mutation in Phase 2 on two engines.
- Investigate connection to natural-evolution strategies (NES) for the optimization side.
- Investigate whether FIM eigenvectors form a useful basis for the studio's "interesting variations" UI.

## Sources

- Amari, *Information Geometry and Its Applications*.
- Sethna et al., "Sloppy models, parameter uncertainty, and the role of experimental design" (PLoS Comp. Bio.).
- Wierstra et al., *Natural Evolution Strategies*.
- Internal: Brief 013 (gene types), Brief 035 (evolution stack synthesis).
