"""Validator sub-agent.

Deterministic (non-LLM). Executes the 8-point validation contract
declared in seed-commons/validation/8_point_contract.md. Uses only
the code_execution tool (Wasm sandbox) for any in-process checks.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass

from agent.stages.stage_3_deterministic_growth import GrownSeed


@dataclass
class Validator:
    """Purely deterministic 8-point contract checker."""

    kernel_version: str
    spec_version: str
    max_payload_bytes: int = 64 * 1024 * 1024
    max_growth_depth: int = 1024

    def check_all_points(self, seed: GrownSeed, points):
        """Return the list of defects found (empty list == pass).

        Points are checked in declared order; every point is pure and
        deterministic. See agent/stages/stage_4_validation.py for the
        point enumeration.
        """
        raise NotImplementedError(
            "Validator.check_all_points is implemented by the kernel "
            "reference binding; see spec/02-gene-system.md §validation."
        )


__all__ = ["Validator"]
