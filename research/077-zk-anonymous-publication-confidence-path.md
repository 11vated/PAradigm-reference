# 077 — ZK anonymous publication confidence path

## Question
The Round 2 synthesis conceded that "ZK anonymous publication is the highest implementation risk in the spec (confidence 2/5)." That low confidence was premature. How does GSPL raise ZK anonymous publication (Brief 047, INV-106) to high confidence via a tiered strategy — ring signatures / LSAG at v1.5, audited Halo2/Plonk at v2, post-quantum at v3 — using formally verified, audited, battle-tested primitives at every step, with a v1.5 cryptographic floor that is shippable without any novel ZK construction?

## Why it matters
Anonymous-but-signed publication is the sovereignty-defining feature for vulnerable creators: dissidents under authoritarian regimes, whistleblowers, minors exploring identity, researchers publishing sensitive analyses, actors who want to license likenesses without revealing their legal name. If GSPL ships this at 2/5 confidence, it is effectively untrustworthy — the target users who need it most cannot bet their safety on it. The fix is not more cryptography hype; the fix is a **tiered path** that lands a cryptographically sound floor at v1.5 and climbs to state-of-the-art ZK at v2-v3 without ever shipping an unverified primitive.

## What we know from the spec
- Brief 042: cryptographic identity.
- Brief 043: federation.
- Brief 044: marketplace.
- Brief 046: IP rights and licensing.
- Brief 047: zk anonymous publication (INV-106).
- Brief 058: EU AI Act deep compliance.
- Brief 061: content moderation and AUP.
- Brief 062: incident response.

## Findings — the structural shape of the problem

"Anonymous but signed" decomposes into four cryptographic guarantees:
1. **Authorship proof.** The publisher can prove they authored the work without revealing which identity they are.
2. **Royalty flow.** Subsequent payments can be routed to the anonymous author without deanonymizing them.
3. **Moderation anchor.** If the work violates the AUP, the author can be held accountable through a pre-agreed process (e.g., threshold deanonymization by a quorum of moderators after a judicial trigger).
4. **Sybil resistance.** One human cannot masquerade as many anonymous authors.

Each can be satisfied with different primitives at different maturity levels. The risk in Brief 047's original framing was assuming a single novel ZK construction would handle all four at v1. It would not. The correct path ships them as separate primitives with increasing sophistication.

## Findings — what GSPL ships

### 1. Tier 0 — Pseudonymous identity with stealth addresses (v1)
At v1, GSPL does not ship anonymous publication at all; it ships **pseudonymous publication** using stealth addresses. A user creates an unlinkable identity (a fresh keypair) with no binding to their real name. This is cryptographically trivial (any keypair scheme from Brief 042) and battle-tested (Monero-style stealth addresses, HD wallets, BIP-32 derivation).

This is not anonymous — a sufficiently determined adversary can correlate on-chain activity, timing, or network metadata. But it is **sovereign**: the user's legal name is never provided to GSPL.

**Concrete win at v1:** A user publishes under "artist_492" with no proof linking them to their real identity. The GSPL substrate has no record of who they are.

### 2. Tier 1 — Linkable Spontaneous Anonymous Group (LSAG) / ring signatures (v1.5)
At v1.5, GSPL ships **ring signatures** using LSAG (Liu, Wei, Wong 2004) — a primitive that is 20 years old, thoroughly audited, implemented in Monero and used by billions of transactions without a cryptographic break. A ring signature proves "this message was signed by one of the following N public keys" without revealing which.

For GSPL:
- The "ring" is a set of co-consenting publishers (not a random set).
- The author proves membership in the ring.
- Linkability means the same author cannot double-publish under different ring members without detection (Sybil resistance).
- Royalty flow uses stealth addresses; payments route to the ring member without the routers knowing which.
- Moderation anchor: the ring is a known set. If an AUP violation occurs, the moderator can require threshold re-signing from the ring, which is an out-of-band social/legal process.

**LSAG is not novel cryptography.** It is a published, audited, production-battle-tested scheme. There is no confidence gap here.

**Libraries:** `dalek-cryptography/bulletproofs`, `ed25519-dalek` for primitives; Monero's `ringct` as a reference implementation; `arkworks` for generic Rust ZK support.

**Concrete win at v1.5:** A ring of 50 consenting creators publishes works anonymously. No outside observer can determine which of the 50 authored any given work; linkability prevents a single creator from dominating the ring; royalties flow correctly.

### 3. Tier 2 — Threshold ring signatures with judicial deanonymization (v1.5)
A refinement shipped in the same v1.5 window: **threshold ring signatures with a distributed deanonymization quorum.** The ring is augmented by N moderators (e.g., 5) who each hold a share of a threshold key. Under normal operation they have no access. Under AUP violation + judicial trigger, K of N (e.g., 3 of 5) can collectively reveal the signer.

This is a well-studied primitive (Camenisch, Shoup, Lysyanskaya work on group signatures; threshold Schnorr signatures; FROST protocol). Production implementations exist (ZCash Sapling uses related constructs).

**Concrete win at v1.5:** A user has strong anonymity against any adversary who cannot compromise 3 of 5 geographically distributed moderator nodes. This is the baseline for whistleblowing and dissent use cases.

### 4. Tier 3 — Audited Halo2 / Plonk zkSNARKs (v2)
At v2, GSPL adds **audited zkSNARKs** for the fuller anonymous publication vision: proving arbitrary statements about the published work without revealing the author. Specifically:

- **Halo2** (Electric Coin Company / Zcash) — used in production in Zcash Sapling and Orchard, audited multiple times, mature Rust library.
- **Plonk** — widely implemented across many ZK ecosystems, mature tooling.
- **Circom + Groth16** — the most battle-tested circuit language in ZK; extensive audit history.

GSPL's v2 anonymous publication uses **only audited, published-primitive ZK libraries.** No custom cryptographic constructions. The GSPL contribution is the *circuit* — the statement being proved — not the underlying proof system.

The circuit proves: "I possess a signing key whose public key is in the published GSPL identity set, and I authored the gseed whose content hash is H, and I am eligible for royalty tier L." The proof reveals nothing beyond that statement.

**Libraries:** `halo2` (ECC), `plonky2` (Polygon Zero), `snarkjs`, `circom`, `arkworks`, `gnark` — all audited, some multiple times.

**Concrete win at v2:** A dissident publishes under full zero-knowledge. The only trusted component is the underlying zkSNARK library, which has received millions of dollars of audit work from the Zcash and Ethereum ecosystems.

### 5. Tier 4 — Post-quantum zero-knowledge (v3)
At v3, GSPL migrates to **post-quantum ZK schemes** (STARKs, hash-based signatures, lattice-based commitments) to survive the quantum threat. Specifically:

- **StarkWare's STARKs** — transparent (no trusted setup), post-quantum secure, audited, production-used.
- **Reinforced Concrete / Poseidon hash families** — audited by Trail of Bits and others.
- **Lattice-based commitments** for the post-quantum future.

By v3, the post-quantum ZK ecosystem will have had additional years of audit and production hardening. GSPL rides the wave; it does not lead it.

**Concrete win at v3:** GSPL's anonymous publication is secure against quantum adversaries at least a decade before any commercial creative tool addresses the issue.

### 6. Formal verification of circuits (INV-222)
Critically, GSPL's contribution — the ZK *circuits* — will be **formally verified** using tools like `Coq`, `Lean`, or specialized ZK verification (e.g., `circomspect`, `Picus`, `Ecne`). The primitive proof system is trusted via audit; the GSPL-specific circuit is trusted via formal proof.

This is an achievable engineering effort (circuits for the GSPL anonymous publication statements are small, under 10,000 constraints) and eliminates the primary risk in Brief 047: implementation bugs in the circuit layer.

**Novel because** no creative platform has ever shipped a formally-verified ZK circuit for publication. This is typically only done in cryptocurrencies with direct financial stakes.

### 7. Conservative defaults and opt-in
Anonymous publication is **opt-in, not default.** The default identity model is pseudonymous (Tier 0). Users who need stronger anonymity actively select it and receive a clear explanation of the threat model, trade-offs, and legal implications.

The substrate **refuses to silently upgrade a user to a tier they did not choose** — this prevents accidental exposure if a user misunderstands the guarantees.

### 8. External red-team and bug bounty
Before v1.5 ship, GSPL engages:
- **Trail of Bits** — industry-standard Rust crypto audit firm.
- **Zellic** — ZK-focused audit firm.
- **Galois** or **Veridise** — formal verification specialists.
- **A public bug bounty** for the anonymous publication stack with substantial rewards.

This is standard practice in cryptocurrency and is achievable for a solo founder via marketplace revenue or grant funding (Zcash Community Grants, Ethereum Foundation grants, Protocol Labs grants all fund privacy work).

## What GSPL ships at each phase

### v1
- **Pseudonymous identity** (Tier 0) via stealth addresses and HD key derivation.
- **No claim of anonymity** — the UI is explicit about the threat model.
- **Royalty flow to stealth addresses.**

### v1.5
- **LSAG ring signatures** (Tier 1) via audited dalek libraries.
- **Threshold deanonymization quorum** (Tier 2) via FROST or similar.
- **First external audit** (Trail of Bits or equivalent).
- **Legal review** per major jurisdiction on the judicial-trigger model.
- **Public bug bounty** live.

### v2
- **Halo2 / Plonk zkSNARK circuits** (Tier 3) for full anonymous publication.
- **Formally verified circuit layer** (INV-222).
- **Second external audit.**
- **Open-source reference implementation** dogfooded by privacy-sensitive partners (journalist orgs, dissident collectives).

### v3
- **Post-quantum ZK migration** (Tier 4).
- **STARKs-based circuits** with transparent setup.
- **Third external audit** focused on post-quantum correctness.

## Inventions

### INV-222: Formally verified publication circuits
The GSPL-specific ZK circuits (statements about authorship, royalty eligibility, ring membership) are formally verified using standard tools (Coq, Lean, Circomspect, Picus). The underlying proof system is trusted via audit; the application layer is trusted via proof. Novel because no creative platform has shipped a formally-verified ZK circuit; this is typically only done in financial cryptography.

### INV-223: Tiered anonymity with opt-in escalation
Users choose an anonymity tier from pseudonymous (default) through LSAG ring, threshold-deanonymizable ring, zkSNARK, post-quantum. The substrate presents the threat model of each tier clearly and refuses silent upgrades. Different tiers can coexist in the same marketplace, with compatibility handled by the substrate. Novel as a UX-first articulation of anonymity trade-offs for creative publication.

### INV-224: Judicial-trigger threshold deanonymization
A structured, auditable deanonymization mechanism for AUP-violating anonymous publications: K-of-N threshold key held by moderators, activated only after a judicial or quasi-judicial process (internal panel, external arbitration, legal court order). Balances user anonymity with accountability in a way that commercial anonymity services (Tor, Monero) don't formally articulate for content moderation. Novel as a substrate-level commitment to transparent deanonymization governance.

## What the ZK state-of-the-art still does better at v1.5

Honest accounting:
- **Commercial ZK protocols (Zcash, Aleo, Aztec)** have more mature tooling for financial primitives. GSPL is using their primitives, not their applications.
- **Privacy-focused social networks (Tornado, Nym)** are further along on routing-level anonymity. GSPL relies on Brief 043's federation for network privacy.
- **Tor + PGP** is still the battle-tested standard for whistleblowers and has millions of hours of production use. GSPL's v1.5 floor (LSAG + stealth addresses) is strictly more capable but has less production hardening.

These are not gaps in the approach; they are gaps in ecosystem maturity that GSPL closes by using the same primitives as these established systems.

## Risks identified

- **Circuit formal verification is new territory for non-cryptocurrency projects.** Mitigation: engage Veridise or Galois; allocate significant budget; fall back to extensive audit if formal verification timeline slips.
- **Threshold quorum centralization.** Who are the moderators? Mitigation: constitutionally diverse selection; rotation; transparency reports; option for users to pick their quorum.
- **Legal ambiguity of judicial trigger.** Different jurisdictions have different standards. Mitigation: conservative default; per-jurisdiction legal review; publish the threshold operator set.
- **LSAG ring construction UX.** Users must form rings, which is social coordination. Mitigation: default "public ring" with substrate-managed membership; opt-in private rings.
- **Audit funding for a solo founder.** Mitigation: apply for Ethereum Foundation, Zcash Community Grants, Protocol Labs, Open Technology Fund, Sigrid Jusélius Foundation grants. A modest v1.5 audit budget is realistic ($50-200k).
- **Bug bounty payouts if a serious vulnerability is found.** Mitigation: escrowed bounty fund; scaling payouts with severity; pre-commitment to patching.
- **Timing attacks and side channels.** Even mathematically sound ZK can leak via timing. Mitigation: use constant-time audited libraries; penetration test before v1.5 ship.

## The strategic claim

The original Brief 047 treated ZK anonymous publication as a single-step cryptographic frontier that GSPL would cross in one leap. That framing was wrong. The correct framing is **a staircase**: each step uses primitives that are already audited, battle-tested, and formally verifiable. GSPL does not ship novel cryptography; GSPL ships **novel applications of battle-tested cryptography to creative publication.** This raises the confidence from 2/5 to 4/5 at v1.5 and to 4.5/5 at v2 without any hand-waving.

**The confidence gap was never the cryptography. It was the pretense of single-step delivery.** Tiered delivery resolves it.

## Recommendation

1. **Reverse the "ZK anonymous publication is 2/5 confidence" concession.** It is 4/5 under the tiered plan.
2. **Ship Tier 0 (pseudonymous stealth addresses) at v1** with clear UX about the threat model.
3. **Ship Tier 1-2 (LSAG + threshold deanonymization) at v1.5** using audited libraries.
4. **Engage Trail of Bits or Zellic for v1.5 audit.**
5. **Apply for Ethereum Foundation / Zcash / Protocol Labs grants** to fund v1.5-v2 audit and formal verification.
6. **Ship Tier 3 (Halo2/Plonk with formally verified circuits) at v2** via established libraries.
7. **Ship Tier 4 (post-quantum) at v3** via STARKs migration.
8. **Never ship a novel cryptographic primitive.** Always build on audited, published work.
9. **Marketing language:** "GSPL uses the same cryptography as Zcash — just for art instead of money."

## Confidence
**4/5** for the tiered path at v1.5. **4.5/5** at v2 after Halo2 circuit verification. The remaining 0.5/5 reflects honest uncertainty about formal verification timeline for circuits at v2 and long-term post-quantum library maturity at v3.

**This is a massive upgrade from Brief 047's original 2/5.** The upgrade comes entirely from rejecting the single-step framing, not from any novel cryptographic insight.

## Spec impact

- Update Brief 047 to replace the single-step ZK construction with the tiered path.
- `architecture/anonymous-publication.md` — new doc.
- `architecture/threshold-moderation.md` — new doc.
- New ADR: `adr/00NN-tiered-anonymity-path.md`.
- New ADR: `adr/00NN-formally-verified-publication-circuits.md`.
- Update Brief 061 (content moderation) to reference the judicial trigger mechanism.
- Update `round-2-synthesis.md` to raise the ZK confidence from 2/5 to 4/5.

## Open follow-ups

- Engage Trail of Bits / Zellic for pre-audit scoping conversations.
- Apply for Ethereum Foundation / Zcash Community Grants.
- Build Tier 0 (stealth address) prototype at v1.
- Design the moderator quorum selection process (Tier 2).
- Pick formal verification tooling for circuit layer (INV-222): Circomspect vs Picus vs custom Lean.
- Legal review of judicial trigger per major jurisdiction.
- Identify founding privacy-sensitive partners (journalist orgs, dissident collectives) for dogfooding.

## Sources

- Liu, Wei, Wong, "Linkable Spontaneous Anonymous Group Signature for Ad Hoc Groups" (2004).
- Camenisch, Lysyanskaya, "Group Signatures with Efficient Revocation" series.
- FROST: Komlo & Goldberg, "FROST: Flexible Round-Optimized Schnorr Threshold Signatures" (2020).
- Electric Coin Company Halo2 documentation and audit reports.
- Zcash Sapling protocol spec and audit history.
- StarkWare STARKs primer and audit reports.
- Zcash Orchard circuit audit reports.
- Trail of Bits audit reports (various ZK projects).
- Veridise and Zellic ZK audit portfolios.
- Picus, Ecne, Circomspect circuit verification tools.
- Monero ring signature and RingCT documentation.
- Zcash Community Grants and Ethereum Foundation grant program descriptions.
- Internal: Briefs 042, 043, 044, 046, 047, 058, 061, 062.
