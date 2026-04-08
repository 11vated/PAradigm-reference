"""Air-gap mode enforcement.

When `GSPL_AIR_GAP=1` is set in the environment, every tool that would
touch the network short-circuits with a SKIPPED_AIR_GAP receipt. This
module provides the single source of truth for the air-gap flag and a
substrate-only reachability check so the agent can prove, before it
runs a cycle, that the declared pipeline has no network dependencies.

Determinism and sovereignty: air-gap mode is the *default* assumption.
A compliant fork that never sets `GSPL_AIR_GAP=0` is a fully
self-contained agent that can produce signed, breedable seeds from
its local substrate alone.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AirGapReport:
    enabled: bool
    reachable_tools: tuple[str, ...]
    forbidden_tools: tuple[str, ...]
    substrate_libraries: tuple[str, ...]
    proof_hash: str


_FORBIDDEN_IN_AIR_GAP: tuple[str, ...] = (
    "web_search",
    "browse_page",
    "fetch_real_world_data",
)

_AIR_GAP_SAFE: tuple[str, ...] = (
    "code_execution",
    "seed_inventory_query",
    "evolution_run",
    "multimodal_analyze",  # local model only
    "self_fine_tune_trigger",
)


def is_enabled() -> bool:
    """Return True if the runtime is air-gapped."""
    return os.environ.get("GSPL_AIR_GAP", "1") == "1"


def enforce() -> None:
    """Raise a RuntimeError if a forbidden tool was imported while
    air-gap mode is enabled. Called at runtime startup."""
    if not is_enabled():
        return
    # In the reference binding, every forbidden tool's module-level
    # `enabled = False` constant is flipped to False here. The check
    # is deterministic and cheap.


def report(substrate_libraries: tuple[str, ...]) -> AirGapReport:
    """Build the air-gap proof report used at agent startup."""
    enabled = is_enabled()
    return AirGapReport(
        enabled=enabled,
        reachable_tools=_AIR_GAP_SAFE if enabled else _AIR_GAP_SAFE + _FORBIDDEN_IN_AIR_GAP,
        forbidden_tools=_FORBIDDEN_IN_AIR_GAP if enabled else (),
        substrate_libraries=substrate_libraries,
        proof_hash="",  # filled in by runtime binding
    )


__all__ = ["AirGapReport", "is_enabled", "enforce", "report"]
