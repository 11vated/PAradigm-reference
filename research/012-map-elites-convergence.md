# 012 — MAP-Elites convergence in Paradigm's compute budgets

## Question
Can the Paradigm exemplar evolution loop, which uses MAP-Elites + CMA-ES + UCB1, converge to a useful archive of diverse exemplars within the compute budget realistically available to a solo founder (single workstation, occasional cloud bursts), and what configuration is required?

## Why it matters (blast radius)
The exemplar archive is the system's accumulated long-term memory of "interesting things the kernel can produce." It is what makes Paradigm get better over time without constant manual curation. If MAP-Elites cannot fill a useful archive at the available compute budget, the spec's "self-improving exemplar pool" promise fails — and with it, the value proposition that distinguishes Paradigm from a pure prompt-and-render system. This brief gates `evolution/map-elites.md` and `evolution/budgets.md`.

## What we know from the spec
- `evolution/map-elites.md` sketches an N-dimensional behavior grid with elites in each cell.
- `evolution/cma-es.md` calls for CMA-ES as the within-cell variation operator.
- `evolution/ucb1.md` calls for UCB1 as the cell-selection bandit.
- The spec does not yet quantify grid size, evaluation budget, or convergence criteria.

## Findings

1. **MAP-Elites is a quality-diversity (QD) algorithm that maintains a discretized archive of elites — one elite per cell of a behavior grid — and improves them over generations via mutation/selection.** [1, 2, 3] Unlike a pure optimizer, MAP-Elites "illuminates" the behavior space, returning a *population* of high-performing solutions across distinct behavior niches rather than a single optimum.

2. **Grid size grows exponentially with the number of behavior dimensions.** [4, 5] A 2D grid with 50 bins per dim is 2,500 cells; 3D with 50 bins is 125,000; 4D is 6.25M. The standard guidance is "start coarse (10-20 bins per dim) and refine, or use hierarchical / adaptive grids." For a solo founder, **3 behavior dimensions with 16-32 bins per dim (4K-32K cells) is the practical envelope.**

3. **Evaluation budget is the dominant cost.** Each generation evaluates a batch of candidates, each candidate requires a kernel run + a fitness computation. Published MAP-Elites runs in robotics, game-content generation, and neural-network search typically use 10^5 to 10^7 evaluations to fill an archive. [2, 3, 6] Paradigm's per-evaluation cost is a kernel render at low fidelity — measured in tens to hundreds of milliseconds on a workstation GPU — so a 10^5-evaluation campaign is on the order of 1-10 hours on a single GPU; 10^7 is weeks and requires cloud bursts.

4. **Multi-emitter MAP-Elites variants (ME-MAP-Elites)** [3, 5] manage a pool of mutation/variation operators with a bandit allocation scheme (UCB-style), boosting both coverage and convergence speed. This is exactly the architecture the Paradigm spec already calls for (UCB1 over multiple operators). The published convergence improvements are 2×-5× over vanilla MAP-Elites on comparable benchmarks.

5. **CMA-ES as the within-cell variation operator** [3] gives a strong local-search component inside each cell, which is helpful when the kernel parameter space is high-dimensional and continuous. The catch: CMA-ES itself maintains state per emitter (mean, covariance) which adds memory overhead per active cell.

6. **Sample-efficient QD methods** (model-based MAP-Elites, surrogate-assisted MAP-Elites) [6, 7] reduce the evaluation budget by 1-2 orders of magnitude by training a cheap surrogate model to pre-screen candidates before paying the full kernel-evaluation cost. **This is the largest available lever for a solo-founder compute budget** and the brief recommends adopting it.

7. **Convergence criteria** in the QD literature are typically "QD-score" (sum of fitness across all filled cells) plateauing, or "coverage" (fraction of cells filled) reaching a target. There is no universal answer; the criterion is set per-application.

## Risks identified

- **Choosing too many behavior dimensions** explodes the grid and makes any compute budget insufficient. The spec must constrain the v1 behavior space.
- **Choosing behavior descriptors that don't actually correspond to interesting variation** wastes the entire budget filling cells nobody cares about. Behavior descriptor design is a load-bearing decision.
- **CMA-ES memory overhead** scales with the number of active cells × parameter-dimension². For a 32K-cell grid with a 100-parameter kernel, the CMA-ES state alone is on the order of 320M floats — fits in workstation RAM but is not free.
- **Without a surrogate**, the evaluation budget is the bottleneck. With a surrogate, the surrogate quality is the bottleneck — and a bad surrogate biases the archive toward whatever the surrogate over-predicts.
- **A solo founder cannot let evolution runs eat the workstation 24/7.** Runs must be checkpointable, resumable, and pausable.
- **No human can curate a 32K-cell archive by hand**, so the archive must be self-curating (the elite selection rule is the only quality gate).

## Recommendation

**Adopt a "small grid, surrogate-assisted, checkpointable" v1 evolution loop:**

### Architecture

1. **Behavior dimensions: 3 at v1.** Recommended: (visual complexity, color diversity, semantic class) — exact descriptors to be decided in `evolution/behavior-descriptors.md`. The brief flags descriptor design as load-bearing and reserves a follow-up.
2. **Grid resolution: 16 bins per dimension at v1 (4,096 cells total).** Coarse enough to fill in days-to-weeks of compute on a single GPU; fine enough to be interesting.
3. **Surrogate-assisted pre-screening: required.** Train a small surrogate model (gradient-boosted trees or a small MLP) on (parameter vector → fitness) pairs from the archive itself. New candidates are first scored by the surrogate; only the top fraction are evaluated by the actual kernel. Target a 10× evaluation reduction.
4. **Multi-emitter UCB1** (already in spec) over a small set of variation operators: (a) CMA-ES local search, (b) random mutation, (c) crossover within behavior neighborhood, (d) novelty-seeking mutation. UCB1 allocates draws across emitters by reward.
5. **CMA-ES state is managed per *active* cell, not per cell of the grid.** A cell becomes active when it has been targeted by the bandit at least N times. Inactive cells use cheap random mutation only.

### Budgets

6. **v1 evaluation budget target: 50,000 kernel evaluations (post-surrogate filtering)** for the initial archive seeding run. At ~100ms per evaluation on a workstation GPU, this is ~1.5 hours of pure compute. Realistic wall-clock with overhead: 3-6 hours.
7. **Continuous evolution after seeding**: 1,000-5,000 evaluations per day on idle compute, runnable as a background process.
8. **Cloud burst budget**: an optional 10× burst (500K evaluations) for major exemplar pool refreshes, budgeted explicitly per release.

### Convergence and operational rules

9. **Convergence criterion: coverage of the grid above 70% AND QD-score plateau (slope < ε over the last K generations).** Specific thresholds to be calibrated empirically in Phase 1.
10. **Checkpointing: every N evaluations** (default N=1000) the entire archive plus emitter state is serialized to disk. Runs are resumable from any checkpoint.
11. **Pausable / preemptible**: a SIGTERM or user pause command triggers a checkpoint and clean shutdown.
12. **Fully deterministic given a seed and a checkpoint** — same seed, same kernel version, same checkpoint → same next-step archive. Required so that evolution runs themselves can be reproduced.
13. **The archive is content-addressed** by the hash of the kernel version + behavior descriptors + checkpoint index, so two instances of the engine can agree on whether they have the same archive.

### Quality gates

14. **Each elite is signed and has a content hash** (per the proof system). Archive corruption is detectable.
15. **An elite cannot be silently overwritten** unless the new candidate strictly dominates by a margin (not just ties or beats by epsilon). Prevents drift from numerical noise.
16. **Behavior descriptors are versioned**; changing the descriptor function invalidates the archive and forces a re-seed (because the cells no longer mean the same thing).

## Confidence
**3/5.** MAP-Elites is well-understood and the recommended architecture is consistent with published literature. The 3/5 (rather than 4/5) reflects two real uncertainties: (a) we have not yet measured the actual per-evaluation cost on representative GSPL kernels — the 100ms estimate is a guess pending Phase 1 measurement, and (b) the surrogate-assisted reduction depends on the surrogate actually being predictive on Paradigm's kernel parameter space, which is unverified. Phase 1 must run a small (1000-eval) pilot before committing to the full v1 budget.

## Spec impact

- **`evolution/map-elites.md`** — fold in the 3-dim, 16-bin, 4096-cell v1 grid and the surrogate-assisted architecture.
- **`evolution/cma-es.md`** — clarify that CMA-ES state is per-active-cell, not per grid cell.
- **`evolution/ucb1.md`** — fix the operator pool and the bandit configuration.
- **New file: `evolution/behavior-descriptors.md`** — describe the 3 v1 descriptors and the versioning rule.
- **New file: `evolution/surrogate.md`** — describe the surrogate model, training data, and re-training cadence.
- **New file: `evolution/budgets.md`** — codify the 50K seeding / 1K-5K daily / 500K burst budgets.
- **New file: `evolution/checkpoint-format.md`** — checkpoint serialization format.
- **`proof/content-hash.md`** — extend to cover archive content addressing.
- New ADR: **`adr/00NN-evolution-budgets-v1.md`** — record the budgets and the rationale.
- New ADR: **`adr/00NN-surrogate-assisted-map-elites.md`** — record the decision and the surrogate choice.

## Open follow-ups

- Pick the 3 behavior descriptors. This is a separate design task and is load-bearing for the entire archive's usefulness.
- Run a 1,000-evaluation pilot on a representative kernel to validate the per-evaluation cost estimate. Phase 1 task.
- Pick the surrogate model class (gradient-boosted trees vs small MLP vs Gaussian process) — depends on the parameter-space dimensionality and the training-data volume.
- Decide on archive sharing across users (federated archives) — out of scope for v1, flagged as v2.
- Decide on the elite-overwrite margin (the "strictly dominates by margin ε" rule needs a concrete ε).

## Sources

1. MAP-Elites: Quality-Diversity Search (Emergent Mind summary). https://www.emergentmind.com/topics/map-elites-algorithm
2. Map Elites (Algorithm Afternoon). https://algorithmafternoon.com/novelty/map_elites/
3. Quality-Diversity papers list. https://quality-diversity.github.io/papers.html
4. Quality-Diversity Algorithms applied to Robot Navigation. https://towardsdatascience.com/quality-diversity-algorithms-a-new-approach-based-on-map-elites-applied-to-robot-navigation-f51380deec5d/
5. MAP-Elites Enables Powerful Stepping Stones and Diversity for Modular Robotics. https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2021.639173/full
6. Sample Efficient Quality Diversity for Neural Network Search. https://openreview.net/pdf?id=8FRw857AYba
7. Quality with Just Enough Diversity in Evolutionary Policy Search. https://arxiv.org/html/2405.04308
8. Evolving Populations of Diverse RL Agents with MAP-Elites. https://arxiv.org/html/2303.12803
