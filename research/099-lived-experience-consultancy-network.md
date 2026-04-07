# Brief 099 — Lived-experience consultancy network

## Question

How does GSPL operate a consultancy network covering mental health depiction, clinical conditions, sacred/restricted cultural symbols, marginalized-community representation, and disability representation, such that the care contracts from Briefs 086E, 086H, and 088 become real human review — not a policy page?

## Why it matters

Constitutional commitments #5 (sacred-restricted cultural symbols), #6 (diagnostic claims), and the mental health depiction care contract (INV-339) cannot be enforced by automated checks alone. They require humans with lived or professional expertise reviewing affected gseeds, saying yes, saying no, asking for changes, and signing their review. Without a real consultancy network, the care contracts become performative and the substrate's credibility with the communities it claims to respect collapses.

## What we know from spec

- INV-333: sacred/restricted respect contract.
- INV-339: mental health depiction care contract.
- INV-343: no living-person gseeds in foundation namespace.
- Brief 086E: culture substrate with source attribution.
- Brief 086H: psychology substrate with care contracts.
- Brief 088: character canon with identity embedding from synthetic-only data.

Missing: who the consultants are, how they're recruited, compensated, how their reviews become lineage-tracked gseeds, how conflict is resolved, and how the network scales without becoming either bureaucratic or tokenistic.

## Findings

### Finding 1: Compensation must be real or the program is exploitative

Research on marginalized-community consultancy in tech (AI ethics consultancies, sensitivity reader programs in publishing, indigenous data sovereignty work) converges: unpaid or token-pay review programs attract either (a) people already employed by privileged institutions or (b) nobody. A real consultancy network pays market rate for the expertise, plus a retainer for availability.

Market rate benchmarks:

- Publishing sensitivity readers: $250–$800 per manuscript (2024 rates).
- AI ethics consultants: $150–$400/hour.
- Clinical psychology consultants for creative projects: $200–$400/hour.
- Indigenous data sovereignty consultants: often structured as community grants ($2K–$10K per engagement).

GSPL should plan a **compensation floor** at professional-equivalent rates.

### Finding 2: Conflict between consultants must be adjudicated, not averaged

Two consultants on the same material can disagree. Publishing houses handle this by deferring to the more senior or more affected consultant; AI ethics work handles it by escalating to a governance body. GSPL should handle it by making both reviews visible as signed gseeds with a governance-council adjudication when binding.

Never average disagreement. Never hide dissent. Users see both reviews and know why the substrate made the call it made.

### Finding 3: Consultancy domains must be mapped to specific substrate-layer triggers

Not every gseed needs review. Most don't. Consultancy engagement must be triggered by specific substrate patterns:

- Any gseed composing `culture://` with a `sacred:true` or `restricted:true` flag → source-culture consultant review mandatory.
- Any gseed composing `psy://` with clinical-condition references → mental health consultant review mandatory.
- Any gseed composing `char://` with a declared disability or marginalized-identity feature → relevant lived-experience consultant review mandatory.
- Any armory seed in the Foundation Kernel touching any of these → review mandatory before signing.
- User-created gseeds in creator namespace → review optional, but the substrate offers to route them for review with the user's consent and compensation.

The review trigger is automatic. The review itself is human.

### Finding 4: Network size should be redundant, not minimal

A network with one consultant per domain fails when that consultant is unavailable. Minimum redundancy: **three consultants per domain**, rotating, with clear refusal/recusal paths. This matters because a solo consultant can be leveraged ("you're the only voice for X community, your approval is required"), which is both unfair to the consultant and structurally fragile.

### Finding 5: The consultancy must hold authority over the substrate, not just review it

A consultancy that can only advise is a consultancy that will be ignored when the founder is busy. A consultancy that can **block** the signing of specific gseeds under the foundation identity has real authority. GSPL's structure should grant consultants signature-blocking authority in their domain, overridable only by a governance-council supermajority (Brief 107), and every override is public.

## Inventions

### INV-407 — Domain-triggered consultancy review

Automatic consultancy triggers encoded in the constraint stack (INV-383):

| Trigger pattern | Consultancy domain | Minimum reviewers |
|---|---|---|
| `culture://` flagged sacred/restricted | Source-culture | 1 from source community + 1 cultural steward |
| `psy://` with clinical-condition reference | Mental health | 1 clinical professional + 1 lived-experience |
| `char://` with declared disability feature | Disability representation | 2 from relevant community |
| `char://` with marginalized-identity feature | Marginalized-community representation | 2 from relevant community |
| Near-miss trademark/living-person risk | Legal/ethics | 1 legal + 1 ethics |

Triggers fire automatically; a seed cannot be signed under foundation identity without the required consultancy gseeds attached.

### INV-408 — The consultancy registry

A signed `consultancy-registry://` gseed listing every consultant with:

- Anonymous or named (consultant's choice).
- Domains of expertise.
- Lived or professional credential.
- Availability tier (active, on-call, on-break, retired).
- Compensation rate or grant structure.
- Signature-blocking authority scope.
- Review count and outcome summary (aggregate, never individual).
- Contact path (through GSPL liaison, never direct unless consultant requests).

The registry is public in structure but can anonymize individuals if they prefer.

### INV-409 — The review-as-gseed contract

Every consultancy review produces a signed `consult-review://` gseed with:

- Candidate seed hash under review.
- Reviewer identity gseed.
- Review state (approve / approve-with-conditions / block / recuse).
- Written reasoning (publishable or private).
- Conditions if approve-with-conditions (specific modifications required).
- Cross-references to prior similar reviews by the same consultant.
- Lineage to the `consult-trigger://` gseed that caused the review.

Reviews are immutable once signed. Retrospective re-review is a new `consult-review://` with a `supersedes` edge.

### INV-410 — Compensation ladder with retainer floor

Three compensation structures:

1. **Per-review rate** — for ad-hoc triggered reviews. Published floor rates: $250 for small seeds, $500 for complex seeds, $1000+ for seeds requiring multi-session consultation. Rates are public.
2. **Retainer** — for consultants on active availability tier, a monthly retainer ($1K–$3K/month) plus reduced per-review rates, in exchange for guaranteed response windows.
3. **Community grant** — for source-culture work where the community prefers a grant over individual compensation, structured payments to a community organization or program rather than individuals.

Consultants choose their compensation structure.

### INV-411 — Block-and-override governance

A consultancy block on a gseed under foundation identity is binding unless overridden by:

- A governance-council (Brief 107) vote at supermajority (≥ 2/3).
- Public reasoning posted for the override.
- The original block review and the override review both visible permanently.
- The consultant whose block was overridden notified before publication.

Historical overrides are tracked. An override rate above a threshold (e.g., 15% of blocks) triggers a governance review of the override pattern itself.

### INV-412 — Recusal and conflict-of-interest discipline

Consultants must recuse from reviews where they have:

- Personal financial interest in the outcome.
- Prior relationship with the seed's creator.
- A history of public disagreement with the subject matter at a level that prevents fair review.

Recusal is signed (`consult-recusal://`). Recusal is never a mark against a consultant; forced or pressured non-recusal is a program violation.

### INV-413 — Network health monitoring

Quarterly signed `consult-health://` gseed reporting:

- Number of active consultants per domain.
- Average time-to-review per domain.
- Block rate per domain.
- Override rate per domain.
- Consultant satisfaction (anonymous survey).
- Budget utilization.

Domain health below thresholds triggers recruitment actions. Consistent understaffing in a domain means that domain's review trigger produces an automatic **hold** rather than a block — the seed cannot be signed under foundation identity until the domain has sufficient review capacity.

## Phase 1 deliverables

**Months 0–3**
- INV-407 triggers encoded in the constraint stack.
- `consult-review://`, `consult-trigger://`, `consult-recusal://` schemes registered.
- Published compensation floor rates.
- Recruitment framework drafted for legal review.

**Months 3–6**
- Outreach to initial 3 consultants in each of: mental health, source-culture (starting with 2 priority cultures), disability representation. Total target: 15 consultants.
- First MOUs signed; first review gseeds produced on Foundation Kernel candidates.
- Network health report v0.1.

**Months 6–12**
- Network expansion to 30+ consultants across 8+ domains.
- Override protocol first tested (even if with a hypothetical); publication of the override precedent.
- Integration with Brief 107 governance council.
- Retainer structure live for active-tier consultants.

## Risks

- **Recruitment failure in a domain.** Mitigation: the domain hold (INV-413) means the substrate refuses to ship gseeds in unreviewable domains rather than shipping them without review. Slower ship is acceptable; unreviewed is not.
- **Consultant fatigue / burnout.** Mitigation: mandatory rotation, retainer structure, cap on reviews per month per consultant, explicit right to refuse any review.
- **Weaponization of review for ideological capture.** Mitigation: multi-reviewer minimum, override path with governance supermajority, public review reasoning.
- **Compensation budget exceeding available funds.** Mitigation: review triggers are scoped to mandatory cases only; creator-namespace review is optional and user-paid. Foundation ships slower if necessary to stay within budget.
- **Consultant privacy exposure from public reviews.** Mitigation: consultants choose anonymous or named; reasoning can be private with summary public.

## Recommendation

**Adopt INV-407 through INV-413 before any Foundation Kernel seed touching sensitive domains is signed.** Start recruitment in parallel with Brief 095's Kernel phase. Begin with mental health and two source-culture domains to establish the workflow before scaling.

Refuse to sign any foundation-identity gseed triggering a consultancy domain until that domain has at least the minimum required reviewers in active tier.

## Confidence

**4/5.** The compensation model and review-as-gseed structure are sound. The main execution risk is recruitment — reaching real consultants in source cultures, especially outside the global North, requires relationships GSPL doesn't yet have. Partner institutions from Brief 098 can help introduce but not substitute.

## Spec impact

INV-333, INV-339, INV-343, and the Brief 088 identity contract gain operational enforcement through INV-407..413. No constitutional changes; this brief operationalizes existing commitments.

## Open follow-ups

- Initial consultant identification and introduction paths (requires real outreach, not research).
- Community-grant fiscal sponsorship structure (501(c)(3) vehicle vs. LLC direct payment).
- Translation of review and reasoning documents for non-English consultants.
- Conflict escalation path when a consultant and a partner institution (Brief 098) disagree.
- Insurance or indemnification for consultants whose reviews become subject to legal challenge.

## Sources

- Publishing sensitivity reader rate benchmarks (Writer's Digest, sensitivity reader collective publications).
- AI ethics consultancy market data (Partnership on AI, community rate surveys).
- Indigenous data sovereignty literature (CARE principles for Indigenous Data Governance).
- Clinical depiction consultation literature in film/TV industry.
- Round 4 Briefs 086E, 086H, 088 for care contracts, culture substrate, character identity.
- Round 4 Brief 095, 097 for constraint stack and CI grounding.
- Round 4 Brief 098 for partner relationships.
