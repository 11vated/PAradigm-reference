# Brief 107 — Governance framework and constitutional amendment process

## Question

What is the composition of GSPL's governance council, what is the amendment process for ordinary substrate decisions, what is the amendment process for constitutional commitments, what authority do consultants and partners hold, and how does governance itself become lineage-tracked so that decisions are auditable?

## Why it matters

The 13 constitutional commitments are non-patchable. The 80+ Round 4–5 inventions sit on top of them. The substrate's credibility depends on those commitments not bending under founder pressure, investor pressure, partner pressure, or community pressure. That requires a governance structure with real authority to refuse and a documented process for amendment that protects the constitutional layer while allowing ordinary improvement.

A governance vacuum is a foundation that bends the moment someone asks. A governance lockout is a foundation that cannot evolve. The middle path is a small council, written rules, supermajority gates for constitutional change, and full transparency.

## What we know from spec

- 13 constitutional commitments from Round 4 (operationalized in Round 5).
- Co-curator reputation system (Brief 095 INV-387).
- Consultancy block-and-override (Brief 099 INV-411).
- Federation peer reputation (Brief 100 INV-416).
- Network-level tombstone ratification (Brief 100 INV-420).
- Refusal override path (Brief 103 INV-439).
- The substrate's commitments to forever-signed credit and tombstone lineage preservation.

## Findings

### Finding 1: Successful tech-foundation governance has three layers

Comparable foundation governance (Linux Foundation, Apache Foundation, Mozilla Foundation, Wikimedia, Blender Foundation, Python PSF, Rust Foundation): consistently three layers.

1. **Founder/BDFL or executive**: day-to-day operational decisions.
2. **Council or board**: strategic decisions, resource allocation, conflict resolution, ordinary policy.
3. **Constitutional layer**: the immutable principles; amendment requires supermajority + public process.

GSPL maps cleanly:

- Founder (Kahlil at solo phase, eventually a small executive team) handles operations.
- Council handles strategy and conflict.
- The 13 commitments are constitutional and amendment is supermajority + public.

### Finding 2: Council size optimum is 7–11

Smaller than 7: cliques and capture risk. Larger than 11: consensus impossible. Comparables: Apache PMCs ~5–11, Python PSF ~12 (often considered slightly large), Rust core team ~6–9, Blender Foundation ~9.

GSPL council target: **9 seats**.

### Finding 3: Council composition matters more than size

A council of nine all-engineers fails on cultural questions. A council of nine all-cultural-experts fails on technical questions. The composition must mix perspectives:

- 1 founder (Kahlil) — institutional memory.
- 2 technical stewards — substrate engineering authority.
- 2 community creators — chosen by reputation from the co-curator program.
- 2 lived-experience consultants — chosen from the consultancy network.
- 1 partner institution representative — rotating among partner institutions.
- 1 independent ethics seat — chosen from outside GSPL by the rest of the council.

Diversity by design. Each seat has clear authority within their domain.

### Finding 4: Constitutional amendment thresholds must be high enough to feel real, low enough to permit evolution

If amendment requires unanimity, the constitution becomes brittle. If it requires only majority, it becomes weak. The right threshold for constitutional commitments: **supermajority of council (≥ 7 of 9) + public RFC + 30-day comment period + independent ethics review**.

For the most foundational commitments (the non-erasure of credit, the grounding floor, no living-person gseeds), the threshold is even higher: **8 of 9 + 60-day comment period + independent ethics review + the right of any single consultant or partner to extend the comment period by 30 days**.

### Finding 5: Governance decisions must themselves be lineage-tracked gseeds

Consistent with the substrate's principle that everything is signed and lineage-tracked, governance decisions must be `governance://` gseeds. Council votes, RFCs, amendment processes, override decisions — all become first-class substrate citizens. Anyone can walk the governance graph the same way they walk a composition graph.

## Inventions

### INV-467 — The 9-seat governance council

Council composition fixed at 9 seats with explicit role definitions:

| Seat | Role | Selection |
|---|---|---|
| 1 | Founder | Kahlil; permanent until designation of successor |
| 2,3 | Technical stewards | Appointed by founder, ratified by council |
| 4,5 | Community creators | Elected from co-curator network at reputation T3 |
| 6,7 | Lived-experience consultants | Elected from consultancy network |
| 8 | Partner institution rep | Rotating annually from partner registry |
| 9 | Independent ethics | Appointed by council majority from outside GSPL |

Term lengths: 2 years for seats 2–9, with staggered renewal so the council never turns over more than 50% in one cycle.

### INV-468 — The three-layer authority model

| Layer | Decisions | Authority |
|---|---|---|
| Operational (founder/exec) | Day-to-day, releases, hires, partner outreach, infrastructure | Unilateral within budget |
| Council | Roadmap, ordinary policy, conflict resolution, override of refusals, governance-amendable parameters | Majority vote (5 of 9) |
| Constitutional | The 13 commitments and the non-amendable economic anchor (INV-466) | Supermajority + public RFC + ethics review |

### INV-469 — The constitutional amendment process

For a proposed amendment to a constitutional commitment:

1. **Proposal**: any council member or community petition (≥ 1% of active creators) files a `gov-proposal://` gseed.
2. **Sponsorship**: at least 2 council members must co-sponsor for the proposal to advance.
3. **Public RFC**: 30-day comment period (60 days for foundational commitments).
4. **Ethics review**: independent ethics seat issues a signed advisory (`gov-ethics-review://`).
5. **Consultancy review**: any consultant in an affected domain may issue a binding objection extending the comment period by 30 days.
6. **Council vote**: ≥ 7 of 9 (≥ 8 of 9 for foundational commitments).
7. **Ratification**: signed `gov-amendment://` gseed published with full process lineage.
8. **Effective date**: minimum 30 days after ratification to allow operational adjustment.

Failed amendments produce a signed `gov-amendment-fail://` gseed with reasoning and the public process trail.

### INV-470 — The ordinary policy amendment process

For non-constitutional decisions (ordinary policy, parameter tuning, roadmap changes):

1. Proposal as `gov-proposal://`.
2. Council discussion (no public RFC required for low-impact decisions; required for high-impact).
3. Council vote: simple majority (5 of 9).
4. Ratification as `gov-decision://`.

Higher-impact ordinary policy (changes affecting > 10% of creators or partners) automatically requires public RFC.

### INV-471 — The non-amendable core

Three principles are explicitly non-amendable, even by supermajority + ethics review:

1. **Forever-signed credit lineage cannot be erased** (INV-466).
2. **The grounding floor cannot be removed** (INV-357 and commitment #8).
3. **The constitutional amendment process itself cannot be weakened** to require a lower threshold than the current minimum.

To change a non-amendable principle requires forking the foundation identity — which is allowed (the substrate is open) but produces a different foundation, not an amended one. The forked foundation is a new signing identity with no claim on the original's federation, partners, or armory.

### INV-472 — Governance decisions as substrate-native gseeds

`governance://` URL scheme covering:

- `gov-proposal://`
- `gov-amendment://`
- `gov-amendment-fail://`
- `gov-decision://`
- `gov-ethics-review://`
- `gov-override://` (for refusal overrides)
- `gov-council-vote://`
- `gov-rfc://`

Every governance event is signed by the participating identities. Anyone can walk the governance graph and audit the substrate's history of decisions.

### INV-473 — Refusal override workflow

When a refusal under a constitutional commitment is challenged:

1. Challenger files `gov-override-request://`.
2. Council reviews within 14 days.
3. Override requires supermajority (≥ 7 of 9) for foundational commitments, simple majority for non-foundational.
4. If override granted, the original refusal remains visible alongside the override decision in the lineage graph.
5. Override is rare; baseline override rate is monitored quarterly. Above-threshold override rate triggers a meta-review of the commitment by the council.

### INV-474 — Public council transparency

Every council vote is public. Every council member's vote on every decision is signed and visible. Council meeting minutes are signed `gov-minutes://` gseeds. Council members may not vote in secret.

The only exception is personnel matters (hiring, firing, individual disputes), which are summarized in aggregate without exposing individual votes.

### INV-475 — Council recusal and conflict-of-interest discipline

Council members must recuse from any decision where they have:

- Personal financial interest in the outcome.
- A direct relationship with a primary affected party.
- A consultancy or partner role with conflicting authority.

Recusals are signed (`gov-recusal://`). Failure to recuse is a council violation reviewable by the rest of the council, with removal as a possible consequence.

## Phase 1 deliverables

**Months 0–4**
- Founder decides initial technical stewards (seats 2, 3).
- Independent ethics seat (9) appointed via cold outreach.
- Council bylaws drafted.
- `governance://` schemes registered.

**Months 4–8**
- Co-curator and consultancy network begin reputation accumulation toward seat eligibility.
- First partner rep (seat 8) appointed from rotating partners.
- First council vote (test) on a low-stakes ordinary decision.

**Months 8–14**
- Seats 4, 5, 6, 7 filled from co-curator and consultancy networks.
- Full 9-seat council operational.
- First constitutional amendment process (even if to a low-stakes commitment) walked end-to-end as a rehearsal.

**Months 14+**
- Year-1 council completes its first full year.
- Annual transparency report published.
- Stagger ratchet begins (some seats rotating).

## Risks

- **Council capture by founder.** Mitigation: founder is 1 of 9 seats; constitutional amendments require 7 (or 8) of 9; non-amendable core protects the substrate even if founder somehow had majority influence.
- **Council deadlock.** Mitigation: ordinary decisions only require majority (5 of 9); deadlock on constitutional amendments preserves the status quo, which is acceptable for a constitution.
- **Council members quit en masse.** Mitigation: staggered terms, recruitment pipeline through co-curator and consultancy networks, vacant seats filled within 90 days.
- **Governance becomes performative.** Mitigation: every decision is a signed gseed in the public graph; performative governance is detectable and itself reviewable.
- **Constitutional amendment used to weaken the substrate.** Mitigation: non-amendable core (INV-471) protects the most important principles; the forking option exists for those who want a different substrate.

## Recommendation

**Adopt INV-467 through INV-475.** The council is the substrate's defense against founder fatigue, investor pressure, and community capture. Build it deliberately, with real authority, on a real timeline. Refuse to launch GA (Brief 105 GA gate) until the council is seated.

The non-amendable core (INV-471) is the substrate's philosophical anchor — refuse any pressure to weaken it.

## Confidence

**4/5.** Foundation governance is well-studied; the model is anchored in proven structures. The main execution risk is recruiting an independent ethics seat and a partner rep that take their roles seriously. Mitigated by the rotating partner mechanism and the cold-outreach process for ethics.

## Spec impact

Round 4 13 constitutional commitments gain operational governance enforcement. New `governance://` URL scheme family. Nine new inventions (INV-467..475). Brief 105 GA gate updated to require seated council.

## Open follow-ups

- Detailed bylaws (legal review).
- Council compensation (probably honorarium, not salary).
- Term limits for the founder seat (handover protocol).
- Emergency protocols for time-critical decisions.
- Whistleblower protection within the council.

## Sources

- Linux Foundation, Apache Foundation, Mozilla Foundation, Wikimedia Foundation, Blender Foundation, Python PSF, Rust Foundation governance documents.
- Open source governance literature (Producing Open Source Software, Karl Fogel).
- Constitutional design literature (J. Elster, J. Buchanan).
- Round 4 Brief 091 (knowledge graph), all 13 constitutional commitments.
- Round 5 Briefs 095, 098, 099, 100, 103, 105, 106.
