# C2PA Content Credentials

## What it is

The Coalition for Content Provenance and Authenticity (C2PA) defines an open technical standard for cryptographically signed provenance metadata that travels with media files. A C2PA manifest is a CBOR-encoded structure embedded inside an image, video, audio file, or other media container that records:

- Who or what created the content
- When and how it was created (camera, AI model, editing tool)
- What edits have been applied since creation
- A digital signature binding all of the above to a verifiable identity

C2PA is the technical foundation underneath Adobe's "Content Credentials," and it is the specific mechanism cited by EU AI Act Article 50 and California SB 942 as an acceptable form of "machine-readable provenance."

Paradigm implements **C2PA 2.0** in every export and in every `.gseed` file (see `infrastructure/gseed-format.md` §"C2PA manifest block").

## Why it matters

A C2PA manifest is the only way Paradigm can satisfy three obligations at once:

1. **Regulatory:** EU AI Act Art. 50 and CA SB 942 explicitly accept C2PA as proof of synthetic-content disclosure.
2. **Trust:** Downstream platforms (Adobe, Microsoft, BBC, social networks) check C2PA on upload and surface a "Content Credentials" badge to viewers.
3. **Provenance chain:** Edits made in Adobe, Affinity, Krita, or any other C2PA-aware tool extend the manifest rather than break it; the seed → render → edit → publish chain stays connected.

A seed without a manifest would be functionally indistinguishable from any other AI image and would fail compliance audits.

## Manifest structure

A Paradigm C2PA manifest contains the following assertions:

| Assertion | Source | Purpose |
|---|---|---|
| `c2pa.actions` | Built per export | Lists every step (created, processed, ai_generated, signed). |
| `c2pa.ingredients` | From lineage edges | Lists parent seeds that contributed (for derivative content). |
| `c2pa.thumbnail.claim.jpeg` | Engine render | A small thumbnail of the content. |
| `c2pa.training-mining` | Static | Whether this content may be used for AI training (default: not allowed without permission). |
| `c2pa.creative-work` | From seed payload | Title, author, description, license. |
| `org.paradigm.seed-hash` | Computed | The seed's canonical hash (`sha256:...`), so verifiers can fetch the canonical seed. |
| `org.paradigm.gspl-agent` | From `agent_runs` | Agent version, provider, model, intent, sub-intent. |
| `org.paradigm.lineage-root` | From lineage walk | The hash of the oldest ancestor. |

The first six assertions are standard C2PA. The three `org.paradigm.*` assertions are vendor-extension assertions allowed by C2PA 2.0 §15.6.

## The `c2pa.actions` assertion

Every Paradigm export carries the following actions in order:

```json
{
  "actions": [
    {
      "action": "c2pa.created",
      "when": "2026-04-06T12:34:56Z",
      "softwareAgent": "Paradigm GSPL Engine v1.0.0",
      "digitalSourceType": "http://cv.iptc.org/newscodes/digitalsourcetype/algorithmicMedia"
    },
    {
      "action": "c2pa.ai_generated",
      "when": "2026-04-06T12:34:56Z",
      "parameters": {
        "provider": "anthropic",
        "model": "claude-sonnet-4-6",
        "agent_version": "1.0.0",
        "intent": "creation.from_concept"
      }
    },
    {
      "action": "c2pa.processed",
      "when": "2026-04-06T12:34:57Z",
      "parameters": {
        "engine": "sprite",
        "engine_version": "1.0.0"
      }
    },
    {
      "action": "c2pa.published",
      "when": "2026-04-06T12:34:58Z"
    }
  ]
}
```

`digitalSourceType` is the IPTC vocabulary identifier for "algorithmic media," which is the term EU AI Act recital 133 maps to.

For a *derivative* seed (created via Variation, Composition, or Translation), an additional `c2pa.derived` action is inserted referencing the parent seeds via their hashes.

## Signing keys

Paradigm holds a single C2PA signing identity per environment:

- **Production:** Paradigm Inc., signed under a EUTL-recognized CA (DigiCert C2PA Verified Identity, when available).
- **Staging:** self-signed for testing only; staging exports carry a visible "STAGING" watermark.

The signing key is held in HashiCorp Vault and accessed by an `export-signer` service. The key never leaves the signer service; the API gateway POSTs unsigned manifests and receives signed ones in return.

The C2PA signing key is **distinct** from the user's seed authorship key. This separation matters because:

- The seed signature attests *who created the seed* (the user, sovereign).
- The C2PA signature attests *that this content was produced by Paradigm* (the platform).

Both signatures appear in the export.

## Where manifests live

| Format | Where C2PA goes |
|---|---|
| PNG | iTXt chunk (`c2pa` keyword) |
| JPEG | APP11 marker segment (JUMBF box) |
| WebP | RIFF chunk (`C2PA`) |
| MP4 / WebM | top-level `uuid` box |
| Opus / WAV / FLAC | format-specific metadata block |
| GLB / glTF | top-level extras with `c2pa` extension |
| `.gseed` | Auxiliary block, see `infrastructure/gseed-format.md` |

For formats that do not natively support metadata (raw PCM, plain text), Paradigm produces a **sidecar** `.c2pa.json` file containing the manifest, named `<original>.c2pa.json`.

## Verification

Anyone can verify a Paradigm export with the public Adobe Verify tool, the C2PA reference verifier, or `c2patool`:

```bash
c2patool verify image.png
```

The output includes:

- The signing identity ("Paradigm Inc.")
- The signature validity
- The full action chain
- All ingredients
- The vendor-extension fields including the seed hash

A user can then look up the seed by hash on `paradigm.app/s/<hash>` to see the canonical seed JSON, the lineage tree, and the original agent run.

## Edits and the chain

When an Adobe / Affinity / GIMP user edits a Paradigm export:

1. The original Paradigm manifest is preserved as an *ingredient*.
2. A new top-level manifest is created by the editing tool.
3. The new manifest references the original by hash and lists the edits applied.

The chain is preserved indefinitely. If a viewer queries the final image, they can walk all the way back to the canonical seed in Paradigm.

If an editor *strips* the manifest (e.g., using a non-C2PA tool, screen-capping, or running the image through an AI upscaler that ignores metadata), the chain breaks. C2PA cannot prevent stripping; it can only make it detectable. Best practice is to publish with the manifest and rely on platforms to detect tampering.

## Performance budget

Manifest generation is on the export hot path. Targets:

- Manifest construction: <5ms
- CBOR encoding: <2ms
- Signing (P-256): <10ms
- Embedding: format-dependent, <20ms for PNG/JPEG, <40ms for MP4

Total overhead per export: **~40ms p95**, dominated by signing. The signing service is colocated with the export worker to minimize RTT.

## Library

Paradigm uses the official **`c2pa-rs`** Rust library wrapped in a thin Node binding (`c2pa-node`). Both are listed in `infrastructure/library-canon.md`. We do not implement C2PA from scratch; the spec is large and the reference library is well-maintained by the Content Authenticity Initiative.

## Test vectors

`tests/c2pa-vectors/` contains:

1. A canonical Paradigm export PNG with a known manifest, used to verify any code path that touches manifests.
2. A derivative export with three ancestors, exercising the `c2pa.ingredients` and `c2pa.derived` actions.
3. An edit chain: Paradigm export → simulated Photoshop edit → final PNG with two-link chain.
4. A negative case: a manifest with a mismatched hash, used to verify the verifier rejects tampered files.

CI runs the verifier against all vectors on every build.

## Open issues

- **Mobile JPEG strippers:** iOS Mail's "Optimize for size" silently strips C2PA from JPEG attachments. We export PNG by default to avoid this until iOS catches up.
- **Sora / Veo / similar:** these tools currently embed C2PA but use different action vocabularies. Cross-tool ingredient parsing requires a small mapping table, maintained in `compliance/c2pa-vocab-map.json`.

## References

- C2PA 2.0 Specification — https://c2pa.org/specifications/specifications/2.0/
- IPTC Digital Source Type vocabulary — https://cv.iptc.org/newscodes/digitalsourcetype/
- Content Authenticity Initiative — https://contentauthenticity.org/
- `c2pa-rs` — https://github.com/contentauth/c2pa-rs
- ADR-011 — chose C2PA compliance
- `compliance/eu-ai-act.md` — how C2PA satisfies Article 50
- `compliance/ca-sb-942.md` — how C2PA satisfies SB 942
