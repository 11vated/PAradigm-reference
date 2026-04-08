"""Composer sub-agent.

LLM-bearing but `may_suggest_only`: proposes multi-seed bundle
structures (e.g. "a bard, a tavern, and a lute that all share lineage
parents") but never emits raw kernel bytes. Actual seed materialization
is always delegated back to the CodeSmith-> kernel-> Validator pipeline.

Tools allowed: seed_inventory_query.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass

from agent.stages.stage_3_deterministic_growth import GrownSeed


@dataclass
class Composer:
    """Suggests bundles; never emits bytes."""

    backend_id: str
    may_suggest_only: bool = True

    def suggest_bundle(self, seed: GrownSeed):
        """Return an iterable of CompositionBundle suggestions."""
        raise NotImplementedError(
            "Composer.suggest_bundle is implemented by the runtime binding."
        )


__all__ = ["Composer"]
