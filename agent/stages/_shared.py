"""Shared primitives for the six-stage GSPL agent pipeline.

Every stage module imports its receipt type, status enum, and the
`air_gap_mode()` helper from here so the pipeline presents a single
deterministic contract to the runtime.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class StageStatus(str, Enum):
    """Deterministic outcome of a single stage run."""

    OK = "ok"
    SKIPPED_AIR_GAP = "skipped_air_gap"
    SKIPPED_NOT_NEEDED = "skipped_not_needed"
    RETRY = "retry"
    FAILED = "failed"
    ESCALATED_TO_EVOLVER = "escalated_to_evolver"


@dataclass(frozen=True)
class StageReceipt:
    """Immutable audit record attached to every stage output.

    Receipts are appended to the lineage ledger of the resulting seed so
    that any compliant reader can reconstruct exactly which stages ran,
    in which order, with which outcome.
    """

    stage_id: str
    status: StageStatus
    note: str = ""
    started_at_rfc3339: str = ""
    finished_at_rfc3339: str = ""
    attempt: int = 1
    metrics: dict[str, Any] = field(default_factory=dict)


def air_gap_mode() -> bool:
    """Return True if the agent runtime is operating in air-gap mode.

    The runtime sets `GSPL_AIR_GAP=1` at startup when the operator
    requests a network-free run. In that mode every tool that would
    touch the network MUST short-circuit with a SKIPPED_AIR_GAP receipt.
    """
    return os.environ.get("GSPL_AIR_GAP", "0") == "1"


__all__ = ["StageStatus", "StageReceipt", "air_gap_mode"]
