"""fetch_real_world_data tool.

Typed, declarative fetches against declared scientific / civic data
sources. Configured via intelligence/data-sources.yaml — the agent
never accepts arbitrary URLs here, only domains it has a registered
schema for. This is the ONLY way real-world numbers enter the
pipeline.

Supported domains out of the box (all optional, all air-gap skippable):
  - noaa.climate      — NOAA CDO v2 climate datasets
  - jpl.horizons      — JPL Horizons solar system ephemeris
  - arxiv             — arXiv paper metadata (OAI-PMH)
  - pubchem           — PubChem compound records
  - copernicus        — ESA Copernicus Earth observation
  - usgs.seismic      — USGS earthquake feed
  - rss               — plain RSS (sanitized to titles + links + pubdate)

Lineage gene: dimensional.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agent.stages._shared import air_gap_mode


@dataclass(frozen=True)
class DataFetch:
    domain: str
    query: dict[str, Any]
    payload_bytes: bytes
    schema_id: str
    fetched_at_rfc3339: str
    source_url: str | None


@dataclass
class FetchRealWorldDataTool:
    config_path: str = "intelligence/data-sources.yaml"

    def fetch(self, *, domain: str, query: dict[str, Any]) -> DataFetch:
        if air_gap_mode():
            raise RuntimeError("fetch_real_world_data disabled in air-gap mode")
        raise NotImplementedError(
            "FetchRealWorldDataTool.fetch is implemented by the runtime "
            "binding; see intelligence/data-sources.yaml for the domain "
            "schema registry."
        )


__all__ = ["FetchRealWorldDataTool", "DataFetch"]
