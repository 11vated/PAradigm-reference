# 158 — Save/load and serialization

## Question

How does GSPL equip the universal save/load surface — full-game save, partial save, autosave, cloud-sync, save lineage, save migration across content updates — as a substrate primitive where the save file *is* a signed gseed and rolling back to any prior save costs nothing extra?

## Why it matters (blast radius)

Save/load is the most-tested, most-bug-prone surface in any non-trivial game: corruption, migration breaks, cloud-sync conflicts, anti-cheat exploits, version drift between client and save. Every game engine reinvents the wheel and ships shaky implementations that creators patch at 2am. GSPL's structural advantage is that the entire game state is *already* a signed gseed graph, and per-tick rollback (Brief 153) already exists; save/load is therefore just "pick a tick, name it, ship it." Brief 158 specifies that simplification.

## What we know from the spec

- Brief 153 — ECS world is the scene; per-tick diff+checkpoint rollback already exists.
- Brief 152 — every fixed tick is a signed scheduling boundary.
- Brief 157 — contacts are signed; saving on a contact boundary is cheap.
- Brief 131 — seven-axis claim; saves are Signed and Lineage-tracked.
- Brief 149 — v0.1 ships save/load.
- Round 4 Brief 091 — federated knowledge graph; saves can reference the graph.

## Findings

1. **A save = a signed scene-state gseed at a chosen tick.** The world is already a typed gseed graph; saving is selecting a tick and signing the resulting state set. Reduction to "pick a tick" eliminates the entire engine-side serialization layer that other engines maintain.

2. **Three save kinds ship at v0.1.** `full` (entire scene gseed graph at the chosen tick), `partial` (creator-declared subset of components), and `pointer` (a signed reference to a tick within the existing checkpoint stream — "no copy" save, near-instant). Pointer saves dominate in practice because Brief 153's checkpoint stream already exists.

3. **Save metadata is structured and queryable.** A save gseed carries `(save_id, scene_id, tick_number, timestamp, player_state_summary, screenshot, version_manifest, parent_save)`. The `version_manifest` lists all gseed types referenced and their schema versions for migration. The `parent_save` enables save-lineage trees (branching saves, undo of saves).

4. **Save-as-undo.** Because saves are pointer-cheap, the substrate auto-saves at every signed contact boundary, every cinematic shot transition, every level transition. Creators can roll back to any auto-save with one click — "the game's undo button" surfaced in the studio for development, in the pause menu for shipped games (opt-in per project).

5. **Migration is schema-driven, not script-driven.** Each component type carries a schema version. When a save is loaded with a different schema version than the current game, the substrate runs declared `schema.migration` gseeds for each affected type to upgrade the data. Migrations are signed gseeds creators write once per breaking change. Failed migrations refuse the load with a clear error and a signed `save.migration.failed` gseed.

6. **Save signature verification on load.** Every save is verified against its signature on load. Tampered saves are refused with `save.signature.invalid`. This is the substrate's anti-cheat foundation at the save boundary; tampering with a save file fails the constitutional integrity check.

7. **Cloud-sync via the federation protocol.** Saves are gseeds; the federation peer protocol (Brief 100, Brief 147) already syncs gseeds. Cloud-sync is "publish my save gseeds to my federation peer." Conflict resolution is lineage-aware: the save with the longer parent_save chain wins by default; explicit conflict prompts otherwise.

8. **Save slots are folders, not numbered slots.** The "save slot" UI is just a view over a folder of save gseeds with metadata. Creators can have unlimited slots, named, tagged, screenshotted. The Studio's first-ten-minutes onboarding (Brief 104) ships a default 3-slot view to match player expectations from console games.

9. **Autosave cadence is signed.** A scene declares `save.autosave.policy` as one of: `every_n_ticks` (e.g., 600 ticks = 10s), `on_event` (a list of event types — checkpoint, room change, scene end), `on_time` (every N wall-seconds), or `manual_only`. Default is `on_event` for v0.1 starter genres.

10. **Save size is bounded.** A pointer save is ~200 bytes. A full save for a typical 2D platformer scene with ~5000 entities is ~150 KB compressed (zstd; see Round 1 Brief 005). A partial save is much smaller. The substrate refuses save files larger than 10 MB at v0.1 to enforce the discipline; creators who need larger saves declare why and bypass the cap with a signed override.

11. **Replay = save + input recording.** Per Brief 154 finding 6, replay is `(initial_scene_gseed, ordered input.tick.snapshots)`. A save is a special case of replay starting at any tick instead of tick 0. This collapses save and replay into one mechanism, leveraging the existing rollback substrate.

12. **Anti-cheat at the save boundary.** Saves carry a signed `(player_id, device_id, federation_signature)` triple. Tier F multiplayer (Brief 213) verifies these on submission. Even at v0.1 single-player, saves are signed so Tier F can later add cheat detection without changing the save format.

13. **Save sharing — the social primitive.** Players can publish saves as signed gseeds to their federation peer; other players can load them (a "ghost" or "speedrun split" or "puzzle solution" mode). The signed lineage shows who recorded the save and from what scene. This is the v0.3 social primitive shipped early as a substrate property at v0.1.

14. **Performance.** Pointer save is O(1) — write the tick number. Full save is O(scene_size) but compressed and async-written off the fixed tick to avoid frame stutter. Load is bounded by the scene-compile cost and is back on the v0.1 hardware floor target of <2 seconds for a 5000-entity scene.

## Risks identified

- **Pointer saves can become invalid if their referenced checkpoint stream is compacted.** Mitigation: pointer saves are upgraded to full saves on first compaction-pruning of their tick range; cost amortized.
- **Schema migrations can be hard to write correctly across many version drifts.** Mitigation: the substrate ships a migration testing harness that runs the migration against random valid old-version gseeds and verifies the result; signed `migration.test.passed` gates publication.
- **Cloud-sync conflicts can lose work if a player edits two devices offline.** Mitigation: conflict prompts surface the lineage tree visually; default never auto-discards.
- **Anti-cheat at save level is weaker than server-authoritative state.** Mitigation: explicit; substrate documents that single-player save signing is integrity, not authority; server-authoritative comes via Tier F Brief 210.
- **Save sharing has moderation/abuse surface.** Mitigation: shared saves go through the federation moderation pipeline (Brief 215 UGC) at v0.3; v0.1 sharing is opt-in and per-direct-link only.

## Recommendation

**GSPL ships save/load at v0.1 as a thin wrapper over Brief 153's existing checkpoint+diff substrate. Three save kinds: full, partial, pointer (default cheap). Saves are signed gseeds with structured metadata, schema-versioned migration, signature verification on load, federation-protocol cloud-sync with lineage-aware conflict resolution, folder-not-slot organization, signed autosave policies, 10MB default cap, replay-equals-save semantics, anti-cheat-ready signing, and opt-in save sharing as the v0.3 social primitive available on substrate from v0.1.**

## Confidence

**4.5/5.** The design is mostly *removing* engine-side machinery rather than adding it: Brief 153 already gave us rollback; Brief 152 already gave us tick boundaries; Brief 154 already gave us replay; Brief 100 already gave us federation sync. Save/load just composes existing substrate. The 0.5 reservation is for cloud-sync conflict UX which is genuinely hard.

## Spec impact

- `gspl-reference/namespaces/save.md` — new namespace: `save.full`, `save.partial`, `save.pointer`, `save.autosave.policy`, `save.share`, `save.migration.failed`, `save.signature.invalid`
- `gspl-reference/research/153-ecs-substrate-binding.md` — cross-reference; saves are tick selections from the existing diff+checkpoint stream
- `gspl-reference/research/152-game-loop-tick-model-namespace.md` — cross-reference; tick boundaries are save points
- `gspl-reference/research/100-federation-peer-protocol-details.md` — cross-reference; cloud-sync is federation publication
- `gspl-reference/research/134-substrate-native-benchmark-battery.md` — save battery: pointer save < 1ms, full save < 100ms, load 5000 entities < 2s
- Tier C Brief 184 — save-slot UI as a stock component
- Tier F Brief 213 — anti-cheat verification reads the save signing

## New inventions

- **INV-624** — *Save = signed pointer to a checkpoint tick* — collapsing save serialization into "pick a tick" because Brief 153's diff+checkpoint substrate already exists; pointer saves are O(1) and ~200 bytes.
- **INV-625** — *Save-as-undo on signed contact boundaries* — auto-saves at structural transitions become first-class undo points, surfaced as the game's "undo button" in development and optionally in shipped games.
- **INV-626** — *Schema-versioned migration gseeds with mandatory migration testing harness* — save migration becomes a one-write-many-load discipline rather than a per-game scripting nightmare.
- **INV-627** — *Folder-not-slot save organization* with structured metadata enabling unlimited named/tagged/screenshotted saves — eliminating an entire class of UI compromise from console-era save UX.
- **INV-628** — *Replay-equals-save unification* — the substrate has one mechanism for "restart from this state with these inputs," used for both replays and saves.
- **INV-629** — *Save sharing as the early social primitive*, leveraging Brief 100 federation sync and Brief 147 adapter review — ghost saves, speedrun splits, puzzle solutions all work day-one as a v0.1 substrate property even though Tier F multiplayer is v0.3.

## Open follow-ups

- Cloud-sync conflict UX detail design (defer to Tier C Brief 184 UI editor with user research per design:user-research skill).
- Whether console-platform certification requirements (PS/Xbox/Switch) require slot-based save UI (out of v0.1 scope; revisit when console export ships).
- Save encryption at rest — not at v0.1; saves are signed (integrity) but not encrypted (confidentiality); revisit at Tier H Brief 229 game-QA strategy.

## Sources

- Brief 100 — federation peer protocol details
- Brief 131 — seven-axis structural claim
- Brief 134 — substrate-native benchmark battery
- Brief 147 — federation-wide adapter review protocol
- Brief 149 — v0.1 scope finalization
- Brief 152 — game loop and tick model namespace
- Brief 153 — ECS substrate binding
- Brief 154 — input abstraction namespace
- Brief 157 — collision and trigger primitives
- Round 1 Brief 005 — zstd deterministic encoding
- Round 4 Brief 091 — federated knowledge graph
- GGPO rollback netcode (checkpoint+diff prior art)
