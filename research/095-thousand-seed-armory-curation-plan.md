# Brief 095 — The 1,000-seed armory curation plan

## Question

How does GSPL curate 1,000 canonical signed seeds across 17 categories (Brief 088A) — at a quality bar that makes the armory the substrate's first-person voice, not a tutorial bin — within a schedule a solo founder can actually execute, with every selection decision itself lineage-tracked and auditable?

## Why it matters

The armory (Brief 088A, INV-345) is how new users meet GSPL. It is not onboarding content. It is the substrate **speaking in its own grammar** — proving, in 1,000 examples, that the libraries (081–086H) compose into coherent, production-grade, grounded creative work across every category a creator cares about.

If the armory is mediocre, every prior brief is marketing copy. The substrate can be perfectly measured and still feel dead if the first 1,000 things a creator sees are clichés, stock-photo archetypes, or lazy compositions. Conversely, if the armory is extraordinary, every library becomes obviously alive — the chemistry primitives (081) are proven by a seed that is a burning candle with lineage-tracked wax chemistry, not by a wiki page listing alkanes.

The armory is also the substrate's **learning surface** (INV-346). Every seed carries its full composition graph. A creator forks any seed and learns by watching the substrate think. A bad armory teaches bad habits. A great armory teaches the substrate's philosophy by example.

## What we know from spec

From Briefs 088 and 088A:

- 1,000 canonical seeds, 17 categories (characters, creatures, vehicles, garments, food, architecture, tools, environments, weather, materials, fx, characters-in-action, scenes, instruments, celestial objects, abstract structures, meta-seeds).
- Every seed is a composition of signed library primitives (chem://, phys://, mat://, fx://, bio://, earth://, astro://, math://, audio://, lang://, culture://, arch://, urban://, garment://, food://, psy://, and Round 4 character/media/vehicle schemes).
- Every seed is signed under the foundation identity and carries forever-signed creator credit.
- Every seed is forkable in one click.
- Every seed carries its full composition graph as a learning surface.

From the constitutional commitments:

- No trademarked-specific named gseeds. The armory ships mechanics, not brands. The "samurai in crimson armor" is fine; "the samurai from that famous film" is not.
- No living-person gseeds.
- No sacred-restricted cultural symbols without source-culture attribution.
- Every measured value carries confidence; unknowns are unbound.

What Round 4 did *not* specify: selection criteria, reviewer rubric, category quotas, rejection protocol, schedule, or the lineage-tracking of the curation decisions themselves.

## Findings

### Finding 1: Comparable foundation-content efforts cluster around 500–2,000 curated assets at ship time

Real data from comparable efforts:

- **Blender** shipped its Open Shading Language library with ~200 curated materials at 2.80 launch; Principled BSDF examples hand-tuned by the Blender Studio (Agent 327 data).
- **Substance Source** launched with ~1,200 curated materials, expanded to 10,000+ by year three, quality-graded by in-house artists.
- **Quixel Megascans** shipped with ~8,000 scanned assets but only ~1,500 surfaced as "featured" at any time — the featured set is effectively the curated canon.
- **Godot** shipped its asset library with ~300 community-submitted assets at 3.0; quality varied and the Godot team acknowledged in retrospectives that an uncurated library hurt first-user experience.
- **Unreal Marketplace** launched with ~500 Epic-sanctioned assets; the "Epic Games Launcher Free Content" tier is today roughly 1,500 items and is treated as the de-facto canon.
- **Krita** ships with ~100 brush presets, hand-tuned, and considers those the "this is Krita's voice" set.
- **Hugging Face Diffusers** example set: ~250 curated pipelines as of 2026, each reviewed by the diffusers team for reproducibility.

**Cluster: 500–2,000 items is the sweet spot.** Below 500, the library feels thin. Above 2,000, curation quality collapses under any reasonable budget unless a full-time team owns it. GSPL's 1,000-seed target is in the right zone.

### Finding 2: Quality comes from constraint stacks, not from total count

Blender, Krita, and Substance Source all ship materials that meet a written constraint stack: PBR-valid across metalness range, dielectric sanity check, roughness in a specific distribution, no stray values, lineage from a named reference. The reason these libraries feel "professional" is not artistic genius — it is **measurable constraint compliance**. An artist cannot ship a brass material with IOR 2.8 because 2.8 is outside the published brass range; the constraint catches it.

GSPL already has constraint stacks baked into the library briefs (082–086H). The curation plan needs to formalize the **seed-level constraint stack** — the per-seed checklist that every candidate seed must pass before being signed under the foundation identity.

### Finding 3: Rejection rates at reputable curated libraries run 40–70%

Published or inferable rejection rates:

- Substance Source historical rejection rate ~55% during the curated-launch era (per ex-Adobe team communications, secondhand).
- Quixel Megascans "featured" promotion rate ~20% of scanned assets.
- Unreal Marketplace Epic-sanctioned tier accepts ~30% of submissions.
- Krita brush preset inclusion rate (hand-curated) ~50% of proposals.
- Blender demo files (the canon set) ~65% of proposals make the cut.

**Cluster: 40–70%.** GSPL should plan for a **~50% rejection rate at the composition stage** and an additional ~15% rejection at the grounding-check stage. To ship 1,000 canonical seeds, the curation pipeline must compose and evaluate roughly 2,300 candidate seeds.

### Finding 4: Solo-curator throughput for content-graded creative assets is ~3–8 per day sustainable

Anecdotal but consistent across indie game-asset studios, digital painting collectives, and curator-founder stories (Krita lead, Blender Studio lead, Godot asset-lib lead, Dwarf Fortress graphical tileset curators): a focused curator can evaluate, compose, ground, review, and sign **3–8 seeds per day sustainably**. Heroic bursts of 15–20/day collapse within two weeks.

For GSPL's 2,300 candidates → 1,000 canonical target at a sustainable 5/day, the curation phase is **~460 working days of solo-founder effort**, which is ~22 months at 5 days/week. This is obviously not acceptable. Two levers close the gap:

1. **Agent-assisted composition.** The GSPL agent composes candidates from library primitives; the founder reviews, refines, rejects. Agent composition throughput is measured in hundreds per day (the bottleneck becomes review, not composition). Realistic review throughput: ~15–25 seeds per day with agent assistance. That brings the curation phase to ~100–150 working days, or **~5–7 months solo**.

2. **Community co-curation post-foundation-seed.** The founder ships an initial **Foundation Kernel** of ~200 seeds personally, then opens co-curation to a vetted reviewer network for the remaining 800 under the governance framework (Brief 107). This brings ship-to-full-armory to **~6 months solo kernel + ~6 months federated completion = 12 months end-to-end**.

### Finding 5: Category quotas prevent silent drift

Uncurated libraries always drift toward the curator's personal taste. Substance Source is material-heavy because its curators were texture artists. Megascans is environment-heavy. Godot's asset lib is programmer-art-heavy. GSPL cannot allow the armory to drift toward the founder's taste because the substrate's credibility depends on proving it composes across **every category a creator might invoke**.

**Published quotas, enforced at review time.**

### Finding 6: Curation decisions themselves must be signed lineage-tracked gseeds

GSPL is lineage-obsessed. It would be inconsistent for the armory (the substrate's first-person voice) to ship with opaque curation decisions. Every acceptance, every rejection, every revision of a candidate seed should itself be a signed lineage-tracked gseed in the `curation://` namespace, cross-referencing the candidate seed and the reviewer's signed identity.

This means: a user can fork any armory seed and walk backward through its curation history the same way they walk backward through its composition graph. The armory is self-documenting.

## Inventions

### INV-382 — The Foundation Kernel: a 200-seed founder-signed bootstrap set

A named, bounded initial armory containing 200 seeds personally composed, reviewed, and signed by Kahlil. Structured such that:

- Every library (081–086H, 092–094) is represented by at least 5 exemplar compositions.
- Every substrate URL scheme has at least one canonical usage.
- Every constitutional commitment is exercised by at least one seed that demonstrates the refusal envelope (e.g., a near-miss candidate that failed the trademark check and the rejection gseed is published alongside).
- Kernel seeds carry a distinct `foundation-kernel` tag so users can filter for the substrate's first voice.

The Foundation Kernel is GSPL's "Krita brush set." It proves the substrate speaks. It is not the whole armory; it is the armory's first sentence.

### INV-383 — The seed-level constraint stack

Every candidate armory seed passes this stack before signing:

1. **Library primitives only.** No hand-waved values; every field traces to a signed library gseed (`chem://`, `phys://`, ..., or an `ext://` extension that has itself passed review).
2. **Dimensional consistency.** All unit-carrying fields pass the dimensional checker from INV-312.
3. **Grounding floor.** Every non-axiomatic value is either (a) a measured library primitive, (b) a confidence-scored reference from the knowledge graph (INV-357), or (c) explicitly unbound with `null`-with-confidence-zero.
4. **Constitutional envelope.** Passes all 13 commitments; rejection recorded as a signed `curation-reject://` gseed.
5. **Style invariant check.** If the seed uses `char://` or `style-adapter://`, all INV-341 invariants hold.
6. **Composition graph non-triviality.** Seeds must compose at least 3 library gseeds at depth ≥ 2. No stub seeds.
7. **Fork clarity.** A test fork must produce a sensibly modifiable object within 30 seconds of a new user clicking fork; if fork behavior is incoherent, the seed is rejected for composition-graph hygiene.
8. **Reproducibility.** Signing includes the deterministic seed hash; re-executing the composition must produce the byte-identical artifact at the same precision tier.
9. **Documentation string.** Every seed carries a one-paragraph description in plain language explaining what the seed is, what it composes from, what it cannot do, and what forks tend to be interesting.
10. **Reviewer sign-off.** A human reviewer (initially Kahlil, eventually the curator network) signs the acceptance with their identity gseed.

Every failure of the stack is itself logged as a signed `curation-audit://` gseed.

### INV-384 — Published category quotas with rebalancing discipline

Fixed category quotas for the 1,000-seed armory, published in the README, enforceable at signing time:

| Category | Quota | Rationale |
|---|---|---|
| Characters (human, non-human, stylized) | 150 | The most demanded category; must span 15 art styles × 10 archetypes minimum |
| Creatures and beasts | 80 | Covers bio:// deep composition |
| Vehicles | 80 | Proves vehicle:// v2 (Brief 094) across class, era, culture, stylization |
| Garments and textiles | 60 | Proves garment:// and culture:// × 30 traditions |
| Food and ingredients | 50 | Proves food:// composition |
| Architecture and interiors | 60 | Proves arch:// × urban:// across 40 traditions |
| Tools, weapons, everyday objects | 50 | Covers mat:// × arch:// intersections |
| Environments and landscapes | 80 | Covers earth:// × weather × seasonal |
| Weather and atmospheric events | 40 | Proves fx:// and particle substrate |
| Materials (standalone exemplars) | 40 | Proves mat:// deep composition |
| FX and particles (standalone) | 30 | Proves fx:// deep composition |
| Characters-in-action (scenes with a character) | 80 | Proves power:// × move:// × form:// composition |
| Multi-element scenes (no character focus) | 60 | Proves cross-library composition |
| Instruments and audio exemplars | 40 | Proves audio:// composition |
| Celestial and cosmological exemplars | 40 | Proves astro:// composition |
| Abstract and mathematical structures | 30 | Proves math:// composition |
| Meta-seeds (composition graphs, learning examples) | 30 | The substrate showing its own thinking |
| **Total** | **1000** | |

Quotas are published so that no category can be silently under-filled. If a category runs behind, the substrate refuses to declare "armory 1.0 shipped" until the quota is met or the quota is explicitly governance-amended (Brief 107).

### INV-385 — The curation decision lineage graph

Every curation decision is itself a signed gseed in one of:

- `curation-candidate://` — a proposed seed entering review.
- `curation-accept://` — an accepted seed, referencing the candidate and the reviewer identity.
- `curation-reject://` — a rejected seed, referencing the candidate, the reviewer, the stack rule that failed, and the reason.
- `curation-revise://` — a revision pass, referencing the prior candidate and the new candidate.
- `curation-audit://` — a retrospective audit entry, referencing a seed whose acceptance is being re-reviewed.

Any user can walk the curation graph of any armory seed the same way they walk its composition graph. The armory is self-documenting and auditable. If a bad seed ships and must be tombstoned (INV-356), the tombstone itself joins the curation graph as a `curation-audit://` with a `supersedes` edge.

### INV-386 — The agent-assisted candidate composer

A dedicated agent mode (extending the eight-subagent architecture from Brief 030) runs the **Candidate Composer**:

- Takes a category and a constraint envelope.
- Composes candidate seeds from library primitives by exploring the knowledge graph.
- Runs the full seed-level constraint stack (INV-383).
- Surfaces candidates that pass the mechanical stack for human review.
- Surfaces candidates that fail the mechanical stack to the `curation-reject://` log with reasoning.
- Never signs under the foundation identity; only human reviewers can sign acceptance.

The Candidate Composer collapses the curation bottleneck from "compose + review + sign" to "review + sign," multiplying sustainable throughput by 3–5x.

### INV-387 — The co-curator reputation system

After the Foundation Kernel ships, co-curators enter with a starting reputation of 0. Co-curator reputation is earned through:

- Accepted candidates contributing to the armory.
- Rejections upheld on audit.
- Audits flagging problems that turn out to be real.

Co-curator reputation is lost through:

- Acceptances overturned on audit.
- Constitutional violations in accepted seeds.
- Failed reviewer-judgment challenges.

At co-curator reputation ≥ threshold T1, a reviewer can sign acceptances on categories they have earned authority in. At T2, on any category. At T3, they join the governance council (Brief 107) for armory-related decisions. Reputation is itself a signed lineage-tracked gseed; it cannot be anonymously inflated and it cannot be silently stripped.

## Phase 1 deliverables

For the 12-month Foundation Kernel → Full Armory path:

**Months 0–1 — Tooling and discipline**
- Candidate Composer agent mode implemented (INV-386).
- Seed-level constraint stack encoded as executable checks (INV-383).
- Curation decision gseed schemes registered (INV-385).
- Published category quotas committed to the README (INV-384).

**Months 1–7 — Foundation Kernel (200 seeds, Kahlil solo)**
- Category target per week: ~7–8 seeds accepted, ~15–20 candidates reviewed, ~5–8 rejects logged.
- Priority category order: Characters → Creatures → Vehicles → Environments → Characters-in-action → remaining.
- Every Kernel seed gets a public composition graph walkthrough.
- Kernel ship gate: all 17 categories have ≥ 10 seeds; every library has ≥ 5 exemplars; every URL scheme has ≥ 1 canonical usage.

**Months 7–12 — Co-curator phase (800 remaining seeds, federated)**
- Co-curator onboarding via governance framework (Brief 107).
- Co-curator reputation system live (INV-387).
- Weekly rotating category focus to prevent drift.
- Audit review cadence: 10% of accepted seeds re-reviewed monthly.
- Full Armory ship gate: all 17 categories at quota; all constitutional checks green; audit sample rejection rate < 5%; first-ten-minute (Brief 104) path tested end-to-end against the full armory.

## Risks

- **Solo-founder burnout during Kernel phase.** Mitigation: hard cap of 25 seeds per week; mandatory off-weeks every 6 weeks; agent composition doing the heavy lift.
- **Category drift despite quotas.** Mitigation: weekly quota dashboard; no category can fall more than 15% behind pace without an escalation to governance.
- **Reviewer fatigue → quality drop.** Mitigation: the audit system (10% monthly re-review) catches quality drop within one cycle; audit failures reset the reviewer's authority temporarily.
- **Co-curator capture.** Mitigation: reputation requires diversity of category; no single co-curator can gate a category alone; all acceptances are public and auditable.
- **Constitutional violations sneaking through.** Mitigation: the constraint stack runs on every candidate; audits specifically sample for commitment #4 (trademark), #5 (sacred-restricted), #6 (diagnostic claims) which are highest injection risk.
- **The Kernel takes longer than 6 months.** Mitigation: the Kernel ships on **quality gate**, not date gate. If it takes 9 months, it takes 9 months; the substrate does not ship a mediocre Kernel on a deadline.
- **1,000 is the wrong number.** Mitigation: the quota is a governance-amendable parameter; if Kernel experience shows 1,200 is correct, Brief 107's amendment process covers the change.

## Recommendation

**Ship the Foundation Kernel (200 seeds) as the definition of Armory v0.1**, open co-curation for Armory v0.5 (600 seeds), and declare Armory v1.0 at the 1,000-seed published quota. Treat the Kernel as the substrate's first-voice moment; everything after Kernel is the federation speaking alongside the substrate, not on behalf of it.

Implement the Candidate Composer (INV-386) before starting Kernel work so the founder's time is spent on review, not composition.

Publish the category quotas (INV-384) and the constraint stack (INV-383) in the README before the first Kernel seed is signed, so the discipline is visible and auditable from day one.

**Adopt INV-382 through INV-387.**

## Confidence

**4/5.** Curation plans always collapse in execution somewhere. The seed-level constraint stack, category quotas, and curation-decision lineage are locked and correct. The schedule estimate (6-month Kernel, 12-month Full Armory) has ~±3 months of execution risk from solo-founder bandwidth alone. The co-curator reputation system is sound on paper but will see real stress only in practice; the audit cadence is the safety net.

## Spec impact

Round 4 Brief 088A (the canonical seed armory) gains six new inventions (INV-382..387). No constitutional commitments change. No substrate primitives change. The armory quota becomes a governance-amendable parameter subject to Brief 107's amendment process.

README must add the published category quotas, the Foundation Kernel definition, and a link to this brief.

## Open follow-ups

- Co-curator recruitment criteria beyond reputation (initial trust seeding).
- Audit sampling methodology detail (random vs stratified vs adversarial).
- Curation-decision gseed storage economics (cheap enough to keep forever? tombstone policy for rejects?).
- Whether `curation-reject://` gseeds should be visible to the rejected candidate's author only or public by default.
- How Foundation Kernel relates to the Brief 104 first-ten-minute experience (the 200 Kernel seeds probably anchor the first 10 minutes).

## Sources

- Substance Source curation retrospectives (community postmortems, secondhand).
- Quixel Megascans featured-tier promotion rates (public marketing + community analysis).
- Blender Studio demo file lineage (Blender Foundation blog archive).
- Godot asset library postmortem threads on the Godot forums.
- Krita brush preset inclusion history (Krita development logs).
- Hugging Face Diffusers example pipelines repository.
- Unreal Marketplace Epic-sanctioned tier documentation.
- Round 4 Briefs 088, 088A for armory definitions.
- Round 4 Brief 091 for knowledge graph grounding floor (INV-357).
- Round 4 Brief 107 (forthcoming) for governance amendment process.
