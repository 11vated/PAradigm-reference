# POET (Paired Open-Ended Trailblazer)

## What it does

POET (Wang et al. 2019, 2020) is the first algorithm explicitly designed for *open-ended* coevolution. Instead of optimizing agents against a fixed environment, POET *coevolves environments and agents together*: each agent has its own environment that's just hard enough to be educational, and successful agents are periodically *transferred* to other environments to test generalization. Over time, both populations escalate in complexity.

In Paradigm, POET is the algorithm behind:

- **ALife domain** — coevolving organisms and ecosystems.
- **FullGame domain** — coevolving level designs and player AIs.
- **Ecosystem domain** — coevolving species and their habitats.
- Anywhere the user wants "evolution that doesn't stop and doesn't converge."

## Key concepts

1. **Environment-Agent pair (EA-pair):** the unit of evolution. Each pair has its own niche.
2. **Minimal Criterion Coevolution (MCC):** environments must be solvable but non-trivial. Agents must clear a fitness threshold to be considered "competent" in their pair.
3. **Transfer:** competent agents from pair A are tested in pair B's environment. If they outperform B's resident agent, they replace it.
4. **Environment mutation:** new environments are created by mutating existing ones. They must pass MCC to be admitted.

## State

```
struct PoetState:
    pairs: [Pair]
    config: PoetConfig
    generation: int
    rng: Rng

struct Pair:
    id: PairId
    environment: Environment       // a seed
    agent: Agent                   // a seed
    age: int
    parent_pair_id: Option<PairId>

struct PoetConfig:
    max_pairs: int                 // typical 8–32
    mc_low: float                  // minimum fitness for "solvable"
    mc_high: float                 // maximum fitness for "non-trivial"
    inner_optimizer_steps: int     // steps of inner agent optimization per outer step
    transfer_interval: int         // generations between transfer attempts
    env_mutation_interval: int     // generations between env mutations
    env_mutation_rate: float
    initial_env: Environment
    initial_agent: Agent
    novelty_threshold: float       // for accepting new environments
```

## Initialization

```
fn init(cfg: PoetConfig, rng: Rng) -> PoetState:
    let initial_pair = Pair {
        id: PairId::new(),
        environment: cfg.initial_env.clone(),
        agent: cfg.initial_agent.clone(),
        age: 0,
        parent_pair_id: None,
    }
    return PoetState {
        pairs: [initial_pair],
        config: cfg,
        generation: 0,
        rng,
    }
```

## One generation

```
fn step(state: &mut PoetState) -> void:
    let cfg = &state.config

    // 1. Inner-loop: optimize each agent against its own environment.
    for pair in &mut state.pairs:
        for _ in 0..cfg.inner_optimizer_steps:
            pair.agent = optimize_step(pair.agent, &pair.environment, &mut state.rng)
        pair.age += 1

    // 2. Periodic transfer: try every agent in every other pair's environment.
    if state.generation % cfg.transfer_interval == 0:
        transfer_attempt(state)

    // 3. Periodic environment mutation: spawn new environments from existing ones.
    if state.generation % cfg.env_mutation_interval == 0:
        environment_mutation(state)

    state.generation += 1
```

## Inner-loop optimizer

The inner optimizer is a single step of any RL or evolutionary algorithm. POET is agnostic to which one. Paradigm uses:

- **CMA-ES** for continuous control agents.
- **Genetic algorithm** for symbolic / discrete agents.
- **PPO** for neural-network agents (when the engine supports it).

```
fn optimize_step(agent: Agent, env: &Environment, rng: &mut Rng) -> Agent:
    let candidates = generate_candidates(agent, n = 16, rng)
    let scored = candidates.map(|c| (evaluate(c, env), c))
    return scored.max_by(|a, b| compare(a.0, b.0)).1
```

## Transfer

```
fn transfer_attempt(state: &mut PoetState) -> void:
    let cfg = &state.config
    let n = state.pairs.length
    for i in 0..n:
        for j in 0..n:
            if i == j: continue
            let visiting_agent = state.pairs[i].agent.clone()
            let target_env = &state.pairs[j].environment
            let visitor_score = evaluate(&visiting_agent, target_env)
            let resident_score = evaluate(&state.pairs[j].agent, target_env)
            // Transfer if visitor strictly beats resident, AND visitor still
            // satisfies MC in the target environment.
            if visitor_score > resident_score and is_in_mc(visitor_score, cfg):
                state.pairs[j].agent = visiting_agent

fn is_in_mc(fitness: float, cfg: &PoetConfig) -> bool:
    return fitness >= cfg.mc_low and fitness <= cfg.mc_high
```

Transfer is the engine of generalization. An agent that has only seen environment A but happens to also work well in environment B is more "robust" and gets to keep evolving in both.

## Environment mutation

```
fn environment_mutation(state: &mut PoetState) -> void:
    let cfg = &state.config
    let mut new_pairs = []
    // Pick "successful" parent pairs whose agent satisfies MC.
    let candidates = state.pairs.iter().filter(|p| {
        let f = evaluate(&p.agent, &p.environment)
        is_in_mc(f, cfg)
    }).collect()
    if candidates.is_empty(): return
    // For each candidate, propose a mutated environment.
    for parent in candidates:
        let new_env = mutate_environment(&parent.environment, cfg.env_mutation_rate,
                                          &mut state.rng)
        // The proposed environment must be:
        //   (a) novel enough vs all existing environments
        //   (b) solvable by SOME existing agent within the MC band
        if not is_novel_enough(&new_env, &state.pairs, cfg.novelty_threshold):
            continue
        let best_agent = state.pairs.iter()
            .map(|p| (evaluate(&p.agent, &new_env), p.agent.clone()))
            .max_by(|a, b| compare(a.0, b.0))
        if not is_in_mc(best_agent.0, cfg):
            continue
        // Admit the new pair, seeded with the best existing agent.
        new_pairs.push(Pair {
            id: PairId::new(),
            environment: new_env,
            agent: best_agent.1,
            age: 0,
            parent_pair_id: Some(parent.id),
        })
    // Bound the population — drop the oldest pairs if needed.
    state.pairs.extend(new_pairs)
    if state.pairs.length > cfg.max_pairs:
        state.pairs.sort_by(|a, b| compare(b.age, a.age))   // oldest first
        state.pairs = state.pairs[0..cfg.max_pairs]
```

## Novelty check

```
fn is_novel_enough(env: &Environment, existing: &[Pair], threshold: float) -> bool:
    let env_descriptor = environment_behavior(env)
    let dists = existing.map(|p| distance(env_descriptor, environment_behavior(&p.environment)))
    return min(dists) > threshold
```

The environment descriptor is domain-specific:

| Domain | Environment Descriptor |
|---|---|
| ALife | (terrain roughness, food density, predator density, climate volatility) |
| FullGame | (level entropy, hazard density, traversable area, key item count) |
| Ecosystem | (biome diversity, carrying capacity, seasonal variance) |

## Termination

POET is open-ended. It does not converge. Termination is by:

1. **Wall-clock budget** — run for `T` generations and inspect.
2. **Lineage interesting events** — stop when a pair reaches a particular landmark capability.
3. **Stagnation** — stop if no new environment has been admitted in `K` cycles (rare; usually means parameters are too restrictive).

```
fn run(cfg: PoetConfig, rng: Rng) -> [Pair]:
    let mut state = init(cfg, rng)
    while state.generation < cfg.max_generations:
        step(&mut state)
    return state.pairs
```

## Determinism

- Pair iteration is in `id` order (sorted) for any operation that aggregates across pairs.
- Mutation, optimization, and evaluation all use the kernel RNG.
- Inner optimizer reset state is part of the pair's serialized form.
- POET runs are deterministic given the same RNG seed and same config; reproducing a 100-generation run should give bit-identical pairs.

## Computational cost

POET is the most expensive Paradigm algorithm by wall clock. With `pairs = 16`, `inner_optimizer_steps = 100`, `evaluate cost = 100ms`, you're looking at:

- Per generation: 16 × 100 × 100ms = 160s
- Plus transfer: 16 × 16 × 100ms = 26s every `transfer_interval` generations
- Plus mutation: ~5s every `env_mutation_interval` generations

A 1000-generation run takes 30+ hours. POET is therefore relegated to the **batch processing tier** of the studio and cannot be run interactively.

## Where it's used in Paradigm

- **ALife domain** — the *only* algorithm; ALife is fundamentally open-ended.
- **Ecosystem domain** — same.
- **FullGame** as an offline option for procedural game design.
- **Character** combined with **Physics** for evolving morphology + control jointly.

## References

- Wang, Lehman, Clune, Stanley, *Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions* (arXiv 2019)
- Wang, Lehman, Rawal, Zhi, Lin, Stanley, *Enhanced POET: Open-Ended Reinforcement Learning through Unbounded Invention of Learning Challenges and their Solutions* (ICML 2020)
- Stanley, Lehman, Soros, *Open-Endedness: The Last Grand Challenge You've Never Heard Of* (O'Reilly 2017)
