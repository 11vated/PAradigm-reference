# 036 — Novelty search and AURORA in GSPL space

## Question
How does novelty search work in seed space, what behavior characterization (BC) does it use, and how does AURORA *learn* the BC dimensions when they aren't obvious to a human?

## Why it matters
Critics have a hard time judging creative work. Novelty search side-steps the critic by rewarding *being different*. AURORA goes one step further: it learns *what dimensions of difference* matter from the data itself. Together they make GSPL's evolution useful for engines (like Music) where hand-engineered BCs feel arbitrary.

## What we know from the spec
- Brief 012 covered MAP-Elites (which uses BCs).
- Brief 035 named Novelty and AURORA as layers in the stack.

## Findings — novelty search

### The mechanism

Each candidate's *fitness* is its average distance (in BC space) from the K nearest neighbors in the **novelty archive**. The novelty archive is a growing collection of "interesting" past candidates. New candidates are added if they're far enough from existing entries.

```
score(candidate) = mean(distance(candidate, knn(candidate, archive, k=15)))
add to archive if score > threshold or with prob p
```

### Distance metrics per gene type

- For ColorGene: ΔE in OKLab.
- For VectorGene: cosine or L2.
- For EmbeddingGene: cosine in embedding space.
- For composite seeds: weighted sum of per-gene distances, with weights from the FIM diagonal (Brief 019) when available.
- For "behavior in output" (the *actual* novelty search use case): metrics on the rendered output, not the seed.

### When novelty search alone

Novelty-search-alone is the right tool when:
- Critics don't exist yet (cold start for a new engine).
- Critics are deceptive (chasing the critic plateaus quickly).
- The engine is *exploratory* (ALife, Procedural).

It is the *wrong* tool when:
- A clear quality target exists (e.g., "match this reference").
- Compute is scarce (novelty search is wasteful by design).

## Findings — AURORA

### The problem

MAP-Elites needs a behavior characterization. For sprite generation, "color hue" and "shape complexity" are obvious. For music, "what are the three numbers that summarize a song?" is genuinely hard.

### The AURORA approach

Train an autoencoder on a corpus of rendered outputs from the engine. The bottleneck layer (e.g., 3-8 dimensions) becomes the BC space for MAP-Elites. The encoder is fixed during evolution; the decoder is discarded.

### Adapted to GSPL

```
1. Collect N seeds (e.g., 5K) from random or warm-start population.
2. Render each seed; extract a feature vector (raw pixels, mel spectrogram, etc.).
3. Train a small autoencoder (encoder + decoder) on the feature vectors.
4. Pin the encoder; bottleneck is the BC space.
5. Run MAP-Elites with the learned BC.
```

### Why the encoder is *part of the seed's metadata*

The same seed renders to the same output, but the *position in BC space* depends on which encoder was used. If the encoder changes, the cell assignment changes. Mitigation:
- The encoder version is part of the MAP-Elites archive metadata.
- An archive bound to encoder v1 is invalid against encoder v2.
- Archives can be re-projected if the new encoder is similar enough (validated by a small test).

### When AURORA shines

- Music, where intuition fails on what BC dimensions to pick.
- Geometry3D, where "shape complexity" is too coarse.
- Cross-engine compositions, where each engine's BC feels arbitrary against the others.

### When AURORA fails

- Tiny corpora (< 1000 seeds): the autoencoder doesn't learn anything useful.
- Highly structured outputs where the autoencoder loses the structure (rare in practice).
- When user-interpretable BC dimensions matter more than learned ones (the user can't explain "the 3rd latent dimension").

### Hybrid: seed AURORA with one human-chosen dimension

The most reliable mode in practice: pick one or two human-chosen BC dimensions (e.g., "tempo" for music) and let AURORA fill the rest.

## Risks identified

- **Novelty archive bloat**: archive grows indefinitely. Mitigation: novelty archive is bounded; oldest-with-lowest-score evictions.
- **Novelty getting stuck in *novel-but-bad* regions**: pure novelty rewards weirdness regardless of quality. Mitigation: combine with a small fitness term (`score = α*novelty + (1-α)*fitness`).
- **AURORA encoder drift across versions**: a re-trained encoder breaks old archives. Mitigation: encoder versioning + validated re-projection.
- **AURORA cold start**: needs a corpus to train on. Mitigation: bootstrap from random seeds + a small global pretrained encoder per engine family.
- **AURORA dimensions are not human-interpretable**: the user can't reason about "BC dimension 4 = 0.7." Mitigation: hybrid mode (one human-chosen dimension); the studio surfaces "neighbors in BC space" UX rather than raw values.

## Recommendation

1. **Adopt novelty search as a v1 algorithm** with default α=0.3 (mostly fitness, some novelty).
2. **Adopt AURORA as a v1 BC discovery mechanism** for engines that opt in.
3. **Encoder versioning is part of the archive metadata.** Re-projection on upgrades.
4. **Hybrid AURORA + human BC dimensions** is the recommended default.
5. **Bootstrap encoders ship with the engine** for the four engines where AURORA is the default (Music, Geometry3D, ALife, Procedural).
6. **Novelty archive bounded** at 10K entries per engine; oldest-lowest evictions.
7. **AURORA encoders are small** (≤ 1M params); training is on-device.

## Confidence
**4/5.** Both algorithms have strong literature and successful applications. The 4/5 reflects the unproven combination at GSPL's heterogeneous engine scale.

## Spec impact

- `algorithms/evolution/novelty.md` — full novelty pseudocode and distance metrics.
- `algorithms/evolution/aurora.md` — AURORA training and BC extraction.
- `architecture/aurora-encoders.md` — bootstrap encoder catalog.
- `tests/novelty-aurora-conformance.md`.
- New ADR: `adr/00NN-aurora-encoder-versioning.md`.

## Open follow-ups

- Train and ship bootstrap encoders for the 4 default-AURORA engines. Phase 1.
- A/B test α values (novelty/fitness mix) per engine.
- Decide on the encoder architecture (likely small CNN or VQ-VAE).
- Build the studio's "neighbors in BC space" UX (Brief 049).

## Sources

- Lehman & Stanley, *Abandoning Objectives*.
- Cully, *Autonomous Skill Discovery with Quality-Diversity and Unsupervised Descriptors*.
- Internal: Briefs 012, 035, 049.
