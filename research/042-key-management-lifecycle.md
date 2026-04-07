# 042 — Key management lifecycle: generation, rotation, recovery, hardware

## Question
How does GSPL manage the cryptographic keys that sign seeds, attest provenance, drive HKDF rng_seeds, and authenticate marketplace transactions — across generation, storage, rotation, recovery, and hardware-backed protection — without becoming a UX disaster for solo creators?

## Why it matters
Brief 004 established RFC 6979 ECDSA as the signing primitive. Brief 017 made content-addressed lineage depend on private keys (HKDF-derived rng_seeds). Brief 008 established C2PA-style attestations. Every one of these requires a private key to *exist*, *be protected*, *survive a laptop wipe*, and *not be stolen*. Cryptography is only useful if key management is right. Bad key UX is the #1 reason consumer crypto fails.

## What we know from the spec
- Brief 004: ECDSA P-256 + RFC 6979 deterministic.
- Brief 008: c2pa-rs attestations.
- Brief 017: HKDF-SHA256 for rng_seeds derived from private key material.
- Brief 042 (this brief): defines lifecycle.

## Findings — six lifecycle phases

### Phase 1: Key generation
- **Algorithm:** ECDSA P-256 for signing; X25519 for ECDH; HKDF-SHA256 for derivation.
- **Source of entropy:** OS CSPRNG (`getrandom(2)` on Linux, `BCryptGenRandom` on Windows, `SecRandomCopyBytes` on macOS).
- **Generation moment:** First launch of the studio. The user is walked through a 3-screen onboarding: identity → backup → confirm.
- **Identity:** display name + optional email. Stored in the local profile only; never sent to a server unless the user opts into federation (Brief 043).
- **No password at generation.** A password is added in the encryption step but is not the *source* of the key.

### Phase 2: Key storage
Three tiers, user-selectable:
- **Tier 1 — Software (default):** Key encrypted at rest with AES-256-GCM. KEK derived via Argon2id (m=64MB, t=3, p=4) from a user passphrase. Stored in the local profile under `~/.paradigm/keys/`. Cross-platform.
- **Tier 2 — OS keychain:** Key stored in macOS Keychain / Windows DPAPI / Linux Secret Service. The OS handles unlock. Better UX, OS-dependent threat model.
- **Tier 3 — Hardware:** Key generated and stored on a hardware token (YubiKey, Nitrokey, Ledger, or platform TPM/Secure Enclave). All signing happens on-device. Highest security, highest friction.

### Phase 3: Key use (signing)
- Every signing operation (seed signature, attestation, marketplace tx) goes through a single `KeyManager` interface that abstracts over the three storage tiers.
- For software/OS-keychain: key is loaded into a locked memory page, used, zeroized.
- For hardware: signing request is sent to the device; the key never leaves.
- **Per-operation unlock prompt** is configurable: always / once-per-session / once-per-N-minutes. Default is once-per-session.
- All signing operations are logged in the local provenance ledger with timestamp, operation type, target hash. Logs are append-only and themselves signed.

### Phase 4: Key rotation
- **Reasons to rotate:** suspected compromise, scheduled rotation (annual default), upgrade to a stronger algorithm.
- **Mechanism:** generate new key, sign a *rotation attestation* with the old key that says "key X is replaced by key Y as of timestamp T". The attestation is published to the local lineage and (if federated) to federation peers (Brief 043).
- **Backward compatibility:** seeds signed by the old key remain valid forever. New seeds use the new key. Verification follows the rotation chain.
- **Rotation cadence guidance:** annual for software-tier; biennial for hardware-tier; immediately for compromise.
- **The rotation chain itself is a Merkle DAG** — each rotation attestation points at the prior key's identity.

### Phase 5: Key recovery
This is the hardest part. The standard "12 word seed phrase" is too high-friction for non-crypto users; "email password reset" is impossible without a server. GSPL uses a layered approach:
- **Primary recovery: passphrase + recovery file.** At onboarding, the user generates a recovery file (a small encrypted blob containing the master seed) and is *strongly* encouraged to save it to a USB stick + a cloud drive of their choice. The file is encrypted with a *recovery passphrase* distinct from the daily passphrase.
- **Secondary recovery: BIP39 mnemonic option.** Power users can opt into a 24-word BIP39 mnemonic at generation. Stored on paper or hardware.
- **Tertiary recovery: social recovery (v2).** Shamir Secret Sharing across N trusted contacts (3-of-5 default). Requires federation infrastructure (Brief 043).
- **Tier 1 (software) keys can be recovered.** Tier 3 (hardware) keys cannot if the device is lost — only the recovery file or mnemonic recovers the *seed material*, not the on-device key. Hardware users get a strong "back up your recovery file" prompt.

### Phase 6: Key destruction
- **Voluntary:** user revokes a key. A revocation attestation is published. Existing signatures remain valid until the revocation timestamp; signatures *after* are rejected.
- **Involuntary:** device wipe. The key is gone; recovery file is the only restoration path.
- **Cryptographic erasure:** when a key is rotated/revoked, the old key material in software storage is overwritten with random bytes and the file is deleted. Best-effort on flash media.

## Risks identified

- **User loses passphrase + recovery file:** key is permanently gone; all signed seeds are still valid but no new ones can be signed under that identity. Mitigation: aggressive onboarding nudges; "test your recovery" prompt at week 1; v2 social recovery.
- **Key theft via malware:** software keys on a compromised laptop are exfiltratable. Mitigation: encourage Tier 2 (OS keychain) for default users; Tier 3 for high-value users; rotation upon suspected compromise.
- **Quantum threat:** P-256 will eventually fall to large quantum computers. Mitigation: planned migration path to ML-DSA (Dilithium) at Phase 3, with a lineage migration operator (Brief 018).
- **Argon2id parameters drift:** parameters considered safe today are weak in 10 years. Mitigation: parameters versioned in the encrypted blob; re-encryption on next unlock if version is too old.
- **HKDF reuse across operations:** if the same `info` string is used for two different derivations, they collide. Mitigation: every derivation has a unique versioned info string; namespacing enforced by `KeyManager`.
- **Hardware token vendor risk:** YubiKey/Ledger/etc. could ship compromised firmware. Mitigation: support multiple vendors; verify firmware signatures where possible.
- **Recovery file encryption is offline-attackable:** a stolen recovery file + weak passphrase = compromised. Mitigation: strong passphrase enforcement at recovery file creation (zxcvbn score ≥ 4).

## Recommendation

1. **Adopt the three-tier storage model** in `architecture/key-management.md`. Software is the default tier; OS keychain is one-click upgrade; hardware is documented and supported.
2. **All signing flows go through a single `KeyManager` abstraction.** No engine or skill touches key material directly.
3. **Argon2id with m=64MB, t=3, p=4** is the v1 KDF. Parameters versioned in the blob.
4. **Mandatory recovery file at onboarding.** The studio refuses to proceed past day 1 without one.
5. **Annual rotation reminders** for software-tier keys.
6. **Revocation and rotation attestations are immutable lineage entries.**
7. **Quantum migration planned for Phase 3** with a lineage migration operator.
8. **Per-operation unlock policy is once-per-session by default**, configurable to stricter.
9. **Test-your-recovery prompt at week 1 and month 6**, until passed.
10. **All key operations are logged in a signed append-only local ledger.**

## Confidence
**4/5.** Key management is a mature field with well-understood primitives. The 4/5 reflects honest uncertainty about UX adoption — recovery files are notoriously skipped by users.

## Spec impact

- `architecture/key-management.md` — full lifecycle spec.
- `architecture/key-storage-tiers.md` — three tiers with threat models.
- `protocols/key-rotation.md` — rotation attestation format.
- `protocols/key-recovery.md` — recovery file format and recovery flow.
- `crypto/key-derivation.md` — Argon2id and HKDF parameter spec.
- New ADR: `adr/00NN-three-tier-key-storage.md`.

## Open follow-ups

- Implement and test recovery file format end-to-end. Phase 1.
- Investigate platform Secure Enclave / Android Keystore integration. Phase 2.
- Decide on Shamir Secret Sharing library for v2 social recovery.
- UX test: how often do users actually save recovery files?
- Plan quantum migration path with PQC working group output.

## Sources

- RFC 5869 (HKDF), RFC 6979 (deterministic ECDSA), RFC 9106 (Argon2).
- BIP-39 (mnemonic), BIP-32 (HD wallets) for the recovery design pattern.
- Apple Secure Enclave documentation; YubiKey PIV documentation.
- NIST SP 800-57 (key management lifecycle).
- Internal: Briefs 004, 008, 017, 018, 043.
