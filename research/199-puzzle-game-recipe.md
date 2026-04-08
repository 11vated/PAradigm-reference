# 199 — Puzzle game genre recipe

## Question
What is the typed genre composition recipe that produces a complete signed puzzle game gseed bundle (match-3 / Sokoban / sliding-tile / physics-puzzle classes) from substrate primitives, with deterministic state, undo/redo, and level-progression structure?

## Why it matters (blast radius)
Puzzle games are mobile's dominant genre and the canonical proving ground for deterministic state and undo/redo. A working recipe demonstrates the substrate's determinism story (Brief 020) holds end-to-end through a creator-instantiable artifact, not just kernel claims.

## What we know from the spec
- Brief 020 — determinism contract.
- Brief 158 — save snapshot model.
- Brief 159 — state machines.
- Brief 173 — tilemap autotile.
- Briefs 197-198 — recipe template precedent.

## Findings
1. **Recipe inherits Brief 197 frame.**
2. **Required primitives.** `tilemap.layer` (puzzle grid), `physics.body` (optional, for physics-puzzles), `input.action`, `audio.bus`, `vfx.system` (match flash, fall trail), `ui.element` (move counter, score, level select), `state.machine` (game-state FSM), `level.scene` (one per puzzle level), `save.snapshot` (per-level state + progression).
3. **Deterministic state requirement.** Validation contract gates that the puzzle's game state lives in typed substrate gseeds (no opaque blobs); Brief 020's determinism contract applies, enabling perfect undo/redo and replay.
4. **Undo/redo as inverse mutations.** Each puzzle move is a typed mutation; undo is the inverse mutation popped from a typed undo stack. Stack lives in the playthrough gseed and persists in `save.snapshot`. Stack depth is a typed parameter (default 50, unlimited for Sokoban).
5. **Game-state FSM canonical states.** Idle → Input → Resolving → Win-check → Idle, with Win → LevelComplete and Lose → GameOver branches.
6. **Sub-recipe: match-3.** Grid + colored tile types + match-detection rule + cascade resolution + special-tile rules. Detection runs on Idle→Resolving transition; cascades repeat until no matches.
7. **Sub-recipe: Sokoban.** Grid + walls + boxes + targets + push rule + win-condition (all targets covered). Move = typed `entity.move` mutation; push = chained mutation; undo = inverse stack pop.
8. **Sub-recipe: sliding-tile.** Grid + numbered tiles + empty cell + slide rule + win-condition (sorted order). Pure tile-swap mutations.
9. **Sub-recipe: physics-puzzle.** Brief 156 2D physics + creator-placed objects + win-condition (typed `physics.body` reaches typed region). Determinism via substrate physics kernel.
10. **Level format.** Each puzzle level is a `level.scene` gseed with creator-authored layout. Levels group into `progression.curve` packs unlocked by completion.
11. **Validation contract.** Sign-time gates: deterministic state requirement (no opaque blobs in playthrough gseed), at least one win-condition rule, undo stack present, at least one level scene.
12. **No-time-pressure default.** Puzzle recipe defaults are turn-based / no real-time; sub-recipes can opt into timer-based gameplay via a typed `time.budget` field.

## Risks identified
- **Undo stack memory.** Long undo stacks blow memory. Mitigation: stack depth is typed and capped per-recipe; older entries serialize to save.snapshot's tail chunk.
- **Cascade complexity.** Match-3 cascades can chain unboundedly. Mitigation: cascade depth is typed-capped; deeper cascades surface a warning.
- **Physics determinism.** Physics-puzzles depend on Brief 020's deterministic kernel being substrate-provided per engine. Mitigation: validator gates that physics-puzzle sub-recipe requires the substrate kernel, not the engine's native physics.
- **Level-authoring overhead.** Creators may not author 50+ puzzle levels. Mitigation: sub-recipes ship 10-level starter packs from procedural generators where applicable (Sokoban via Brief 175 procgen).

## Recommendation
Specify the puzzle game recipe as a `recipe.gseed` with deterministic-state validation, typed undo/redo via inverse mutations, four sub-recipes (match-3 / Sokoban / sliding-tile / physics-puzzle), and a canonical game-state FSM. Default instantiation produces a 10-level playable puzzle game.

## Confidence
**4.5 / 5.** Puzzle mechanics are simple and well-precedented. The novelty is undo/redo via typed inverse mutations on the substrate. Lower than 5 because cascade-depth caps and physics-puzzle determinism need Phase-1 validation.

## Spec impact
- New spec section: **Puzzle game genre recipe specification**.
- Adds typed `mutation.inverse` contract enabling undo/redo as substrate primitive.
- Adds four sub-recipes.
- Cross-references Briefs 020, 158, 197.

## New inventions
- **INV-829** — Typed inverse-mutation contract enabling perfect undo/redo as a substrate primitive: every typed mutation declares its inverse, and the playthrough gseed maintains a typed stack of applied/inverse pairs.
- **INV-830** — Deterministic-state validation gate for puzzle recipes: opaque-blob playthrough state is rejected at sign-time, enforcing Brief 020 determinism end-to-end through the creator-facing surface.
- **INV-831** — Cascade-depth typed cap with substrate-warning surfacing: match-3 cascades have a structural ceiling visible to creators rather than a silent runtime hang.
- **INV-832** — Procgen-seeded starter level packs for sub-recipes: Sokoban / sliding-tile starter levels ship as procgen-generated signed gseeds, eliminating creator level-authoring overhead at instantiation.
- **INV-833** — Time-budget opt-in field for puzzle recipes: real-time pressure is structurally optional, defaulting to turn-based.

## Open follow-ups
- Procedural Sokoban generator integration with Brief 175 — Phase 1.
- Multiplayer puzzle (e.g., Tetris versus) — deferred to v0.4 with Brief 209.
- Match-3 cascade visual polish parameters — deferred to v0.2.
- Physics-puzzle determinism validation across all eight engines — covered by Brief 196 parity suite.

## Sources
1. Brief 020 — Determinism contract.
2. Brief 156 — Physics integration.
3. Brief 158 — Save snapshot model.
4. Brief 173 — Tilemap autotile.
5. Brief 175 — Procgen.
6. Brief 197 — 2D platformer recipe.
7. "Designing the Sokoban Solver" — academic puzzle literature.
8. Bejeweled / Candy Crush match-3 design analyses.
