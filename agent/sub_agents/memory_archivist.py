"""MemoryArchivist sub-agent.

Deterministic (non-LLM). Writes validated seeds to a content-addressed
path in the agent-managed commons:

    <commons_root>/<domain>/<intent_id>/<content_hash[:2]>/<content_hash>.gseed

Also appends a lineage ledger entry recording every tool call and
every stage receipt for the seed. The ledger is append-only and
tamper-evident via chained SHA-256.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MemoryArchivist:
    commons_root: str
    ledger_path: str

    def write_commons(
        self,
        *,
        intent_id: str,
        content_hash: str,
        jcs_bytes: bytes,
    ) -> str:
        """Write the seed to the content-addressed commons path.

        Returns the absolute path written. The path is a pure function
        of (commons_root, intent_id, content_hash) so re-archiving is a
        no-op idempotent.
        """
        raise NotImplementedError(
            "MemoryArchivist.write_commons is implemented by the runtime "
            "binding; see agent/tools/filesystem_write_commons."
        )


__all__ = ["MemoryArchivist"]
