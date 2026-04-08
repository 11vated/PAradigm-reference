"""evolution_run tool.

Thin facade over the Evolver sub-agent's algorithm library. Lets the
agent runtime trigger MAP-Elites / CMA-ES / Novelty / DQD / POET runs
from manifest configuration without hard-coding an algorithm choice
into Stage 5.

Lineage gene: graph (evolutionary runs emit graph-gene edges over the
population's behavior descriptors).

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Algorithm = Literal["MAP_Elites", "CMA_ES", "Novelty_Search", "DQD", "POET"]


@dataclass(frozen=True)
class EvolutionConfig:
    algorithm: Algorithm
    generations: int
    population_size: int
    rng_seed_hex: str
    behavior_descriptors: tuple[str, ...]


@dataclass
class EvolutionRunTool:
    default_generations: int = 32
    default_population: int = 64

    def run(self, config: EvolutionConfig, seed_payload: dict):
        raise NotImplementedError(
            "EvolutionRunTool.run is implemented by the Evolver sub-agent "
            "binding; see agent/sub_agents/evolver.py."
        )


__all__ = ["EvolutionRunTool", "EvolutionConfig", "Algorithm"]
