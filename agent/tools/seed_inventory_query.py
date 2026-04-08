"""seed_inventory_query tool.

Purely local, air-gap compatible. Queries the agent-managed commons
by (domain, archetype, tag, lineage_parent) and returns content-hashed
pointers to matching seeds. Used by IntentOracle to check whether a
similar seed already exists before asking CodeSmith to emit a new one.

Lineage gene: symbolic.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class InventoryHit:
    intent_id: str
    content_hash: str
    commons_path: str
    tags: tuple[str, ...]
    lineage_parents: tuple[str, ...]


@dataclass
class SeedInventoryQueryTool:
    commons_root: str
    index_path: str = "agent/bootstrap/corpus/manifest.json"

    def query(
        self,
        *,
        domain: str | None = None,
        archetype: str | None = None,
        tags: tuple[str, ...] = (),
        lineage_parent: str | None = None,
        limit: int = 32,
    ) -> list[InventoryHit]:
        raise NotImplementedError(
            "SeedInventoryQueryTool.query is implemented by the runtime "
            "commons index binding."
        )


__all__ = ["SeedInventoryQueryTool", "InventoryHit"]
