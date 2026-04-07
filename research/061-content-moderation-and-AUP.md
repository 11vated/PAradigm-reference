# 061 — Content moderation and acceptable use policy

## Question
GSPL is decentralized, sovereignty-first, and has no central operator. How does it handle content moderation — preventing CSAM, NCII, doxxing, illegal weapons content, and abuse — when the architecture deliberately removes the standard moderation tools (centralized review, takedown infrastructure, account suspension)?

## Why it matters
Decentralized systems are routinely abused. The lesson of every previous decentralized creator platform is that without moderation, the worst content drives out the best — and inevitably creates legal and ethical disasters. GSPL must thread this needle: maintain decentralization, but prevent the platform from becoming a haven for the worst content. This is the hardest single problem in the spec.

## What we know from the spec
- Brief 043: federation with community blocklists.
- Brief 045: anti-piracy with reputation cost.
- Brief 047: anonymous publication with commitment-based reputation.
- The studio has no central operator.

## Findings — five-layer moderation model

### Layer 1: Acceptable Use Policy (AUP)
GSPL publishes an AUP that defines what is unacceptable. The AUP applies to:
- The studio (what users can generate locally).
- The marketplace (what can be listed).
- The federation (what can be propagated).

**Forbidden categories:**
- **CSAM:** child sexual abuse material. Zero tolerance, illegal everywhere.
- **NCII:** non-consensual intimate imagery (revenge porn, deepfake porn of real people without consent).
- **Doxxing:** publishing personal information of real individuals without consent.
- **Targeted harassment** of identifiable individuals.
- **Weapons synthesis instructions** (chemical, biological, nuclear, explosives) — even in fictional framing.
- **Real-person likeness** without consent for political deception or harassment.
- **Content that violates applicable law** (regional law applies to regional users).

**Permitted but watched:**
- Adult content (legal, consensual, watermarked, age-gated where required).
- Violent fiction (clearly fictional context).
- Politically controversial creative work.
- Likenesses of public figures in clearly creative or satirical context (fair use varies by jurisdiction).

### Layer 2: Pre-generation filters
The studio runs *local, on-device* content filters before generating output for the most clearly forbidden categories.
- **CSAM detection** via Microsoft PhotoDNA / Apple NeuralHash–style hashes (no network calls; on-device hash matching).
- **Likeness detection** for known public figures combined with deepfake detection.
- **Weapons content** keyword and embedding filters in the agent's prompt path.
- **Filters are conservative** but not the *only* defense.
- **Filters are documented and audited** for false positive rates.
- **Filters cannot be bypassed** by the user; bypass attempts are logged locally.

### Layer 3: Watermark + provenance
Every generated artifact carries a watermark (Brief 009) and a c2pa attestation (Brief 008). When abusive content surfaces, the originating identity (or anonymous commitment) is identifiable.
- **Forensic identification** is the basis for downstream community moderation.

### Layer 4: Community blocklists
Federation peers can publish signed blocklists of:
- Identities (public keys or anonymous commitments).
- Specific seed hashes.
- Topic patterns.
- IP ranges (rare; federation peers are not normally identified by IP).

Subscribers to a blocklist automatically reject content from blocked sources. Blocklists are *opt-in*, *user-curated*, and *layered* — a user can subscribe to multiple lists with different policies.

GSPL itself ships a small **default blocklist** containing:
- Known CSAM hashes (NCMEC database where available).
- Known NCII victims' likeness hashes (from ethical sources).
- Known weapons synthesis content hashes.

This default is updateable per release and can be replaced by the user.

### Layer 5: Out-of-band law enforcement
For criminal content (CSAM, doxxing, credible threats):
- The studio surfaces a "report to law enforcement" flow that prepares evidence in legally usable form (signed timestamps, content hashes, lineage).
- The user (not GSPL) submits to law enforcement.
- GSPL does not have a central abuse team; reporting flows through the user.

## What GSPL deliberately does *not* do

- **No central content review.** GSPL does not have a moderation team that reads user content.
- **No account suspension** by GSPL. Reputation is community-driven.
- **No backdoors** for de-anonymization (Brief 047).
- **No mandatory pre-screening of all content.** The pre-generation filters are limited to clearly illegal categories.
- **No upload of user content** to GSPL servers for review.
- **No takedown of already-shared content.** A revocation cannot un-distribute.

These choices are *constitutional commitments*. They follow from sovereignty.

## Dual-use tension

The same architecture that protects whistleblowers and dissidents also protects abusers. GSPL accepts this tension explicitly. The mitigation is *not* to compromise sovereignty but to:
1. Make the most-harmful content as hard to generate as possible (Layer 2 filters).
2. Make abusive identities reputationally radioactive (Layers 3-4).
3. Make criminal content provably traceable to its source (Layer 3).
4. Empower communities to moderate themselves (Layer 4).
5. Cooperate with lawful processes (Layer 5).

This is the same model as PGP, Tor, Signal, and Bitcoin — sovereignty-respecting platforms that have collectively faced and survived this debate for decades.

## Risks identified

- **Filter false positives:** legitimate art flagged as CSAM. Mitigation: conservative thresholds; user can override with review; published false positive rates.
- **Filter false negatives:** abusers find ways around the filter. Mitigation: defense in depth; community moderation as backstop.
- **Blocklist abuse:** a malicious blocklist publisher targets innocents. Mitigation: blocklist subscription is opt-in; blocklist trustworthiness is a reputation issue itself.
- **Default blocklist disagreement:** users in different cultures disagree on what should be blocked. Mitigation: the default blocklist contains only universally illegal content; everything else is opt-in.
- **Legal exposure of GSPL:** prosecutors may try to hold GSPL responsible for what users do. Mitigation: clear AUP; documented filters; cooperation with lawful processes; section 230 / Article 14 defenses.
- **Whistleblower targeting:** law enforcement uses lineage to unmask whistleblowers. Mitigation: anonymous publication mode (Brief 047) cuts the link.
- **Filter circumvention research:** publishing how to bypass filters helps abusers. Mitigation: responsible disclosure; filter improvements via private feedback channels.
- **Cultural over-reach:** Western-centric filter standards offend users elsewhere. Mitigation: filters are local and replaceable; cultural review (Brief 050).

## Recommendation

1. **Adopt the five-layer moderation model** in `architecture/content-moderation.md`.
2. **Publish a clear AUP** at `legal/aup.md`.
3. **Pre-generation filters for CSAM, NCII, weapons synthesis** at v1.
4. **PhotoDNA-style on-device CSAM detection** mandatory.
5. **C2PA provenance + watermarks** on all output.
6. **Default blocklist** for universally illegal content; replaceable.
7. **Community blocklists are first-class** in federation (Brief 043).
8. **Out-of-band law enforcement reporting flow** with evidence preparation.
9. **No central moderation, no backdoors, no takedown of already-shared content.**
10. **Filter audit reports** published quarterly.
11. **AUP review by legal counsel** in every release with substantive changes.

## Confidence
**3/5.** The model is principled and consistent with sovereignty, but moderation is the hardest unsolved problem in decentralized systems. The 3/5 reflects honest uncertainty about whether community moderation actually scales for GSPL.

## Spec impact

- `architecture/content-moderation.md` — full five-layer model.
- `legal/aup.md` — public Acceptable Use Policy.
- `protocols/blocklists.md` — blocklist format and subscription.
- `protocols/pre-generation-filters.md` — filter spec.
- `protocols/law-enforcement-reporting.md` — evidence prep flow.
- New ADR: `adr/00NN-no-central-moderation.md`.

## Open follow-ups

- Implement on-device CSAM detection (PhotoDNA license + integration).
- Engage civil liberties counsel for the AUP.
- Build the law enforcement reporting evidence prep tool.
- Plan the default blocklist source and update process.
- Quarterly filter audit process.
- UX research on the abuse reporting flow.

## Sources

- INHOPE network and PhotoDNA technical documentation.
- *No, Speech Is Not Free Online* and other content moderation literature.
- EU Digital Services Act (Article 14 hosting safe harbor).
- Section 230 of the Communications Decency Act (US).
- Internal: Briefs 008, 009, 043, 045, 047, 050, 058.
