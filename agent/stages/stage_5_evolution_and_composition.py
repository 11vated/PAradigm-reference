"""Stage 5 — Evolution and composition (optional).

Invoked when:
  (a) Stage 4 validation failed three attempts in a row and escalated
      the seed to the Evolver sub-agent for remedial search, OR
  (b) The intent envelope explicitly requests evolutionary refinement
      (e.g. "evolve 50 variants of this bard and pick the novel one"),
      OR
  (c) The Composer sub-agent was asked to suggest a multi-seed bundle
      (e.g. "produce a bard, a tavern, and a lute that all share
      lineage parents").

The Evolver runs fully deterministic quality-diversity / evolutionary
strategy algorithms (MAP-Elites, CMA-ES, Novelty Search, DQD, POET)
against the seed's parameter space using the RNG seed from Stage 3.
The Composer is LLM-bearing but `may_suggest_only`: it proposes bundle
structures, it never emits raw kernel bytes.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from agent.stages._shared import StageReceipt, StageStatus
from agent.stages.stage_3_deterministic_growth import GrownSeed
from agent.stages.stage_4_validation import ValidationReport
from agent.sub_agents.composer import Composer
from agent.sub_agents.evolver import Evolver


EvolutionAlgorithm = Literal[
    "MAP_Elites",
    "CMA_ES",
    "Novelty_Search",
    "DQD",
    "POET",
]


@dataclass(frozen=True)
class EvolutionRun:
    algorithm: EvolutionAlgorithm
    generations: int
    population_size: int
    best_fitness: float
    novelty_score: float
    elites_archived: int


@dataclass(frozen=True)
class CompositionBundle:
    """A Composer-suggested multi-seed bundle."""

    bundle_id: str
    member_intent_ids: tuple[str, ...]
    shared_lineage_parents: tuple[str, ...]
    rationale: str


@dataclass
class Stage5Output:
    evolved_seeds: tuple[GrownSeed, ...] = ()
    evolution_runs: tuple[EvolutionRun, ...] = ()
    composition_bundles: tuple[CompositionBundle, ...] = ()
    receipt: StageReceipt | None = None


def run(
    seed: GrownSeed,
    prior_report: ValidationReport | None,
    evolver: Evolver,
    composer: Composer,
    mode: Literal["skip", "remedial", "requested_variants", "composition"],
) -> Stage5Output:
    """Execute Stage 5.

    `mode` selects behaviour:
      - "skip"               — pipeline is happy; return empty output.
      - "remedial"           — Stage 4 failed; ask Evolver to heal.
      - "requested_variants" — user asked for a generated population.
      - "composition"        — Composer proposes a multi-seed bundle.
    """
    if mode == "skip":
        return Stage5Output(
            receipt=StageReceipt(
                stage_id="stage_5_evolution_and_composition",
                status=StageStatus.SKIPPED_NOT_NEEDED,
                note="no evolution or composition requested",
            ),
        )

    evolved: tuple[GrownSeed, ...] = ()
    runs: tuple[EvolutionRun, ...] = ()
    bundles: tuple[CompositionBundle, ...] = ()

    if mode in ("remedial", "requested_variants"):
        result = evolver.run(
            seed=seed,
            remedial=(mode == "remedial"),
            prior_defects=prior_report.defects if prior_report else (),
        )
        evolved = tuple(result.population)
        runs = tuple(result.runs)

    if mode == "composition":
        bundles = tuple(composer.suggest_bundle(seed))

    return Stage5Output(
        evolved_seeds=evolved,
        evolution_runs=runs,
        composition_bundles=bundles,
        receipt=StageReceipt(
            stage_id="stage_5_evolution_and_composition",
            status=StageStatus.OK,
            note=(
                f"mode={mode} "
                f"evolved={len(evolved)} "
                f"runs={len(runs)} "
                f"bundles={len(bundles)}"
            ),
        ),
    )


__all__ = [
    "EvolutionAlgorithm",
    "EvolutionRun",
    "CompositionBundle",
    "Stage5Output",
    "run",
]
