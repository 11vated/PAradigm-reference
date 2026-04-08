# 020 — INV: Five new gene types beyond the 17

> **DEFERRED TO PHASE 2.** `spec/02-gene-system.md` v0.1 ships **exactly seventeen** kernel gene types and explicitly forbids additions in v0.1. The five experimental types proposed here (`EmbeddingGene`, `NarrativeGene`, `EnvelopeGene`, `SwarmGene`, `RuleGene`) live in a Phase 2 experimental branch for A/B testing and can enter v0.2 only via a typed GSEP (Brief 230) with migration tooling (Brief 229). The kernel type-id space reserves IDs **18–31** for these and future experimental types so adding them later does not require a major version bump.

## Question
What additional gene types should GSPL invent — beyond the 17 in the v1 catalog — to cover expressive needs that current types cannot reach without ugly workarounds, and what are their formal definitions?

## Why it matters
The 17 types of Brief 013 are the recognizable canon from evolutionary computation literature. To make GSPL *unsurpassable*, the spec must extend the canon with types that reflect domains the canon never studied: latent embeddings, narrative arcs, modulation envelopes, swarms, and rule programs. Each of these is currently being shoehorned into existing types in ways that break operator semantics. Inventing them properly is a competitive moat.

## Why these five (and not others)
The five proposed below are the union of: (a) types implied by existing engines that don't fit cleanly into the 17, (b) types referenced in Tier B engine briefs as needed primitives, and (c) types that have no good prior art in the EC literature but obvious creative-asset value.

## What we are inventing and why

### 1. EmbeddingGene — points in a learned latent space

**Domain:** ℝᵏ where the space is a learned manifold (e.g., a CLIP feature, a VAE latent, a learned style code). Comes with an *anchor model fingerprint* identifying which model's space this point lives in.

**Mutation operator:** Gaussian perturbation in the tangent space of the manifold, with optional projection back to a "natural" subregion via a learned density model. Step size auto-scaled by the local Fisher information (Brief 019).

**Crossover operator:** SLERP along the geodesic between two points. (Linear interpolation in latent space is a known mistake; SLERP preserves norm and is qualitatively better for most learned latents.)

**Distance metric:** Cosine distance with respect to the anchor model.

**Validation invariant:** Point lies within the model's documented operating region (e.g., norm bounds), and the anchor fingerprint resolves to a known model.

**Why we need it:** Several engine briefs (033 concept-to-seed, 034 self-improving agent) need to attach learned embeddings as steerable handles on a seed. Currently they would be encoded as `VectorGene<512>` with no operator awareness of the manifold, which is wrong.

**Risk:** Couples seeds to specific learned models. Mitigation: embed the model fingerprint inside the gene, and require that any verifier wanting to *operate* on the gene have the model available. Verifiers without the model can still load and serialize the gene; they just can't mutate it.

### 2. NarrativeGene — typed story structure

**Domain:** A typed graph of *narrative beats* where nodes are events with role tags (setup, conflict, climax, resolution) and edges are causal or temporal links with optional "tension delta" weights.

**Mutation operator:** Beat insertion / deletion / reordering subject to causal-link preservation. A small grammar enforces "no resolution before conflict" and similar structural constraints.

**Crossover operator:** Subgraph swap, with grafting rules that re-bind dangling causal links to compatible nodes in the host.

**Distance metric:** Tree edit distance over a canonicalized form, weighted by role.

**Validation invariant:** All causal links are acyclic; every "resolution" beat has at least one upstream "conflict" beat; total tension stays within a configured range.

**Why we need it:** The Narrative engine (Brief 023) currently uses `GraphGene` with stringly-typed labels, which loses every interesting operator. Story-shaped operators need type-awareness to avoid producing nonsense.

### 3. EnvelopeGene — time-varying parameter curves

**Domain:** A piecewise function `t → ℝ` (or `t → ℝᵏ`) over a normalized time interval `[0,1]`, parameterized by a small number of control segments (linear, exponential, ADSR, custom Bézier).

**Mutation operator:** Control-point jitter with topology preservation; segment-type swap (e.g., linear → exponential) at low rate.

**Crossover operator:** Time-aligned blending; segment-aware splicing.

**Distance metric:** L² over the realized curve sampled at fixed timesteps.

**Validation invariant:** Endpoints in `[lo, hi]`; total energy bounded; for ADSR variant the four segments are ordered.

**Why we need it:** Music, audio, animation, particle systems, and physics simulations all need time-varying parameters. Currently they're encoded as either `CurveGene` (which is geometric, not temporal) or `SequenceGene` (which loses the continuous-time semantics). EnvelopeGene is the right primitive for "value over time."

### 4. SwarmGene — agent-population specification

**Domain:** A specification of an agent population: count distribution, per-agent role distribution, behavioral parameter distribution, spatial distribution. Not the agents themselves, but the *generative recipe* for them.

**Mutation operator:** Distribution parameter jitter; role-mix shift; population size step.

**Crossover operator:** Mix of distributions (Wasserstein interpolation where defined; convex combination otherwise).

**Distance metric:** Wasserstein over the joint distribution.

**Validation invariant:** Population size in budget; role mix sums to 1; behavioral params per role are valid for that role's behavior schema.

**Why we need it:** Ecosystem, ALife, FullGame, and Physics engines (Briefs 023, 025) all need to spawn populations of agents whose collective properties are evolvable. Encoding each individual agent as a separate gene blows up the seed; encoding them as a `DistributionGene` loses role structure. SwarmGene is the right level of abstraction.

### 5. RuleGene — small executable rule programs

**Domain:** A program in a small, total, deterministic DSL — typically a list of `(precondition, action, weight)` rules or a decision table. Bounded execution: the DSL has no loops, only finite case analysis.

**Mutation operator:** Rule add / remove / swap; precondition perturbation; weight Gaussian; action substitution from a typed action vocabulary.

**Crossover operator:** Rule-set union with conflict resolution by weight; rule reordering preserved where possible.

**Distance metric:** Set edit distance over rules + symmetric difference of precondition coverage.

**Validation invariant:** All preconditions are well-typed; all actions are in the legal vocabulary; total rule count ≤ budget; no two rules with identical preconditions (deduplicated).

**Why we need it:** Game logic, Behavior, Ecosystem, and Procedural engines all need *small programs* as evolvable artifacts. Currently they encode programs as `BehaviorGene` (which is FSM/BT-shaped, not rule-shaped) or `SequenceGene` (which loses typing). RuleGene is the natural type for "what should this thing do under these conditions" that isn't already covered by behavior trees.

## Risks identified

- **Type proliferation**: 22 types is more cognitive load than 17. Mitigation: each new type has at least two engines that need it, and each comes with a complete operator suite at introduction.
- **EmbeddingGene model lock-in** if the anchor model is deprecated. Mitigation: model fingerprints; warning on load if the anchor model isn't available; encouragement to use models with stable releases.
- **NarrativeGene grammar drift**: the structural constraints will need iteration. Mitigation: the grammar is in an external table that can be revised without changing the gene type itself.
- **EnvelopeGene vs CurveGene confusion**: users will ask why both exist. Mitigation: documentation makes it explicit — Curve is geometric, Envelope is temporal.
- **RuleGene becomes a Turing tarpit** if the action vocabulary is too rich. Mitigation: action vocabulary is per-engine and audited; total program execution time bounded.
- **All inventions need empirical validation**. None of these types has prior literature to lean on; they may not survive contact with real engines.

## Recommendation

1. **Adopt all five as gene types 18-22** in `spec/02-gene-system.md`.
2. **Extend Brief 013's table with the five new rows.** Operator suite, distance metric, validation invariant per type.
3. **Each new type ships with a Repair operator** consistent with Brief 013's universal Repair requirement.
4. **EmbeddingGene's anchor model fingerprint** is a 32-byte hash of the model's published weights file. The fingerprint is part of the gene's value.
5. **NarrativeGene's grammar lives in an external table** so it can be revised without a major bump.
6. **Reserve gene type IDs 23-31** for future inventions.
7. **Phase 2 task**: implement and A/B test each new type in at least one engine before any of them is marked normative. Until then they ship as `experimental.*` gene types.
8. **A new ADR per type** in `adr/00NN-gene-type-XX.md`.

## Confidence
**3/5.** As an invention proposal, this is necessarily lower confidence than research briefs. EmbeddingGene and EnvelopeGene are 4/5 (clear precedent in adjacent fields); NarrativeGene, SwarmGene, and RuleGene are 3/5 (structurally sound but unvalidated in our context).

## Spec impact

- `spec/02-gene-system.md` — five new rows in the catalog, reserve IDs 23-31.
- `algorithms/gene-types/embedding.md`, `narrative.md`, `envelope.md`, `swarm.md`, `rule.md` — five new operator-spec files.
- `tests/gene-type-conformance.md` — five new test sections.
- New ADRs: `adr/00NN-gene-type-18-embedding.md` through `adr/00NN-gene-type-22-rule.md`.

## Open follow-ups

- Prototype each new type in its strongest engine (Embedding→Visual2D, Narrative→Narrative, Envelope→Music, Swarm→Ecosystem, Rule→Game).
- Decide whether `experimental.*` gene types are visible in the studio at all in v1.
- Explore whether NarrativeGene wants its own dedicated breeding operator for "story-aware" recombination beyond the generic crossover.
- Decide on serialization formats per type (binary + JCS) before promoting to normative.

## Sources

- Stanley & Lehman, *Why Greatness Cannot Be Planned* (open-ended evolution intuitions).
- Karras et al., *StyleGAN3* (latent space geometry).
- Propp, *Morphology of the Folktale* (narrative beat decomposition).
- Reynolds, *Flocks, Herds, and Schools* (agent population specification).
- Internal: Brief 013, Briefs 023, 025, 033, 034.
