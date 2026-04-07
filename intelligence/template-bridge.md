# Template Bridge

## What it does

The Template Bridge is the interface between the GSPL Agent's *plan-level* output (a high-level construction plan in human-readable terms) and the engine's *gene-level* input (a fully-specified gene assignment vector). It is the layer where words like "muted earth tones" become `palette: { hue: 30, saturation: 0.3, value: 0.55, harmony: "analogous", desaturation: 0.4 }`.

Without the bridge, the GSPL Agent would have to know every gene of every engine in detail and hallucinate values directly. With the bridge, the agent only has to pick a *template* and a small set of high-level *modifiers*, and the bridge fills in the 50–500 actual gene values from a curated library.

## Why a bridge

Three reasons:

1. **Determinism.** Templates are versioned, hand-curated artifacts. Same template + same modifiers = same gene values. The agent's role is reduced to *selection*, which is much easier to validate than *generation*.
2. **Quality floor.** Curated templates are guaranteed to produce sensible output. The agent's worst case is "boring but correct" rather than "broken."
3. **Maintainability.** When an engine adds a new gene, only the templates need to be updated. The agent code does not need to know.

## Anatomy of a template

```
struct Template:
    id: string                       // e.g., "musician_archetype"
    engine: Domain                   // which engine this targets
    version: SemVer
    description: string              // human-readable
    base_genes: GeneSet              // the default values
    modifier_slots: [ModifierSlot]   // the parameters the agent can fill in
    examples: [SeedRef]              // example seeds produced from this template
    tags: [string]
    author: UserRef
    license: License

struct ModifierSlot:
    name: string                     // e.g., "mood"
    type: ModifierType               // categorical | scalar | vector | reference
    domain: ModifierDomain           // valid values or range
    affects: [GenePath]              // which genes this modifier touches
    default: ModifierValue
    description: string
```

A template is a function: `(modifier_values) → fully_specified_seed`. The function is deterministic.

## Example template

```yaml
id: musician_archetype
engine: Character
version: 2.1.0
description: A character defined primarily by their musical practice.
base_genes:
  body_morph:
    height: 1.75
    build: "lean"
  outfit:
    layers: 3
    silhouette: "flowing"
  signature_pose: "seated_with_instrument"
  hands:
    dexterity_emphasis: 0.85
modifier_slots:
  - name: instrument
    type: categorical
    domain: ["harp", "lute", "flute", "fiddle", "drum", "voice"]
    affects: [outfit.accessories, signature_pose, hands.shape]
    default: "lute"
  - name: era
    type: categorical
    domain: ["medieval", "renaissance", "baroque", "modern", "fantasy"]
    affects: [outfit.style, palette]
    default: "fantasy"
  - name: mood
    type: scalar
    domain: { min: -1.0, max: 1.0 }
    affects: [personality.warmth, palette.value, posture.openness]
    default: 0.0
  - name: virtuosity
    type: scalar
    domain: { min: 0.0, max: 1.0 }
    affects: [hands.dexterity_emphasis, signature_pose.confidence]
    default: 0.6
```

When the agent says "musician_archetype with `instrument=harp, era=medieval, mood=-0.6, virtuosity=0.85`," the bridge produces a fully-specified Character seed with all 47 genes set deterministically.

## The bridge algorithm

```
fn apply_template(template: &Template, modifiers: &Map<string, ModifierValue>) -> Seed:
    let mut seed = empty_seed(template.engine)

    // Step 1: Apply base genes.
    for (path, value) in &template.base_genes:
        seed.set(path, value)

    // Step 2: Apply each modifier in declared order.
    //   Order matters because later modifiers can override earlier ones.
    for slot in &template.modifier_slots:
        let value = modifiers.get(slot.name).unwrap_or(&slot.default)
        validate_value(value, slot.domain)?
        let gene_updates = compute_modifier_effect(slot, value)
        for (path, gene_value) in gene_updates:
            seed.set(path, gene_value)

    // Step 3: Apply derived genes (computed from other genes).
    let derived = template.derived_gene_rules.iter().map(|rule| rule.evaluate(&seed))
    for (path, value) in derived:
        seed.set(path, value)

    // Step 4: Validate the resulting seed.
    seed.validate_against_schema(template.engine.schema())?
    return seed
```

## Modifier effect computation

The most subtle part of the bridge is `compute_modifier_effect`. A scalar modifier like `mood: -0.6` doesn't just write `personality.warmth = -0.6` — it has a *transfer function* defined per gene path:

```
fn compute_modifier_effect(slot: &ModifierSlot, value: &ModifierValue) -> [(GenePath, GeneValue)]:
    let mut updates = []
    for path in &slot.affects:
        let transfer_fn = slot.transfer_for(path)
        let new_value = transfer_fn(value)
        updates.push((path.clone(), new_value))
    return updates
```

Transfer functions are declared inside the template. They can be:

- **identity:** `gene_value = modifier_value`
- **linear:** `gene_value = a * modifier_value + b`
- **piecewise:** lookup table (e.g., "harp" → `accessory = harp_model`)
- **scaled curve:** `gene_value = (modifier_value + 1) / 2 * (max - min) + min`
- **conditional:** `if modifier == "medieval" { palette = "muted_earth" } else { ... }`

The transfer functions are written in a tiny domain-specific sub-language that the agent doesn't need to understand — the template author writes them once.

## Template composition

Templates compose. If the agent picks `musician_archetype` for the Character and `solo_harp_melancholy` for the Music, the bridge applies both, then the cross-domain functor `character_to_music` ties their gene spaces together.

```
fn compose_templates(templates: [(Template, Modifiers)]) -> CompositeSeed:
    let primary_seed = apply_template(&templates[0].0, &templates[0].1)
    let mut composite = CompositeSeed::primary(primary_seed)
    for i in 1..templates.length:
        let sub_seed = apply_template(&templates[i].0, &templates[i].1)
        composite.add_secondary(sub_seed)
    composite.bind_via_functors(/* automatic */)
    return composite
```

## Template registry

Templates live in a versioned registry (`templates/` directory in the codebase mirror, plus a runtime database). Each template has:

- A SemVer version. Bumping the major version is a breaking change; the agent considers `v2.x` and `v1.x` to be different templates.
- A diff history.
- Approval status: draft, review, approved, deprecated.
- Usage statistics (how many seeds were produced from it, mean quality, etc.).

The agent's planning stage selects templates from this registry based on intent classification, taking only templates with `status >= approved`.

## How the agent picks a template

In Stage 3 (Plan), the agent does:

```
1. List all approved templates for the inferred primary domain.
2. For each candidate, score it against the resolved spec:
   - Tag overlap (e.g., resolved spec has "musician" tag → templates tagged "musician" score high)
   - Modifier slot coverage (templates whose modifier_slots match the resolved spec's modifiers score high)
   - Recency-weighted user preference (this user has used template X 10 times → small bonus)
3. Pick the highest-scoring template, with ties broken by lexicographic ID.
4. Map the resolved spec's modifier values onto the chosen template's slot names.
5. Emit a ConstructionPlan that names the template and the modifier values.
```

This is the entire LLM-touching logic for template selection. Once the template is chosen, the bridge takes over and produces the seed deterministically.

## Why this matters

The Template Bridge is the *single most important reason* the GSPL Agent's output is reproducible. Without it, every seed would depend on whatever the LLM hallucinated for each gene at sample time. With it, the LLM only picks templates and high-level knobs, and the engine's behavior is bounded by curated, version-controlled, hand-reviewed templates.

The agent can be wrong about which template to pick — but it cannot be wrong about what a template *means*. The bridge guarantees that.

## Versioning and migration

When a template is bumped to a new version:

- Existing seeds reference the *old* version by exact ID.
- New agent runs use the *new* version by default.
- The migration tool can be invoked to re-derive a seed against the new template version, but this *creates a new seed* (with a new hash and lineage edge), not an in-place rewrite.

This is consistent with Paradigm's "seeds are immutable" principle.

## References

- The pattern is similar to "skinning" in game character creators (e.g., Black Desert's appearance editor).
- HuggingFace's `pipeline()` API has a similar selector-bridge dynamic for ML models.
- Adobe Substance Designer's "graph templates" use a comparable structure for material authoring.
