# 035 — Evolution stack synthesis: GA + ME + CMA-ES + Novelty + AURORA + DQD + POET

## Question
Which evolutionary algorithms does the GSPL evolution stack include, how do they compose, and what does each contribute that the others can't?

## Why it matters
Evolution is GSPL's core production mechanism. A single algorithm (e.g., plain GA) is too brittle for the diversity of engines GSPL ships. A pile of algorithms with no integration story is just a library. The synthesis brief defines the layered stack and the composition story.

## What we know from the spec
- Brief 012 (round 1) covered MAP-Elites convergence in detail.
- The 17 + 5 gene types support the operators each algorithm needs.

## Findings — the seven-algorithm layered stack

### Layer 0: Genetic Algorithm (GA) — substrate

The base mechanism. Population, selection, crossover, mutation, generations. Every other algorithm in the stack uses GA primitives. Per-gene-type operators come from Brief 013.

**Use:** Default for engines whose fitness function is well-defined and convex-ish.

### Layer 1: MAP-Elites (ME) — quality + diversity

A grid over a behavior-characterization (BC) space, each cell holding the best seed found with that behavior. Solves the diversity problem GA has. Detailed in Brief 012.

**Use:** Default for creative engines where novelty matters more than convergence (most engines).

### Layer 2: CMA-ES — local refinement

Covariance Matrix Adaptation Evolution Strategy. Excellent at finding the local optimum within a single MAP-Elites cell. Slow but precise.

**Use:** As a *cell-refiner* on top of MAP-Elites — once a cell has a candidate, CMA-ES polishes it.

### Layer 3: Novelty Search — exploration without fitness

Optimizes for being different from previously-found solutions, not for fitness. Useful when fitness is unknown or deceptive.

**Use:** Bootstrapping when there's no critic yet; complement to MAP-Elites for hard-to-characterize engines.

### Layer 4: AURORA — learned behavior characterization

Auto-encoder-based discovery of the behavior-characterization space from raw outputs. Removes the need for hand-engineered BC dimensions.

**Use:** When MAP-Elites' BC dimensions aren't obvious. Cross-reference Brief 036.

### Layer 5: DQD — differentiable quality-diversity

When the fitness function and BC are differentiable, gradient information dramatically accelerates QD search. Brief 037 covers this in detail.

**Use:** Engines with differentiable critics (most learned-critic engines).

### Layer 6: POET — open-ended co-evolution

A pair of populations co-evolves: solutions and environments. Open-ended, generates novelty indefinitely. Brief 038 details.

**Use:** ALife, Ecosystem, FullGame at long-running evolution scales.

## How they compose

The stack is **not** a strict hierarchy where layer N replaces layer N-1. It's a *menu* — every engine picks the layers it needs, and the kernel runs them as a pipeline:

```
                          [GA primitives]
                                │
                                ▼
                        ┌─────────────────┐
                        │   MAP-Elites    │ ← BC from AURORA when applicable
                        └────────┬────────┘
                                 │
                ┌────────────────┼────────────────┐
                ▼                ▼                ▼
          [CMA-ES per cell]  [Novelty]       [DQD when diff'able]
                │                │                │
                └────────────────┼────────────────┘
                                 ▼
                        [POET when engine
                         supports environments]
```

**Default presets per engine type** (from Briefs 021-026):

| Engine family | Default stack | Notes |
|---|---|---|
| Humanoid (Char/Sprite/Anim) | GA + ME (3 BCs) + CMA-ES | Critics are mostly perceptual |
| Sound (Music/Audio) | GA + ME + AURORA | Hard to hand-engineer BCs for music |
| Interactive (Narr/Game/Full) | GA + ME + Novelty | Critics include playability metrics |
| Visual (V2D/Proc/Geo3D) | GA + ME + DQD | Differentiable when learned critic is in the loop |
| Simulation (Phys/Eco/ALife) | GA + ME + POET | Open-ended is the point |
| UI | GA + ME | Constraint-heavy, simple is fine |

## Shared infrastructure

All layers share:

- **The same gene-typed operator suite** (Brief 013).
- **The same critic framework** (Brief 040).
- **The same archive backend** (the user's exemplar archive, Brief 031).
- **The same lineage recording** (Brief 017).
- **The same FIM-aware mutation step sizing** (Brief 019).

This shared infrastructure is what makes "an engine picks the layers it needs" tractable.

## Compute budgeting

Evolution is expensive. Per-engine compute budgets:

| Engine type | Default eval budget per generation | Generations per session |
|---|---|---|
| Humanoid | 256 | 50 |
| Sound | 128 | 30 |
| Interactive (single-mechanic Game) | 128 | 50 |
| Interactive (FullGame) | 32 | 20 |
| Visual | 256 | 50 |
| Simulation | 64 | 100 |
| UI | 64 | 20 |

These are GPU-eval-equivalent counts. The kernel batches evals to amortize GPU launch cost.

## Risks identified

- **Stack complexity**: seven algorithms is a lot to maintain. Mitigation: shared infrastructure and per-engine presets reduce the surface area to "pick a preset, occasionally tune."
- **POET runaway costs**: open-ended evolution can run forever. Mitigation: explicit step budget per session; checkpointing.
- **AURORA encoder drift**: a learned BC encoder changes between versions. Mitigation: pin the encoder version per cell index; AURORA encoder bumps require a fresh archive (or migration).
- **DQD non-trivially harder to implement** than the others. Mitigation: deferred to engines that explicitly need it; not v1 default.
- **Algorithm selection paralysis** for new users. Mitigation: presets are mandatory unless the user opts in to manual tuning.

## Recommendation

1. **Adopt the seven-layer evolution stack** with presets per engine family.
2. **Shared infrastructure** is normative: gene operators, critics, archive, lineage, FIM all single-sourced.
3. **Per-engine presets** are normative; users override only with explicit opt-in.
4. **Compute budgets** above are v1 defaults, calibrated empirically in Phase 2.
5. **DQD is opt-in at v1**, default at v2 for engines with learned critics.
6. **POET is opt-in at v1**, available only for simulation engines.
7. **Algorithm contributions documented per layer** in `architecture/evolution-stack.md`.

## Confidence
**4/5.** Each algorithm in the stack is well-understood individually. The 4/5 reflects the unproven combination at GSPL's scale and budgets.

## Spec impact

- `architecture/evolution-stack.md` — full stack architecture.
- `algorithms/evolution/ga.md`, `map-elites.md`, `cma-es.md`, `novelty.md`, `aurora.md`, `dqd.md`, `poet.md` — seven files.
- `architecture/evolution-presets.md` — per-engine preset table.
- `tests/evolution-conformance.md` — preset reproducibility tests.
- New ADR: `adr/00NN-evolution-stack-v1.md`.

## Open follow-ups

- Build the shared infrastructure layer first. Phase 1.
- Empirically calibrate compute budgets per engine.
- Decide on the AURORA encoder architecture and training data.
- Build the DQD prototype against the SpriteEngine in Phase 2.

## Sources

- Mouret & Clune, *Illuminating Search Spaces by Mapping Elites*.
- Hansen, *The CMA Evolution Strategy: A Tutorial*.
- Lehman & Stanley, *Abandoning Objectives: Evolution Through the Search for Novelty Alone*.
- Cully, *Autonomous Skill Discovery with Quality-Diversity and Unsupervised Descriptors* (AURORA).
- Fontaine & Nikolaidis, *Differentiable Quality Diversity*.
- Wang et al., *Paired Open-Ended Trailblazer (POET)*.
- Internal: Briefs 012, 013, 017, 019, 031, 040.
