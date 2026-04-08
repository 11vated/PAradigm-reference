"""Stage 0 — Live context ingestion (optional).

Runs only when the prompt references real-world context (e.g. "make a seed
based on today's climate data for Jakarta"). Skipped entirely in air-gap mode.

Pulls typed real-world data through the Researcher sub-agent's tool-layer
access. Every fetch is hashed and attached to the intent envelope as a
`live_context` record. The downstream Stage 1 IntentOracle is free to
consume these records when resolving intent, but the substrate compiler
(Stage 2 CodeSmith) never sees them directly — it only sees the structured
intent envelope.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Iterable

from agent.stages._shared import StageReceipt, StageStatus, air_gap_mode
from agent.sub_agents.researcher import Researcher


@dataclass(frozen=True)
class LiveContextRecord:
    """One typed real-world fetch, attached to the intent envelope."""

    domain: str  # e.g. "noaa.climate", "jpl.horizons", "pubchem"
    query: dict[str, Any]
    payload_sha256: str
    fetched_at_rfc3339: str
    source_url: str | None


@dataclass
class Stage0Output:
    live_context: list[LiveContextRecord] = field(default_factory=list)
    receipt: StageReceipt | None = None


def needs_live_context(prompt: str) -> bool:
    """Heuristic: does the prompt reference a live, time- or place-dependent fact?

    Uses a deterministic rule set over the adjacentcy graph of the prompt's
    tokenization against the intent taxonomy's `live_context_triggers`.
    """
    triggers = (
        "today",
        "current",
        "live",
        "real-time",
        "latest",
        "now",
        "this week",
        "forecast",
        "tonight",
    )
    lowered = prompt.lower()
    return any(t in lowered for t in triggers)


def run(prompt: str, researcher: Researcher) -> Stage0Output:
    """Execute Stage 0.

    Returns a Stage0Output with either an empty list (no live context needed
    or air-gap mode) or a list of typed LiveContextRecord entries.

    This function is PURE given (prompt, researcher.deterministic_receipts).
    Re-running with the same inputs produces byte-identical output.
    """
    if air_gap_mode():
        return Stage0Output(
            live_context=[],
            receipt=StageReceipt(
                stage_id="stage_0_live_context",
                status=StageStatus.SKIPPED_AIR_GAP,
                note="air-gap mode: no network access",
            ),
        )

    if not needs_live_context(prompt):
        return Stage0Output(
            live_context=[],
            receipt=StageReceipt(
                stage_id="stage_0_live_context",
                status=StageStatus.SKIPPED_NOT_NEEDED,
                note="prompt contains no live-context triggers",
            ),
        )

    records: list[LiveContextRecord] = []
    for fetch in researcher.resolve_live_context(prompt):
        payload_hash = sha256(fetch.payload_bytes).hexdigest()
        records.append(
            LiveContextRecord(
                domain=fetch.domain,
                query=fetch.query,
                payload_sha256=payload_hash,
                fetched_at_rfc3339=fetch.fetched_at_rfc3339,
                source_url=fetch.source_url,
            )
        )

    return Stage0Output(
        live_context=records,
        receipt=StageReceipt(
            stage_id="stage_0_live_context",
            status=StageStatus.OK,
            note=f"fetched {len(records)} live context records",
        ),
    )


__all__ = ["LiveContextRecord", "Stage0Output", "needs_live_context", "run"]
