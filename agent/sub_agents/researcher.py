"""Researcher sub-agent.

LLM-bearing. Owns all outward-facing tool access: web_search,
browse_page, multimodal_analyze, fetch_real_world_data. Disabled
entirely in air-gap mode.

Every fetch is typed and hashed before it enters the pipeline so the
downstream IntentOracle and CodeSmith never see raw web bytes, only
structured records attached to the intent envelope.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class LiveFetch:
    domain: str                  # e.g. "noaa.climate", "jpl.horizons", "pubchem"
    query: dict
    payload_bytes: bytes
    fetched_at_rfc3339: str
    source_url: str | None


class ToolLayer(Protocol):
    def web_search(self, query: str) -> list[dict]: ...
    def browse_page(self, url: str) -> bytes: ...
    def fetch_real_world_data(self, domain: str, query: dict) -> LiveFetch: ...
    def multimodal_analyze(self, blob: bytes, modality: str) -> dict: ...


@dataclass
class Researcher:
    """Bounds every live-context fetch to a typed, hashable record."""

    tools: ToolLayer
    deterministic_receipts: bool = True

    def resolve_live_context(self, prompt: str) -> list[LiveFetch]:
        """Return typed fetches needed to ground the prompt.

        Only called by Stage 0. In air-gap mode, Stage 0 never reaches
        this method.
        """
        raise NotImplementedError(
            "Researcher.resolve_live_context is implemented by the runtime "
            "binding; see intelligence/tool-layer.md for the schema."
        )


__all__ = ["Researcher", "LiveFetch", "ToolLayer"]
