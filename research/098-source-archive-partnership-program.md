# Brief 098 — Source-archive partnership program

## Question

Which institutions should GSPL engage as tiered source partners, with what outreach templates, licensing terms, attribution contracts, crawl agreements, and conflict-resolution workflows, so that the tiered source ladder (Brief 090) becomes a concrete operational program — not an aspirational list?

## Why it matters

Brief 090 promised a tiered authoritative source ladder. Brief 091 grounded the agent against that ladder through the federated knowledge graph. Brief 097's anti-hallucination gate depends on those sources actually being reachable, stable, and attributable. All of that collapses if GSPL has no relationships with the institutions behind those sources.

Worse: institutions that discover an AI system is crawling them without engagement tend to issue cease-and-desist letters first and ask questions later. A reputable foundation must engage **before** scale, with explicit agreements, or it forfeits its "grounded in the measured world" claim the moment the first partner sends a lawyer.

## What we know from spec

From Brief 090 (tiered source ladder):

- Tier 1: primary source institutions (Met, Smithsonian, V&A, BL, LoC, NASA, NIST, PubChem, USGS, NOAA).
- Tier 2: secondary aggregators (Wikimedia, Europeana, OpenStreetMap, Wikidata, MusicBrainz).
- Tier 3: community open data (Flickr Commons, OpenContext, Internet Archive).
- Tier 4: agent-surfaced research quality (cited papers, preprints, community corpora).

From Brief 091:

- References become signed `ref://` gseeds with full provenance.
- Confidence scores depend on tier and corroboration.

From the constitutional commitments:

- No silent guesses (must be grounded).
- Source attribution is mandatory.
- Sacred-restricted cultural symbols require source-culture attribution.

## Findings

### Finding 1: Tier 1 institutions already have published open-access terms

Most Tier 1 institutions have already published open-access policies that GSPL can use out of the box, with attribution:

- **Met Museum** — Open Access for 406,000+ objects under CC0; bulk download available; stable attribution format documented.
- **Smithsonian Open Access** — 4.5M+ objects under CC0; API and bulk dataset available.
- **Rijksmuseum** — ~700K objects under CC0; API with stable identifiers.
- **V&A (Victoria and Albert)** — API with open licensing on most images; some rights-restricted material flagged.
- **British Library** — Open image collection under Public Domain Mark; bulk Flickr dataset.
- **Library of Congress** — Public domain and rights-assessed collections via API.
- **NASA** — Public domain image and dataset collections; astrophysics data via NASA ADS and SIMBAD.
- **NIST** — CODATA, NIST Chemistry WebBook, materials databases — public technical data.
- **PubChem** — Full chemistry database, public API, no fee.
- **USGS** — Earth science open data.
- **NOAA** — Weather, ocean, climate open data.

**No partnership negotiation required for Tier 1 on technical data and open-access image collections.** What IS required: attribution format compliance, rate-limit respect, and a courtesy notification when GSPL reaches meaningful scale.

### Finding 2: Wikimedia requires an explicit bulk-crawler relationship at scale

Wikipedia, Wikimedia Commons, Wikidata, and Wiktionary are under CC-BY-SA or CC0 (Wikidata). Bulk crawling above a modest threshold triggers Wikimedia's operations team. The correct path is:

- Use the published dumps first (they update every 2 weeks).
- Use the Wikidata Query Service within published rate limits.
- For high-throughput live access, register via the Wikimedia Cloud Services or engage directly through `contact@wikimedia.org`.
- Attribution requires linking to the specific article/revision, not just "Wikipedia."

### Finding 3: Source-culture archives need active relationship-building, not terms-of-use compliance

Here is where GSPL's constitutional commitments matter most. Archives of non-Western cultural heritage (Tasveer Ghar for South Asian popular art, Nasher Museum for African art, ORBIS for Roman-era data, the Endangered Archives Programme for at-risk source materials, cultural heritage archives in source countries) often have open terms of use but also **community expectations that aggregators engage directly** before republishing. The technical right to use does not equal the moral or community right.

GSPL's commitment #5 (no sacred-restricted cultural symbols without source-culture attribution and respect) requires that GSPL go beyond terms-of-use and engage source-culture institutions as actual partners, with compensation where appropriate, representation on governance where appropriate, and the ability to raise concerns through a documented escalation path.

### Finding 4: Institutional partners need one point of contact and a lightweight MOU

Research on AI-institutional partnership efforts (Hugging Face × libraries, Common Crawl × institutional reviewers, the ML Commons data work) consistently finds that institutions engage when:

- A single named point of contact is identified on the GSPL side.
- A lightweight MOU exists covering attribution, rate limits, data retention, removal-on-request, and a named escalation path.
- GSPL commits to a quarterly partner newsletter (not constant interruption).
- The institution can inspect GSPL's use of their materials via a public transparency report.

Heavy legal agreements kill partnerships before they start. MOUs should be 1–2 pages, plain language, reviewable in an hour.

### Finding 5: Partner crawl agreements should be rate-tiered, not flat

Different partners have different capacity and sensitivity. A rate-tiered model:

- **Tier A** (Met, Smithsonian, LoC, Wikimedia bulk dumps): high-throughput, bulk, cached.
- **Tier B** (V&A, BL API, Europeana): moderate throughput, respect published limits, cache aggressively.
- **Tier C** (source-culture archives, smaller institutions): very low throughput, manual review, human-in-loop fetches only.
- **Tier D** (partners who request reduced access): whatever the partner asks for, including "none, only send users our way."

Rates are negotiated with each partner and encoded in the fetcher (Brief 090) as per-partner rate limits.

## Inventions

### INV-401 — The tiered partner registry

A signed `partner-registry://` gseed listing every partner institution with:

- Institution name, URL, jurisdiction.
- Tier (1–4) and rate tier (A–D).
- License type and attribution format.
- Point of contact.
- MOU status (none / informal / signed / under review).
- Escalation path for concerns.
- Last contact date.
- Transparency report URL.

The registry is public. Users can see every partner GSPL grounds against. Changes to the registry are lineage-tracked.

### INV-402 — The 1-page partnership MOU template

A plain-language MOU covering:

1. What GSPL does and does not do with partner materials.
2. Attribution format with a concrete example.
3. Rate limits and caching policy.
4. Data retention (cache eviction per Brief 102).
5. Removal-on-request workflow (the partner can request removal of any specific material within 30 days; tombstone preserves lineage).
6. Quarterly report of usage and transparency obligations.
7. Single-page technical contact info and escalation path.
8. Term and renewal.
9. Termination without penalty.
10. Governing law and dispute resolution (lightweight mediation first).

The template is published; partners can request modifications and the modified version is signed jointly.

### INV-403 — The source-culture respect contract

For source-culture institutions (defined as any institution that is the primary cultural steward for materials from a marginalized, indigenous, or historically extracted community), the MOU is augmented with:

- A sacred/restricted material registry — materials the community explicitly asks GSPL to not surface in the foundation namespace.
- A representation pathway — the option for a source-culture reviewer to join the governance council (Brief 107) for decisions affecting their materials.
- A compensation option — depending on the institution's wishes, either a direct grant, a revenue share on derived creator content, a contribution to a community program, or explicit "none, we participate only for attribution."
- An escalation line that bypasses normal support.
- Annual review of the contract.

Commitment #5 is operationalized through this contract, not through policy pages.

### INV-404 — The outreach template library

Four outreach templates for different partner types:

- **Template T1-O** — Tier 1 institutions already publishing open access. Brief introduction, commitment to attribution, request for courtesy acknowledgment, offer of transparency report. Length: 250 words.
- **Template T2-O** — Tier 2 aggregators (Wikimedia, Europeana). Introduction, commitment to dump-first crawling, rate limit compliance, offer to register. Length: 300 words.
- **Template T3-S** — Source-culture institutions. Longer, more careful. Explicit acknowledgment of community authority, offer of representation pathway, ask for guidance on sacred/restricted materials, offer of compensation options. Length: 500 words, with a concrete follow-up invitation.
- **Template T4-R** — Research and academic institutions. Commitment to citing preprints correctly, offer to participate in academic review, ask for collaboration. Length: 350 words.

All templates ship with GSPL's mission paragraph, the constitutional commitments relevant to the partner type, and a link to the public partner registry.

### INV-405 — Quarterly partner transparency reports

Every quarter, GSPL publishes a signed `partner-report://` gseed per partner showing:

- Total fetches from the partner.
- Total cached references alive.
- Removal requests received and handled.
- Derivative creator content counts where the partner's materials are upstream.
- Attribution chain samples (randomly selected).
- Any escalations raised in the quarter.

The report is co-signed by GSPL and optionally by the partner. Partners can request changes before signing.

### INV-406 — The partner escalation workflow

Any concern raised by a partner follows a fixed escalation workflow:

1. Received within 24 hours by the named GSPL contact.
2. Initial response within 72 hours.
3. Temporary mitigation (cache freeze, fetch pause) within 7 days if requested.
4. Full resolution or mediation within 30 days.
5. Post-resolution signed `partner-escalation://` gseed documenting the issue, response, and outcome.

Every step is lineage-tracked. Partners have a public log of how their concerns have been handled historically.

## Phase 1 deliverables

**Months 0–3 — Tier 1 technical data and open-access outreach**
- Outreach to 8 Tier 1 institutions (Met, Smithsonian, Rijksmuseum, BL, LoC, NASA, NIST, PubChem) using Template T1-O.
- MOU signed with at least 3 (stretch: 5) by end of month 3.
- Partner registry v0.1 published.
- Quarterly transparency report discipline in place.

**Months 3–6 — Wikimedia and aggregator engagement**
- Bulk dump ingestion pipeline for Wikipedia, Wikimedia Commons, Wikidata.
- Rate-tier compliance checker in the fetcher.
- Europeana and OpenStreetMap engagement using Template T2-O.

**Months 6–9 — Source-culture outreach**
- Map of source-culture priority partners (first 12 target institutions) with community contact review before outreach.
- Template T3-S sent with community-reviewer pre-check.
- At least 3 source-culture MOUs in motion.
- Representation pathway for the Brief 107 governance council opened.

**Months 9–12 — Research and expansion**
- Academic and research institution engagement via Template T4-R.
- Second-wave Tier 1 expansion to non-US/EU institutions.
- Partner registry v1.0 with ≥ 25 partners.
- First escalation handled under INV-406 and postmortem published.

## Risks

- **Legal exposure from pre-MOU crawling.** Mitigation: crawling of any institution beyond public open-access dumps waits for outreach acknowledgment; the fetcher enforces partner-registry gates.
- **Source-culture institutions decline to engage.** Mitigation: decline is a valid answer; GSPL respects it by not surfacing that institution's materials in the foundation namespace at all.
- **Founder bandwidth for outreach.** Outreach is a full-time job. Mitigation: outreach is explicitly on the critical path for Brief 108's roadmap and is one of the first items to expand beyond solo-founder capacity.
- **Partner MOU disputes.** Mitigation: the escalation workflow (INV-406) has a 30-day resolution window; long disputes trigger governance review.
- **Over-promising attribution and under-delivering.** Mitigation: the quarterly transparency reports are the automatic accountability — if attribution is slipping, the report shows it.

## Recommendation

**Adopt INV-401 through INV-406.** Start with Template T1-O outreach to Met, Smithsonian, LoC, NASA, NIST, and PubChem in month 0; these are the lowest-friction first wins. Move to Wikimedia in month 2. Delay source-culture outreach until month 6 so it can be done with the care and preparation it requires — these relationships are too important to rush.

Refuse to scale the fetcher against any partner until either (a) they are in the registry with at least informal acknowledgment, or (b) they are a Tier 1 institution with published open-access terms and GSPL has sent Template T1-O.

## Confidence

**4/5.** The partner landscape is well understood; open-access terms are well documented. Execution depends on outreach response rates, which are historically 30–50% for institutional partnership requests, suggesting 8–15 signed MOUs in year one is realistic. Source-culture outreach is the highest execution risk because the stakes are highest and the relationships are not transactional.

## Spec impact

Brief 090 and 091 gain six new inventions (INV-401..406). The `partner-registry://`, `partner-report://`, and `partner-escalation://` schemes join the lineage namespaces. No substrate primitives change. Commitment #5 becomes operationally enforced via INV-403.

## Open follow-ups

- Legal review of the MOU template for US/EU/UK jurisdictions (no review yet).
- Translation of templates T3-S for source-culture institutions (English-first is insufficient).
- Compensation model mechanics for source-culture partners (grant pool budget).
- Partner onboarding automation for scale (manual outreach only works for the first 50 partners).

## Sources

- Met Museum Open Access documentation.
- Smithsonian Open Access and API terms.
- Wikimedia Cloud Services and Dumps documentation.
- Rijksmuseum API documentation.
- V&A open licensing policies.
- British Library Flickr Commons dataset.
- PubChem API terms.
- NASA open data policies.
- NIST CODATA and Chemistry WebBook.
- Hugging Face × libraries partnership retrospectives (community).
- Common Crawl institutional reviewer program documentation.
- Round 4 Briefs 086E, 088, 090, 091 for culture substrate, identity, ladder, and grounding.
