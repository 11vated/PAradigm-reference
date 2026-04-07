# 047 — INV: Zero-knowledge proof of authorship

## Question
Can GSPL invent a system where a creator proves they authored a seed *without revealing their identity* — useful for whistleblowers, activists, anonymous artists, and researchers — while still preserving the lineage and provenance guarantees that make GSPL trustworthy?

## Why it matters
GSPL's identity model (Brief 042) ties every signature to a public key. That's great for accountability but terrible for anonymity. Creators in hostile jurisdictions, victims of harassment, or researchers studying sensitive topics need a way to publish *attributable* work without being *identifiable*. The current state of the art (PGP signatures, Tor, anonymous remailers) lets you publish anonymously but breaks attribution: you can't prove later that *you* made the work without revealing yourself. ZK proofs solve exactly this. No competitor has it. GSPL can.

## What we know from the spec
- Brief 042: identity keys.
- Brief 017: signed lineage.
- ZK proofs are not yet referenced in the spec.

## Findings — the construction

### The goal in one sentence
**A creator can prove "I am the author of seed S" to anyone, at any later time, without revealing which key signed it or which identity they hold — while still allowing GSPL's verifier to confirm the proof is valid.**

### The cryptographic primitives
- **zk-SNARK** (Groth16 or Plonk): the standard for compact, fast-verification ZK proofs.
- **Pedersen commitments** for hiding the key.
- **Merkle trees** for proving membership in a set without revealing which member.

### The construction in five steps

1. **Anonymous identity creation.** The creator generates an anonymous identity: a fresh keypair. The public key is *not* published. Instead, the creator publishes a Pedersen commitment to the public key: `C = g^{pk} * h^{r}`, where `r` is a blinding factor.

2. **Anonymous publication.** The creator signs the seed with the anonymous private key, then publishes:
   - The seed itself (content-addressed as usual).
   - The commitment `C`.
   - A zk-SNARK proving "I know `pk`, `r`, and `sig` such that `C = g^{pk} * h^{r}` and `sig` is a valid ECDSA signature of the seed under `pk`."
   - **Crucially:** the public key `pk` is *not* in the proof; only the commitment.

3. **Anonymous lineage.** All operators (mutate, crossover, etc.) on this seed produce lineage entries that reference the commitment `C` instead of an identity key. The lineage DAG looks the same; only the identity is hidden.

4. **Selective de-anonymization.** Later, the creator can choose to prove they made the seed by publishing a second zk-SNARK proving "I know `r` such that `C = g^{pk} * h^{r}` for *this specific* `pk`." Anyone with the second proof + the original commitment can verify the link without the creator revealing the original blinding factor in plaintext.

5. **Threshold re-identification (optional).** The creator can also publish a "key recovery share" encrypted to a trusted third party (legal counsel, family member, archive). If they go silent for N years, the share can be used to recover the link.

### What this enables

- **Anonymous publication with later attribution.** A creator can publish work today and claim it years later (e.g., after a regime change) without being identified in the meantime.
- **Pseudonymous brand building.** A creator builds a body of work under a pseudonymous commitment; followers can verify all works are from the same anonymous author, without knowing who.
- **Whistleblower-grade publishing.** Source documents about corruption, abuse, or research misconduct can be published with cryptographic provenance but anonymous authorship.
- **Anonymous peer review.** Reviewers can prove they're qualified (membership in a credentialed set) without revealing identity.
- **Sealed authorship for testaments.** "I authored this; on my death, my recovery share is released; my heirs can prove the link."

### Anti-abuse considerations

ZK anonymous publication is dual-use. Mitigations:
- **Anonymous publication is opt-in and visually distinct in the studio.** It's not the default; users have to explicitly choose it.
- **Anonymous identities accrue *commitment-based reputation*** based on past works tied to the same commitment. A commitment is essentially a pseudonymous identity.
- **Federation peers can blocklist commitments**, the same way they blocklist identities.
- **Watermarking still applies.** Anonymous-published seeds carry watermarks tied to the commitment (not a real identity).
- **GSPL does not provide content moderation** for anonymous publications beyond what it provides for normal ones. The community is the moderator.
- **Anonymous publication of CSAM, doxxing, or weapons information is forbidden** by the AUP and is grounds for federation-wide commitment blocklisting (the commitment's reputation collapses but the underlying identity stays hidden).

## Performance and cost

- **Proof generation:** ~5 seconds on a laptop with a Groth16-style SNARK (one-time cost per anonymous publication).
- **Proof verification:** ~20ms (cheap; can be batched).
- **Proof size:** ~200 bytes.
- **Trusted setup:** Groth16 requires a trusted setup ceremony; Plonk requires only a universal setup. GSPL ships with a community-run universal setup output, with the setup audit trail published.
- **Compute cost:** marginal at v1; on-device generation works.

## Risks identified

- **Trusted setup compromise:** if the universal setup is poisoned, soundness is broken. Mitigation: community-audited multi-party computation ceremony; published setup trail; ability to migrate to a fresh setup later.
- **Cryptographic failure:** ZK constructions are subtle; bugs are catastrophic. Mitigation: use audited libraries (arkworks, halo2); third-party review.
- **Anonymity de-anonymization via metadata:** a creator may inadvertently leak identity through writing style, timing, or network traces. Mitigation: documentation warning users; anonymity is a tool, not a guarantee.
- **Quantum threat:** Groth16 is broken by quantum computers. Mitigation: post-quantum ZK migration path planned for Phase 3 (e.g., zk-STARKs).
- **Abuse of anonymity:** see anti-abuse section above.
- **Legal compliance:** some jurisdictions may demand de-anonymization. Mitigation: GSPL has no key escrow; the studio cannot de-anonymize even under legal compulsion. The threshold recovery share is *user-chosen*, not platform-controlled.

## Recommendation

1. **Adopt zk-SNARK anonymous publication** in `architecture/anonymous-authorship.md` as a v1.5 feature.
2. **Plonk over Groth16** because of the universal setup advantage.
3. **Anonymous publication is opt-in**, visually distinct, and accompanies a strong onboarding warning about metadata leakage.
4. **Commitment-based reputation** parallels identity-based reputation.
5. **Watermarking and AUP still apply** to anonymous publications.
6. **Threshold recovery shares** are user-chosen and not platform-controlled.
7. **Trusted setup ceremony is community-audited** with a published trail.
8. **Post-quantum migration path** to zk-STARKs is planned for Phase 3.
9. **Audited libraries only** (arkworks, halo2, equivalent).
10. **Third-party cryptographic review** is mandatory pre-v1.5 launch.

## Confidence
**2/5.** The cryptography exists and works, but the GSPL-specific construction is novel. The 2/5 reflects the high implementation risk, the dual-use abuse considerations, and the unverified UX. This is the most ambitious invention in the spec to date.

## Spec impact

- `architecture/anonymous-authorship.md` — full ZK construction.
- `protocols/zk-publication.md` — proof format and verification.
- `protocols/threshold-recovery.md` — optional recovery share format.
- `crypto/zk-trusted-setup.md` — ceremony spec.
- New ADR: `adr/00NN-zk-anonymous-publication.md`.

## Open follow-ups

- Audit existing ZK libraries (arkworks, halo2, snarkjs) for fitness.
- Plan the trusted setup ceremony for Phase 1.5.
- Engage cryptographic counsel for the construction review.
- UX research on the anti-de-anonymization warnings.
- Investigate zk-STARKs as the post-quantum replacement.

## Sources

- Groth, *On the Size of Pairing-Based Non-interactive Arguments* (Groth16).
- Gabizon, Williamson, Ciobotaru, *PLONK: Permutations over Lagrange-bases for Oecumenical Noninteractive arguments of Knowledge*.
- Pedersen, *Non-Interactive and Information-Theoretic Secure Verifiable Secret Sharing*.
- Ben-Sasson et al., *Scalable Zero Knowledge with no Trusted Setup* (zk-STARKs).
- Tornado Cash and Zcash for the commitment-based anonymity pattern.
- Internal: Briefs 017, 042, 045, 046.
