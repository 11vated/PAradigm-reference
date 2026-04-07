# 018 — Versioning and migration: how seeds survive spec evolution

## Question
How does GSPL evolve its spec, gene types, file format, and operators over years without breaking older seeds, while keeping reproducibility and proofs intact?

## Why it matters
A `.gseed` from 2026 must still load, validate, render, and verify in 2036. The competition (Stable Diffusion checkpoints, Unity project files, Blender .blend) routinely strands users on old versions. GSPL's promise of decade-scale reproducibility is only credible with a versioning discipline planned from day one.

## What we know from the spec
- `spec/06-gseed-format.md` reserves a `format-version` field (Brief 015).
- `spec/01-universal-seed.md` reserves a SemVer `version` field on each seed.
- No migration story exists yet.

## Findings — versioning across four layers

GSPL has **four independently versioned things**, and conflating them is the most common mistake in long-lived formats:

1. **Spec version** — the document version of `spec/01-universal-seed.md` and friends. SemVer.
2. **File format version** — the binary layout of `.gseed` (Brief 015's `format-version` field). Major-version-only; bumps only when the layout itself changes.
3. **Gene type version** — each of the 17 gene types has its own version. A `ColorGene v1` and `ColorGene v2` may coexist in the same seed.
4. **Operator version** — every breeding/mutation operator is named with a version suffix (e.g., `mutate.gaussian.v1`). Once shipped, an operator version is frozen forever.

**The rules:**

- **Spec evolves monotonically**: any change is either a no-op (clarification), additive (new optional field, new gene type, new operator version), or a major break (new file format version).
- **Additive changes do not break old readers** as long as old readers ignore unknown optional sections (Brief 015's section ID rules).
- **Major breaks bump the file format version**. v1 readers refuse to load v2 files. The studio offers a migration tool that rewrites v1 → v2.
- **Gene types are never removed**. A deprecated gene type stays in the catalog with a `deprecated_since` annotation; readers warn but still load.
- **Operator versions are never reused**. `mutate.gaussian.v1` is frozen; if its semantics change, it becomes `mutate.gaussian.v2`. Lineage replay always uses the version stamped in the edge record.

**Migration tool design:**

- Pure function: `migrate(old_seed, target_version) → new_seed | error`.
- Migration is *content-preserving where possible*: every gene that maps cleanly from old to new is preserved bit-for-bit. Genes with no mapping become `legacy.<old_type>` extensions and trigger a warning.
- Migration is *not* a retroactive rewrite of lineage. The migrated seed is a new seed with a new content hash; its lineage records the original as a parent with the operator `migrate.<from>.<to>.v1`.
- Migrations are testable: every migration ships with a corpus of `(old_seed, expected_new_seed)` pairs in `tests/migration-conformance.md`.

**Reproducibility across versions:**

- Every breeding edge stores the *spec version* and *operator version* used. Replay always uses those exact versions, even if the verifier has a newer spec installed.
- This requires shipping multiple operator implementations side-by-side. Old operator versions are kept indefinitely. Compute cost is bounded — operators are small.
- The reference implementation ships with a *bundled archive of past spec versions* so a fresh checkout can replay any historical seed.

**Deprecation path:**

- A spec change that obsoletes a gene type or operator goes through three phases over at least one year:
  1. **Soft deprecation**: documentation says "deprecated, use X instead." Readers and writers continue to support it without warning.
  2. **Warned deprecation**: validators emit a warning when encountering the type/operator. Tooling encourages migration.
  3. **Frozen**: type/operator removed from the writer's vocabulary. Reader continues to load and replay. This is the terminal state — never removed beyond frozen.

## Risks identified

- **Major-version churn** breaks the contract. The discipline must be: only bump file format version when truly necessary, not for cosmetic reasons. Target: at most one major bump every five years.
- **Migration tool bugs** silently corrupt seeds. Mitigation: every migration produces a sidecar diff log, and the migration corpus is run on every release.
- **Operator implementation drift**: a v1 operator subtly changes when reimplemented for a new platform. Mitigation: golden-output tests for every operator on every supported platform, locked in CI.
- **Bundled archive grows** without bound. Reality check: operators are small (a few KB each); ten years of operators is still a few MB.
- **Validator strictness changes** are also a versioning concern. Mitigation: validator strictness is tied to the spec version, not the validator binary version. A v1 seed is always validated by v1 rules.

## Recommendation

1. **Adopt the four-layer versioning model.** Document in `architecture/versioning.md`.
2. **SemVer for spec and gene types.** Major version for the file format. Frozen-version-suffix for operators.
3. **Operators are immutable post-release.** New behavior = new version suffix.
4. **Old gene types are never removed.** Three-phase deprecation, frozen as the terminal state.
5. **Migration is a lineage operation**, not a rewrite. The migrated seed has its own ID and a `migrate.<from>.<to>.v1` parent edge.
6. **Reference implementation bundles historical operators and validators** so any historical seed can be loaded and replayed locally.
7. **Migration corpus** lives in `tests/migration-conformance.md` and is part of CI.
8. **At most one file format major bump per 5 years.** Hard target.

## Confidence
**4/5.** The model follows long-lived format best practices (PNG, PDF, USD). The 4/5 reflects the inability to know now how often genuine major bumps will be needed; the 5-year target is aspirational.

## Spec impact

- `architecture/versioning.md` — new file with the four-layer model.
- `spec/01-universal-seed.md` — pin SemVer field semantics.
- `spec/06-gseed-format.md` — pin file format major-version semantics.
- `algorithms/migration.md` — migration tool API and pseudocode.
- `tests/migration-conformance.md` — corpus.
- New ADR: `adr/00NN-versioning-discipline.md`.

## Open follow-ups

- Decide where the bundled historical archive lives — in the binary, on a CDN, or as a separately downloadable pack.
- Build the migration tool reference implementation. Phase 1.5 task (after v1 ships).
- Define the exact validator-strictness-pinning mechanism (probably: load-time spec version detection branches into version-specific validator code paths).

## Sources

- PNG specification (chunk additivity rules).
- Pixar USD versioning policy.
- Semantic Versioning 2.0.0.
- Internal: Briefs 014 (validator), 015 (file format), 017 (lineage).
