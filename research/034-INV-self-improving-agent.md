# 034 — INV: Self-improving agent via exemplar-archive feedback

## Question
Can the GSPL Agent *improve at producing seeds for a given user* over time *without* fine-tuning the underlying language model, using only the exemplar archive, the per-user vocabulary mappings, and a small set of trainable lightweight components? What is the architecture for this self-improvement?

## Why it matters
A static agent gets a baseline score. A self-improving agent gets better the more it's used, which compounds over months and years into a personalized creative partner that's *actually irreplaceable*. No competitor has this. Every diffusion model is the same one for everyone. GSPL's typed system + per-user archive enables a different shape of personalization that doesn't require expensive retraining.

## What we are inventing and why
A *retrieval-and-routing* self-improvement loop with three trainable lightweight components: a retrieval re-ranker, a critic ensemble, and a planner policy bias. None of them is a fine-tune of the base LLM. All of them improve from user feedback signals collected in the exemplar archive and the negative archive (Brief 031).

## Findings — the three trainable components

### 1. Retrieval re-ranker

- **What it does**: Given a user intent, the Researcher fetches top-K similar exemplars from the archive (Brief 031). The re-ranker is a small model that takes (intent, exemplar) pairs and outputs a relevance score, re-sorting the K results by quality for *this user*.
- **Architecture**: A small transformer (≤ 50M params) or a logistic-regression-style model over hand-engineered features (Core distance, FIM-weighted distance, lineage proximity, user history overlap).
- **Trained on**: Pairs `(intent, exemplar, label)` where `label = +1` if the user accepted a seed derived from the exemplar, `-1` if rejected.
- **Update cadence**: Online learning — every user interaction is a labeled example. Re-ranker weights update per session.
- **Storage**: Per-user weights file, ~1 MB.

### 2. Critic ensemble

- **What it does**: Wraps the existing critic models (Brief 040) in an ensemble whose mixture weights are learned per user. Some users care about novelty; others care about polish. The ensemble learns the user's preference profile.
- **Architecture**: A linear mixture of N base critics (rule-based + learned) with weights tuned per user.
- **Trained on**: User accept/reject signals correlated with each base critic's score on the candidate.
- **Update cadence**: Online; mixture weights update after each labeled example.
- **Storage**: Per-user weight vector, ≤ 100 floats.

### 3. Planner policy bias

- **What it does**: Influences the Planner's branching decisions. The base ToT planner generates N alternatives at each step; the policy bias tilts the prior over which alternatives the planner explores first.
- **Architecture**: A bandit policy (e.g., contextual UCB1) over discrete action types: which engine to start with, which composition pattern to apply, which mutation operator to favor.
- **Trained on**: Per-action reward = downstream user acceptance signal.
- **Update cadence**: Online bandit updates.
- **Storage**: Per-user policy state, ~10 KB.

## How they compose

```
intent ──> Researcher ──> top-K candidates ──> Retrieval re-ranker ──> top-K' best for user
                                                                       │
                                                                       ▼
                                                                    Planner
                                                                       │
                                                                       ▼
                                                            Planner policy bias
                                                                       │
                                                                       ▼
                                                                  Plan tree
                                                                       │
                                                                       ▼
                                                                Sub-agents execute
                                                                       │
                                                                       ▼
                                                                 Critic ensemble
                                                                       │
                                                                       ▼
                                                              Ranked candidates
                                                                       │
                                                                       ▼
                                                                User reaction
                                                                       │
                                                                       ▼
                                                                Update all 3 components
```

The base LLM never fine-tunes. The improvement happens in the three lightweight components, which are cheap to update and easy to inspect.

## Cold start

- **New user**: Components start with neutral weights (uniform mixture, no retrieval bias, uniform bandit prior).
- **Bootstrap exemplars**: The agent ships with a small global exemplar archive (~10K seeds across the 19 v1 engines) so retrieval has something to work with on day one.
- **Convergence**: Empirically, RAG re-rankers converge to useful weights in tens to hundreds of labeled examples. Critic ensembles converge similarly. Bandits need more.

## Privacy

- All trainable components are per-user and stored locally (encrypted; Brief 042 keys).
- Weights never leave the device unless the user opts in.
- Federated learning is not part of v1; it's a Phase 3 question.

## Risks identified

- **Filter bubble**: The agent learns to give the user only what they liked before. Mitigation: novelty is a critic dimension, the bandit has an exploration term, retrieval mixes in deliberate-divergence picks (Brief 031).
- **Catastrophic forgetting**: A user's preferences shift; old data dominates. Mitigation: exponential decay on training-example weight by recency.
- **Adversarial labeling**: A user rapidly toggles between contradictory preferences. Mitigation: detect inconsistency and back off to neutral weights for that signal until it stabilizes.
- **Cold-start awkwardness**: A new user gets generic suggestions for the first hour. Mitigation: bootstrap exemplars + the explicit "preferences" UI to shortcut early labeling.
- **Local component drift across versions**: A new version of GSPL changes the critic feature space and old re-ranker weights become wrong. Mitigation: weights are versioned and migrate or reset on version bumps.

## Recommendation

1. **Adopt the three-component self-improvement architecture as a v1.5 deliverable.** Not v1, because the cold-start UX needs polish.
2. **All three components are local, lightweight, and trained online.**
3. **The base LLM is never fine-tuned at v1 or v1.5.** Saves cost, preserves portability.
4. **Bootstrap exemplar archive ships with the agent**, ~10K seeds across the 19 engines.
5. **Per-user weights are encrypted and local.** Federation is Phase 3.
6. **Novelty and exploration are first-class** to fight the filter bubble.
7. **Component versioning** matches the spec versioning discipline (Brief 018).
8. **A telemetry mode** (opt-in) lets users contribute aggregate component performance back to GSPL for spec improvement, never raw data.

## Confidence
**3/5.** The three-component design is a known-good shape (RAG re-rankers and bandits are mature). The 3/5 reflects (a) the unproven assumption that user feedback signals are dense enough in this domain to learn from, and (b) the risk of filter bubbles outweighing the gains.

## Spec impact

- `architecture/self-improving-agent.md` — full architecture document.
- `algorithms/retrieval-reranker.md` — feature and training spec.
- `algorithms/critic-ensemble.md` — mixture and update spec.
- `algorithms/planner-policy-bandit.md` — bandit spec.
- New ADR: `adr/00NN-self-improvement-without-finetuning.md`.

## Open follow-ups

- Build the bootstrap exemplar archive (10K curated seeds across 19 engines). Phase 1.
- Decide between transformer re-ranker and feature-based for v1.5.
- Build the cold-start preferences UI (Brief 048).
- Empirically measure convergence on real users in Phase 2.
- Investigate Phase 3 federated learning carefully — privacy is the dominant concern.

## Sources

- Lewis et al., *Retrieval-Augmented Generation*.
- Auer et al., *Finite-time Analysis of the Multiarmed Bandit Problem* (UCB1).
- Christiano et al., *Deep RL from Human Preferences*.
- Internal: Briefs 029, 031, 040.
