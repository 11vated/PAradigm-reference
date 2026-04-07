# 017 — Lineage data model: ancestry, breeding, pruning, content addressing

## Question
What is the data model for seed lineage — how are parent/child relationships, breeding operators, and ancestry chains represented, stored, queried, and pruned without ballooning storage or losing reproducibility?

## Why it matters
Lineage is the substrate for breeding, royalties, attribution, and reproducibility. If lineage is sloppy, every downstream system (marketplace, federation, evolution archives, audit trails) inherits that sloppiness. Lineage is also the most likely place for storage to explode: a popular seed with 10K descendants must not require 10K full copies of the parent.

## What we know from the spec
- `architecture/lineage.md` exists as a stub.
- `spec/01-universal-seed.md` mentions `lineage_parents` in metadata.
- Brief 005 fixed the content hash to be over the JCS canonical seed bytes (uncompressed).

## Findings — the lineage graph

**Node = seed**, identified by its content hash (Brief 005). Content addressing is the primitive; database IDs are derivative.

**Edge = breeding event**, with these fields:
- `child_id` (content hash)
- `parents` (1 or 2 content hashes for asexual or sexual breeding; 3+ reserved for future polyploid)
- `operator` (named breeding operator from a fixed registry, e.g., `mutate.gaussian.v1`, `crossover.uniform.v1`, `crossover.sbx.v1`)
- `operator_params` (small JSON-canonical blob describing the operator's settings — e.g., σ, crossover rate)
- `rng_seed` (a 32-byte seed derived from the parents' hashes via HKDF; ensures reproducibility)
- `timestamp` (creation time, wall clock; not load-bearing for proofs)
- `author` (signing key fingerprint)

**Graph shape**: a directed acyclic graph (DAG) where edges point from parent to child. Multiple children per parent are common. A node may have zero parents (genesis seed) or one or two (mutation or crossover). Cycles are forbidden by content addressing — a seed cannot reference its own hash before it exists.

**Storage model**:
- Each seed file (`.gseed`) embeds the immediate parent IDs in its LINEAGE section (Brief 015). This is the *local* view.
- A *lineage server* (optional, federated) stores the full graph for query and replay. This is the *global* view. Anyone can run one; trust is earned by signature consistency.
- The graph is content-addressed throughout: no parent reference without a hash.

**Reproducibility:**
- Given two parent seeds and an edge record, any verifier can replay the breeding operator and verify that the resulting child's content hash matches.
- The `rng_seed` is derived: `HKDF-SHA256(parent1_hash || parent2_hash || operator_id, info="paradigm-breeding-v1")`. Pure function, no entropy.
- Replay does not require the lineage server — the edge record is enough.

**Pruning and compression:**
- The lineage graph grows fast. Pruning rules:
  1. **Lineage roots** (genesis seeds) are never pruned.
  2. **Marked seeds** (manually flagged as historically important) are never pruned.
  3. **Leaf seeds** with no children and no marketplace activity may be pruned after a TTL (default 90 days).
  4. **Long linear chains** (no branching) may be compacted by storing endpoints + the operator sequence as a single "lineage segment."
- Pruning never deletes the seed file itself (those live in user storage); it only removes nodes from the lineage server's index.

**Royalty trace:**
- For royalty calculation, the lineage server walks the ancestry chain from a sold seed back to its roots, identifies the contribution of each ancestor by an attribution function, and produces a royalty split. (Detailed economics in Brief 044.)
- Attribution is bounded: chains longer than 10 hops cap at the 10-hop ancestor for royalty purposes. This bounds compute and stops gaming.

## Risks identified

- **Content hash collisions** would corrupt the entire model. SHA-256 makes this practically impossible, but the spec must pin the hash function and forbid downgrades.
- **Lineage server divergence**: two federated servers disagree on a seed's parents because of a bug or attack. Mitigation: signed edge records — every edge is signed by its author and verifiers reject unsigned edges.
- **Pruning regret**: a seed pruned today becomes important tomorrow (e.g., a viral remix). Mitigation: pruning is reversible by resubmitting the seed file; lineage edges are content-addressed and can be re-derived.
- **Royalty gaming via long chains**: a creator inserts trivial intermediate seeds to dilute attribution. Mitigated by the 10-hop cap and by attribution functions that weight by genetic distance, not hop count.
- **Polyploid breeding** (3+ parents) is forbidden at v1 but reserved. Adding it later requires no schema break because parents is already a list.

## Recommendation

1. **Adopt the DAG model above as normative.** Embed the edge schema in `architecture/lineage.md`.
2. **Content hash = SHA-256 over JCS canonical seed payload.** Pinned at v1; any change is a major version bump.
3. **Edge records are signed.** Verifiers reject unsigned edges.
4. **`rng_seed` derivation via HKDF-SHA256** with a pinned info string.
5. **Lineage server is optional**, federated, and trust-by-signature. The reference implementation ships with the studio.
6. **Pruning rules above are defaults**, configurable per server. Pruning never deletes seed files.
7. **Royalty trace caps at 10 hops** at v1.
8. **Long-chain compaction** is a server-side optimization, not a normative protocol element.
9. **Polyploid breeding reserved** but disabled at v1.

## Confidence
**4/5.** Content-addressed DAGs are well-understood (Git, IPFS). The 4/5 reflects unmeasured questions: real-world graph density, pruning effectiveness, and whether the 10-hop royalty cap is the right number.

## Spec impact

- `architecture/lineage.md` — full rewrite with the schema.
- `spec/01-universal-seed.md` — pin SHA-256 as content hash; reference the lineage spec.
- `spec/06-gseed-format.md` — confirm LINEAGE section schema.
- `algorithms/breeding-replay.md` — pseudocode for replay verification.
- New ADR: `adr/00NN-lineage-dag-and-content-hash.md`.

## Open follow-ups

- Empirically measure lineage graph density on the existing 182K-LOC codebase's archive.
- Decide whether the 10-hop royalty cap is right (revisit after Brief 044).
- Build the lineage server reference implementation. Phase 1 task.
- Decide signing key rotation policy for lineage edges (cross-reference Brief 042).

## Sources

- Git internals (DAG model, content addressing).
- IPFS Merkle DAG specification.
- Internal: Briefs 004 (signature), 005 (hash domain), 015 (file format), 044 (royalties).
