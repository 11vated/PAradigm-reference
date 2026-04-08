# 201 — Roguelike / roguelite genre recipe

## Question
What is the typed genre composition recipe that produces a complete signed roguelike or roguelite gseed bundle (traditional ASCII / modern action-roguelite class) from substrate primitives, with procedural generation, permadeath, meta-progression, and run-based seed determinism?

## Why it matters (blast radius)
Roguelikes are the canonical proving ground for procedural generation + replay determinism + meta-progression as a unified loop. A working recipe demonstrates that the substrate's procgen (Brief 175) and seed-as-first-class story (Brief 162) compose into a complete creator-instantiable game.

## What we know from the spec
- Brief 162 — VFX with deterministic seeds.
- Brief 175 — procgen library.
- Brief 158 — save snapshot model.
- Brief 159 — behavior trees.
- Briefs 197-200 — recipe template precedent.

## Findings
1. **Recipe inherits frame.** Same `recipe.gseed` pattern.
2. **Required primitives.** `procgen.dungeon` (Brief 175), `entity.archetype` (player + enemies + items + props), `behavior.tree` (enemy AI), `inventory.container`, `stats.sheet`, `progression.curve` (meta-progression separate from in-run progression), `state.machine`, `level.scene` (one per dungeon level), `save.snapshot` (run state + meta state), `seed.record` (run seed).
3. **Run seed as first-class typed field.** Each run has a `seed.record` typed gseed declaring the master PRNG seed. All procgen, AI decisions, and loot rolls draw from sub-seeds derived from the master via Brief 162's deterministic sub-seeding rule. Daily challenge runs share a date-derived seed.
4. **Meta-progression separation.** `save.snapshot` has two typed regions: `run.state` (cleared on death) and `meta.state` (persisted across runs). Validation contract gates that meta.state cannot reference run.state without an explicit unlock-event mutation.
5. **Permadeath as typed mutation.** On death, the substrate runtime emits a `run.death` typed mutation that clears run.state, applies any meta-progression unlocks, and signs the run's lineage. Lineage is appendable across runs forming a creator's run history.
6. **Procgen dungeon contract.** Recipe imports a `procgen.dungeon` instance with typed parameters: room count, room size range, corridor width, monster density, loot density, theme. All parameters are creator-tunable.
7. **Sub-recipes.** Traditional roguelike (turn-based, ASCII or tile, full Brief 175 procgen), action roguelite (real-time, room-cleared, Hades-class), deck-builder roguelite (Slay the Spire-class with `card.deck` substitution), Brogue-style (turn-based with rich tactics).
8. **Daily challenge mode.** Sub-recipe option enabling date-derived run seeds; all players on the same day get the same dungeon. Creators can verify run integrity via lineage.
9. **Validation contract.** Sign-time gates: `seed.record` present, `procgen.dungeon` present, run.state / meta.state separation, permadeath mutation declared, at least one enemy archetype.
10. **Replay-as-shareable-artifact.** Each completed run produces a signed replay gseed (per Brief 185 playtest harness) that is shareable. Anyone can replay a run from its seed and the substrate produces the bit-identical sequence of events.

## Risks identified
- **Procgen quality variance.** Bad seeds produce unfair runs. Mitigation: typed validity gates in `procgen.dungeon` rejecting unwinnable layouts; reroll until validity holds.
- **Meta-progression balancing.** Meta unlocks can trivialize the game. Mitigation: not the substrate's job; document the design trade-off in the recipe's open follow-ups.
- **Save bloat.** Run history accumulates. Mitigation: typed cap on stored run replays (default 50, creator-tunable); old replays compress to summary form.
- **Daily challenge cheating.** Players can fake completion. Mitigation: lineage signing per Brief 152 makes server-side verification trivial; substrate provides the primitive but server-side verification is not in v0.1 scope.

## Recommendation
Specify the roguelike recipe as a `recipe.gseed` with typed `seed.record` master seed, run.state / meta.state separation in save.snapshot, permadeath as typed mutation, four sub-recipes (traditional / action / deckbuilder / Brogue), daily-challenge mode option, and replay-as-shareable-artifact pattern. Default sub-recipe instantiation produces a playable run-based game.

## Confidence
**4.5 / 5.** Roguelike mechanics are well-precedented; the novelty is the run.state/meta.state typed separation and the daily-challenge seed-as-date pattern. Lower than 5 because procgen validity gates need Phase-1 measurement against real dungeon layouts.

## Spec impact
- New spec section: **Roguelike genre recipe specification**.
- Adds the run.state / meta.state typed separation to `save.snapshot`.
- Adds the typed `run.death` permadeath mutation contract.
- Cross-references Briefs 152, 158, 162, 175, 185, 197.

## New inventions
- **INV-839** — Typed run.state / meta.state separation in save.snapshot with sign-time gating against unsanctioned cross-references: roguelite meta-progression is a structural substrate guarantee, not creator code discipline.
- **INV-840** — Typed `run.death` permadeath mutation with lineage-signed appendable run history: deaths are first-class substrate events, not opaque save-file deletions.
- **INV-841** — Date-derived daily challenge seed pattern with substrate-provided integrity verification: shared-seed daily runs are a substrate-level primitive, not per-game implementation.
- **INV-842** — Typed procgen-validity gates with deterministic reroll: unwinnable layouts are structurally rejected before reaching the player.
- **INV-843** — Replay-as-shareable-artifact pattern: completed runs produce signed replay gseeds shareable for community verification or content creation.

## Open follow-ups
- Server-side daily-challenge verification — deferred to v0.4 with Brief 209.
- Run-summary compression for old replays — Phase 1.
- Deck-builder card primitive (`card.deck`) — Brief 202 covers card games specifically.
- Tactical roguelike (XCOM-class) — covered by Brief 203.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 158 — Save snapshot model.
3. Brief 162 — VFX with deterministic seeds.
4. Brief 175 — Procgen library.
5. Brief 185 — Playtest harness.
6. Brief 197 — 2D platformer recipe.
7. Brogue source code (github.com/tmewett/BrogueCE).
8. Hades GDC postmortem.
9. NetHack design literature.
