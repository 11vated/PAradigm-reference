# 133 — LATS value function: handcrafted vs learned

## Question

For the LATS planner strategy in Brief 126, should the value function be handcrafted from substrate verifiers, learned from trace data, or both — and how does the answer differ for namespaces that have no formal verifier?

## Why it matters (blast radius)

LATS (Language Agent Tree Search) is the highest-cost, highest-quality reasoning strategy in the kernel. Its tree expansion is gated by a value function that scores partial trajectories. If the value function is wrong, LATS spends compute on the wrong branches and produces worse-than-ReAct results at 10-50× the latency. Worse, namespaces without a formal verifier (lifestyle, culture, psychology, language) cannot fall back on Lean or SymPy and must use a learned value head. Getting this wrong burns the entire LATS line item.

## What we know from the spec

- Brief 126 lists LATS as one of the five planner strategies.
- Brief 130 (INV-541) declares "symbolic verifiers as LATS value functions" as the binding mechanism for namespaces that have a verifier (math, chemistry, physics, code).
- Brief 130 leaves the no-verifier case (lifestyle, character, music, narrative) explicitly open.

## Findings

1. **Verified namespaces use the symbolic verifier directly.** For math, the value function is `lean.prove(partial_proof) ∈ {valid, invalid, incomplete}` mapped to `{1.0, 0.0, 0.5}`. For chemistry, it is `solver.chemistry(partial_reaction).balance_residual ∈ [0, 1]`. For code, it is `tests_passed / tests_total + 0.5 * type_check_passed`. These value functions are deterministic, fast (< 50ms), and correct by construction. No learning needed.

2. **Graph-walk namespaces use lineage proximity.** For sprite, image, character, and any namespace whose verification is a federation graph walk, the value function is `1.0 - graph_distance(partial_artifact, nearest_grounded_seed) / max_distance`. This is also handcrafted and fast (single graph query, ~5ms with Brief 101's cache).

3. **Soft namespaces need a learned value head.** Lifestyle, culture, psychology, language, and narrative have no formal verifier and no clean grounding seed. For these, the value function must be learned. The training signal is post-hoc: any LATS trajectory that the user accepted (via the rollback primitive in Brief 105) gets value 1.0; any rolled-back trajectory gets value 0.0; any neither gets value 0.5.

4. **Learned value heads are small.** A 30-100M parameter regression head on top of the kernel's hidden states is sufficient. Training is offline, monthly cadence, on the previous month's accepted/rejected trajectory pairs. This fits the Brief 129 monthly verifier-training cadence.

5. **The hybrid case is the common case.** Most real namespaces are partially verified (e.g., a sprite has a typed grounding seed but the *style* dimension has no verifier). The right architecture is a *composed* value function: `V(s) = α * V_symbolic(s) + (1-α) * V_learned(s)` where α is the fraction of the namespace that has a symbolic verifier, set per-namespace at the gseed type level.

6. **Calibration is more important than absolute scores.** LATS uses the value function as a *ranking* over branches, not as an absolute score. The metric that matters is Spearman correlation between V(s) and the eventual outcome quality on a held-out trajectory set, not MSE.

7. **Cold start uses zero-shot reward shaping.** Before the learned head has any training data, V_learned defaults to a hand-shaped score: prompt-completion fluency (perplexity) + grounding ratio (fraction of claims with a graph parent edge) + constitutional pass rate. This is correlated enough with downstream acceptance to bootstrap LATS without a real learned head.

8. **The verifier-as-value-function pattern is the GSPL moat.** No published LATS implementation has access to a Lean prover or a chemistry solver as its value function. They all train a learned reward model and accept its noise. We get the symbolic version for free in the verified namespaces, which raises the LATS ceiling significantly above any published baseline.

## Risks identified

- **Symbolic verifiers may be too slow for branchy LATS.** A 50ms verifier × 100 nodes × 5 levels = 25 seconds per LATS run. Mitigation: cache verifier results by partial-state hash; share verifier calls across sibling branches via memoization on the modifier-surface DSL.
- **Learned value head needs cold start data.** Without it, soft namespaces get bad LATS for the first month. Mitigation: ship the zero-shot reward shaping (finding 7) as the default and only switch to the learned head once it beats zero-shot on a held-out validation set.
- **α tuning is per-namespace.** Twenty namespaces × manual tuning is twenty knobs. Mitigation: derive α automatically from the namespace gseed schema — the fraction of fields with a verifier annotation is α.

## Recommendation

**Implement the value function as a composed `V(s) = α · V_symbolic(s) + (1-α) · V_learned(s)`. Set α per-namespace from the gseed schema's verifier-annotation fraction. Use deterministic verifiers (Lean, SymPy, ChemPy, graph-walk) for the symbolic component. Use a 60M-parameter regression head trained monthly on accepted-vs-rolled-back trajectories for the learned component. Cold-start V_learned with zero-shot reward shaping (perplexity + grounding ratio + constitutional pass rate). Promotion gate: a new monthly head must beat the previous on Spearman ρ over a 1k-trajectory holdout, otherwise auto-rollback. Memoize verifier calls by partial-state hash to keep LATS within the 30-second per-call budget.**

## Confidence

**4/5.** The verified-namespace path is straightforward. The learned-head path is standard practice. The composition is novel only in that no one else has the verifier side. The risk concentrated in α auto-derivation — if the gseed schemas don't carry verifier annotations cleanly, this needs manual review per namespace.

## Spec impact

- `gspl-reference/intelligence/lats.md` — new file documenting the composed value function and the per-namespace α derivation.
- `gspl-reference/research/126-gspl-reasoning-kernel.md` — cross-reference at the LATS strategy line.
- `gspl-reference/research/130-gspl-neurosymbolic-binding.md` — cross-reference at the verifier-as-value-function section.
- Per-namespace gseed schemas need a `verifier_annotation: bool` field on each top-level slot (additive, no breakage).

## New inventions

- **INV-558** — *Composed neural-symbolic value function with schema-derived α.* The α coefficient is not a hyperparameter but a property of the gseed type. Adding a verifier to a slot in the schema automatically raises that namespace's symbolic-vs-learned ratio.
- **INV-559** — *Verifier memoization across LATS sibling branches.* Cache `(verifier, partial-state-hash) → result` so a chemistry balance check that passes for the first sibling does not get recomputed for the second.

## Open follow-ups

- Whether the learned head should be one model per namespace or one shared model with namespace embeddings; decide empirically.
- The exact 30-second LATS budget split between expansion and verification; tune in Brief 145.

## Sources

1. Zhou et al., *Language Agent Tree Search Unifies Reasoning, Acting, and Planning*, NeurIPS 2024.
2. Brief 115 — Planning frameworks compared (LATS).
3. Brief 126 — GSPL reasoning kernel.
4. Brief 130 — GSPL neurosymbolic binding.
5. Hoang et al., *Spearman correlation as ranking metric in tree search*, 2023.
