# 229 — Substrate versioning and migration

## Question
What is the typed substrate versioning and migration surface that enables substrate creators to upgrade across substrate versions (v0.1 → v0.2 → v0.5 → v1.0) without breaking existing gseed projects, with typed migration scripts, schema-diff-driven migration generation, multi-version interoperability, and rollback safety?

## Why it matters (blast radius)
The substrate evolves. Schemas change. Primitives are added, deprecated, renamed. Without typed migration, every substrate version bump breaks every project. With typed migration, substrate versions evolve smoothly and existing projects upgrade reliably. Combined with the lineage-tracking property (Brief 152), every gseed has a migration path that's verifiable.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 217 — CLI and headless toolchain.
- Brief 222 — testing framework and CI integration.
- Brief 223 — package registry and distribution.

## Findings
1. **Typed `substrate.version` field on every gseed.** Every gseed records the substrate version it was authored against. Lineage preserves the version through every mutation. Mixed-version projects (legitimate during migration) are detectable.
2. **Semver across substrate versions.** Substrate follows semver: major (breaking schema), minor (additive), patch (bug fix). v0.x is pre-stable; v1.0 commits to long-term semver enforcement.
3. **Schema diff manifest.** Each substrate version ships a typed `schema.diff.gseed` against the previous version: added primitives, removed primitives, renamed fields, type-changed fields, deprecated paths. Lossless serialization.
4. **`gspl migrate` subcommand.** CLI subcommand `gspl migrate --to <version>` runs the typed migration chain from current substrate version to target. Each migration step is a typed `migration.def` gseed authored by substrate maintainers, signed by substrate identity.
5. **Auto-generated migrations.** For most schema changes (renames, additive fields, type widenings), substrate auto-generates the migration from the schema diff. Creators don't write migration code for the common case.
6. **Hand-authored migrations.** For semantic changes (e.g., changed mutation semantics that need state recomputation), substrate maintainers author typed migration logic. Migrations are signed and shipped with the substrate version.
7. **Migration dry-run.** `gspl migrate --dry-run` reports which gseeds would change and how. Creator reviews before applying.
8. **Lineage preservation.** Migrations append a typed `migration.applied` mutation to the lineage rather than rewriting history. Original lineage remains queryable.
9. **Rollback support.** Each migration declares an inverse where possible. `gspl migrate --rollback` reverts. Where inverse is impossible (e.g., dropped fields), substrate documents the loss explicitly and requires creator acknowledgment.
10. **Multi-version interop.** Substrate runtime can load gseeds from version range [N-2, N] without migration (with degraded feature support for older gseeds). Older versions are sign-time downgraded to closest compatible runtime feature set.
11. **Deprecated-not-removed.** Removed primitives spend at least one minor version cycle as deprecated (sign-time warning) before removal. Creators get migration runway.
12. **Test fixture migration.** `gspl test --migrate` runs the test suite against migrated gseeds; failures indicate migration issues.
13. **Validation contract.** Sign-time gates: every gseed declares `substrate.version`, declared version supported by current substrate runtime (in [N-2, N]), migrations available for target version, rollback inverse declared or marked irreversible with creator acknowledgment.

## Risks identified
- **Migration script bugs.** Bad migration silently corrupts gseeds. Mitigation: migrations are typed gseeds with sign-time validation; substrate ships migration test fixtures verifying round-trip correctness.
- **Lossy migrations.** Some changes drop information. Mitigation: substrate marks lossy migrations explicitly; creators acknowledge before applying.
- **Schema-diff completeness.** Auto-generated migrations may miss edge cases. Mitigation: hand-authored migrations cover semantic edge cases; auto-generation only for syntactic changes.
- **Multi-version interop overhead.** Loading [N-2, N] versions costs runtime complexity. Mitigation: typed downgrade map per version transition; bounded runtime cost.
- **v0.x volatility.** Pre-1.0 substrate may have frequent breaking changes. Mitigation: documented v0.x → v1.0 stability plan; creators know to expect migrations until v1.0.

## Recommendation
Specify substrate versioning as typed `substrate.version` field on every gseed, semver-tracked substrate releases, typed `schema.diff.gseed` per version, auto-generated + hand-authored typed `migration.def` gseeds, `gspl migrate` subcommand with dry-run / rollback / inverse support, lineage-preserving migration application, multi-version interop across [N-2, N], and deprecation cycles before removal.

## Confidence
**4 / 5.** Migration patterns are well-precedented (Rails migrations, Django migrations, schema evolution in Avro / Protobuf). The novelty is the typed migration gseeds with substrate-signed identity and the lineage-preserving application that doesn't rewrite history. Lower than 4.5 because v0.x → v1.0 migration testing requires Phase-1 schema-diff measurement.

## Spec impact
- New spec section: **Substrate versioning and migration specification**.
- Adds typed `substrate.version`, `schema.diff.gseed`, `migration.def`, `migration.applied` gseed kinds.
- Adds the `gspl migrate` subcommand contract.
- Adds the [N-2, N] multi-version interop window.
- Adds the deprecation cycle policy.
- Cross-references Briefs 152, 217, 222, 223.

## New inventions
- **INV-1044** — Typed `substrate.version` field on every gseed with lineage preservation: substrate version is structural per-gseed primitive.
- **INV-1045** — Typed `schema.diff.gseed` per substrate release: schema evolution is a first-class queryable artifact.
- **INV-1046** — Auto-generated migrations for syntactic schema changes (rename / additive / type widening): common-case migrations are zero-creator-effort.
- **INV-1047** — Hand-authored typed `migration.def` gseeds for semantic changes signed by substrate identity: semantic migrations are auditable.
- **INV-1048** — Lineage-preserving migration via `migration.applied` mutation rather than history rewrite: substrate's lineage chain stays unbroken across version bumps.
- **INV-1049** — Inverse-migration rollback support with explicit irreversible marker: migrations are reversible by default, lossy ones flagged.
- **INV-1050** — [N-2, N] multi-version runtime interop with typed downgrade map: substrate runtime tolerates a window of older gseed versions.
- **INV-1051** — Deprecated-not-removed cycle (one minor version minimum): primitives don't disappear without warning.
- **INV-1052** — `gspl migrate --dry-run` reporting changed gseeds before application: migrations are reviewable before commit.
- **INV-1053** — Test-suite-driven migration verification via `gspl test --migrate`: migration correctness is structurally testable.

## Open follow-ups
- Phase-1 v0.1 → v0.2 migration as the first real-world test.
- Migration registry for community-authored migrations — deferred to v0.3.
- Cross-substrate-version diffing UI — Phase 1.
- Per-mod migration coordination — deferred to v0.3.
- v1.0 stability commitment finalization — Phase 1 deliverable.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 217 — CLI and headless toolchain.
3. Brief 223 — Package registry and distribution.
4. Rails ActiveRecord Migrations.
5. Django Migrations framework.
6. Apache Avro schema evolution.
7. Protocol Buffers backward compatibility rules.
8. semver.org specification.
