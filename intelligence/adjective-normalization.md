# Adjective Normalization

## What it does

Natural language is full of adjectives — "melancholy," "fierce," "delicate," "ancient," "cheerful," "menacing" — that carry rich semantic information but cannot be used directly as gene values. The Adjective Normalization layer maps each adjective onto a structured *adjective vector* in a fixed semantic space, which the Template Bridge then projects onto specific gene paths.

This layer is what lets the agent translate "a melancholy bard" into actual numbers without inventing them on the fly.

## The semantic space

Every adjective resolves to a vector in a 12-dimensional space:

| Dim | Name | Range | Examples |
|---|---|---|---|
| 1 | valence | -1.0 (negative) to +1.0 (positive) | sad: -0.7, joyful: +0.9 |
| 2 | arousal | -1.0 (calm) to +1.0 (intense) | sleepy: -0.8, fierce: +0.9 |
| 3 | dominance | -1.0 (submissive) to +1.0 (dominant) | meek: -0.7, commanding: +0.8 |
| 4 | warmth | -1.0 (cold) to +1.0 (warm) | sterile: -0.7, cozy: +0.8 |
| 5 | weight | -1.0 (light) to +1.0 (heavy) | airy: -0.8, ponderous: +0.9 |
| 6 | speed | -1.0 (slow) to +1.0 (fast) | languid: -0.8, brisk: +0.7 |
| 7 | precision | -1.0 (rough) to +1.0 (precise) | crude: -0.7, exact: +0.9 |
| 8 | age | -1.0 (young/new) to +1.0 (old/ancient) | youthful: -0.8, ancient: +0.9 |
| 9 | luminosity | -1.0 (dark) to +1.0 (bright) | shadowy: -0.7, radiant: +0.9 |
| 10 | naturalness | -1.0 (artificial) to +1.0 (natural) | synthetic: -0.8, organic: +0.8 |
| 11 | rarity | -1.0 (common) to +1.0 (rare) | mundane: -0.7, exquisite: +0.8 |
| 12 | density | -1.0 (sparse) to +1.0 (dense) | minimal: -0.7, ornate: +0.9 |

These dimensions are based on (extended from) the **VAD** (Valence-Arousal-Dominance) model from emotion psychology, plus additional dimensions tailored to creative work.

## The lookup table

Adjectives are normalized via a curated lookup table with ~3,000 entries. Each entry maps an adjective to its 12D vector and a confidence weight:

```yaml
- word: "melancholy"
  vector:
    valence: -0.7
    arousal: -0.4
    dominance: -0.2
    warmth: -0.1
    weight: 0.4
    speed: -0.5
    precision: 0.0
    age: 0.3
    luminosity: -0.4
    naturalness: 0.2
    rarity: 0.1
    density: 0.0
  confidence: 0.95
  synonyms: ["sad", "wistful", "mournful", "pensive", "blue", "sombre"]
  antonyms: ["cheerful", "joyful", "exuberant"]

- word: "fierce"
  vector:
    valence: 0.0
    arousal: 0.9
    dominance: 0.8
    warmth: 0.3
    weight: 0.4
    speed: 0.6
    precision: 0.4
    age: 0.0
    luminosity: 0.2
    naturalness: 0.4
    rarity: 0.2
    density: 0.3
  confidence: 0.95
  synonyms: ["fearsome", "ferocious", "savage", "intense"]
  antonyms: ["gentle", "meek", "mild"]
```

The table is curated by hand for the top ~1,000 most common adjectives, then extended via semi-automated bootstrapping (an LLM proposes vectors for new adjectives, a curator approves or edits them) for the next ~2,000.

## Lookup with fallback

```
fn normalize(word: string) -> AdjectiveVector:
    let canonical = lemmatize(word.lowercase())
    if let Some(entry) = LOOKUP_TABLE.get(&canonical):
        return entry.vector.clone()
    // Fallback 1: synonym lookup
    if let Some(entry) = LOOKUP_TABLE.find_by_synonym(&canonical):
        return entry.vector.clone()
    // Fallback 2: nearest-neighbor in embedding space
    let embedding = WORD_EMBEDDING.get(&canonical)?
    let neighbors = LOOKUP_TABLE.knn_by_embedding(embedding, k = 5)
    return weighted_average(neighbors)   // by inverse distance
    // Fallback 3: ask the LLM (cached)
    return llm_propose_vector(canonical)
```

The fallback chain ensures that *no* adjective will fail to normalize. Even truly novel words ("bioluminescent," "subterranean") get a reasonable vector.

## Composing multiple adjectives

When the user provides multiple adjectives ("a melancholy AND fierce bard"), they are normalized individually then combined via *weighted vector average*:

```
fn normalize_phrase(words: [string], weights: [float]) -> AdjectiveVector:
    let vectors = words.map(normalize)
    let total_weight = sum(weights)
    let mut combined = zero_adjective_vector()
    for i in 0..vectors.length:
        for d in 0..12:
            combined[d] += vectors[i][d] * weights[i] / total_weight
    return combined
```

By default, all adjectives have equal weight. Modifiers like "very" or "slightly" adjust the weight (very: 1.5x, somewhat: 0.6x, slightly: 0.3x).

## Conflict detection

When two adjectives produce contradictory vectors (e.g., "joyful sad"), the agent does *not* silently average them. The CritiqueAgent flags the conflict and either:

1. Asks the user which they meant.
2. Resolves it via context (e.g., "bittersweet" pattern → small positive valence + small negative valence is intentional and actually encoded as a single vector).

```
fn detect_conflict(vectors: [AdjectiveVector]) -> Option<Conflict>:
    for d in 0..12:
        let values = vectors.map(|v| v[d])
        let span = max(values) - min(values)
        if span > 1.4:    // straddles more than 70% of the dimension's range
            return Some(Conflict { dimension: d, values })
    return None
```

## Projection onto gene paths

Once we have an `AdjectiveVector`, the Template Bridge projects it onto specific gene paths. Each template's modifier slots declare which dimensions affect which genes:

```yaml
- name: mood
  affects:
    - path: personality.warmth
      from_dim: warmth
      transfer: linear(0.5, 0.5)        # warmth dim [-1,1] → gene [0,1]
    - path: palette.value
      from_dim: luminosity
      transfer: linear(0.5, 0.5)
    - path: posture.openness
      from_dim: dominance
      transfer: linear(0.5, 0.5)
```

This declarative mapping means that *adding a new template never requires changing the normalization layer.* The lookup table is shared; only the projection rules change per template.

## Determinism

- The lookup table is a static, version-controlled asset (`adjectives.yaml` in the codebase mirror).
- `lemmatize` uses a deterministic morphological analyzer (no ML).
- Word embeddings (for the embedding-based fallback) are pinned to a specific model version + checksum.
- The LLM-based fallback (for truly novel words) is *cached forever* by `(word, model_version)` so it never produces different results for the same input.
- Compositions are pure functional vector averages.

The result: the same adjective phrase always normalizes to the same vector across runs, sessions, and agent versions.

## Quality measurement

The lookup table is validated against three test sets:

1. **Synonym coherence:** synonyms should have cosine similarity > 0.85.
2. **Antonym opposition:** antonyms should have cosine similarity < -0.5 on the relevant dimensions.
3. **Human alignment:** for a held-out set of 200 adjectives, the table's vectors should match human raters (Spearman > 0.7).

The table is rebuilt and re-validated whenever entries change. CI fails if any of the three metrics regresses.

## Limitations

- **Cultural specificity:** "warm" and "cold" mean different things in different cultures and aesthetic traditions. Our table is biased toward Western European language conventions. We plan to add culture-tagged variants in v2.
- **Domain-specific overloading:** "loud" in music vs. "loud" in fashion mean different things. We handle this with sub-tables per domain that override the global table.
- **Context-dependent meanings:** "killer" meaning excellent vs. literal. The agent uses surrounding context to disambiguate before normalizing.

## References

- Russell, *A Circumplex Model of Affect* (Journal of Personality and Social Psychology 1980) — VAD origins
- Mohammad, *Obtaining Reliable Human Ratings of Valence, Arousal, and Dominance for 20,000 English Words* (ACL 2018) — large-scale VAD ratings
- Mikolov et al., *Efficient Estimation of Word Representations in Vector Space* (2013) — word embeddings for fallback
