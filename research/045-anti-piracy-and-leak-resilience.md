# 045 — Anti-piracy and leak resilience

## Question
How does GSPL make piracy unattractive (not impossible — that's a fool's errand) and how does it stay resilient when seeds inevitably leak?

## Why it matters
Every digital good is pirated. The question isn't whether GSPL seeds will be pirated — they will be — but whether the *legitimate* path is meaningfully better, and whether the platform survives when copies escape. The history of DRM is the history of failed attempts to make digital goods uncopyable. GSPL takes a different stance: legitimate access is *richer* than pirated access, not just legally distinct from it.

## What we know from the spec
- Brief 008: c2pa-rs attestations and content provenance.
- Brief 009: watermarks for content traceability.
- Brief 017: lineage with signatures.
- Brief 044: marketplace with reputation and royalty flow.

## Findings — five anti-piracy strategies (none of them are DRM)

### 1. Lineage-bound utility
A pirated seed is a *flat file*. A legitimate seed is *part of a lineage* — it can be bred, mutated, evolved, and its descendants have provenance. Pirated seeds break the lineage chain because they have no signed parent edge connecting them to the buyer's identity.
- **Concrete impact:** a pirate can render the asset, but they cannot legitimately *evolve* it within their own studio without forging signatures. Their derivative work has no provenance and cannot be sold legitimately.
- **Why this matters more for GSPL than for other media:** GSPL's value is in the *generative substrate*, not the rendered output. Pirating the rendered output is like pirating a single frame from a movie — useful but a fraction of the value.

### 2. Watermarked outputs (Brief 009)
Every rendered output from a legitimate seed carries a perceptual watermark that encodes the buyer's identity hash + the seed lineage. This is *forensic* watermarking, not access control.
- **Removable?** Yes, with effort. The watermark survives JPEG compression, mild crops, color shifts, and re-rendering. A determined attacker can strip it; a casual pirate cannot.
- **What it enables:** if a leaked output appears online, the watermark identifies who leaked it. Their identity is then publicly tied to the leak; their reputation collapses; their key is community-blocklisted.
- **Plausible deniability:** mitigated by signed delivery attestations (Brief 044) — a buyer cannot claim "I never bought it."

### 3. Reputation cost
The GSPL identity (Brief 042) is the user's reputation anchor. A user caught laundering pirated seeds loses their reputation. Their listings stop being trusted. Their creator livelihood evaporates.
- **Reputation is local to communities, not global.** A pirate can find communities that don't care, but they're cut off from the productive creator economy.
- **Reputation transfers nowhere.** A new identity starts at zero.

### 4. Service value beyond the seed
Legitimate buyers get:
- **Critic ensembles** trained on the seed family — improves their own derivative work.
- **Updates** via lineage migration when the engine version changes.
- **Composition recipes** from the seller (Brief 028 cross-engine patterns).
- **Direct support channel** with the creator.
- **Inclusion in curator endorsements**.

A pirate gets the seed and nothing else. As GSPL matures, the *seed-plus-everything* bundle becomes harder to pirate because the everything part is service-delivered.

### 5. Cheap and abundant legitimate access
The most effective anti-piracy is making legitimate access cheap and frictionless. Strategies:
- **Pay-what-you-want** patterns lower the price barrier (Brief 044).
- **Bundles and subscriptions** at low effective per-seed cost.
- **Free tier seeds** as loss-leaders for paid downstream.
- **Educational pricing** for students.
- **Geographic price differentiation** via the seller's choice.

## Leak resilience

Leaks happen. Resilience strategies:

### Forensic leak attribution
When a leak is detected (community report, automated scan, watermark detection):
1. The studio scans the leaked artifact for watermarks.
2. The buyer identity is recovered.
3. A signed leak report is published to federation.
4. The buyer's reputation is downgraded; community blocklists may add them.
5. The seller can revoke that buyer's future access.

### Lineage forking
A widely-leaked seed can be *forked*: the original creator publishes a new version with a different lineage and the leaked version becomes a stale dead-end. The new version has the latest critics, the latest improvements, and the latest community attention.
- **Forking is cheap** because GSPL is generative — the creator doesn't have to redraw, they just re-evolve.
- **The leaked old version doesn't compete** because it's stale.

### Community moderation
Federation peers (Brief 043) can publish blocklists of known-pirate identities and known-leaked seed hashes. Subscribing to these lists is opt-in. Centralized enforcement is impossible; community-curated enforcement is feasible.

### Insurance pricing
Creators can price in expected leak losses, the same way physical-goods retailers price in shoplifting. The marketplace surfaces estimates of leak rates per seed category.

## What GSPL deliberately *does not* do

- **No DRM.** No encrypted runtime; no hardware attestation requirement; no online activation.
- **No call-home.** Studios work fully offline.
- **No "feature unlocks"** based on payment status.
- **No revocation of already-delivered seeds.** A seed sold yesterday remains usable forever, even if the buyer's reputation collapses.
- **No legal threats as a primary strategy.** Lawyers are a last resort.

## Risks identified

- **Watermark stripping:** sophisticated attackers can defeat perceptual watermarks. Mitigation: multi-layer watermarks (visible signature + perceptual + steganographic); ongoing watermark research as a research-track investment.
- **Identity laundering:** a pirate creates a fresh identity for each leak. Mitigation: reputation accrual takes time; new identities are explicitly low-trust in the studio UI; seller-side throttling on new-identity buyers.
- **Mass leak via marketplace breach:** if a seller's account is compromised, all their seeds leak at once. Mitigation: hardware key tier (Brief 042); per-listing rotation; key compromise revocation.
- **Reputation systems are gameable:** sybil attacks on positive reviews. Mitigation: reviews are signed; review weight is proportional to reviewer reputation; community curators surface trusted reviewers.
- **Curator bribery:** curators can be paid to endorse junk. Mitigation: curator reputation; multiple curators per topic; user can audit curator history.
- **The free-rider problem:** a small fraction of buyers fund the whole ecosystem. Mitigation: this is the same as every creator economy; subscription models help.

## Recommendation

1. **Adopt the five-strategy anti-piracy model** in `architecture/anti-piracy.md`. Lineage-bound utility is the headline.
2. **No DRM, no call-home, no runtime activation.** Ever. This is a constitutional commitment.
3. **Forensic watermarking is mandatory** on all rendered outputs at v1 (Brief 009).
4. **Leak attribution flow** is documented and supported by the studio.
5. **Community blocklists are first-class** in federation (Brief 043).
6. **Reputation cost is enforced** by community curation and federation visibility.
7. **Lineage forking is supported as a first-class operator** in the marketplace.
8. **Educational pricing tier** is suggested as a default in the listing UI.
9. **No revocation of delivered seeds.** Constitutional commitment.
10. **Watermark stripping resistance** is a research track for v2.

## Confidence
**3/5.** The strategy is sound conceptually but unproven empirically for a generative-asset marketplace. The 3/5 reflects honest uncertainty about how much piracy actually happens and how much it actually costs creators in this context.

## Spec impact

- `architecture/anti-piracy.md` — full anti-piracy strategy.
- `protocols/leak-attribution.md` — forensic flow and signed leak reports.
- `protocols/lineage-forking.md` — forking operator.
- `architecture/community-blocklists.md` — blocklist format and subscription.
- New ADR: `adr/00NN-no-drm-commitment.md`.

## Open follow-ups

- Multi-layer watermarking research (Phase 2).
- Decide on the leak report attestation format.
- Build the lineage forking operator (Phase 1.5).
- UX test: how do creators set educational pricing?
- Investigate adversarial watermark attacks and current best defenses.

## Sources

- Doctorow, *DRM is About Restricting Users, Not Piracy* (the philosophical anchor).
- Cox et al., *Digital Watermarking and Steganography* (textbook).
- itch.io's pay-what-you-want experience as empirical anchor.
- Internal: Briefs 008, 009, 017, 042, 043, 044.
