# 016 — Cross-domain composition: functor laws, naturality, the category of seeds

## Question
What does it mean, *formally*, for a sprite seed to "become" a music seed or a game seed, and what laws must the cross-domain composition machinery satisfy so that compositions are consistent, associative, and reproducible?

## Why it matters
The "one seed, many domains" promise is the most distinctive thing about Paradigm. If composition is ad-hoc string-matching between engines, the system becomes a swamp of one-off converters that no agent can reason about. If composition is formalized as functors between categories of seeds, every cross-domain bridge inherits algebraic guarantees for free.

## What we know from the spec
- `architecture/cross-domain-composition.md` proposes category theory as the formal framework.
- The 17 gene types (Brief 013) are the morphism alphabet.
- The 26 engines (Tier B briefs) are the objects of the category.

## Findings

**The category `Seed`:**

- **Objects**: domain-typed seed schemas. Each domain (sprite, music, narrative, ...) is an object.
- **Morphisms**: typed coercions between seed schemas — functions `Seed_A → Seed_B` that are total, deterministic, and commute with mutation in a controlled way.
- **Identity**: each schema has the trivial identity coercion.
- **Composition**: morphisms compose. `f: A→B` and `g: B→C` give `g∘f: A→C`.

**The category satisfies (or must be made to satisfy):**

1. **Associativity**: `(h∘g)∘f = h∘(g∘f)` for any composable triple. Required for reproducible chains.
2. **Identity laws**: `id_B ∘ f = f = f ∘ id_A`.
3. **Determinism**: each morphism is a pure function of its input plus a small per-morphism RNG seed (derived from the composition path).

**Functors between categories:**

- A *domain bridge* is a functor `F: Seed_A → Seed_B` that maps not just objects but the *operators* on objects (mutation, crossover, distance) so that:
  - `F(mutate(s)) ≈ mutate(F(s))` up to a controlled drift
  - `F(crossover(s₁, s₂)) ≈ crossover(F(s₁), F(s₂))`
- This is the *naturality square*: bridges must commute with operators "as much as possible." Perfect naturality is not always achievable (a sprite has color genes a music seed doesn't), but the bridge must be honest about which operators it preserves and which it drops.

**The shared core trick:**

- Define a small *core schema* `Core` (e.g., emotional valence, complexity, energy, palette) that every domain extends.
- Cross-domain bridges factor through `Core`: `Sprite → Core → Music`. This makes bridges N+M instead of N×M.
- The core gene set is small (≤ 8 genes) and stable across all domains.

**Lineage compatibility:**

- A child seed produced by composition records its parent seed IDs *and* the composition path used. This lets a verifier replay the composition and check that the result matches.

## Risks identified

- **Bridges that "almost" commute** (the naturality square is not exact) silently produce drift over long chains. Solution: cap composition chain length and require commutativity tests.
- **Lossy bridges**: dropping a gene in `F(s)` is sometimes unavoidable but must be logged in metadata.
- **Composition explosion**: 26 domains × 26 → 676 potential pairwise bridges. The factor-through-Core trick reduces this to 52 bridges (26 to Core, 26 from Core).
- **Naturality only "up to ε"** is fine for evolutionary use but breaks any literal-equality test. Tests must use the right notion of equivalence per gene type.

## Recommendation

1. **Adopt the category-theoretic framing as normative.** `architecture/cross-domain-composition.md` is rewritten to use category and functor language explicitly with worked examples.
2. **Define the `Core` schema in `spec/01-universal-seed.md`.** Eight core genes: valence, energy, complexity, palette (ColorGene[3]), tempo, density, structure, theme.
3. **Every engine ships two functors**: `to_core: Engine → Core` and `from_core: Core → Engine`. Cross-domain composition uses these as the only bridge.
4. **Naturality conformance suite**: for each engine pair, verify `to_core ∘ from_core ≈ id_Core` and the operator-commutativity squares within ε.
5. **Composition path is recorded in lineage metadata** for every composed seed. Verifiers can replay.
6. **Composition chains capped at 5 hops** at v1 to bound drift; revisable when measured.
7. **A composed seed is a first-class seed** — it has its own ID, hash, signature, and lineage row.

## Confidence
**4/5.** Category theory as a formalism for compositional systems is well-established (Conal Elliott, Bartosz Milewski, Brendan Fong & David Spivak). The specific application to creative-asset composition is novel; the 4/5 reflects the empirical work needed to validate that real-world bridges satisfy naturality within an acceptable ε.

## Spec impact

- `architecture/cross-domain-composition.md` — full rewrite with the formalism.
- `spec/01-universal-seed.md` — add the Core schema.
- `algorithms/functor-composition.md` — pseudocode for `to_core`, `from_core`, and the chain runner.
- `tests/composition-laws.md` — naturality and associativity tests.
- New ADR: `adr/00NN-category-of-seeds.md`.

## Open follow-ups

- Empirically measure naturality drift on real bridges. Phase 1 task.
- Decide on the exact 8 core genes (the proposal above is provisional).
- Consider whether to allow direct (non-Core) bridges as an optimization for hot pairs (e.g., Character → Sprite).
- Investigate higher-category structures (2-functors) for composition of compositions.

## Sources

- Fong & Spivak, *Seven Sketches in Compositionality* (applied category theory).
- Milewski, *Category Theory for Programmers*.
- Internal: `architecture/cross-domain-composition.md`, Brief 013.
