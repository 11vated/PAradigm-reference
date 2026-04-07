# ADR-009: Use a Custom .gseed Binary Format with MessagePack Core

**Status:** Accepted
**Date:** 2024-11-04
**Layer:** Layer 1 (Seed System)

## Context

A "seed" must be portable: a single file you email, attach to a GitHub PR, drag onto a marketplace, or import into the studio. The file format has to:

1. Carry the seed JSON, a SHA-256 hash of the canonicalized payload, an ECDSA-P256 signature, and optional C2PA manifest.
2. Be compact (we want seeds to be < 100 KB typical, < 5 MB worst case).
3. Self-describing, with a magic number and version.
4. Detectable as a single file type (`.gseed` extension; magic bytes for content sniffing).
5. Streamable when large.
6. Friendly to inspection in `xxd` or `hexdump` (for debugging).

## Decision

We will use a custom binary format with extension `.gseed`. The structure is:

```
[ "GSED" magic (4 bytes) ]
[ format version (1 byte, currently 0x01) ]
[ flags (1 byte) — bit0=zstd-compressed, bit1=has-c2pa-appendix, bit2-7 reserved ]
[ payload_len (uint32_le, 4 bytes) ]
[ payload_sha256 (32 bytes, raw) ]
[ signature (64 bytes, raw ECDSA r||s) ]
[ payload (MessagePack-encoded seed JSON, optionally zstd-compressed) ]
[ optional C2PA appendix (length-prefixed, only if flags bit1 set) ]
```

Total fixed header: **42 bytes** (4 + 1 + 1 + 4 + 32 = 42).

The payload is the canonical JSON of the seed, encoded as MessagePack for compactness. If the payload exceeds 4 KB, it is zstd-compressed (level 3) and the flag bit is set.

The C2PA appendix, if present, is a complete CBOR-encoded C2PA manifest as defined in the C2PA spec.

## Consequences

**Positive:**

- Magic bytes `GSED` make the format trivially identifiable. `file --magic-file=...` recognizes it.
- 42-byte fixed header is enough for cheap inspection without parsing the payload.
- MessagePack is 30-50% smaller than JSON for typical seeds, with mature libraries everywhere.
- Optional zstd compresses larger seeds (mesh genes, trained encoder weights) by another 4-10×.
- The signature is over the canonical JSON, *not* the MessagePack bytes — this means the signature survives re-encoding (anyone can decode → re-canonicalize → verify against the embedded signature).
- The C2PA appendix lives outside the signed payload, so a marketplace can add provenance metadata without invalidating the author's signature.
- File size: typical sprite seed ~5 KB, character ~15 KB, mesh-heavy ~200 KB, max practical ~5 MB.

**Negative:**

- We invented a format. We must specify it precisely (this ADR + a binary format spec doc) so other implementations can interoperate.
- MessagePack adds a dependency. Mature libraries exist in every target language but it's not part of any standard library.
- C2PA appendix length must be carefully bounded to prevent unbounded reads.

## Alternatives Considered

- **Plain JSON files:** Easy, debuggable, no special tooling. Rejected because file sizes are 2-3× larger and there's no place for the signature except as another field (ugly).
- **CBOR (RFC 8949):** Standardized binary JSON, similar to MessagePack. Strongly considered. Chose MessagePack because it's faster to parse in TypeScript and the C2PA appendix already uses CBOR (we don't want both parsers active for typical reads).
- **Protocol Buffers:** Strong schemas, fast. Rejected because seeds need to be schema-flexible (each engine adds genes), and protobuf's `Any` workaround is ugly.
- **ZIP archive:** Multi-file container. Rejected because we want a single contiguous file with a fixed-offset header.
- **glTF-style JSON+binary:** External binary blobs referenced by JSON. Rejected for the same reason — single file is easier to share.

## Format spec — full details

See [`infrastructure/gseed-format.md`](../infrastructure/gseed-format.md) (TODO) for the formal binary spec, including:

- Endianness (little-endian throughout)
- Maximum sizes per field
- Reserved bits and forward-compatibility rules
- Reference encoder/decoder pseudocode

## References

- MessagePack: https://msgpack.org
- RFC 8949: Concise Binary Object Representation (CBOR)
- C2PA Specification 1.x: https://c2pa.org/specifications/specifications/
- Zstandard: https://facebook.github.io/zstd/
