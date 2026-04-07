# Fisher Information Matrix Approximation

## What it does

The Fisher Information Matrix (FIM) is the local geometric structure of a parametric family of probability distributions. In Paradigm, it's the **Riemannian metric** on the SeedManifold (Layer 1) — it tells us how "different" two seeds are by measuring how distinguishable their *output distributions* are, not how different their parameter vectors look.

This matters because seed parameters are often non-Euclidean: a small change in a temperature gene can be enormous (different output regime), while a large change in a rarely-used gene is meaningless. The FIM corrects for this by giving us a metric where "distance 1" always corresponds to "one standard deviation of perceptible output change."

## Mathematical definition

For a parametric distribution `p(x | θ)`, the Fisher Information Matrix is:

```
F(θ)_{ij} = E_{x ~ p(x|θ)} [ ∂/∂θ_i log p(x|θ)  ·  ∂/∂θ_j log p(x|θ) ]
```

Equivalently, under regularity conditions:

```
F(θ)_{ij} = -E_{x ~ p(x|θ)} [ ∂² log p(x|θ) / ∂θ_i ∂θ_j ]
```

The FIM is symmetric, positive semi-definite, and gives the Cramér-Rao lower bound on parameter estimation variance: `Var(θ̂) ≥ F(θ)^(-1)`.

## Why we want it

- **Natural gradient.** `θ_{t+1} = θ_t - η F(θ)^(-1) ∇L(θ)` is the natural gradient. It's invariant to reparameterization, which means the optimization is robust to how we name our genes.
- **Distance metric.** `d(θ_1, θ_2)² ≈ (θ_1 - θ_2)^T F((θ_1 + θ_2)/2) (θ_1 - θ_2)` for nearby parameters. This is the **Fisher-Rao distance**, used by Paradigm for seed similarity searches.
- **Sensitivity analysis.** Eigendecomposition of `F(θ)` reveals which gene combinations are "stiff" (small changes have huge effects) vs. "sloppy" (large changes have no effect). The studio's gene-editor uses this to scale slider sensitivities.

## The exact computation is intractable

For a Paradigm seed, `p(x | θ)` is the implicit distribution defined by *running the engine* on the seed and observing the output. We have no closed form. We must approximate.

## Empirical FIM (observed information)

The most useful approximation: replace the expectation with a Monte-Carlo average over samples drawn by re-running the engine with different RNG substreams.

```
fn empirical_fim(seed: Seed, n_samples: int, rng: Rng) -> matrix:
    let theta = extract_continuous_genes(seed)
    let n = theta.length
    let mut fim = zero_matrix(n, n)

    for sample in 0..n_samples:
        let substream_rng = substream(&rng, format("fim_sample:{}", sample))
        let log_p_grad = score_function(seed, &substream_rng)
        // log_p_grad is the gradient of log-likelihood at theta, shape (n,)
        let outer = outer_product(log_p_grad, log_p_grad)
        fim = matrix_add(fim, outer)

    return scalar_mat_mul(1.0 / n_samples as float, fim)
```

The score function `∂/∂θ log p(x|θ)` requires either:

1. **Reparameterization trick:** if the engine has differentiable noise injection (like a VAE), we can compute the gradient directly via autodiff.
2. **REINFORCE estimator:** for non-differentiable engines, `∇log p ≈ (output_perturbed - output_baseline) / σ²` via finite differences.

## Diagonal-only approximation

For high-dimensional seeds (n > 100), the full FIM is `O(n²)` storage and `O(n³)` to invert. Paradigm uses the **diagonal approximation** by default, which assumes gene independence:

```
fn diagonal_fim(seed: Seed, n_samples: int, rng: Rng) -> vec<float>:
    let theta = extract_continuous_genes(seed)
    let n = theta.length
    let mut diag = zeros(n)

    for sample in 0..n_samples:
        let substream_rng = substream(&rng, format("fim_diag:{}", sample))
        let log_p_grad = score_function(seed, &substream_rng)
        for i in 0..n:
            diag[i] += log_p_grad[i] * log_p_grad[i]
    return diag.map(|d| d / n_samples as float)
```

The diagonal FIM gives per-gene curvature without the cross-terms. It's `O(n)` storage, `O(n)` invert, and good enough for the gene-editor sensitivity scaling.

## K-FAC approximation

For mid-sized seeds (n in 100-1000) where the diagonal is too coarse but the full matrix is too expensive, Paradigm uses **K-FAC** (Kronecker-Factored Approximate Curvature, Martens & Grosse 2015): `F ≈ A ⊗ B` where `A` is the per-layer input covariance and `B` is the per-layer gradient covariance. K-FAC is `O(n^(4/3))` and approximates the full FIM well for layered/structured seeds.

## Empirical FIM via output perturbation (engine-agnostic)

The most engine-agnostic FIM approximation: treat the output of the engine as a multivariate Gaussian and measure its Jacobian with respect to the seed parameters.

```
fn jacobian_fim(seed: Seed, output_fn: fn(Seed) -> vec<float>, eps: float) -> matrix:
    let theta = extract_continuous_genes(seed)
    let n = theta.length
    let baseline_output = output_fn(seed)
    let m = baseline_output.length
    let mut jacobian = zero_matrix(m, n)
    for i in 0..n:
        let mut perturbed_seed = seed.clone()
        perturbed_seed.genes[i] += eps
        let perturbed_output = output_fn(perturbed_seed)
        let column = vec_scalar_mul(vec_sub(perturbed_output, baseline_output), 1.0 / eps)
        for j in 0..m:
            jacobian[j][i] = column[j]
    // F ≈ J^T J (the Gauss-Newton approximation, exact for Gaussian outputs)
    return mat_mul(transpose(jacobian), jacobian)
```

This is the FIM that Paradigm actually computes by default in the studio because it requires no autodiff and works on any engine.

## Use 1: Natural gradient for evolution

When CMA-ES updates the mean, multiplying the update by `F^(-1)` gives a *natural* update that's invariant to reparameterization:

```
delta_natural = inv(F) * delta_euclidean
```

The Paradigm CMA-ES variant supports a `natural_gradient: true` config flag which, when set, multiplies the mean update by the inverse FIM at each step. This typically improves convergence by 2-5× on heterogeneous-scale gene spaces.

## Use 2: Fisher-Rao distance for similarity search

```
fn fisher_rao_distance(seed_a: Seed, seed_b: Seed, F_avg: matrix) -> float:
    let theta_a = extract_continuous_genes(seed_a)
    let theta_b = extract_continuous_genes(seed_b)
    let delta = vec_sub(theta_a, theta_b)
    let quad = vec_dot(delta, mat_vec_mul(F_avg, delta))
    return sqrt(max(quad, 0.0))
```

The Layer 1 SeedManifold uses this distance for the "similar seeds" feature in the studio. Two seeds with completely different gene values can be "near" if the FIM tells us their *outputs* are statistically indistinguishable — and vice versa.

## Use 3: Stiff/sloppy decomposition

Eigendecomposition of `F(θ)` produces eigenvalues sorted from largest (stiff) to smallest (sloppy):

```
fn stiff_sloppy_axes(fim: matrix) -> [Axis]:
    let (eigenvalues, eigenvectors) = symmetric_eigh(fim)
    let mut axes = []
    for i in 0..eigenvalues.length:
        axes.push(Axis {
            direction: eigenvectors.column(i),
            stiffness: eigenvalues[i],
        })
    axes.sort_by(|a, b| compare(b.stiffness, a.stiffness))
    return axes
```

The studio's "Important Genes" panel shows the top-3 stiff axes — the gene combinations to which the output is most sensitive. The user can edit these directly without scrolling through all 47 raw gene sliders.

## Determinism

- Sample substreams are derived deterministically from the parent RNG via FNV-1a labels.
- The Jacobian-based FIM is fully deterministic given the engine.
- Eigendecomposition uses a deterministic Jacobi or QR algorithm with fixed pivot order.

## Numerical stability

- Add a small ridge `λI` (typically `λ = 1e-6 * trace(F) / n`) before inverting.
- For the diagonal FIM, floor each entry at `1e-12` to prevent overflow when inverting.
- For the Jacobian FIM, choose `eps` per gene based on its scale; a single global eps is wrong.

## Where it's used in Paradigm

- **SeedManifold** distance metric (Layer 1).
- **CMA-ES natural gradient** option in continuous evolution.
- **Studio gene editor** for slider sensitivity scaling.
- **Lineage tree** for measuring "interesting" mutations vs "trivial" ones (a stiff-direction mutation is interesting; a sloppy-direction one is noise).
- **Seed similarity search** in the marketplace.

## References

- Amari, *Information Geometry and Its Applications* (Springer 2016) — the foundational reference
- Martens & Grosse, *Optimizing Neural Networks with Kronecker-factored Approximate Curvature* (ICML 2015) — K-FAC
- Transtrum, Machta, Sethna, *Why are Nonlinear Fits to Data so Challenging?* (PRL 2010) — sloppy models
- Pascanu & Bengio, *Revisiting Natural Gradient for Deep Networks* (ICLR 2014)
