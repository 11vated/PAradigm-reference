# 028 — INV: Cross-engine emergent compositions

## Question
What net-new compositional patterns become possible *only* because GSPL has a typed gene system across many engines, and how does GSPL surface, encourage, and exploit those patterns? What can we *invent* here that no rival can reproduce?

## Why it matters
The 26 engines in isolation are competitive at best. Their *composition* is GSPL's unfair advantage. If composition is just "use a sprite and a sound together" — every game engine already does that. The interesting thing is what falls out of *typed gene-level* composition: emergent behaviors that appear because two engines share gene primitives. This brief invents the catalog of composition patterns to expose deliberately.

## What we are inventing and why
A *catalog of cross-engine composition patterns* with names, semantics, and concrete examples. Each pattern is an inference rule the studio can suggest, the agent can apply, and the evolution stack can exploit. Naming them gives users a vocabulary; documenting them creates a moat.

## Findings — the 12 inventive composition patterns

### 1. **Palette Inheritance**
- **Definition:** A child seed in domain A inherits its palette from a parent seed in domain B by reading the parent's `palette.*` ColorGenes through the Core projection.
- **Example:** A MusicEngine seed for a "warm autumn" mood inherits its instrumentation timbre choices from the OKLab `palette.primary` of an associated SpriteEngine seed via the Core energy/valence projection.
- **Why novel:** Music doesn't usually inherit *color palettes*, but the Core projection gives a meaningful translation: warm colors → warmer instrumentation, cool colors → colder.

### 2. **Tension Lock**
- **Definition:** A NarrativeEngine `arc.tension_envelope` is bound to a MusicEngine `texture.density_envelope` and a GameEngine `feel.tuning_envelope` so that all three share the same time-aligned pacing curve.
- **Example:** A boss fight's music intensity, narrative tension, and game difficulty all rise and fall on the same envelope.
- **Why novel:** Cross-engine envelopes are not a primitive in any rival; they require the EnvelopeGene type and Core composition.

### 3. **Genome Mirror**
- **Definition:** Two seeds in different domains *share* a subset of their genes by reference, not value. Mutating the shared subset propagates to both.
- **Example:** A character's `palette.*` is shared between SpriteEngine and UIEngine for that character's HUD, so changing the character's outfit color also updates their UI accent.
- **Why novel:** Most engines have no notion of cross-asset gene sharing; GSPL's content-addressed genes make it natural.

### 4. **Behavior Echo**
- **Definition:** A BehaviorGene from one engine becomes a *constraint* on another engine's BehaviorGene via Core (energy, complexity).
- **Example:** A character with a "cautious" behavior (low energy, high complexity) becomes a music score with a sparse, deliberate texture.
- **Why novel:** Behavior-to-aesthetic translation is usually hand-coded; GSPL makes it a typed inference.

### 5. **Embedding Bridge**
- **Definition:** Two seeds in different domains share an EmbeddingGene anchor and use the embedding as a common steering handle.
- **Example:** Tweaking a "mood embedding" attached to a NarrativeEngine seed automatically updates the bound MusicEngine and Visual2D seeds via their own embeddings interpolated to match.
- **Why novel:** Cross-domain embedding sync is a research topic; GSPL's typed gene system makes it a primitive.

### 6. **Procedural Substrate Reuse**
- **Definition:** A Procedural seed's GridGene is consumed simultaneously by Visual2D (as a texture), Geometry3D (as displacement), and Game (as a level layout), with the same content hash.
- **Example:** A Wang-tile dungeon layout drives the visual look, the playable geometry, *and* the music density envelope (mapped via Core).
- **Why novel:** Same-content multi-domain consumption is what makes "one seed grows everything" tangible.

### 7. **Lineage Steering**
- **Definition:** Breeding operators take *cross-engine* parents and produce a child whose composition tree is a structured blend of both parents' composition trees.
- **Example:** Breeding a CharacterEngine seed with a SoundEngine seed produces a "character with theme music" seed where the music is derived from the character's palette and traits via Core.
- **Why novel:** Cross-domain breeding is meaningless in rival systems; GSPL makes it a typed operator.

### 8. **Constraint Propagation**
- **Definition:** A constraint on one engine (e.g., UIEngine's accessibility floor) propagates to bound engines so they respect it (e.g., the Visual2D background art reduces saturation behind text).
- **Example:** A UI seed's contrast floor causes the Visual2D background it sits on to auto-tone-map.
- **Why novel:** Most rival systems have constraints in one direction (UI overlays art); GSPL makes it bidirectional and typed.

### 9. **Critic Fan-In**
- **Definition:** A critic model trained for one engine's quality metric is applied across other engines via Core projection. A "good music" critic biases the breeding of "good narratives" by projecting both into Core mood space.
- **Example:** A high-rated MusicEngine seed pulls bound NarrativeEngine seeds toward its Core coordinates during evolution.
- **Why novel:** Critic transfer across modalities is a research idea; GSPL's typed Core makes it natural.

### 10. **Symmetry Breaking**
- **Definition:** When a composition collapses to "everything looks the same" the system actively perturbs along sloppy directions of the FIM (Brief 019) to introduce variation that preserves identity.
- **Example:** Breeding a sprite family that has converged to identical poses; the system finds the pose-direction the FIM identifies as sloppy and explores it.
- **Why novel:** No rival has the FIM as a primitive; this pattern depends on it.

### 11. **Co-evolution Arena**
- **Definition:** Two populations from different engines are co-evolved against each other with cross-domain fitness coupling. A POET-style open-ended setup (Brief 038) where Game seeds evolve to be "fun for" character seeds that themselves evolve to be "interesting in" the games.
- **Example:** Characters and the levels they're best in co-adapt over generations.
- **Why novel:** Cross-engine co-evolution requires the typed cross-domain composition story to even make sense as a fitness signal.

### 12. **Recursive Composition**
- **Definition:** A composed seed becomes a parent in a new composition tree. Bounded by the 5-hop chain limit (Brief 016) and the 10-hop royalty cap (Brief 017).
- **Example:** A "cyberpunk warrior" composed from sprite + animation + music + narrative is itself fed back into a FullGame composition as a single named asset.
- **Why novel:** Without content-addressed seeds and typed composition, recursive composition is a maintenance nightmare; with them, it's the natural workflow.

## Risks identified

- **Pattern overload**: 12 named patterns are more than users can remember. Mitigation: surface them as *suggestions* in the studio, not as required vocabulary; the agent uses the vocabulary internally.
- **Naturality drift across long compositions**: each pattern adds a hop; chains stack drift (Brief 016's ε bound). Mitigation: chain cap stays at 5 even when patterns nest.
- **Pattern misuse**: a user applies "Tension Lock" to two engines whose envelopes don't semantically align. Mitigation: pattern definitions include applicability preconditions; the validator rejects misapplications.
- **Cult of patterns**: over-reliance on named patterns crowds out free-form creativity. Mitigation: patterns are *defaults*, not constraints. Users can always compose without naming.

## Recommendation

1. **Adopt the 12 patterns as the normative cross-engine composition vocabulary.** Document in `architecture/composition-patterns.md`.
2. **Each pattern has an entry** with: name, definition, applicable engine pairs, Core gene dependencies, example, anti-example, and validator preconditions.
3. **The agent (Brief 029) uses pattern names internally** when planning multi-engine compositions.
4. **The studio surfaces pattern suggestions** as inline tooltips when the user composes engines that match a pattern's preconditions.
5. **Patterns are versioned**: a pattern can be revised by adding a v2 alongside v1 (no breaking changes).
6. **Reserve pattern IDs 13-32** for Phase 2 inventions.
7. **A conformance test corpus** for each pattern: known inputs with known expected outputs.

## Confidence
**3/5.** As a pure invention proposal, this is unproven. The 3/5 reflects (a) confidence that *some* of these patterns are useful, mixed with (b) honest uncertainty about which will survive contact with real users.

## Spec impact

- `architecture/composition-patterns.md` — new file with the catalog.
- `architecture/cross-domain-composition.md` — reference the pattern catalog.
- `algorithms/pattern-applicability.md` — applicability check pseudocode.
- `tests/composition-pattern-conformance.md` — corpus.
- New ADR: `adr/00NN-cross-engine-pattern-catalog.md`.

## Open follow-ups

- Prototype the top three patterns (Palette Inheritance, Tension Lock, Genome Mirror) in the studio for Phase 1.
- Decide which patterns are auto-applied by the agent vs user-opt-in.
- Empirically measure which patterns users adopt vs ignore in Phase 2 and prune the catalog accordingly.
- Investigate whether co-evolution arena (Pattern 11) is feasible at v1 compute budgets.

## Sources

- Stanley & Lehman, *Why Greatness Cannot Be Planned* (open-ended co-evolution).
- Bartosz Milewski, *Category Theory for Programmers* (composition as a first-class concept).
- Internal: Briefs 013, 016, 019, 020, 021-027, 038.
