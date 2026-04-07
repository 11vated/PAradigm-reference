# 031 — Memory system + exemplar feedback loop

## Question
What does the GSPL Agent's memory system look like — short-term, long-term, exemplar archive, user-history — and how does the exemplar feedback loop close so the agent gets better at producing seeds the user actually wants?

## Why it matters
A stateless agent forgets the user's preferences, repeats mistakes, and produces generic output. The competitive position GSPL wants is *the agent that remembers*. Memory + exemplar feedback is the mechanism by which the agent personalizes without retraining.

## What we know from the spec
- Brief 029 introduced the agent architecture with a "memory + exemplar archive" block.
- Brief 030 stipulated that sub-agents do not share working state — all state lives in the plan tree and the archive.
- Brief 011 (reliability) and Brief 040 (refinement loop) intersect with this.

## Findings — three memory layers

### Layer 1: Short-term (per-session working memory)

- **Scope:** A single user session with the agent.
- **Contents:** The plan tree, the executed tool calls, the candidate seeds produced, the critic scores, the user's reactions (accepted/rejected/edited).
- **Persistence:** In-process only. Wiped when the session ends.
- **Used by:** All sub-agents within the session.
- **Capacity:** Unbounded within reason; sessions are short.

### Layer 2: Long-term (per-user profile)

- **Scope:** A single user across sessions.
- **Contents:**
  - **Preferences**: explicit (saved settings) and implicit (inferred from history of accepted vs rejected seeds).
  - **Style fingerprints**: aggregated Core gene distributions over the user's accepted seeds.
  - **Vocabulary mappings**: how this user uses adjectives ("warm" might mean a specific OKLab range for one user, a different one for another).
  - **Engine affinities**: which engines this user touches most.
  - **Recent intent embeddings** for short-horizon recall.
- **Persistence:** Encrypted local file (per Brief 042 keys); optional sync to a user-controlled server.
- **Capacity:** ~10 MB cap; older entries pruned by recency × influence.
- **Used by:** Planner, Researcher, Composer.

### Layer 3: Exemplar archive (per-user library)

- **Scope:** Per-user library of seeds the user has *kept*. Plus a global pre-seeded archive of well-known reference seeds the system ships with.
- **Contents:** Full `.gseed` files plus computed metadata: Core projection, FIM diagonal (Brief 019), tags, user labels, lineage.
- **Persistence:** On-disk seed library; indexed for similarity search.
- **Capacity:** Bounded only by disk; the index is bounded.
- **Used by:** Researcher (for retrieval), Breeder (for parent selection), Critic (for novelty calculation).
- **Indexing:** A small ANN index (HNSW) over Core projections + EmbeddingGene values for fast similarity queries.

## The exemplar feedback loop

The closing of the loop is the *interesting* part of memory. Here is the cycle:

1. **User states intent.** Agent produces N candidates.
2. **User reacts**: accepts one, rejects others, optionally edits the accepted one.
3. **The accepted-and-edited seed is added to the exemplar archive** with a `provenance: user_accepted` tag.
4. **The rejected candidates are added to a *negative* archive** with their rejection reason if the user supplied one. Negative examples are weighted lower but still retrieved.
5. **The user's style fingerprint is updated** by walking the new seed's Core projection into the running aggregate.
6. **The vocabulary mapping is updated** by associating the user's adjective tokens with the actual gene values that ended up in the accepted seed.
7. **Next session, the Researcher and Planner consult the updated profile.**

This is a **personalization loop without model fine-tuning**. The model is fixed; the *retrieval and prompting* change based on the user's history. This is cheaper, faster, and more transparent than fine-tuning.

## Sharing across users (opt-in only)

- A user may choose to publish a seed to the global exemplar archive. Published seeds become available to other users' Researchers.
- Publishing requires a signed seed (Brief 004) and consent metadata.
- The user's style fingerprint and vocabulary are *never* shared automatically.
- Federation rules (Brief 043) govern cross-server exemplar sharing.

## Risks identified

- **Privacy**: per-user style fingerprints contain inferred information the user may not want exfiltrated. Mitigation: encrypted at rest with the user's key (Brief 042); never transmitted off-device unless the user explicitly publishes.
- **Filter bubble**: the agent learns to give the user only what they've liked before; novelty dies. Mitigation: novelty is a critic dimension; the Researcher mixes in deliberately-different exemplars at a tunable rate.
- **Negative archive misuse**: a user's rejection might be a one-off mood, not a real preference. Mitigation: rejection weight decays faster than acceptance weight; explicit "this was a one-off" flag.
- **Vocabulary mapping drift**: the same user uses "warm" differently in different contexts. Mitigation: vocabulary mappings are *contextual* — bound to engine + intent context, not global.
- **Index bloat**: a user with 10K seeds has a slow Researcher. Mitigation: HNSW scales fine to that size; pruning by influence handles 100K+.

## Recommendation

1. **Adopt the three-layer memory model.**
2. **Long-term and exemplar storage are local and encrypted by default.** Sync is opt-in.
3. **The exemplar feedback loop is the *only* personalization mechanism in v1.** No model fine-tuning.
4. **Negative examples are tracked separately** with faster decay.
5. **Vocabulary mappings are contextual**, not global.
6. **HNSW index over Core + EmbeddingGene** for fast similarity retrieval.
7. **Novelty mix rate** in the Researcher is configurable; default biases toward 20% deliberately-different exemplars.
8. **Federation of exemplars** is opt-in per seed and follows Brief 043 trust rules.

## Confidence
**4/5.** The retrieval-augmented personalization loop is well-trodden in production LLM systems. The 4/5 reflects the unproven assumption that this generalizes to the seed editing domain.

## Spec impact

- `architecture/agent-memory.md` — full memory architecture.
- `algorithms/exemplar-feedback-loop.md` — the loop pseudocode.
- `algorithms/style-fingerprint.md` — fingerprint computation.
- `algorithms/vocabulary-mapping.md` — adjective → gene mapping.
- New ADR: `adr/00NN-personalization-via-retrieval.md`.

## Open follow-ups

- Decide on the encryption key derivation (probably from the user's signing key, Brief 042).
- Build the HNSW index integration. Phase 1 task.
- A/B test novelty mix rates in Phase 2.
- Define the "one-off rejection" UX in the studio.

## Sources

- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*.
- HNSW algorithm (Malkov & Yashunin).
- Internal: Briefs 029 (agent), 030 (sub-agents), 042 (keys), 043 (federation).
