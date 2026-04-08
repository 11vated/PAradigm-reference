# 015 — The .gseed file format: layout, magic, sections, forward-compat

> **v0.2 PROPOSAL — NOT IMPLEMENTED IN PHASE 1.0.** The shipping `.gseed` format for v0.1 is **ADR-009** (4-byte `GSED` magic, 1-byte version, 42-byte fixed header, MessagePack-encoded canonical payload, optional zstd, optional C2PA appendix). This brief proposes a richer section-table format with per-section hashes for partial verification (better for streaming and live-content pipelines). It is queued as a **v0.2 supersede candidate for ADR-009** and is not part of Phase 1.0.

## Question
What is the on-disk binary layout of a `.gseed` file, what magic bytes and section structure does it use, and how does it handle forward-compatible extension without breaking older readers?

## Why it matters
The `.gseed` file is the canonical user-visible artifact. It must be self-describing, content-addressable, signable, embeddable in C2PA, and stable across decades of spec evolution. A bad format choice now is a 10-year tax later.

## What we know from the spec
- `spec/06-gseed-format.md` exists as a placeholder.
- Brief 005 established that the *content hash* is over the uncompressed canonical payload, not the compressed bytes.
- Brief 007 established that C2PA can use external/remote manifests for custom containers.

## Findings — the v1 format

```
+----------------------+
| Magic (8 bytes)       |   "GSEED\0\0\1"  -- 5-char ASCII + 2 reserved + version byte
+----------------------+
| Header (32 bytes)     |   format-version (u16) | flags (u16) | section-count (u16) |
|                       |   reserved (u16) | uncompressed-size (u64) | content-hash-offset (u64)
+----------------------+
| Section Index (var)   |   per section: section-id (u16) | offset (u64) | length (u64) | hash (32 bytes)
+----------------------+
| Section: SEED_JCS     |   The JCS canonical bytes of the seed object (uncompressed)
+----------------------+
| Section: SEED_BIN     |   Compact binary encoding of the same seed (optional, for fast load)
+----------------------+
| Section: SIGNATURE    |   64-byte raw r||s ECDSA + author public key (65 bytes SEC1)
+----------------------+
| Section: C2PA_REF     |   URI or sidecar reference for the C2PA manifest
+----------------------+
| Section: PREVIEW      |   Optional small thumbnail/audio preview
+----------------------+
| Section: LINEAGE      |   Optional parent IDs and breeding operator descriptor
+----------------------+
| Section: EXTENSIONS   |   TLV list for forward-compatible additions
+----------------------+
| Trailer (8 bytes)     |   "GSEEDEND"
+----------------------+
```

**Key design decisions:**

1. **Two seed encodings**, JCS canonical and binary, both included. JCS is the proof-bearing form (hashed and signed); binary is a fast-load convenience.
2. **Section index with per-section hash** enables partial verification — a reader can verify any section without parsing the whole file.
3. **Content hash is computed only over the SEED_JCS section bytes** (matching Brief 005's "hash domain is the uncompressed canonical payload").
4. **Sections have stable IDs** assigned by the spec. New section IDs are additive; readers MUST ignore unknown sections rather than fail.
5. **EXTENSIONS section uses TLV** (type-length-value) so the format itself can carry forward-compatible payloads without a section-ID assignment.
6. **Magic + trailer** make truncation detectable.
7. **Compression is optional and applied at the file level after section assembly**, not per section. The compressed file uses a `.gseed.zst` extension; readers handle both transparently. Compression is not part of the proof.

**Forward-compatibility rules:**

- Section IDs ≥ 0x8000 are mandatory: a reader that doesn't understand them MUST refuse to load.
- Section IDs < 0x8000 are optional: a reader that doesn't understand them MUST ignore.
- Format-version field allows wholesale schema bumps if ever needed; v1 = 0x0001.
- Flags field is reserved for future bits; v1 readers MUST reject any flag they don't understand.

## Risks identified

- **TLV extension misuse**: extensions become a dumping ground for vendor extensions that fragment the ecosystem. Mitigation: vendor extension IDs require a public registry entry.
- **Magic bytes collision** with another format — `GSEED\0\0\1` is unlikely to collide but should be searched against the file-format magic database before freezing.
- **Endianness**: pin everything to little-endian explicitly.
- **Section reordering**: sections must be in index order; readers must reject out-of-order sections.

## Recommendation

1. **Adopt the layout above as v1** with the section IDs assigned in `spec/06-gseed-format.md`.
2. **Maintain a public section ID registry** so third parties can reserve IDs for extensions.
3. **Provide a reference reader and writer** in Rust as the canonical implementation. A second implementation in TypeScript is strongly recommended for interop testing.
4. **Conformance test corpus** ships ≥ 100 reference `.gseed` files with documented expected hashes and signatures.
5. **Compression**: `zstd` level 19, single-thread, no dictionary (per Brief 005). The compressed form is the on-disk default; readers transparently handle both.
6. **Never reuse a section ID** even after deprecation.

## Confidence
**4/5.** The layout follows well-tested patterns from PNG (chunks), Matroska (EBML), and FlatBuffers. The 4/5 reflects (a) the unmeasured concrete byte budgets for each section and (b) the unfrozen section ID assignments.

## Spec impact

- `spec/06-gseed-format.md` — embed the layout and section ID table.
- `tests/format-conformance.md` — the corpus.
- `infrastructure/library-canon.md` — pin the reference reader/writer crate version.
- New ADR: `adr/00NN-gseed-binary-layout.md`.

## Open follow-ups

- Search the file format magic database (`/usr/share/file/magic`, libmagic) for collisions.
- Decide whether the LINEAGE section is normative or optional at v1.
- Reference reader/writer implementation. Phase 1 task.

## Sources

- PNG specification (chunk model).
- Matroska / EBML specification (extensible binary).
- C2PA Container specification.
- Internal: Briefs 003, 004, 005, 007.
