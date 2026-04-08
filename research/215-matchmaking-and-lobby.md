# 215 — Matchmaking and lobby

## Question
What is the typed matchmaking and lobby surface that enables substrate creators to support player-vs-player matchmaking, party formation, room-based lobbies, and skill-rated queues across the eight engine targets, with federation-friendly hosting and replay-verified ranking?

## Why it matters (blast radius)
Multiplayer (Brief 209) needs more than transport — players must find each other. Without typed matchmaking primitives, every multiplayer creator integrates Steam Lobbies / EOS Sessions / GameLift independently. The brief specifies a typed matchmaking surface that composes with Brief 209 transport and Brief 210 identity.

## What we know from the spec
- Brief 209 — multiplayer transport.
- Brief 210 — account and identity surface.
- Brief 211 — leaderboards and achievements.
- Brief 187 — mod surface (federation precedent).

## Findings
1. **Lobby as typed gseed.** `lobby.def` declares: typed mode (open / invite-only / matchmade), max player count, typed match parameters (game mode, map, difficulty), host policy (peer / dedicated), region, current player list, signed lobby state.
2. **Matchmaking as typed mutation.** Player emits typed `matchmaking.request` mutation with criteria (mode, region, skill range). Substrate matchmaker assigns players to lobbies satisfying constraints. Assignment emits typed `matchmaking.assigned` mutation.
3. **Backend adapter pattern.** `matchmaker.adapter` typed gseed declares the implementation: built-in adapters for Steam Lobbies, Epic EOS Sessions, AWS GameLift, plus a creator-extensible adapter, plus a substrate-default federation matchmaker (deployable substrate server).
4. **Skill rating.** Optional typed `rating.def` declares: rating system (Elo / Glicko-2 / TrueSkill), update rules, decay parameters. Substrate ships Glicko-2 as default. Rated lobbies match players within typed rating range.
5. **Party / group support.** Typed `party.def` declares pre-formed player groups that matchmake together. Party state lives in lobby state.
6. **Region and latency awareness.** Lobby creation includes typed region; matchmaker prefers same-region matches. Latency probes between players inform host selection in peer mode.
7. **Reconnection support.** Disconnected players have typed reconnection windows (default 60s); substrate runtime preserves their slot in the lobby.
8. **Federation matchmaker.** Substrate ships a deployable federated matchmaker (analogous to Brief 210 federated identity). Creators run their own; cross-federation matchmaking is opt-in and signed.
9. **Replay-verified ranking.** Rated matches submit replay gseeds (Brief 211 leaderboard pattern); rating updates are gated on replay verification. Eliminates rating manipulation.
10. **Validation contract.** Sign-time gates: at least one matchmaker adapter declared, lobby max player count valid for replication model (Brief 209), rating system declared if rated lobbies exist, region declared.

## Risks identified
- **Matchmaker scaling.** Large queues stress matchmakers. Mitigation: federated matchmaker scales horizontally by region; substrate ships a sharding primitive.
- **Skill rating gaming.** Players can manipulate ratings via match-throwing. Mitigation: replay-verified ranking + statistical anomaly detection (server-side) close common attacks.
- **Cross-federation trust.** Trusting another federation's matchmaker requires verifying their identity claims. Mitigation: signed federation proofs per Brief 210; creators choose which federations to trust.
- **Latency probe overhead.** Probing all players costs bandwidth. Mitigation: typed budget for probe count; default 5 candidates per matchmaking request.

## Recommendation
Specify matchmaking and lobby as typed `lobby.def` + `matchmaking.request` + `matchmaker.adapter` + `rating.def` gseeds with built-in adapters for 3 platforms plus federation default, Glicko-2 as default rating system, party and reconnection support, replay-verified ranking, and federated matchmaker hosting.

## Confidence
**4 / 5.** Matchmaking mechanics are well-precedented; the novelty is the federated matchmaker pattern with replay-verified ranking. Lower than 4.5 because matchmaker scaling under real player loads needs Phase-1 measurement.

## Spec impact
- New spec section: **Matchmaking and lobby specification**.
- Adds typed `lobby.def`, `matchmaking.request`, `matchmaking.assigned`, `matchmaker.adapter`, `rating.def`, `party.def` gseed kinds.
- Adds the federation matchmaker as substrate-deployable.
- Cross-references Briefs 187, 209, 210, 211.

## New inventions
- **INV-921** — Typed `lobby.def` + `matchmaking.request` pair with creator-selectable matchmaker adapter: matchmaking is a first-class substrate primitive with pluggable backend.
- **INV-922** — Federated matchmaker as substrate-deployable server analogous to Brief 210 identity: matchmaking lives with creators, no centralized substrate service.
- **INV-923** — Typed `rating.def` with substrate-shipped Glicko-2 default: skill ratings are first-class typed primitives with pluggable systems.
- **INV-924** — Replay-verified ranking via Brief 211 leaderboard pattern: rated match outcomes verified before rating updates apply, eliminating manipulation.
- **INV-925** — Typed `party.def` for pre-formed group matchmaking: parties are first-class typed primitives with structural party-state in lobbies.
- **INV-926** — Typed reconnection window with slot preservation: disconnects are recoverable as a substrate primitive, not creator implementation.
- **INV-927** — Region-aware latency-probed host selection with typed probe budget: latency optimization is structured creator choice.

## Open follow-ups
- Phase-1 matchmaker scaling measurement.
- Tournament bracket primitives — deferred to v0.3.
- Cross-platform matchmaking (Steam + console + federation) — deferred to v0.4.
- Behavior-based matchmaking (avoid toxic players) — deferred to v0.4.

## Sources
1. Brief 187 — Mod and plugin surface.
2. Brief 209 — Multiplayer transport.
3. Brief 210 — Account and identity surface.
4. Brief 211 — Leaderboards and achievements.
5. Glicko-2 rating system paper — Mark Glickman.
6. TrueSkill paper — Microsoft Research.
7. Steam Lobbies API documentation.
8. Epic Online Services Sessions documentation.
