# Brief 106 — Creator economics and marketplace pricing

## Question

What is the revenue model, what are the federation tolls, how does lineage-based royalty distribution work, what are the free-tier boundaries, what are the subscription tiers, what is the marketplace transaction structure, and how does the constitutional commitment that creator credit is never erasable interact with monetization — such that GSPL has a viable economy that compensates creators in proportion to upstream contribution and never extracts from them?

## Why it matters

A foundation that depends on charity dies. A foundation that extracts from creators corrupts. The middle path is an economy where creators are compensated in proportion to lineage contribution, the substrate covers its costs, and no one is forced to pay for the act of creating.

The forever-signed-by edge (Brief 088) and tombstone-preserves-lineage (INV-356) make royalty distribution mechanically possible because every fork credits its upstream. This is the substrate's economic superpower: derivative work pays the original automatically.

## What we know from spec

- Brief 044: marketplace economics (Round 2 baseline).
- Brief 047: zk-proof-of-authorship.
- Brief 088 INV-303: forever-signed credit lineage.
- INV-356: tombstone deletion preserves lineage.
- Brief 100 INV-419: fork-and-reconcile in creator namespaces.
- Brief 101 INV-426: cost accounting per namespace.
- Brief 105 INV-454: cost transparency report.

## Findings

### Finding 1: Creator-tool monetization clusters as freemium with paid power-tiers

Industry pattern: Figma, Notion, Canva, Substack, Roblox, Hugging Face, GitHub, Substack, Patreon — almost all use freemium-with-paid-tiers. The free tier is generous enough to make the tool feel non-limiting for hobbyists; paid tiers unlock professional capacity, federation publishing, marketplace listing, and team features.

GSPL fits this pattern naturally:

- **Free tier**: full studio, full Foundation Kernel access, signing in personal namespace, query budget calibrated for hobbyists, no marketplace listing.
- **Creator tier (~$9–15/month)**: extended query budget, marketplace listing, federation publishing, lineage royalty receipt, partner reference fetch budget extended.
- **Professional tier (~$25–40/month)**: high query budget, multi-fork projects, priority support, governance council eligibility (with reputation), bulk export.
- **Studio tier (~$80–150/month)**: team accounts, shared namespaces, dedicated cache headroom, custom partnership terms.

These price points are anchored to comparable platforms; they will be calibrated against actual cost transparency data (INV-454).

### Finding 2: Lineage-based royalty distribution is mechanically possible because of forever-signed-by

The forever-signed-by edge means every gseed knows its upstream signers. When a derivative work generates revenue (marketplace sale, federation download with paid access, commercial use license), the substrate can mechanically split the revenue across the lineage according to a published royalty curve.

A typical curve:

- Direct fork creator: 70%.
- One step upstream: 15%.
- Two steps upstream: 8%.
- Three steps upstream: 4%.
- Foundation Kernel base: 3% (back to the foundation pool).

This is the substrate's commitment: **creating things based on others' work pays the others, automatically, with no negotiation, no platform-mediated contract, no opt-in**. The upstream creator can choose to waive their royalty (creating a public-good seed) but they cannot be erased from it.

### Finding 3: Federation tolls must compensate peers but not gate access

If federation peers bear costs of replicating gseeds, they should be compensated, but the substrate cannot allow access to be gated by who pays. The right structure: peers can charge a small toll for high-throughput access (bulk download, programmatic API) but must serve normal user queries free. Tolls are paid by professional/studio tier users via their subscription, not by hobbyists.

### Finding 4: Marketplace transaction take rate cluster

Industry comparables for marketplace take rates:

- App stores: 15–30%.
- Steam: 30%.
- Etsy: 6.5% + listing fee.
- Bandcamp: 10–15%.
- Substack: 10%.
- Gumroad: 10%.
- Patreon: 8–12%.

The lower end is the right anchor for a substrate that wants creators to thrive. **GSPL's recommended take rate: 10%**, of which 60% covers operational costs and 40% returns to the foundation pool for armory expansion, partner compensation, consultancy network, and grants.

### Finding 5: The constitutional non-erasure commitment makes opt-out impossible

Creators can choose to:

- Waive their royalty (let downstream pay nothing upstream).
- Make their seed public-domain (no marketplace listing).
- Tombstone their seed (content removed, credit preserved).

Creators cannot:

- Be removed from the lineage of derivatives.
- Have their forever-signed-by edge deleted.
- Have their authorship anonymized retroactively.

This is non-negotiable. It is the constitutional anchor of the economy.

## Inventions

### INV-459 — The lineage royalty curve

Default royalty distribution for marketplace and licensing revenue:

| Lineage step | Share |
|---|---|
| Direct creator | 70% |
| 1 upstream | 15% |
| 2 upstream | 8% |
| 3 upstream | 4% |
| Foundation Kernel | 3% |

The curve is governance-amendable (Brief 107) but the principle (upstream gets paid) is constitutional. Creators can publish a custom curve when forking under explicit creator decision; the published curve is signed and visible.

### INV-460 — The four-tier subscription model

| Tier | Price | What it gives |
|---|---|---|
| Free | $0 | Full studio, full Kernel, personal namespace, hobbyist query budget |
| Creator | ~$12/mo | Extended query budget, marketplace listing, federation publishing, lineage royalty receipts, partner fetch budget |
| Professional | ~$32/mo | High query budget, multi-fork projects, priority support, governance reputation |
| Studio | ~$120/mo | Team accounts, shared namespaces, dedicated cache, custom partnership terms |

Pricing is initial; final pricing calibrated against cost transparency reports. The free tier cannot be reduced — it is the substrate's commitment to access.

### INV-461 — The marketplace transaction structure

10% take rate split:

- 6% operational (compute, storage, network, partner crawl, partner compensation).
- 4% foundation pool (armory expansion, consultancy network, grants, governance operations).

90% to the seller (which then flows through the lineage royalty curve to upstream creators).

Listing is free for creator-tier and above. Sellers set their own prices.

### INV-462 — Federation tolls for high-throughput access

Peers may charge high-throughput access tolls (bulk download, API throughput beyond fair-use limits). Tolls are paid via the subscription tier (Professional and Studio bundle a toll allowance) or per-request for free-tier users who need occasional bulk access. Normal interactive query traffic is always free.

Tolls are governance-bounded; no peer may charge above a published ceiling without governance review.

### INV-463 — The royalty waiver and public-good designation

Creators can:

- Mark a seed as `royalty-waived` — downstream owes them nothing, but the credit edge remains.
- Mark a seed as `public-good` — content is released under the most permissive license, no marketplace listing, royalty waived.
- Mark their entire namespace as `public-good` — applies to all current and future seeds.

Public-good seeds receive a visible badge in the studio; their lineage walks reach back to a creator who explicitly chose to give.

### INV-464 — The royalty receipt as signed gseed

Every royalty distribution event produces a signed `royalty-receipt://` gseed:

- Source transaction.
- Lineage chain at the time of distribution.
- Per-creator amount.
- Timestamp and signing identities.

Receipts are visible to the creators in their dashboards. Aggregated transparency reports are public per quarter.

### INV-465 — The foundation grant program

A portion of the foundation pool funds:

- Source-culture compensation (Brief 098 INV-403).
- Consultancy network retainers (Brief 099 INV-410).
- Co-curator program (Brief 095 INV-387).
- Grants for underrepresented creators (governance-decided criteria).
- Anti-hallucination corpus contributors (Brief 097 INV-399).

Grant decisions are public (recipient names, amounts, purpose). Grant program is governed by Brief 107.

### INV-466 — Constitutional non-erasure of credit

Encoded as INV-466 (a re-statement to elevate it as economic foundation): creator credit on any gseed cannot be erased by any party, including:

- The creator themselves (they can waive royalty, not authorship).
- Downstream creators (they cannot fork without preserving the upstream chain).
- The marketplace (it cannot delist a seed in a way that severs lineage).
- The foundation itself (governance cannot amend the non-erasure rule out).
- Tombstone deletion (tombstones preserve the credit edge).

Non-erasure is the substrate's economic anchor. Without it, royalty distribution is meaningless.

## Phase 1 deliverables

**Months 0–4**
- Royalty curve and waiver mechanisms encoded.
- Free tier and Creator tier infrastructure.
- Marketplace listing flow.

**Months 4–8**
- Professional tier and Studio tier.
- Marketplace transaction processing with royalty distribution.
- Royalty receipt gseeds.
- Cost transparency report integrated with pricing calibration.

**Months 8–12**
- Federation toll structure.
- Foundation grant program operational.
- Quarterly royalty transparency report.
- First marketplace transactions in closed beta.

## Risks

- **Free tier too generous; foundation runs out of cash.** Mitigation: free-tier query budget is calibrated against cost transparency; if break-even doesn't approach by 100K users, free-tier budget tightens (visibly, with notice) before foundation is endangered.
- **Royalty distribution computation cost.** Mitigation: lineage walks are bounded by the depth budget (default 6 steps); deeper attribution accumulates into the foundation pool.
- **Royalty curve disputes.** Mitigation: governance-amendable; non-erasure of credit is the only non-amendable principle.
- **Marketplace fraud (fake transactions to game royalties).** Mitigation: signing identity verification, anomaly detection, governance review for outliers.
- **Subscription pricing wrong by 2x.** Mitigation: prices are calibrated quarterly against cost transparency; changes are announced 30 days in advance and never apply retroactively.

## Recommendation

**Adopt INV-459 through INV-466.** Ship the free tier and Creator tier first (months 0–4); add Professional and Studio tiers when closed beta reaches its gate. Royalty distribution is the substrate's economic distinguisher — operationalize it before any marketplace transaction can occur.

Refuse to ever charge for the free tier capabilities. Refuse to extract take rate above 10%. Refuse to amend the non-erasure of credit out.

## Confidence

**4/5.** Pricing models are well-understood from comparables; royalty distribution is mechanically straightforward given the lineage substrate. The main risk is calibrating free-tier and paid-tier numbers against real cost data, which only happens with real users.

## Spec impact

Brief 044 (Round 2 marketplace) gains eight new inventions (INV-459..466). No new substrate primitives. `royalty-receipt://`, `royalty-waiver://`, and `royalty-curve://` join the lineage namespace.

## Open follow-ups

- Tax and legal review of cross-jurisdiction royalty distribution.
- Payment processor selection (Stripe, Wise, crypto rails optional).
- Currency support beyond USD.
- Refund and chargeback handling.
- Creator KYC where required by law.

## Sources

- Figma, Notion, Canva, Substack, Roblox, Hugging Face, GitHub pricing pages and earnings.
- Etsy, Bandcamp, Patreon, Gumroad take rate analyses.
- App store policy debates (Apple, Google) on take rate.
- Music industry royalty distribution mechanics (composer, performer, publisher splits).
- Round 2 Briefs 044, 046, 047.
- Round 4 Briefs 088, 091.
- Round 5 Briefs 095, 098, 099, 101, 105.
