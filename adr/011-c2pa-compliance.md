# ADR-011: Embed C2PA Manifests in All Exported Artifacts

**Status:** Accepted
**Date:** 2025-01-18
**Layer:** Cross-cutting (export, compliance, sovereignty)

## Context

Two regulations are coming into force during Paradigm's MVP timeframe:

- **EU AI Act, Article 50** (effective August 2026) — requires synthetic content to carry machine-readable provenance metadata.
- **California SB 942** (effective January 2026) — requires disclosure of AI-generated material in commerce.

Independent of regulation, Paradigm's whole identity is "AI-assisted, but provenance-verified." We *want* our outputs to advertise their lineage, not hide it.

The de facto standard for content provenance is **C2PA** (Coalition for Content Provenance and Authenticity), backed by Adobe, Microsoft, BBC, NYT, Sony, and many others. C2PA defines a manifest format (CBOR over COSE-Sign1) that embeds in image metadata (PNG iTXt chunks, JPEG XMP/Exif), audio metadata, video containers, and PDF.

## Decision

Every artifact exported from Paradigm carries an embedded C2PA manifest. This applies to:

- PNG, JPEG, WebP, GIF, AVIF (image exports)
- MP3, FLAC, WAV, OGG (audio exports)
- MP4, WebM (video exports)
- glTF, USDZ, FBX (3D exports — embed in metadata extensions)
- PDF (embed via XMP)
- HTML5 game zips (embed a `c2pa.json` next to the index.html)
- `.gseed` files (embed in the appendix per ADR-009)

The manifest claims:

- **Author:** the user's sovereignty public key (JWK thumbprint).
- **Created with:** "Paradigm GSPL Engine vX.Y.Z"
- **Generation method:** "trainedAlgorithmicMedia" (the standard C2PA enum for AI-assisted content).
- **Source seeds:** the lineage chain — every parent seed hash, every functor applied.
- **Signature:** ECDSA-P256 over the manifest, by the user's sovereignty key.
- **Optional consent flag:** whether the user has opted in to use of the artifact for training other AI models (default: no).

The manifest is deterministic given the seed and the export settings — a re-export produces a byte-identical manifest (modulo timestamp, which is fixed to the seed's logical time).

## Consequences

**Positive:**

- Day-one compliance with EU AI Act Article 50 and California SB 942.
- Verifiable lineage: anyone with the C2PA tool can drag a Paradigm export onto contentcredentials.org and see its full history.
- Aligns Paradigm with the largest provenance coalition in the world; we benefit from their tooling, viewers, and browser support as it grows.
- Author control: the user can choose to be anonymous (sign with a one-time key) or to assert identity (sign with their long-term sovereignty key).
- Strong defense if a Paradigm output is later misattributed or claimed by someone else — the manifest is cryptographically tied to the original creator.

**Negative:**

- C2PA libraries are still maturing. The official Rust crate (`c2pa-rs`) is the main implementation; we ship it as a WASM module in the studio. JavaScript bindings exist but are larger than ideal (~500 KB gzipped).
- Manifest adds 2-10 KB to most exports. Negligible for files > 100 KB but noticeable for tiny PNG sprites. We provide a "lightweight" mode for sprite atlases that uses an external sidecar manifest instead of an embedded one.
- C2PA is non-deterministic by default (uses walltime). We pin the timestamp to seed-logical-time and use deterministic ECDSA per ADR-004 to make it reproducible.

## Privacy choices

Users have three sovereignty modes for C2PA signing:

1. **Identified** — sign with the long-term sovereignty key. Public, attributable.
2. **Pseudonymous** — sign with a stable per-channel key. Attributable to the channel but not to the human.
3. **Anonymous** — sign with a one-time ephemeral key. Not attributable.

The default is **Pseudonymous** to balance accountability with privacy.

## Alternatives Considered

- **No provenance metadata:** Easier but illegal under upcoming regulation, and contrary to Paradigm's identity.
- **IPTC PhotoMetadata only:** Insufficient — not signed, not lineage-aware, not the regulatory standard.
- **XMP custom namespace:** We could roll our own. Rejected because it would not be recognized by mainstream tools.
- **C2PA + IPTC + XMP all together:** Belt and suspenders. We may add this later; for MVP, C2PA is enough.

## References

- C2PA Specification 1.x: https://c2pa.org/specifications/specifications/
- EU AI Act, Article 50 — Provenance and Transparency
- California SB 942 — California AI Transparency Act
- Content Credentials viewer: https://contentcredentials.org/verify
