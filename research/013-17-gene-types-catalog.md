# 013 — The 17 gene types: complete catalog, semantics, operators

> **SUPERSEDED — see `spec/02-gene-system.md`.** This brief is Round-1 research. The locked kernel gene type catalog is `spec/02-gene-system.md`. Where this brief and spec/02 disagree, **spec/02 wins**. Operator hints in this brief (BLX-α, SBX, OKLab ΔE, Hausdorff distance, etc.) survive as implementation guidance for the matching spec/02 type.

## Question
What is the complete v1 catalog of GSPL gene types, what does each one mean semantically, and what mutation / crossover / distance / validation operators must each one ship with?

## Why it matters
The 17-type gene system is GSPL's identity. If two engines disagree on what a `ColorGene` means or how it mutates, every cross-domain composition is broken. The gene type system is the *only* place in the spec where the DSL surface, the kernel pipeline, the proof system, the breeding system, and every domain engine intersect.

## What we know from the spec
- `spec/02-gene-system.md` names 17 gene types but does not yet pin operator semantics for each.
- `algorithms/` has scaffolding for some operators but not a complete cross-product.
- Cross-domain composition (`architecture/cross-domain-composition.md`) assumes gene types are stable across engines.

## Findings (the 17 types)

| # | Gene type | Domain | Mutation operator | Crossover operator | Distance metric | Validation invariant |
|---|---|---|---|---|---|---|
| 1 | **ScalarGene** | ℝ | Gaussian step σ scaled to range | Arithmetic mean, BLX-α, SBX | Absolute or normalized | Within `[lo, hi]` |
| 2 | **IntGene** | ℤ | ±k step or geometric step | Midpoint or one-of | Absolute | Within `[lo, hi]` |
| 3 | **BoolGene** | {0,1} | Bit flip with prob p | Uniform | Hamming | None |
| 4 | **CategoricalGene** | finite set | Resample, swap-to-neighbor | One-of | 0/1 or learned | Member of set |
| 5 | **ColorGene** | OKLab L,a,b | Per-channel Gaussian in OKLab | Channel-wise mean or one-of | ΔE in OKLab | In gamut after sRGB conversion |
| 6 | **VectorGene<N>** | ℝⁿ | Per-component Gaussian, optional simplex projection | Component-wise BLX | L2 or cosine | Norm/sum constraint |
| 7 | **CurveGene** | spline / Bézier | Control-point Gaussian + topological repair | Knot-aware blend | Hausdorff or area | Monotonicity if required |
| 8 | **GraphGene** | DAG / tree | Node add/remove/relabel, edge rewire | Subtree swap, induced-subgraph mix | Graph edit distance | Acyclic, typed |
| 9 | **GridGene** | discrete N-D grid | Cell mutation, region swap, WFC repair | Region crossover | Hamming or Wang-tile | Adjacency rules satisfied |
| 10 | **SequenceGene** | ordered list | Insert/delete/swap/transpose | Order-preserving (PMX, OX) | Edit distance | Length ∈ [min,max] |
| 11 | **PolygonGene** | 2D/3D polygon | Vertex jitter, edge split/collapse | Vertex-wise blend with re-triangulation | Polygon Hausdorff | Manifold, non-self-intersecting |
| 12 | **WaveGene** | audio/signal | Amplitude/phase jitter, time-stretch | Spectral mix, Griffin-Lim repair | Spectral L2 or PESQ | Sample-rate normalized |
| 13 | **TextGene** | constrained string | Token replace from vocab, n-gram swap | Cut-and-stitch | Levenshtein on tokens | Grammar/vocab valid |
| 14 | **AffineGene** | SE(3) transform | Rotation jitter (axis-angle) + translation Gaussian | SLERP for rotation, lerp for translation | Rotation angle + translation L2 | Orthonormal rotation |
| 15 | **DistributionGene** | parameterized PDF | Parameter Gaussian | Wasserstein interpolation if available | Wasserstein or KL | Parameters in admissible set |
| 16 | **MaterialGene** | PBR (albedo, metallic, roughness, normal) | Per-channel mutation | Channel mix | Channel L2 in perceptual space | Energy-conserving (albedo+specular≤1) |
| 17 | **BehaviorGene** | finite-state machine / behavior tree | State add/remove, transition rewire | Subtree swap | Tree edit distance | Reachability, no deadlocks |

## Risks identified

- **Cross-engine semantic drift**: an engine that interprets `CurveGene` as Catmull-Rom while another interprets it as cubic Bézier breaks composition. Operators are not enough — the *parameterization* must also be pinned.
- **Operator non-closure**: a mutation can produce a gene that violates its validation invariant (e.g., a polygon vertex jitter that creates a self-intersection). Every operator must ship with a *repair* fallback.
- **Distance metrics that aren't true metrics** (no triangle inequality) break MAP-Elites cell assignment and novelty search. Three of the listed metrics (graph edit distance variants, BehaviorGene tree edit) are only pseudo-metrics; the spec must pick concrete formulations that satisfy the metric axioms.
- **Composition under types**: a `ColorGene` from a SpriteEngine has to bind to a `ColorGene` slot in a UIEngine without a manual converter. The type system must enforce this.

## Recommendation

1. **Adopt the 17-type catalog above as normative**, with the operator and metric columns frozen at v1.
2. **Every gene type ships a `Repair` operator** that takes a possibly-invalid gene and returns the nearest valid gene under the type's distance metric. Mutation = naive mutation ∘ repair.
3. **The kernel rejects any seed whose genes do not pass validation** at load time. There is no "best effort" mode.
4. **Each gene type has a stable serialization** (binary + JSON canonical) pinned in `spec/06-gseed-format.md`. Cross-implementation interop tests are mandatory.
5. **Cross-engine semantic equivalence** is enforced by a typed coercion table — not by string matching on type names. The coercion table is part of the spec.
6. **Reserve gene type IDs 18-31** for future types. (Brief 020 proposes the next five.)

## Confidence
**4/5.** The 17 types are recognizable from established type theory and evolutionary computation literature. The 4/5 reflects two open items: the BehaviorGene operator suite is the least mature and may need more empirical work, and the distance-metric formulations need to be checked against the metric axioms before being frozen.

## Spec impact

- `spec/02-gene-system.md` — embed the table verbatim as the normative catalog.
- `algorithms/` — one file per gene type with the operator pseudocode.
- `spec/06-gseed-format.md` — pin the binary + JCS serialization for each type.
- New ADR: `adr/00NN-gene-type-catalog-v1.md`.

## Open follow-ups

- Verify each distance metric satisfies the metric axioms; replace any that fail.
- Build the cross-implementation interop test suite for serialization.
- Empirically tune mutation step sizes per gene type using exemplar archives.
- Decide whether `MaterialGene` should be split into per-channel sub-types or kept as a composite.

## Sources

- Eiben & Smith, *Introduction to Evolutionary Computing*, 2nd ed. (canonical operator survey).
- Deb, *Multi-Objective Optimization Using Evolutionary Algorithms* (SBX, BLX-α).
- Stanley & Miikkulainen, *Evolving Neural Networks through Augmenting Topologies* (NEAT — graph operators).
- Gumin, *WaveFunctionCollapse* (grid adjacency repair).
- Internal: `spec/02-gene-system.md`, `architecture/cross-domain-composition.md`.
