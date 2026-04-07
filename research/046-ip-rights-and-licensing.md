# 046 — IP rights and licensing model

## Question
How does GSPL handle intellectual property — who owns a seed, who owns its derivatives, what rights are licensed in a sale, how do training-data IP issues interact with the AI Act, and how does the lineage system encode all of this?

## Why it matters
IP is the legal substrate of every creator economy. GSPL's lineage system encodes *what was made* and *how it was made*; the IP layer must encode *who has what rights*. Get this wrong and the marketplace is a lawsuit factory. Get it right and GSPL is the cleanest provenance story in generative AI history.

## What we know from the spec
- Brief 008: c2pa-rs attestations.
- Brief 010: EU AI Act compliance.
- Brief 017: lineage with operator history.
- Brief 044: marketplace listings with license terms.

## Findings — five IP layers

### Layer 1: Authorship
Authorship of a seed is recorded in the lineage entry as the *signing identity* of the creating operator. Multiple authors are possible via co-signed lineage entries.
- **Original authorship:** the identity that signed the seed creation operator (`emit_seed`).
- **Derivative authorship:** the identity that signed the operator producing the derivative (`mutate`, `crossover`, `compose`).
- **Co-authorship:** multiple identities signing the same lineage entry. All co-authors are listed in the entry.
- **Attribution is permanent and verifiable** via signature, content addressing, and the lineage DAG.

### Layer 2: Ownership
Authorship and ownership are *distinct*. Authorship is a fact (who made it); ownership is a right (who controls it). Ownership transfers through licenses and transfers.
- **Default ownership = original author.**
- **Transfers** are signed attestations: "I, A, transfer all rights in seed S to B." Recorded in the lineage as a non-content edge.
- **Co-ownership** is supported: multiple owners with declared shares.
- **Ownership controls listing rights** (who can sell), revocation rights (where applicable), and license issuance.

### Layer 3: License
A license is what a buyer gets when they pay. GSPL ships with five default license tiers, modeled loosely on Creative Commons:
- **L1 — Personal Use Only:** the buyer may render and use the seed for personal projects only. No commercial use, no derivatives.
- **L2 — Commercial Use:** L1 + the buyer may use renders in commercial projects. No derivatives, no resale.
- **L3 — Derivative Allowed:** L2 + the buyer may evolve the seed (mutate, crossover) and sell the derivatives, subject to royalty flow.
- **L4 — Full Commercial:** L3 + the buyer may sublicense and resell the seed itself.
- **L5 — Public Domain Dedication:** the seller waives all rights, equivalent to CC0.

Sellers can also write **custom licenses** as plain text attached to the listing. The five defaults are *machine-readable*; custom licenses are not (humans must read them).

### Layer 4: Derivatives and royalty flow
When a buyer with an L3+ license creates a derivative and sells it, royalties flow upstream along the lineage (Brief 017, Brief 044). This is enforced *socially* (visible in the lineage; non-payment is a reputation hit) and *technically* where settlement processors support split payments (Brief 044).
- **Royalty rates are declared at sale time**, not at seed creation time. The seller of seed S sets the royalty for derivatives.
- **The 10-hop cap** ensures royalty chains don't grow unbounded.
- **Royalty bypass is possible but reputationally expensive.**

### Layer 5: Training data and the AI Act
GSPL is *generative substrate*, not a trained model. Most of the IP-from-training-data issues that plague image diffusion models don't apply directly. But:
- **Learned critics (Brief 040)** are trained on data. Their training data must be licensed appropriately.
- **AURORA encoders (Brief 036)** ditto.
- **Bootstrap exemplar archives** ditto.
- **The studio ships with a license declaration** for every shipped model: data sources, license, training date, model card.
- **AI Act Article 53 transparency obligations** are met by publishing the training data summary for every shipped model.

GSPL's model cards are *cryptographically signed* and bundled with the engine release; users can inspect them in-studio.

## Authorship attribution UX

Every output the studio renders includes (visibly or accessibly):
- The seed's identity hash.
- The list of upstream authors via lineage.
- The license under which the output is delivered.
- Any custom attribution requirement (e.g., "Credit: J. Doe").

## Disputes

- **Authorship disputes:** rare, because authorship is signature-bound. A claim that "I really made this first" requires either invalidating the existing signatures (cryptographically infeasible) or showing the signature was made by a stolen key (key compromise → revocation flow, Brief 042).
- **License disputes:** more common. A buyer alleges they had broader rights than the seller granted. Mitigation: license terms are signed and timestamped; the lineage entry is the authoritative record.
- **Derivative disputes:** "you copied my style without my permission." Style is not copyrightable in most jurisdictions; GSPL doesn't try to enforce this.
- **Trademark and persona rights:** GSPL doesn't validate that a seed isn't infringing a trademark or right of publicity. The seller is responsible. Listings with obvious infringements are blocklist-worthy.

## Public domain and CC interop

- **L5 (Public Domain Dedication)** is intentionally CC0-equivalent.
- Sellers can attach Creative Commons license URLs as custom licenses; the studio recognizes the standard CC URLs and displays them with appropriate icons.
- Public domain seeds get a **PD badge** in the studio.

## Risks identified

- **License language ambiguity:** the five defaults are short and may be challenged in court. Mitigation: ship plain-language explanations; include legal review for v1 launch.
- **Cross-jurisdictional IP differences:** what counts as fair use in the US is different in the EU. Mitigation: the license is contractual; the contract overrides default law where possible.
- **Training data IP exposure:** if a learned critic was trained on un-licensed data, every seed it scored is downstream-tainted. Mitigation: data provenance for all shipped models; exemplar archives are licensed-only at v1.
- **Derivative-of-derivative ambiguity:** at hop 11+ (past the cap), is the contributor still entitled to attribution? GSPL says yes (attribution, not royalty). Mitigation: lineage entries always show the full chain.
- **Persona rights and likeness:** generating an image of a real person via SpriteEngine could violate right of publicity. Mitigation: documented in the AI Act compliance brief (Brief 010); seller responsibility; engine-side content filters at v2.
- **License revocation impossibility:** once a license is granted, it cannot be unilaterally revoked. Some sellers will want this; GSPL says no, by constitutional commitment.

## Recommendation

1. **Adopt the five-tier license model** (L1-L5) in `architecture/licensing.md`.
2. **Authorship is signature-bound** and recorded in lineage entries.
3. **Ownership is distinct from authorship** and transferred via signed attestations.
4. **Royalty flow follows lineage** with the 10-hop cap (Brief 017).
5. **Custom licenses are supported** but only the five defaults are machine-readable.
6. **All shipped models have signed model cards** with training data declarations.
7. **CC license interop** via standard URL recognition.
8. **Public domain badging** for L5 seeds.
9. **License revocation is impossible** by constitutional commitment.
10. **Legal review of the five license tiers** is mandatory pre-launch.

## Confidence
**3/5.** The model is conservative and grounded in existing IP frameworks. The 3/5 reflects honest uncertainty about cross-jurisdictional enforcement and the legal review outcome.

## Spec impact

- `architecture/licensing.md` — full IP layer architecture.
- `protocols/license-tiers.md` — five default tiers in detail.
- `protocols/ownership-transfer.md` — transfer attestation format.
- `architecture/model-cards.md` — shipped model card format.
- `legal/license-language.md` — the actual license text (legal review required).
- New ADR: `adr/00NN-five-tier-license-model.md`.

## Open follow-ups

- Engage IP counsel for L1-L5 language review. Phase 0 (pre-launch).
- Build the model card format and tooling. Phase 1.
- Decide on the persona/likeness content filter strategy. Phase 2.
- Investigate Creative Commons license URL canonical list.
- Decide on the dispute resolution flow for license disputes (peer mediation? arbitration?).

## Sources

- Creative Commons license framework.
- WIPO Copyright Treaty.
- EU AI Act Articles 50, 53 (transparency).
- Andersen v. Stability AI and similar ongoing cases.
- Internal: Briefs 008, 010, 017, 040, 042, 044, 045.
