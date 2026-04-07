# ADR-002: Use JCS (RFC 8785) for JSON Canonicalization

**Status:** Accepted
**Date:** 2024-08-14
**Layer:** Layer 0 (Kernel)

## Context

To hash, sign, or compare seeds, we need a *canonical* serialization — two semantically equal JSON values must produce identical bytes regardless of formatting, key order, or whitespace. This is non-trivial because JSON is permissive (the same object can be serialized many ways) and floating-point numbers have multiple valid string representations.

We need a canonicalization that is:

1. Standardized and supported by libraries in every language we care about (TypeScript, Rust, Go, Python).
2. Designed for cryptographic use (handles edge cases that naive serializers miss).
3. Stable: the spec will not change underneath us.

## Decision

We will use JCS (JSON Canonicalization Scheme), defined in RFC 8785. Every place in Paradigm that hashes, signs, or compares JSON content will use JCS as the serialization step.

See [`algorithms/canonicalization.md`](../algorithms/canonicalization.md) for the full spec and pseudocode.

## Consequences

**Positive:**

- Cross-language interop is trivial. We have JCS libraries in all four target languages, and the RFC test vectors guarantee they agree.
- Seed hashes are stable across platforms, file systems, OS line-ending conventions, and editor reformatting.
- We inherit RFC 8785's careful handling of number edge cases (NaN, Infinity, large integers, scientific notation), which is the place naive canonicalizers all fail.
- JCS is the same canonicalization used by C2PA, COSE_Sign1, and several DID specs — we are aligned with the broader crypto-JSON ecosystem.

**Negative:**

- JCS requires UTF-16 code-unit sort, not byte sort. This is a subtle pitfall on the Rust and Go side; we must use audited library implementations.
- ECMA-262 ToString(Number) is required for floats, which not every standard library provides; some languages need a polyfill.
- Canonicalization is not free — for very large JSON documents, it adds 5-15% overhead vs naive serialization. We mitigate by canonicalizing once at write time and caching the result.

## Alternatives Considered

- **Custom canonicalization:** Tempting because we control the input shape and could simplify, but every team that has tried this has shipped subtle bugs (UTF-16 sort, number normalization, escape handling). Use a standard.
- **Protocol Buffers canonical form:** Strong, well-tested, and faster than JSON. Rejected because it requires a schema, and we want seeds to be schema-flexible at the Paradigm-extension layer.
- **CBOR Deterministic Encoding (RFC 8949 §4.2.1):** Also strong, also standardized, also faster. Rejected for ergonomic reasons: JSON is debuggable in any text editor, CBOR is not. Since seeds will be inspected by users in studio dev tools and on GitHub, plain-text wins.
- **Capnproto Canonical Form:** Same reasons as Protobuf.

## References

- RFC 8785: JSON Canonicalization Scheme (JCS)
- ECMA-262 §7.1.12.1: ToString applied to the Number type
- C2PA Specification §6.1 (which references JCS)
