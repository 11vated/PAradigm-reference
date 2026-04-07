# 043 — Federation protocol: peer discovery, sync, gossip, conflict resolution

## Question
How do GSPL studios federate with each other to share seeds, lineage, attestations, and preference signals — without a central server, without leaking private data, and without becoming a botnet target?

## Why it matters
GSPL is sovereignty-first. A central server is a single point of failure, a censorship target, and a privacy risk. Federation is the only architecture consistent with the founding constraints: every studio is a peer, every seed is content-addressed, every signature is verifiable independently. But federation has its own pitfalls — gossip storms, sybil attacks, content moderation impossibility, the diaspora-fail-mode. GSPL must do federation *carefully*.

## What we know from the spec
- Brief 017: content-addressed lineage DAG.
- Brief 042: per-user identity keys.
- Federation has not been formally specified yet.

## Findings — federation in five layers

### Layer 1: Peer discovery
Two modes:
- **Direct invite (default v1):** users exchange a peer URL containing the public key, network address, and a signed handshake nonce. Out-of-band exchange (paste a string in chat).
- **DHT-based discovery (v1.5):** opt-in Kademlia DHT for finding peers by public key. Bootstrap nodes are community-run; the studio ships a small list of known bootstraps but rotates them every release.
- **No central directory.** Ever.

### Layer 2: Transport
- **libp2p as the transport substrate.** Battle-tested, well-maintained, polyglot. Same stack as IPFS and Filecoin.
- **QUIC + Noise** for the secure channel. TCP+TLS as fallback.
- **NAT traversal:** STUN + TURN where needed. The studio ships a small list of community TURN relays.
- **Bandwidth budgets:** federation runs with a configurable per-day cap (default 500MB up, 1GB down) so it doesn't dominate the user's connection.

### Layer 3: Sync protocol
The unit of sync is the **lineage edge** (Brief 017). Edges are signed, content-addressed, and small (<1KB typically).
- **Sync model:** set reconciliation. Two peers exchange Bloom filters of their edge-hash sets, then exchange the missing edges. Inspired by IPFS's bitswap.
- **Sync scope:** the user explicitly chooses what to sync. Default is "my own seeds + seeds I've explicitly imported." Power users can subscribe to a peer's full archive.
- **Sync cadence:** opportunistic. When a peer is online, opportunistic sync runs. No background polling.
- **Sync verification:** every received edge is signature-verified before being added to the local DAG. Invalid edges are dropped silently.

### Layer 4: Gossip and propagation
- **Pull-based by default**, not push. A peer asks for what it wants; nothing is forced on it.
- **Optional pubsub (v1.5)** via libp2p gossipsub for power users who want to hear about new seeds in topics they follow.
- **Topic spaces are user-defined** (e.g., "pixel-art-knights", "ambient-music-2026"). No global registry; topic discovery is again peer-to-peer.
- **Spam prevention:** rate limits per peer; reputation scoring; topic-level proof-of-work for high-traffic topics (Hashcash-style).

### Layer 5: Conflict resolution and consistency
The lineage DAG is *append-only* and content-addressed, so most operations are conflict-free (CRDT-like). Two peers that have seen disjoint subgraphs simply union them.
- **The only conflict is rotation/revocation timing.** Peer A says "key K rotated at T1"; peer B says "key K used to sign seed S at T2 > T1." Resolution: the rotation is authoritative; the post-rotation signature is invalid.
- **Eventual consistency:** all peers converge to the same DAG given enough connectivity. No global consensus required.
- **Causal ordering:** Lamport timestamps embedded in attestations; vector clocks for lineage merging.

## Federation use cases

1. **Solo creator + collaborator:** two studios federate to share an in-progress project.
2. **Studio with N seats:** a small team federates internally.
3. **Following an exemplar creator:** one-way pull of a creator's public seeds.
4. **Marketplace fanout:** marketplace listings (Brief 044) propagate via federation.
5. **Federation-as-backup:** a user runs a second studio on a home server that pulls from their primary as a backup.

## What federation is *not*

- **Not a social network.** No comments, likes, profiles. Just seeds and attestations.
- **Not a public CDN.** Peers serve only what they've explicitly chosen to publish.
- **Not consensus.** No proof-of-anything globally; no token; no chain.
- **Not anonymous by default.** Peer identities are public keys; users can run multiple identities for separation.

## Risks identified

- **Sybil attacks on the DHT:** a single attacker spawns thousands of nodes. Mitigation: DHT is opt-in; bootstrap node rotation; reputation scoring; proof-of-work for write operations.
- **Content moderation impossibility:** federation cannot enforce content rules globally. Mitigation: peers can blocklist other peers; community-curated blocklists are first-class; content provenance (Brief 008) means bad actors are identifiable.
- **Bandwidth abuse:** a malicious peer floods us with garbage edges. Mitigation: rate limits; per-peer bandwidth quotas; circuit-breaker disconnects.
- **Gossipsub spam:** topic flooding. Mitigation: per-topic proof-of-work; sender reputation; topic moderation by topic creator.
- **NAT traversal failure:** users behind strict NATs can't connect. Mitigation: TURN relays; UPnP; manual port forwarding fallback.
- **Privacy leaks:** the set of edges a peer requests reveals what they're interested in. Mitigation: cover traffic option; private information retrieval (PIR) is researched but not v1.
- **Diaspora-fail-mode:** users start with enthusiasm, abandon when their peers go offline. Mitigation: federation-as-backup pattern (sync to your own home server); studio works fully offline so no peer dependency.

## Recommendation

1. **Adopt libp2p as the federation substrate** in `architecture/federation.md`.
2. **Direct invite is the v1 discovery mechanism**; DHT is v1.5 and opt-in.
3. **Pull-based sync only at v1**; gossipsub at v1.5.
4. **Bloom-filter-based set reconciliation** is the v1 sync algorithm.
5. **Per-day bandwidth cap configurable**, default 500MB up / 1GB down.
6. **Federation is opt-in.** A studio that never federates is fully functional.
7. **Federation identities are the same key as signing identities** (Brief 042); users can run multiple.
8. **No global consensus, no token, no chain.** Federation is purely a sync layer.
9. **Community-curated blocklists** are first-class; not centrally enforced.
10. **TURN relays ship as a small community-run set**; users can configure their own.

## Confidence
**3/5.** libp2p and Bloom-filter sync are mature; the GSPL-specific lineage CRDT model is straightforward. The 3/5 reflects honest uncertainty about whether users will actually federate at all and how to bootstrap network effects without a central directory.

## Spec impact

- `architecture/federation.md` — full federation architecture.
- `protocols/federation-sync.md` — Bloom-filter set reconciliation.
- `protocols/federation-discovery.md` — invite and (v1.5) DHT.
- `protocols/federation-gossip.md` — gossipsub topic spec (v1.5).
- `architecture/federation-bandwidth.md` — quota and rate limit spec.
- New ADR: `adr/00NN-libp2p-as-federation-substrate.md`.

## Open follow-ups

- Investigate libp2p-rust vs go-libp2p for the v1 implementation. Lean Rust.
- Decide on the Bloom filter parameters (false positive rate ~0.001).
- Build the invite-string format (likely base32 with checksum).
- Plan TURN relay community ops for v1.
- Investigate PIR for v2 query privacy.
- Empirical bandwidth profiling at varying peer counts.

## Sources

- libp2p documentation and IPFS architecture.
- Maymounkov & Mazières, *Kademlia: A Peer-to-Peer Information System Based on the XOR Metric*.
- Vyzovitis et al., *GossipSub: Attack-Resilient Message Propagation in the Filecoin and ETH2.0 Networks*.
- Eppstein et al., *Set Reconciliation with Almost Optimal Communication Complexity*.
- Internal: Briefs 008, 017, 042, 044.
