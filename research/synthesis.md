# Synthesis — Technical R&D, round 1

This document folds the twelve briefs in this directory into a single set of cross-cutting findings, a spec impact summary, and a Phase 1 plan delta. It exists so that an AI coding agent (or a human engineer) starting Phase 1 can read one document and know what changed.

## Headline findings

1. **The hash domain must be the *uncompressed* canonical payload, not the compressed bytes.** zstd is not bit-stable across versions or SIMD levels, so any hash that includes compressed bytes will diverge across machines. This is the single most consequential normative change in the round and reverses an implicit assumption in the original spec. (Brief 005.)

2. **Cross-vendor GPU determinism is achievable only by running the proof-bearing kernels in fixed-point integer arithmetic.** Floating-point WGSL is not bit-stable across NVIDIA / AMD / Intel / Apple. The kernel pipeline splits into a "proof-bearing core" (fixed-point, hashed) and a "post-processing tail" (float, not hashed). (Brief 001.)

3. **The portable WGSL subset is much narrower than the WebGPU spec.** Mesh shaders, cooperative matrix, atomic floats, subgroup float reductions, and non-core texture formats are all forbidden at v1. The remaining subset is documented as a normative table in Brief 002.

4. **Refinement types are a v2 feature, not a v1 feature.** A solo founder cannot ship a Liquid-Types implementation in Phase 1. v1 ships vanilla Hindley-Milner; v1.5 adds datasort refinements; v2 adds SMT-backed refinements. The spec must stop promising compile-time refinement checking at v1 and explicitly mark the v1 invariants that are runtime-checked at the kernel boundary. (Brief 006.)

5. **The existing C2PA + image watermark + audio watermark architecture already covers the technical requirements of EU AI Act Article 50.** No new primitives are needed for August 2026 compliance. The spec needs a mapping document and a one-week fold-in window in July 2026 for the final Code of Practice. (Brief 010.)

6. **Watermarks are probabilistic provenance signals, not guarantees.** Both image (DCT, Brief 008) and audio (audiowmark, Brief 009) watermarks have honestly-documented robustness envelopes that survive single-stage common attacks but degrade under combined or multi-stage attacks. The spec must say so in writing and rely on the "state of the art" defense from EU AI Act Article 50.

7. **`audiowmark` is GPLv3 and must be invoked as a subprocess, not linked.** This is the only cross-cutting license issue in the round. The subprocess integration model is workable but constrains the runtime architecture. (Brief 009.)

8. **The agent reliability story rests on constrained decoding + type-constrained decoding + a 200-prompt conformance suite.** Published evidence supports 99%+ parse success and 95%+ task accuracy on constrained DSLs; Paradigm must measure on its own DSL before committing to specific error budgets. (Brief 011.)

9. **The MAP-Elites archive at v1 is a 4,096-cell, surrogate-assisted, checkpointable evolution loop with a ~50,000-evaluation seeding budget.** Larger archives are deferred to v2. Without the surrogate-assisted reduction, the budget is unrealistic for a solo founder. (Brief 012.)

10. **Every load-bearing dependency is pinned and treated as a determinism event on bump.** wgpu, p256, c2pa, zstd, audiowmark, the LLM provider — all are pinned at exact version (or exact commit), and bumping any of them re-runs a conformance suite. (Briefs 001, 002, 004, 005, 007, 009, 011.)

## Cross-cutting risks

- **Pin discipline is the load-bearing operational practice for the entire spec.** If the team (one person plus future contributors) gets sloppy about pinning, the determinism, compliance, and reliability stories all degrade silently.
- **Empirical measurement is required before committing to several headline numbers** (kernel per-evaluation cost, agent reliability, c2pa-rs latency, watermark BER on Paradigm content). Phase 1 must do these measurements early — they gate downstream decisions.
- **Phase 1 scope creep is the biggest project-level risk.** Every brief identified Phase 1 tasks; the synthesis must pick the minimal set that actually unlocks the next phase rather than running every recommended measurement.
- **Solo-founder operational fragility**: every subsystem must fail safely without a human in the loop. Briefs 005, 011, and 012 each address this in their own area; the synthesis flags it as a global property, not a per-subsystem one.

## Spec impact summary

The complete list of files this round's briefs touch. Each entry is "file → action → source brief".

### Files to rewrite (normative changes)

| File | Action | Brief |
|---|---|---|
| `proof/content-hash.md` | Hash the *uncompressed* canonical payload, not compressed bytes | 005 |
| `dsl/types.md` | Drop refinement promises at v1; add three-milestone phasing | 006 |
| `compliance/eu-ai-act.md` | Fold in Article 50 mapping, Code of Practice tracking, July 2026 window | 010 |
| `compliance/watermark-image.md` | Mid-frequency DCT band, BCH, sync template, robustness envelope | 008 |
| `compliance/watermark-audio.md` | audiowmark via subprocess, strength rules, robustness envelope | 009 |
| `agent/reliability.md` | Layered architecture, conformance suite, error budgets | 011 |
| `evolution/map-elites.md` | 3-dim 16-bin grid, surrogate-assisted, checkpointable | 012 |

### Files to update (additive)

| File | Action | Brief |
|---|---|---|
| `kernels/README.md` | Add fixed-point determinism root + portable WGSL subset table | 001, 002 |
| `runtime/gpu-pipeline.md` | wgpu version pin, conformance matrix | 001, 002 |
| `runtime/export-pipeline.md` | Single-thread zstd default, watermark steps, latency budgets | 005, 008, 009 |
| `formats/file-format.md` | Compression layer is not proof-bearing; external manifest mode | 005, 007 |
| `formats/seed.md` | Numeric fields are integers in safe-integer range | 003 |
| `proof/canonicalization.md` | UTF-16 sort rule + worked example + conformance vector list | 003 |
| `proof/signature.md` | Curve, hash, encoding, API choice, no randomized ECDSA | 004 |
| `compliance/c2pa-binding.md` | Pin c2pa version, Builder/Reader API, Paradigm custom assertion | 007, 010 |
| `infrastructure/library-canon.md` | Pin every load-bearing dependency, document bump process | all |
| `infrastructure/ci.md` | WGSL linter, JCS conformance suite, reliability conformance suite | 002, 003, 011 |
| `agent/architecture.md` | 5-stage pipeline + Layer 1-4 reliability backstops | 011 |
| `evolution/cma-es.md` | CMA-ES state per active cell | 012 |
| `evolution/ucb1.md` | Operator pool fixed | 012 |
| `dsl/inference.md` | Algorithm J / Damas-Milner approach for v1 | 006 |
| `roadmap/phase-1.md` | Adjust scope to v1 type system + measurements | 006 |
| `roadmap/phase-2.md` | Add v1.5 datasort + v2 Liquid Types milestones | 006 |

### New files to create

| File | Purpose | Brief |
|---|---|---|
| `kernels/wgsl-style.md` | Operational WGSL rules (workgroup sizes, layout, linter) | 002 |
| `dsl/runtime-checks.md` | Invariants runtime-checked at v1 | 006 |
| `agent/grammar.md` | GSPL DSL grammar in constrained-decoding form | 011 |
| `agent/budgets.md` | Per-request latency / token / repair caps | 011 |
| `evolution/behavior-descriptors.md` | The 3 v1 behavior descriptors + versioning | 012 |
| `evolution/surrogate.md` | Surrogate model, training data, retraining | 012 |
| `evolution/budgets.md` | Evaluation budgets and convergence criteria | 012 |
| `evolution/checkpoint-format.md` | Checkpoint serialization format | 012 |
| `compliance/eu-ai-act-mapping.md` | Obligation-to-primitive mapping table | 010 |
| `compliance/ca-sb942.md` | California parallel | 010 |
| `compliance/c2pa-fallback.md` | Contingency plan | 007 |
| `compliance/watermark-adversarial.md` | v2 placeholder | 008 |

### New ADRs to write

| ADR | Topic | Brief |
|---|---|---|
| `adr/00NN-fixed-point-kernel-core.md` | Why proof-bearing kernels use fixed-point | 001 |
| `adr/00NN-wgsl-portable-subset.md` | The v1 portable WGSL subset table | 002 |
| `adr/00NN-jcs-implementation.md` | Build vs buy for JCS | 003 |
| `adr/00NN-deterministic-ecdsa.md` | Curve / hash / library / encoding | 004 |
| `adr/00NN-hash-domain-is-uncompressed.md` | The uncompressed-payload hash decision | 005 |
| `adr/00NN-type-system-phasing.md` | v1 / v1.5 / v2 type system milestones | 006 |
| `adr/00NN-c2pa-rs-dependency.md` | Single-vendor library acceptance | 007 |
| `adr/00NN-image-watermark-scheme.md` | DCT + BCH + sync template | 008 |
| `adr/00NN-audiowmark-via-subprocess.md` | GPL via subprocess | 009 |
| `adr/00NN-eu-ai-act-compliance-posture.md` | Existing primitives + July 2026 fold-in | 010 |
| `adr/00NN-agent-reliability-architecture.md` | Layered reliability | 011 |
| `adr/00NN-llm-provider-pin.md` | LLM pin and bump process | 011 |
| `adr/00NN-evolution-budgets-v1.md` | 50K seeding / daily / burst | 012 |
| `adr/00NN-surrogate-assisted-map-elites.md` | Surrogate choice and rationale | 012 |

## Phase 1 plan deltas

The original Phase 1 plan needs the following changes based on this round of research.

### New Phase 1 tasks (load-bearing measurements)

1. **Fixed-point kernel performance pilot** — measure throughput of a representative kernel stage in `Q16.16` vs `f32` on NVIDIA, AMD, Intel iGPU, and Apple Silicon. Goes/no-goes the determinism strategy from Brief 001.
2. **WGSL portable-subset linter** — small in-tree tool that rejects forbidden features. Required for any kernel work to start.
3. **GPU determinism conformance suite** — same seeds, four vendors, hash equality. Required before any kernel ships.
4. **JCS conformance suite + chosen implementation (build or buy)** — the 13 conformance vectors from Brief 003. Required before any seed is signed.
5. **`p256` ECDSA RFC 6979 vector test** — verify against the RFC's published vectors. One-day task.
6. **`c2pa-rs` latency benchmark harness** — p50/p95/p99 for Builder::sign and Reader on representative payloads.
7. **DCT image watermark robustness harness** — Paradigm-encoded test set vs the standard attack corpus from Brief 008.
8. **`audiowmark` robustness harness** — same idea as image, plus measurement of subprocess invocation overhead.
9. **HM type checker prototype** — one-week prototype to validate the 2-4 week v1 estimate from Brief 006.
10. **Datasort refinement prototype** — two-week prototype to validate the 4-8 week v1.5 estimate.
11. **LLM bake-off on a 50-prompt seed conformance suite** — pick the v1 model and provider.
12. **Constrained-decoding library bake-off** — pick the v1 tooling.
13. **MAP-Elites pilot run** — 1,000 evaluations on a representative kernel to validate the per-evaluation cost estimate.

### Tasks deferred from Phase 1 to later phases

- **Refinement type system** — moves from "v1" to "v1.5 (datasorts) and v2 (Liquid Types)."
- **Mesh-shader fast path for the geometry kernel** — moves from v1 to "re-evaluate at v2."
- **Federated exemplar archives** — moves from "v1 nice-to-have" to "v2."
- **Adversarial-removal-resistant watermarks** — explicitly v2.
- **Custom Paradigm trust list** — explicitly v2.

### Tasks the round confirmed are still on track

- Kernel pipeline architecture is sound; the changes are about *where* float vs fixed-point lives.
- C2PA integration is sound; the choice is `c2pa-rs` and the operational rules.
- Watermark integration is sound; the changes are about honest envelopes and the GPL subprocess model.
- Agent architecture is sound; the changes are about explicit error budgets and the reliability conformance suite.
- Evolution loop architecture is sound; the changes are about budget realism and surrogate assistance.

## Open follow-ups not resolved by this round

- **Behavior descriptor design for MAP-Elites** — load-bearing for archive usefulness; needs its own brief.
- **LLM model and provider selection** — needs the bake-off, then a brief.
- **Constrained-decoding library selection** — same.
- **Subgroup operations stability across wgpu releases** — track upstream.
- **AAC audio watermark survival rates** — needs the empirical harness from Brief 009.
- **`c2pa-rs` 1.0 release tracking** — re-evaluate operational rules when it ships.
- **Final EU AI Act Code of Practice (June 2026)** — fold in via the July 2026 window.
- **Per-request cost model for the agent (free tier vs paid tier)** — product decision, flagged for follow-up.
- **External legal review of the EU AI Act mapping document** — needed before any release in the EU.
- **Constant-time audit of the pinned `p256` field arithmetic** — needed before any release.

## How to use this synthesis

1. **Before writing kernel code**, read Briefs 001, 002, and the corresponding rows in the spec impact table. Then read `kernels/README.md` (post-update) and `runtime/gpu-pipeline.md` (post-update).
2. **Before writing seed serialization or proof code**, read Briefs 003, 004, 005 and the corresponding spec impact rows. The single most important thing is "the hash is over the uncompressed canonical payload."
3. **Before writing the type system or DSL inference**, read Brief 006 and `dsl/types.md` (post-update). v1 is vanilla HM. Refinements are not a v1 feature.
4. **Before writing the export pipeline**, read Briefs 007, 008, 009, 010 and confirm the C2PA + watermark + EU AI Act story.
5. **Before writing the agent**, read Brief 011 and `agent/reliability.md` (post-update). Build the conformance suite first; everything depends on it.
6. **Before writing the evolution loop**, read Brief 012 and `evolution/map-elites.md` (post-update). Build the surrogate first; the budget assumes it.
7. **Whenever you bump a pinned dependency**, re-run the relevant conformance suite. No exceptions.

## Round 1 status

All twelve briefs are written. Confidence ratings range 3-4. No brief reached 5 because every recommendation depends on at least one Phase 1 measurement that has not yet been performed. This is expected and consistent with the methodology in `research/README.md`.

The next research round (round 2, post-Phase-1 measurements) should re-evaluate every brief whose confidence is below 4 and update or replace it based on the empirical data.
