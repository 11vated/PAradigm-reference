# Brief 096 — Style adapter quality acceptance criteria

## Question

How does GSPL prove that its 80 style adapters (Brief 088) actually preserve character identity across every art style, and what measurable acceptance criteria must each adapter pass before being signed under the foundation identity?

## Why it matters

Brief 088 promised cross-art-style character coherence: a character defined once must be expressible in pixel art, anime, watercolor, claymation, cubism, ukiyo-e, voxel, Pixar-grade CG, Ghibli-grade hand-painted, and 70+ more styles **without losing identity**. That promise is the substrate's most visible claim. If a user forks the armory's "stoic masked archer" and renders them in 80 styles and the results look like 80 different people, the substrate has failed its most public test — and every remaining library loses credibility by association.

Style adapter quality cannot be hand-waved as "looks good to me." It must be **measurable, reproducible, and rejection-gated**.

## What we know from spec

From Brief 088 and INV-341 (character as substrate primitive with style invariants), INV-342 (substrate identity embedding from synthetic-only data), INV-344 (cross-engine character coherence contract):

- A character has a canonical identity embedding trained on synthetic-only data (no living persons).
- Style invariants are enforced at composition time: silhouette, color-palette weight distribution, proportional landmarks, costume signature elements.
- Style adapters are composable with `char://` gseeds and produce a rendered result in the adapter's medium.
- 80 adapters planned: pixel art (8-bit, 16-bit, 32-bit), anime (shonen, shoujo, seinen, sakuga), cartoon (Western 2D TV, Disney renaissance, modern-flat), Pixar-grade CG, Ghibli-grade hand-painted, claymation (Aardman, Laika), watercolor, ink wash, ukiyo-e, cubism, voxel, low-poly, photoreal, and many more.

What Round 4 did *not* specify: the exact metrics, thresholds, gold-standard test set, or acceptance workflow.

## Findings

### Finding 1: Identity preservation has four orthogonal axes

Research on face recognition, character illustration consistency, and style transfer (ArcFace, CLIP identity probes, Character-Aware StyleGAN research, the DreamBooth fidelity literature) converges on four orthogonal identity axes:

1. **Structural identity** — silhouette, proportion, landmark layout. Measured by silhouette IoU against a canonical pose render and by landmark distance in a style-normalized latent.
2. **Chromatic identity** — color palette weight distribution, signature color preservation. Measured by weighted ΔE against the character's canonical palette.
3. **Costume/signature identity** — the object-level features that make the character recognizable even in silhouette (mask shape, weapon, distinctive garment). Measured by per-signature-element presence check and location IoU.
4. **Expressive identity** — the character's bearing, the way they inhabit space. Hardest to measure; proxied by FACS intensity distribution match and pose-axis angular distance.

A style adapter that preserves 1–3 but drops 4 produces characters that are "technically the same person but feel wrong." The acceptance criteria must cover all four.

### Finding 2: Gold-standard test sets come from combinatorial coverage, not cherry-picked demos

Comparable efforts (DreamBooth evals, ControlNet model cards, IPAdapter benchmarks) all use **combinatorial** test grids: N characters × M poses × P expressions × Q lighting conditions = test cases. The specific numbers vary but the discipline is consistent: style adapter acceptance requires a published test grid, not a showreel.

GSPL's test grid for each style adapter:

- **10 canonical characters** drawn from the Foundation Kernel (diverse archetypes: masked warrior, child scholar, elder craftsman, armored knight, robed mage, field worker, creature-hybrid, non-humanoid sentient, elderly non-human, child non-human).
- **12 canonical poses** (neutral standing, walking, running, jumping, sitting, crouching, reaching, pointing, defensive, offensive, reclining, crowd-pose).
- **8 canonical expressions** (neutral, joy, anger, grief, fear, surprise, concentration, exhaustion).
- **5 lighting conditions** (high-key, low-key, backlit, golden hour, moonlight).

= **4,800 renders per adapter**. At 80 adapters that's 384,000 renders in the full acceptance grid. Rendering is cheap relative to review; the bottleneck is the measurement pipeline, not the render count.

### Finding 3: Thresholds come from a baseline calibration, not invention

Rather than making up thresholds, GSPL calibrates thresholds against a **reference adapter cohort** — three adapters that are obviously high quality by human judgment (e.g., Pixar-grade CG, Ghibli-grade hand-painted, shonen anime). The distributions of structural IoU, chromatic ΔE, signature presence, and expressive angular distance for the reference cohort become the **pass floor** for every other adapter. An adapter that can't match the reference cohort's 25th percentile on any axis fails.

This turns adapter acceptance from a subjective fight into a calibration problem.

### Finding 4: Failure modes cluster into six taxonomized categories

Review of style transfer failures in published research and community forums shows six dominant failure modes:

1. **Identity collapse** — character becomes generic in the style (most common). Caught by structural + chromatic metrics.
2. **Signature drop** — mask, weapon, or distinctive garment vanishes. Caught by signature presence check.
3. **Proportion drift** — child character renders as adult, or vice versa. Caught by landmark distance and proportion ratio checks.
4. **Expression flattening** — complex expressions collapse to neutral. Caught by FACS intensity match.
5. **Chromatic hijacking** — the style's palette overwhelms the character's signature colors. Caught by weighted ΔE.
6. **Pose instability** — the character's weight and balance change between renders of the same pose. Caught by pose-axis angular distance and silhouette consistency across the pose row of the grid.

Every style adapter must have documented behavior on each failure mode.

### Finding 5: Mutation testing catches adapter brittleness

A mutation test perturbs the input character gseed by a small epsilon (palette shift by 5 ΔE, pose angle shift by 3°, landmark shift by 2px) and checks that the output adapter render shifts correspondingly. Adapters that produce wildly different outputs for small input perturbations are brittle and fail — even if their grid scores are fine. This catches adapters that overfit to specific characters.

## Inventions

### INV-388 — The four-axis identity preservation metric

A composite metric with four axes, each independently enforced:

- **Structural identity score (SIS)** = weighted mean of silhouette IoU (0.4) + landmark distance score (0.4) + proportion ratio deviation (0.2). Range 0–1, higher is better.
- **Chromatic identity score (CIS)** = inverse weighted ΔE against canonical palette, normalized. Range 0–1, higher is better.
- **Signature presence score (SPS)** = fraction of signature elements present × mean location IoU. Range 0–1, higher is better.
- **Expressive identity score (EIS)** = cosine similarity of FACS intensity vectors + pose-axis angular match. Range 0–1, higher is better.

No averaging across axes. An adapter passes only if **every axis independently** meets its threshold.

### INV-389 — The 4,800-render canonical acceptance grid

The combinatorial test grid (10 × 12 × 8 × 5) is published, immutable once frozen for a given substrate version, and re-run on every adapter candidate. Results are signed lineage-tracked gseeds in the `adapter-eval://` namespace. Regression is detected automatically: any subsequent change to the adapter or its dependencies re-runs the grid and any axis dropping below threshold blocks the release.

### INV-390 — Reference-calibrated thresholds

Thresholds for SIS, CIS, SPS, EIS are derived from the 25th percentile of the reference cohort (Pixar-grade, Ghibli-grade, shonen anime). The thresholds are not hand-set; they are calibrated from the cohort each substrate version and published in the `adapter-eval://` gseed for that version. When the substrate version advances, the reference cohort is re-measured and thresholds move with it.

### INV-391 — Failure mode taxonomy with mandatory behavior declaration

Every adapter's acceptance gseed includes a declaration of its behavior on each of the six failure modes:

- `identity_collapse`: `pass` | `bounded_risk` | `fail`
- `signature_drop`: `pass` | `bounded_risk` | `fail`
- `proportion_drift`: `pass` | `bounded_risk` | `fail`
- `expression_flattening`: `pass` | `bounded_risk` | `fail`
- `chromatic_hijacking`: `pass` | `bounded_risk` | `fail`
- `pose_instability`: `pass` | `bounded_risk` | `fail`

`bounded_risk` means the adapter has a documented failure condition (e.g., "ukiyo-e adapter cannot preserve glowing-eye signature elements because the medium lacks value range"). `fail` on any mode blocks acceptance. `bounded_risk` is surfaced to users at compose time so the creator knows what to expect.

### INV-392 — Mutation test as mandatory second-stage gate

After an adapter passes the 4,800-render grid, it must pass a mutation test: 500 randomly sampled (character, pose, expression, lighting) cells are perturbed by documented epsilons and re-rendered. The output shift must be bounded and proportional to the input perturbation. Adapters that produce chaotic output for small perturbations are rejected with a `mutation-fail` rejection gseed.

### INV-393 — Style invariant contract as substrate-enforceable checker

The style invariants from Brief 088 (silhouette, palette weight, landmark proportion, signature elements) become substrate-level checkers runnable at compose time. When a user composes `char://` × `style-adapter://`, the invariants run before rendering; a violation either blocks rendering with a helpful error or degrades gracefully with a warning, per the adapter's declared `bounded_risk` behavior.

## Phase 1 deliverables

- **Grid infrastructure** (month 1) — the 10 × 12 × 8 × 5 grid is executable as a single batch job producing `adapter-eval://` gseeds.
- **Reference cohort calibration** (month 2) — Pixar-grade, Ghibli-grade, and shonen anime adapters hand-tuned to pass every axis; their 25th percentile becomes the pass floor.
- **Failure mode taxonomy implementation** (month 2) — the six failure-mode detectors run against every grid render.
- **Mutation test harness** (month 3) — 500-cell perturbation test runs as the second-stage gate.
- **First 20 adapters through the pipeline** (months 3–6) — pixel art 16-bit, cartoon Western 2D, watercolor, ink wash, cubism, voxel, low-poly, claymation-Aardman, hand-drawn line, photoreal, plus others, all signed `style-adapter://` with full `adapter-eval://` lineage.
- **Remaining 60 adapters** (months 6–12) — federated co-curator adapters per Brief 107's governance.

## Risks

- **Reference cohort drift.** The pass floor depends on reference adapter quality; if the reference adapters degrade, thresholds drop silently. Mitigation: reference cohort is itself re-measured on every substrate version and the delta is published.
- **Over-tuning to the grid.** An adapter can pass the 4,800 renders and fail in practice. Mitigation: mutation test (INV-392) catches overfitting; spot-check audits beyond the grid catch remainder.
- **Combinatorial explosion at 80 adapters.** 384,000 renders per substrate version is non-trivial compute. Mitigation: caching; incremental re-evaluation only for affected adapters and affected cells.
- **Subjective disagreement on what "bounded_risk" is acceptable.** Mitigation: bounded_risk is documented and visible to users; users decide, not the substrate.
- **Adapters good at Foundation Kernel characters but bad at out-of-distribution characters.** Mitigation: periodic extension of the character test set (10 canonical + sampled armory additions) as the armory grows.

## Recommendation

**Adopt the four-axis metric, the canonical grid, reference-calibrated thresholds, the failure mode taxonomy, the mutation test gate, and the style invariant compose-time checker.** Ship no adapter without a signed `adapter-eval://` gseed. Publish reference cohort calibrations with every substrate version release.

Accept that 20 adapters through the pipeline in 6 months is realistic; the remaining 60 depend on co-curator bandwidth under governance.

## Confidence

**4/5.** The metric architecture is sound and draws on settled research. Threshold calibration against a reference cohort is the right move and avoids invention. The main execution risk is compute throughput and reviewer bandwidth, both bounded by engineering effort, not design.

## Spec impact

Brief 088 gains six new inventions (INV-388..393). No constitutional commitments change. `adapter-eval://` joins the substrate grammar as a lineage scheme (not a new primitive; it is a lineage-only namespace like `curation-reject://`).

## Open follow-ups

- How out-of-distribution characters (user forks far from the Kernel) are handled — probably Brief 104.
- Whether the reference cohort should be 3 or 5 or more adapters.
- Threshold drift alerts: how much the pass floor can move between versions before governance review triggers.
- Adapter deprecation: what happens when an adapter stops meeting threshold on a new substrate version.

## Sources

- ArcFace face recognition metrics (Deng et al., literature).
- CLIP identity probe techniques (Radford et al., secondary literature).
- DreamBooth and IPAdapter evaluation methodologies (public papers and community benchmarks).
- ControlNet model card evaluation disciplines.
- Style transfer failure mode taxonomies from academic literature and community postmortems.
- Round 4 Brief 088 for style invariants and character canon.
- Round 4 Brief 091 for knowledge graph grounding.
