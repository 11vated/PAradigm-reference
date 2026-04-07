# .gseed Binary Format

## Purpose

The `.gseed` file is the **portable, signed, content-addressed container** for a single canonical seed. It is the unit of exchange between Paradigm nodes, the marketplace, and third-party tools. A `.gseed` file is self-describing, verifiable offline, and round-trips losslessly to and from the canonical JSON form used by the Postgres `seeds` table.

The format is specified normatively here. Any decoder that follows this spec can read any seed produced by any Paradigm node, regardless of version.

## Design goals

1. **Self-describing.** A reader needs nothing but the file itself to interpret it.
2. **Verifiable offline.** The signature can be checked without contacting any server.
3. **Compact.** A typical sprite seed compresses to 4-12 KB; a complex composite under 64 KB.
4. **Forward compatible.** Unknown fields are preserved on round-trip.
5. **Streaming friendly.** The header can be parsed before the body is available.
6. **Single canonical encoding.** Two semantically equal seeds always produce the *same* bytes.

## File layout

```
+----------------------------------------------------------+
| Header (42 bytes, fixed)                                 |
+----------------------------------------------------------+
| Payload (variable, MessagePack, optionally zstd)         |
+----------------------------------------------------------+
| Signature block (variable, see below)                    |
+----------------------------------------------------------+
| Optional C2PA manifest block (variable)                  |
+----------------------------------------------------------+
| Optional attachment table + attachments (variable)       |
+----------------------------------------------------------+
| Footer (8 bytes, fixed)                                  |
+----------------------------------------------------------+
```

All multi-byte integers are **little-endian**. All offsets are absolute byte offsets from the start of file.

## Header (42 bytes)

| Offset | Size | Field | Type | Notes |
|---|---|---|---|---|
| 0 | 4 | `magic` | bytes | Must be ASCII `GSED` (`0x47 0x53 0x45 0x44`). |
| 4 | 1 | `version_major` | u8 | Currently `1`. |
| 5 | 1 | `version_minor` | u8 | Currently `0`. |
| 6 | 2 | `flags` | u16 LE | Bitfield, see below. |
| 8 | 8 | `payload_len` | u64 LE | Length in bytes of the payload block. |
| 16 | 2 | `payload_codec` | u16 LE | `0` = msgpack/raw, `1` = msgpack/zstd. |
| 18 | 8 | `signature_offset` | u64 LE | Absolute offset to signature block. |
| 26 | 8 | `aux_offset` | u64 LE | Absolute offset to first aux block (C2PA / attachments / 0 if none). |
| 34 | 4 | `header_crc32` | u32 LE | CRC32C of bytes [0..34). |
| 38 | 4 | `reserved` | u32 LE | Must be `0`. |

`magic` is `GSED` rather than `GSEED` so the header lands on a 4-byte boundary; the human-friendly extension `.gseed` is preserved at the filesystem layer.

### Flag bits

| Bit | Name | Meaning |
|---|---|---|
| 0 | `HAS_C2PA` | A C2PA manifest block follows the signature. |
| 1 | `HAS_ATTACHMENTS` | One or more binary attachments are appended. |
| 2 | `IS_DRAFT` | Seed is unsigned and not canonicalized; tooling only. |
| 3 | `IS_FEDERATED` | Seed originated from another federation node (origin in payload). |
| 4 | `IS_MARKETPLACE` | Seed is associated with a marketplace listing. |
| 5–15 | reserved | Must be `0`. |

## Payload block

The payload is the **canonical seed JSON** encoded as MessagePack, optionally compressed with zstd.

### Canonicalization

Before encoding, the seed is canonicalized exactly as for signing:

1. JCS (RFC 8785) on the JSON form: keys sorted lexicographically, no whitespace, `\u` escapes only where required, integers encoded without trailing zeros, floats in shortest round-trip form.
2. The canonical JSON is then encoded to MessagePack via a deterministic encoder: maps are written with sorted keys (matching JCS order), integers use the smallest sufficient int family, floats use `f64` always, strings use UTF-8.

This dual-canonical (JSON-canonical and MessagePack-canonical) approach is intentional: the JSON canonical form is what gets *hashed* and *signed*, while the MessagePack form is what is *transmitted*. A reader recovers the JSON canonical form by decoding MessagePack and then re-applying JCS to validate.

### Compression

If `payload_codec == 1`, the MessagePack bytes are wrapped in zstd with the following fixed parameters:

- Level: 9
- Dictionary: none (single-shot)
- Frame format: zstd skippable frames disallowed
- Checksum: enabled

The zstd parameters are pinned so that two encoders given the same input produce the same compressed bytes. (zstd is not formally byte-deterministic across versions, but pinning to a single encoder version per release of Paradigm achieves it in practice. Decoders MUST verify the recovered MessagePack against the JSON-canonical hash regardless of compression.)

### Hash

The `hash` field of the seed (used as the database primary key in `seeds.hash`) is `SHA-256(JSON-canonical bytes)`, encoded as lowercase hex with prefix `sha256:`.

## Signature block

```
+--------+--------+--------+--------+--------+
| algo   | klen   | key id (klen)            |
+--------+--------+--------+--------+--------+
| siglen | signature (siglen bytes)          |
+-----------------------------------+
```

| Field | Type | Notes |
|---|---|---|
| `algo` | u8 | `1` = ECDSA P-256 / SHA-256 (currently the only supported value). |
| `klen` | u8 | Length of key id in bytes. |
| `key_id` | bytes | RFC 7638 JWK thumbprint (SHA-256 over the canonical JWK). 32 bytes for the current algo. |
| `siglen` | u16 LE | Signature length. |
| `signature` | bytes | ECDSA signature in `r || s` form. 64 bytes for `algo == 1`. |

The signed bytes are the SHA-256 of the **JSON-canonical** payload, signed deterministically per RFC 6979.

Verification:

```
fn verify(file: &[u8]) -> Result<()>:
    let header = parse_header(file)?
    let payload = file[42 .. 42 + header.payload_len]
    let json_canonical = decode_payload(payload, header.payload_codec)?
    let digest = sha256(json_canonical)
    let sig_block = parse_signature_block(file, header.signature_offset)?
    let pubkey = lookup_pubkey(sig_block.key_id)?
    return ecdsa_verify(pubkey, digest, sig_block.signature)
```

`lookup_pubkey` consults the local trust store first, then the network resolver if online. Offline verification with a known author works without any external lookup.

## C2PA manifest block

If `HAS_C2PA` is set, a C2PA manifest follows the signature block (or starts at `aux_offset` if there are no attachments).

```
+--------+--------+--------+
| 'C2PA' (4 bytes magic)   |
+--------+--------+--------+
| len (u32 LE)             |
+--------------------------+
| manifest bytes (CBOR)    |
+--------------------------+
```

The manifest is a standard C2PA CBOR manifest, signed independently with a Paradigm-controlled C2PA signing key. See `compliance/c2pa.md` for the manifest content (assertions, claim generator, etc.).

Important: the C2PA signature is **separate** from the seed signature. The seed signature attests authorship; the C2PA signature attests provenance for downstream content authenticity tools (Adobe, social platforms, browsers).

## Attachment table + attachments

If `HAS_ATTACHMENTS` is set, an attachment block follows.

```
+--------+--------+--------+
| 'ATCH' (4 bytes magic)   |
+--------+--------+--------+
| count (u32 LE)           |
+--------------------------+
| entry[0]                 |
| entry[1]                 |
| ...                      |
+--------------------------+
| blob[0]                  |
| blob[1]                  |
| ...                      |
+--------------------------+
```

Each entry is:

| Field | Type | Notes |
|---|---|---|
| `name_len` | u8 | UTF-8 byte length of the attachment name. |
| `name` | bytes | Attachment name (e.g., `preview.png`). |
| `mime_len` | u8 | UTF-8 byte length of MIME type. |
| `mime` | bytes | MIME type (e.g., `image/png`). |
| `offset` | u64 LE | Absolute offset of the blob's first byte. |
| `length` | u64 LE | Blob length. |
| `sha256` | 32 bytes | SHA-256 of blob bytes. |

Attachments hold previews and exports that are derived from the seed but are too large to embed in the canonical payload. Common attachments:

- `preview.png` — 256×256 PNG render
- `preview.webp` — 256×256 WebP render (smaller for browsers)
- `audio_preview.opus` — 5s audio preview for music seeds
- `mesh_preview.glb` — low-res GLB for 3D seeds

The attachment hashes are NOT included in the seed signature. They are integrity-checked individually via their `sha256` fields. This is intentional: attachments can be regenerated, replaced, or stripped without invalidating the seed signature.

## Footer (8 bytes)

| Offset | Size | Field | Notes |
|---|---|---|---|
| –8 | 4 | `total_crc32c` | CRC32C of bytes [0..filesize-8). |
| –4 | 4 | `magic_end` | ASCII `GEND` (`0x47 0x45 0x4E 0x44`). |

Reading the last 8 bytes lets a tool verify a `.gseed` file is complete without parsing the header. The CRC is integrity-only; security comes from the ECDSA signature.

## Encoding (write path)

```
fn write_gseed(seed: Seed, signing_key: PrivateKey, attachments: List<Attachment>) -> bytes:
    // 1. Canonicalize
    let json_canonical = jcs_canonicalize(seed.to_json())
    let digest = sha256(json_canonical)
    let payload = msgpack_canonical(json_canonical)
    let payload_codec = 0u16
    let payload_bytes = payload
    if payload.len() > 1024:
        payload_bytes = zstd_compress(payload, level = 9)
        payload_codec = 1u16

    // 2. Sign
    let signature = ecdsa_sign_rfc6979(signing_key, digest)
    let key_id = jwk_thumbprint(signing_key.public)

    // 3. Layout
    let header_size = 42
    let payload_offset = header_size
    let signature_offset = payload_offset + payload_bytes.len()
    let sig_block = serialize_signature_block(key_id, signature)
    let aux_offset = signature_offset + sig_block.len()
    let aux_blocks = []
    if seed.has_c2pa: aux_blocks.append(serialize_c2pa(seed))
    if attachments: aux_blocks.append(serialize_attachments(attachments))

    // 4. Header
    let mut header = [0u8; 42]
    header[0..4]   = b"GSED"
    header[4]      = 1; header[5] = 0
    header[6..8]   = flags(seed, attachments).to_le_bytes()
    header[8..16]  = (payload_bytes.len() as u64).to_le_bytes()
    header[16..18] = payload_codec.to_le_bytes()
    header[18..26] = (signature_offset as u64).to_le_bytes()
    header[26..34] = (aux_offset as u64).to_le_bytes()
    header[34..38] = crc32c(header[0..34]).to_le_bytes()
    header[38..42] = [0,0,0,0]

    // 5. Concatenate
    let body = header ++ payload_bytes ++ sig_block ++ flatten(aux_blocks)
    let footer_crc = crc32c(body).to_le_bytes()
    let footer = footer_crc ++ b"GEND"
    return body ++ footer
```

## Decoding (read path)

```
fn read_gseed(bytes: &[u8]) -> Result<Seed>:
    if bytes.len() < 50: return Err("too short")
    if &bytes[0..4] != b"GSED": return Err("bad magic")
    if &bytes[bytes.len()-4..] != b"GEND": return Err("bad end magic")

    let header = parse_header(&bytes[0..42])?
    if crc32c(&bytes[0..34]) != header.header_crc32: return Err("bad header crc")

    let body_end = bytes.len() - 8
    let total_crc = u32::from_le_bytes(bytes[body_end..body_end+4])
    if crc32c(&bytes[0..body_end]) != total_crc: return Err("bad file crc")

    let payload_end = 42 + header.payload_len
    let payload = &bytes[42..payload_end]
    let json_canonical = match header.payload_codec:
        0 => msgpack_decode_canonical(payload)?
        1 => msgpack_decode_canonical(zstd_decompress(payload)?)?
        _ => return Err("unknown payload codec")

    let sig_block = parse_signature_block(&bytes[header.signature_offset..])?
    let pubkey = lookup_pubkey(sig_block.key_id)?
    let digest = sha256(&json_canonical)
    if !ecdsa_verify(pubkey, digest, sig_block.signature):
        return Err("signature failed")

    let seed = Seed::from_canonical_json(&json_canonical)?
    return Ok(seed)
```

## Size budget

A typical sprite seed measured in bytes:

| Section | Size |
|---|---|
| Header | 42 |
| Payload (msgpack canonical) | ~3 KB |
| Payload (msgpack + zstd) | ~1.4 KB |
| Signature block | 100 |
| C2PA manifest (optional) | ~2 KB |
| `preview.png` (256×256, optional) | ~30 KB |
| `preview.webp` (256×256, optional) | ~10 KB |
| Footer | 8 |
| **Total (no attachments)** | **~3.5 KB** |
| **Total (with previews)** | **~45 KB** |

Composite seeds (3D scenes, full music tracks) can reach a few hundred KB even without attachments, dominated by the gene tree.

## Versioning

The format uses (major, minor) versioning:

- **Major** bumps are breaking. A reader for major `N` MUST reject files with major `> N`.
- **Minor** bumps add fields or flag bits. A reader for major `N` minor `M` MUST tolerate files with minor `> M` by ignoring unknown flag bits and skipping over aux blocks with unknown magics.
- The current version is **1.0**.

Future minor bumps under 1.x are reserved for: additional `aux_block` magics (e.g., `LIN ` for embedded lineage proofs), new compression codecs (Brotli is candidate), and multi-signature support.

A future major bump (2.0) is reserved for post-quantum signatures (see ADR-004 §"Post-quantum migration").

## Test vectors

The reference implementation ships with a fixed set of test vectors in `tests/gseed-vectors/`:

1. `minimal.gseed` — empty payload (`{}`) with default flags. Tests the smallest valid file.
2. `sprite-bard.gseed` — the canonical "melancholy bard" sprite seed used throughout the docs.
3. `compressed-large.gseed` — a 50 KB payload to verify zstd round-trip.
4. `with-c2pa.gseed` — includes a C2PA manifest.
5. `with-attachments.gseed` — includes preview.png and preview.webp.
6. `tampered-payload.gseed` — payload modified post-signing; verification MUST fail.
7. `tampered-header.gseed` — header CRC mismatch; parse MUST fail.

Conforming implementations must pass all 7 vectors.

## References

- ADR-009 — chose this format
- RFC 8785 — JSON Canonicalization Scheme (JCS)
- RFC 6979 — Deterministic ECDSA
- RFC 7638 — JWK Thumbprint
- MessagePack spec — https://github.com/msgpack/msgpack/blob/master/spec.md
- zstd RFC 8878
- C2PA 2.0 specification — https://c2pa.org/specifications/specifications/2.0/
