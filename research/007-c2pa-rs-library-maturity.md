# 007 — c2pa-rs library maturity, performance, and embedding budgets

## Question
Is the `c2pa` Rust crate (Adobe Content Authenticity Initiative reference implementation) mature, performant, and stable enough for Paradigm to depend on it as the only C2PA implementation in the export pipeline, or does the spec need a contingency plan?

## Why it matters (blast radius)
Every Paradigm export embeds a C2PA 2.0 manifest. The C2PA manifest is the spec's bridge to the C2PA ecosystem (browsers, social networks, news verifiers, AI labelling tools). If the only viable Rust C2PA library is unstable, slow, or unmaintained, the spec either has to rewrite C2PA itself (a year of work, plus a maintenance burden forever) or accept a non-Rust dependency (breaks the boring-tech rule). This brief gates `compliance/c2pa-binding.md` and `runtime/export-pipeline.md`.

## What we know from the spec
- `compliance/c2pa-binding.md` mandates a C2PA 2.0 manifest on every exported asset.
- `compliance/c2pa-binding.md` cites the c2pa-rs library as the implementation.
- The spec assumes a per-export C2PA budget on the order of tens of milliseconds.

## Findings

1. **`c2pa-rs` is the official Rust SDK from the Coalition for Content Provenance and Authenticity (Adobe-led, hosted at github.com/contentauth/c2pa-rs).** [1, 2, 3] It is the reference implementation of the C2PA technical specification and the CAWG identity assertion specification. There is no second mature Rust C2PA implementation; this is the only viable Rust path.

2. **The crate is in beta (0.x.x).** [3] The maintainers explicitly state that the minor version is incremented on breaking API changes and that breaking changes "may happen frequently." As of recent releases, the crate is at version 0.36.x [4], which suggests the project has been through dozens of breaking-change minor bumps but is also clearly under active maintenance.

3. **The crate already supports C2PA v2 claims by default.** [3] This is critical — Paradigm targets C2PA 2.0, not 1.x — and the library has already done the migration. New checks and status codes for v2 are present.

4. **The library has a Builder/Reader API that focuses on simplicity and stream support.** [3] It uses threaded I/O for some operations to improve performance, with a `no_interleaved_io` feature flag to force fully-synchronous I/O if a caller needs determinism in I/O ordering. **Implication: stream-based embedding is supported, which matters for large exports.**

5. **The library reads, creates, and embeds C2PA data for a variety of asset types.** [3] PNG, JPEG, MP4, WAV, and others are covered out of the box. Custom asset types (the `.gspl` container) require a "remote manifest" approach where the manifest is stored alongside or referenced by the asset rather than physically embedded.

6. **MSRV is Rust 1.88.0 or newer in current releases.** [3] This is a recent toolchain and should be tracked in `infrastructure/library-canon.md`.

7. **Performance is not benchmarked publicly with hard numbers.** The library uses threaded I/O and is the reference implementation for production tools shipped by Adobe and Microsoft, which suggests it is "fast enough" in practice, but we have no published p50/p95 latencies for manifest creation, signing, or verification on representative payloads. This is an empirical gap that Phase 1 must close before committing to a hard latency budget.

8. **The library is Apache-2.0 licensed**, matching the Paradigm spec license.

## Risks identified

- **API churn during 0.x means the spec must pin an exact minor version** and budget for periodic minor-bump migrations. This is the largest practical risk.
- **No public latency benchmarks** mean the "tens of milliseconds per export" assumption in the spec is unverified. It might be 5ms; it might be 200ms.
- **Custom asset type embedding** (the `.gspl` container) is the path of most resistance — the library covers standard formats well, but a custom container needs the "remote manifest" or "external manifest" mode, which the library supports but is less commonly exercised.
- **The library is single-vendor-led** (Adobe through CAI). A Paradigm production dependency on a single-vendor library is acceptable for now (the alternative is to rewrite a complex spec), but the boring-tech ADR should explicitly note it.
- **Trust list / trust anchor management** is a separate concern — embedding a manifest is one thing; ensuring it verifies against the C2PA trust list is another. Out of scope for this brief but flagged.

## Recommendation

**Adopt `c2pa-rs` as the sole C2PA implementation, with operational rules that bound the API-churn risk:**

1. **Pin an exact `c2pa` version in `Cargo.toml`** and treat bumps as a release event with its own changelog entry and conformance suite run.
2. **Use the Builder/Reader API**, not the deprecated read/write API. The library has already moved on; do not adopt the old surface.
3. **Use the `no_interleaved_io` feature flag** for the proof-bearing export path, so I/O ordering is deterministic and easier to reason about under fault injection. The threaded-I/O path is allowed for non-proof-bearing previews if needed.
4. **Embed manifests using the standard embedded mode for PNG/JPEG/MP4/WAV exports.** For the native `.gspl` container, use the external/remote manifest mode and document the manifest URL or local sidecar format in `formats/file-format.md`.
5. **Track Rust MSRV at 1.88+** and bump the workstation-wide MSRV pin as required.
6. **Phase 1 task: build a benchmark harness that measures p50/p95/p99 latency for `Builder::sign` and `Reader::from_stream` on representative payloads** (10 KB seed, 4 MB image, 40 MB video). Until those numbers exist, the spec's latency budget is provisional.
7. **Treat the Adobe trust list as authoritative for v1.** A Paradigm-controlled trust list is a v2 concern.
8. **Reserve a `compliance/c2pa-fallback.md` slot for a contingency plan** in case `c2pa-rs` is abandoned or ships a breaking change we cannot follow. The contingency is "freeze on the last working version, fork it, maintain it ourselves" — not "rewrite from scratch."

## Confidence
**4/5.** The library is real, official, actively maintained, and the only credible path. The 4/5 (rather than 5/5) reflects (a) the unverified performance numbers and (b) the API-churn risk during the 0.x era. Both risks are bounded by the operational rules above.

## Spec impact

- **`compliance/c2pa-binding.md`** — pin the `c2pa` crate version and document the Builder/Reader API choice. Add the embedded vs external manifest mode rule per asset type.
- **`runtime/export-pipeline.md`** — mark the latency budget as "provisional, pending Phase 1 benchmark."
- **`infrastructure/library-canon.md`** — pin `c2pa` exact version, set MSRV ≥ 1.88, mark the bump process as a release event.
- **`formats/file-format.md`** — specify the external/remote manifest format for the native `.gspl` container.
- New file: **`compliance/c2pa-fallback.md`** — minimal contingency document.
- New ADR: **`adr/00NN-c2pa-rs-dependency.md`** — record the single-vendor-library acceptance and the contingency plan.

## Open follow-ups

- Build the latency benchmark harness. Phase 1 task.
- Decide on the external manifest format for `.gspl` (sidecar `.c2pa` file? URL inside the container?).
- Decide whether Paradigm runs its own trust list or relies entirely on the Adobe one. Defer to a separate brief.
- Track the `c2pa-rs` 1.0 release if/when it ships and re-evaluate the operational rules.

## Sources

1. c2pa-rs on GitHub. https://github.com/contentauth/c2pa-rs
2. c2pa crate on docs.rs. https://docs.rs/c2pa
3. CAI open-source documentation for the Rust SDK. https://opensource.contentauthenticity.org/docs/rust-sdk/
4. c2pa 0.36.3 release on docs.rs. https://docs.rs/crate/c2pa/0.36.3
5. c2pa-rs release notes. https://github.com/contentauth/c2pa-rs/blob/main/docs/release-notes.md
