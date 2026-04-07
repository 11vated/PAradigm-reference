# Brief 100 — Federation peer protocol details

## Question

How do GSPL federation peers gossip gseeds, resolve conflicts, score reputation, resist sybils, handle node outages, propagate constitutional refusals, and reconcile forked federation state — such that Brief 043's federation protocol and Brief 091's federated knowledge graph become an operational multi-peer system?

## Why it matters

Federation is the difference between GSPL as a centralized service and GSPL as a living substrate. The federation architecture was defined in Brief 043 and extended in Brief 091 with content-addressed nodes and a 10-edge ontology. What was not specified: the wire protocol, the gossip semantics, the conflict-resolution UX, and the reputation model that makes the federation resist bad actors without becoming a gated club.

## What we know from spec

- Content-addressed node IDs (INV-354).
- 10-edge ontology including `refutes` and `supersedes` (INV-355).
- Tombstone deletion preserving lineage (INV-356).
- Grounding floor as the agent's truth contract (INV-357).
- Forever-signed-by edges for credit lineage.

## Findings

### Finding 1: Gossip-with-anti-entropy is the proven baseline

Distributed system literature (Amazon Dynamo, Cassandra, Riak, Scuttlebutt, IPFS) converges on gossip-with-anti-entropy as the robust baseline for eventually-consistent content-addressed stores. GSPL should not invent a new protocol; it should adopt gossip-with-anti-entropy and customize the edge ontology on top.

Key properties:

- Each peer maintains a Merkle-DAG-like view of the content-addressed graph.
- Peers periodically gossip summaries (bloom filters or Merkle roots) with a random subset of known peers.
- Diffs flow toward the newest or the longest chain of signed edges.
- Anti-entropy rounds reconcile gaps on a slower cadence (every 15 min by default, configurable).

### Finding 2: Content-addressed deduplication is automatic

Because every gseed's ID is a hash of its canonical form, deduplication is free. A peer receiving a gseed it already has simply no-ops. This matters because federation growth is limited by new content, not by duplicate traffic.

### Finding 3: Conflict-resolution for content-addressed stores reduces to edge conflicts, not node conflicts

Two peers cannot produce different versions of the same gseed (content-addressed means the content *is* the ID). They can, however, produce conflicting **edges**:

- Peer A says `seed_X refutes seed_Y`.
- Peer B says `seed_X supersedes seed_Y`.
- Peer C says `seed_X composes seed_Y`.

Edge conflicts are preserved, not resolved. Both edges are stored with their signers. The UX surfaces them as "this seed is characterized differently by different federation members." The agent's grounding floor treats conflicting edges as ungrounded until the user picks a perspective.

### Finding 4: Sybil resistance works via proof-of-authorship cost, not proof-of-work

GSPL peers are identified by their signing key, not by work. A sybil attacker can spin up arbitrary keys. The defense is that **only signed content-addressed gseeds count for reputation**, and signing takes effort (compose, ground, review). A peer can flood the network with junk gseeds, but junk gseeds earn no reputation and can be tombstoned by the network through the `supersedes` edge with reasoning.

Additionally, the co-curator reputation system (INV-387) and the consultancy network (INV-408) create separate reputation tracks that sybils cannot cheaply colonize.

### Finding 5: Constitutional refusal propagation requires explicit edges

When one peer refuses to host a gseed under its constitutional interpretation, other peers need to know. The `refuses` edge is added to the ontology:

- `peer_X refuses seed_Y reason: commitment_4_trademark`

Other peers see this refusal and can decide independently whether to also refuse. The substrate's 13 core constitutional commitments are non-optional at the foundation namespace level, so a foundation peer MUST propagate any refusal tagged with a core commitment. A creator-namespace peer can choose to host content that the foundation refused, clearly flagged as `creator-namespace-only`.

### Finding 6: Node-outage recovery is handled by caching and re-gossip

A peer coming back online runs anti-entropy against its neighbors, learning what it missed. This is classic Dynamo-style recovery. For GSPL, the discipline is that **any gseed that was previously reachable must remain reachable as long as one online peer holds it**. The federation's redundancy target: every signed gseed replicated to ≥ 5 peers by default, ≥ 9 peers for Foundation Kernel content.

## Inventions

### INV-414 — Gossip protocol with Merkle-root summaries

GSPL federation peers exchange Merkle roots of their content-addressed views every 5 minutes with a random subset of 3 known peers. A mismatch triggers a pull of the diff. Full anti-entropy runs every 15 minutes. Protocol parameters (intervals, fanout, peer subset size) are governance-configurable.

### INV-415 — Edge-conflict preservation, not resolution

Conflicting edges from different signers are stored together. Queries against the graph return all conflicting edges with their signers and reasoning. The agent's grounding floor downgrades grounding confidence when querying a seed whose characterization has conflicting edges, and the studio UI shows the conflict as a first-class feature, not a warning to hide.

### INV-416 — Peer reputation from signed content and honored refusals

Peer reputation is computed from:

- Signed gseeds authored and not tombstoned (positive).
- Signed reviews confirmed by audit (positive).
- Signed refusals that were upheld across the network (positive).
- Gseeds tombstoned for constitutional violations (negative).
- Unhonored foundation-level refusals propagated by the peer (negative — a peer that ignores constitutional refusals loses reputation).

Reputation is itself a signed `peer-reputation://` gseed updated periodically and visible to all peers.

### INV-417 — The `refuses` edge for constitutional propagation

New edge type added to the ontology (taking the ontology from 10 to 11 edges):

- `refuses` — peer X refuses seed Y for reason R. Foundation-level refusals (commitments 1–13) MUST propagate; creator-level refusals MAY propagate.

The refusal edge becomes part of the lineage graph. Users can see every seed that has been refused, by whom, and why. Constitutional transparency becomes an emergent property of federation.

### INV-418 — Replication targets and quorum

Default replication target: every signed gseed on ≥ 5 peers, Foundation Kernel content on ≥ 9 peers. When a query's grounding depends on a seed with fewer than the target replications, the agent downgrades grounding confidence and surfaces the replication status to the user.

### INV-419 — Fork-and-reconcile semantics for creator namespaces

Creator namespaces (non-foundation signed content) can fork freely. Forks are tracked via the `refines` edge. When two creator forks of the same upstream seed diverge significantly, the federation presents both to users without picking a winner. Users choose which fork to compose against.

### INV-420 — Network-level tombstone ratification

A single peer can propose a tombstone for a constitutionally violating seed. The tombstone becomes binding on the foundation namespace when ratified by:

- A governance council majority (Brief 107), OR
- A peer-weighted quorum where ≥ 2/3 of reputation-weighted peers honor the proposed tombstone within 72 hours.

Tombstones preserve lineage per INV-356; the seed's content is removed but the tombstone, the reasoning, and the `supersedes` or `refutes` edges remain.

### INV-421 — The peer onboarding handshake

A new peer joining the federation presents:

- Their signing key.
- Their constitutional posture (foundation-level or creator-only namespace).
- Their initial peer list.
- A signed acknowledgment of the 13 core constitutional commitments (required for foundation-level peers; creator-only peers acknowledge a reduced set).

Peers that refuse the handshake or deviate from core commitments are quarantined — the network accepts gseeds from them only in creator namespace and does not replicate them for foundation-level queries.

## Phase 1 deliverables

**Months 0–4**
- Gossip-with-anti-entropy baseline implementation.
- Content-addressed dedupe confirmed operational.
- First two peers running (Kahlil's primary + a test peer).

**Months 4–8**
- Edge-conflict preservation in storage.
- The `refuses` edge added to ontology.
- Replication target enforcement with status surfacing.
- Peer reputation signed gseeds.
- Third and fourth peers joined for real multi-peer testing.

**Months 8–12**
- Fork-and-reconcile UX in studio (Brief 103).
- Network-level tombstone ratification first trial (hypothetical seed).
- Peer onboarding handshake live.
- First five real peers in production federation.

## Risks

- **Protocol bugs leading to gseed loss.** Mitigation: content-addressing means loss is recoverable as long as any peer holds the data; replication target of 5/9 peers gives margin.
- **Reputation gaming.** Mitigation: reputation is computed from audited outcomes, not self-reporting; sybils don't accumulate real authored content.
- **Constitutional refusal ignored by creator-only peers.** Mitigation: foundation-level grounding queries only trust foundation-level peers; creator-only peers are visible but do not ground against core commitments.
- **Federation fracture from unresolved edge conflicts.** Mitigation: conflicts are preserved not resolved; the UX makes conflict visible rather than hiding it.
- **Slow anti-entropy under load.** Mitigation: parameters are tunable; peers can choose intervals within governance-set bounds.

## Recommendation

**Adopt INV-414 through INV-421.** Use gossip-with-anti-entropy as the baseline; do not invent a new protocol. Preserve edge conflicts as a feature of the substrate rather than a bug to resolve. Ship with two peers (founder + test), expand to five real peers by year end under governance review.

## Confidence

**4/5.** The protocol baseline is well-proven. The main risk is in the specifics of reputation weighting and refusal propagation, which will only be stress-tested once a real multi-peer network exists. Parameters are governance-tunable.

## Spec impact

Brief 043 and 091 gain eight new inventions (INV-414..421). The edge ontology grows from 10 to 11 edges with the addition of `refuses`. No substrate primitives change. Commitment #8 (grounding floor) gains federation-level enforcement via replication targets and peer reputation.

## Open follow-ups

- Wire protocol format (likely libp2p or a subset).
- Cryptographic key rotation for long-lived peers.
- Bandwidth budgets for gossip and anti-entropy under growth.
- Geographic distribution and regional latency.
- Legal jurisdiction for peers in different countries.

## Sources

- Dynamo, Cassandra, Riak distributed store papers and retrospectives.
- Secure Scuttlebutt peer-to-peer protocol documentation.
- IPFS and libp2p gossip and content-addressing literature.
- Merkle-DAG and anti-entropy algorithm research.
- Round 2 Brief 043 for federation protocol baseline.
- Round 4 Brief 091 for content-addressed knowledge graph.
