# Brief 105 — Launch criteria and scaling plan

## Question

What are the gate criteria for GSPL Foundation v1.0 release, what is the phased rollout from alpha to GA, what is the cost model at 1K / 10K / 100K / 1M users, what is the degradation strategy under unexpected load, and what is the rollback protocol — such that launch is a measurable event with named gates, not a marketing date?

## Why it matters

A foundation that ships before its gates pass either ships hallucinations (commitment #8 violated), ships placeholders (Round 4 directive violated), ships partner-unhappy attribution (Brief 098 violated), or ships an 8-minute path that doesn't complete (Brief 104 violated). Any of those events does irreversible reputational harm to the substrate's "measured world inside it" claim. Launch must be gate-driven.

## What we know from spec

- Round 4 confidence 4.5/5: architecture locked, execution work remaining.
- Round 5 briefs 095–104 define the curation, quality, partnerships, operational, and first-user gates.
- Brief 080 Woah Moments and Brief 104 8-minute path define the user-visible launch surface.
- Brief 074 multiplayer runtime, Brief 075 GPU-less fallback define scaling envelope considerations.

## Findings

### Finding 1: Phased rollouts cluster as alpha → closed beta → open beta → GA

Industry pattern is consistent: Figma, Notion, Roblox, Hugging Face, GitHub, Substack, Discord all used some variant of alpha (internal + invited) → closed beta (waitlist, ~hundreds) → open beta (public, signup, sometimes free) → GA (public, monetized). Skipping phases produces incidents that erode trust.

GSPL should plan four phases:

| Phase | Audience | Size | Duration | Gate to next |
|---|---|---|---|---|
| Alpha | Founder + 5 invited reviewers | ~6 | 1–2 months | All Round 5 briefs operational |
| Closed beta | Invited creators from waitlist + co-curators | ~200 | 2–3 months | First-session 8-min target ≥ 70% |
| Open beta | Public signup, free | ~5K | 3–6 months | Federation peers ≥ 5; partner MOUs ≥ 8 |
| GA | Public, full marketplace, paid tiers | unbounded | ongoing | Operational SLO met for 30 consecutive days |

### Finding 2: Cost models for federated content-addressed substrates are dominated by storage and network

Comparable platforms' cost composition (Hugging Face, Wikimedia, IPFS providers, Roblox cloud spend disclosed in earnings):

- Storage: 30–45% of infra cost.
- Network egress: 20–35%.
- Compute (queries, rendering, agent): 15–30%.
- Cache layers: 10–15%.

For GSPL the agent compute is higher than typical (grounding queries are heavier than CRUD reads). Model estimate at user count tiers:

| Users | Daily active | Compute / month | Storage | Network | Total / month |
|---|---|---|---|---|---|
| 1K | 200 | $200 | $50 | $80 | ~$330 |
| 10K | 2K | $2K | $300 | $700 | ~$3K |
| 100K | 20K | $25K | $2K | $9K | ~$36K |
| 1M | 200K | $300K | $20K | $90K | ~$410K |

These are order-of-magnitude estimates anchored to comparable workloads. Monetization (Brief 106) must reach break-even by the 100K tier or the foundation depends on external funding.

### Finding 3: Degradation strategy must downgrade visibly, never silently

Under unexpected load, GSPL has only one acceptable degradation path: surface the degradation to the user, downgrade grounding confidence per Brief 101 INV-425, throttle low-priority namespaces first (creator before foundation, anonymous before authenticated), and refuse new sign-ups before existing users see degradation.

Never silently fail a query. Never drop grounding to "best effort." Never approximate a refusal.

### Finding 4: Rollback protocol must preserve user data and lineage

When a release introduces a regression severe enough to require rollback, the rollback must:

- Revert the substrate version.
- Preserve all gseeds signed during the affected window.
- Re-run the grounding gate against the prior version.
- Communicate to affected users via notification (INV-434).
- Produce a public postmortem within 7 days.

Rollback is not a failure; refusing to rollback when needed is.

### Finding 5: Operational SLOs must be conservative and visible

GSPL's SLO targets are not best-case; they are floors. A foundation built on commitments cannot operate at "we usually meet this." The targets:

- Grounded query availability: ≥ 99.5% (downtime visible to users).
- First-session completion target: ≥ 70% complete the 8-min path within 12 min.
- Partner MOU SLA compliance: 100% (no exceptions; SLAs are contractual).
- Hallucination rate: 0 in CI; user-reported 0 false-grounded responses.
- Constitutional refusal upheld rate: 100% (no overridden refusals without governance majority).

## Inventions

### INV-453 — The four-phase rollout with gate criteria

Each phase has explicit, measurable gates:

**Alpha gate:** all Round 5 briefs operational. Foundation Kernel v0.1 (200 seeds) shipped. Grounding gate (INV-397) green for 7 consecutive days. At least 2 federation peers running. At least 3 partner MOUs in informal acknowledgment.

**Closed beta gate:** First-session 8-minute path tested with at least 5 invited reviewers, 4/5 completing within 12 minutes. Style adapter cohort (Brief 096) at ≥ 10 adapters at acceptance. At least 6 partner MOUs signed informally. Anti-hallucination corpus at ≥ 250 prompts.

**Open beta gate:** Closed-beta cohort at ≥ 200 with 8-min path success rate ≥ 70%. Federation at ≥ 5 peers. Partner MOUs at ≥ 8 with at least 1 source-culture MOU informal. Consultancy network at ≥ 15 active consultants. First quarterly cache audit published.

**GA gate:** Open-beta operational SLOs met for 30 consecutive days. Hallucination rate 0 in CI and 0 user-reported. Foundation Kernel at full 200, armory at ≥ 600 toward 1000. Marketplace operational per Brief 106. Governance council seated per Brief 107. Year-1 roadmap (Brief 108) published.

### INV-454 — The cost transparency report

Monthly signed `cost-transparency://` gseed reporting:

- Compute, storage, network, cache cost.
- Per-namespace cost split.
- Per-tier cost split.
- Headroom against monetization.
- Forecast for the coming month.

Public to users at the foundation namespace level. Provides accountability and informs Brief 106 pricing.

### INV-455 — The visible degradation protocol

Under load, degradation follows a fixed ladder:

1. Pre-warm cache misses surface to users as "live fetch in progress" with latency badge.
2. Per-query budget reductions surface as "budget reduced; extend?" affordances (INV-428).
3. Anonymous query throttling surfaces as "sign in for full access."
4. Creator-namespace throttling surfaces with namespace-scoped cost bills.
5. Sign-up pause surfaces as a public banner ("waitlist active; existing users unaffected").

Each step is visible and reversible. No silent failures.

### INV-456 — The rollback protocol with lineage preservation

Triggered by:

- Hallucination rate above threshold detected post-release.
- Constitutional refusal regression detected.
- Performance regression beyond SLO floor.
- Severe user-reported issue confirmed by postmortem.

Steps:

1. Halt new feature rollout.
2. Revert substrate version to last good.
3. Preserve all gseeds from the affected window in a frozen `rollback-window://` gseed.
4. Re-run grounding gate against the prior version.
5. Notify users via INV-434 channels.
6. Publish a public postmortem within 7 days.
7. Add a regression test for the failure to the relevant test suite (anti-hallucination, adapter, federation).

Rollback is treated as a normal operation, not an emergency.

### INV-457 — The operational SLO contract

Published, signed, version-bound SLO floors:

- Grounded query availability ≥ 99.5%.
- 8-min path success ≥ 70% within 12 minutes.
- Partner MOU SLA compliance 100%.
- Hallucination rate 0 in CI.
- Constitutional refusal upheld rate 100% absent governance override.
- Anti-hallucination corpus growth ≥ 100 prompts/quarter.

Failure to meet any SLO triggers an automatic incident response and a public status update within 24 hours.

### INV-458 — Sign-up pause as first-class capability

When the system needs to throttle, the first lever is **pause new sign-ups**, not degrade existing user service. This is the inverse of growth-at-all-costs. The substrate refuses to dilute existing creators' experience to onboard more.

Sign-up pause is visible publicly with an explanation and a waitlist join option.

## Phase 1 deliverables

- Months 0–4: Alpha gate criteria operationalized.
- Months 4–8: Closed beta gate; closed-beta cohort onboarded; first-session metrics collected.
- Months 8–14: Open beta gate; cost transparency reporting live; degradation protocol tested.
- Months 14–18: GA gate; SLO contract published; rollback protocol live; first 30 consecutive SLO-green days achieved.

## Risks

- **Gate criteria too strict; launch slips by months.** Mitigation: gates are explicit and governance-tunable; if a gate is unrealistic in practice, governance review can adjust it with public reasoning.
- **Cost projections off by an order of magnitude.** Mitigation: cost transparency reports start at alpha; surprise costs are caught within one month, not one year.
- **Sign-up pause perceived as failure.** Mitigation: communicated as a feature ("we throttle to protect existing creators"), public waitlist is dignified, not punishing.
- **Rollback protocol slow to execute.** Mitigation: rollback is rehearsed, not improvised; regression tests run against rollback artifacts.
- **First 30 SLO-green days never happens.** Mitigation: SLOs are floors not targets; if floors are missed repeatedly, something is wrong with the architecture, not the operations, and Round 6 covers it.

## Recommendation

**Adopt INV-453 through INV-458.** Treat the four phases as immutable; refuse pressure to skip a phase. Publish the SLO contract before alpha so the discipline is visible from the start. Use the cost transparency reports to validate the monetization model in Brief 106.

## Confidence

**4/5.** Phased rollout is well-understood. Cost projections are anchored to comparable workloads but carry order-of-magnitude uncertainty. The main execution risk is achieving the SLO floors with limited engineering resources; mitigated by the sign-up pause lever (INV-458) which preserves existing users at the cost of growth.

## Spec impact

Round 5 Briefs 095–104 gain six new inventions (INV-453..458). No substrate primitives change. The four phases become the official launch path documented in the README.

## Open follow-ups

- Detailed SLO measurement implementation.
- Incident response runbook (Brief 062 from Round 3 still applies).
- Disaster recovery and backup strategy.
- Insurance against partner MOU breaches.
- Founder bandwidth at each phase (probably solo through alpha, growing through beta).

## Sources

- Figma, Notion, Roblox, Hugging Face phased rollout retrospectives.
- AWS / GCP / Cloudflare cost benchmarks for similar workloads.
- Wikimedia and IPFS storage cost public reports.
- SRE workbook (Google) for SLO methodology.
- Round 3 Briefs 062, 074, 075.
- Round 4 Briefs 080, 091.
- Round 5 Briefs 095, 097, 098, 100, 101, 102, 103, 104.
