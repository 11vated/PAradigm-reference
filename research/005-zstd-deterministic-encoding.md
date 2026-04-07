# 005 — zstd deterministic encoding

## Question
Can the Paradigm export pipeline rely on zstd to produce bit-identical compressed bytes for the same input across platforms, CPU instruction sets, and library versions, and what configuration is required to make that guarantee hold?

## Why it matters (blast radius)
The compressed `.gspl` artifact is hashed into the C2PA manifest and signed. If two implementations of the spec compress the same canonical seed and produce different bytes, the content hash diverges and the proof breaks at the file level. zstd is the spec's only compression primitive — it is on the critical path for every export. This brief gates `formats/file-format.md`, `proof/content-hash.md`, and `infrastructure/library-canon.md`.

## What we know from the spec
- `formats/file-format.md` mandates zstd as the only allowed compression for the `.gspl` payload.
- `proof/content-hash.md` hashes the *compressed* bytes as part of the manifest input.
- `infrastructure/library-canon.md` prefers `zstd` from facebook/zstd (or its Rust binding `zstd-rs`).

## Findings

1. **zstd is deterministic within a single version, single thread count, single platform, and single SIMD level — but not across any of those axes.** The facebook/zstd maintainers have stated this directly across multiple issues [1, 2, 3]. Reproducibility is "best effort," not a guarantee.

2. **Output differs between zstd library versions.** Issue #999 [1] documents that compressor output is not stable between versions; the maintainers explicitly do not guarantee output stability across version bumps, even patch versions in some cases. Issue #4049 [4] is a concrete example: the same options produce different output between 1.5.5 and 1.5.6.

3. **Output can differ based on CPU SIMD support (SSE / NEON / AVX2 / etc.) on the same library version.** Issue #4099 [5] documents this explicitly: zstd's parsing/matching code has SIMD-specialized paths whose match selection can differ from the scalar path under certain inputs. The same library binary moved between machines with different SIMD support produces different compressed bytes for the same input.

4. **Multi-threaded compression is non-deterministic by default but can be made deterministic.** Issue #2079 [6] confirms that multi-threaded zstd is reproducible only if the thread count is held constant and the worker boundaries are deterministic. The CLI provides a reproducibility mode independent of thread count, but the C API requires explicit care.

5. **There is no LTS / "forever-stable" zstd release.** Issue #4173 [7] is an open feature request for exactly this; the maintainers have not committed.

6. **There is no test in the zstd CI that validates cross-platform reproducibility.** Issue #4330 [8] is an open feature request to add such tests. Internal determinism fuzzers exist for single-platform single-version reproducibility only.

7. **Decompression is deterministic and stable.** zstd's decoder is bit-for-bit stable across versions because the bitstream format is frozen — only the *encoder* has reproducibility issues.

## Risks identified

- **Pinning the zstd library version is necessary but not sufficient.** Two CI runners with different SIMD support can produce different bytes from the same pinned version.
- **Implementations using the system zstd library** (e.g., distro packaged) will see version drift across user machines and will not interoperate.
- **The Rust `zstd` crate vendors a specific upstream version per release** — this is good — but bumping the crate is a determinism event.
- **Multi-threaded compression** is tempting for export performance but introduces another determinism axis. Single-threaded is the safe default.
- **Future SIMD optimizations** in upstream zstd can silently change output even on a pinned version if the binary is recompiled with different `RUSTFLAGS` / `CFLAGS`.

## Recommendation

**The export pipeline does not depend on zstd output being byte-stable across versions or platforms.** Instead, the spec separates the *content hash domain* from the *compression domain*:

1. **The content hash is computed over the *uncompressed* canonical payload, not the compressed bytes.** This is the load-bearing change. Compression becomes a transport concern, not a proof concern.
2. **The C2PA manifest references the uncompressed payload hash.** Verifiers decompress the `.gspl` payload, recompute the hash over the decompressed bytes, and compare against the manifest.
3. **zstd is still mandatory** as the on-disk compression format because the file format spec demands a single compression primitive, but its output bytes are not proof-bearing.
4. **Pin the zstd library version anyway** for ecosystem hygiene and to eliminate "compression failed" classes of bugs that vary across versions.
5. **Single-threaded compression at a fixed level (recommended: 19, the maximum non-experimental level) is the default.** Multi-threaded export is allowed but flagged as a performance optimization that does not affect proof.
6. **Do not use zstd dictionaries at v1.** Dictionaries are another determinism axis (the dictionary version becomes part of the encoder state) and the spec doesn't need them.

This is the most important finding in the entire research workstream so far: **the original spec assumption that "the compressed bytes are part of the hash domain" is wrong and must be fixed.**

## Confidence
**4/5.** The zstd reproducibility limits are well-documented by the maintainers themselves; this is not a guess. The 4/5 reflects residual uncertainty about whether some other Paradigm subsystem (e.g., the C2PA embedder) implicitly assumes the compressed bytes are stable; the spec impact list calls this out and the synthesis brief will track it.

## Spec impact

- **`proof/content-hash.md` — REWRITE.** The hash domain is the uncompressed canonical payload, not the compressed bytes. This is a normative change.
- **`formats/file-format.md`** — clarify that the payload is compressed *after* hashing and that the compression layer is not proof-bearing.
- **`compliance/c2pa-binding.md`** — confirm that the C2PA assertion targets the uncompressed-payload hash, not the on-disk file hash.
- **`infrastructure/library-canon.md`** — pin the zstd version and document that "we pin zstd for hygiene, not for hash stability."
- **`runtime/export-pipeline.md`** — add the "single-threaded, level 19, no dictionary" defaults and note multi-threading as an opt-in optimization.
- New ADR: `adr/00NN-hash-domain-is-uncompressed.md` — capture this decision and the reasoning, because it is non-obvious and reverses a prior implicit assumption.

## Open follow-ups

- Confirm with a literal read of every existing `proof/` and `formats/` doc that no other place implicitly assumes the compressed bytes are part of the hash. Synthesis-brief task.
- Decide whether the spec wants a separate "transport hash" over the compressed bytes (for HTTP `Content-Digest` or similar transport-layer integrity) — this is allowed and useful but distinct from the proof-bearing hash.
- Decide if multi-threaded export should be explicitly forbidden or just discouraged. Recommendation: allowed, with a `--reproducible` flag that forces single-thread.

## Sources

1. zstd issue #999 — Clarify zstd compressor output compatibility guarantees across versions. https://github.com/facebook/zstd/issues/999
2. zstd issue #2949 — Is zstd compression deterministic? https://github.com/facebook/zstd/issues/2949
3. zstd repository. https://github.com/facebook/zstd
4. zstd issue #4049 — Output differs with same options between 1.5.5 and 1.5.6. https://github.com/facebook/zstd/issues/4049
5. zstd issue #4099 — Output varies based on presence of SSE / NEON. https://github.com/facebook/zstd/issues/4099
6. zstd issue #2079 — Deterministic multi-threaded compression. https://github.com/facebook/zstd/issues/2079
7. zstd issue #4173 — Consider an LTS / "forever" output-stable release. https://github.com/facebook/zstd/issues/4173
8. zstd issue #4330 — Add tests that validate reproducibility across hardware platforms. https://github.com/facebook/zstd/issues/4330
