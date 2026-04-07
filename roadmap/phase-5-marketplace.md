# Phase 5 — Marketplace, Federation, and Launch

**Duration:** Months 11-12 (8 weeks)
**Goal:** v1.0 — a federated, monetized creative platform. Users can list seeds, buy seeds, federate with other Paradigm nodes, and the public verifier is live.

## Why this is last

The marketplace and federation depend on every layer below: signed seeds (kernel), valid output (engines), high-quality content (agent), a UI to interact with (Studio). Building the marketplace earlier would mean rebuilding it as the lower layers stabilize. The federation protocol depends on the seed format being final, which only happens after Phase 1's freeze sticks through several rounds of usage.

## Deliverables

| Deliverable | Acceptance |
|---|---|
| Marketplace database tables | All listings/sales/royalty tables in Postgres |
| Stripe Connect onboarding | Sellers can connect Stripe accounts |
| Listing flow in Studio | Author lists a seed for sale |
| Buy flow in Studio | Buyer purchases a seed and downloads `.gseed` |
| Royalty distribution worker | Lineage-based royalty splits paid out automatically |
| Federation peer protocol | Peers can subscribe and exchange signed seeds |
| Federation gateway service | uWebSockets.js, scaling to 10K concurrent peers |
| Public verifier | `paradigm.app/verify` accepts uploads, returns C2PA + watermark verdict |
| Public seed pages | `paradigm.app/s/<hash>` shows canonical seed + lineage tree |
| Launch landing page | Marketing site with the value prop |
| Final security audit | External pen test, all critical findings fixed |
| Final accessibility audit | External WCAG audit, AA confirmed |
| v1.0.0 release | Tagged, documented, deployed to production |

## Week-by-week plan

### Week 1: Marketplace database + Stripe Connect

- Migrations: `listings`, `sales`, `royalty_payouts` (already in `db-schema.md`)
- Stripe Connect onboarding flow
- Webhook handlers for `account.updated`, `payment_intent.succeeded`, `transfer.created`
- Seller dashboard skeleton
- Test: complete a $1 sandbox transaction end-to-end

### Week 2: Listing + Buy flow in Studio

- "List for sale" button on seed detail page
- Listing form: price, currency, royalty percent, license
- Buy button on public seed pages
- Stripe Checkout integration for the buyer
- Receipt page with signed `.gseed` download

### Week 3: Royalty distribution

- Lineage walker: from sold seed → ancestor seeds → recipients
- Royalty calculation per `algorithms/functor-composition.md` weights
- Worker that processes `sales` events and creates `royalty_payouts` rows
- Stripe Transfers API integration
- Test: a 3-generation lineage with 3 different authors all receive correct splits

### Week 4: Federation protocol

- Federation peer registration (`federation_peers` table)
- WebSocket protocol per `architecture/federation.md` (TODO if missing)
- Subscribe / unsubscribe / publish messages
- Signature verification on every inbound seed
- Trust store: which peers we trust automatically
- Cross-node test: two local Paradigm instances exchange seeds

### Week 5: Federation gateway + public verifier

- `federation-gateway` service on uWebSockets.js
- Connection pooling, rate limiting, abuse defenses
- Public verifier endpoint and minimal HTML UI
- C2PA verification + watermark detection in the verifier
- Test: 10 known-good and 10 known-bad files

### Week 6: Public pages + landing site

- `/s/<hash>` public seed page: canonical JSON, lineage tree, attachments, links
- `/verify` public tool
- `/accessibility` accessibility statement
- `/legal/*` terms, privacy, AUP, EU representative
- Marketing landing page with value prop, pricing, demo video

### Week 7: External audits

- Send the system to a third-party security firm for pen testing
- Send the Studio to an accessibility audit firm
- Fix every critical finding in flight
- Document residual issues with severity and timeline

### Week 8: Launch

- Final go/no-go review
- Production deployment (Argo Rollouts, canary)
- Status page (`status.paradigm.app`) live
- Press / blog post drafted
- Discord/community channel opened
- v1.0.0 tagged, released, announced

## Risks and mitigations

**Risk:** Stripe Connect onboarding has a long manual review for high-risk countries.
**Mitigation:** Launch with restricted geographies initially (US, EU, UK, Canada, Australia), expand later.

**Risk:** Federation protocol exposes a new attack surface (untrusted peers sending malicious seeds).
**Mitigation:** Strict signature verification on every inbound message; trust store is opt-in; rate limits per peer; sandboxed seed validation.

**Risk:** Royalty distribution math has rounding errors at scale.
**Mitigation:** Use integer cents everywhere; sum-of-payouts must equal `royalty_pool_cents` exactly; reconciliation job runs hourly.

**Risk:** External audits surface critical findings late.
**Mitigation:** Run informal internal audits in week 5 to surface as much as possible before the formal audit.

**Risk:** Launch traffic overwhelms the MVP infrastructure.
**Mitigation:** Pre-scale to 4× normal capacity for launch week; CloudFlare in front; soft launch (Discord) before press.

## What is *not* in Phase 5 (post-v1.0)

- Mobile apps
- Native desktop clients
- The remaining 20 domain engines (we ship 6 in v1)
- Multi-region active-active
- Fine-tuned in-house models
- Enterprise SSO
- Plugin / extension marketplace (vs the seed marketplace)

These all become roadmap items for v1.x and v2.0 post-launch.

## Done definition

1. v1.0.0 is tagged.
2. Production is up, dashboards green, error rate <0.5%.
3. A real external buyer has bought a real seed for real money and received a signed `.gseed`.
4. A second Paradigm node has federated with the first and exchanged at least one seed.
5. The public verifier correctly identifies a Paradigm export and rejects a non-Paradigm one.
6. External security audit critical findings: 0.
7. External accessibility audit confirms WCAG 2.2 AA.
8. Launch announcement is published.

That is v1.0. Everything after is v1.x or v2.0.
