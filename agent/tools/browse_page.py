"""browse_page tool.

Fetches a single URL as typed bytes + MIME + ETag. Respects robots.txt
by default. No JS execution, no cookies. Every fetch produces a
typed lineage record.

Lineage gene: dimensional.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass

from agent.stages._shared import air_gap_mode


@dataclass(frozen=True)
class PageFetch:
    url: str
    mime_type: str
    etag: str | None
    body_bytes: bytes
    fetched_at_rfc3339: str


@dataclass
class BrowsePageTool:
    respects_robots_txt: bool = True
    user_agent: str = "gspl-agent/1.0 (+https://gspl.dev)"
    max_bytes: int = 8 * 1024 * 1024

    def fetch(self, url: str) -> PageFetch:
        if air_gap_mode():
            raise RuntimeError("browse_page disabled in air-gap mode")
        raise NotImplementedError(
            "BrowsePageTool.fetch is implemented by the runtime binding; "
            "see intelligence/tool-layer.md §browse_page."
        )


__all__ = ["BrowsePageTool", "PageFetch"]
