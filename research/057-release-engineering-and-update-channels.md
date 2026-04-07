# 057 — Release engineering and update channels

## Question
How does GSPL ship updates safely — across studio binaries, engine plugins, model files, and shipped models — while preserving determinism, lineage compatibility, and the offline-first commitment?

## Why it matters
Auto-updaters are a notorious source of bugs, security issues, and user frustration. GSPL has additional constraints: updates must not break content addressing (a re-rendered seed must produce the same hash), must not break lineage (existing projects must continue to work), and must be cryptographically verifiable (no MITM, no rogue updates). Get this right and GSPL ships smoothly forever; get it wrong and the platform fragments.

## What we know from the spec
- Brief 018: four-layer versioning (spec, file format, gene type, operator).
- Brief 042: signing keys.
- Brief 048: studio architecture with engine plugins.

## Findings — five release tracks

### Track 1: Stable
The default channel. Releases are infrequent (quarterly), thoroughly tested, and backward compatible.
- **Cadence:** every 3 months.
- **Backward compatibility:** every existing project must work without migration.
- **Migration tooling:** if a migration is needed, it's a separate operator (Brief 018), not silent.
- **Audit trail:** every release has a signed changelog and a release attestation.

### Track 2: Beta
Pre-release channel for testing.
- **Cadence:** every 2-4 weeks.
- **Stability:** mostly stable; known issues documented.
- **Opt-in only.**
- **Auto-falls-back to stable** if the user encounters severe issues.

### Track 3: Nightly
Latest commits, possibly broken.
- **Cadence:** daily.
- **For developers and contributors only.**
- **Visible warning** in the studio.

### Track 4: Frozen
Pinned to a specific version forever. Used by professional creators who can't tolerate any drift.
- **No auto-updates.**
- **Manual upgrade only.**
- **Critical security fixes still ship** as patch versions but the user is notified before applying.

### Track 5: Self-built
For sovereignty-maximalist users who build from source.
- **Reproducible builds** (deterministic compilation).
- **Bit-for-bit hash check** between self-built and official binaries published in the release attestation.

## Update artifacts

A release contains several artifact types, each with its own update strategy:

### Studio binary
- **Distribution:** signed installer per OS (.dmg, .msi, .deb/.rpm/.AppImage).
- **Auto-update:** opt-in; default is "notify only."
- **Verification:** signature check before install.
- **Rollback:** previous version retained for 30 days.

### Engine plugins
- **Distribution:** signed plugin files.
- **Versioning:** independent per engine (Brief 018).
- **Auto-update:** opt-in per engine.
- **Compatibility:** plugin ABI versioned; mismatched ABI refuses to load.
- **Rollback:** previous engine version retained per project.

### Model files (LLM, critic models, AURORA encoders)
- **Distribution:** signed model files via direct download or torrent.
- **Versioning:** independent.
- **Auto-update:** opt-in per model.
- **Verification:** SHA256 hash check + signature check.
- **Rollback:** previous version retained.

### Locale files
- **Distribution:** signed bundles.
- **Versioning:** per-language.
- **Auto-update:** silently OK because locale changes can't break determinism.

### Spec documents
- **Distribution:** versioned documentation served via static site or local docs.
- **Versioning:** matches the studio version.

## Update verification

Every artifact is verified before install:
1. **Signature check** against the GSPL release signing key.
2. **Hash check** against the published manifest.
3. **Compatibility check** (engine ABI, file format version).
4. **Sandbox install** (extract to temp; verify; then promote).
5. **Rollback on failure** (atomic install with previous version retained).

The release signing key is hardware-backed and stored in a YubiKey. Multi-sig (2-of-3) for releases. The signing process is documented in `release/signing-process.md`.

## Update transport

- **HTTPS** for the official update server.
- **Mirror network** of community-run mirrors for redundancy.
- **Tor** for users who prefer to update via onion service (the GSPL release server has an onion address).
- **Sneakernet** for users in disconnected environments — releases are published as a single signed `.tar.gz` archive that can be transferred via USB.

## Determinism and content addressing across versions

A released version pins:
- **Engine versions** (per engine).
- **Operator versions** (frozen post-release per Brief 018).
- **Critic model versions.**
- **Renderer versions** (Tier 1 deterministic kernel).

Updating any of these *can* change a re-rendered output. To preserve determinism:
- **Existing projects** keep their pinned versions until manually migrated.
- **New projects** use the latest pinned versions of the active release.
- **Content addressing** is therefore stable per project across studio updates.

When a migration *is* required (rare; e.g., critical security fix in an operator), the migration is a first-class lineage operation (Brief 018), recorded in the lineage as an explicit edge.

## Risks identified

- **Auto-update bricks:** an update fails midway and the studio won't start. Mitigation: atomic install + rollback.
- **Signing key compromise:** an attacker signs a malicious update. Mitigation: hardware-backed multi-sig; key rotation; community key transparency log.
- **Mirror compromise:** a mirror serves a malicious binary. Mitigation: hash check against the official manifest; signature verification.
- **Plugin ABI churn:** every release breaks plugins. Mitigation: ABI is stable within a major version; breaking changes only at majors; deprecation warnings precede.
- **Frozen track left vulnerable:** users who never update remain vulnerable to known issues. Mitigation: critical security patches ship with explicit user prompts; the studio shows a clear "your version is N months behind, here's what you're missing" notice.
- **Reproducible build drift:** small toolchain differences produce different binaries. Mitigation: pinned toolchain in the build manifest; reproducible-builds.org compliance.
- **Update size:** large model files are slow to download. Mitigation: torrent fallback; delta updates where possible.

## Recommendation

1. **Adopt the five-track release model** in `architecture/release-engineering.md`.
2. **Quarterly stable cadence** as the v1 default.
3. **Hardware-backed multi-sig signing** for releases.
4. **Atomic install with rollback** for the studio binary.
5. **Independent versioning per engine, model, and locale** (Brief 018).
6. **Content addressing remains stable per project** across updates.
7. **Migrations are first-class lineage operations**, never silent.
8. **Reproducible builds** at v1; published hashes for self-built verification.
9. **HTTPS + mirror network + Tor + sneakernet** distribution.
10. **Critical security fixes ship with user notification** even on frozen track.
11. **Engine ABI stable within a major version.**

## Confidence
**4/5.** Release engineering is well-understood. The 4/5 reflects honest uncertainty about reproducible build complexity across the Rust toolchain.

## Spec impact

- `architecture/release-engineering.md` — full release spec.
- `protocols/release-tracks.md` — five-track definition.
- `protocols/update-verification.md` — signature and hash check flow.
- `architecture/distribution.md` — HTTPS / mirror / Tor / sneakernet.
- `release/signing-process.md` — multi-sig signing process.
- New ADR: `adr/00NN-quarterly-stable-cadence.md`.

## Open follow-ups

- Build the auto-update mechanism with atomic install.
- Set up the multi-sig hardware signing process.
- Investigate reproducible-builds.org compliance for Rust.
- Build the mirror network bootstrap.
- Design the migration operator UX.
- Plan the bug bounty for the update mechanism.

## Sources

- Reproducible Builds project documentation.
- Sigstore and the in-toto framework.
- Apple notarization and Windows Authenticode for OS-level signing.
- Tor Browser update mechanism (relevant for onion service updates).
- Internal: Briefs 018, 042, 048.
