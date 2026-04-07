# Intent Taxonomy

## What it does

When the GSPL Agent receives a natural-language concept, the very first thing Stage 1 (Parse) must do is classify the user's *intent*. Different intents take wildly different paths through the pipeline. Asking the agent to "make a sprite" is a Creation intent; asking "what would a happier version of this look like?" is a Variation intent; asking "rebuild this with the new music engine" is a Migration intent. Treating them all the same produces bad results.

The Intent Taxonomy is a fixed, hierarchical classification of all the things users can ask Paradigm to do.

## Top-level intents

| Intent | Description | Example phrasing |
|---|---|---|
| **Creation** | Produce a new seed from scratch | "make me a melancholy bard" |
| **Variation** | Produce variants of an existing seed | "now make a happier version" |
| **Composition** | Combine two or more existing seeds | "put this character in this music" |
| **Translation** | Cross-domain functor application | "show what this character would sound like" |
| **Refinement** | Improve an existing seed against a quality target | "make the texture sharper" |
| **Inspection** | Read or explain an existing seed | "what genes drive its color palette?" |
| **Migration** | Re-derive a seed under a new template/engine version | "rebuild with v2 of the character template" |
| **Marketplace** | Browse, search, or buy seeds | "find seeds like this one" |
| **Project** | Workspace management actions | "create a new project for my game" |
| **Help** | Documentation, how-to, tutorial requests | "how do I export to Godot?" |

These 10 top-level intents are mutually exclusive at the conversation-turn level. A conversation can drift between them across turns.

## Sub-intents

Each top-level intent has a small fan-out of sub-intents:

### Creation
- `creation.from_concept` — full natural-language description
- `creation.from_template` — explicit template ID + modifiers
- `creation.from_reference_image` — image upload + "make this"
- `creation.from_audio` — audio upload + "make a sprite for this music"
- `creation.from_seed_lineage` — "make a child of this seed"

### Variation
- `variation.style_swap` — same content, different style
- `variation.modifier_change` — change one or two modifiers
- `variation.random_explore` — "give me a few different takes"
- `variation.targeted_axis` — "more melancholy"

### Composition
- `composition.character_with_environment`
- `composition.character_with_music`
- `composition.scene` — multiple characters + environment
- `composition.collection` — gallery of related seeds

### Translation
- `translation.functor_explicit` — user names a functor
- `translation.functor_inferred` — user describes the target domain in words

### Refinement
- `refinement.quality_axis` — improve a specific QualityVector axis
- `refinement.constraint_satisfaction` — meet a hard constraint
- `refinement.iterative_critique` — apply a user critique

### Inspection
- `inspection.gene_explanation` — what does this gene do?
- `inspection.lineage_trace` — where did this come from?
- `inspection.quality_report` — how good is this seed?
- `inspection.compatibility` — would this work in engine X?

### Migration
- `migration.template_version_bump`
- `migration.engine_version_bump`
- `migration.cross_engine_port`

### Marketplace
- `marketplace.search`
- `marketplace.recommendation`
- `marketplace.purchase`
- `marketplace.publish`

### Project
- `project.create`
- `project.organize`
- `project.export`
- `project.invite_collaborator`

### Help
- `help.how_to`
- `help.troubleshoot`
- `help.documentation_lookup`

Total: 33 sub-intents. The taxonomy is small enough to be hand-curated and exhaustive enough to cover virtually every reasonable user request.

## Routing

Each (intent, sub-intent) pair has a routing rule that tells the GSPL Agent which pipeline branch to take:

```
fn route(intent: Intent, sub_intent: SubIntent) -> Pipeline:
    match (intent, sub_intent):
        (Creation, FromConcept)        -> standard_5_stage_pipeline
        (Creation, FromTemplate)       -> short_pipeline_skip_to_assemble
        (Creation, FromReferenceImage) -> reference_extract + standard_pipeline
        (Variation, StyleSwap)         -> retrieve_parent + style_substitute_pipeline
        (Variation, ModifierChange)    -> retrieve_parent + modifier_diff_pipeline
        (Variation, RandomExplore)     -> retrieve_parent + evolution_one_step
        (Variation, TargetedAxis)      -> retrieve_parent + refinement_one_axis
        (Composition, _)               -> retrieve_parents + composition_pipeline
        (Translation, FunctorExplicit) -> retrieve_parent + functor_apply
        (Translation, FunctorInferred) -> retrieve_parent + functor_pathfind + apply
        (Refinement, _)                -> retrieve_parent + refinement_pipeline
        (Inspection, _)                -> read_only_response
        (Migration, _)                 -> retrieve_parent + migration_pipeline
        (Marketplace, _)               -> marketplace_action
        (Project, _)                   -> project_action
        (Help, _)                      -> documentation_lookup
```

This routing is the *first* deterministic step after intent classification, and it dramatically simplifies the rest of the pipeline because each branch only has to handle one intent class.

## Classification

Intent classification is done in Stage 1 (Parse) by an LLM call with structured output:

```
fn classify_intent(user_message: string, recent_context: ConversationHistory) -> (Intent, SubIntent, float):
    let prompt = build_classification_prompt(user_message, recent_context)
    let response = llm_call(prompt, schema = INTENT_SCHEMA, temperature = 0.0)
    return (response.intent, response.sub_intent, response.confidence)
```

The model is given the full taxonomy as part of its system prompt and is constrained to return a `(intent, sub_intent)` pair from the enumerated set. Confidence is the model's self-reported certainty.

## Confidence handling

```
fn handle_classification(intent: Intent, sub_intent: SubIntent, confidence: float):
    if confidence >= 0.85:
        return route(intent, sub_intent)
    if confidence >= 0.6:
        return route_with_confirmation(intent, sub_intent)   // ask user "did you mean?"
    return ask_clarifying_question()
```

For confidence below 0.6, the agent asks the user a clarifying question before committing. The clarifying question is itself templated by the candidate intent — different intents need different disambiguating questions.

## Multi-intent turns

Sometimes the user packs multiple intents into one message: "make me a bard and find me similar seeds in the marketplace." The agent handles this by:

1. Classifying as the *primary* intent (Creation in this case).
2. Recognizing the secondary intent (Marketplace.search).
3. Sequencing them: complete the primary, then surface the secondary as a follow-up offer ("Done! Want me to also search the marketplace for similar bards?").

The taxonomy doesn't explicitly model multi-intent turns; sequencing is the agent's job.

## Determinism

- Classification itself is not deterministic (LLM call).
- The (intent, sub_intent) → routing map *is* deterministic.
- The routing decision is logged and replayable.
- Re-classifying a cached message returns the cached classification, not a fresh LLM call.

## Versioning

The taxonomy is part of the agent's published interface. Changes to it are SemVer-tracked:

- **Patch:** rewording of a sub-intent description.
- **Minor:** adding a new sub-intent (does not break existing classifiers).
- **Major:** renaming, removing, or moving an intent (breaks classifiers).

The agent records the taxonomy version it used at classification time so old conversations can be replayed correctly.

## Why not more intents

Three temptations to grow the taxonomy must be resisted:

1. **Domain-specific intents** ("create_sprite," "create_character") — wrong because the domain is part of the *resolved spec*, not the intent. The intent is the user's *action* (creation), not their target.
2. **Engine-specific intents** ("evolve_via_map_elites") — wrong because algorithm choice is a planning detail, not a user action.
3. **Granular sub-intents** ("create_bard," "create_warrior") — wrong because there's no end to this; the user's free-text content carries the specifics.

The 10/33 split is the right size: small enough to memorize, large enough to be useful.

## References

- *Slot Filling and Intent Classification for Dialog Systems* — long line of NLP research
- *Anthropic's Model Card on Tool Use* and structured-output enforcement patterns
