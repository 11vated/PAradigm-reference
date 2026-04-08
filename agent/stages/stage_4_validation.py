"""Stage 4 — Validation.

Runs the 8-point validation contract against the grown seed:

  1. Twice-run determinism diff — grow the seed a second time and
     assert byte-identity of the JCS canonical payload and content hash.
  2. JCS canonicalization round-trip — parse and re-serialize; must be
     a fixed point.
  3. Kernel parse round-trip — source -> parsed -> re-emitted source
     -> parsed must reach the same IR.
  4. Lineage closure — every lineage parent URI must resolve inside
     the declared substrate libraries; no dangling edges.
  5. Sovereignty gate — sovereignty gene is immutable and present.
  6. Gene-type coverage — every referenced gene is in the 17 kernel
     types declared in spec/02.
  7. Licensing pin — every emitted artifact carries GSPL-OSL-1.0.
  8. Size and complexity bounds — payload <= configured max bytes,
     growth trace <= configured max depth.

On failure, the Validator sub-agent returns a structured defect list.
Stage 4 retries the pipeline (max 3 attempts) before escalating to
Stage 5's Evolver.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from agent.stages._shared import StageReceipt, StageStatus
from agent.stages.stage_3_deterministic_growth import GrownSeed
from agent.sub_agents.validator import Validator


ContractPoint = Literal[
    "twice_run_determinism",
    "jcs_round_trip",
    "kernel_parse_round_trip",
    "lineage_closure",
    "sovereignty_gate",
    "gene_type_coverage",
    "licensing_pin",
    "size_and_complexity_bounds",
]


@dataclass(frozen=True)
class Defect:
    point: ContractPoint
    severity: Literal["error", "warning"]
    message: str
    remediation_hint: str = ""


@dataclass(frozen=True)
class ValidationReport:
    seed_hash: str
    passed: bool
    defects: tuple[Defect, ...]
    points_checked: tuple[ContractPoint, ...]


@dataclass
class Stage4Output:
    report: ValidationReport | None = None
    receipt: StageReceipt | None = None


_ALL_POINTS: tuple[ContractPoint, ...] = (
    "twice_run_determinism",
    "jcs_round_trip",
    "kernel_parse_round_trip",
    "lineage_closure",
    "sovereignty_gate",
    "gene_type_coverage",
    "licensing_pin",
    "size_and_complexity_bounds",
)


def run(seed: GrownSeed, validator: Validator, attempt: int = 1) -> Stage4Output:
    """Execute Stage 4.

    Invokes the (purely deterministic) Validator on the grown seed and
    returns a structured report. Does NOT itself retry — the agent
    runtime's outer loop owns the retry-policy declared in manifest.yaml.
    """
    defects = validator.check_all_points(seed, points=_ALL_POINTS)
    passed = not any(d.severity == "error" for d in defects)

    report = ValidationReport(
        seed_hash=seed.content_hash,
        passed=passed,
        defects=tuple(defects),
        points_checked=_ALL_POINTS,
    )

    status = StageStatus.OK if passed else StageStatus.RETRY
    note = (
        f"pass hash={seed.content_hash[:16]}…"
        if passed
        else f"{sum(1 for d in defects if d.severity == 'error')} errors; attempt={attempt}"
    )

    return Stage4Output(
        report=report,
        receipt=StageReceipt(
            stage_id="stage_4_validation",
            status=status,
            note=note,
            attempt=attempt,
        ),
    )


__all__ = [
    "ContractPoint",
    "Defect",
    "ValidationReport",
    "Stage4Output",
    "run",
]
