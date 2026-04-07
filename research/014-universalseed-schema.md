# 014 — UniversalSeed schema invariants and validation

## Question
What is the complete set of structural invariants the UniversalSeed schema must enforce, and how does the validator catch violations before any kernel run?

## Why it matters
Every Paradigm artifact is grown from a UniversalSeed. If a malformed seed reaches the kernel, the determinism, proof, and breeding stories all break in subtle ways. The validator is the only firewall.

## What we know from the spec
- `spec/01-universal-seed.md` defines the seed as a typed graph of genes plus metadata.
- The spec implies but does not enumerate the structural invariants.

## Findings — the invariant catalog

**Structural invariants:**
1. **Top-level shape**: a seed is an object with exactly the fields `version`, `domain`, `genes`, `composition`, `metadata`, `signature`.
2. **Version field** is a SemVer string and must match a known schema version.
3. **Domain field** is one of the 26 domain identifiers.
4. **Genes field** is an ordered, named map. Names are unique within a seed and follow `snake_case` with length ≤ 64.
5. **Each gene** has `type` (one of the 17), `value`, `range` (where applicable), and optional `tags`.
6. **Composition field** is a DAG of gene references describing how genes feed downstream stages. No cycles.
7. **Metadata** carries author key, creation time, lineage parent IDs (zero, one, or two), and optional human label.
8. **Signature** is a 64-byte `r||s` ECDSA signature over the JCS canonical form of the rest of the seed (per Brief 004).

**Type invariants:**
9. Every gene's `value` matches its `type`'s value space (Brief 013).
10. Every gene passes its type's validation operator.
11. Every gene reference in `composition` resolves to an existing gene name.
12. Every cross-domain reference in `composition` carries a coercion tag from the spec's typed coercion table.

**Lineage invariants:**
13. `lineage_parents` IDs (if present) reference seeds that exist in the local archive or are accompanied by their canonical hashes.
14. If lineage parents are present, the seed's `composition` must be derivable from a breeding operator over those parents (verifiable but not always cheap).

**Proof invariants:**
15. Signature verifies against the author public key embedded in metadata.
16. The canonical content hash matches the value referenced by any C2PA assertion (per Brief 007).

**Resource invariants:**
17. Total gene count ≤ a per-domain budget (e.g., 1024 for sprite, 16384 for fullgame).
18. No gene's value blob exceeds a per-type byte budget.
19. Total seed size ≤ 1 MiB uncompressed at v1 (revisable).

## Risks identified

- **Validator drift across implementations** is the worst class of bug — a seed that passes one validator and fails another. Mitigation: a normative validator test suite.
- **Lineage cycles** introduced by malicious or buggy clients (a "child" referencing itself) — prevent at validation, not at runtime.
- **Resource invariants too tight** kill expressiveness; too loose enable DoS. The numbers above are first cuts and need empirical calibration.
- **Cross-domain coercion drift** (a `ColorGene` from sprite → ui that carries different gamut assumptions) — solved by the typed coercion table being normative.

## Recommendation

1. **Embed the 19 invariants above in `spec/01-universal-seed.md` as a numbered list.** Reference them by number from the validator implementation.
2. **Validator pseudocode lives in `algorithms/seed-validator.md`** with a stable function signature.
3. **A normative validator conformance suite** (≥ 200 valid seeds and ≥ 500 invalid seeds, each invalid seed labeled with the invariant it violates) ships in the repo.
4. **Validation is deterministic and side-effect-free.** It returns either `Valid` or `Invalid(reason, invariant_id, gene_path)`.
5. **The validator is invoked at three points**: load (any seed entering the system), pre-mutation (in evolution), pre-export (before any artifact ships). Three calls, same code.
6. **Resource budgets per domain** live in a single table in `infrastructure/resource-budgets.md` so they can be tuned without spec churn.

## Confidence
**4/5.** The invariants are derived directly from the spec's existing structure and standard schema-validation practice. The 4/5 reflects the empirical calibration debt on the resource budgets.

## Spec impact

- `spec/01-universal-seed.md` — add numbered invariant list.
- `algorithms/seed-validator.md` — new file with pseudocode.
- `tests/validator-conformance.md` — new file describing the conformance suite.
- `infrastructure/resource-budgets.md` — new file with per-domain budgets.
- New ADR: `adr/00NN-validator-architecture.md`.

## Open follow-ups

- Empirically calibrate per-domain resource budgets from real seeds in the existing 182K-LOC codebase.
- Decide whether validator errors are user-readable strings or stable error codes (recommendation: both — codes for tools, strings for humans).
- Reserve a "warning" severity for invariants that should never block but should be surfaced (e.g., "you're at 95% of the gene budget").

## Sources

- JSON Schema 2020-12 spec (general schema validation patterns).
- Internal: `spec/01-universal-seed.md`, Brief 004 (signature), Brief 007 (C2PA).
