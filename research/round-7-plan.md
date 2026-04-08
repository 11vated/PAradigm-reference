# Round 7 — Plan: Equipping GSPL for the full game-design surface

## Charter

Round 6.5 closed the architectural phase: the substrate is signed, scoped, costed, and benchmarked. The seven structural axes are operational. The v0.1 build-ready statement holds.

But the substrate is not yet **equipped**. Rounds 4 and 4.5 filled the *measured world* (chemistry, physics, biology, materials, characters, vehicles, music, language, etc.) — the stuff of reality. Round 7 fills the **game-design surface** — the stuff of *games*: the systems creators run, the patterns they compose, the tooling they use, the pipelines that ship the result, and the genre vocabularies that name what they're making.

This is the difference between "a substrate that *could* host a game" and "a substrate where every game any creator wants to make has typed primitives, signed recipes, and a composition path waiting." The user directive: **"all the game design and full game potentials GSPL needs full equipability all across the board."**

## Charter principles

1. **Equipping, not inventing.** Round 7 fills out existing namespaces with concrete primitives, recipes, and inventories. It does not add new substrate axes, new constitutional commitments, or new architectural primitives. (Those are frozen at end of Round 6.5.)

2. **All genres, 2D and 3D.** Per the scope decision: platformer, RPG, shooter, strategy, puzzle, racing, sim, roguelike, fighting, sandbox, narrative, MMO-lite, idle, deck-builder, metroidvania, survival, horror, rhythm, sports, fighting, card, tabletop, immersive sim, walking sim, point-and-click, visual novel, JRPG, ARPG, CRPG, RTS, 4X, tower defense, MOBA, battle royale, auto-battler, party, music, dating sim, life sim, city builder, factory, farming, cooking, fishing, dungeon crawler, bullet hell, twin-stick, side-scroller, top-down, isometric, first-person, third-person.

3. **v0.1 honesty per Brief 149.** Each brief explicitly notes which inventions ship at v0.1 (sprite/image/character era) and which are deferred to v0.2 (audio/video), v0.3 (multiplayer), v0.4 (3D-default), v0.5 (sim/world model). Round 7 equips the **full** roadmap; v0.1 just reaches into the equipped library on day one.

4. **Same brief depth as Rounds 4-6.** Full template, signed conclusions, confidence ratings, INV numbering, source citations. No catalog-style shortcuts.

5. **Composition over configuration.** Every system is specified as primitives + composition rules, not as a fixed engine. Creators compose; the substrate guarantees the composition is signed, typed, and rollback-able.

6. **DNA match to existing rounds.** Round 7 inherits the seven-axis discipline: every primitive is signed, typed, lineage-tracked, graph-structured, confidence-bearing, rollback-able, and (where applicable) differentiable.

## Non-goals

- No new substrate primitives below the engine layer (those are frozen at Round 4).
- No new constitutional commitments (frozen at 13, end of Round 4).
- No new structural axes (frozen at 7, end of Round 6).
- No new namespaces (frozen at end of Round 4).
- No code. Round 7 is research output; Round 8+ is implementation.
- No re-litigation of any Round 1-6.5 decision.
- No "engine wars" — Round 7 does not re-evaluate Godot vs Unity vs Unreal as a backbone choice. It equips the *export pipeline* to all five (Godot, Unity, Unreal, Phaser, GameMaker, Spine, Defold, plus HTML5).

## End conditions (Round 7 done when)

- Every game system any genre needs has a typed namespace with primitives and ≥3 composition recipes.
- Every major game-design pattern has a signed gseed template with parameter bounds.
- The export pipeline reaches all 8 target engines with parity tests.
- The level/scene/quest/dialogue authoring surfaces have a defined creator workflow.
- The genre matrix maps every named genre to a composition recipe drawing from the equipped libraries.
- Each brief has a confidence ≥3.
- Round 8 can begin engine implementation without re-opening any equipping question.

## Tier structure

Round 7 is organized into **eight tiers**, each with 8-12 briefs. Total expected: **~80 briefs (152-231)**. Estimated invention range: **INV-594 to ~INV-800**.

Tiers are written in dependency order — Tier A unblocks B, B unblocks C, etc. — so creators wanting to skim can read tier-by-tier.

---

### Tier A — Game system primitives (briefs 152-163)

The runtime systems any game needs, equipped as typed namespaces over Round 4 primitives.

| # | Title | Why it matters |
|---|---|---|
| 152 | Game loop and tick model namespace | Fixed/variable timestep, frame budgeting, deterministic scheduling, pause/resume/serialize |
| 153 | Entity-component-system (ECS) substrate binding | Typed components, signed entity gseeds, lineage on every spawn/destroy, rollback to any tick |
| 154 | Input abstraction namespace | Keyboard/gamepad/touch/motion/voice; rebinding; accessibility; signed input recordings for replay |
| 155 | Camera namespace | 2D/3D, fixed/follow/orbit/free; cinematic camera language; camera-as-gseed |
| 156 | Physics integration: 2D and 3D | Box2D-class + Bullet-class typed wrappers; deterministic mode; collision tagging; constraint primitives |
| 157 | Collision and trigger primitives | Layers, masks, triggers, queries, raycasts; signed contact events |
| 158 | Save/load and serialization | gseed-as-savefile; partial saves; signed save lineage; cloud-sync hooks |
| 159 | State machines and behavior trees | Typed state primitives, signed transitions, BT node library, GOAP primitives |
| 160 | Game AI primitives namespace | Pathfinding (A*, navmesh, flow fields), steering, perception, group behavior, utility AI |
| 161 | Animation runtime namespace | Skeletal, sprite, blend trees, IK, root motion, retargeting; integrates Round 2's IK briefs |
| 162 | Particle and VFX runtime | Emitters, simulators, GPU/CPU paths; deterministic mode; typed VFX gseeds |
| 163 | Audio runtime namespace | Mixing, busses, 3D positional, ducking, dynamic music; integrates Round 4 music brief; v0.2 default |

---

### Tier B — Game content inventories (briefs 164-176)

The content pools games draw from. Catalog-heavy briefs with structured inventories.

| # | Title | Why it matters |
|---|---|---|
| 164 | Mechanics vocabulary catalog | ~300 named mechanics (jump, dash, parry, craft, mine, build, hack, trade, persuade...) as typed primitives |
| 165 | Progression system patterns | XP/level, skill tree, gear score, mastery, prestige, milestone, narrative gates — each as a typed gseed template |
| 166 | Economy and currency patterns | Single/dual/multi-currency, soft/hard, faucets/sinks, inflation control, marketplace, auction, barter |
| 167 | Combat system patterns | Real-time, turn-based, ATB, action, tactics, asymmetric, hitstop/juice library |
| 168 | Enemy and creature taxonomies | Roles (tank/DPS/support/swarmer/elite/boss); telegraphs; AI archetypes; difficulty curves |
| 169 | Loot, drop, and reward systems | Drop tables, weighted RNG, pity timers, bad-luck protection, crafting reagents, set bonuses |
| 170 | Quest and mission patterns | Fetch, escort, kill, defend, explore, collect, branching, time-limited, faction; quest-as-gseed |
| 171 | Dialogue and narrative patterns | Branching trees, Ink/YarnSpinner-class typed graphs, voice integration, localization-aware |
| 172 | Level pattern library | Platformer rooms, dungeon templates, racetrack layouts, RTS map archetypes, puzzle grids |
| 173 | Tilemap and procedural generation | WFC, herringbone, BSP, drunkard's walk, cellular automata, Perlin/Simplex, Wang tiles |
| 174 | UI and HUD pattern library | Inventories, menus, dialogs, tooltips, minimaps, healthbars, ammo counters, dialog wheels |
| 175 | Sound design and music pattern library | Stingers, layered tracks, vertical/horizontal remixing, Wwise/FMOD-class typed surfaces |
| 176 | Cutscene and scripted sequence patterns | In-engine, prerendered, interactive QTE, cinematic camera, dialogue-driven, signed scene gseeds |

---

### Tier C — Authoring and tooling surfaces (briefs 177-187)

The creator-facing surfaces that touch the equipped libraries.

| # | Title | Why it matters |
|---|---|---|
| 177 | Scene and level editor specification | 2D and 3D scene graph, gizmos, snapping, prefab/inheritance, signed scene gseeds |
| 178 | Tilemap editor specification | Brushes, autotile, layers, animated tiles, collision painting |
| 179 | Animation editor specification | Timeline, curves, IK rigging, sprite-sheet packing, skeleton retargeting UI |
| 180 | Dialogue and quest editor specification | Visual node graph, voice attachment, condition expressions, localization keys |
| 181 | Behavior tree and state machine editor | Visual node graph, debugger, breakpoints, signed BT gseeds |
| 182 | Particle and VFX editor specification | Curve editors, preview, GPU/CPU toggle, deterministic seed input |
| 183 | Audio mixer and music editor | Bus routing, real-time preview, dynamic music graph, ducking rules |
| 184 | UI/HUD layout editor | Anchors, layouts, themes, accessibility checks (ties to design:accessibility-review) |
| 185 | Playtest harness specification | Recorded sessions, telemetry capture, deterministic replay, regression suite |
| 186 | Balance tooling specification | Stat tables, simulation runs, monte-carlo, sensitivity analysis |
| 187 | Mod and plugin surface specification | Sandboxed mod gseeds, signed mod manifests, federation distribution path |

---

### Tier D — Export pipeline equipment (briefs 188-196)

Parity-tested export to every target engine, end-to-end.

| # | Title | Why it matters |
|---|---|---|
| 188 | Godot export pipeline (GDScript + scenes + resources) | Reference engine; first-class parity; 2D and 3D |
| 189 | Unity export pipeline (C# + prefabs + ScriptableObjects) | Largest creator pool; 2D and 3D; URP/HDRP awareness |
| 190 | Unreal export pipeline (Blueprints + C++ + uassets) | AAA path; 3D-first; Niagara/Chaos integration |
| 191 | Phaser export pipeline (TypeScript + 2D-only) | Web-first 2D; HTML5 native |
| 192 | GameMaker Studio export pipeline (GML) | Indie 2D; sprite-first |
| 193 | HTML5 standalone export (Three.js + WebGPU) | Zero-install creator demos; v0.1 requirement |
| 194 | Defold and Cocos export pipelines | Mobile 2D path; lightweight runtime |
| 195 | Spine and DragonBones runtime export | Animation parity; cross-tool |
| 196 | Cross-engine parity test suite | Identical gseed renders identically across all 8 targets within published tolerance |

---

### Tier E — Genre composition recipes (briefs 197-208)

Every named genre as a signed composition recipe drawing from Tiers A-D.

| # | Title | Genres covered |
|---|---|---|
| 197 | 2D platformer family | Side-scroll, metroidvania, precision, puzzle-platformer, runner |
| 198 | RPG family | JRPG, ARPG, CRPG, tactical, roguelike, MMO-lite |
| 199 | Shooter family | Top-down, twin-stick, FPS, third-person, hero shooter, bullet hell |
| 200 | Strategy family | RTS, 4X, turn-based tactics, tower defense, auto-battler |
| 201 | Puzzle and casual family | Match-3, sokoban, tile-laying, hidden object, hyper-casual |
| 202 | Simulation family | City builder, factory, farming, life sim, dating sim, vehicle sim |
| 203 | Sandbox and survival family | Open-world, voxel, crafting, base-building, horror survival |
| 204 | Narrative family | Visual novel, walking sim, point-and-click, interactive fiction, immersive sim |
| 205 | Racing and sports family | Arcade racer, sim racer, kart, ball sports, fighting sports, extreme sports |
| 206 | Fighting family | 2D, 3D, platform fighter, arena fighter, brawler |
| 207 | Card and tabletop family | TCG, deck-builder, board-game digital, dice, dominos, tabletop RPG |
| 208 | Rhythm and music family | Hit-the-beat, free-form, instrument sim, generative music games |

---

### Tier F — Multiplayer and live-service equipment (briefs 209-216)

Equipping the substrate for shared and persistent worlds. v0.3 default; v0.1 ships hooks.

| # | Title | Why it matters |
|---|---|---|
| 209 | Networking model namespace | Lockstep, client-server, p2p, rollback netcode (GGPO-class), federation-aware |
| 210 | Authority and prediction primitives | Server-authoritative, client-predicted, reconciliation, signed authoritative gseeds |
| 211 | Matchmaking and lobby primitives | Skill rating, queue types, party systems, region routing |
| 212 | Persistent world and database hooks | Player state gseeds, server-side lineage, anti-cheat substrate hooks |
| 213 | Anti-cheat and integrity primitives | Server-side determinism check, signed input recordings, rollback challenge |
| 214 | Live-ops and seasonal content patterns | Battle pass, seasons, events, time-limited content, signed content drops |
| 215 | UGC and player-creation surfaces | Player-built levels, signed player gseeds, federation distribution, moderation pipeline |
| 216 | Monetization patterns library | Premium, F2P, freemium, ads, sub, season pass, IAP — opt-in per creator, ethics gate |

---

### Tier G — Developer experience and observability (briefs 217-223)

The surfaces that make the equipped substrate pleasant to build with.

| # | Title | Why it matters |
|---|---|---|
| 217 | In-Studio debugger and profiler | Tick stepping, hot-reload, lineage view, deterministic replay, signed bug repros |
| 218 | Visual scripting surface | Optional node-based language compiling to the same DSL as text-mode; signed visual gseeds |
| 219 | Asset import and conversion pipeline | Round 4 brief 089 universal pipeline applied to game-asset formats (FBX/glTF/WAV/OGG/PNG/etc.) |
| 220 | Localization and i18n pipeline | Source-of-truth in gseeds, machine + human translation, signed locale snapshots |
| 221 | Accessibility check pipeline | Color contrast, font size, control rebinding, screen reader, motion reduction — automated per build |
| 222 | Performance budget enforcement | Per-platform target FPS, draw call limits, memory ceilings, automated regression on budget breach |
| 223 | Telemetry and analytics namespace | Opt-in player telemetry, signed event gseeds, federation-aware aggregation, GDPR-clean by construction |

---

### Tier H — Genre-spanning depth and the equipping synthesis (briefs 224-231)

The cross-cutting briefs that tie the eight prior tiers into one composition surface, and the synthesis.

| # | Title | Why it matters |
|---|---|---|
| 224 | Game-feel and juice library | Hitstop, screen shake, particles, freeze frames, sound layering — typed primitives composable across all systems |
| 225 | Difficulty and pacing primitives | Difficulty curves, dynamic difficulty, mastery checks, flow-state heuristics |
| 226 | Tutorial and onboarding pattern library | Diegetic, hand-holding, sandbox, gated, contextual hint — typed patterns with telemetry hooks |
| 227 | Replay value and roguelike-loop primitives | Run seeds, meta-progression, unlock graphs, NG+, daily challenges |
| 228 | Procedural narrative and emergent story primitives | Storylets, drama managers, simulation-driven narrative, character memory |
| 229 | Game testing and QA strategy for the equipped substrate | Unit/integration/playtest/balance/regression — substrate-native test categories |
| 230 | Cross-genre composition matrix | Every Tier E genre × every Tier A system: which primitives bind to which, which combinations create which sub-genres |
| 231 | Round 7 final equipping audit | What's covered, what's not, gap registry, link-back to every tier |

---

### Synthesis

| Doc | Purpose |
|---|---|
| `round-7-plan.md` | This file — Round 7 charter and brief inventory |
| `round-7-synthesis.md` (to be written) | Round 7 (briefs 152-231) cross-brief synthesis: full equipping audit, the genre × system matrix, the v0.1 vs v0.2-v0.5 reach by tier, the inventions catalog (~INV-594..INV-800), the build-ready statement for game creation specifically |

## Brief order, dependencies, and parallelism

- **Tier A first** (152-163) — runtime systems must exist before content can land on them.
- **Tier B in parallel with C** (164-176 ‖ 177-187) — content inventories and authoring tooling co-evolve.
- **Tier D after B** (188-196) — export pipeline equips the inventories produced in B.
- **Tier E after A+B+D** (197-208) — genre recipes compose A-systems, B-content, exported via D.
- **Tier F can start after A+E** (209-216) — multiplayer needs a base game to multiplay.
- **Tier G in parallel throughout** (217-223) — devex applies to everything.
- **Tier H last** (224-231) — cross-cutting synthesis after the eight prior tiers are done.

## Estimated invention surface

Conservative estimate: **2-3 inventions per brief × 80 briefs ≈ 160-240 new inventions**. Bringing the cumulative GSPL invention catalog from 593 to roughly **750-830** by end of Round 7. Final invention count tracked in `round-7-synthesis.md`.

## v0.1 reach by tier

Per Brief 149's frozen scope, here is what each Round 7 tier ships at v0.1 vs later:

| Tier | v0.1 | v0.2 | v0.3 | v0.4 | v0.5 |
|---|---|---|---|---|---|
| A — Systems | 8/12 (loop, ECS, input, camera, 2D-physics, collision, save/load, FSM, AI-2D, anim-2D, particles-2D) | + audio runtime | + networking hooks | + 3D physics, 3D anim | + sim integration |
| B — Content | 9/13 (mechanics, progression, economy, combat-2D, enemies-2D, loot, quest, dialogue, level-2D, tilemap, UI) | + audio/music | + multiplayer patterns | + 3D content | + emergent narrative |
| C — Authoring | 7/11 (scene-2D, tilemap, anim-2D, dialogue, BT, particle-2D, UI) | + audio mixer | + multiplayer test | + 3D scene | + sim editor |
| D — Export | 5/9 (Godot, Unity-2D, Phaser, HTML5, GameMaker) | + Spine | + Unity-3D, Unreal-2D | + Unreal-3D, Defold/Cocos | + parity-3D |
| E — Genres | 6/12 (platformer, RPG-2D, puzzle, narrative, card, rhythm-2D) | + sim, sandbox-2D | + shooter-mp | + 3D-shooter, racing, fighting | + immersive sim |
| F — Multiplayer | hooks only | hooks only | first-class | first-class | sim-mp |
| G — DevEx | 5/7 (debugger, visual scripting, asset import, accessibility, perf budget) | + i18n | + telemetry | full | full |
| H — Spanning | 4/8 (juice, difficulty, tutorial, QA) | + replay loops | + multiplayer-spanning | + 3D-spanning | + emergent + matrix + audit |

**v0.1 directly equips ~50% of Round 7's surface area by item count, ~80% by creator-visible workflow coverage** (because the 2D + sprite + image + character creator workflows are the v0.1 ship, and Round 7 Tiers A-E equip them densely).

## What Round 7 deliberately defers

Even within Round 7's expansive scope, these are explicitly **out of Round 7** and will be Round 8+:

- **Specific game implementations.** Round 7 equips primitives and recipes; it does not build "GSPL Mario." That's Round 9+ when creators build their games.
- **The first showcase game.** A signed end-to-end demonstration game shipped by the founder is Round 8 work, after the equipping is in place.
- **Engine implementation in Rust.** Round 7 specifies; Round 8 implements.
- **Shader libraries beyond what Round 4 already defined.** Custom shader equipping is Round 8 if needed.
- **Specific marketplace assets.** The seed armory (Round 4 brief 088A) is the v0.1 launch content; Round 7 equips the *types* assets can take, not specific assets.
- **AI companion and NPC LLM integration patterns.** Defer to Round 8; this is its own dedicated tier.

## Risks identified

1. **Scope creep.** 80 briefs is the largest round. Mitigation: tier order is dependency-strict; we can ship Tier A as Round 7.1 if energy depletes.
2. **Genre drift.** Some named genres (auto-battler, idle, MOBA) don't have clean decompositions. Mitigation: Tier E's genre matrix forces every genre to point to existing primitives or flag a missing one.
3. **Engine parity is hard.** Tier D's parity test (brief 196) is the hardest brief in the round. Mitigation: published tolerance bands per engine, not bit-for-bit equality.
4. **Multiplayer is its own substrate.** Tier F may need to spawn a Round 7.5 the way Round 6 spawned 6.5. Mitigation: write F as hooks-only at first; expand if needed.
5. **Content catalogs may explode in length.** Tier B briefs (esp. 164 mechanics catalog) could be 300+ items. Mitigation: structured tables, not prose; cite ~10 examples per category, not all of them.

## Open questions for the user before tier writing begins

None — the three answers from the AskUserQuestion gate (full plan first, same brief depth as Rounds 4-6, all genres 2D+3D) fully constrain Round 7. Writing of Tier A can begin as soon as this plan is approved.

## Sources

- Round 6.5 synthesis (`round-6.5-synthesis.md`) — confirms architectural phase complete
- Brief 149 — v0.1 scope freeze (drives the v0.1 reach table)
- Brief 131 — seven-axis structural claim (drives the equipping discipline)
- Round 4 synthesis — measured-world libraries that Round 7 builds on top of
- Round 4 brief 089 — universal anything-to-gseed pipeline (referenced by Tier G brief 219)
- Round 4 brief 088A — canonical seed armory (referenced by Round 7 v0.1 reach)
- Round 2 brief 021 — sprite engine deep dive (foundational for Tier A 152, 153, 156)
- Round 2 brief 022 — image engine deep dive (foundational for Tier A 162)
- Brief 136 — Deep Research workflow (analog: Round 7 ships parallel game-creation workflows)
