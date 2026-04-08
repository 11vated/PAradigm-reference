"""Evolver sub-agent.

Deterministic (non-LLM). Runs quality-diversity and evolutionary
strategy algorithms over the seed's parameter space:
  - MAP-Elites
  - CMA-ES
  - Novelty Search
  - DQD (Differentiable QD)
  - POET (Paired Open-Ended Trailblazer)

Every run uses the RNG seed derived from the intent envelope so
populations are byte-exact reproducible.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from agent.stages.stage_3_deterministic_growth import GrownSeed


@dataclass(frozen=True)
class EvolverResult:
    population: tuple[GrownSeed, ...]
    runs: tuple                          # tuple[EvolutionRun, ...]


@dataclass
class Evolver:
    """Deterministic evolutionary search driver."""

    default_population_size: int = 64
    default_generations: int = 32
    novelty_archive_size: int = 512

    def run(
        self,
        seed: GrownSeed,
        *,
        remedial: bool,
        prior_defects,
    ) -> EvolverResult:
        """Evolve a population from the given seed.

        If `remedial`, the fitness function penalizes whatever defects
        caused Stage 4 to fail. Otherwise the fitness function is
        quality-diversity over the seed's declared behavior descriptors.
        """
        raise NotImplementedError(
            "Evolver.run is implemented by the runtime binding; "
            "see intelligence/gspl-agent-full-capacity.md §evolver."
        )


__all__ = ["Evolver", "EvolverResult"]
