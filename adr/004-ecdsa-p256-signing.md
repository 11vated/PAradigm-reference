# ADR-004: Use ECDSA P-256 with RFC 6979 for Sovereignty Signing

**Status:** Accepted
**Date:** 2024-08-20
**Layer:** Layer 0 (Kernel) — Sovereignty subsystem

## Context

Paradigm seeds carry cryptographic signatures that prove authorship and enable royalty propagation. We need a signature scheme that is:

1. **Standardized** — supported in browsers (WebCrypto), Node, and major languages.
2. **Deterministic** — same key + same message → same signature, every time.
3. **Patent-free and open** — no licensing risk.
4. **Compact** — small public keys and signatures (we embed them in seeds).
5. **Future-proof for ~10 years** — quantum threats are still distant for elliptic curves.
6. **Audit-friendly** — well-known, well-implemented, well-attacked.

## Decision

We will use **ECDSA over the NIST P-256 curve (secp256r1)** with **deterministic nonce generation per RFC 6979**, hashing with SHA-256, and signing the JCS-canonicalized JSON of the seed.

Public keys are encoded as JWK (RFC 7517) with thumbprints per RFC 7638. Signatures are encoded as raw `(r, s)` 64-byte concatenation, base64url'd for embedding in JSON.

## Consequences

**Positive:**

- Native support in WebCrypto (`SubtleCrypto.sign("ECDSA", ...)`), Node `crypto.sign`, Rust `p256` crate, Go `crypto/ecdsa`, Python `cryptography` library. All have FIPS-validated implementations available.
- 64-byte signatures, 32-byte private keys, 64-byte public keys (uncompressed). Compact enough to embed in every seed.
- RFC 6979 deterministic nonces eliminate the catastrophic "k reuse" vulnerability — there is no RNG to fail at sign time.
- JWK + thumbprint gives us a standardized identity URI we can use across the federation.
- ECDSA-P256 is already audited, attacked, and trusted by every browser, every smartphone, every TLS connection.

**Negative:**

- ECDSA verification is slower than Ed25519 (~5× slower in microseconds, but still fast enough).
- ECDSA has historical pitfalls (k reuse, weak nonce, side-channel) that we mitigate by *only* using RFC 6979 deterministic nonces and constant-time library implementations.
- P-256 is a NIST curve; some users prefer Curve25519 for political/trust reasons. We chose P-256 because WebCrypto supports it natively and Ed25519 is only newly standardized in WebCrypto (2023, not yet universal).

## Alternatives Considered

- **Ed25519:** Faster, smaller (32-byte signatures!), no nonce-reuse failure mode by design. Strongly considered. Rejected primarily because WebCrypto support is incomplete in older browsers and our target deployment (the studio web app) needs to work in 95%+ of browsers from day one. We may revisit this in 2027 when Ed25519 WebCrypto coverage hits ~99%.
- **RSA-PSS:** Mature and well-supported. Rejected because key sizes (2048+ bits) are too large to embed in every seed without dominating storage.
- **secp256k1 (Bitcoin curve):** Same security level as P-256. Rejected because WebCrypto doesn't support it; we'd have to ship a JavaScript polyfill.
- **Dilithium / Falcon (post-quantum):** Post-quantum signatures. Rejected for now because key sizes are 1-2 KB and the standards are too new. We will revisit when NIST PQC has been deployed at scale (~2028+).

## Migration plan to post-quantum

When NIST PQC signatures (ML-DSA / Dilithium) are widely deployed, we will support **dual signatures**: each seed carries both an ECDSA-P256 signature and a Dilithium signature, and verifiers can accept either. This gives a 5+ year transition window. The dual-sig format will be specified in a future ADR.

## References

- RFC 6979: Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA)
- RFC 7517: JSON Web Key (JWK)
- RFC 7638: JSON Web Key (JWK) Thumbprint
- FIPS 186-4: Digital Signature Standard
