# 090 — Agent web cross-reference and reference gathering system

## Question
How does the GSPL agent reach out to the open web to find references, images, citations, and grounding data for **anything** a user mentions — a character, a place, a material, an obscure historical detail, a niche art style — and turn those references into lineage-tracked, signed reference gseeds the substrate can compose with, while respecting privacy, copyright, trademark, source-culture restrictions, and the constitutional refusal envelope of Brief 089?

## Why it matters
The substrate's libraries (Briefs 081–088) cover the universe of measured primitives, and the conversion pipeline (Brief 089) turns user uploads into gseeds. But users will routinely mention things the substrate doesn't already know: a specific Edo-period kimono pattern, a 1973 Lagos street scene, a Yoruba folk hero whose iconography lives in archives the substrate hasn't ingested, a particular weave from a regional textile museum, a cinematographer's lens style. The agent must be able to **go find references on the open web**, ground them against the libraries, and compose them into the user's gseed — without lying, hallucinating, or laundering copyrighted content. This is the substrate's **outward sensory channel**.

## What we know from the spec
- Brief 089: conversion pipeline.
- Brief 088A: armory.
- Brief 086E: source-culture restrictions.
- Brief 077: anonymity tiers.
- Brief 074: critic ensemble.

## Findings — what reference gathering looks like at v1

### 1. The reference gseed
Every external reference the agent fetches is stored as a signed `ref://` gseed:

```
ref://image/<sha256>@v1.0
  source_url: <URL>
  fetched_at: <ISO-8601>
  fetched_by: <agent-identity>
  license: <SPDX or "unknown">
  attribution: <author/publisher>
  embeddings: <perceptual + semantic vectors>
  matched_primitives: [<library gseed URLs>]
  cultural_flags: [<sacred/restricted/contested>]
  copyright_flag: <public-domain | fair-use-claim | unknown>
  trademark_flag: <none | named-brand | named-vehicle>
  signed_by: <agent-identity>
```

References are **never** rendered into the canvas verbatim. They are grounded against library primitives and used as conditioning evidence for composition. The original is cached locally for the user's review and audit.

### 2. The reference gathering loop
When the user mentions something the substrate doesn't already have, the agent runs:

```
NEED → SEARCH → FETCH → CLASSIFY → GROUND → STORE → CITE
```

- **NEED:** the agent identifies a missing primitive ("the user said 'Nubian throne' and I have no nubian-throne primitive").
- **SEARCH:** the agent queries authoritative open sources first (museums, encyclopedias, academic, government, public-domain archives) before commercial search engines.
- **FETCH:** the agent retrieves candidate references through the sandboxed fetcher (no JavaScript execution, no cookies, no tracking).
- **CLASSIFY:** the consent classifier (Brief 089 §1) flags real-person faces, copyrighted works, trademarked content, sacred symbols.
- **GROUND:** the analyzer (Brief 089 §2) extracts features and matches them against library primitives.
- **STORE:** the reference is signed as a `ref://` gseed and lineage-linked to whatever gseed the user is composing.
- **CITE:** the agent shows the user the source URL, the license, the attribution, and the matched primitives. The user can accept, override, or reject.

### 3. Source priority ladder
The agent searches sources in priority order, preferring authoritative and openly licensed:

1. **Tier 1 — Curated open archives:** Wikimedia Commons, Internet Archive, Library of Congress, Europeana, Smithsonian Open Access, Met Open Access, V&A, Rijksmuseum, BnF Gallica, Trove, DPLA, NASA Image and Video Library, USGS, NOAA, ESA, Wellcome Collection, Biodiversity Heritage Library, Open Library, Project Gutenberg.
2. **Tier 2 — Academic and reference:** Wikipedia (with citations followed), Wikidata, Stanford Encyclopedia of Philosophy, JSTOR Open Access, PubMed Central, arXiv, OSF, Zenodo, Figshare, OpenStax, Encyclopaedia Iranica, ArchNet (Islamic architecture), HRAF eHRAF (where licensed).
3. **Tier 3 — Government and official:** UNESCO, WHO, World Bank, official government heritage sites, national libraries, national museums.
4. **Tier 4 — Authoritative news and documentation:** BBC, Reuters, AP archives, encyclopedic news sites (with date and author).
5. **Tier 5 — General web search:** only after Tiers 1–4 fail. Web results are flagged as lower-confidence and require explicit user acceptance before grounding.

The ladder is **visible to the user** — they always see which tier a reference came from.

### 4. Refusals at the reference layer
The reference fetcher refuses to retrieve, store, or compose:

- **Identifiable living persons** as character references in the foundation namespace (Brief 088 INV-343).
- **Paywalled or DRM-protected content** (no bypass).
- **Pirate sites, leaked content, scraped paywall mirrors.**
- **Sites flagged for harassment, doxing, or malicious code.**
- **Sacred-restricted cultural materials** without source-culture attribution and respect flag (Brief 086E INV-333).
- **Trademark-specific imagery** for use in named-brand gseeds (Brief 086F INV-335).
- **Weapons manufacturing schematics** (Brief 089 refusal envelope).
- **Sources known to host CSAM, even tangentially** — these are blocklisted at the fetcher.

Refusals are constitutional, not patchable.

### 5. Deduplication and the global reference cache
References are content-addressed by sha256. If two users in the federation fetch the same reference, the network shares the cached `ref://` gseed (Brief 091 will formalize). This:

- Reduces redundant web fetches.
- Builds a federated reference library over time.
- Lets the substrate accumulate a collective memory of grounded sources without anyone having to re-search.

### 6. Cross-art-style reference gathering
A common user request: "show me what a samurai looks like in the styles of: photoreal, ukiyo-e, anime, watercolor, comic, pixel art." The agent:

1. Gathers reference imagery for *historical samurai* (Tier 1 archives — Met, Smithsonian, Tokyo National Museum digital collection).
2. Grounds the references against Brief 088 character invariants (anatomy, wardrobe silhouette, distinguishing marks).
3. Composes a single character gseed using those grounded invariants.
4. Renders that gseed through every requested style adapter (Brief 088 §2), preserving identity invariants.

The user gets six coherent renders of the *same* substrate-grounded character — not six unrelated outputs from six unrelated models.

### 7. The agent's transparency contract
For every reference the agent fetches, the user sees:

- **Source URL** (clickable).
- **Tier** (1–5).
- **License** (CC0, CC-BY, public domain, fair-use claim, unknown).
- **Attribution.**
- **Cultural flag** (if any).
- **Copyright flag.**
- **Confidence in the ground match.**
- **What was extracted** vs **what was discarded** vs **what was unknown**.

Nothing the agent fetches is silently used. **Every reference is shown.**

### 8. Citation in the gseed lineage
Every gseed composed using a reference carries a permanent lineage edge to the `ref://` gseed, which carries a permanent edge to the source URL. A user months later can ask "where did the throne in this scene come from?" and the substrate will trace it back to the British Museum object record.

## Findings — agent reference gathering interaction

The agent's behavior when the user says something it doesn't know:

> User: "Make a scene with a 1920s Hindustani court musician playing a sarangi in a Lucknow palace."
>
> Agent: "I have base primitives for sarangi (audio://instrument/sarangi@v1) and Lucknow palace architecture (arch://south-asia/awadhi-palace@v1). I don't have a measured 1920s court-musician wardrobe primitive yet. Want me to search Tier 1 archives for period photographs from the British Library, V&A, and Tasveer Ghar? I'll show you what I find before I ground anything."
>
> User: "Yes."
>
> [Agent runs the reference loop, returns 8 sourced photographs from Tier 1, with attribution and licenses, grounds them against existing wardrobe primitives, surfaces gaps where it had to leave fields unbound.]
>
> Agent: "I composed a candidate `garment://south-asia/awadhi-court-musician-1920s` from these references. The angarkha cut is grounded with confidence 0.91, the turban style with 0.82, the jewelry with 0.71. The waistband knot pattern was inconsistent across references — I left it unbound. Want me to mark this as a fork or sign it as a new primitive?"

This is the interaction surface. **Negotiated, transparent, reference-cited.**

## Inventions

### INV-351: Tiered authoritative source ladder for substrate reference gathering
The agent searches a fixed priority ladder of curated open archives, academic sources, government data, and authoritative news *before* general web search, and the tier is always shown to the user. Novel because no creative tool's reference fetcher exposes a source-priority ladder as a substrate-level commitment.

### INV-352: Reference gseeds as lineage-tracked first-class substrate citizens
Every external reference becomes a signed content-addressed `ref://` gseed with license, attribution, cultural flags, and matched primitives. References are never silently consumed — they live as substrate-level citations that any future query can trace. Novel as a substrate-level external-reference provenance contract.

### INV-353: Federated reference cache as collective substrate memory
Content-addressed references are deduplicated and shared across federation peers, building a collective substrate memory of grounded sources. Each user benefits from every other user's reference gathering without needing to re-fetch. Novel as a federated reference commons.

## Phase 1 deliverables

- **Tiered source ladder** with Tier 1 sources wired at v1.
- **Sandboxed fetcher** (no JS, no cookies, no tracking) at v1.
- **Reference gseed schema** with license, attribution, cultural and copyright flags at v1.
- **Reference loop** (NEED → SEARCH → FETCH → CLASSIFY → GROUND → STORE → CITE) at v1.
- **Refusal envelope** at the fetcher at v1.
- **Federated reference cache** at v1 (consumes Brief 091).
- **Transparency surface** in the studio (Brief 079) at v1.
- **Cross-art-style reference workflow** at v1 (works with Brief 088).

## Risks

- **Source quality drift over time.** Mitigation: Tier 1 sources are versioned; refetches are content-hashed; obsolete URLs are flagged.
- **Copyright misclassification.** Mitigation: license is fetched from source metadata; unknowns are flagged; users see flag before composing.
- **Cultural appropriation through reference gathering.** Mitigation: source-culture restriction check before fetch; restricted material requires explicit attribution and respect flag.
- **Search engine bias.** Mitigation: Tier 1–4 priority before any general search; agent reports the ladder used.
- **Fetch volume / rate limits.** Mitigation: federated cache reduces redundant fetches; per-source rate limiting; respectful crawler identity.

## Recommendation

1. **Lock the Tier 1 source list at v1** with at least 25 curated archives.
2. **Build the sandboxed fetcher** as a substrate-level service.
3. **Sign every reference** as a `ref://` gseed with full provenance.
4. **Wire the federated reference cache** through Brief 091.
5. **Treat the transparency surface as non-negotiable** — every reference is shown.
6. **Engage source-archive partners** (Met, Smithsonian, V&A, Wikimedia) for crawl agreements where applicable.

## Confidence
**4/5.** Architecture is clear; partner engagement and the long-tail license classification are the engineering work.

## Spec impact

- `inventory/reference-gathering.md` — new doc.
- `inventory/source-tiers.md` — new doc.
- New ADR: `adr/00NN-tiered-source-ladder.md`.
- New ADR: `adr/00NN-reference-gseed-as-substrate-citizen.md`.

## Open follow-ups

- Tier 1 source partner outreach.
- License classification heuristic calibration.
- Reference cache eviction policy.
- Studio UI for reference transparency surface.

## Sources

- Internal: Briefs 074, 077, 086E, 086F, 088, 088A, 089, 091.
