# 023 — Interactive family: Narrative + Game + FullGame engines

## Question
What are the seed schemas, kernel pipelines, and composition rules for the three engines that produce *interactive* artifacts: NarrativeEngine (story structure), GameEngine (single-mechanic games), and FullGameEngine (complete playable products)?

## Why it matters
Interactive content is the highest-value asset class in the creator economy and the one no rival can produce from a single seed. Sora makes video; Midjourney makes images; Suno makes music; *no one* generates a complete playable game from a structured prompt with proof-bearing reproducibility. The three interactive engines are GSPL's most ambitious bet and the place where the gene-based composition story has to deliver.

## What we know from the spec
- `engines/narrative.md`, `engines/game.md`, `engines/fullgame.md` exist as stubs.
- The 17 + 5 gene types now include NarrativeGene, RuleGene, BehaviorGene, GraphGene, and SwarmGene — the building blocks of interactive content.
- The existing 182K-LOC codebase has the GameEngine prototype furthest along.

## Findings

### NarrativeEngine

Produces *story structure*: characters in roles, plot beats, tension arcs, dialogue scaffolds. Does not produce prose or media; downstream engines do that.

**Genes (typical 20-50):**
- `theme.embedding` (EmbeddingGene anchored to a story-theme model)
- `theme.tags` (CategoricalGene over a vocabulary of tropes)
- `cast.size` (IntGene)
- `cast.roles` (SwarmGene over the role taxonomy: protagonist, antagonist, mentor, ally, foil, …)
- `arc.shape` (NarrativeGene — the typed beat graph from Brief 020)
- `arc.tension_envelope` (EnvelopeGene over normalized story duration)
- `setting.world_rules` (RuleGene defining what is and isn't possible in this story's world)
- `pacing.scene_density` (ScalarGene per act)
- `dialogue.register` (CategoricalGene: formal, casual, period, alien)
- `dialogue.embedding` (EmbeddingGene)
- Plus the 8 Core genes.

**IR**: a typed scene graph with characters, beats, and dependencies. Proof-bearing.

### GameEngine

Produces a *single-mechanic playable*: one rule set, one win condition, one loop. The GameEngine is the simpler sibling of FullGame and the canonical demo for the GSPL → playable pipeline.

**Genes (typical 25-50):**
- `mechanic.family` (CategoricalGene: dodge, collect, shoot, build, sort, match, stealth, puzzle, race, …)
- `mechanic.rules` (RuleGene defining state transitions)
- `mechanic.parameters` (per-rule ScalarGene/IntGene blob — hp, damage, speed, …)
- `win_condition` (RuleGene)
- `loss_condition` (RuleGene)
- `world.size` (VectorGene<2 or 3>)
- `world.tile_grid` (GridGene if grid-based)
- `entities.spawn` (SwarmGene over entity types)
- `entities.behavior` (BehaviorGene per entity type)
- `controls.scheme` (CategoricalGene: keyboard, gamepad, mouse, touch)
- `feel.tuning_envelope` (EnvelopeGene for difficulty ramp over a session)
- `juice.particle_density` (ScalarGene)
- `juice.screenshake` (ScalarGene)
- Plus the 8 Core genes.

**IR**: a deterministic game state machine + spawn table + rule list. Proof-bearing.

### FullGameEngine

Produces a *complete playable game*: a structured composition of GameEngine mechanics + NarrativeEngine arc + assets from sprite/animation/music/audio engines. This is the engine that demonstrates GSPL's "one seed, full product" claim.

**Genes (typical 80-200):**
- `genre` (CategoricalGene)
- `loop.composition` (GraphGene of GameEngine seeds composed into a meta-loop, e.g., town → dungeon → boss → town)
- `progression.system` (RuleGene for XP, unlocks, currency)
- `narrative.binding` (reference to a NarrativeEngine seed)
- `world.layout` (GraphGene of GameEngine instances tied to story locations)
- `meta.economy` (RuleGene)
- `meta.tutorial_arc` (NarrativeGene, smaller subset)
- `assets.character_seeds` (SequenceGene<seed_ref>)
- `assets.music_seeds` (SequenceGene<seed_ref>)
- `assets.audio_seeds` (SequenceGene<seed_ref>)
- Plus the 8 Core genes.

**IR**: a typed composition tree where every leaf is a sub-engine seed and every internal node is a composition operator. Proof-bearing.

## Composition rules

- `Game ⊂ FullGame`: a FullGame seed contains references to multiple GameEngine seeds. Breeding a FullGame can re-bind any contained Game seed without re-breeding it (the references are content hashes), enabling cheap remixes.
- `Narrative ↔ FullGame`: bidirectional binding via Core. Narrative tension envelope drives FullGame difficulty envelope; FullGame composition feeds back into Narrative pacing.
- `Game ↔ Narrative`: a single-mechanic Game can host a "scene" of a Narrative arc; bound by Core (energy, tension).
- `FullGame ⊃ Sprite, Animation, Music, Audio`: the asset references in a FullGame seed are content-addressed; mutating any asset in isolation produces a new FullGame seed without re-breeding the structure.

## Pipeline

Each engine: Seed → IR → Runtime spec → Export.

- **NarrativeEngine** exports to a structured JSON the studio reads, plus optional Twine/Ink/Yarn export.
- **GameEngine** exports to runtime specs that can be consumed by GSPL's reference player (a small HTML5/canvas runtime) and to Godot/Unity/Phaser projects via the existing exporter.
- **FullGameEngine** exports to a project bundle: runtime spec + asset bundle + lineage manifest. The bundle is itself signable and verifiable.

## Risks identified

- **FullGameEngine ambition vs feasibility**: producing a *complete*, *playable*, *good* game from a seed is the hardest thing GSPL is attempting. v1 must scope FullGame to small genres (arcade, roguelike, puzzle) before attempting RPG or narrative-adventure scopes.
- **Composition explosion**: a FullGame is a tree of seeds, each with its own breeding history. Naive evolution explodes. Mitigation: evolution operates on the FullGame seed *structure* by default, with sub-engine breeding as opt-in.
- **Runtime spec format drift**: the GameEngine runtime spec is itself a versioned format. It must follow the same versioning discipline as the seed format (Brief 018).
- **Game balance is not in the genome**: balance is emergent from rule interactions. Mitigation: balance is an *evaluation* concern (critic models, RL preferences — Brief 040), not a gene.
- **Asset binding stale**: a FullGame references a sprite seed that has been evolved further; the FullGame still references the old hash. This is a feature, not a bug — it preserves reproducibility — but the studio needs UI to surface "an asset has newer versions."

## Recommendation

1. **Adopt the three-engine schemas as drafted.**
2. **Phase the FullGameEngine v1 to small genres**: arcade, roguelike, puzzle, match-3, platformer. RPG and narrative-adventure are Phase 3.
3. **Composition tree is normative**: every FullGame seed is a tree of sub-engine references plus operators.
4. **Runtime spec is its own versioned artifact**, governed by Brief 018's discipline.
5. **Asset references are content hashes**, never mutable pointers.
6. **Game balance lives outside the seed** in the evaluation/critic layer.
7. **Reference player** is part of v1: a small HTML5 runtime that can play any GameEngine seed for testing and demo.

## Confidence
**3/5.** NarrativeEngine and GameEngine are 4/5 confidence — the schemas are extensions of well-understood structures. FullGameEngine is 2/5 — it is the most ambitious engine and the one most likely to require iteration. The 3/5 averages these.

## Spec impact

- `engines/narrative.md`, `engines/game.md`, `engines/fullgame.md` — full schemas.
- `algorithms/composition-tree.md` — FullGame's composition operator catalog.
- `runtime/reference-player.md` — the HTML5 reference player spec.
- `tests/interactive-conformance.md` — playable test corpus.
- New ADR: `adr/00NN-fullgame-composition-tree.md`.

## Open follow-ups

- Pin the v1 FullGame genre list and freeze it for Phase 1.
- Build the reference player. Phase 1 task.
- Decide on the runtime spec format (likely a small JCS/binary hybrid like the .gseed format itself).
- Define the asset-staleness UX in the studio (Phase 2).
- Investigate whether GameEngine can borrow from the existing GameEngine prototype in the 182K-LOC codebase.

## Sources

- *Designing Games* (Tynan Sylvester) — single-mechanic loop framing.
- Picbreeder, EndlessForms (interactive evolution of game-like artifacts).
- Internal: Briefs 016 (composition), 020 (Narrative/Rule/Swarm gene types), 040 (refinement loop).
