"""web_search tool.

Providers: self-hosted SearXNG (default), Brave Search API, Kagi API.
No provider is mandatory; the agent is fully air-gap capable without
any of them.

Lineage gene: dimensional (every result is attached as a dimensional
lineage edge on the final seed).

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from agent.stages._shared import air_gap_mode


Provider = Literal["searxng_self_hosted", "brave_search_api", "kagi_api"]


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str
    rank: int


@dataclass
class WebSearchTool:
    provider: Provider = "searxng_self_hosted"
    endpoint: str = "http://localhost:8080"
    api_key: str | None = None
    max_results: int = 10

    def search(self, query: str) -> list[SearchResult]:
        if air_gap_mode():
            return []
        raise NotImplementedError(
            "WebSearchTool.search is implemented by the runtime provider "
            "binding; see intelligence/tool-layer.md §web_search."
        )


__all__ = ["WebSearchTool", "SearchResult", "Provider"]
