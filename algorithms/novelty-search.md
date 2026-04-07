# Novelty Search

## What it does

Novelty Search abandons the objective function entirely and selects for *behavioral novelty* — how different a candidate is from everything seen before. The insight (Lehman & Stanley 2008) is that on deceptive landscapes, chasing the gradient of the objective leads to local optima, while chasing novelty maintains diversity and often finds the global optimum *as a side effect*.

In Paradigm, Novelty Search is the default algorithm when:

- The fitness landscape is **deceptive** (e.g., walking gaits where partial progress looks worse than not moving).
- You want maximum exploration before any exploitation.
- The user explicitly requests "wild" or "creative" outputs in the studio.

It also serves as the diversity backbone of MAP-Elites' parent selection when configured in `nsga` mode.

## Behavioral characterization

Each individual is reduced to a **behavior descriptor** `b ∈ R^d` — a low-dimensional vector summarizing *what the artifact does*, not what it's made of. For Paradigm domains:

| Domain | Behavior Descriptor |
|---|---|
| Sprite | (silhouette area ratio, palette hue mean, palette saturation mean, animation extent) |
| Character | (height, mass distribution, archetype-vec PCA[0..3]) |
| Music | (mean tempo, harmonic density, rhythmic entropy, dynamic range) |
| FullGame | (mechanic complexity, win-rate of random policy, level entropy, asset count) |

The descriptor is hand-designed per domain (or learned via AURORA — see [`aurora.md`](aurora.md)).

## Novelty score

The novelty of an individual is its average distance to the `k` nearest neighbors in a combined set of (current population) ∪ (archive of past individuals).

```
fn novelty(b: vec<float>, population: [vec<float>], archive: [vec<float>], k: int) -> float:
    let all = concat(population, archive)
    let dists = all.map(|other| euclidean_distance(b, other))
    dists.sort()
    // Skip the first (which is `b` itself if it's in `all`).
    let nearest = dists[1..=k]
    return mean(nearest)
```

Higher = more novel = better. There is no objective fitness anywhere in this score.

## State

```
struct NoveltySearchState:
    population: [Individual]                  // current generation
    archive: [vec<float>]                     // accumulated novel descriptors
    config: NoveltySearchConfig
    generation: int
    rng: Rng

struct NoveltySearchConfig:
    descriptor_fn: fn(seed: Seed) -> vec<float>
    k: int                                    // neighbors for novelty calc
    population_size: int
    archive_threshold: float                  // novelty above this → add to archive
    archive_max_size: int                     // bounded archive
    mutation_rate: float
    max_generations: int

struct Individual:
    seed: Seed
    descriptor: vec<float>
    novelty_score: float
```

## Initialization

```
fn init(initial: [Seed], cfg: NoveltySearchConfig, rng: Rng) -> NoveltySearchState:
    let population = initial.map(|s| Individual {
        seed: s,
        descriptor: cfg.descriptor_fn(s),
        novelty_score: 0.0,
    })
    return NoveltySearchState {
        population, archive: [], config: cfg, generation: 0, rng,
    }
```

## One generation

```
fn step(state: &mut NoveltySearchState) -> void:
    let cfg = &state.config
    // 1. Score every individual.
    let descriptors = state.population.map(|ind| ind.descriptor)
    for ind in &mut state.population:
        ind.novelty_score = novelty(ind.descriptor, descriptors, state.archive, cfg.k)

    // 2. Tournament-select parents by novelty.
    let parents = tournament_select_by_novelty(&state.population, cfg.population_size,
                                                tournament_size = 4, rng = &mut state.rng)

    // 3. Mutate to produce next generation.
    let next_population = parents.map(|parent| {
        let child_seed = mutate(parent.seed, cfg.mutation_rate, &mut state.rng)
        let child_desc = cfg.descriptor_fn(child_seed)
        Individual { seed: child_seed, descriptor: child_desc, novelty_score: 0.0 }
    })

    // 4. Update archive: any individual whose novelty exceeds the threshold
    //    is added to the persistent archive.
    for ind in &state.population:
        if ind.novelty_score > cfg.archive_threshold:
            state.archive.push(ind.descriptor.clone())
    if state.archive.length > cfg.archive_max_size:
        // Drop oldest entries (FIFO) to bound memory.
        state.archive = state.archive[state.archive.length - cfg.archive_max_size..]

    state.population = next_population
    state.generation += 1
```

## Tournament selection by novelty

```
fn tournament_select_by_novelty(pop: &[Individual], n: int, tournament_size: int,
                                  rng: &mut Rng) -> [Individual]:
    let mut selected = []
    for _ in 0..n:
        let mut tournament = []
        for _ in 0..tournament_size:
            let i = uniform_int(rng, 0, pop.length)
            tournament.push(&pop[i])
        // Pick the most novel member.
        let winner = tournament.max_by(|a, b| compare(a.novelty_score, b.novelty_score))
        selected.push(winner.clone())
    return selected
```

## Termination and result

Novelty search has no natural termination since there's no objective. Three common stopping criteria:

1. **Fixed budget:** Run for `max_generations` and return the entire archive as the gallery.
2. **Coverage:** Stop when the descriptor space is "filled" (variance plateau).
3. **Hybrid:** Track an objective fitness *separately* (without using it for selection) and stop when any individual exceeds a target.

```
fn run(initial: [Seed], cfg: NoveltySearchConfig, rng: Rng) -> [Seed]:
    let mut state = init(initial, cfg, rng)
    while state.generation < cfg.max_generations:
        step(&mut state)
    // Return the union of population and archive as the gallery.
    let mut gallery = state.population.map(|ind| ind.seed)
    return gallery
```

## Novelty + Local Competition (NSLC)

A widely-used variant adds *local* fitness pressure: among individuals with similar behavior, prefer the higher-fitness one. This is the basis of NSGA-style multi-objective + novelty hybrids.

```
fn local_competition_score(ind: &Individual, neighbors: &[Individual],
                            objective_fn: fn(Seed) -> float) -> float:
    let ind_fit = objective_fn(ind.seed)
    let beaten = neighbors.iter().filter(|n| objective_fn(n.seed) < ind_fit).count()
    return beaten as float / neighbors.length as float
```

NSLC then performs Pareto sort on `(novelty_score, local_competition_score)` and uses crowding distance for tie-breaking — this is the canonical NSGA-II machinery applied to (novelty, local-competition) instead of (objective1, objective2).

## Determinism

- Tournament selection samples via the deterministic RNG.
- Archive insertion order is deterministic since the population is processed in array order.
- FIFO archive bounding is deterministic.
- The `descriptor_fn` must itself be deterministic (which all Paradigm domain descriptors are).

## When to use vs MAP-Elites

| Property | Novelty Search | MAP-Elites |
|---|---|---|
| Behavior space | Continuous, unbounded | Discretized into bins |
| Output | Population + archive | Archive grid |
| Memory | Bounded archive (FIFO) | Bounded by bin count |
| Visualization | Scatter / t-SNE | Grid heatmap |
| When | Don't know good descriptor bounds | Bounds known, want even coverage |

In practice: **Novelty Search for early exploration, MAP-Elites for organized presentation.** The studio uses Novelty Search when the user clicks "Surprise me" and MAP-Elites for the default gallery view.

## Where it's used in Paradigm

- **Sprite engine** when the user requests "weird" or "experimental" sprites.
- **FullGame engine** for discovering unexpected mechanic combinations.
- **ALife engine** as the default — open-ended evolution should not have an objective.
- **As a sub-routine** of POET for environment generation (see [`poet.md`](poet.md)).

## References

- Lehman & Stanley, *Abandoning Objectives: Evolution Through the Search for Novelty Alone* (Evolutionary Computation 2011) — foundational paper
- Lehman & Stanley, *Evolving a Diversity of Virtual Creatures Through Novelty Search and Local Competition* (GECCO 2011) — NSLC
- Mouret & Doncieux, *Encouraging Behavioral Diversity in Evolutionary Robotics: An Empirical Study* (Evolutionary Computation 2012)
