# 021 — Humanoid family: Character + Sprite + Animation engines

## Question
What is the seed schema, gene composition, kernel pipeline, and cross-engine binding for the three engines that produce humanoid characters: Character (identity & traits), Sprite (rendered 2D form), and Animation (motion)?

## Why it matters
Humanoid characters are the most-requested asset class across every creator platform GSPL is positioned against. The existing Sprite Forge codebase (35K+ LOC) is GSPL's deepest in-house asset; getting the seed schemas right here unlocks reuse and proves the cross-engine composition story on familiar territory.

## What we know from the spec
- `engines/character.md`, `engines/sprite.md`, `engines/animation.md` exist as stubs.
- Sprite Forge ships a 19-stage text-to-sprite pipeline with OKLab color, IK solvers, Verlet physics, multi-engine export.
- Brief 016 introduced the Core schema (8 genes) as the cross-engine bridge.

## Findings — schemas

### CharacterEngine

The CharacterEngine produces a *domain-agnostic identity*: the persona, body proportions, traits, palette, and behavioral inclinations of a character. It does not render anything itself; downstream engines (Sprite, Animation, Narrative, Game) consume its seed.

**Genes (typical count: 24-40):**
- `identity.archetype` (CategoricalGene over a small archetype taxonomy: warrior, mage, scout, healer, beast, …)
- `identity.alignment` (VectorGene<2> over a 2D alignment plane)
- `body.proportions` (VectorGene<8>: head, torso, arms, legs, hands, feet, neck, hip ratios)
- `body.build` (ScalarGene: skinny ↔ heavy)
- `body.height` (ScalarGene)
- `palette.skin`, `palette.hair`, `palette.eye`, `palette.primary`, `palette.secondary`, `palette.accent` (six ColorGenes in OKLab)
- `traits.physical` (RuleGene over physical trait actions, e.g., "is winged → wing pair")
- `traits.behavioral` (RuleGene over behavioral preconditions)
- `voice.timbre` (ScalarGene), `voice.pitch_range` (VectorGene<2>)
- `narrative.embedding` (EmbeddingGene anchored to a published character-embedding model)
- Plus the 8 Core genes for cross-engine bridges (Brief 016).

### SpriteEngine

The SpriteEngine consumes a CharacterEngine seed and produces a 2D sprite atlas. This engine is where Sprite Forge's existing pipeline lives.

**Additional genes (specific to rendering):**
- `style.family` (CategoricalGene: pixel_art, anime, chibi, modern_2d, realistic, cartoon, isometric, hand_drawn, retro)
- `style.line_weight`, `style.shadow_strength`, `style.outline_color` (Scalar/Color)
- `pose.rest` (AffineGene per joint, an array — could be `SequenceGene<AffineGene>`)
- `silhouette.shapes` (PolygonGene array for shape-language design)
- `material.skin`, `material.cloth`, `material.metal`, `material.hair` (MaterialGene per layer)
- `accessories` (GraphGene of attached items with attachment-point references)
- `composition.atlas_layout` (CategoricalGene: 4x4, 8x8, packed, custom)

### AnimationEngine

The AnimationEngine consumes a CharacterEngine seed *and* a SpriteEngine seed, and produces motion data.

**Additional genes:**
- `gait.style` (CategoricalGene: bipedal_normal, bipedal_heavy, bipedal_light, quadruped, custom)
- `motion.idle.envelope` (EnvelopeGene per joint over a normalized loop)
- `motion.walk.envelope` (EnvelopeGene)
- `motion.attack.envelope` (EnvelopeGene)
- `physics.cape_stiffness`, `physics.hair_stiffness` (ScalarGene)
- `physics.gravity_scale` (ScalarGene)
- `behavior.fsm` (BehaviorGene)
- `timing.fps` (IntGene)
- `loop.lengths` (VectorGene<N> in frames per animation type)

## Cross-engine bindings

- `Sprite ← Character`: a SpriteEngine seed embeds a `parent_character` reference (content hash). At evolution time, breeding the sprite without breeding the character is allowed; breeding the character forces a re-bind via the `to_core / from_core` functor pair (Brief 016).
- `Animation ← (Character, Sprite)`: an AnimationEngine seed embeds two parent references. Re-binding when either parent mutates is automatic via Core; warnings are emitted when the re-bind crosses an ε threshold (Brief 016).
- All three engines share the 8 Core genes for cross-domain composition with non-humanoid engines.

## Pipeline architecture

Each engine implements three stages:

1. **Seed → IR**: deterministic seed expansion into an intermediate representation. No rendering. Stage is the proof-bearing stage; hashes are computed here.
2. **IR → Output**: rasterization / animation baking / atlas packing. Non-deterministic across hardware is acceptable here as long as the proof is on the IR.
3. **Output → Export**: format-specific writers (Godot/Unity/Unreal/Phaser/etc.).

The split lets cross-vendor reproducibility live in stage 1 (Brief 001), while stage 2 takes advantage of GPU acceleration freely.

## Risks identified

- **Sprite Forge integration cost**: 35K LOC is real, and adapting it to the 17+5 gene type system requires schema mapping work. Mitigation: phased adoption — keep the existing pipeline functional, build the GSPL-typed front-end as a translation layer first.
- **CharacterEngine ambition creep**: it's tempting to put everything (combat stats, inventory, dialogue tree) into the character seed. Resist — character is identity + body + traits, not gameplay state.
- **Animation EnvelopeGene explosion**: a fully-articulated character has 30+ joints × 8+ animations × N curve segments. Mitigation: hierarchical envelopes (root → joint → channel) and per-joint default curves with override.
- **Cross-engine ε drift**: SpriteEngine producing slightly different output for "the same" character after CharacterEngine mutation. Mitigation: the Core projection is the only allowed bridge; fail loudly if drift exceeds budget.

## Recommendation

1. **Adopt the three-engine schemas as drafted.** Document in `engines/character.md`, `engines/sprite.md`, `engines/animation.md`.
2. **Two-phase Sprite Forge adoption**: Phase A keeps the existing pipeline behind a translation layer; Phase B reimplements with the typed gene system as the source of truth.
3. **All three engines implement the Seed → IR → Output → Export staging** with proofs on IR.
4. **CharacterEngine is the canonical example** for the cross-engine functor laws (Brief 016) — its `to_core` is the simplest and most-tested bridge.
5. **Animation envelopes are hierarchical** by default to avoid gene explosion.
6. **Explicit binding records** (parent content hashes embedded in child seeds) are enforced by the validator.

## Confidence
**4/5.** The schemas closely follow Sprite Forge's existing decomposition, which has been battle-tested at 35K LOC. The 4/5 reflects unmeasured questions about exact gene counts and EnvelopeGene practicality.

## Spec impact

- `engines/character.md`, `engines/sprite.md`, `engines/animation.md` — full schemas.
- `tests/humanoid-family-conformance.md` — interop tests.
- `algorithms/character-to-core.md`, `sprite-to-core.md`, `animation-to-core.md` — functor implementations.
- New ADR: `adr/00NN-humanoid-family-schema.md`.

## Open follow-ups

- Pin exact gene counts after measuring against Sprite Forge's existing parameter space.
- Decide whether AnimationEngine's BehaviorGene is shared with the Game engine or separate.
- Build the translation layer between Sprite Forge's current schema and the typed system. Phase 1.

## Sources

- Sprite Forge codebase (`Sprite_forge_system/`).
- Internal: Brief 013 (gene types), Brief 016 (composition), Brief 020 (new gene types).
