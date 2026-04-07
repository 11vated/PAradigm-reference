# 041 — INV: GSPL-native evolution operators

## Question
What net-new evolutionary operators does GSPL enable that the standard evolutionary computation literature does not cover, by virtue of GSPL's typed gene system, content-addressed lineage, Fisher information, and cross-engine composition?

## Why it matters
Standard EC operators (uniform crossover, Gaussian mutation, tournament selection) treat genomes as flat vectors. GSPL's seed space has *structure*: typed genes with semantic operators (Brief 013), content-addressed lineage with operator history (Brief 017), per-gene Fisher curvature (Brief 019), category-theoretic composition across engines (Brief 016), and a critic suite with preference signals (Brief 040). Each of these enables operators with no obvious analog in the EC literature. Inventing them is a moat: competitors using flat-vector EC cannot replicate what GSPL does without first replicating its entire substrate.

## What we know from the spec
- Briefs 013, 016, 017, 019, 028, 035, 040 are the substrate.
- Brief 035 named GA, MAP-Elites, CMA-ES, Novelty, AURORA, DQD, POET as the seven existing layers.

## Findings — ten new operators

### 1. Lineage-Aware Crossover
**What it does:** When crossing parents A and B, consult their shared lineage ancestor C. Genes that A and B *both inherited unchanged from C* are preserved unchanged in the child. Genes where A and B diverged from C are recombined normally. This makes crossover lineage-respecting: it can't accidentally undo a mutation that both parents have agreed on for generations.
**Substrate required:** Brief 017 lineage DAG.
**Behavior:** Acts as a soft genetic conservatism — successful long-stable traits are stickier than recent ones.

### 2. FIM-Weighted Mutation
**What it does:** Per-gene mutation magnitude is `σ_i ∝ 1/√I_ii`. Stiff (high-curvature) genes get tiny perturbations; sloppy (low-curvature) genes get large ones. This is the formalization of the rule "don't waste mutations on the parameters that don't matter."
**Substrate required:** Brief 019 FIM.
**Behavior:** Massively reduces wasted evaluations on inert dimensions. Standard CMA-ES does something similar via covariance adaptation but requires 10^4 evaluations to learn what FIM gives in closed form.

### 3. Sloppy-Direction Crossover
**What it does:** Decompose the FIM into eigenvectors. Crossover happens *along sloppy eigendirections only* — the directions where the fitness landscape is flat. Stiff directions are inherited from the higher-fitness parent unchanged.
**Substrate required:** Brief 019 FIM eigendecomposition.
**Behavior:** Generates valid offspring more reliably because it doesn't disturb the dimensions that matter.

### 4. Operator-History-Aware Selection
**What it does:** Selection probability includes a small bonus for candidates whose lineage contains *rarely-used operators*. Encourages exploration of operator-space, not just gene-space.
**Substrate required:** Brief 017 lineage edges with operator IDs.
**Behavior:** Prevents the population from being dominated by candidates produced by the same two operators.

### 5. Naturality-Square Composition
**What it does:** When two seeds from different engines compose (e.g., a sprite + a music track), the composition operator uses the category-theoretic Core projection (Brief 016) to share structure. Crossover between cross-engine pairs operates on the *Core projection*, then re-lifts back into both engines.
**Substrate required:** Brief 016 Core schema and engine functors.
**Behavior:** Enables coherent cross-engine breeding (e.g., the music's tempo and the sprite's animation speed evolve together) instead of independent drift.

### 6. Critic-Gradient Reflection Mutation
**What it does:** When a critic gives a low score, compute the gradient of the critic with respect to the gene values (where differentiable, Brief 037 DQD). Reflect the candidate across the gradient: take the opposite direction. This is one mutation step that *guaranteed* moves toward higher critic score, even when far from convergence.
**Substrate required:** Differentiable critic from Brief 040.
**Behavior:** A single high-information mutation, useful when compute is expensive.

### 7. Preference-Pairwise Crossover
**What it does:** Given a user preference "A > B" from Brief 040, the operator produces a child that takes from A in the *direction A differs from B* and from B everywhere else. Concretely: child = B + α * (A - B) projected onto the preference axis.
**Substrate required:** Brief 040 preference critic.
**Behavior:** Each preference signal directly steers offspring, not just trains a model.

### 8. Lineage-Constrained Mutation
**What it does:** Mutation is forbidden from re-entering a region the lineage has already explored and rejected. Maintains a lineage-local "anti-archive" of previously rejected nearby genotypes; mutation rejects samples too close to anti-archive entries.
**Substrate required:** Brief 017 lineage + per-lineage anti-archive.
**Behavior:** Prevents the dreaded "evolution rediscovers the same bad solution every 50 generations."

### 9. Cross-Engine Symmetry-Breaking Operator
**What it does:** When two engines have a near-symmetric composition (e.g., a level and its mirror), explicitly break the symmetry along a chosen axis to spawn a non-symmetric variant. Symmetry detection uses Core-projection automorphism check.
**Substrate required:** Brief 016 Core, Brief 028 composition patterns.
**Behavior:** Creates *qualitatively new* variants instead of small perturbations.

### 10. Multi-Generation Replay Mutation
**What it does:** Re-applies the mutation chain from a *different* high-fitness lineage to the current candidate. Concretely: take the operator history of seed S' from generation N-k to N, and apply that exact operator sequence to candidate S. This is "imitative evolution" — borrowing successful evolutionary trajectories.
**Substrate required:** Brief 017 operator history with deterministic operator replay.
**Behavior:** Massively accelerates convergence when one branch of the population has discovered something useful.

## How they compose into the existing stack

These operators slot into Layer 1 (GA) of the Brief 035 stack. They are not replacements; they augment standard operators. The default v1 mutation/crossover registry includes all ten plus the standard Gaussian/uniform/single-point baselines.

The operator selection within a generation is itself a bandit problem: the per-user planner policy (Brief 034) tracks which operators produce accepted offspring and shifts probability mass accordingly.

## Risks identified

- **Operator complexity tax**: ten operators × 19 engines × validation = a lot of test surface. Mitigation: operators are *engine-agnostic at the gene-type level*; they need no per-engine code.
- **Determinism preservation**: each new operator must be deterministic given (parents, rng_seed). Mitigation: operator implementations are pure; rng_seed via HKDF (Brief 017).
- **Critic-gradient operator deceives**: chasing the gradient finds critic-game inputs. Mitigation: critic ensemble (Brief 040) + ensemble disagreement penalty.
- **Lineage-constrained mutation can starve**: if the lineage is dense, no valid moves remain. Mitigation: anti-archive bounded; oldest-first eviction; threshold relaxed when starvation detected.
- **Naturality-square composition correctness**: requires the Core functors to actually be functorial (not just vibes). Mitigation: per-engine functor tests (Brief 016 already mandates these).
- **Operator IDs are public**: attackers can reverse-engineer evolution by knowing which operators were used. Mitigation: operator IDs in lineage are stable but rng_seeds are HKDF-derived from private keys (Brief 017), so the *trajectory* is not reproducible without the private key.

## Recommendation

1. **Adopt all ten operators** in `algorithms/evolution/gspl-native-operators.md` as v1 normative additions to Layer 1.
2. **Operator IDs reserved** in the operator registry: 100-109 for the new ten.
3. **All ten operators are deterministic** given (parents, rng_seed).
4. **Operator selection is bandit-driven** at the planner level (Brief 034).
5. **FIM-weighted mutation is the v1 default mutation** for all engines where FIM is available (cached or estimated).
6. **Lineage-aware crossover is the v1 default crossover** for all engines.
7. **Critic-gradient reflection is opt-in at v1**, default for engines with differentiable critics.
8. **Naturality-square composition is the v1 default** for cross-engine breeding.
9. **Preference-pairwise crossover is v1.5** (requires sufficient preference signal).
10. **Lineage-constrained mutation is v1**, with cooldown when anti-archive saturates.
11. **Per-operator unit tests** validate determinism and contract conformance.
12. **Operators are immutable post-release** (Brief 018 immutable operator policy).

## Confidence
**3/5.** Each operator is individually plausible and grounded in GSPL substrate. The 3/5 reflects the unproven combination at scale and the unmeasured per-operator value contribution. Some of the ten will turn out to be marginal; the bandit selector should reveal which.

## Spec impact

- `algorithms/evolution/gspl-native-operators.md` — full pseudocode for all ten.
- `algorithms/evolution/operator-bandit.md` — bandit-driven selection.
- `architecture/operator-registry.md` — reserved IDs 100-109.
- `tests/operator-determinism.md` — per-operator determinism tests.
- New ADR: `adr/00NN-gspl-native-evolution-operators.md`.

## Open follow-ups

- Empirically validate each operator against a baseline GA on three engines (Phase 2).
- Decide on the bandit algorithm (UCB1 vs Thompson sampling).
- Build the visualizer for operator history in lineage trees (Brief 048).
- Investigate whether multi-generation replay mutation can be generalized to cross-user replay (with explicit consent).
- Decide on the anti-archive bound and eviction policy per engine.

## Sources

- Standard EC: Eiben & Smith, *Introduction to Evolutionary Computing*.
- Lineage-aware operators: novel, no direct prior art in EC literature for content-addressed lineage.
- FIM-weighted mutation: Amari, *Natural Gradient Works Efficiently in Learning* (the underlying math).
- Sloppy/stiff: Transtrum et al., *Perspective: Sloppiness and Emergent Theories*.
- Internal: Briefs 013, 016, 017, 019, 028, 034, 035, 037, 040.
