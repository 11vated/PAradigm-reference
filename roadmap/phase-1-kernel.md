# Phase 1 — Kernel and Seed System

**Duration:** Months 1-2 (8 weeks)
**Goal:** A standalone Rust crate that produces, signs, and verifies canonical seeds with byte-for-byte reproducibility across machines.

## Why this is first

Everything depends on the kernel. The signing semantics, the canonical-form definition, the random number generator, and the algebraic effects runtime all live here. If any of these is wrong, every layer above is wrong. If any of these is *unstable*, every layer above must be rebuilt every time something changes. So we lock the kernel down first and never touch it again without a major version bump.

## Deliverables

| Deliverable | Acceptance |
|---|---|
| `kernel/` Rust crate | Builds clean, all tests pass, Clippy clean |
| `kernel/rng.rs` | Matches reference output for 1000 fixed seeds |
| `kernel/canonical.rs` | Matches RFC 8785 test vectors exactly |
| `kernel/effects.rs` | Effect tracking covers Read/Write/Random/Time/Network/GPU/Log/Sign |
| `kernel/sign.rs` | RFC 6979 deterministic ECDSA, matches NIST test vectors |
| `seeds/` Rust crate | Encodes/decodes UniversalSeed, signs seeds, hashes match |
| `gseed/` Rust crate | Round-trips `.gseed` files matching the spec in `infrastructure/gseed-format.md` |
| Test suite | ≥1000 unit tests, ≥50 property-based tests, ≥10 cross-machine reproducibility tests |
| CI pipeline | GitHub Actions runs the full suite on Linux, macOS, Windows |
| `cargo doc` output | Public API fully documented |

## Week-by-week plan

### Week 1: Project setup + RNG

- Init Cargo workspace with `kernel/`, `seeds/`, `gseed/` crates
- Configure CI: build, test, fmt, clippy, audit, deny
- Implement `xoshiro256**` core
- Implement `splitmix64` substream derivation
- Implement Box-Muller normal distribution
- Property-based tests for RNG: distribution tests, period tests, seedability
- Reproducibility tests: 1000 fixed seeds → fixed outputs

### Week 2: Canonicalization + hashing

- Implement JCS (RFC 8785) for `serde_json::Value`
- Test against the official JCS test vectors
- Implement SHA-256 wrapper with prefix handling (`sha256:` form)
- Implement RFC 7638 JWK thumbprint
- Edge cases: deeply nested objects, large arrays, NaN/Inf handling, escape sequences

### Week 3: Algebraic effects + signing

- Define `Effect` enum with all 8 variants (Read/Write/Random/Time/Network/GPU/Log/Sign)
- Implement an effect runtime that records and replays effect sequences
- Implement RFC 6979 deterministic ECDSA P-256 (use `p256` crate, not handrolled)
- Test against NIST CAVP vectors
- Document effect taxonomy in `kernel/effects.rs` doc comments

### Week 4: UniversalSeed types

- Define `UniversalSeed` struct
- Define all 17 gene types as enums + structs
- Implement `serde::Serialize` / `Deserialize` with explicit field ordering
- Define `Lineage`, `QualityVector`, `Provenance`
- Builder API for constructing seeds in tests

### Week 5: Seed canonical form + hashing

- Implement `Seed::to_canonical_json()` using JCS
- Implement `Seed::hash()` returning `sha256:<hex>`
- Test: 50 hand-crafted seeds, hashes verified against the reference Python implementation
- Test: round-trip JSON → seed → JSON → identical bytes

### Week 6: Seed signing + verification

- Implement `Seed::sign(private_key)` and `Seed::verify(public_key)`
- Test: sign 100 sample seeds, verify all
- Test: tampered seeds fail verification
- Test: signature is deterministic (same input → same signature)

### Week 7: `.gseed` format

- Implement `gseed::encode(seed, key, attachments)` per `infrastructure/gseed-format.md`
- Implement `gseed::decode(bytes)` with full validation
- Implement CRC32C, MessagePack canonical encoder, zstd integration
- Test: round-trip 100 seeds through `.gseed`
- Test: all 7 test vectors from `infrastructure/gseed-format.md` §"Test vectors"

### Week 8: Hardening + freeze

- Run the full test suite on Linux/macOS/Windows in CI
- Run with `--features=miri` to catch UB
- Run with `cargo fuzz` on the parser paths for 24 hours
- Write the public API documentation
- Release `kernel-0.1.0`, `seeds-0.1.0`, `gseed-0.1.0` (internal versions, not yet on crates.io)
- Lock the API surface — no further changes without a major version bump

## Risks and mitigations

**Risk:** ECDSA P-256 has subtle gotchas (signature malleability, low-s normalization).
**Mitigation:** Use the audited `p256` crate; never implement curve math by hand. Run NIST CAVP tests.

**Risk:** JCS edge cases around floating-point and Unicode escapes.
**Mitigation:** Use the official JCS test vector suite. Test with both ASCII and non-ASCII strings.

**Risk:** zstd is not byte-deterministic across versions.
**Mitigation:** Pin the zstd library to one version per release; verification is by hash of the *decompressed* canonical JSON, not the compressed bytes, so cross-version compatibility is preserved.

**Risk:** Cross-platform endianness or floating-point differences.
**Mitigation:** Run reproducibility tests on x86_64 and aarch64 in CI from day one.

## What is *not* in Phase 1

- No GSPL parser (Phase 2)
- No engines (Phase 3)
- No agent or LLMs (Phase 4)
- No HTTP, no database, no UI
- No marketplace logic
- No federation

The only output of Phase 1 is a set of Rust crates that other layers will depend on.

## Done definition

Phase 1 is done when:

1. All deliverables above are checked off.
2. The CI badge is green for 7 consecutive days.
3. A second engineer (or a careful re-read by the original engineer after a week off) can read the public API and write a sample program that produces a signed `.gseed` in <30 minutes.
4. The kernel public API is frozen and tagged `kernel-0.1.0`.
