"""Stage 3 — Deterministic growth.

Parses the CodeSmith-emitted GSPL source through the reference kernel,
then grows the resulting seed to its canonical materialization using
the deterministic engine readers (meshes, audio frames, simulation
trajectories, etc.). This stage performs NO network I/O and uses a
fixed RNG seed derived from the intent envelope's `intent_id`, so it
is byte-exact reproducible across compliant readers.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

from agent.stages._shared import StageReceipt, StageStatus
from agent.stages.stage_1_intent_resolution import IntentEnvelope
from agent.stages.stage_2_code_generation import CodeSmithOutput


@dataclass(frozen=True)
class GrownSeed:
    """A parsed, grown, in-memory seed.

    `jcs_canonical_bytes` is the RFC 8785 JSON Canonicalization Scheme
    serialization of the seed's kernel payload, and `content_hash` is
    the SHA-256 digest of those exact bytes (per ADR-009).
    """

    intent_id: str
    kernel_payload: dict[str, Any]
    jcs_canonical_bytes: bytes
    content_hash: str  # hex SHA-256 of jcs_canonical_bytes
    growth_trace: tuple[str, ...]  # ordered list of reader invocations


@dataclass
class Stage3Output:
    seed: GrownSeed | None = None
    receipt: StageReceipt | None = None


def _derive_rng_seed(intent_id: str) -> bytes:
    """RNG seed = SHA-256(b'gspl.stage3:' || intent_id)."""
    return sha256(b"gspl.stage3:" + intent_id.encode("utf-8")).digest()


def run(
    envelope: IntentEnvelope,
    code: CodeSmithOutput,
    kernel: "Kernel",  # type: ignore[name-defined]
) -> Stage3Output:
    """Execute Stage 3.

    Parses `code.source` through the reference kernel with a fixed RNG
    seed, grows every reachable engine reader, and serializes the
    resulting payload to JCS-canonical bytes. All operations are pure
    given (envelope.intent_id, code.source, kernel version).
    """
    rng_seed = _derive_rng_seed(envelope.intent_id)
    parsed = kernel.parse(code.source, rng_seed=rng_seed)
    grown = kernel.grow(parsed, envelope=envelope, rng_seed=rng_seed)

    jcs_bytes = kernel.to_jcs_canonical_bytes(grown.payload)
    content_hash = sha256(jcs_bytes).hexdigest()

    seed = GrownSeed(
        intent_id=envelope.intent_id,
        kernel_payload=grown.payload,
        jcs_canonical_bytes=jcs_bytes,
        content_hash=content_hash,
        growth_trace=tuple(grown.growth_trace),
    )

    return Stage3Output(
        seed=seed,
        receipt=StageReceipt(
            stage_id="stage_3_deterministic_growth",
            status=StageStatus.OK,
            note=(
                f"grown {envelope.intent_id}; "
                f"hash={content_hash[:16]}…; "
                f"readers={len(seed.growth_trace)}"
            ),
        ),
    )


__all__ = ["GrownSeed", "Stage3Output", "run"]
