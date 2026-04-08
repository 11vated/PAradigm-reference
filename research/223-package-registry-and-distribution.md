# 223 — Package registry and distribution

## Question
What is the typed package registry and distribution surface that enables substrate creators to publish and consume gseed packages (recipes, mods, asset bundles, sub-substrates) via a federated registry — analogous to crates.io / npm / PyPI but signed, lineage-tracked, and federation-friendly without a centralized authority?

## Why it matters (blast radius)
Recipes (Briefs 197-208), mods (Brief 187), and asset bundles (Brief 221) need a distribution surface. Hand-publishing through git repos is friction. A typed registry turns the substrate ecosystem into a discoverable, version-pinned, dependency-resolvable network — but federation-not-monopoly avoids the cargo-cult / npm-leftpad failure modes by ensuring no single registry is the sole source of truth.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 187 — mod and plugin surface.
- Brief 197-208 — recipes.
- Brief 210 — federated identity surface.
- Brief 217 — CLI and headless toolchain.
- Brief 221 — asset pipeline and import tooling.

## Findings
1. **`gspl publish` and `gspl install`.** CLI subcommands manage registry interactions. `gspl publish <package>` uploads a signed package to a registry; `gspl install <package@version>` resolves and downloads dependencies into the project.
2. **Package as typed gseed bundle.** A package is a typed `package.gseed` declaring: name, version (semver), description, license, authors, dependencies, target substrate version range, included gseeds, signed bundle hash.
3. **Federated registry hosts.** Substrate ships a deployable registry server. Anyone can host a registry (substrate, studios, communities). Substrate.org runs a default registry. Creators choose which registries to trust per project via typed `gspl.toml` registry list.
4. **Typed dependency resolution.** Resolver computes a version-locked dependency graph satisfying typed constraints. Lockfile (`gspl.lock`) records exact versions and content hashes. Identical resolution across machines and CI.
5. **Content addressing.** Packages are content-addressed by signed BLAKE3 hash. Identical packages from different registries deduplicate. Tampering is structurally detectable.
6. **Semver enforcement.** Substrate enforces semver via typed schema diff: any breaking schema change requires a major version bump. Diff computed automatically by the registry on publish; non-semver changes rejected.
7. **License field required.** Packages must declare a typed SPDX license identifier. Resolver warns on incompatible license combinations (e.g., GPL into MIT-only project).
8. **Yanking, not deletion.** Bad versions are typed `package.yank` mutations: the version is marked unsafe but content remains addressable for reproducibility. No silent disappearance.
9. **Mirror federation.** Registries can mirror each other via signed federation messages. Resolver falls back to mirrors if primary unavailable. Reproducibility is preserved across mirror chains.
10. **Audit trail.** Every publish appends to a signed audit log: who published what version when. Audit logs are queryable by package name; supply-chain attacks are post-hoc detectable.
11. **Search and discovery.** Registry servers expose typed search API: by name, tag, recipe genre, mod capability, license. CLI `gspl search <query>` queries configured registries.
12. **No script execution.** Packages contain only signed gseeds — no install scripts, no postinstall hooks, no executable code. The substrate's typed surface is inherently safer than npm-style ecosystems where postinstall scripts have driven major attacks.
13. **Validation contract.** Sign-time gates on publish: package signed by author identity (Brief 210), schema version matches declared substrate version, all referenced dependencies resolve, license SPDX identifier valid, semver bump matches schema diff.

## Risks identified
- **Federation discoverability.** Multiple federated registries fragment discovery. Mitigation: substrate-default registry indexes metadata from federated mirrors; creators discover via federation graph traversal.
- **Squatting.** Name squatting is a registry-economy problem. Mitigation: registry name reservation requires identity verification; expired reservations release names.
- **Version conflict resolution.** Diamond dependency conflicts can be unsolvable. Mitigation: typed semver enforcement reduces conflicts; resolver reports actionable conflicts; creators can pin via override.
- **Supply chain attacks.** Even signed packages can hide malicious gseeds. Mitigation: substrate is typed end-to-end; no executable code in packages; gseed validation gates run before install.
- **Registry availability.** Single registry outage breaks installs. Mitigation: federation mirroring; lockfile + content-addressed cache makes locally-cached installs reproducible offline.

## Recommendation
Specify the package registry as a `gspl publish` / `gspl install` / `gspl search` subcommand surface against federated registry hosts (substrate-default + creator-deployable + community-mirrored), with typed `package.gseed` packages, semver-enforced schema-diff publish gates, content-addressed deduplication, lockfile reproducibility, signed audit trails, and no-script-execution by construction.

## Confidence
**4 / 5.** Package registry patterns are well-precedented (crates.io, npm, PyPI, Hex). The novelty is the federation-not-monopoly architecture, the schema-diff-driven semver enforcement, and the structural elimination of postinstall script attacks. Lower than 4.5 because federation mirror reliability needs Phase-1 measurement.

## Spec impact
- New spec section: **Package registry and distribution specification**.
- Adds the `gspl publish` / `install` / `search` subcommand contracts.
- Adds the typed `package.gseed` kind with required fields.
- Adds the federated registry server contract.
- Adds the `gspl.lock` lockfile format.
- Adds the `package.yank` mutation kind.
- Cross-references Briefs 152, 187, 197-208, 210, 217, 221.

## New inventions
- **INV-985** — Federated package registry as substrate-deployable analogous to Brief 210 identity / Brief 215 matchmaking: distribution lives with the community, not a centralized authority.
- **INV-986** — Typed `package.gseed` with required SPDX license / dependency declarations / signed bundle hash: packages are structured substrate primitives, not opaque archives.
- **INV-987** — Schema-diff-enforced semver: breaking schema changes structurally require major version bumps, eliminating accidental breakage.
- **INV-988** — No-script-execution by construction: substrate packages contain only typed gseeds, structurally eliminating npm-style postinstall attack surface.
- **INV-989** — Content-addressed package deduplication via signed BLAKE3 hash: identical packages from different registries collapse to one storage entry.
- **INV-990** — `gspl.lock` reproducible lockfile with exact versions and content hashes: identical resolution across machines, CI, and time.
- **INV-991** — Yank-not-delete via typed `package.yank` mutation: bad versions are marked unsafe but remain addressable for reproducibility.
- **INV-992** — Signed audit log per registry with creator-queryable history: supply chain attacks are post-hoc detectable and publicly auditable.
- **INV-993** — Mirror federation with resolver fallback chains: registry availability degrades gracefully across mirror networks.

## Open follow-ups
- Phase-1 federated registry implementation and reliability measurement.
- Package vulnerability database — deferred to v0.2.
- Paid / commercial package distribution — deferred to v0.3.
- Cryptographic transparency log (Sigstore-style) — deferred to v0.3.
- Package download analytics — deferred to v0.4.
- Web UI for registry browsing — Phase 1.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 187 — Mod and plugin surface.
3. Brief 210 — Account and identity surface.
4. Brief 217 — CLI and headless toolchain.
5. crates.io design — rust-lang.
6. npm registry design and post-install attack history.
7. Hex.pm registry — Elixir.
8. PyPI design — Python.
9. SPDX license identifier list.
10. Sigstore transparency log.
11. BLAKE3 hash specification.
