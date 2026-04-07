# 032 — Adjective normalization and intent taxonomy

## Question
How does the GSPL Agent normalize ambiguous natural-language intent ("make it more warm and dreamy") into a typed manipulation of gene values, and what is the canonical intent taxonomy that downstream sub-agents consume?

## Why it matters
Adjectives are the user's main verb. "Warm," "dreamy," "punchy," "epic," "minimal" — these are how creators talk. The agent must convert each adjective into something the kernel understands. If "warm" maps to a different gene direction every time, users feel the system is unpredictable. If it maps consistently, users feel the system is *understanding*.

## What we know from the spec
- Brief 029 referenced an "intent normalizer" as the input to the Planner.
- Brief 031 introduced per-user vocabulary mappings.

## Findings — the normalization pipeline

### Stage 1: Tokenization

The user's natural-language input is tokenized into: **noun phrases** (subjects), **verb phrases** (intents), **adjective phrases** (modifiers), **negations**, and **constraints**.

Example input: *"Make a cozy autumn sprite, but more punchy and not too dark."*

Tokenized:
- subject = "sprite"
- intent = "make"
- modifiers (positive) = "cozy", "autumn", "punchy"
- modifiers (negative) = "dark"
- intensities = "more", "not too"

### Stage 2: Subject → engine resolution

A small typed table maps subject nouns to engines.

| Subject token | Resolves to | Confidence |
|---|---|---|
| sprite, character art, illustration | SpriteEngine | high |
| song, music, beat, soundtrack | MusicEngine | high |
| level, dungeon, map | GameEngine.world | high |
| story, plot, arc | NarrativeEngine | high |
| menu, button, hud | UIEngine | high |
| world, planet, biome | WorldEngine | high |
| ... | ... | ... |

Unresolved subjects trigger a clarifying question to the user (interactive mode) or a guess + a low-confidence flag (autonomous mode).

### Stage 3: Modifier → adjective category

Each modifier is assigned a **category** from a fixed taxonomy. The taxonomy is the canonical adjective ontology for GSPL.

**The 12 modifier categories:**

| # | Category | Examples | Maps to (Core gene) |
|---|---|---|---|
| 1 | **Energy** | calm, energetic, sleepy, frantic, lively, drowsy | `core.energy` |
| 2 | **Valence** | happy, sad, melancholy, joyful, somber, uplifting | `core.valence` |
| 3 | **Temperature** | warm, cool, cold, hot, icy, sun-baked | `core.palette` (chroma+hue shift) |
| 4 | **Density** | dense, sparse, busy, minimal, packed, airy | `core.density` |
| 5 | **Complexity** | simple, intricate, ornate, plain, baroque | `core.complexity` |
| 6 | **Tempo** | fast, slow, brisk, languid, snappy, stately | `core.tempo` |
| 7 | **Brightness** | bright, dim, vivid, muted, glowing, dull | `core.palette` (lightness shift) |
| 8 | **Roughness** | smooth, gritty, polished, raw, refined, jagged | engine-specific (material, texture) |
| 9 | **Scale** | epic, intimate, vast, tiny, monumental, modest | engine-specific (size, count) |
| 10 | **Style** | retro, modern, futuristic, gothic, kawaii, cyberpunk | `style.embedding` (Brief 020) |
| 11 | **Mood** | cozy, eerie, dreamy, tense, playful, ominous | composite of valence + energy + tempo |
| 12 | **Theme** | autumn, winter, ocean, desert, neon, pastel | composite of palette + style + structure |

**Multiple categories per modifier are allowed**: "epic" might be both Scale and Mood, with weights.

### Stage 4: Modifier → gene delta

Each `(modifier, category, intensity)` triple resolves to a **typed gene delta**: a small list of `(gene_path, operator, magnitude)` tuples.

- Operator is one of `set`, `nudge_up`, `nudge_down`, `replace`, `mix`.
- Magnitude is from a small set: `slight` (0.1σ), `moderate` (0.3σ), `strong` (1.0σ), `extreme` (3.0σ).
- Intensity modifiers ("more", "not too", "very", "slightly") map to magnitude bands.

Example: `(warm, Temperature, moderate)` → `[(palette.*.hue, nudge_up, 0.3σ), (palette.*.chroma, nudge_up, 0.2σ)]` (approximate; exact values per engine).

### Stage 5: Per-user override

The user's vocabulary mapping (Brief 031) can override default deltas. If the user has historically interpreted "warm" as a specific palette range, the override wins.

### Stage 6: Conflict resolution

Conflicting modifiers ("dark" + "bright") are reconciled by:
1. If one is negated ("not too dark"), the negated one becomes a constraint on the other ("bright but not too bright").
2. Otherwise, last-wins with a warning surfaced to the user.

### Stage 7: Output to Planner

Output of normalization is a typed `Intent` struct:
```
Intent {
  engine: EngineId,
  subject_modifiers: [GeneDelta],
  constraints: [Constraint],
  references: [seed_id],
  mode: "create" | "edit" | "remix" | "evolve",
  context: { user_id, session_id, prior_seeds }
}
```

The Planner consumes this. No sub-agent below the Planner sees the raw user text.

## Risks identified

- **Adjective ambiguity**: "warm" can mean many things in many engines. Mitigation: per-engine resolution table, falling back to `core.palette` direction.
- **Cultural variance**: "epic" means different things across cultures and audiences. Mitigation: per-user vocabulary mapping captures this over time.
- **Adversarial prompts** (e.g., "make it inappropriate"): the normalizer must refuse or sanitize. Mitigation: negative-modifier blocklist with safety-tier filtering.
- **Synonym explosion**: "warm" ≈ "cozy" ≈ "snug" — listing all synonyms is a maintenance burden. Mitigation: a small embedding-based synonym matcher backs the explicit table.
- **Intensity confusion**: "really really" → ?. Mitigation: cap intensity at `extreme` (3σ) regardless of stacking.

## Recommendation

1. **Adopt the seven-stage normalization pipeline** in `algorithms/intent-normalization.md`.
2. **The 12-category modifier taxonomy is normative** at v1, with a versioning rule (additive only).
3. **The subject→engine resolution table is normative**.
4. **Per-engine modifier→delta tables** live in each engine's spec.
5. **Per-user vocabulary overrides take precedence** over defaults.
6. **The Intent struct is the only thing the Planner sees**, never raw text.
7. **A safety blocklist** rejects unsafe modifiers before normalization completes.
8. **Synonym matching via a small frozen embedding table** that ships with the agent.

## Confidence
**3/5.** The taxonomy is sound and matches established UX research on creative tooling vocabulary, but the per-modifier→delta tables are unmeasured and will need iteration.

## Spec impact

- `algorithms/intent-normalization.md` — pipeline pseudocode.
- `architecture/intent-taxonomy.md` — the 12 categories with normative semantics.
- `engines/*/modifier-deltas.md` — per-engine delta tables.
- New ADR: `adr/00NN-intent-taxonomy-v1.md`.

## Open follow-ups

- Build the per-engine modifier→delta tables for the 19 v1 engines. Phase 1.
- A/B test default deltas vs user-tuned deltas in Phase 2.
- Decide on the safety blocklist contents (cross-reference Brief 060).
- Investigate whether a small fine-tuned classifier outperforms the embedding synonym matcher.

## Sources

- Cognitive linguistics literature on adjective grading.
- Stanley & Lehman, *Why Greatness Cannot Be Planned* (vocabulary as steering).
- Internal: Briefs 016 (Core), 020 (EmbeddingGene), 029, 031.
