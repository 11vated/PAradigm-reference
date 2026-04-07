# 143 — Differentiable action learning recipe

## Question

How does the kernel actually learn from signed tool calls (Brief 128, INV-526), and what is the end-to-end recipe — from signal extraction to LoRA update to promotion gate?

## Why it matters (blast radius)

Differentiable action learning is the seventh structural axis. It is what makes GSPL's tools self-improving in ways no other agent system has. Brief 128 declares the capability; this brief specifies the concrete recipe. Without a written recipe, Round 7 has to invent it inline, which risks regressions, broken signal extraction, and a quietly-disabled differentiable axis.

## What we know from the spec

- Brief 128 (INV-526) declares differentiable action learning as a v0.4+ capability with cold-start v0.1.
- Brief 129 specifies signed tool calls as one of the five free training signals.
- Round 6 deferred the recipe; this brief writes it.

## Findings

1. **The signal: a signed tool call carries a downstream quality grade.** Every `tool-call://` gseed has a parent edge to its enclosing turn, which has a parent edge to its enclosing session, which carries an outcome label (accepted / rolled-back / cleared-grounding-floor / failed-constitutional-fence). This implicit grading is the training signal — no human labeling needed.

2. **Action embeddings live in a small adapter on top of the kernel hidden state.** The kernel produces, for each tool call, a hidden state $h \in \mathbb{R}^{d}$. An action adapter $f_\theta: \mathbb{R}^d \to \mathbb{R}^{d_a}$ projects to a small action embedding (say $d_a = 64$). The action embedding is the differentiable representation that learning targets.

3. **Loss: contrastive over outcome classes.** Tool calls that led to accepted outcomes are positives; tool calls that led to rolled-back or constitution-violating outcomes are negatives. Contrastive (InfoNCE) loss over the action embedding pulls accepted-tool embeddings toward each other and pushes rejected-tool embeddings away.

4. **Why contrastive and not direct reward.** Direct reward (REINFORCE / PPO) requires reward shaping that we cannot reliably provide for the wide tool surface. Contrastive learning needs only the *relative* outcome ordering (accepted > none > rolled-back > constitution-violated), which is naturally produced by the substrate.

5. **Adapter scope: the action adapter is creator-local.** Per Brief 129's LoRA composition, the differentiable action layer is the *creator* tier of the four-tier composition (base + namespace + creator + task). It learns each creator's specific tool-use preferences without contaminating the base or namespace layers.

6. **Update cadence: weekly DPO + monthly verifier alignment.** Weekly DPO (Brief 129's weekly cadence) updates the action adapter on the previous week's signed tool calls. Monthly cadence runs a verifier alignment check: for each tool, does the learned action embedding correctly cluster the accepted-vs-rejected examples held out from training? If not, that tool's slice of the action adapter is rolled back.

7. **Cold start v0.1: the action adapter is initialized to identity.** No learning happens at v0.1 launch; the differentiable axis is *enabled* (the data is being collected and signed) but the adapter does not yet update. The first weekly DPO fires after ≥7 days × ≥50 tool calls × ≥80% acceptance ratio. This guarantees the first update has real signal.

8. **v0.4+: full differentiable mode.** Per Brief 131's release arc, v0.4 is when differentiable action learning becomes the default. At v0.4, the action adapter has been collecting signal for a year and the recipe is mature enough to be on by default.

9. **Privacy: action embeddings stay creator-local.** The action adapter never leaves the creator's machine unless explicitly federated. Federation publishes the *learned action embedding centroids*, not raw tool calls, and only with creator consent. This is the privacy-preserving analog of federated learning over the action space.

10. **Promotion gate for the action adapter:** any new weekly version must clear (a) Spearman ρ ≥0.7 between learned action embedding similarity and outcome label, AND (b) zero new constitutional fence violations on the held-out 20% slice. Otherwise auto-rollback to the previous week's adapter.

11. **Recipe summary in pseudocode:**

```
each week:
    triples = collect signed tool calls from past 7 days
    if len(triples) < 50: skip
    pos = [t for t in triples if t.outcome == accepted]
    neg = [t for t in triples if t.outcome in (rolled_back, fence_violated)]
    if len(pos) < 0.8 * len(triples): skip
    loss = contrastive_loss(action_adapter(pos.h), action_adapter(neg.h))
    new_adapter = train(loss, lr=1e-5, epochs=3)
    if (spearman(new_adapter, holdout) >= 0.7
        and constitutional_violations(new_adapter, holdout) == 0):
        sign_and_promote(new_adapter)
    else:
        rollback()
```

## Risks identified

- **Sample efficiency.** 50 tool calls per week is low; learning from such small sets is unstable. Mitigation: pool tool calls across the past 4 weeks for the contrastive loss; maintain weekly cadence on adapter updates.
- **Distribution shift in tool surface.** New tools added during a week have no positive history. Mitigation: new tools start at the action-adapter identity (no learned offset) and only get learned offsets after 30 calls of history.
- **Cross-creator contamination via federation.** If centroids are published carelessly, they leak creator workflows. Mitigation: publish only k-anonymity-aggregated centroids (≥10 creators per centroid) and only with creator opt-in.

## Recommendation

**Implement differentiable action learning as a creator-tier LoRA adapter on the kernel hidden states with InfoNCE contrastive loss over signed tool-call outcome classes (accepted / none / rolled-back / fence-violated). Update weekly under Brief 129's cadence; require ≥7 days × ≥50 calls × ≥80% acceptance to fire the first update. Promotion gate: Spearman ρ ≥0.7 on held-out 20% slice AND zero new fence violations, otherwise auto-rollback. Privacy: adapter stays creator-local; federation publishes only k≥10 anonymized centroid aggregates with explicit consent. v0.1 ships with collection-only (data flowing, adapter at identity); v0.2 enables creator-private learning; v0.4 becomes default as per Brief 131 release arc.**

## Confidence

**3.5/5.** The mechanics are standard contrastive-learning practice; the GSPL-specific bits (signed outcome labels as the supervision signal, four-tier LoRA composition) follow from prior briefs. The 3.5/5 reflects that v0.1 ships collection-only — the actual learning happens after 7+ days of telemetry, so we will not know how well it works until v0.2.

## Spec impact

- `gspl-reference/intelligence/differentiable-actions.md` — new file with the full recipe, contrastive loss formula, promotion gate, privacy protocol.
- `gspl-reference/research/128-gspl-tool-use-and-modifier-surface.md` — cross-reference at INV-526.
- `gspl-reference/research/129-gspl-self-improvement-loop.md` — cross-reference at the weekly DPO cadence.
- `gspl-reference/research/131-gspl-differentiable-reasoning-substrate.md` — cross-reference at the v0.4 release arc row.

## New inventions

- **INV-577** — *Contrastive action learning over signed outcome classes.* The substrate's free outcome labels (accepted / rolled-back / fence-violated) are the supervision signal; no human reward shaping needed.
- **INV-578** — *k-anonymity-aggregated action centroid federation.* Creator-local action adapters can share learned structure across the federation without leaking individual workflows; only k≥10 aggregated centroids cross the federation boundary.

## Open follow-ups

- Whether 50 calls/week is the right minimum (telemetry-tuned in Round 7).
- Whether to publish the v0.2 creator-private adapter as a model gseed (almost certainly yes).
- How to handle creators with very low tool-call volume (likely: skip differentiable learning entirely for them, fall back to base adapter).

## Sources

1. Oord et al., *Representation Learning with Contrastive Predictive Coding*, 2018 (InfoNCE).
2. Chen et al., *A Simple Framework for Contrastive Learning of Visual Representations (SimCLR)*, ICML 2020.
3. Brief 128 — GSPL tool-use and modifier-surface intelligence.
4. Brief 129 — GSPL self-improvement loop.
5. Brief 131 — GSPL as a differentiable reasoning substrate.
