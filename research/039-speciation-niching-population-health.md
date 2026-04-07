# 039 — Speciation, niching, and population health

## Question
How does GSPL's evolution stack maintain a *healthy population* — diverse, novel, not collapsed to a single attractor — across evolutionary runs that may last hours or days?

## Why it matters
Without explicit population health management, evolution converges to a small attractor and stops being interesting. Speciation (treating different families as separate sub-populations), niching (rewarding diversity within a population), and health monitoring are the standard mechanisms. Without them, MAP-Elites + Novelty alone are not enough.

## What we know from the spec
- Brief 035 named MAP-Elites and Novelty as the diversity-preserving algorithms.
- Brief 036 covered AURORA's BC discovery.

## Findings — three mechanisms

### 1. Speciation

Speciation partitions a population into sub-populations ("species") that compete primarily within themselves. New offspring are assigned to the species closest to them in genotype space; if no species is close enough, a new species is born.

**GSPL adaptation:**
- Species distance metric is the FIM-weighted Mahalanobis (Brief 019) or, in cold start, naive L2 over Core projections (Brief 016).
- Species threshold is dynamic: the system adjusts it to keep species count in a target band (e.g., 5-15 species).
- Each species has its own elite (best member); the global archive merges across species.
- Speciation is *cross-domain-aware*: species can span engines via Core, but typically don't.

### 2. Niching

Niching is a complement to speciation: within a species, fitness is shared among similar individuals so that crowding is penalized. Borrowed from NSGA-II's crowding distance.

**GSPL adaptation:**
- Niche distance is the same FIM-weighted Mahalanobis.
- Crowding penalty: `effective_fitness = raw_fitness / (1 + α * neighbor_density)`.
- The penalty is applied at selection time, not stored in the seed itself.

### 3. Population health monitoring

Even with speciation and niching, populations can collapse. The kernel monitors health metrics and triggers interventions:

**Health metrics tracked per session:**
- **Diversity index**: entropy of species occupancy. Low = collapse.
- **Novelty rate**: fraction of new candidates added to the novelty archive in the last N generations. Low = stagnation.
- **Cell coverage** (in MAP-Elites mode): fraction of cells filled. Plateau = exhausted local search.
- **Mean fitness gain per generation**: trending toward zero = converged.
- **Genetic diversity**: mean pairwise distance in genotype space.

**Interventions when health degrades:**
1. **Mutation rate boost**: increase σ on stuck dimensions (FIM tells us which).
2. **Species fragmentation**: lower the species threshold to spawn more species.
3. **Random restart of worst species**: replace the lowest-fitness species with random seeds.
4. **Catastrophe injection**: introduce highly novel seeds from the global pre-seeded archive.
5. **BC re-projection**: when AURORA is in use, re-train the encoder on the current population to discover new dimensions.
6. **Switch algorithms**: e.g., from plain MAP-Elites to Novelty when diversity is low.

Interventions are triggered by simple thresholds; they're logged so the user can see what happened.

## Risks identified

- **Speciation thresholds are notoriously fragile**: too tight = one species; too loose = thousands. Mitigation: dynamic adjustment to target band.
- **Niching penalty deceives MAP-Elites**: MAP-Elites already does diversity via cells; niching on top can over-penalize. Mitigation: niching is off by default in MAP-Elites mode; on by default in plain GA mode.
- **Health monitoring overhead**: tracking 5+ metrics every generation is non-trivial. Mitigation: cheap metrics only; no extra renders.
- **Intervention thrashing**: alternating interventions every generation. Mitigation: cooldowns between interventions; trend windows for triggers.
- **User confusion**: "why did the system suddenly do something weird?" Mitigation: every intervention is logged with a human-readable reason in the session timeline.

## Recommendation

1. **Adopt the three-mechanism model** (speciation, niching, health monitoring) in `architecture/population-health.md`.
2. **Speciation is on by default in plain GA mode**, off by default in MAP-Elites mode (cells already partition).
3. **Niching is on by default in plain GA mode**, off in MAP-Elites mode.
4. **Five health metrics** tracked every generation: diversity, novelty, coverage, mean fitness gain, genetic diversity.
5. **Six interventions** available: mutation boost, species fragmentation, restart worst, catastrophe, BC re-projection, algorithm switch.
6. **Interventions are logged with reasons**; surfaced in the session timeline.
7. **Cooldowns between interventions** to prevent thrashing.
8. **Dynamic species threshold** with target band per engine.

## Confidence
**4/5.** Speciation, niching, and health monitoring are textbook techniques in evolutionary computation. The 4/5 reflects the unmeasured tuning cost across 19 engines.

## Spec impact

- `architecture/population-health.md` — full health management spec.
- `algorithms/speciation.md` — speciation pseudocode and threshold dynamics.
- `algorithms/niching.md` — crowding-distance penalty.
- `algorithms/health-interventions.md` — six interventions with triggers.
- New ADR: `adr/00NN-population-health-monitoring.md`.

## Open follow-ups

- Calibrate species count target bands per engine.
- Decide on the cooldown durations between interventions.
- Build the session timeline UI that shows interventions (Brief 048).
- Empirically validate the diversity entropy metric on real runs.

## Sources

- Stanley & Miikkulainen, *NEAT* (speciation by genotypic compatibility).
- Deb et al., *NSGA-II* (crowding distance).
- Mouret & Doncieux, *Encouraging Behavioral Diversity in Evolutionary Robotics*.
- Internal: Briefs 016, 019, 035, 036, 048.
