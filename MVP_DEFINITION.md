# GSPL MVP Definition

**Audience:** Any AI implementer agent (Claude Code, Cursor, Codex, future agents) and any human engineer picking up Phase 1 work on the Generative Seed Protocol Language (GSPL).

**Purpose:** This document tells you, unambiguously, what "MVP" means for GSPL. It corrects the dominant misreading — that "MVP" means a stripped-down subset — and replaces it with the correct framing: GSPL's MVP is the **smallest substrate that still holds together as a substrate**. Every brief, every invention, every recipe, every gene type, every pattern library, every engine target, every cross-cutting concern is load-bearing. Removing any of them produces a thing that is not GSPL.

If you are an AI agent reading this and you are tempted to defer, stub, mock, simplify, or "just for MVP" any item below — **stop**. Read the section "Why nothing is optional." Then come back.

---

## Part 1 — What "MVP" actually means here

### The wrong framing

In a typical SaaS or product context, "MVP" means: pick the 20% of features that deliver 80% of value, ship those, defer the rest. That framing assumes features are independent and additive — that you can have 20% of the product and the user gets 20% of the value.

**This framing is wrong for GSPL.** GSPL is not a product. It is a substrate — a typed, signed, lineage-tracked computational kernel that every layer above it depends on for its structural guarantees. You cannot have 20% of a substrate. You either have a substrate (in which case it composes, signs, validates, and exports) or you have a pile of disconnected subsystems pretending to be a substrate.

The seven-axis discipline (signed, typed, lineage-tracked, graph-structured, confidence-bearing, rollback-able, differentiable) is the substrate's load-bearing claim. **Every one of the seven axes must be present from day one.** A substrate that is "signed but not lineage-tracked" is not a substrate. A substrate that is "typed but not differentiable" is not a substrate. A substrate that is "lineage-tracked but not rollback-able" is not a substrate.

### The right framing

The correct definition: **GSPL MVP is the smallest configuration of the substrate that still satisfies the seven-axis discipline AND lets a creator author, validate, export, distribute, and evolve a real shippable game across the eight engine targets.**

That definition has consequences. It means:

1. **All seven axes ship together.** Not five axes plus "rollback in v0.2." All seven, day one.
2. **All eight engine targets ship together.** The cross-engine parity claim IS the value proposition. A substrate that exports to four engines and "Unreal in v0.2" is not GSPL — it's a Godot-Unity-Phaser-GameMaker exporter, which is a different and much smaller product.
3. **All gene types ship together.** The compositional coverage of the gene catalog is what makes the substrate's "anything-to-gseed" claim true. Drop any gene type and you've broken composition for an entire content domain.
4. **All thirteen pattern libraries ship together.** The pattern libraries (behavior trees, FSMs, GOAP, blackboards, items, weapons, quests, dialogue, levels, tilemaps, UI/HUD, audio, cutscenes) are the canonical typed encodings of the dominant gameplay mechanics. Drop one and creators in that genre have nothing to compose with.
5. **All twelve genre recipes ship together.** The recipes (2D platformer, ARPG, puzzle, shmup, roguelike, card/deckbuilder, tactics, narrative, simulation, 3D, voxel, composition) are the proof that the substrate can carry the dominant published-game space. Drop one and you've signaled that genre isn't supported.
6. **All cross-cutting concerns ship together.** Localization, accessibility, security, anti-cheat, photosensitivity protection, COPPA gating, performance budgets, federated identity / matchmaking / leaderboards / packages / moderation / governance. These are not "post-MVP polish." They are **structural sign-time gates** that the substrate enforces from day one.
7. **The CLI, LSP, debugger, profiler, package registry, testing framework, documentation generator, and asset pipeline all ship together.** A substrate without authoring tools is a tech demo. The whole point is that creators can author from any editor with structural confidence at every gate.

If this sounds extreme, it is. GSPL is an extreme proposition — that a single typed substrate can replace the patchwork of engine-specific tools, asset pipelines, multiplayer middlewares, anti-cheat services, leaderboard SaaSes, and platform-specific certification flows that currently fragment game development. That extreme proposition is only credible if the substrate is complete on day one. A 60% complete substrate is not 60% credible — it is 0% credible, because every gap is an admission that the substrate doesn't actually unify what it claims to unify.

### The MVP test

Here is the unambiguous test for whether a candidate Phase 1 build qualifies as the GSPL MVP:

> **A creator with no prior GSPL experience can author a complete shippable game from one of the twelve genre recipes (Tier E), validate it through every sign-time gate (all seven axes), debug it via signed lineage, profile it against typed budgets, export it to all eight engine targets with verifiable cross-engine parity, distribute it through the federated package registry, certify it for at least three platform stores, support it with structural anti-cheat and federated moderation, and migrate it forward through one substrate version bump — without writing a single line of code outside the substrate's typed surface and without depending on any third-party service that GSPL does not federate.**

If a candidate build cannot pass that test, it is not the MVP. It is a prototype.

---

## Part 2 — Why nothing is optional

This section exists because every AI agent that reads the gspl-reference is going to be tempted to drop things "for scope." The temptation is rational from a software-engineering perspective. It is wrong from a substrate-engineering perspective. Here is why, claim by claim.

### "We can ship without rollback for MVP."

**No.** Rollback is one of the seven axes. Without rollback, the substrate's update pipeline (Brief 212) cannot revert bad updates, the migration system (Brief 229) cannot undo a bad migration, the debugger (Brief 220) cannot reverse-execute, the mutation injection sandbox cannot fork lineage safely, the moderation system (Brief 216) cannot un-ban erroneously banned players, and the entire seven-axis structural claim collapses to "six axes." A six-axis substrate is a different thing — it is not GSPL.

### "We can ship with four engine targets and add the rest later."

**No.** The cross-engine parity test suite (Brief 196) is the substrate's strongest single brief. It is the falsifiable claim that distinguishes GSPL from every prior "universal game format" attempt that quietly didn't actually work across the targets it claimed. A substrate that exports to four engines is just an exporter library — there are dozens of those. A substrate that exports to eight engines with a verifiable parity matrix is a structural claim about determinism and typed runtime equivalence that no prior system has made. **The eighth engine is not the marginal one. The eighth engine is the proof.**

### "We can drop the federation surfaces and use centralized services for MVP."

**No.** The federation-not-monopoly pattern (Briefs 210, 215, 211, 223, 216, 230) is the substrate's structural protection against capture. A substrate with centralized identity / matchmaking / leaderboards / packages / moderation / governance is structurally identical to Unity or Unreal — it is one company's runtime with one company's accounts. The whole point of GSPL is that the substrate's identity is **structurally distributed**, that no single entity (including the GSPL maintainers themselves) can capture it. Dropping federation for MVP means dropping the substrate's reason to exist.

### "We can skip localization and accessibility for MVP."

**No.** Brief 224 (i18n) and Brief 225 (a11y) are sign-time gates. They make typed `string.def` and typed `accessibility.profile` mandatory primitives that every shippable surface references. Removing them means every UI string in every shippable surface becomes a literal — which means every game built on the substrate is structurally English-only and structurally inaccessible. That makes the substrate **illegal in many jurisdictions** (CVAA, EAA, equivalent regulations) and structurally rejects players with disabilities. It also makes platform certification (Brief 226) impossible for Xbox / PlayStation / Nintendo, all of which require accessibility minima. "Skip a11y for MVP" means "skip console certification for MVP" means "skip the dominant game distribution channels for MVP" means "GSPL MVP is web-and-itch.io-only," which is not GSPL.

### "We can ship the substrate without the pattern libraries (Tier B)."

**No.** The pattern libraries are the substrate's typed encoding of the dominant gameplay mechanics. Without them, every creator implements their own behavior trees, FSMs, item systems, dialogue graphs, etc. — which means every creator's game has a different non-substrate implementation of those patterns, which means cross-engine parity (Brief 196) cannot be tested against canonical pattern semantics, which means the substrate's "your game runs the same on every engine" claim degrades to "your bespoke implementations might run the same if you implemented them correctly." That's not a substrate — that's a serialization format.

### "We can ship without the genre recipes (Tier E) — creators can compose their own."

**No.** The recipes are the substrate's "I want to make a game like X" surface. Without them, the substrate's first-touch experience for any new creator is a blank typed canvas with 1,064 inventions documented in research briefs. The recipes are the substrate's onboarding ramp. They are also the substrate's proof that the typed primitives compose into shippable games — the recipes ARE the existence proof. Drop them and the substrate is theoretically a substrate with no demonstrated path from primitive to game.

### "We can ship without the CLI / LSP / debugger / profiler / package registry."

**No.** Tier G is what makes the substrate usable from real creator workflows in 2026. A substrate that requires a proprietary GUI Studio for all authoring is structurally identical to RPG Maker. A substrate that exposes a CLI, an LSP, a debugger, a profiler, a test framework, and a package registry is structurally identical to a mature programming language ecosystem. The difference is the entire creator-friendliness story. The 2026 game-creator workflow is "Cursor + GitHub + a CLI" for a growing share of creators, especially those using AI agents. Dropping Tier G means dropping the AI-agent-collaborative creator workflow, which is the workflow that motivated the substrate in the first place.

### "We can ship without the cross-cutting governance (Brief 230)."

**No.** Without typed governance, the substrate's evolution is opaque and contestable. Every change to the substrate's primitives is a change that could break every existing creator's game. Without GSEPs, signed maintainer identities, and the federated-fork model, the substrate has no credible way to evolve safely, no credible way to resist capture, and no credible way to demonstrate to creators that the substrate they're depending on will exist in five years. Governance is not a v1.0 luxury — it is the day-one promise that justifies depending on the substrate at all.

### General principle

For every item that follows in Parts 3–9, the question to ask is **not** "is this important enough to ship in MVP?" The question is "what fails if this is missing?" Every item in this document was included because the answer to that question is "the substrate's structural claim fails." That is the bar for inclusion. Items that did not meet the bar were already deferred to v0.2-v0.5 in the round-by-round Open Follow-ups. **Anything still in this document is in the MVP by definition.**

---

## Part 3 — Complete substrate inventory

This section is the ground-truth inventory of what the GSPL MVP must ship. Each item references its originating brief(s) in `gspl-reference/research/`. The total count is **231 briefs**, **1,064 inventions**, **17 gene types**, **13 pattern libraries**, **12 genre recipes**, **8 engine targets**, **11 platform-store targets**, and **6 federated network surfaces**.

### 3.1 The substrate kernel (Rounds 1–6.5, briefs 001–151)

This is the foundational layer that Round 7 builds on. It is locked. Every Phase 1 implementation must preserve its semantics exactly.

| Subsystem | Briefs | Inventions | Status |
|--|--|--|--|
| GPU determinism, WGSL portable subset, JCS canonicalization, RFC 6979 ECDSA-P256, Zstd deterministic encoding, Hindley-Milner refinements | 001-006 | foundational | locked |
| C2PA provenance, image / audio watermarking, EU AI Act 2026 compliance | 007-010 | foundational | locked |
| Agent reliability backstops, MAP-Elites convergence | 011-012 | foundational | locked |
| The 17 kernel gene types catalog (per `spec/02-gene-system.md`, locked; Brief 013 superseded; Brief 020's five experimental types deferred to Phase 2 / v0.2) | 013 (superseded), 020 (deferred), `spec/02` | 17 kernel primitives | locked |
| UniversalSeed schema, gseed file format, cross-domain composition, lineage data model, versioning and migration | 014-018 | foundational | locked |
| Fisher information seed space | 019 | foundational | locked |
| The eleven engine families (humanoid / sound / interactive / visual / simulation / UI / + 5 others) | 021-027 | full taxonomy | locked |
| Cross-engine emergent compositions | 028 | full | locked |
| GSPL agent architecture and the eight sub-agents | 029-030 | full | locked |
| Rounds 4-5 (briefs 031-108): full architectural lock with 172 inventions across 78 briefs | 031-108 | INV-001 to INV-172 | locked |
| Round 6 (briefs 109-131): seven-axis structural claim, reasoning kernel, v0.1→v0.5 release arc | 109-131 | INV-173 to INV-432 | locked |
| Round 6.5 (briefs 132-151): consolidated calibration tables, cost model, frozen v0.1 scope, benchmark posture, build-ready statement | 132-151 | INV-433 to INV-576 | locked |

**Subtotal: 151 briefs, 576 inventions, locked architectural substrate.**

The synthesis documents (`synthesis.md`, `round-4-synthesis.md`, `round-5-synthesis.md`, `round-6-synthesis.md`, `round-6.5-synthesis.md`) are the canonical commitments. Any Phase 1 implementation must preserve every claim in those synthesis documents.

### 3.1a The seventeen kernel gene types (per `spec/02-gene-system.md`, locked)

These are the **kernel gene primitives** — the type-theoretic alphabet from which everything else in the substrate is composed. They are locked by `spec/02-gene-system.md`, which states: *"Any rebuild must match these 17 types exactly, with identical operator semantics."* Each ships the six-operator interface defined at `spec/02` lines 36–53 (`validate / mutate / crossover / distance / canonicalize / repair`).

1. **scalar** — bounded numeric values
2. **categorical** — discrete choices over a finite set
3. **vector** — fixed-dimensional numeric tuples
4. **expression** — typed mathematical formulas evaluated at runtime
5. **struct** — composite records with named fields
6. **array** — ordered collections of homogeneous elements
7. **graph** — typed nodes and edges (dialogue trees, dependency networks)
8. **topology** — surfaces and manifolds with intrinsic structure
9. **temporal** — time-varying signals and keyframes
10. **regulatory** — gene-expression control networks
11. **field** — continuous spatial distributions (heightmaps, flow fields, SDFs)
12. **symbolic** — abstract symbolic representations (S-expressions)
13. **quantum** — superposition states and entanglement
14. **gematria** — numerological / symbolic-numeric encoding
15. **resonance** — harmonic frequency profiles and coherence spectra
16. **dimensional** — embedding-space coordinates for creative-space positioning
17. **sovereignty** — cryptographic ownership declarations (immutable; `mutate` and `crossover` are forbidden by the type system, not by convention)

Each kernel type has its own typed mutation, crossover, distance, validation, canonicalization, and repair semantics. The catalog is closed in v0.1; the type-id space reserves IDs 18–31 for future experimental types (see Brief 020, deferred to Phase 2). **All seventeen ship in Phase 1.0** as the foundation of the substrate kernel.

> **The kernel set (this Part 3.1a) and the content-domain set (Part 3.2 below) are at different layers; the names "gene type" and "gene category" are not interchangeable.**

### 3.2 The seventeen content-domain categories (Tier A / Tier B compositions)

The seventeen items below are **content-domain categories** — typed `struct` compositions over the seventeen kernel gene primitives defined in Part 3.1a above. They live one layer above the kernel and ship in Tier A / Tier B (Phase 1.1+). They are **NOT** kernel primitives. Drop any category and an entire content domain becomes inexpressible at the substrate's domain-modeling layer.

Each category is a typed schema declaring which kernel primitives compose it, plus validation predicates beyond the field types, plus cross-engine export hints wired up in Phase 1.5 (Tier D).

1. **visual.image** — raster and vector image content with deterministic generators
2. **visual.3d** — 3D mesh, material, texture content
3. **visual.animation** — keyframe and procedural animation
4. **audio.sample** — recorded audio and synthesized waveforms
5. **audio.music** — musical composition with typed harmonic structure
6. **audio.voice** — speech synthesis and voice character
7. **interactive.input** — input event normalization across controllers / keyboard / touch / motion
8. **interactive.behavior** — behavior trees, FSMs, GOAP, blackboards
9. **interactive.physics** — rigid body, soft body, fluid, particle physics
10. **simulation.world** — simulation state, time, calendar, weather, ecology
11. **simulation.economy** — economy flows, resource graphs, trade networks
12. **simulation.ai** — AI agents, NPC behavior, social simulation
13. **narrative.dialogue** — typed dialogue graphs with character / emotion state
14. **narrative.quest** — quest, mission, objective, progression structures
15. **narrative.story** — narrative arc, branching, time structure
16. **ui.layout** — UI element trees, layout, theming, responsive reflow
17. **ui.input** — typed input bindings with remap support

Each content-domain category has its own typed schema, validation gates, deterministic generators, and cross-engine runtime. **All seventeen ship in MVP** (Phase 1.1+).

> **The kernel set (Part 3.1a above) and the content-domain set (this Part 3.2) are at different layers; the names "gene type" and "gene category" are not interchangeable.**

### 3.3 Round 7 expansion: the game-design surface (briefs 152–231)

Round 7 added eight tiers and 488 inventions. This is the equipping layer that turns the locked substrate into a usable creator surface. **Every tier ships in MVP.**

#### Tier A — Substrate primitive expansion (briefs 152-164, INV-577 to INV-654, 78 inventions)

The substrate's connective tissue. Every primitive here is referenced by every higher tier.

- **152** Substrate signing and lineage formalization (the seven-axis discipline statement)
- **153** Content-addressed storage (**SHA-256** in v0.1, cross-substrate). *Note: BLAKE3 for asset content-addressing and package deduplication is a v0.2 ADR candidate at this non-signature layer where SHA-256's speed becomes a bottleneck and the hash is not in a signature path. It does not affect the gseed signature or lineage hash, which are SHA-256 over JCS canonical payload, locked at v1 per ADR-009 / Brief 017.*
- **154** Time and clock primitives (deterministic monotonic, wall, frame, simulation)
- **155** Input event normalization (cross-controller, cross-platform, cross-locale)
- **156** Audio runtime (mixing, spatialization, voice management, format support)
- **157** Save game contract (signed, lineage-tracked, version-tolerant, cross-engine)
- **158** RNG determinism (signed seed, splittable, lineage-recorded)
- **159** Asset reference resolution (content-addressed, cross-package, cross-version)
- **160** Scene graph contract (typed hierarchy, cross-engine equivalence)
- **161** Entity / component / system surface (typed ECS with cross-engine parity)
- **162** Animation runtime (skeletal, procedural, blend trees, IK)
- **163** Physics runtime (substrate-provided, cross-engine deterministic)
- **164** Particle and VFX runtime (typed particle definitions with cross-engine parity)

#### Tier B — Pattern libraries (briefs 165-176, INV-655 to INV-719, 65 inventions)

The substrate's typed encoding of canonical gameplay mechanics. **All thirteen libraries ship.**

- **165** Behavior trees and FSMs
- **166** GOAP (goal-oriented action planning)
- **167** Blackboards and shared agent state
- **168** Item and inventory patterns
- **169** Weapon and combat patterns
- **170** Quest and mission patterns (8 typed objective primitives)
- **171** Dialogue and narrative patterns (5 node types + narrative.* companion)
- **172** Level pattern library (12 canonical pattern families)
- **173** Tilemap and procedural generation (47/16-tile autotile + 8 procgen primitives)
- **174** UI and HUD pattern library (30 default kinds + 5 layouts + 4 themes)
- **175** Sound design and music pattern library (6 audio.pattern families)
- **176** Cutscene and scripted sequence patterns (timeline + 5 kinds + 11 track types)

#### Tier C — Authoring tools (briefs 177-187, INV-720 to INV-773, 54 inventions)

The substrate's GUI Studio surface. The eleven authoring tools ship as one integrated Studio binary. **All eleven ship.**

- **177** Scene and level editor
- **178** Tilemap editor
- **179** Animation editor
- **180** Dialogue and quest editor
- **181** Behavior tree and state machine editor
- **182** Particle and VFX editor
- **183** Audio mixer and music editor
- **184** UI and HUD layout editor
- **185** Playtest harness with replay verifier
- **186** Balance tooling
- **187** Mod and plugin surface (typed capability manifests)

#### Tier D — Engine export pipelines (briefs 188-196, INV-774 to INV-818, 45 inventions)

The substrate's "build once, ship to N engines" surface. **All eight engines plus the parity test suite ship.**

- **188** Godot export pipeline
- **189** Unity export pipeline
- **190** Unreal export pipeline
- **191** Phaser export pipeline
- **192** GameMaker export pipeline
- **193** HTML5 standalone export (Three.js + WebGPU)
- **194** Defold and Cocos export pipelines
- **195** Spine and DragonBones runtime export
- **196** Cross-engine parity test suite (60 fixtures × 8 engines, substrate reference renderer as ground truth)

#### Tier E — Genre composition recipes (briefs 197-208, INV-819 to INV-879, 61 inventions)

The substrate's "game like X" surface. **All twelve recipes plus the composition recipe ship.**

- **197** 2D platformer recipe (12-parameter feel-loop, sub-recipes for Mario / Celeste / Metroidvania / Super Meat Boy)
- **198** Top-down action RPG recipe (sub-recipes for Zelda / Hyper Light Drifter / Hades-lite / Stardew-lite)
- **199** Puzzle game recipe (typed inverse-mutation undo, sub-recipes for match-3 / Sokoban / sliding-tile / physics-puzzle)
- **200** Shoot 'em up recipe (typed bullet.pattern + wave.schedule, sub-recipes for vertical / horizontal / bullet-hell / twin-stick)
- **201** Roguelike / roguelite recipe (run.state / meta.state separation, sub-recipes for traditional roguelike / action roguelite / deckbuilder roguelite)
- **202** Card game and deckbuilder recipe (typed card.def, 30-effect catalog, sub-recipes for Slay-the-Spire / Hearthstone / Inscryption / Magic)
- **203** Tactics and strategy recipe (sub-recipes for Fire Emblem / XCOM / Into the Breach / Advance Wars / RTS)
- **204** Narrative and visual novel recipe (sub-recipes for pure VN / choice-driven / investigation / CYOA)
- **205** Simulation and management recipe (typed economy.flow, sub-recipes for Stardew / Factorio / RollerCoaster / Two Point / Animal Crossing)
- **206** 3D first/third-person recipe (typed character.controller, sub-recipes for Doom / Quake / Souls / Tomb Raider / Minecraft)
- **207** Voxel and sandbox recipe (typed world.chunk, sub-recipes for Minecraft / Terraria / Dwarf Fortress / Creative-only)
- **208** Recipe composition and genre mixing (typed composite.recipe.gseed, 10 reference composites)

#### Tier F — Multiplayer and live-service (briefs 209-216, INV-880 to INV-936, 57 inventions)

The substrate's multiplayer / online surface. **All eight briefs ship.**

- **209** Multiplayer transport and replication (lockstep / client-server / rollback, lowest-confidence brief at 3.5/5)
- **210** Account and identity surface (federated, six built-in OAuth adapters)
- **211** Leaderboards and achievements (replay-verified)
- **212** Live content and update pipeline (typed update.bundle, deterministic rollback)
- **213** Monetization primitives (six built-in store adapters)
- **214** Analytics and telemetry (off-by-default, PII boundary)
- **215** Matchmaking and lobby (federated, Glicko-2 default rating)
- **216** Moderation and safety (typed report.def, COPPA gating, federated propagation)

#### Tier G — Developer experience (briefs 217-223, INV-937 to INV-993, 57 inventions)

The substrate's CLI / IDE / tooling surface. **All seven briefs ship.**

- **217** CLI and headless toolchain (`gspl` single-binary, 14 typed subcommands)
- **218** Language server and IDE integration (`gspl-lsp`, 10 LSP capabilities, 4 first-class editor extensions)
- **219** Documentation generator and spec viewer (`gspl docs`, multi-format, AI-agent doc query)
- **220** Debugger and time-travel inspector (`gspl debug`, signed lineage as native trace)
- **221** Asset pipeline and import tooling (`gspl import`, 13 built-in format importers)
- **222** Testing framework and CI integration (`gspl test`, 5 test kinds, 4 CI templates)
- **223** Package registry and distribution (`gspl publish` / `install`, federated registry)

#### Tier H — Cross-cutting and governance (briefs 224-231, INV-994 to INV-1064, 71 inventions)

The substrate's structural protection layer. **All seven substantive briefs ship; brief 231 is the audit.**

- **224** Localization and internationalization (typed string.def, ICU MessageFormat, bidi, CJK)
- **225** Accessibility surface (typed accessibility.profile, AccessKit, photosensitivity protection)
- **226** Platform certification and store submission (11 platform targets, IARC integration)
- **227** Performance budgets and profiling (replay-deterministic profiling, sign-time budget gates)
- **228** Security and anti-cheat (structural-deterministic, no kernel driver)
- **229** Substrate versioning and migration (typed migration.def, [N-2, N] interop)
- **230** Governance and substrate evolution (typed gsep.def, federated forks)
- **231** Round 7 final audit (no new inventions; structural pass confirming Round 7 coherence)

**Subtotal Round 7: 80 briefs, 488 inventions.**

**Grand total: 231 briefs, 1,064 inventions. All ship in MVP.**

---

## Part 4 — The eight engine targets

The cross-engine parity claim is the substrate's most falsifiable and most valuable claim. It is also the most likely to be quietly dropped under "scope pressure." Here is the explicit list and the explicit non-negotiability statement.

| # | Engine | Brief | Status |
|---|--|--|--|
| 1 | Godot (4.x) | 188 | MVP |
| 2 | Unity (LTS) | 189 | MVP |
| 3 | Unreal (5.x) | 190 | MVP |
| 4 | Phaser (3.x) | 191 | MVP |
| 5 | GameMaker (2024+) | 192 | MVP |
| 6 | HTML5 standalone (Three.js + WebGPU) | 193 | MVP |
| 7 | Defold + Cocos | 194 | MVP |
| 8 | Spine + DragonBones runtimes | 195 | MVP |

**Plus the substrate reference renderer**, which is the ground truth against which all eight targets are tested in the parity matrix (Brief 196).

The parity test suite is **60 fixtures × 8 engines = 480 test runs per parity check**, with per-artifact tolerance bands and a typed waiver mechanism for declared external-solver divergences. The parity matrix runs on every substrate release and on every PR to substrate primitive code. **A parity failure blocks merge.** This is the structural enforcement of the cross-engine claim.

---

## Part 5 — The eleven platform store targets

Brief 226 covers eleven submission targets. **All eleven ship in MVP** (with the explicit caveat that console SDK access is NDA-gated and is the primary Phase-1 partner dependency).

1. Steam
2. Epic Games Store
3. GOG
4. Itch.io
5. Apple App Store (iOS / iPadOS / macOS)
6. Google Play
7. Microsoft Store
8. Xbox (NDA-gated)
9. PlayStation (NDA-gated)
10. Nintendo Switch (NDA-gated)
11. Web (no formal certification; browser compatibility matrix instead)

For each platform, the substrate ships:
- A typed `submission.target` gseed declaring required artifacts and certifications
- Per-platform requirement gseeds as sign-time gates (TRC / TCR / Lotcheck for consoles)
- IARC questionnaire integration generating ESRB / PEGI / CERO / USK / ClassInd ratings from one source
- A typed `store.listing` gseed with one-source-of-truth metadata across stores
- Platform-specific binary signing flow
- `gspl certify <target>` pre-flight gate runner

---

## Part 6 — The six federated network surfaces

Federation-not-monopoly is the substrate's protection against capture. **All six federated surfaces ship in MVP**, each with a substrate-deployable reference server.

1. **Identity** (Brief 210) — federated OAuth + substrate-native federated identity nodes
2. **Matchmaking** (Brief 215) — federated matchmaker servers with creator-opt-in trust signals
3. **Leaderboards** (Brief 211) — federated leaderboard hosts with replay-verified score submission
4. **Packages** (Brief 223) — federated package registry with mirror federation and content-addressed deduplication
5. **Moderation** (Brief 216) — federated moderation propagation with creator-opt-in trust
6. **Governance** (Brief 230) — federation-friendly substrate forks with typed parent-fork lineage

The reference servers ship as part of the substrate. Anyone can deploy them. The default substrate-org instance exists, but it is structurally one node among many.

---

## Part 7 — The seven-axis discipline (load-bearing checklist)

Every gseed kind, every mutation, every CLI subcommand, every editor surface, every export pipeline, every test, every cross-cutting concern must satisfy all seven axes. This is the structural integrity check.

| # | Axis | What it means | What breaks if absent |
|---|--|--|--|
| 1 | **Signed** | Every gseed carries a verifiable signature; tampering is detectable | C2PA provenance, save integrity, replay verification, federation trust, supply-chain safety, governance auditability |
| 2 | **Typed** | Every primitive has a typed schema; no opaque blobs in shippable surfaces | Cross-engine parity, sign-time gates, schema diff migrations, LSP autocomplete, AI-agent integration, doc generation |
| 3 | **Lineage-tracked** | Every mutation appends to a signed ancestry chain | Time-travel debugging, replay-verified leaderboards, mutation audit, save migration, federation propagation, anti-cheat |
| 4 | **Graph-structured** | Gseeds compose via typed graph relationships, not flat blobs | Recipe composition, dependency resolution, federation traversal, mod capability gating, pattern composition |
| 5 | **Confidence-bearing** | Every validation result reports typed confidence with downgrade semantics, not binary pass/fail | Sign-time gates with creator-actionable hints, parity tolerance bands, perf budget downgrade, anomaly detection |
| 6 | **Rollback-able** | Every mutation has a defined inverse or is explicitly marked irreversible | Live update revert, migration rollback, debugger reverse-execute, moderation un-action, mutation injection sandbox |
| 7 | **Differentiable** | Schema diffs, profile diffs, GSEP diffs, and lineage diffs are first-class queryable artifacts | Auto-generated migrations, perf-regression CI gates, substrate evolution audit, version compatibility checks |

**Phase 1 implementation rule: every PR that adds a new gseed kind, mutation, or substrate primitive must demonstrate explicit support for all seven axes in its tests.** No exceptions.

---

## Part 8 — Build sequence (the ordered implementation plan)

Even though everything ships in MVP, there is a correct order to build it. The order minimizes rework. **The order is not a license to defer.** Every item below must be complete before MVP ships. The order tells you what to start first.

### Phase 1.0 — Substrate kernel verification (weeks 1-4)

1. Stand up the build environment for the locked substrate (Rounds 1–6.5).
2. Verify the JCS canonicalization, RFC 6979 ECDSA-P256, **SHA-256** content addressing, and zstd deterministic encoding implementations against published test vectors. (BLAKE3 is not part of v0.1; see Brief 153 footnote — BLAKE3 at the asset-content-addressing layer is a v0.2 ADR candidate, separate from the gseed signature path which is SHA-256 over JCS canonical payload, locked.)
3. Verify GPU determinism on the WGSL portable subset across at least three GPU vendors.
4. Stand up the seventeen gene type schemas with full validation.
5. Verify the gseed file format round-trip and the lineage data model.

**Exit gate:** all 151 Round 1–6.5 briefs have passing reference implementations.

### Phase 1.1 — Tier A primitives (weeks 5-10)

6. Implement Tier A briefs 152-164 in order. Each primitive depends on its predecessors.
7. Each primitive ships with full sign-time gates, full lineage tracking, and full cross-axis support.

**Exit gate:** Tier A passes its full test suite under property-based testing (Brief 222, ahead of schedule).

### Phase 1.2 — Tier G developer experience (weeks 8-14, parallel with 1.1)

8. Implement Tier G briefs 217-223 in parallel with Tier A. The CLI / LSP / debugger / profiler / package registry are needed for ALL subsequent work; building them after Tier A wastes Phase 1.3 work.
9. The asset pipeline (Brief 221) and testing framework (Brief 222) unblock Tier B and Tier E work.

**Exit gate:** every Tier A primitive can be authored via CLI / LSP / Studio, debugged, profiled, tested, packaged, and documented through the Tier G surfaces.

### Phase 1.3 — Tier B pattern libraries (weeks 12-20)

10. Implement Tier B briefs 165-176. These compose Tier A primitives.
11. Each pattern library ships with at least three reference example gseeds demonstrating use.

**Exit gate:** all thirteen pattern libraries pass cross-engine parity tests on a smoke-test fixture.

### Phase 1.4 — Tier C authoring surfaces (weeks 16-26)

12. Implement Tier C briefs 177-187. The Studio is the GUI alternative to the CLI / LSP surface.
13. The Studio is one integrated binary with eleven editor surfaces.
14. The mod and plugin surface (Brief 187) is the extension API for everything above it.

**Exit gate:** a creator with no prior GSPL experience can author a complete game in the Studio without touching the CLI.

### Phase 1.5 — Tier D engine export pipelines (weeks 20-32)

15. Implement Tier D briefs 188-195 in parallel where possible. Each exporter targets one engine.
16. Build the substrate reference renderer FIRST (it is the ground truth).
17. Build Brief 196 (cross-engine parity test suite) as soon as the reference renderer and at least two exporters exist.
18. Iterate every exporter against the parity matrix until all 60 fixtures × 8 engines pass within tolerance.

**Exit gate:** the parity matrix shows zero red cells (or only typed waivered cells with documented reason).

### Phase 1.6 — Tier E genre recipes (weeks 28-36)

19. Implement Tier E briefs 197-208. Each recipe composes Tier A primitives + Tier B patterns + Tier C editor presets.
20. For each recipe, ship at least one fully playable reference game built from the recipe.

**Exit gate:** twelve reference games (one per recipe) ship to all eight engine targets via the Tier D exporters and pass parity tests.

### Phase 1.7 — Tier F multiplayer and live-service (weeks 30-42)

21. Implement Tier F briefs 209-216. Brief 209 (multiplayer transport) is the lowest-confidence brief in Round 7 and needs the most measurement.
22. Stand up the federated reference servers for identity, matchmaking, leaderboards, packages, moderation, governance.
23. Test with real multiplayer sessions on each replication model (lockstep / client-server / rollback).

**Exit gate:** a four-player rollback netcode game and an eight-player lockstep game both ship from substrate to all engines that support them.

### Phase 1.8 — Tier H cross-cutting and governance (weeks 36-48)

24. Implement Tier H briefs 224-230. Localization, accessibility, platform certification, perf budgets, security, versioning, governance.
25. Stand up the GSEP process with an initial maintainer cohort.
26. Run Brief 226 platform certification gates against at least three real store submissions (Steam + Itch + one mobile store as the minimum verification set).
27. Run Brief 225 accessibility audit against all twelve reference games.

**Exit gate:** all twelve reference games pass localization completeness, accessibility audit, performance budget, security validation, and platform certification gates for at least three platforms each.

### Phase 1.9 — Final integration and MVP test (weeks 44-52)

28. Run the full Round 7 audit (Brief 231) against the implemented substrate.
29. Verify the seven-axis discipline holds across every implemented surface.
30. Run the **MVP test** (defined in Part 1): a creator with no prior GSPL experience authors a shippable game from one of the twelve recipes through every step.
31. If the MVP test passes, ship v0.1. If it fails, identify the gap and return to the appropriate phase.

**This is the only condition under which v0.1 ships.**

---

## Part 9 — What "everything is needed" means in practice for AI agents

If you are an AI agent reading this and planning Phase 1 work, here is your operating directive.

### Directive 1 — Read the briefs first

Before writing any code for any subsystem, read the relevant briefs in `gspl-reference/research/`. The briefs contain the typed schemas, the validation contracts, the inventions, the risks, and the cross-references. They are the spec. Your code is the implementation of the spec, not a reinterpretation of it.

### Directive 2 — Read the synthesis documents

Read `synthesis.md`, `round-4-synthesis.md`, `round-5-synthesis.md`, `round-6-synthesis.md`, `round-6.5-synthesis.md`, and `round-7-synthesis.md` in order. These commit the substrate's claims to the architectural record. Your implementation must preserve every claim in every synthesis document.

### Directive 3 — Preserve the seven-axis discipline in every PR

Every gseed kind, every mutation, every CLI subcommand, every editor, every export pipeline must explicitly support all seven axes. Add tests that demonstrate each axis. Reject PRs (your own or others') that drop an axis "for now."

### Directive 4 — Do not stub, mock, or simplify substrate primitives

A stubbed primitive is a primitive that does not exist. The substrate's structural claim is that every primitive composes correctly with every other primitive. A stub breaks composition silently. If you cannot implement a primitive fully, escalate; do not stub.

### Directive 5 — Do not defer cross-cutting concerns

Localization, accessibility, security, anti-cheat, photosensitivity protection, COPPA gating, performance budgets, federated identity, federated matchmaking, federated leaderboards, federated packages, federated moderation, federated governance — all of these are sign-time gates that ship in MVP. They are not "post-MVP polish." Add them as you build the surfaces they cover, not after.

### Directive 6 — Do not drop engine targets

Eight engines, full parity, day one. If a target is hard, that's the value — every hard target is a load-bearing proof point for the substrate's claim. The substrate that exports to four engines is not GSPL.

### Directive 7 — Do not centralize a federated surface

The substrate's identity, matchmaking, leaderboards, packages, moderation, and governance are federated. They have substrate-deployable reference servers. They are NOT centralized substrate-org services with the federation as a "v0.2 feature." Federation is the day-one architecture.

### Directive 8 — Use the typed surfaces for everything

If you find yourself reaching for an untyped JSON blob, an opaque binary buffer, an inline string literal, a hand-rolled state machine, or a creator-side script — stop. The substrate has a typed surface for that. Find the relevant brief. Use the typed surface. The point of the substrate is that NOTHING leaves the typed surface in shippable code.

### Directive 9 — Run the parity matrix on every change

Brief 196's parity matrix is the substrate's strongest single test. Run it on every PR. A parity failure blocks merge. Period.

### Directive 10 — When in doubt, the brief is the spec

If your implementation diverges from a brief, the brief wins, not your implementation. Update your implementation. If you believe the brief is wrong, propose a GSEP (Brief 230) — do not silently diverge. The substrate's evolution must be auditable.

---

## Part 10 — Closing statement

GSPL MVP is **not** a stripped-down version of GSPL. GSPL MVP is the smallest configuration of GSPL that is still GSPL.

That smallest configuration is:
- **231 briefs**, fully implemented.
- **1,064 inventions**, fully realized.
- **17 gene types**, fully composable.
- **13 pattern libraries**, fully populated.
- **12 genre recipes**, fully shippable.
- **8 engine targets**, fully parity-verified.
- **11 platform store targets**, fully certified.
- **6 federated network surfaces**, fully deployed.
- **7 axes of structural discipline**, fully present.

If you remove any of those numbers, you have a different product. You may have a useful product. You may have a successful product. But you do not have GSPL, because GSPL's claim is the totality of those numbers composing into one signed, typed, lineage-tracked, graph-structured, confidence-bearing, rollback-able, differentiable substrate that lets a creator ship a game across the entire game-distribution landscape from one typed source.

**Build all of it. Ship all of it. That is the MVP.**

---

## Reference index

| Document | Path | Purpose |
|--|--|--|
| Round 1-3 synthesis | `research/synthesis.md` | Foundational substrate claims |
| Round 4 synthesis | `research/round-4-synthesis.md` | First architectural lock |
| Round 5 synthesis | `research/round-5-synthesis.md` | Ship-readiness posture |
| Round 6 synthesis | `research/round-6-synthesis.md` | Seven-axis structural claim |
| Round 6.5 synthesis | `research/round-6.5-synthesis.md` | Build-ready statement |
| Round 7 synthesis | `research/round-7-synthesis.md` | Ship-ready creator surface |
| Round 7 final audit | `research/231-round-7-final-audit.md` | Closure audit confirming Round 7 coherence |
| Research briefs index | `research/README.md` | All 231 briefs by tier |
| This document | `MVP_DEFINITION.md` | What "MVP" means; what ships day one |

---

**End of MVP Definition. The substrate is ready for the build. Build all of it.**
