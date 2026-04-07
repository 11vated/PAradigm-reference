# 060 — Supply chain and dependency security

## Question
How does GSPL secure its software supply chain — across the Rust crate ecosystem, the JS ecosystem, the model weights, the engine plugins, and the build pipeline — given that supply chain attacks are now the dominant threat vector for software?

## Why it matters
SolarWinds, xz-utils, npm package compromises, PyPI typosquatting — supply chain attacks are the way modern software gets owned. GSPL is a single binary that processes content-addressed data, signs lineage, and holds private keys. A supply chain compromise is catastrophic. The standard answer (audit your deps) is inadequate for an ecosystem with thousands of transitive dependencies. GSPL needs a layered defense.

## What we know from the spec
- Brief 042: signing key infrastructure.
- Brief 057: release engineering.
- Brief 048: studio architecture (Rust + Tauri + JS frontend).

## Findings — six-layer supply chain defense

### Layer 1: Dependency minimization
Every dependency is a liability. The first defense is to have fewer of them.
- **Strict dependency budget per crate.** A new dependency requires justification ("why can't we write this ourselves?").
- **Vendoring small dependencies** that we'd otherwise inherit transitively for one function.
- **Avoiding heavyweight ecosystems** where small wins. E.g., custom JSON parser, not serde for kernel paths.
- **Periodic dep audits** to remove unused crates.

Target: ≤ 200 direct dependencies; ≤ 1000 transitive.

### Layer 2: Pinning and lockfiles
- **`Cargo.lock` committed** for the studio binary and all engine crates.
- **`package-lock.json` committed** for the JS frontend.
- **Lockfile changes reviewed manually** as part of every PR.
- **No floating versions** in any manifest.
- **Reproducible builds** (Brief 057) verify that lockfile pinning produces the same binary.

### Layer 3: Vetting
- **`cargo-vet`** to track which crates have been audited and by whom.
- **`cargo-deny`** for license compliance and known-bad-version blocklisting.
- **`cargo-audit`** against the RustSec advisory database.
- **`npm audit`** for the JS frontend.
- **Manual review** of every new direct dependency.
- **Trust import** from known-good vetting orgs (Mozilla, Google, embarrasingly small list of others).

### Layer 4: Build pipeline security
- **Hermetic builds** in CI: builds run in clean containers with no network access except the dependency mirror.
- **Reproducible builds** verified by independent rebuilds.
- **Build provenance** via SLSA Level 3 attestations.
- **Signed builds** by the multi-sig release key (Brief 042).
- **Tamper-evident build logs** published per release.

### Layer 5: Runtime defense
Even with a clean build, runtime exploitation is possible.
- **Sandboxing** of engine plugins: each plugin runs in a separate process with restricted capabilities.
- **Capability-based file access**: the studio kernel is the only component that touches the file system; engines and the agent ask for files via API.
- **Network segregation**: only the federation service touches the network.
- **Memory safety** via Rust as the first defense; `unsafe` blocks audited.
- **Fuzz testing** of all external data parsers (gseed format, c2pa attestations, lineage entries).

### Layer 6: Runtime supply chain monitoring
- **Local crash reporter** (Brief 056) flags unusual behavior.
- **Bug bounty program** for vulnerability disclosure.
- **CVE monitoring** for all dependencies; auto-alert on new advisories.
- **Periodic re-vetting** of high-risk dependencies (crypto, networking, parsing).

## Model supply chain

LLM and critic model weights are also supply chain.
- **Model files signed** by the GSPL release key after independent verification.
- **Hash-chained model registry** so changes are detectable.
- **Provider attestations** linked from the model registry.
- **Models downloaded over HTTPS + signature check + hash check.**
- **Sandboxed model execution**: the LLM runtime cannot touch the file system or network directly.

## Engine plugin supply chain

- **Engines signed by the GSPL release key** at v1.
- **Community engines (v2)** have a separate signing key per author + manual review for inclusion.
- **Engine ABI versioned** so that mismatched plugins are rejected (Brief 048).
- **Engine sandboxing** per Layer 5.

## Specific threat models

### Threat: Typosquatting in crates.io / npm
A malicious crate with a similar name to a popular one. Mitigation: dependency review; lockfile pinning.

### Threat: Compromised maintainer
A trusted maintainer pushes a malicious update. Mitigation: cargo-vet; pinning; manual lockfile review.

### Threat: Compromised CI runner
The CI runner injects malicious code into the build. Mitigation: hermetic builds; reproducible builds; multiple independent build verification.

### Threat: Compromised release key
The signing key is stolen. Mitigation: hardware-backed multi-sig; key rotation; key transparency log.

### Threat: Compromised model weights
A malicious actor publishes weights with a backdoor. Mitigation: model registry vetting; community review; sandboxed execution.

### Threat: Engine plugin compromise
A plugin is malicious. Mitigation: signing; sandboxing; capability-based access; review for community plugins.

## Risks identified

- **Reproducible builds in Rust are fragile.** Mitigation: pinned toolchain; careful build env; reproducible-builds.org guidance.
- **cargo-vet is community-driven and has gaps.** Mitigation: import multiple vetting orgs; manual fill-in.
- **Sandboxing has performance cost.** Mitigation: only enforce on engines and the LLM runtime; the kernel itself is trusted.
- **Bug bounty cost.** Mitigation: tiered rewards; community recognition for low-severity.
- **Model weight backdoors are hard to detect.** Mitigation: provenance from upstream + sandboxed execution + activation pattern monitoring (research).
- **Engine plugin sandboxing breaks features.** Mitigation: plugins request capabilities explicitly; user grants per-plugin permission.

## Recommendation

1. **Adopt the six-layer defense model** in `architecture/supply-chain-security.md`.
2. **Cargo.lock and package-lock.json committed**, manually reviewed.
3. **cargo-vet, cargo-deny, cargo-audit in CI**, blocking on findings.
4. **Hermetic + reproducible builds** at v1.
5. **SLSA Level 3 build provenance** at v1.
6. **Engine and LLM sandboxing** at v1.
7. **Model files signed and hash-verified.**
8. **Bug bounty program at launch.**
9. **CVE monitoring for all dependencies** with auto-alert.
10. **Manual review of every new direct dependency** as a PR requirement.
11. **Dependency budget enforced**: ≤200 direct, ≤1000 transitive.

## Confidence
**3/5.** The defenses are well-understood individually but the combination is operationally heavy. The 3/5 reflects honest uncertainty about reproducible build reliability and sandboxing performance.

## Spec impact

- `architecture/supply-chain-security.md` — full six-layer model.
- `protocols/dependency-vetting.md` — vetting process.
- `protocols/build-provenance.md` — SLSA L3 spec.
- `architecture/sandboxing.md` — engine and LLM sandboxing.
- `tests/supply-chain-tests.md` — automated tests.
- New ADR: `adr/00NN-six-layer-supply-chain.md`.

## Open follow-ups

- Set up cargo-vet, cargo-deny, cargo-audit in CI.
- Plan reproducible build infrastructure.
- Decide on the sandboxing primitive (Wasmtime, native containers, OS sandbox API).
- Launch bug bounty program at v1.
- Build CVE monitoring automation.
- Engage external security audit pre-launch.

## Sources

- SLSA Framework specification.
- Sigstore documentation.
- cargo-vet documentation.
- *Reflections on Trusting Trust* by Ken Thompson.
- xz-utils backdoor postmortem (CVE-2024-3094).
- Internal: Briefs 042, 048, 055, 057.
