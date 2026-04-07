# AURORA (AUtonomous RObots that Realize their Abilities)

## What it does

AURORA (Cully 2019) is the answer to the question "what if I don't know what behavior dimensions to use for MAP-Elites?" It learns the behavior characterization automatically by training an **autoencoder** on raw observations of evolved individuals, then uses the autoencoder's latent space as the descriptor space for quality-diversity.

In Paradigm, AURORA is the default when:

- The user is exploring a new domain where hand-designed descriptors don't yet exist.
- The user wants to discover *unforeseen* axes of variation, not just optimize along expected ones.
- The domain produces high-dimensional artifacts (3D meshes, full game-state trajectories, music spectrograms) that don't reduce naturally to a few scalars.

## High-level loop

```
1. Bootstrap: evolve a small initial population with random descriptors.
2. Collect raw observations (e.g., screenshots, mesh point clouds, audio waveforms).
3. Train an autoencoder on these observations → latent encoder E: obs -> R^d.
4. Use E as the descriptor function for MAP-Elites.
5. Run QD evolution for N generations.
6. Periodically retrain E on the now-larger archive of observations
   (the "container update").
7. Repeat 4–6 until budget exhausted.
```

The retraining step is critical: as the population fills out, the autoencoder learns more nuanced features, which subdivides existing MAP-Elites cells and reveals new axes of diversity.

## State

```
struct AuroraState:
    archive: Map<DescriptorKey, Individual>
    encoder: AutoEncoder                       // learned descriptor function
    raw_observations: [Observation]            // training data for encoder
    config: AuroraConfig
    generation: int
    rng: Rng

struct AuroraConfig:
    observation_fn: fn(seed: Seed) -> Observation
    latent_dim: int                            // d, e.g., 8
    bin_counts: [int]                          // length d
    fitness_fn: fn(seed: Seed) -> float
    encoder_arch: AutoEncoderArch              // CNN, MLP, transformer, etc.
    encoder_train_epochs: int
    container_update_interval: int             // generations between retrains
    initial_population_size: int
    max_generations: int

struct Individual:
    seed: Seed
    observation: Observation
    descriptor: vec<float>      // current encoder output
    fitness: float

struct AutoEncoder:
    encoder: NeuralNetwork      // obs → latent
    decoder: NeuralNetwork      // latent → obs reconstruction
```

## Encoder choice per domain

| Domain | Observation | Encoder |
|---|---|---|
| Sprite | 64×64 RGBA atlas | 4-layer CNN, latent dim 8 |
| Character | 256-vert mesh point cloud | PointNet, latent dim 12 |
| Music | 128-bin mel-spectrogram (10s) | 5-layer CNN, latent dim 16 |
| FullGame | game-state trajectory (state every 30 frames, 1000 frames) | LSTM autoencoder, latent dim 16 |
| Geometry3D | voxel grid 32³ | 3D CNN, latent dim 12 |

The encoder architecture is configurable; the only requirement is that it's a deterministic function of its inputs and weights.

## Initialization

```
fn init(initial_population: [Seed], cfg: AuroraConfig, rng: Rng) -> AuroraState:
    let mut state = AuroraState {
        archive: empty_map(),
        encoder: AutoEncoder::random(cfg.encoder_arch, &rng),
        raw_observations: [],
        config: cfg,
        generation: 0,
        rng: rng,
    }
    // Bootstrap: evaluate the initial population with random descriptors,
    // gather observations.
    for seed in initial_population:
        let obs = cfg.observation_fn(seed)
        state.raw_observations.push(obs)
        let descriptor = encode(&state.encoder, &obs)
        let key = descriptor_to_key(descriptor, cfg.bin_counts)
        let ind = Individual { seed, observation: obs, descriptor, fitness: cfg.fitness_fn(seed) }
        try_insert(&mut state.archive, key, ind)
    // Initial encoder training pass.
    train_encoder(&mut state.encoder, &state.raw_observations, cfg.encoder_train_epochs)
    return state
```

## Inner step: a normal MAP-Elites generation

```
fn step(state: &mut AuroraState) -> void:
    let cfg = &state.config
    // 1. Sample parents from archive.
    let parents = sample_random_elites(&state.archive, batch_size = 32, rng = &mut state.rng)
    // 2. Mutate.
    for parent in parents:
        let child_seed = mutate(parent.seed, &mut state.rng)
        let child_obs = cfg.observation_fn(child_seed)
        let child_descriptor = encode(&state.encoder, &child_obs)
        let key = descriptor_to_key(child_descriptor, cfg.bin_counts)
        let child = Individual {
            seed: child_seed,
            observation: child_obs,
            descriptor: child_descriptor,
            fitness: cfg.fitness_fn(child_seed),
        }
        let inserted = try_insert(&mut state.archive, key, child)
        if inserted:
            state.raw_observations.push(child.observation)
    state.generation += 1

    // 3. Container update (encoder retrain + archive re-binning).
    if state.generation % cfg.container_update_interval == 0:
        container_update(state)
```

## Container update (the magic step)

```
fn container_update(state: &mut AuroraState) -> void:
    let cfg = &state.config
    // 1. Retrain the encoder on all collected observations.
    train_encoder(&mut state.encoder, &state.raw_observations, cfg.encoder_train_epochs)
    // 2. Re-encode every individual in the archive.
    let old_individuals: [Individual] = state.archive.values().clone()
    state.archive.clear()
    // 3. Re-insert with new descriptors. Some cells will collide;
    //    fitness wins as in standard MAP-Elites.
    for mut ind in old_individuals:
        ind.descriptor = encode(&state.encoder, &ind.observation)
        let key = descriptor_to_key(ind.descriptor, cfg.bin_counts)
        try_insert(&mut state.archive, key, ind)
```

The container update is what differentiates AURORA from "MAP-Elites with a fixed neural descriptor." Without it, the encoder is a fixed projection; with it, the descriptor space *evolves* alongside the population.

## try_insert

```
fn try_insert(archive: &mut Map<DescriptorKey, Individual>, key: DescriptorKey,
               new: Individual) -> bool:
    let occupant = archive.get(&key)
    match occupant:
        None -> { archive.insert(key, new); return true }
        Some(curr) -> {
            if new.fitness > curr.fitness:
                archive.insert(key, new)
                return true
            return false
        }
```

## descriptor_to_key

Same as plain MAP-Elites — see [`map-elites.md`](map-elites.md) §"Bin discretization". Each latent dimension is normalized into `[0, 1]` (using running min/max over the archive) and discretized.

## train_encoder

```
fn train_encoder(enc: &mut AutoEncoder, observations: &[Observation], epochs: int):
    let optimizer = Adam(lr = 1e-3, beta1 = 0.9, beta2 = 0.999)
    for epoch in 0..epochs:
        let batches = shuffle(observations, &deterministic_rng).chunks(batch_size = 64)
        for batch in batches:
            let recon = batch.map(|obs| decode(&enc.decoder, encode(&enc.encoder, obs)))
            let loss = mean_squared_error(batch, recon)
            backprop(loss, &mut enc, optimizer)
```

The shuffling uses a deterministic RNG seeded from the AURORA state for reproducibility.

## Loss for non-image observations

- **Point clouds:** Chamfer distance, not MSE.
- **Mel-spectrograms:** Log-magnitude MSE.
- **Sequences:** Per-step MSE summed over time.

## Determinism

AURORA introduces a major determinism challenge: neural network training. Paradigm enforces it via:

1. **Deterministic batch ordering** (RNG-shuffled).
2. **Deterministic weight init** (RNG-seeded).
3. **Deterministic GPU kernels** — set CUDA `deterministic = true`, disable cuDNN benchmark mode, force algorithm 1 for convolutions.
4. **Fixed precision** (binary32 for the encoder, no mixed precision).
5. **Pinned library versions** in the seed metadata.

The result: same initial population + same RNG seed + same library versions → same archive bit-for-bit.

## Computational cost

AURORA is the most expensive Paradigm algorithm by 1–2 orders of magnitude:

- Encoder training: 30s–5min per container update on a consumer GPU.
- 100 generations × `container_update_interval = 10` = 10 retrains.
- Full run: 5min–1h depending on encoder size.

For interactive studio use, AURORA is restricted to the *batch* mode and runs in the background while the user does other things.

## Where it's used in Paradigm

- **Geometry3D** when the user wants 3D shapes that aren't characterizable by simple stats.
- **FullGame** to discover gameplay archetypes nobody anticipated.
- **Music** for spectral diversity beyond tempo/density.
- **Optional override** for any domain where the user clicks "auto-discover diversity axes."

## References

- Cully, *Autonomous Skill Discovery with Quality-Diversity and Unsupervised Descriptors* (GECCO 2019) — foundational AURORA paper
- Grillotti & Cully, *Unsupervised Behavior Discovery with Quality-Diversity Optimization* (IEEE TEVC 2022) — improved AURORA variants
- Paolo et al., *Discovering and Exploiting Sparse Rewards in a Learned Behavior Space* (ICML 2021)
