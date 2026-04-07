# 151 — Creator-facing communication of the seven axes

## Question

How do the seven structural axes (Signed, Typed, Lineage-tracked, Graph-structured, Confidence-bearing, Rollback-able, Differentiable) get translated from formal architecture language into accessible creator-facing messaging at v0.1 launch — without diluting the claim or overpromising?

## Why it matters (blast radius)

The seven-axis claim is the moat. If we ship it in academic language, creators bounce. If we ship it in marketing language, the press calls it vapor. The launch message must be honest, accessible, and structurally faithful — every claim grounded in a brief, every cut from Brief 149 acknowledged. This is the last brief of Round 6.5 because every prior brief feeds the message it codifies.

## What we know from the spec

- Brief 105 specifies launch criteria including 1k creator capacity.
- Brief 104 specifies the first-ten-minutes onboarding.
- Brief 106 specifies creator economics tier 1.
- Brief 136 names Deep Research as the v0.1 headline workflow.
- Brief 149 freezes the v0.1 scope and the explicit cuts.
- Round 6 synthesis names the seven structural axes.

## Findings

1. **Creators do not buy axes; creators buy outcomes.** The seven axes are the *why* GSPL produces better outcomes; the messaging leads with the outcome and reveals the axes only on demand.

2. **Three audiences, three messages.**
   (a) *Creators* (the 1k launch cohort) — outcome-first: "make a thing, ship a thing, own a thing."
   (b) *Press and influencers* — claim-first: "the substrate is the moat; here is what changes."
   (c) *Engineers and researchers* — axis-first: "seven structural properties, each grounded in a brief."

3. **The five outcome promises (creator-facing).**
   (a) **It works the same every time.** (Determinism + Signed + Rollback-able)
   (b) **It tells you when it's not sure.** (Confidence-bearing + Grounding floor)
   (c) **You can undo anything.** (Lineage + Rollback-able)
   (d) **It learns from your work without taking it.** (Differentiable + Federation review)
   (e) **You own what you make.** (Signed + C2PA + Creator economics tier 1)

4. **The one-sentence pitch.** *"GSPL is the first creative substrate where every artifact is signed, typed, and rollback-able — so the AI can plan deeply, the work compounds across creators, and nothing you make can be silently rewritten."* This sentence carries five of seven axes implicitly and is the headline.

5. **The one-paragraph pitch.** *"Most AI tools are black boxes that produce one-shot outputs. GSPL is a substrate: every creation is a typed, signed object with full lineage. The AI plans by composing these objects and tells you how confident it is in every step. If you don't like a result, you roll it back to any earlier state in one click. As the substrate grows, every creator's work makes every other creator's tools sharper — without anyone losing ownership of what they made."*

6. **The Deep Research demo is the headline.** Per Brief 136, the Deep Research workflow is the v0.1 plugin that showcases all seven axes in one creator-visible loop: signed source citations (Signed), typed claim objects (Typed), parent → child research lineage (Lineage), federation graph backing (Graph), confidence pills on every claim (Confidence-bearing), one-click rollback to any prior outline state (Rollback), and the underlying substrate learning from accepted research traces (Differentiable). The demo IS the seven-axis pitch in motion.

7. **Honest scope language.** Per Brief 149's 17 explicit cuts, the launch page lists in plain language what is and is not in v0.1: "v0.1 ships image, sprite, and character creation. Audio, video, and simulation are coming in v0.2 (~3 months). Mobile and multiplayer are on the roadmap." No hedging, no asterisks, no "subject to change."

8. **The substrate uplift framing for benchmarks.** Per Brief 150, external benchmarks are reported as "GSPL makes any backbone better, and the better the backbone, the better the result." Creators see this as "you're not locked to one model"; engineers see it as "the substrate is doing real work." Press sees a verifiable claim instead of a leaderboard chase.

9. **Three things we promise NOT to do.** (a) We will not silently change your work. (b) We will not train on your private creations without consent (Brief 139's procedural promotion is opt-in). (c) We will not lock you to a single model — the backbone is swappable, your gseeds are portable. These three negative promises are as load-bearing as the positive ones for trust.

10. **The constitutional fence is creator-visible.** Per Brief 097 grounding floor and the 13 non-patchable commitments, the constitutional fence is named on the launch page in one sentence: "There are 13 things the AI cannot do, ever — even if you ask. They are listed and signed; you can read them." Then we link to the actual list. Most creators will never read it; the fact that it's signed and immutable is the trust signal.

11. **First-ten-minutes message.** Per Brief 104, the onboarding ships *one* end-to-end signed creation in the first ten minutes. The narrator language during that ten minutes is the first creator-facing exposure to the axes — and uses the outcome language from finding 3, never the axis names. The axes appear in the studio UI as labels (the lineage panel says "lineage," the confidence pill says "confidence") so creators absorb the vocabulary by use, not by being lectured.

12. **The "what's different from ChatGPT/Midjourney/Sora" line.** *"Those tools give you one image. GSPL gives you a typed object with provenance, lineage, and confidence — so your second creation builds on your first instead of starting from zero."* This is the differentiation line that avoids attacking competitors directly while making the structural difference vivid.

13. **No press release before the substrate uplift number.** Per Brief 150, the headline benchmark is SWE-bench Verified substrate uplift. The launch press release does not go out until that number is measured and ≥3 percentage points over the bare backbone baseline. This protects against shipping a marketing claim that doesn't match the eval.

14. **Federation messaging is explicit and modest.** Per Brief 149, v0.1 ships with the founder as the only seeded peer; first external peer onboards within 30 days post-launch. The launch message says exactly that: "Federation is live; the network grows from 1 to N starting in your first month." Honesty here prevents the "where are the other peers?" question from becoming a credibility attack.

## Risks identified

- **Outcome-first messaging may obscure the moat from press.** Mitigation: the press version (audience b) is axis-first and links to the briefs; creators get the outcome version; the two coexist on different pages.
- **"Rollback anything" promise may be misunderstood as undo for non-substrate operations.** Mitigation: clarify in product copy — rollback is for signed gseeds, not for typing in a text field.
- **The 13-commitments list may itself become a target for legal/political pressure.** Mitigation: it's signed; changing it requires the council process (Brief 107); transparency is the defense.
- **Substrate uplift may underperform the target at first measurement.** Mitigation: per finding 13, no press until the number is in. Internal launch can still proceed with creators on the substrate-native canonical battery (Brief 134) leading.

## Recommendation

**Adopt the three-audience messaging structure: outcome-first for creators, claim-first for press, axis-first for engineers. The one-sentence pitch carries five axes implicitly. The Deep Research workflow (Brief 136) is the headline demo that shows all seven axes in motion. The launch page lists Brief 149's cuts honestly and the three negative promises (no silent changes, no consent-free training, no model lock-in). The constitutional fence is named in one sentence with the 13 commitments linked. The first-ten-minutes onboarding (Brief 104) introduces axis vocabulary by use, not by lecture. No press release until the SWE-bench Verified substrate uplift number is measured and clears the target. Federation messaging is explicit about peer count (1 at launch, growing). The headline differentiation line is "those tools give you one image; GSPL gives you a typed object with provenance, lineage, and confidence."**

## Confidence

**4/5.** The messaging structure is sound and grounded in every prior brief. The unknowns are creator response to the outcome language (testable in onboarding) and how press receives the substrate uplift framing (testable at launch). Low risk because every claim is back-stopped by an actual brief.

## Spec impact

- `gspl-reference/launch/creator-message.md` — new file with the five outcome promises, the one-sentence and one-paragraph pitches, the three negative promises, the differentiation line, the Deep Research demo script.
- `gspl-reference/launch/press-message.md` — new file with the claim-first version for press and influencers.
- `gspl-reference/launch/engineer-message.md` — new file with the axis-first version linking to Briefs 109-150.
- `gspl-reference/research/104-first-ten-minutes-onboarding.md` — cross-reference; onboarding script uses outcome language.
- `gspl-reference/research/136-deep-research-workflow-recipe.md` — cross-reference; Deep Research is the headline demo.
- `gspl-reference/research/149-v0-1-scope-finalization.md` — cross-reference; cuts list is communicated verbatim.
- `gspl-reference/research/150-external-benchmark-battery-selection.md` — cross-reference; substrate uplift framing for press.

## New inventions

- **INV-591** — *Three-audience messaging structure* (outcome-first creators / claim-first press / axis-first engineers) so the same seven-axis substrate is communicated faithfully to each without dilution or jargon.
- **INV-592** — *Vocabulary-by-use onboarding* — axis names appear as Studio UI labels during the first-ten-minutes onboarding rather than as concepts to be taught.
- **INV-593** — *Three explicit negative promises* (no silent changes, no consent-free training, no model lock-in) as load-bearing trust signals alongside the positive seven-axis claim.

## Open follow-ups

- Whether to publish a public technical whitepaper at launch (probably yes, but defer write to Round 7 launch prep).
- Exact wording of the constitutional 13-commitment one-sentence framing (defer to launch copy review).
- Whether the Deep Research demo becomes a video, an interactive walkthrough, or both (defer to launch production).

## Sources

- Brief 097 — Grounding floor and anti-hallucination test suite.
- Brief 104 — First-ten-minutes onboarding.
- Brief 105 — Launch criteria and scaling plan.
- Brief 106 — Creator economics.
- Brief 107 — Governance and constitutional amendment process.
- Brief 136 — Deep Research workflow recipe.
- Brief 149 — v0.1 scope finalization.
- Brief 150 — External benchmark battery selection.
- Round 6 synthesis — seven-axis structural claim.
