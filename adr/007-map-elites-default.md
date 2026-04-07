# ADR-007: Make MAP-Elites the Default Evolution Algorithm

**Status:** Accepted
**Date:** 2024-10-08
**Layer:** Layer 4 (Evolution)

## Context

The Paradigm studio gives users a button: "Evolve." We have to choose what algorithm runs when they click it. There are seven evolution algorithms in the platform (GA, MAP-Elites, CMA-ES, Novelty Search, AURORA, DQD, POET), each suited to different problem shapes. The default matters because most users will never change it.

The evolution must:

1. Produce a *gallery* of varied results, not a single optimum (creative work needs options).
2. Show progress visually within seconds — not minutes.
3. Work for any domain without per-domain tuning.
4. Handle mixed gene types (continuous, categorical, structural).
5. Be deterministic and parallelizable.

## Decision

The default evolution algorithm is **MAP-Elites** with default behavior descriptors per domain (defined in each engine's `defaultDescriptors`). Users can switch to any of the other 6 algorithms via a "Method" dropdown, but MAP-Elites is selected when the studio loads.

The studio surfaces the MAP-Elites archive as a 2D grid (or N-dim heatmap for higher D), with each cell showing the best seed found in that behavioral cell. Users click cells to inspect and breed.

See [`algorithms/map-elites.md`](../algorithms/map-elites.md).

## Consequences

**Positive:**

- The default UX is "watch a grid fill in over time," which is dramatically more engaging than "watch a fitness number tick up."
- Users discover variations they never asked for, which is the entire creative point.
- MAP-Elites handles any gene type via the mutation operator; no per-domain optimizer tuning.
- Determinism is straightforward (sorted iteration, hash tie-break).
- Trivially parallelizable: each generation evaluates 32 children in parallel.

**Negative:**

- MAP-Elites is *not* the fastest for single-objective optimization. Users wanting "the best one" with high fidelity should switch to CMA-ES or DQD.
- The behavior descriptors are hand-designed per domain. If they're wrong, the archive doesn't reflect interesting variation. We mitigate this by offering AURORA as the "auto-discover" option.
- Storage: archives can grow to 10K-100K seeds. We bound by `bin_count` (typically 100-400) to keep memory under 100 MB.

## Alternatives Considered

- **Genetic Algorithm (single-population):** Faster for pure optimization but produces only one champion. Rejected because creative work demands diversity.
- **CMA-ES:** Excellent for continuous optimization but doesn't handle structural genes. Made available but not default.
- **Novelty Search:** Excellent exploration but no sense of "good" — doesn't reward fitness at all. Made available but too unguided as a default.
- **AURORA:** Auto-discovers descriptors. Almost the right default. Rejected because the upfront autoencoder training delays the first visible result by 30+ seconds; bad first-run UX.
- **Random sampling:** No evolution at all. Rejected because there's no learning over time.

## References

- Mouret & Clune, *Illuminating Search Spaces by Mapping Elites* (2015)
- Cully & Demiris, *Quality and Diversity Optimization: A Unifying Modular Framework* (IEEE TEVC 2018)
