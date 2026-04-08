# 207 — Voxel and sandbox genre recipe

## Question
What is the typed genre composition recipe that produces a complete signed voxel sandbox gseed bundle (Minecraft / Terraria / Dwarf Fortress class) from substrate primitives, with chunk-based world streaming, place/break mutations, persistent worlds, and crafting?

## Why it matters (blast radius)
Voxel sandboxes are the highest-revenue indie genre per unit (Minecraft: $4B+) and the canonical proving ground for chunk-streamed worlds and player-as-modifier-of-world. They are also the most demanding test of Brief 158 save snapshot's chunked save model — without that primitive working, this genre is impossible.

## What we know from the spec
- Brief 158 — save snapshot model (chunked saves).
- Brief 175 — procgen (terrain).
- Brief 156 — physics integration.
- Brief 173 — tilemap (2D variant).
- Brief 205 — sim recipe (economy flow precedent).
- Briefs 197-206 — recipe template precedent.

## Findings
1. **Recipe inherits frame.**
2. **Required primitives.** `world.chunk` (typed 3D voxel chunk; or 2D for Terraria-class), `voxel.def` / `tile.def` (typed block library), `entity.archetype` (player + mobs), `inventory.container`, `item.def`, `economy.flow` (crafting recipes from Brief 205), `behavior.tree` (mob AI), `procgen.terrain` (Brief 175), `physics.body` (3D), `character.controller` (Brief 206), `camera.rig`, `audio.bus`, `vfx.system`, `save.snapshot` (heavy chunked use), `ui.element` (hotbar / inventory / crafting menu).
3. **Chunk-based world.** `world.chunk` declares: chunk size (default 16×16×16 voxels for 3D; 16×64 for Terraria-style 2D), voxel data (typed dense array), generation seed reference, modification timestamp. Chunks load/unload around the player; only modified chunks save to `save.snapshot`.
4. **Place/break as typed mutations.** Player actions emit typed `voxel.place` and `voxel.break` mutations. Each mutation references chunk coords + voxel type. Mutations append to lineage; world state is reproducible by replaying the procgen seed + mutation log (canonical voxel-game pattern).
5. **Procgen terrain.** `procgen.terrain` uses Brief 175 noise + biome systems. Terrain seed is a `seed.record` typed gseed (Brief 162). All chunks generate deterministically from the seed, modified only by player mutations.
6. **Crafting.** `economy.flow` from Brief 205 is reused: typed input items + processing → output items. Recipes declarable as creator gseeds. Sub-recipes (Minecraft / Terraria) ship default recipe books.
7. **Mob AI.** Default mobs use Brief 159 BTs with wander → spot → chase → attack patterns. Hostile mobs spawn under typed conditions (darkness, biome, depth).
8. **Sub-recipes.** Minecraft-class (3D voxel + survival + crafting + creative mode), Terraria-class (2D tile-based + exploration + bosses), Dwarf-Fortress-class (top-down management overlay; layered with Brief 205), Creative-mode-only (no survival, just building).
9. **Save model.** `save.snapshot` chunks are spatial regions of voxel chunks. Unmodified chunks save zero bytes (procgen reproduces them). Modified chunks save the full chunk + metadata. Save grows linearly with player modification, not world size — critical.
10. **Validation contract.** Sign-time gates: `world.chunk` schema declared, `voxel.def` library non-empty, `seed.record` for terrain present, save chunking declared, at least one default mutation kind (place + break minimum).

## Risks identified
- **Chunk streaming cost.** Loading/unloading chunks at runtime is performance-critical. Mitigation: substrate provides typed chunk LOD and view distance parameters; engine-side optimizations are creator-tunable.
- **Save bloat from heavy modification.** Players who modify millions of voxels balloon saves. Mitigation: per-chunk RLE compression in save; warning when save exceeds typed threshold.
- **Cross-engine parity.** Voxel rendering differs sharply across engines. Mitigation: voxel meshing is substrate-provided (greedy meshing algorithm shipped as runtime module); engines render the resulting mesh, not the voxel data directly.
- **Procgen determinism.** Terrain generation must be bit-identical across engines or saves break. Mitigation: substrate procgen runs in pure-substrate code, not engine native; Brief 196 parity suite validates.

## Recommendation
Specify the voxel sandbox recipe as a `recipe.gseed` with typed `world.chunk`, `voxel.def`, `voxel.place` / `voxel.break` mutation primitives, substrate-provided greedy meshing, procgen terrain via Brief 175, crafting via reused Brief 205 `economy.flow`, four sub-recipes, and zero-byte save for unmodified chunks. Default sub-recipe (Minecraft-class) produces a playable voxel sandbox.

## Confidence
**4 / 5.** Voxel mechanics are well-precedented; the novelty is the substrate-provided greedy meshing for cross-engine parity and the zero-byte unmodified-chunk save. Lower than 4.5 because chunk streaming performance and save bloat need Phase-1 measurement at scale.

## Spec impact
- New spec section: **Voxel and sandbox genre recipe specification**.
- Adds typed `world.chunk`, `voxel.def`, `voxel.place`, `voxel.break` gseed kinds.
- Adds substrate greedy meshing as runtime-provided primitive.
- Adds the zero-byte unmodified-chunk save contract.
- Cross-references Briefs 156, 158, 162, 175, 197, 205, 206.

## New inventions
- **INV-869** — Typed `world.chunk` primitive with declared chunk size and voxel data array: voxel worlds are first-class typed gseeds, not opaque save blobs.
- **INV-870** — Typed `voxel.place` / `voxel.break` mutation primitives appending to lineage: world modification is a structured mutation log replayable from terrain seed.
- **INV-871** — Substrate-provided greedy meshing runtime module for cross-engine voxel rendering parity: meshing is substrate code; engines render the substrate-produced mesh.
- **INV-872** — Zero-byte save for unmodified chunks via procgen reproducibility: save size grows with player modification, not world size — a structural guarantee.
- **INV-873** — Reused `economy.flow` from Brief 205 for voxel crafting: crafting is not a new primitive, it's the sim economy primitive applied to voxel inventories.

## Open follow-ups
- Multiplayer voxel sandbox (Minecraft co-op) — deferred to v0.3 with Brief 209.
- Cross-engine voxel rendering parity validation — Phase 1 with Brief 196 parity suite.
- Chunk streaming over network — deferred to v0.4.
- 3D path-finding through voxel terrain — deferred to v0.3.

## Sources
1. Brief 158 — Save snapshot model.
2. Brief 162 — VFX with deterministic seeds.
3. Brief 175 — Procgen library.
4. Brief 196 — Cross-engine parity test suite.
5. Brief 197 — 2D platformer recipe.
6. Brief 205 — Simulation recipe.
7. Brief 206 — 3D first-person recipe.
8. Greedy meshing algorithm (0fps.net/2012/06/30/meshing-in-a-minecraft-game/).
9. Minecraft technical analyses (community-documented).
10. Terraria postmortem — Re-Logic.
