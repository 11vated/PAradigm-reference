# DQD (Differentiable Quality-Diversity)

## What it does

DQD (Fontaine & Nikolaidis 2021) brings gradient information into quality-diversity. Where MAP-Elites only uses fitness *rankings* (so it works with any black-box fitness), DQD assumes the fitness function and behavior descriptors are **differentiable** with respect to seed parameters and uses gradient ascent to find improvements far more efficiently than mutation alone.

In Paradigm, DQD is the algorithm of choice when:

- The seed has many continuous gene values (10–10,000).
- The fitness and descriptors are differentiable (the engine has a `@gpu` differentiable mode, or the loss is computed with autodiff).
- You want fast convergence with QD coverage.

A typical DQD run reaches the same archive coverage as MAP-Elites in 10–100× fewer fitness evaluations.

## Key idea: gradient arborescence

For each elite in the archive, DQD does not just mutate randomly. It computes:

- **∇f** — the gradient of fitness with respect to the seed parameters.
- **∇b₁, …, ∇b_d** — the gradient of each behavior descriptor with respect to the seed parameters.

It then samples a *combination* of these gradients (a vector in the gradient subspace) and steps in that direction. This produces a child whose fitness is *intentionally improved or whose descriptor is intentionally shifted* — not random.

The standard DQD variant in Paradigm is **CMA-MEGA** (Covariance Matrix Adaptation MAP-Elites via Gradient Arborescence).

## State

```
struct DqdState:
    archive: Map<DescriptorKey, Individual>
    config: DqdConfig
    cma_es: CmaEsState           // CMA-ES over the gradient subspace coefficients
    generation: int
    rng: Rng

struct DqdConfig:
    fitness_fn: fn(theta: vec<float>) -> (float, vec<float>)        // fitness + grad
    descriptor_fns: [fn(theta: vec<float>) -> (float, vec<float>)]  // each: value + grad
    bin_counts: [int]
    initial_population_size: int
    branch_population_size: int     // λ for the inner CMA-ES, e.g., 36
    max_generations: int
    sigma_init: float

struct Individual:
    theta: vec<float>          // raw gene parameter vector
    fitness: float
    descriptor: vec<float>
```

## Initialization

```
fn init(initial: [vec<float>], cfg: DqdConfig, rng: Rng) -> DqdState:
    let mut archive = empty_map()
    for theta in initial:
        let (f, _) = cfg.fitness_fn(theta.clone())
        let descriptor = cfg.descriptor_fns.map(|fn_| fn_(theta.clone()).0)
        let key = descriptor_to_key(descriptor, cfg.bin_counts)
        try_insert(&mut archive, key, Individual { theta, fitness: f, descriptor })
    let n = 1 + cfg.descriptor_fns.length
    return DqdState {
        archive,
        config: cfg,
        cma_es: CmaEsState::init(n, zeros(n), cfg.sigma_init),
        generation: 0,
        rng,
    }
```

The CMA-ES inside DQD operates on a *small* `(1+d)`-dimensional space — the coefficients in front of the (`∇f, ∇b₁, …, ∇b_d`) gradients — *not* the full `n`-dimensional gene space.

## One generation (CMA-MEGA)

```
fn step(state: &mut DqdState) -> void:
    let cfg = &state.config
    // 1. Pick a random elite from the archive.
    let parent = sample_random_elite(&state.archive, &mut state.rng)
    let theta = parent.theta.clone()

    // 2. Compute gradient arborescence: f-grad and each b-grad at theta.
    let (f_val, grad_f) = (cfg.fitness_fn)(theta.clone())
    let mut grads = [grad_f]
    for fn_ in &cfg.descriptor_fns:
        let (_, grad_bi) = fn_(theta.clone())
        grads.push(grad_bi)

    // Stack gradients into a matrix G of shape (1+d, n).
    let G = stack_rows(grads)

    // 3. Sample λ coefficient vectors from the inner CMA-ES.
    let coefficients = state.cma_es.sample_population(cfg.branch_population_size,
                                                      &mut state.rng)
    // shape (λ, 1+d)

    // 4. For each coefficient vector, compute the new candidate theta.
    let mut new_inds = []
    for c in coefficients:
        let direction = mat_vec_mul(transpose(G), c)        // shape (n,)
        let new_theta = vec_add(theta, direction)
        let (new_f, _) = cfg.fitness_fn(new_theta.clone())
        let new_descriptor = cfg.descriptor_fns.map(|fn_| fn_(new_theta.clone()).0)
        new_inds.push(Individual { theta: new_theta, fitness: new_f, descriptor: new_descriptor })

    // 5. Try to insert each into the archive; rank candidates by improvement.
    let mut improvements = []
    for (i, ind) in new_inds.enumerate():
        let key = descriptor_to_key(ind.descriptor, cfg.bin_counts)
        let occupant = state.archive.get(&key)
        let improvement = match occupant:
            None       -> 1.0 + ind.fitness    // huge bonus for opening a new cell
            Some(curr) -> ind.fitness - curr.fitness
        improvements.push((improvement, i))
        try_insert(&mut state.archive, key, ind)

    // 6. Update the inner CMA-ES using the improvement ranking as the fitness signal.
    improvements.sort_by(|a, b| compare(b.0, a.0))   // descending
    let ranked_coefficients = improvements.map(|(_, i)| coefficients[i])
    state.cma_es.tell(ranked_coefficients)

    state.generation += 1
```

## Why this works

The inner CMA-ES is doing CMA-ES not over the *gene parameter space*, but over the *space of recombinations of the gradient directions*. It learns: "for this region of the archive, the best update is 0.7·∇f + 0.3·∇b₁ − 0.2·∇b₂." That coefficient vector is highly transferable across generations because the gradients change slowly.

After `(1+d) × 10` generations, the inner CMA-ES has converged on a good recombination strategy and starts outputting near-optimal updates.

## Termination and result

```
fn run(initial: [vec<float>], cfg: DqdConfig, rng: Rng)
    -> Map<DescriptorKey, Individual>:
    let mut state = init(initial, cfg, rng)
    while state.generation < cfg.max_generations:
        step(&mut state)
        // Periodically reset the inner CMA-ES to escape local optima.
        if state.generation % 200 == 0:
            state.cma_es.reset()
    return state.archive
```

## Differentiability requirements

For DQD to work, the engine must support **autodiff**. Paradigm domains with autodiff support:

| Domain | Differentiable? | How |
|---|---|---|
| Sprite | ✅ | Soft rasterizer + differentiable color blending |
| Character | ✅ | Differentiable mesh deformation (RBS) |
| Music | ⚠️ Partial | Spectral loss only; symbolic genes are non-diff |
| FullGame | ❌ | Game logic is discrete |
| Geometry3D | ✅ | SDFs are differentiable everywhere |
| Physics | ✅ | Differentiable physics (DiffTaichi backend) |
| Audio | ✅ | DDSP-style oscillators |

For non-differentiable domains, fall back to plain MAP-Elites or DQD with finite-difference gradient estimation (much slower but always works).

## Determinism

- The inner CMA-ES uses the kernel `xoshiro256**`.
- Gradient computation is deterministic provided the engine is.
- Tie-breaking uses content-hash order, same as plain MAP-Elites.

## Computational cost

- Each generation requires 1 backward pass per descriptor function plus 1 backward pass for fitness (so `1 + d` backward passes).
- Each candidate evaluation is one forward pass.
- For `n = 100`, `d = 2`, `λ = 36`: ~3 backward + 36 forward = 39 differentiable engine evaluations per generation.
- Compare to plain MAP-Elites: 32 forward per generation, but needs ~10× more generations for the same coverage.
- Net: DQD is 3–10× cheaper in wall-clock for differentiable domains.

## Where it's used in Paradigm

- **Geometry3D** when fine-tuning SDF parameters for visual targets.
- **Character** for matching reference body morphologies.
- **Sprite** for matching reference style images.
- **Physics** for inverse-design (e.g., "find a creature morphology that walks fastest").
- **Default** for any continuous-only seed when the engine declares `@diff` capability.

## References

- Fontaine & Nikolaidis, *Differentiable Quality Diversity* (NeurIPS 2021) — foundational paper
- Tjanaka et al., *Approximating Gradients for Differentiable Quality Diversity in Reinforcement Learning* (GECCO 2022)
- Pyribs library — reference implementation: https://pyribs.org
