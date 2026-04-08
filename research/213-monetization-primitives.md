# 213 — Monetization primitives

## Question
What is the typed monetization surface that enables substrate creators to support purchases (one-time, DLC, subscription, in-app), in-game currencies, and storefront integration across the eight engine targets, without locking creators into a centralized payment processor and with PII boundaries preserved?

## Why it matters (blast radius)
Monetization is the existential question for any commercial creator. Without typed primitives, every creator integrates Steam / Apple / Google billing independently, leaks PII, and the substrate's compliance story breaks at the payment edge. The brief specifies the typed monetization surface as substrate-provided structure with creator-managed payment processors.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 158 — save snapshot model.
- Brief 187 — mod surface.
- Brief 210 — account and identity surface (PII boundary).
- Brief 212 — live content pipeline.

## Findings
1. **Monetization as typed gseed.** `monetization.def` declares: typed product list, pricing tiers per region, processor adapter selection, currency definitions (in-game currencies if any), entitlement schema.
2. **Product types.** Substrate ships four typed product kinds: **one-time** (single purchase, permanent entitlement), **dlc** (content unlock with associated update bundle from Brief 212), **subscription** (time-bound entitlement with renewal logic), **iap** (consumable in-game currency or item).
3. **Processor adapter pattern.** `processor.adapter` typed gseed declares the implementation: built-in adapters for Steam, Epic, Apple App Store, Google Play, Microsoft Store, Itch.io, plus a creator-extensible adapter for custom processors. Substrate handles the platform-specific flow per engine target; creators write zero payment code.
4. **PII boundary.** Same as Brief 210: substrate handles only opaque transaction identifiers, never card numbers, email addresses, billing addresses. PII lives entirely in the platform processor's domain. Substrate runtime cannot read it.
5. **Entitlement as typed gseed.** Successful purchase emits typed `entitlement.grant` mutation appended to player identity (Brief 210) listing which products are owned. Entitlement check is a typed predicate substrate runtime queries before unlocking content.
6. **In-game currency.** Optional `currency.def` typed gseed declares: name, max balance, exchange rules. In-game currency is a typed `wallet.balance` field on player identity. Substrate provides typed `currency.add` / `currency.spend` mutations with overflow / underflow validation.
7. **Anti-cheat for IAP.** In-game currency mutations from non-purchase sources (achievements, gameplay) are typed and signed. Server-authoritative for multiplayer (Brief 209); client-authoritative with lineage signing for single-player (cheating only affects the cheater).
8. **Receipt validation.** Each purchase produces a typed `purchase.receipt` gseed signed by the processor. Substrate verifies receipts via processor adapter. Failed validation rejects the entitlement.
9. **Refund handling.** Processors can revoke entitlements after refund. Substrate listens for `entitlement.revoke` events from processor adapters and applies inverse mutations.
10. **Subscription renewal.** Subscription entitlements expire at typed timestamps; substrate runtime queries the processor adapter for renewal status before each session.
11. **Region-aware pricing.** `pricing.tier` declares per-region prices via typed currency code; processor adapter handles display per platform conventions.
12. **Validation contract.** Sign-time gates: at least one processor adapter declared, all products have valid pricing tiers, currency definitions have non-negative max balances, entitlement schema valid.
13. **Loot boxes / gambling.** Substrate provides primitives but does not endorse gambling mechanics. Creators implementing loot boxes must comply with regional gambling laws (creator responsibility); substrate documents the legal exposure.

## Risks identified
- **Processor API churn.** Platform billing APIs change frequently. Mitigation: substrate ships processor adapters versioned with substrate releases.
- **Receipt validation security.** Local receipt validation is bypassable. Mitigation: server-side validation via processor's web API for high-value products; documented as creator-required for subscriptions.
- **Region pricing complexity.** Currency conversion and tax compliance vary. Mitigation: substrate provides typed pricing tiers; creators set per-region prices manually; substrate doesn't auto-convert.
- **Loot box legal exposure.** Gambling laws vary by region. Mitigation: substrate documents the risk; creators are legally responsible for compliance.
- **Console certification.** Console platforms require certification for IAP. Mitigation: substrate's console adapters are deferred to v0.5 with platform certification.

## Recommendation
Specify monetization primitives as typed `monetization.def` + `processor.adapter` + `entitlement.grant` + `currency.def` gseeds with built-in adapters for 6 major platforms, server-side receipt validation for subscriptions, region-aware pricing tiers, refund handling via inverse mutations, and PII boundary at the processor edge. Ship loot box primitives but document legal responsibility as creator-side.

## Confidence
**4 / 5.** Monetization mechanics are well-precedented; the novelty is the typed processor adapter pattern with substrate-managed flow per engine target. Lower than 4.5 because per-platform certification (console especially) needs platform-specific Phase-1 work.

## Spec impact
- New spec section: **Monetization primitives specification**.
- Adds typed `monetization.def`, `processor.adapter`, `entitlement.grant`, `entitlement.revoke`, `currency.def`, `wallet.balance`, `purchase.receipt`, `pricing.tier` gseed kinds.
- Adds the PII boundary at the processor edge.
- Adds creator-responsibility documentation for loot box compliance.
- Cross-references Briefs 152, 158, 187, 209, 210, 212.

## New inventions
- **INV-907** — Typed `monetization.def` with creator-selectable processor adapter: monetization is a first-class substrate primitive with pluggable platform integration.
- **INV-908** — Six built-in processor adapters (Steam / Epic / Apple / Google / Microsoft / Itch.io) shipped per substrate release: platform billing complexity is substrate-managed.
- **INV-909** — Typed `entitlement.grant` and `entitlement.revoke` mutations on player identity: entitlements are signed substrate state, not opaque DRM.
- **INV-910** — Typed `currency.def` with overflow/underflow validation: in-game currencies are first-class typed primitives with structural anti-cheat.
- **INV-911** — Typed `purchase.receipt` with processor signature verification: receipts are structured substrate artifacts verifiable post-hoc.
- **INV-912** — PII boundary at the processor edge mirroring Brief 210: substrate never sees payment PII; creators / processors handle it entirely.
- **INV-913** — Region-aware typed `pricing.tier` field with creator-managed per-currency prices: pricing is structured creator data, not framework auto-conversion.

## Open follow-ups
- Console processor adapters (Xbox, PlayStation, Nintendo) — deferred to v0.5.
- Cryptocurrency / blockchain processor adapters — explicitly out of scope (substrate non-goal).
- Subscription tier upgrade/downgrade flows — deferred to v0.3.
- Refund automation — deferred to v0.3.
- Tax compliance (VAT, sales tax) helpers — deferred to v0.4.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 187 — Mod and plugin surface.
3. Brief 210 — Account and identity surface.
4. Brief 212 — Live content pipeline.
5. Steamworks IAP documentation.
6. Apple StoreKit documentation.
7. Google Play Billing Library documentation.
8. Itch.io API documentation.
