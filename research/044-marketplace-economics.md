# 044 — Marketplace economics: pricing, discovery, royalties, settlement

## Question
How does the GSPL marketplace work — how seeds are listed, priced, discovered, sold, and how royalties flow through lineage — without a central operator and without becoming an NFT-style speculative casino?

## Why it matters
Creators need to get paid. Without a viable economic layer, GSPL is just a hobbyist tool. The marketplace is the bridge between sovereignty and livelihood. But marketplaces are hard: pricing discovery is brutal, royalty enforcement is contested, fraud is rampant, and the NFT space has poisoned the well for token-based content economies. GSPL must build something that actually works for working creators.

## What we know from the spec
- Brief 008: C2PA attestations and provenance.
- Brief 017: lineage with operator history and 10-hop royalty cap.
- Brief 042: identity keys.
- Brief 043: federation.

## Findings — five marketplace primitives

### 1. Listings
A **listing** is a signed attestation that says "I, identity K, offer seed S at price P, terms T, contact C." Listings are content-addressed and propagate via federation (Brief 043).
- **Listing fields:** seed_hash, price (currency, amount), license terms (use-only, derivative-allowed, commercial-allowed, redistribution-allowed), contact channel, expiry timestamp, signature.
- **Listings are not exclusive.** A seed can have multiple listings from multiple sellers (the original creator + downstream re-licensors).
- **Price is denominated in fiat currency.** No GSPL token. No crypto required.
- **Off-chain settlement** (see #4).

### 2. Discovery
- **No central marketplace UI.** Studios browse listings via federation subscriptions: "show me listings from peers I follow" / "show me listings in topic T."
- **Search uses the embedding index from Brief 031** (HNSW). A user describes what they want; the studio matches against listing seeds.
- **Ranking is local.** Each studio ranks listings via the user's preference critic (Brief 040), the global preference critic, and explicit filters (price, license, creator).
- **Featured listings via opt-in curators** (v1.5). Curators publish signed lists of recommended listings. Users subscribe to curators they trust.

### 3. Royalty flow
This is GSPL's killer feature. Lineage is content-addressed and the operator history is signed; royalty flow is *automatic* and *verifiable*.
- **Royalty rate per lineage edge:** the operator that creates an edge can attach a royalty percentage (default 0%, max 10%). When a downstream seed is sold, royalties flow upstream along the lineage path.
- **10-hop cap (Brief 017):** royalties only flow back 10 hops. Beyond that, the upstream contributors are out of the chain.
- **Royalty distribution algorithm:** the sale amount is split: seller gets `(1 - sum_of_upstream_royalties)`; each upstream hop gets its declared rate.
- **Royalty payments are settled on sale**, not promised. The buyer's settlement transaction includes payments to all upstream parties simultaneously.
- **Disputes over lineage:** rare. The lineage DAG is signed and content-addressed; falsifying it requires forging signatures.

### 4. Settlement
GSPL deliberately avoids being a payment processor. Three settlement modes:
- **Off-chain manual (v1):** the seller posts payment instructions in the listing. Buyer pays via PayPal/Stripe/wire/bank transfer. Buyer marks the order as paid; seller signs a delivery attestation; the studio verifies and unlocks the seed locally.
- **Stripe Connect / equivalent (v1.5):** integration with hosted payment processors. The studio acts as a thin client; Stripe holds the funds; royalty splits are wired through Stripe Connect's transfer API.
- **Lightning / on-chain (v2, opt-in):** for users in regions where banking is hostile or for international micropayments. Bitcoin Lightning for sub-$10 sales.
- **Settlement is decoupled from the studio.** The studio's only job is to verify a signed receipt from the chosen processor.

### 5. Trust and reputation
- **Per-identity reputation score** based on completed transactions, dispute outcomes, attestation freshness.
- **Dispute resolution is peer-mediated (v1).** A disputing buyer publishes a signed dispute attestation; sellers respond. Federation surfaces both. Bad actors get blocklisted by community-curated lists.
- **Escrow (v1.5)** via the chosen payment processor. Buyer pays into escrow; seller delivers; buyer releases.
- **Hard reputation reset is impossible** because identity is a key (Brief 042). A bad actor must rotate keys, which destroys their reputation.

## Pricing patterns

GSPL doesn't dictate pricing, but the studio offers patterns:
- **Fixed price**, the simplest.
- **Tiered license** (use-only $X / derivative $Y / commercial $Z).
- **Pay-what-you-want with floor.**
- **Subscription** (a creator publishes a "season pass" listing that grants buyers access to all their seeds in the season).
- **Bundles** (multiple seeds at a single price).

## Anti-NFT principles

Explicit design choices to avoid the NFT trap:
- **No tokens.** No speculation vehicle.
- **No artificial scarcity.** A seed can be sold to N buyers; there's no "1-of-1."
- **No on-chain provenance overhead.** Lineage is local + federated, not on a blockchain.
- **No gas fees.** Settlement is between buyer, seller, and their chosen payment processor.
- **No "floor price" tracking** as a first-class concept.
- **License terms are first-class**, not afterthoughts.

## Risks identified

- **Discovery problem:** without a central marketplace, how do new creators get found? Mitigation: curator system; embedding-based discovery; topic-based federation.
- **Payment processor risk:** Stripe/PayPal can ban creators arbitrarily. Mitigation: multi-processor support; optional Lightning fallback; manual mode always works.
- **Price discovery is brutal:** new creators don't know what to charge. Mitigation: studio shows aggregate pricing data for similar seeds (anonymized).
- **Royalty bypass:** a buyer copies a seed manually and re-lists without lineage. Mitigation: c2pa watermarks (Brief 008); reputation cost; community detection.
- **Tax compliance:** sellers are responsible for their own tax reporting. Mitigation: studio exports transaction history in tax-software-friendly format.
- **License enforcement:** GSPL can't actually stop a buyer from violating license terms. Mitigation: the social/legal layer is the enforcement, same as music/photo licensing.
- **Race to the bottom:** infinite supply of seeds → price collapses. Mitigation: differentiation via brand, lineage, curator endorsement; the marketplace is for *creators*, not commodity bulk.

## Recommendation

1. **Adopt the listing-attestation model** in `architecture/marketplace.md`.
2. **No central marketplace UI**; discovery via federation + curator subscriptions.
3. **Royalty flow follows lineage** with the 10-hop cap from Brief 017.
4. **Off-chain manual settlement at v1**; Stripe Connect at v1.5; Lightning at v2 opt-in.
5. **Prices in fiat**; no GSPL token, ever.
6. **License terms are first-class** with five default tiers (use-only, derivative, commercial, redistribution, full).
7. **Reputation is per-identity-key**, accrued from transaction history.
8. **Disputes are peer-mediated** at v1; escrow at v1.5.
9. **Pricing patterns are surfaced as templates** in the listing UI.
10. **Studio exports transaction history** in CSV / Form 1099 / equivalent.

## Confidence
**3/5.** Marketplace mechanics are well-understood; the federated/sovereign twist is unproven at scale. The 3/5 reflects honest uncertainty about discovery and bootstrap.

## Spec impact

- `architecture/marketplace.md` — full marketplace architecture.
- `protocols/listing-attestation.md` — signed listing format.
- `protocols/royalty-flow.md` — lineage-based royalty algorithm.
- `protocols/settlement-modes.md` — three settlement integrations.
- `architecture/reputation.md` — per-identity reputation accrual.
- New ADR: `adr/00NN-no-token-marketplace.md`.

## Open follow-ups

- Build the listing format end-to-end at v1.
- Stripe Connect integration spike for v1.5.
- Investigate Lightning integration libraries.
- Decide on the dispute attestation format.
- Empirical: how do existing creator marketplaces (Gumroad, itch.io) handle discovery?
- UX test: tiered license selection.

## Sources

- Gumroad and itch.io marketplace mechanics (existing creator platforms).
- Creative Commons license framework as a model for tiered terms.
- Stripe Connect documentation.
- BOLT specs (Lightning Network).
- Internal: Briefs 008, 017, 040, 042, 043, 045, 046.
