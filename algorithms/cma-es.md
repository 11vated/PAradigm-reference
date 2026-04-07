# CMA-ES (Covariance Matrix Adaptation Evolution Strategy)

## What it does

CMA-ES is the gold-standard derivative-free optimizer for continuous numerical problems. It maintains a multivariate normal distribution `N(m, σ²C)` over the search space and adapts both the mean `m` and the covariance matrix `C` based on the fitness ranking of sampled offspring. After enough generations, the distribution concentrates around the optimum without ever computing a gradient.

In Paradigm, CMA-ES is the default optimizer for **continuous gene tuning** — when you have a fixed seed topology and want to find the best values for its scalar/vector genes (e.g., tuning the 47 numeric parameters of a procedural creature so its walk cycle minimizes energy expenditure).

## When to use CMA-ES vs MAP-Elites

- **CMA-ES:** single objective, continuous parameters, smooth-ish landscape, want a single best.
- **MAP-Elites:** multi-objective via behavior space, mixed gene types, want a diverse gallery.
- **Combined:** Use CMA-ES *inside* a MAP-Elites cell to refine the elite of that cell.

## State

```
struct CmaEsState:
    n: int                     // problem dimensionality
    mean: vec<float>           // current distribution mean (length n)
    sigma: float               // overall step size
    C: matrix<float, n, n>     // covariance matrix
    pc: vec<float>             // evolution path for C (length n)
    ps: vec<float>             // evolution path for sigma (length n)
    B: matrix<float, n, n>     // eigenvectors of C (columns)
    D: vec<float>              // sqrt of eigenvalues of C (length n)
    eigen_eval_gen: int        // last generation B/D were recomputed
    generation: int
    rng: Rng

struct CmaEsConfig:
    n: int
    initial_mean: vec<float>
    initial_sigma: float
    population_size: int       // λ; default 4 + floor(3 * ln(n))
    parent_count: int          // μ; default λ/2
    fitness_fn: fn(x: vec<float>) -> float       // minimization
    max_generations: int
    target_fitness: float      // optional early-stop
```

## Strategy parameters (computed once)

```
fn init_strategy_params(n: int, lambda: int, mu: int) -> StrategyParams:
    // Recombination weights (log-decreasing).
    let mut w = []
    for i in 1..=mu:
        w.push(ln((lambda + 1) as float / 2.0) - ln(i as float))
    let w_sum = sum(w)
    let weights = w.map(|wi| wi / w_sum)
    let mu_eff = 1.0 / sum(weights.map(|wi| wi * wi))

    // Step-size control constants.
    let c_sigma = (mu_eff + 2.0) / (n as float + mu_eff + 5.0)
    let d_sigma = 1.0 + 2.0 * max(0.0, sqrt((mu_eff - 1.0) / (n as float + 1.0)) - 1.0) + c_sigma

    // Covariance matrix adaptation constants.
    let cc = (4.0 + mu_eff / n as float) / (n as float + 4.0 + 2.0 * mu_eff / n as float)
    let c1 = 2.0 / ((n as float + 1.3).pow(2) + mu_eff)
    let cmu = min(1.0 - c1,
                  2.0 * (mu_eff - 2.0 + 1.0 / mu_eff) / ((n as float + 2.0).pow(2) + mu_eff))

    // Expected length of N(0, I) — used as the reference for ps.
    let chi_n = sqrt(n as float) * (1.0 - 1.0 / (4.0 * n as float)
                                       + 1.0 / (21.0 * (n as float).pow(2)))
    return StrategyParams { weights, mu_eff, c_sigma, d_sigma, cc, c1, cmu, chi_n }
```

These constants are the canonical Hansen recommendations from *The CMA Evolution Strategy: A Tutorial* (2016). Do not deviate without a good reason.

## init

```
fn init(cfg: CmaEsConfig, rng: Rng) -> CmaEsState:
    return CmaEsState {
        n: cfg.n,
        mean: cfg.initial_mean,
        sigma: cfg.initial_sigma,
        C: identity_matrix(cfg.n),
        pc: zeros(cfg.n),
        ps: zeros(cfg.n),
        B: identity_matrix(cfg.n),
        D: ones(cfg.n),
        eigen_eval_gen: 0,
        generation: 0,
        rng: rng,
    }
```

## One generation

```
fn step(state: &mut CmaEsState, cfg: &CmaEsConfig, sp: &StrategyParams) -> void:
    // 1. Sample λ offspring from N(mean, sigma^2 * C).
    let mut offspring = []
    for _ in 0..cfg.population_size:
        let z = sample_normal_vec(&mut state.rng, state.n)            // z ~ N(0, I)
        let y = mat_vec_mul(state.B, elementwise_mul(state.D, z))     // y = B * D * z ~ N(0, C)
        let x = vec_add(state.mean, scalar_mul(state.sigma, y))       // x ~ N(mean, sigma^2 C)
        offspring.push((x, y))

    // 2. Evaluate and rank.
    let mut scored = offspring.map(|(x, y)| (cfg.fitness_fn(x), x, y))
    scored.sort_by(|a, b| compare(a.0, b.0))                          // ascending (minimization)

    // 3. Recombine the μ best.
    let selected = scored[0..cfg.parent_count]
    let new_mean = weighted_mean(selected.map(|s| s.1), sp.weights)
    let y_w      = weighted_mean(selected.map(|s| s.2), sp.weights)   // average of y vectors

    // 4. Update evolution paths.
    // ps update uses C^(-1/2) * y_w; we have C^(-1/2) = B * diag(1/D) * B^T.
    let c_inv_sqrt_yw = mat_vec_mul(state.B,
                          elementwise_div(mat_vec_mul(transpose(state.B), y_w), state.D))
    let ps_new = vec_add(scalar_mul(1.0 - sp.c_sigma, state.ps),
                          scalar_mul(sqrt(sp.c_sigma * (2.0 - sp.c_sigma) * sp.mu_eff),
                                     c_inv_sqrt_yw))

    let hs = if norm(ps_new) /
                sqrt(1.0 - (1.0 - sp.c_sigma).pow(2 * (state.generation + 1)))
                < (1.4 + 2.0 / (state.n as float + 1.0)) * sp.chi_n
              { 1.0 } else { 0.0 }

    let pc_new = vec_add(scalar_mul(1.0 - sp.cc, state.pc),
                          scalar_mul(hs * sqrt(sp.cc * (2.0 - sp.cc) * sp.mu_eff), y_w))

    // 5. Update covariance matrix.
    let rank_one = outer_product(pc_new, pc_new)
    let mut rank_mu = zero_matrix(state.n, state.n)
    for i in 0..cfg.parent_count:
        let yi = selected[i].2
        rank_mu = matrix_add(rank_mu, scalar_mat_mul(sp.weights[i], outer_product(yi, yi)))

    let delta_h = (1.0 - hs) * sp.cc * (2.0 - sp.cc)
    let C_new = matrix_add(
        scalar_mat_mul(1.0 - sp.c1 - sp.cmu + sp.c1 * delta_h, state.C),
        matrix_add(scalar_mat_mul(sp.c1, rank_one),
                   scalar_mat_mul(sp.cmu, rank_mu)))

    // 6. Update step size.
    let sigma_new = state.sigma * exp((sp.c_sigma / sp.d_sigma) *
                                       (norm(ps_new) / sp.chi_n - 1.0))

    // 7. Commit.
    state.mean = new_mean
    state.ps = ps_new
    state.pc = pc_new
    state.C = C_new
    state.sigma = sigma_new
    state.generation += 1

    // 8. Lazy eigendecomposition (every n/(c1+cmu)/10 generations is enough).
    let interval = max(1, floor(1.0 / (sp.c1 + sp.cmu) / state.n as float / 10.0) as int)
    if state.generation - state.eigen_eval_gen >= interval:
        eigendecompose(&mut state)
        state.eigen_eval_gen = state.generation

fn eigendecompose(state: &mut CmaEsState) -> void:
    // Symmetrize C to combat numerical drift.
    state.C = scalar_mat_mul(0.5, matrix_add(state.C, transpose(state.C)))
    let (eigvals, eigvecs) = symmetric_eigh(state.C)
    state.B = eigvecs
    state.D = eigvals.map(|e| sqrt(max(e, 0.0)))   // guard against tiny negatives
```

## run

```
fn run(cfg: CmaEsConfig, rng: Rng) -> vec<float>:
    let sp = init_strategy_params(cfg.n, cfg.population_size, cfg.parent_count)
    let mut state = init(cfg, rng)
    let mut best = (infinity, cfg.initial_mean.clone())
    while state.generation < cfg.max_generations:
        step(&mut state, &cfg, &sp)
        let f = cfg.fitness_fn(state.mean)
        if f < best.0:
            best = (f, state.mean.clone())
        if best.0 <= cfg.target_fitness:
            break
    return best.1
```

## Determinism

- The RNG is the kernel `xoshiro256**` — every Gaussian draw is reproducible.
- Sort comparisons break ties by the lexicographic order of the candidate vector's content hash, never by floating-point equality.
- `symmetric_eigh` must use a deterministic algorithm (e.g., Jacobi rotations or LAPACK with a fixed pivot strategy). For reproducibility across hardware, prefer a Jacobi implementation in pure software over BLAS.
- All matrix operations use IEEE-754 binary64 with FMA disabled (or consistently enabled across all platforms — pick one and document it).

## Numerical guards

- Cap `sigma` at `1e10 * initial_sigma` to detect divergence.
- Floor `sigma` at `1e-10 * initial_sigma`; below that, restart.
- If `min(D) / max(D) < 1e-12`, restart with a perturbed mean.
- If `norm(mean - mean_previous) < 1e-12 * sigma` for 10 consecutive generations, declare convergence.

## Restart strategies

The standard improvement is **IPOP-CMA-ES** (Auger & Hansen 2005): on convergence or stagnation, restart with `lambda *= 2`. This handles multimodal landscapes by progressively widening the search.

```
fn ipop_cma_es(cfg: CmaEsConfig, rng: Rng) -> vec<float>:
    let mut lambda = cfg.population_size
    let mut best = (infinity, cfg.initial_mean.clone())
    for restart in 0..10:
        let mut local_cfg = cfg.clone()
        local_cfg.population_size = lambda
        local_cfg.parent_count = lambda / 2
        let result = run(local_cfg, substream(&rng, format("restart:{}", restart)))
        let f = cfg.fitness_fn(result)
        if f < best.0:
            best = (f, result)
        lambda *= 2
    return best.1
```

## Compute considerations

- Per generation: `λ` fitness evaluations, one `O(n²)` matrix update, occasional `O(n³)` eigendecomposition.
- For `n < 100`, the entire algorithm runs in microseconds per generation excluding fitness.
- For `n > 1000`, switch to **sep-CMA-ES** (diagonal covariance) or **LM-CMA-ES** (limited-memory).
- Fitness is virtually always the bottleneck. Parallelize the `λ` evaluations across workers.

## Where it's used in Paradigm

- **Continuous gene refinement** — when MAP-Elites finds a promising cell, an inner CMA-ES loop polishes the elite.
- **Music tempo/harmony tuning** — for music seeds where the genes are mostly continuous (BPM, dynamics curves, tempo ramps).
- **Physics parameter calibration** — tuning the 20-50 numeric parameters of a `Physics` engine seed to match a target behavior video.
- **NOT used for** topology, categorical, or structural genes — those are MAP-Elites / GA territory.

## References

- Hansen, *The CMA Evolution Strategy: A Tutorial* (2016, arXiv:1604.00772) — canonical reference
- Hansen & Ostermeier, *Completely Derandomized Self-Adaptation in Evolution Strategies* (2001) — original CMA-ES paper
- Auger & Hansen, *A Restart CMA Evolution Strategy with Increasing Population Size* (CEC 2005) — IPOP variant
