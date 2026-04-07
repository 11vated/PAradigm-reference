# The GSPL Agent: 5-Stage Concept-to-Seed Pipeline

## What it does

The GSPL Agent takes a natural-language description (the "concept") and produces a fully-formed, signed, deterministic GSPL seed. It is the front door of the Intelligence layer and the only path by which natural language enters Paradigm.

The agent runs in **5 stages**, each with a clear input, a clear output, and a quality gate:

```
Concept (string)
   │
   ▼
[1] Parse        ─────►   ParsedIntent
   │
   ▼
[2] Resolve      ─────►   ResolvedSpec
   │
   ▼
[3] Plan         ─────►   ConstructionPlan
   │
   ▼
[4] Assemble     ─────►   DraftSeed
   │
   ▼
[5] Validate     ─────►   FinalSeed (signed)
```

Each stage is independently testable and replaceable. Stages 1, 2, and 3 are LLM-driven (with structured-output enforcement). Stages 4 and 5 are deterministic transformations that do *not* call LLMs — once Stage 3 completes, the rest of the pipeline is reproducible.

## Stage 1: Parse

**Input:** raw user concept string (e.g., "a melancholy bard who plays a harp in a forgotten cathedral")

**Output:** `ParsedIntent` — a structured tree of:

- **primary_subject** — "bard"
- **primary_domain** — "Character" (inferred from the subject taxonomy)
- **modifiers** — `["melancholy"]`
- **objects** — `[{ noun: "harp", verb: "plays" }]`
- **setting** — `"forgotten cathedral"`
- **secondary_domains** — `["Music", "Architecture"]` (inferred from objects and setting)
- **emotional_tone** — `["melancholy", "wistful", "reverent"]`
- **explicit_constraints** — `[]` (none in this concept; would be `["max_height: 1.8m"]` if user said so)

**LLM call:** structured-output JSON mode against the `ParsedIntent` schema. Provider: cheap tier (gpt-4o-mini, claude-haiku, gemini-flash). Temperature: 0.0 for determinism within a session.

**Quality gate:** schema validation, plus a confidence threshold from the LLM. If confidence < 0.7, the agent asks the user a clarifying question rather than proceeding.

## Stage 2: Resolve

**Input:** `ParsedIntent`

**Output:** `ResolvedSpec` — a richly-annotated version of the parsed intent with:

- **canonical_archetype** — looked up from the archetype library: `"melancholic_bard"`
- **archetype_genes** — the gene template for that archetype: `{ warmth: 0.6, melancholy: 0.85, energy: 0.3, ... }`
- **secondary_archetypes** — for each secondary domain, the corresponding archetype
- **adjective_mappings** — each modifier resolved against the adjective normalization table (see [`adjective-normalization.md`](adjective-normalization.md)): `melancholy → { mood: "low", tempo_modifier: -0.2, color_temp: -0.3, ... }`
- **knowledge_snippets** — facts retrieved from Layer 4 memory (the long-term knowledge base) that are relevant: e.g., the medieval bard tradition, what a harp's range is, what a Gothic cathedral's acoustic profile sounds like
- **contradictions_resolved** — any modifier conflicts and how they were reconciled

**LLM call:** retrieval-augmented prompt against the long-term memory layer. Provider: mid tier (gpt-4o, claude-sonnet-4, gemini-2.5-pro). Temperature: 0.2.

**Quality gate:** every resolved modifier must map to a known adjective bucket; unknown adjectives trigger a fallback prompt. The CritiqueAgent (see [`8-sub-agents.md`](8-sub-agents.md)) reviews the spec for internal consistency.

## Stage 3: Plan

**Input:** `ResolvedSpec`

**Output:** `ConstructionPlan` — a directed graph of seed-construction operations:

```json
{
  "primary": {
    "engine": "Character",
    "template": "musician_archetype",
    "gene_overrides": {
      "personality.melancholy": 0.85,
      "personality.warmth": 0.5,
      "outfit.style": "medieval_robes",
      "outfit.color_palette": "muted_earth_tones",
      "signature_pose": "seated_with_instrument"
    }
  },
  "composes_with": [
    {
      "engine": "Music",
      "template": "solo_harp_melancholy",
      "gene_overrides": { "tempo": 60, "key": "D minor", "dynamics": "pp" },
      "functor": "character_to_music"
    },
    {
      "engine": "Architecture",
      "template": "gothic_cathedral_ruined",
      "gene_overrides": { "decay_level": 0.7, "lighting": "candlelight" }
    }
  ],
  "lineage_tags": ["agent:gspl", "intent:character", "concept_hash": "...sha256..."]
}
```

This is the most LLM-intensive stage. The ConstructionPlan must respect the engine's published gene schema; the LLM is constrained by tool calls that validate each gene name against the engine's `geneSchema`.

**LLM call:** structured-output with tool calls for gene-name validation. Provider: top tier (gpt-4o, claude-opus-4). Temperature: 0.4 (higher for creative variation in template selection).

**Quality gate:** every gene name in `gene_overrides` must exist in the engine's schema and the value must be in range. The plan is run through a *dry assemble* (Stage 4 with no commit) to verify it produces a valid seed.

## Stage 4: Assemble

**Input:** `ConstructionPlan`

**Output:** `DraftSeed` — a fully-formed but unsigned seed JSON object.

This stage is **fully deterministic** and contains *no LLM calls*. It is a pure function of the construction plan:

```
fn assemble(plan: ConstructionPlan) -> DraftSeed:
    let mut seed = empty_seed(plan.primary.engine)
    seed.apply_template(plan.primary.template)
    for (path, value) in plan.primary.gene_overrides:
        seed.set(path, value)
    for composition in plan.composes_with:
        let sub_seed = empty_seed(composition.engine)
        sub_seed.apply_template(composition.template)
        for (path, value) in composition.gene_overrides:
            sub_seed.set(path, value)
        if composition.functor != null:
            seed = apply_functor(composition.functor, seed, sub_seed)
        else:
            seed.compose(sub_seed)
    seed.lineage_tags = plan.lineage_tags
    return seed
```

The assembler is the *reproducibility boundary*. From this point on, the same plan will always produce the same draft seed, regardless of which LLMs were involved upstream.

## Stage 5: Validate

**Input:** `DraftSeed`

**Output:** `FinalSeed` — a signed, hashed, ready-to-store seed.

Validation steps (all deterministic, no LLM):

1. **Schema validation** — every gene must conform to the engine's published schema.
2. **Engine smoke test** — instantiate the engine and run all stages with the seed; if any stage throws, fail.
3. **Quality gate** — run a single iteration of the refinement loop's `evaluate_all` and reject if `scalar(QualityVector) < 0.4`.
4. **Canonicalization** — JCS-canonicalize the seed JSON.
5. **Hashing** — SHA-256 of the canonical bytes; embedded as `seed.$hash`.
6. **Signing** — ECDSA-P256 over the hash with the user's sovereignty key.
7. **Lineage commit** — write any parent edges to the lineage table.

If validation fails, the agent loops back to Stage 3 with a critique describing what went wrong, and tries up to 3 times. After 3 failures, it surfaces the error to the user with a clarifying-question prompt.

## End-to-end example

**User concept:** *"a melancholy bard who plays a harp in a forgotten cathedral"*

1. **Parse** → `{ subject: "bard", domain: "Character", modifiers: ["melancholy"], objects: [{noun:"harp",verb:"plays"}], setting:"forgotten cathedral", secondary_domains: ["Music","Architecture"] }`
2. **Resolve** → archetype `melancholic_bard`, harp range `B0-G7`, gothic cathedral RT60 ≈ 7s, melancholy → `mood:-0.6, tempo_mod:-0.2, color_temp:-0.3`
3. **Plan** → primary Character + composed Music + composed Architecture as shown above
4. **Assemble** → draft seed with all genes set, lineage tags applied
5. **Validate** → schema OK, engine smoke OK, quality 0.78, hash + sign → final seed

Total wall time: 4-12 seconds depending on provider. Total LLM cost: ~\$0.02 with gpt-4o, ~\$0.04 with claude-opus-4.

## Determinism boundary

| Stage | LLM? | Deterministic? |
|---|---|---|
| 1. Parse | yes | per-session only |
| 2. Resolve | yes | per-session only |
| 3. Plan | yes | per-session only |
| 4. Assemble | no | yes, always |
| 5. Validate | no | yes, always |

The output of Stage 3 is *cached* by `(concept_hash, agent_version, model_version)`, so the same concept asked twice in a row gives the same plan. The cache is invalidated when the agent version or model version changes.

## Failure modes

- **Ambiguous concept** ("make me something cool") → agent asks 1-3 clarifying questions before proceeding.
- **Out-of-domain concept** ("calculate the meaning of life") → polite refusal with explanation.
- **Adversarial input** (prompt injection attempts) → input is sanitized and never used as a control instruction; the agent treats user text as data.
- **Provider outage** → fallback chain across providers; if all fail, surface a "platform degraded" message.
- **Validation loop fails 3×** → surface specific gene-name and value errors so the user (or a human reviewer) can debug.

## References

- ReAct: Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* (ICLR 2023)
- Tree of Thoughts: Yao et al., *Tree of Thoughts: Deliberate Problem Solving with Large Language Models* (NeurIPS 2023)
- Toolformer: Schick et al., *Toolformer: Language Models Can Teach Themselves to Use Tools* (NeurIPS 2023)
