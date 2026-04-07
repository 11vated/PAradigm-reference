# MAP-Elites

## What it does

MAP-Elites is the canonical quality-diversity algorithm. Instead of finding a single optimum, it fills a discretized **behavior space** with the best solution found so far in each cell. The result is an *archive* — a gallery of diverse high-quality solutions, not one champion.

In Paradigm, MAP-Elites is the **default** evolution algorithm in the studio because galleries beat single answers for creative work.

## State

```
struct MapElitesState:
    archive: Map<DescriptorKey, Seed>
    config: MapElitesConfig
    generation: int
    rng: Rng

struct MapElitesConfig:
    descriptor_fns: [fn(seed: Seed) -> float]   // length D = number of behavior dims
    bin_counts: [int]                            // length D, e.g., [10, 10] for 100 cells
    fitness_fn: fn(seed: Seed) -> float
    mutation_rate: float
    initial_population_size: int
    max_generations: int

type DescriptorKey = [int]    // bin indices, length D
```

## Bin discretization

Each behavior dimension is divided into a fixed number of bins. A seed's descriptors map to a tuple of bin indices, which is the cell key.

```
fn descriptor_to_key(seed: Seed, cfg: MapElitesConfig) -> DescriptorKey:
    let key: DescriptorKey = []
    for d in 0..cfg.descriptor_fns.length:
        let value = cfg.descriptor_fns[d](seed)
        // Each descriptor must return a value in [0, 1].
        let clamped = clamp(value, 0.0, 1.0)
        let bin = floor(clamped * cfg.bin_counts[d]) as int
        let bin = min(bin, cfg.bin_counts[d] - 1)
        key.push(bin)
    return key
```

## Initialization

```
fn init(initial_population: [Seed], cfg: MapElitesConfig, rng: Rng) -> MapElitesState:
    let mut state = MapElitesState {
        archive: empty_map(),
        config: cfg,
        generation: 0,
        rng: rng,
    }
    for seed in initial_population:
        try_insert(&mut state, seed)
    return state
```

## Insertion

A seed is inserted into the archive at its descriptor cell, **only if** its fitness exceeds the current occupant (or the cell is empty).

```
fn try_insert(state: &mut MapElitesState, seed: Seed) -> bool:
    let key = descriptor_to_key(seed, state.config)
    let new_fit = state.config.fitness_fn(seed)
    let occupant = state.archive.get(key)
    match occupant:
        None        -> { state.archive.insert(key, seed); return true }
        Some(curr)  -> {
            let curr_fit = state.config.fitness_fn(curr)
            if new_fit > curr_fit:
                state.archive.insert(key, seed)
                return true
            return false
        }
```

For determinism, ties are broken by the seed's content hash (lexicographic), so a re-run produces the same archive.

## One generation

```
fn step(state: &mut MapElitesState) -> void:
    if state.archive.is_empty():
        return    // nothing to mutate from
    let parents = sample_random_elites(state, batch_size = 32)
    for parent in parents:
        let child = mutate(parent, state.config.mutation_rate, &mut state.rng)
        try_insert(state, child)
    state.generation += 1
```

`sample_random_elites` picks parents uniformly from the current archive. This is the standard MAP-Elites parent selection — *no* fitness-proportional bias, because diversity is what we want, not over-exploitation of the current best.

```
fn sample_random_elites(state: &MapElitesState, batch_size: int) -> [Seed]:
    let keys = sorted(state.archive.keys())   // sort for determinism
    let mut out = []
    for _ in 0..batch_size:
        let i = uniform_int(&mut state.rng, 0, keys.length)
        out.push(state.archive.get(keys[i]).unwrap())
    return out
```

## Termination

```
fn run(initial: [Seed], cfg: MapElitesConfig, rng: Rng) -> Map<DescriptorKey, Seed>:
    let mut state = init(initial, cfg, rng)
    while state.generation < cfg.max_generations:
        step(&mut state)
    return state.archive
```

## Defaults per domain (from `evolution-stack.md`)

| Domain | Descriptor 1 | Descriptor 2 |
|---|---|---|
| Sprite | silhouette complexity | palette diversity |
| Character | strength | agility |
| Music | tempo | harmonic density |
| FullGame | mechanic complexity | difficulty curve |
| Geometry3D | mesh density | symmetry |

The descriptor functions for each domain live in the engine's `engine.fitnessHints.defaultDescriptors`.

## Determinism

- Archive iteration always uses sorted keys.
- Parent sampling uses the deterministic RNG.
- Tie-breaking on insertion uses content hash order.
- Two runs with the same initial population, the same config, and the same RNG seed produce the same final archive bit-for-bit.

## Compute considerations

A typical run is 100–10,000 fitness evaluations. Fitness is the bottleneck. Paradigm offloads fitness to a Web Worker pool (CPU) or WebGPU compute shaders (GPU) when the engine declares `@gpu`. See [`architecture/evolution-stack.md`](../architecture/evolution-stack.md) §GPU Acceleration.

## References

- Mouret & Clune, *Illuminating Search Spaces by Mapping Elites* (2015)
- Cully & Demiris, *Quality and Diversity Optimization: A Unifying Modular Framework* (2018)
