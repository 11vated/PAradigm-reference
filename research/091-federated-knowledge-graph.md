# 091 — Federated knowledge graph (the GSPL substrate brain)

## Question
What is the architecture of the **federated knowledge graph** that backs every library, every armory seed, every conversion lineage, every reference, and every user-authored gseed in GSPL — and how does it let the substrate, the agent, and every user share a coherent, queryable, lineage-traced collective memory of *everything the substrate has ever known*?

## Why it matters
Every brief in Round 4 produces signed gseeds: chemistry, physics, materials, biology, earth, astronomy, math, audio, language, culture, built world, lifestyle, psychology, characters, the armory, the conversion pipeline, the reference fetcher. These gseeds are useless if they live in isolated silos. They must compose into **one queryable, federated, lineage-bearing graph** that the agent can traverse to answer any question, ground any reference, and compose any new gseed. The knowledge graph is the substrate's brain — the structure that makes "everything composes with everything" a substrate-level guarantee rather than a marketing claim.

## What we know from the spec
- Brief 075: federated execution and identity.
- Brief 077: anonymity tiers.
- Brief 078: lineage and credit.
- Briefs 081–088, 088A, 089, 090: domain libraries, armory, pipeline, references.

## Findings — graph architecture

### 1. Nodes
Every signed gseed is a node. Nodes are content-addressed by sha256 of canonical serialization. URL patterns by domain:

- `chem://`, `phys://`, `mat://`, `fx://`, `bio://`, `earth://`, `astro://`, `math://`, `audio://`, `lang://`, `culture://`, `arch://`, `urban://`, `vehicle://`, `textile://`, `garment://`, `food://`, `psy://`, `char://`, `seed://`, `ref://`.

Every node carries:

- **Content hash** (sha256 of canonical CBOR).
- **Versioned URL** (`@vN`).
- **Signature** (Ed25519 by GSPL Foundation Identity or user identity).
- **Lineage edges** (out-edges to consumed nodes).
- **Authored-by** (creator identity, possibly stealth-addressed per Brief 077).
- **Forever-signed-by** (Brief 078 INV-303 — credit edge).
- **Cultural / copyright / trademark / care flags.**
- **Confidence scores** per measured field.
- **Federation visibility** (private / mirror-allowed / fully public).

### 2. Edges
The graph is multi-typed. Edge classes:

- `composes` — A consumes B as a substrate primitive.
- `derives_from` — A is a fork of B.
- `references` — A cites B as evidence.
- `forever_signed_by` — credit lineage to a creator (Brief 078).
- `respects` — A acknowledges a source-culture custodian for B.
- `attributes` — A names B as the original author of a referenced asset.
- `refines` — A is a higher-confidence resolution of B.
- `reconciles` — A merges multiple parents into one.
- `refutes` — A measurably contradicts B (used for science updates).
- `supersedes` — A replaces B as the recommended primitive (B remains immutable).

Edges are themselves signed and content-addressed; the graph is immutable append-only.

### 3. Storage
- **Local node:** every user runs a local node with their own keystore, cache, and graph index.
- **Federation peers:** a network of peers mirror subgraphs by topic, by author, or by federation policy.
- **Anchoring:** Brief 075 federation provides cryptographic anchoring (Merkle DAG) so the graph cannot be silently rewritten.
- **Sharding:** the graph is sharded by URL prefix and by content hash. Hot subgraphs (the armory, common library primitives) are mirrored everywhere; cold subgraphs (one user's private workspace) live only on the local node and chosen mirrors.

### 4. Query language
The agent queries the graph through a substrate-level query API:

```
SELECT char://*
WHERE composes mat://skin/*
  AND composes psy://personality/big-five/*
  AND signed_by != null
  AND fictional == true
RETURN top 20 BY breeding-affinity
```

Query types:

- **Lineage traversal** ("show me everything composed from this primitive").
- **Cousin search** ("find character gseeds with similar invariants").
- **Reverse citation** ("which gseeds cite this reference?").
- **Confidence filtering** ("only return nodes with skin confidence > 0.85").
- **Cultural filtering** ("only return nodes with full source-culture attribution").
- **Time travel** ("show the state of this subgraph as of date X").

### 5. Federation rules
- **Public mirror:** GSPL Foundation Identity nodes (the libraries, the armory, the canonical references) are mirrored across every federation peer at v1.
- **Opt-in mirror:** user-signed nodes are mirrored only when the user opts in or chooses a public visibility tier.
- **Stealth mirror:** users on Brief 077 anonymity tiers can publish through ring signatures; mirrors store the gseed without resolving the author.
- **Refusal mirror:** federation peers may **refuse** to mirror any node that violates their local moderation; the foundation namespace itself enforces the constitutional refusals (Brief 088 INV-343, Brief 089 INV-350).
- **Conflict resolution:** if two federations disagree about a node, both versions persist with `refutes`/`supersedes` edges; the user sees both and chooses.

### 6. The substrate's collective memory
Over time the graph becomes the substrate's collective memory:

- Every reference any user has fetched becomes a `ref://` node any other user can reuse.
- Every armory fork becomes a derivative node visible to anyone in that subgraph.
- Every cultural attribution becomes a respect edge that compounds into a global record of which cultures contributed which primitives.
- Every science update becomes a `refutes`/`supersedes` edge that lets users see the substrate's epistemic history.
- Every refusal becomes a public substrate commitment.

The graph is not just storage. It is the substrate's **first-person memory** and the source of its first-person voice.

### 7. Privacy contract
- User content is private by default.
- Authoring identity may be stealth-addressed (Brief 077).
- The graph stores only what is necessary to verify lineage; PII in references is metadata-stripped at ingest (Brief 089).
- Users can request **deletion of their authored nodes from federation mirrors** at any time. Mirrors are obligated to honor the request within a published SLA. The local immutable history is preserved for audit but un-mirrored.
- Lineage edges to a deleted node persist as **tombstones** so downstream gseeds remain composable, but the original content is no longer retrievable from mirrors.

### 8. Knowledge graph as the agent's working memory
The GSPL agent loads relevant subgraphs into its working context as it answers any user request. When the user says "make a Heian-era courtesan writing a letter," the agent:

1. Queries the graph for `culture://japan/heian-period`, `garment://japan/heian/junihitoe`, `arch://japan/heian-shinden-zukuri`, `audio://japan/heian-court-music`, plus relevant `char://` and `seed://` nodes.
2. Loads the matching subgraph and its lineage.
3. Composes a candidate scene using only nodes the graph proves exist.
4. Returns the result with full citation lineage.

The agent is *grounded by the graph*. It cannot hallucinate a primitive that the graph does not contain — and if it must, it surfaces the gap to the user and offers to fetch a reference (Brief 090) before continuing.

## Inventions

### INV-354: Federated content-addressed substrate knowledge graph
Every signed gseed in GSPL becomes a node in a federated, content-addressed, Merkle-anchored knowledge graph. The graph is the substrate's single source of truth and its collective memory across all peers. Novel because no creative tool ships a federated cryptographic knowledge graph as the substrate primitive layer.

### INV-355: Multi-typed edge ontology with refutes/supersedes for epistemic history
The graph supports `refutes` and `supersedes` edges that record when one node measurably contradicts or improves on another, preserving the substrate's epistemic history rather than overwriting it. Users can time-travel through the substrate's knowledge updates. Novel as a substrate-level epistemic history ledger.

### INV-356: Tombstone deletion with lineage preservation
Users can request deletion of their authored nodes from federation mirrors; mirrors honor the request within a published SLA, leaving tombstone references so downstream gseeds remain composable but the original content is no longer retrievable. Novel as a privacy-preserving substrate deletion contract that does not break composability.

### INV-357: Knowledge graph as the agent's grounding floor
The GSPL agent's reasoning is grounded in the federated knowledge graph: it cannot compose primitives the graph does not contain without surfacing the gap and fetching references. Hallucination becomes a substrate-prevented failure mode. Novel as a substrate-level anti-hallucination contract.

## Phase 1 deliverables

- **Node schema** with content addressing, signing, lineage, flags, confidence at v1.
- **Edge ontology** with all 10 edge classes at v1.
- **Local node implementation** (keystore + cache + index) at v1.
- **Federation peer protocol** with Merkle anchoring at v1.
- **Query API** with all six query types at v1.
- **Public mirror of GSPL Foundation Identity nodes** (libraries + armory + references) at v1.
- **Privacy contract with tombstone deletion** at v1.
- **Agent grounding loop** wired to the graph at v1.

## Risks

- **Federation churn.** Mitigation: Foundation Identity nodes are guaranteed-mirrored; user nodes are opt-in.
- **Storage cost at scale.** Mitigation: cold sharding + content addressing + dedup.
- **Conflict between federation peers on contested cultural material.** Mitigation: parallel versions with `refutes`/`supersedes`; users see both.
- **Deletion abuse (e.g., attempts to scrub legitimate attribution).** Mitigation: deletion removes content from mirrors but tombstones preserve the lineage edge so credit cannot be erased.
- **Query cost.** Mitigation: index hot subgraphs; query budget per agent turn.

## Recommendation

1. **Lock the node and edge ontology at v1.**
2. **Build the local node** as a substrate-level service.
3. **Define federation peer protocol** with Merkle anchoring.
4. **Mirror Foundation Identity nodes globally** at v1.
5. **Wire the agent grounding loop** as a substrate constitutional commitment — no hallucinated primitives.
6. **Publish the deletion SLA** as a substrate constitutional commitment.

## Confidence
**4/5.** The ontology is clear; federation peer protocol details and the deletion SLA are the engineering work.

## Spec impact

- `inventory/knowledge-graph.md` — new doc.
- `inventory/edge-ontology.md` — new doc.
- New ADR: `adr/00NN-federated-content-addressed-knowledge-graph.md`.
- New ADR: `adr/00NN-tombstone-deletion-with-lineage-preservation.md`.
- New ADR: `adr/00NN-agent-grounding-floor-anti-hallucination.md`.

## Open follow-ups

- Federation peer protocol details.
- Deletion SLA timing and audit format.
- Query budget calibration.
- Index hot subgraph selection.

## Sources

- Internal: Briefs 075, 077, 078, 081–088, 088A, 089, 090.
