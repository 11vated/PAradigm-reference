# Brief 108 — Year-1 roadmap and milestones

## Question

Quarter by quarter, what are the milestones, the dependency graph, the risk register, the budget envelope, the go/no-go gates, and the honest list of what gets dropped if something slips — such that GSPL has a year-1 plan that a solo founder can actually execute, that closes every Round 4 open follow-up, and that arrives at GA with all four launch gates (Brief 105 INV-453) green?

## Why it matters

Round 5 Briefs 095–107 each have phase deliverables. Without an integrated roadmap, those phases collide, dependencies get missed, and the founder works on the wrong thing in the wrong week. The roadmap is the integration layer that turns 14 briefs into one executable year.

## What we know from spec

All Round 5 brief Phase 1 deliverables. The Round 4 nine open follow-ups. The Round 5 Brief 105 four-phase rollout. The current state (Round 4 architecture locked, no Round 5 implementation yet).

## Findings

### Finding 1: Solo-founder execution capacity is ~1.5 substantial deliverables per week

Anchored in indie game/tool founder retrospectives (Stardew Valley, Cassette Beasts, Dwarf Fortress, Krita early years, Blender pre-1.0, dwarf indie tooling postmortems): a focused founder ships ~1.5 substantial deliverables per week sustainably (counting agent-assisted work, against the established Brief 095 finding that solo curators ship 5/day with agent assistance — but a "deliverable" here is a system, not a single seed).

Year 1 = 52 weeks = ~78 substantial deliverables. The Round 5 brief inventory has ~80–120 phase 1 deliverables across 14 briefs. **This barely fits and depends on aggressive prioritization.**

### Finding 2: Critical-path scheduling beats parallel ambition

Trying to do all 14 briefs in parallel produces drift. The roadmap must establish a critical path: the deliverables that block everything else come first; the deliverables that can wait, wait. The critical path through Round 5:

1. Constraint stack and grounding gate (Briefs 095, 097) — blocks armory and CI.
2. Foundation Kernel composition (Brief 095) — blocks first-user experience.
3. First 5 partner MOUs (Brief 098) — blocks reference fetcher operational use.
4. Composition graph viewer + provenance panel (Brief 103) — blocks first-user experience.
5. 8-minute path (Brief 104) — blocks closed beta gate.
6. First 10 style adapters at acceptance (Brief 096) — blocks closed beta gate.
7. Initial council seating (Brief 107) — blocks GA gate.
8. Marketplace and royalty distribution (Brief 106) — blocks GA gate.

### Finding 3: Quarterly milestones force integration moments

Quarterly milestones are the gates where parallel work is forced to integrate. Each quarter ends with a measurable state: alpha gate, mid-alpha checkpoint, closed beta gate, mid-beta checkpoint, open beta gate, GA gate.

### Finding 4: A risk register with named mitigations beats a risk list

Generic "things might go wrong" lists are useless. A real risk register names the specific risk, the trigger condition, the mitigation, and the owner. GSPL has six top risks for year 1:

1. Solo-founder bandwidth collapse.
2. Foundation Kernel quality not meeting bar by closed beta gate.
3. Partner MOU response rate below threshold.
4. Anti-hallucination corpus too narrow.
5. Cost transparency revealing 2x+ misestimate.
6. Council recruitment failure for an independent or community seat.

### Finding 5: A drop-list is a feature, not an admission of failure

The roadmap must publish, in advance, what gets cut if something slips. Not "we'll figure it out" — explicit triage. This protects the substrate from sliding into compromise.

## Inventions

### INV-476 — The integrated 4-quarter roadmap

**Q1 (months 0–3) — Foundation tooling and Alpha gate work**

Goals:
- Constraint stack (INV-383) operational.
- Grounding gate (INV-397) running in CI.
- Candidate composer (INV-386) operational.
- First 50 Foundation Kernel seeds composed and signed.
- Composition graph viewer v0.1 (INV-436).
- Provenance panel (INV-438).
- 4-state visual encoding (INV-437).
- Per-query budget envelope (INV-422).
- Three-tier cache with tier-source labeling (INV-423).
- Partner outreach Wave 1: 8 Tier 1 institutions via Template T1-O (Brief 098).
- Initial 3 consultancy domain consultants identified and engaged.
- Initial 2 council seats (founder + first technical steward).
- `governance://` schemes registered.
- Cost transparency report v0.1.

End-of-Q1 gate: Alpha gate from Brief 105 INV-453.

**Q2 (months 3–6) — Closed beta preparation**

Goals:
- Foundation Kernel reaches 200 seeds.
- First 10 style adapters at full Brief 096 acceptance.
- Anti-hallucination corpus at 250 prompts (INV-394).
- Refusal explanation surface (INV-439).
- Lineage walker (INV-441).
- Removal-on-request workflow (INV-430).
- First 6 partner MOUs signed informally.
- Outreach Wave 2: Wikimedia, Europeana.
- Compensation framework live for consultants (INV-410).
- Council seats 3, 4 filled (second technical steward + first community creator).
- Closed beta cohort onboarded (~50 invited reviewers).
- 8-minute path (INV-445) operational.
- First-session metrics (INV-450) collecting data.
- Cost transparency v0.5 with first calibration insights.

End-of-Q2 gate: Closed beta gate from Brief 105 INV-453.

**Q3 (months 6–9) — Open beta preparation**

Goals:
- Closed beta cohort grows to 200; 8-minute path success rate measured ≥ 70%.
- Foundation Kernel proven against the cohort.
- Co-curator phase opens; armory grows toward 600 seeds.
- Style adapter cohort grows to 30 at acceptance.
- Federation peers grow to 5 (founder + test + 3 invited co-curator peers).
- Source-culture outreach Wave 1 (Template T3-S) sent with community pre-review.
- First source-culture MOU informally acknowledged.
- Consultancy network at 15 active consultants.
- Council seats 5, 6, 7 filled (community + lived-experience).
- Royalty curve and lineage royalty distribution (INV-459, INV-464).
- Free and Creator subscription tiers operational (INV-460).
- Marketplace listing flow live.
- First quarterly cache audit (INV-435).
- First quarterly partner transparency reports (INV-405).
- First quarterly governance transparency report (INV-474).

End-of-Q3 gate: Open beta gate from Brief 105 INV-453.

**Q4 (months 9–12) — Toward GA**

Goals:
- Open beta opens; cohort grows to 5K.
- Operational SLOs (INV-457) measured for 30 consecutive days.
- Foundation Kernel 200 + armory ≥ 600 toward 1000.
- Style adapters at 50 toward 80.
- Anti-hallucination corpus at 500.
- Federation peers at 5+ stable.
- Partner MOUs at 10+ formal.
- Consultancy network at 30+ active.
- Council seats 8 (partner rep) + 9 (independent ethics) filled.
- Constitutional amendment process rehearsed end-to-end.
- Professional and Studio subscription tiers (INV-460).
- Foundation grant program operational (INV-465).
- First constitutional amendment opportunity walked (test or real).
- Cost transparency reports show approach to break-even at 100K user projection.
- Year-1 retrospective and Year-2 planning brief drafted.

End-of-year gate: GA gate from Brief 105 INV-453 (likely ratified in early Year 2 once 30-day SLO floor is hit).

### INV-477 — The dependency graph

```
Constraint stack ──► Foundation Kernel ──► First-user experience ──► Closed beta
       │                  │                       │                       │
       ▼                  ▼                       ▼                       ▼
   Grounding           Style                Composition             Open beta
   gate              adapters             graph viewer                  │
       │                  │                       │                     ▼
       └──► Anti-hallucination corpus ──► Refusal surface            GA gate
                                                                         │
Partner outreach ──► Reference cache ──► Cache audit ◄───────────────────┘
       │                                              ▲
       └──► Source-culture MOUs ──► Consultancy network
                                            │
                                            ▼
                                       Council seating
                                            │
                                            ▼
                                       Marketplace + royalty
```

### INV-478 — The risk register with named mitigations

| Risk | Trigger | Owner | Mitigation |
|---|---|---|---|
| Solo-founder bandwidth collapse | More than 2 weeks of missed deliverables | Founder | Mandatory off-week every 6 weeks; drop list activated |
| Foundation Kernel quality below bar | Audit rejection rate > 5% in any month | Founder | Slow Kernel pace, raise constraint stack rigor, add reviewer |
| Partner MOU response rate < 30% | Q1 outreach response rate measured | Founder | Outreach personalization; intermediary introductions; revised templates |
| Anti-hallucination corpus too narrow | Quarterly red-team finds undocumented attack category | Founder + red team | Emergency corpus addition; CI gate re-run |
| Cost surprises above 2x estimate | Cost transparency report shows 2x overrun for 2 consecutive months | Founder | Tighten free-tier query budget; sign-up pause if needed |
| Council recruitment failure | Q4 with seats unfilled | Founder + council | Active recruitment; rotate partner rep faster; outreach for ethics seat |

### INV-479 — The drop list

If a deliverable must be cut, this is the order:

1. Cosmetic studio refinements (Brief 079 polish beyond MVP).
2. Style adapters beyond the first 30 (target was 80 — accept 30 at GA).
3. Federation peers beyond 5 (target was higher — accept 5).
4. Marketplace transaction features beyond listing (e.g., promotional surfaces).
5. Source-culture MOUs beyond the first formal one (acknowledged informal is acceptable).
6. Foundation grant program (defer to Year 2 if cost transparency shows headroom is too tight).

What is **never dropped**:
- Constraint stack and grounding gate.
- Foundation Kernel at minimum 100 seeds (half of the 200 target acceptable for closed beta).
- Composition graph viewer + provenance panel.
- Refusal explanation surface.
- 8-minute path infrastructure.
- Anti-hallucination corpus and CI grounding gate.
- At least 5 partner MOUs.
- Council at minimum 5 seats (not 9).
- The 13 constitutional commitments (non-droppable, non-amendable on this timeline).

### INV-480 — The budget envelope

Year 1 budget categories (rough; calibrated against cost transparency reports):

- Infrastructure (compute, storage, network): ~$30K (closed beta) → ~$80K (open beta) → ~$200K (GA approach).
- Consultancy compensation: ~$50K initial pool with $5K/month retainers.
- Partner compensation (source-culture grants): ~$30K Year 1 pool.
- Co-curator stipends: ~$20K Year 1 pool.
- Governance honorarium (council members): ~$30K (modest annual stipend per seat).
- Anti-hallucination red-team bounties: ~$10K Year 1.
- Legal review (MOUs, terms, governance bylaws): ~$25K.
- Founder compensation: dependent on outside funding.

**Year 1 operational target: ~$200K-$500K depending on growth phase reached. GA-approach operational target: ~$1M.**

These are aspirational order-of-magnitude. The cost transparency reports (INV-454) provide month-by-month reality.

### INV-481 — Quarterly retrospective discipline

End of every quarter, a signed `retrospective://` gseed published with:

- Goals shipped vs. planned.
- Risks materialized.
- Drop-list invocations.
- Budget actual vs. envelope.
- User cohort growth.
- Operational SLO performance.
- Adjustments for next quarter.

Retrospectives are public. They are not marketing; they are honest accounts.

## Phase 1 deliverables

The roadmap is the meta-deliverable. Phase 1 is the entire year. The brief itself ships month 0 as the planning artifact.

## Risks

Already covered in INV-478.

## Recommendation

**Adopt INV-476 through INV-481.** Treat the quarterly gates as immutable; treat the drop list as the planning safety net; refuse to extend Year 1 past 14 months. If GA is not achievable in Year 1 due to dropped deliverables, GA slips to early Year 2 and Year 1 is declared complete on the basis of open-beta operational discipline, which is acceptable.

Publish this roadmap as the substrate's commitment to its first-thousand-creator mission. Update it quarterly via the retrospective discipline.

## Confidence

**3.5/5.** Roadmaps always slip. The architecture is locked, the Round 5 briefs are clear, but solo-founder bandwidth is the single largest unknown. The drop list and risk register provide the safety margin. Confidence will improve quarter by quarter as actuals replace estimates.

## Spec impact

Round 5 gains the integration layer. Six new inventions (INV-476..481). No new substrate primitives. The roadmap is the bridge between Round 5 plan and Year-2 plan (which becomes Round 6).

## Open follow-ups

- Year 1 actual budget (depends on funding).
- Founder external funding strategy.
- Hiring plan if and when funding allows.
- Year 2 planning (becomes Round 6 work).
- Closing the original Round 4 nine open follow-ups one by one with explicit completion gseeds.

## Sources

- Stardew Valley, Cassette Beasts, Dwarf Fortress, Krita early-years founder retrospectives.
- Indie tool founder bandwidth analyses (Patrick Rothfuss, Notch's Minecraft early-year writings).
- Apache Foundation and Linux Foundation budget transparency reports.
- All Round 5 Briefs 095–107.
- Round 4 round-4-synthesis.md.
