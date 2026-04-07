# 074 — GSPL multiplayer runtime

## Question
Brief 065 and Brief 067 conceded that "GSPL doesn't have a multiplayer runtime" and that Roblox wins on this axis. That concession was premature. How does GSPL ship multiplayer natively — without a central server, without a client-authority model, without Roblox-style hosting — using federation, deterministic kernels, CRDTs, and lineage-as-shared-state?

## Why it matters
Multiplayer is the defining property of Roblox, Fortnite, and any live social creator platform. If GSPL claims to be "the anti-Roblox" (Brief 067) but has no multiplayer story, the claim is hollow. Worse, multiplayer is *where creators make money* — live events, shared worlds, collaborative creation are the economic lifeblood of modern creator platforms. The right answer is not "export to Unity and use their netcode"; the right answer is "GSPL multiplayer is substrate-native and structurally superior."

## What we know from the spec
- Brief 015: gseed format is content-addressed.
- Brief 026: deterministic kernel.
- Brief 042: cryptographic identity.
- Brief 043: federation with libp2p.
- Brief 045: anti-piracy via lineage utility.
- Brief 052: lineage time machine.
- Brief 053: local-first storage with CRDT config sync.

## Findings — Roblox/Unreal multiplayer's structural limits

Traditional multiplayer (Roblox, Unreal Replication, Unity Netcode, Photon, Nakama) is built around three architectural assumptions GSPL rejects:

1. **Client-server with authoritative server.** The server is the source of truth; clients are thin replicas. This requires *trust in the operator* running the server — a privileged position GSPL's sovereignty principle cannot grant to any single party.
2. **State synchronization over deltas.** Game state lives in server memory; clients get diffs. When the server dies, the world ends. Roblox's entire economy is hostage to Roblox Corp's uptime.
3. **No cryptographic identity of participants.** Usernames, not signatures. Players cannot prove authorship of their contributions; moderation is centralized; bans are server-side.

These are not features those platforms can remove. Centralization is their business. GSPL's multiplayer starts from the opposite axioms.

## Findings — what GSPL ships

### 1. Lineage as shared state (INV-210)
A "multiplayer room" in GSPL is a **shared lineage DAG**. Every participant has a local copy of the lineage; every change is a new lineage node signed by its author; changes propagate over federation; conflicts resolve via CRDT merge on the parameter graph and via explicit branching on the artifact graph. The room *is* the lineage; the lineage is the room.

There is no server. There are peers, the federation transport (libp2p/QUIC per Brief 043), and the cryptographically-signed lineage. Any peer can host a snapshot; any peer can relay; any peer can leave without killing the room.

**Concrete win:** A collaborative level-design session with 8 people editing the same scene simultaneously. Every edit is signed, attributed, reversible, and reproducible. If Alice drops out, the room continues. If the "host" disconnects, nothing happens because there is no host. If everyone drops out and comes back tomorrow, the lineage is waiting on disk. Roblox cannot do this without its entire infrastructure.

### 2. Deterministic-kernel lockstep for real-time gameplay (INV-211)
For real-time multiplayer games (not just collaborative editing), GSPL leverages the deterministic kernel (Brief 026) for classical lockstep networking. Every participant runs the same simulation bit-exactly; only inputs are exchanged; state emerges identically on every machine.

Lockstep is an old technique (Age of Empires, Starcraft, fighting games) with two historical downsides: (a) it requires bit-exact determinism across platforms, which is hard, and (b) it's vulnerable to cheating because clients are trusted. GSPL's deterministic kernel is purpose-built for bit-exact reproducibility across platforms (Brief 026, Brief 027). And cheating is addressed via signed-input attestation: every input is signed by the player's cryptographic identity; a cheater's signature is on the record; community blocklists (Brief 061) propagate reputation.

**Concrete win:** Fighting games, RTS, co-op roguelikes — all playable multiplayer in GSPL with zero server cost and full replay/provenance. The replay *is* the lineage. Every frame is verifiable.

### 3. CRDT-based concurrent editing for collaborative creation (INV-212)
For collaborative creation (level design, dialog writing, procedural tuning), GSPL uses state-of-the-art CRDTs (Yjs, Automerge, Loro, diamond-types) on the parameter graph. CRDTs guarantee convergence without coordination: every peer sees the same final state regardless of network order.

GSPL's parameter graph is structured for CRDT-friendliness: parameters are per-node, changes are local, conflicts are semantic. The substrate ships a specialized CRDT that understands the gseed schema — per-parameter LWW (last-writer-wins) for scalars, OR-set for collections, RGA for sequences.

**Concrete win:** Eight people editing the same scene in real-time with zero "merge conflicts" — the substrate merges automatically and the lineage records every contribution with authorship.

### 4. Authority via consent, not operators (INV-213)
Every room has an explicit authority model declared in its metadata: open (anyone signs anything), curated (one or more curators sign final merges), democratic (majority vote among signers), or capability-scoped (per-area editors). The authority model is enforceable at the substrate level; unauthorized changes don't propagate past their branch.

Moderation is per-room. A room owner can kick a peer by refusing their signed changes. The peer can fork the room and continue independently. There is no platform-level deplatforming because there is no platform.

**Concrete win:** A creator hosts an open-world game where anyone can visit but only signed curators can modify the main branch. Visitors see the canonical branch; anyone can fork it; forks compete via federated discovery (Brief 067).

### 5. Session resumability and offline play (INV-214)
Because the room is a lineage on disk, and the lineage is content-addressed, a player can go offline, play solo on their local branch for hours, come back, and merge their changes. This is structurally impossible in a client-server architecture.

**Concrete win:** An MMO-style experience where your offline play counts. Roblox and every other multiplayer platform loses your progress the moment you disconnect.

### 6. Provenance and fair play
Every multiplayer event is c2pa-attested through the lineage (Brief 008, 058). Disputes ("did that player really do that?") are resolved by the signed lineage. Cheaters are identified by their signatures. Rankings are reproducible because they're lineage-derived.

**Concrete win:** Competitive play with cryptographic anti-cheat. No "the server saw it differently" — the substrate is the record.

### 7. Zero hosting cost for creators
A Roblox creator depends on Roblox's servers for every player session. A GSPL creator's "server" is the federation; there is no per-player cost. The economic model (Brief 044) settles via creator-chosen license tiers with no platform fee.

**Concrete win:** A solo creator hosts a world with 10,000 concurrent players at zero infrastructure cost. In Roblox, scaling is limited by what Roblox chooses to allocate and what percentage Roblox takes.

### 8. Netcode that works offline-first
GSPL's netcode is fundamentally asynchronous: all changes are local first, federated second. Latency-sensitive real-time play uses the lockstep path (INV-211); everything else is CRDT async. There is no "connection lost" error — worst case, the lineage pauses federating and resumes when the network returns.

## Architecture summary

Three multiplayer modes on the substrate:

| Mode | Latency | Use case | Mechanism |
|---|---|---|---|
| **Async shared-world** | seconds to hours | Collaborative creation, persistent worlds, asynchronous MMOs | Lineage-as-state + CRDT merge + federation propagation |
| **Real-time lockstep** | 10-50ms | Competitive games, fighting games, RTS | Deterministic kernel + signed-input exchange + per-frame consensus |
| **Hybrid** | mixed | Most game genres | Async state + lockstep for real-time events |

Every mode is substrate-native. Every mode ships with provenance and signed identity.

## What GSPL ships at each phase

### v1
- **CRDT-based collaborative editing** in the studio (multi-user scene editing, parameter tuning).
- **Async lineage federation** (Brief 043 direct-invite mode).
- **Signed-input attestation** for all lineage contributions.
- **Authority model v1**: open / curated / capability-scoped.
- **Session resumability** (lineage persists on disk).

### v1.5
- **Deterministic-kernel lockstep** for real-time game prototypes.
- **DHT federation** for discovering multiplayer rooms (Brief 043).
- **Democratic authority** (majority-vote merges).
- **Per-room moderation** with community blocklists (Brief 061).
- **Replay-as-lineage** demos.

### v2
- **Production-grade real-time multiplayer** with predicted-and-rolled-back lockstep (GGPO-style but lineage-backed).
- **Federated matchmaking** via DHT and reputation.
- **Cross-engine multiplayer** (the same room renders differently in different engine exports).
- **Marketplace for hosted "rooms as services"** where creators can monetize session access.

## Inventions

### INV-210: Lineage-as-shared-state multiplayer
A multiplayer session is a federated, CRDT-synchronized lineage DAG. No central server; every change is signed and replicable; offline-first by default. Novel because no multiplayer architecture treats the session state as a content-addressed federated artifact.

### INV-211: Deterministic-kernel lockstep with signed inputs
Classical lockstep networking over the GSPL deterministic kernel, with every player input signed and recorded in the lineage. Replay is byte-identical; cheating is cryptographically attributable; the lineage *is* the replay. Novel because classical lockstep never had cryptographic identity or content-addressed state.

### INV-212: Gseed-schema-aware CRDT
A CRDT specialized for the GSPL parameter graph: per-parameter LWW for scalars, OR-set for collections, RGA for sequences, with the substrate guaranteeing convergence. Distinct from generic CRDTs because it understands gseed semantics and propagates intent, not just bytes.

### INV-213: Consent-based authority model
Room-level authority declared as substrate metadata: open / curated / democratic / capability-scoped, enforced by the federation. Forking is always available as an exit. Novel because no multiplayer platform makes authority a substrate property instead of a server configuration.

### INV-214: Offline-first session with async merge
Players can go offline, make changes, and merge back via CRDT + lineage when they return. The session persists without the network. Novel because no multiplayer platform treats sessions as local-first.

## What Roblox still does better at v1

Honest accounting:
- **Matchmaking and discovery.** Roblox has 70M DAU and a polished discovery UI. GSPL federation starts empty.
- **Monetization polish.** Roblox's Robux economy, developer exchange, and payout infrastructure are mature; GSPL's marketplace is v1.
- **Integrated voice/chat.** Roblox has built-in voice; GSPL ships in v1.5.
- **Mobile-first UX.** Roblox is mobile-native; GSPL is desktop-native at v1.

These are time-and-investment gaps. The architectural ledger favors GSPL on every axis except installed-base.

## Risks identified

- **CRDT convergence on complex schemas is hard.** Mitigation: specialized gseed CRDT (INV-212); extensive property-based testing; reference implementations from Automerge/Yjs/Loro.
- **Lockstep determinism across platforms is hard.** Mitigation: Brief 026 deterministic kernel is already a core spec commitment; Brief 027 is the test harness.
- **NAT traversal for peer-to-peer.** Mitigation: libp2p handles this; STUN/TURN fallback; optional relay peers.
- **DDoS on federated rooms.** Mitigation: reputation-based admission; signed-input rate limiting; blocklist federation.
- **Cheating via input fabrication.** Mitigation: signed inputs + lineage replay. A cheater can fake inputs but cannot hide the signature.
- **Session discovery without central matchmaker.** Mitigation: DHT-based discovery at v1.5; reputation indexers; social-graph invites.
- **Latency for global play.** Lockstep mode is latency-sensitive; peers far from each other will experience lag. Mitigation: rollback networking (GGPO-style) on top of the deterministic kernel at v2.

## The strategic claim

Every major multiplayer platform today is **one server outage away from existential failure**. Roblox goes down, Fortnite goes down, World of Warcraft goes down — the worlds literally cease to exist. GSPL's lineage-as-state multiplayer is the first architecture where the world *cannot* go down, because the world is on every participant's hard drive. **This is not a feature. This is a new category of multiplayer.** And it's only possible because of the substrate decisions already locked in (signed identity, federation, deterministic kernel, lineage, content addressing).

## Recommendation

1. **Reverse the Brief 065 and Brief 067 concessions.** GSPL ships substrate-native multiplayer from v1.
2. **CRDT collaborative editing at v1** as the first multiplayer feature (lowest-risk, highest-value for creators).
3. **Deterministic-kernel lockstep at v1.5** for real-time game prototypes.
4. **Ship INV-210 (lineage-as-state) as the headline demo** — "we killed the server."
5. **Engage Automerge, Yjs, Loro teams** as CRDT advisors.
6. **Engage GGPO author (Tony Cannon)** on rollback networking for v2.
7. **Position as "the multiplayer platform with no platform"** in marketing.
8. **Marketing language**: "Roblox's servers can go down. GSPL's can't — there aren't any."

## Confidence
**4/5.** The architectural pieces all exist individually (CRDTs, lockstep, libp2p); the novel contribution is composing them with GSPL's substrate guarantees. The 4/5 reflects honest uncertainty about matchmaking UX at federation scale.

## Spec impact

- `architecture/multiplayer-substrate.md` — new doc.
- Update Brief 065 to remove the "no multiplayer runtime" concession.
- Update Brief 067 to replace the Roblox multiplayer concession with the anti-platform thesis.
- New ADR: `adr/00NN-lineage-as-shared-state.md`.
- New ADR: `adr/00NN-deterministic-lockstep.md`.

## Open follow-ups

- Pick CRDT library foundation (Automerge vs Yjs vs Loro).
- Build INV-210 prototype with 8-way collaborative editing.
- Engage CRDT research community.
- Engage GGPO author on rollback for v2.
- Design federated matchmaking at v1.5.
- Legal review of peer-to-peer liability per jurisdiction.

## Sources

- Shapiro et al., "A comprehensive study of Convergent and Commutative Replicated Data Types" (2011).
- Automerge (Kleppmann et al.), Yjs (Jahns et al.), Loro, diamond-types.
- Cannon, "GGPO Developer Guide" (rollback networking).
- Age of Empires lockstep postmortem.
- libp2p specification.
- Roblox developer documentation.
- Internal: Briefs 015, 026, 027, 042, 043, 044, 045, 052, 053, 058, 061, 065, 067.
