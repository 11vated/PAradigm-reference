# Refinement Loop with QualityVector + UCB1 Bandit

## What it does

The refinement loop is the **default fitness function** for every Paradigm evolution algorithm. It does two things:

1. Grows a seed and evaluates a 6-dimensional `QualityVector` measuring multiple aspects of quality.
2. Selects which mutation strategy to apply next using a **UCB1 multi-armed bandit**, learning which strategies are most effective for the current seed and domain.

The UCB1 bandit is what turns "evolve some seeds" into "the platform is getting smarter as you use it." Successful mutation strategies get reinforced; unsuccessful ones get tried less often.

## QualityVector

```
struct QualityVector:
    geometry:  float    // [0, 1] — surface/topology fidelity
    texture:   float    // [0, 1] — color/material coherence
    animation: float    // [0, 1] — motion smoothness
    coherence: float    // [0, 1] — gene values match archetype expectations
    style:     float    // [0, 1] — distance to style corpus in dimensional space
    novelty:   float    // [0, 1] — distance from k-nearest archive neighbors
```

A scalar score is computed by weighted average:

```
fn scalar(qv: QualityVector, weights: QualityVector) -> float:
    return weights.geometry  * qv.geometry
         + weights.texture   * qv.texture
         + weights.animation * qv.animation
         + weights.coherence * qv.coherence
         + weights.style     * qv.style
         + weights.novelty   * qv.novelty
```

Default weights are uniform (1/6 each); the studio lets the user re-weight.

## evaluateAll

```
fn evaluate_all(artifact: Artifact, archive: ArchiveSnapshot) -> QualityVector:
    return QualityVector {
        geometry:  evaluate_geometry(artifact),
        texture:   evaluate_texture(artifact),
        animation: evaluate_animation(artifact),
        coherence: evaluate_coherence(artifact),
        style:     evaluate_style(artifact),
        novelty:   evaluate_novelty(artifact, archive),
    }
```

### Geometry

Sample N points on the surface (e.g., 200), check `|∇field| ≈ 1` (true SDF property). For polygonal meshes, check that the mesh is watertight and manifold.

```
fn evaluate_geometry(art: Artifact) -> float:
    if art is SDFArtifact:
        let samples = sample_surface(art.field, n = 200)
        let errors = samples.map(|p| abs(length(grad(art.field, p)) - 1.0))
        return 1.0 - clamp(mean(errors), 0.0, 1.0)
    if art is MeshArtifact:
        let manifold_score = if is_manifold(art.mesh) { 1.0 } else { 0.5 }
        let watertight_score = if is_watertight(art.mesh) { 1.0 } else { 0.7 }
        return manifold_score * watertight_score
    return 1.0    // domains without geometry get full score
```

### Texture

Convert RGB → HSL, measure palette coherence (low variance in saturation), and contrast (range of luminance).

```
fn evaluate_texture(art: Artifact) -> float:
    let palette = extract_palette(art)
    let coherence = 1.0 - variance(palette.map(|c| c.s))
    let contrast = (max(palette.map(|c| c.l)) - min(palette.map(|c| c.l)))
    return 0.5 * coherence + 0.5 * contrast
```

### Animation

Check motion smoothness via second-derivative bounded analysis. Animations whose joint accelerations exceed a threshold get penalized.

```
fn evaluate_animation(art: Artifact) -> float:
    if art has no animation: return 1.0
    let smoothness_scores = []
    for clip in art.animation_clips:
        let accels = second_derivatives(clip.joint_curves)
        let max_accel = max(accels)
        let s = 1.0 / (1.0 + max_accel * 0.01)
        smoothness_scores.push(s)
    return mean(smoothness_scores)
```

### Coherence

Cross-checks gene values against archetype expectations. If the archetype is "warrior" and the personality has high warmth + low aggression, coherence drops.

```
fn evaluate_coherence(art: Artifact) -> float:
    let archetype = art.metadata.archetype
    let expectations = lookup_archetype_expectations(archetype)
    let mut score = 1.0
    for (gene_name, expected_range) in expectations:
        let actual = art.metadata.genes[gene_name]
        if actual not in expected_range:
            score -= 0.1
    return clamp(score, 0.0, 1.0)
```

### Style

Distance to a style corpus in `dimensional` embedding space. The corpus is a Layer 4 memory of "good" seeds for each style tag. Closer = higher score.

```
fn evaluate_style(art: Artifact) -> float:
    let embedding = compute_style_embedding(art)
    let style_tag = art.metadata.style_tag
    let corpus = lookup_style_corpus(style_tag)
    let dist = min_cosine_distance(embedding, corpus)
    return 1.0 - clamp(dist, 0.0, 1.0)
```

### Novelty

Bell-curve at 0.15 deviation from the seed's k-nearest archive neighbors. Too similar to existing seeds → low novelty; too different → also low (incoherent); just right → high.

```
fn evaluate_novelty(art: Artifact, archive: ArchiveSnapshot) -> float:
    let neighbors = k_nearest(art, archive, k = 5)
    let avg_dist = mean(neighbors.map(|n| distance(art, n)))
    return gaussian(avg_dist, mean = 0.15, stddev = 0.1)
```

## The UCB1 Mutation Strategy Bandit

There are 8 mutation strategies:

```
enum MutationStrategy:
    refine_sdf
    smooth_surface
    enhance_color
    adjust_energy
    enforce_constraints
    add_detail
    adjust_proportions
    harmonize_palette
```

Each strategy is a function `Seed -> Seed` that mutates a specific aspect of the seed (the SDF field, the color palette, the energy parameters, etc.). The bandit picks which one to apply at each refinement step.

```
struct BanditState:
    counts: [int; 8]                  // times each strategy has been tried
    rewards: [float; 8]               // total reward from each strategy
    total_pulls: int

fn select_strategy(b: &BanditState) -> MutationStrategy:
    // Cold start: try each strategy at least once.
    for i in 0..8:
        if b.counts[i] == 0:
            return MutationStrategy::from_index(i)
    // UCB1: argmax_i (mean_reward_i + sqrt(2 * ln(N) / n_i))
    let mut best_i = 0
    let mut best_score = -infinity
    for i in 0..8:
        let mean_r = b.rewards[i] / b.counts[i]
        let bonus = sqrt(2.0 * ln(b.total_pulls as float) / b.counts[i] as float)
        let score = mean_r + bonus
        if score > best_score:
            best_score = score
            best_i = i
    return MutationStrategy::from_index(best_i)

fn update(b: &mut BanditState, strategy: MutationStrategy, reward: float):
    let i = strategy.to_index()
    b.counts[i] += 1
    b.rewards[i] += reward
    b.total_pulls += 1
```

The reward is the *improvement* in scalar QualityVector after the mutation:

```
reward = scalar(QV_after) - scalar(QV_before)
```

## The Refinement Loop

```
fn refine(seed: Seed, max_iterations: int, archive: ArchiveSnapshot) -> Seed:
    let mut bandit = BanditState::new()
    let mut current = seed
    let mut current_qv = evaluate_all(grow(current), archive)
    for _ in 0..max_iterations:
        let strategy = select_strategy(&bandit)
        let candidate = apply_strategy(strategy, current)
        let candidate_qv = evaluate_all(grow(candidate), archive)
        let reward = scalar(candidate_qv) - scalar(current_qv)
        update(&mut bandit, strategy, reward)
        if reward > 0:
            current = candidate
            current_qv = candidate_qv
    return current
```

The bandit state is **per-domain** (and optionally per-user). It accumulates across runs, so over time the platform learns which strategies are most effective for sprite vs character vs music etc.

## Determinism

- The bandit state is part of the run configuration; same initial state + same RNG → same trajectory.
- `select_strategy` is deterministic (no random in the cold-start path; UCB1 ties broken by lowest index).
- `evaluate_all` is deterministic given the artifact bytes.

## References

- Auer, Cesa-Bianchi, Fischer, *Finite-time Analysis of the Multiarmed Bandit Problem* (2002) — UCB1
- Lehman & Stanley, *Abandoning Objectives* (2008) — novelty as a fitness signal
- The QualityVector axes are an internal Paradigm choice; no single paper covers them
