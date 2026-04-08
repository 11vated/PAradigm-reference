# 209 — Multiplayer transport and replication

## Question
What is the typed multiplayer transport and replication layer that enables substrate gseeds to support 2-32 player real-time multiplayer (lockstep, client-server, and rollback) across all eight v0.1 engine targets, with deterministic state synchronization and signed replay parity?

## Why it matters (blast radius)
Multiplayer is the highest-revenue genre stratification in modern games (live-service, MOBAs, battle royales). It is also the substrate's most demanding determinism test: every client must produce bit-identical state from identical input streams. Without a typed transport layer, multiplayer is per-game implementation and the substrate's "write once, ship anywhere" promise collapses for the entire live-service category.

## What we know from the spec
- Brief 020 — determinism contract per engine.
- Brief 152 — substrate signing and lineage.
- Brief 158 — save snapshot model.
- Brief 162 — VFX with deterministic seeds.
- Briefs 197-208 — single-player recipes.

## Findings
1. **Three replication models supported.** Substrate ships three typed replication strategies: **lockstep** (all clients run identical sim with synchronized inputs; canonical for RTS / fighting / fully-deterministic), **client-server** (authoritative server with client prediction; canonical for FPS / MMO), and **rollback** (lockstep with client-side prediction and state rewind on input miss; canonical for fighting games / netcode-critical genres). Recipes select via typed `multiplayer.model` field.
2. **Transport layer abstraction.** `transport.def` typed gseed declares: protocol (UDP / WebRTC DataChannel / WebSocket / TCP), reliability mode (ordered-reliable / unreliable / unordered-reliable), max message size, jitter buffer config. Substrate ships transport implementations for each engine target — WebRTC for browser exports, ENet for native exports, engine-native (Unity Netcode / Unreal Replication) where the engine's solution composes with substrate's deterministic kernel.
3. **Deterministic input stream.** All replication models share the same primitive: typed `input.frame` gseeds delivered per-tick. Each frame contains all clients' input.action values for that tick. Lockstep waits for all frames before advancing; client-server forwards to the authoritative server; rollback predicts and rewinds on mismatch.
4. **Replication contract.** Recipes declare which gseeds replicate via typed `replicate.policy` field per gseed kind. Three policies: **full** (every field replicates), **delta** (only changed fields), **eventual** (replicates on quiescence, e.g., for inventory). Default policies ship per substrate primitive type.
5. **Authoritative server option.** Client-server model requires a substrate server runtime. Substrate ships a headless server build per engine target (Godot headless, dedicated Unity / Unreal server builds, Node.js for web targets). Server runtime applies the same substrate kernel as the clients.
6. **Lag compensation.** Client-server model ships substrate-provided lag compensation: server records typed snapshot history and re-simulates hit detection at the client's render time. Typed `lag.budget.ms` field caps the maximum compensation window.
7. **Anti-cheat surface.** Substrate provides typed input validation gates at the server (input rate limits, action validity, position sanity). Cheating is hard to fully prevent but the typed gates close the most common holes. v0.1 ships the gates; sophisticated anti-cheat (BattlEye / EAC integration) is creator-responsibility deferred to v0.4.
8. **Replay parity.** Each multiplayer session produces a signed replay gseed via Brief 185 playtest harness, recording all `input.frame` gseeds from the session. Replay reconstructs the session bit-identically by replaying inputs through the substrate kernel — across any of the eight engines per Brief 196.
9. **Player count caps.** v0.1 ships with typed `player.count.max` validated per replication model: lockstep ≤ 8 (synchronization cost grows with N²), client-server ≤ 32, rollback ≤ 4 (typically 1v1 or 2v2). Higher caps deferred to v0.3+.
10. **Matchmaking.** Out of v0.1 scope. Substrate provides the transport + replication layer; matchmaking is creator-responsibility or covered by federation surface in Brief 187. Brief 215 covers matchmaking primitives.
11. **NAT traversal.** WebRTC handles NAT traversal natively for browser exports; native exports use STUN servers. Substrate ships a default STUN config; creators can override.

## Risks identified
- **Determinism across engines under network conditions.** Network jitter can expose latent non-determinism. Mitigation: Brief 196 parity suite includes multiplayer fixtures; cross-engine replay parity is the gate.
- **Cheat surface.** Client-server is the only model with meaningful cheat resistance. Mitigation: document model trade-offs; recommend client-server for competitive games.
- **Server hosting cost.** Authoritative servers cost real money. Mitigation: v0.1 ships peer-to-peer lockstep / rollback for cost-free hosting; client-server for creators willing to pay.
- **Engine-native vs substrate-provided.** Some engines (Unity, Unreal) have mature replication. Mitigation: substrate uses engine-native where it composes deterministically; substrate-provided otherwise. Per-engine matrix documented.
- **Latency budgets.** Real-time games need sub-100ms round-trip. Mitigation: substrate exposes typed latency budgets; recipes warn at sign-time when budget unrealistic for target audience geography.

## Recommendation
Specify multiplayer transport and replication as a typed `multiplayer.def` gseed kind composing `transport.def` + replication-model selection (lockstep / client-server / rollback) + `replicate.policy` per gseed kind + signed replay parity, with substrate-provided transports per engine target and engine-native replication where it composes deterministically. Default player count caps per model (8 lockstep, 32 client-server, 4 rollback). Defer matchmaking and sophisticated anti-cheat to later versions.

## Confidence
**3.5 / 5.** Multiplayer is the hardest brief in Round 7. Lockstep and rollback are well-understood; client-server with deterministic substrate kernel is novel and needs Phase-1 validation. Lower than 4 because the engine-native vs substrate-provided per-engine matrix has high uncertainty until measured.

## Spec impact
- New spec section: **Multiplayer transport and replication specification**.
- Adds typed `multiplayer.def`, `transport.def`, `input.frame`, `replicate.policy` gseed kinds.
- Adds the three replication models as substrate-provided runtimes.
- Adds the substrate headless server build per engine target.
- Cross-references Briefs 020, 152, 158, 162, 185, 196.

## New inventions
- **INV-880** — Typed `multiplayer.def` gseed composing transport + replication-model + replicate.policy: multiplayer is a first-class typed substrate primitive, not per-game implementation.
- **INV-881** — Three substrate-provided replication models (lockstep / client-server / rollback) with creator-selectable model: substrate ships the algorithms; recipes pick.
- **INV-882** — Typed `input.frame` per-tick primitive shared across all three replication models: input streams are first-class signed gseeds enabling replay-bit-determinism across network conditions.
- **INV-883** — Typed `replicate.policy` per gseed kind (full / delta / eventual): replication granularity is structured creator choice, not opaque framework decisions.
- **INV-884** — Substrate headless server build per engine target with shared kernel: authoritative servers run the same substrate kernel as clients, guaranteeing parity.
- **INV-885** — Typed lag compensation with substrate-provided snapshot history and re-simulation: lag compensation is a substrate primitive with creator-tunable budget.
- **INV-886** — Per-replication-model player count caps validated at sign-time: substrate enforces realistic player counts per model with explicit upgrade paths.

## Open follow-ups
- Phase-1 cross-engine multiplayer parity validation — Brief 196.
- Matchmaking primitives — Brief 215.
- Sophisticated anti-cheat (EAC / BattlEye) integration — deferred to v0.4.
- Massively multiplayer (32+ players) — deferred to v0.3.
- Cross-region datacenter routing — deferred to v0.4.

## Sources
1. Brief 020 — Determinism contract per engine.
2. Brief 152 — Substrate signing and lineage.
3. Brief 162 — VFX with deterministic seeds.
4. Brief 185 — Playtest harness.
5. Brief 196 — Cross-engine parity test suite.
6. "1500 archers on a 28.8" — Mark Terrano (Age of Empires lockstep).
7. "I Shot You First" — Valve (Source engine lag compensation).
8. GGPO rollback netcode documentation.
9. WebRTC specification (w3.org/TR/webrtc/).
10. ENet documentation (enet.bespin.org).
