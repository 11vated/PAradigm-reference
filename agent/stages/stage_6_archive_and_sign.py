"""Stage 6 — Archive and sovereign sign.

The final stage. Takes the validated (and optionally evolved) seed,
asks the MemoryArchivist to write it to the commons, then asks the
SovereignSigner to produce a deterministic ECDSA-P256 signature using
RFC 6979 (per ADR-009). The signed `.gseed` bundle is the sole
externally-visible artifact the agent emits.

No seed may claim human authorship; provenance is one of
{"fully_agentic", "agent_assisted"} as declared in manifest.yaml.
The sovereignty gene is immutable and must be present.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from agent.stages._shared import StageReceipt, StageStatus
from agent.stages.stage_1_intent_resolution import IntentEnvelope
from agent.stages.stage_3_deterministic_growth import GrownSeed
from agent.sub_agents.memory_archivist import MemoryArchivist
from agent.sub_agents.sovereign_signer import SovereignSigner


Provenance = Literal["fully_agentic", "agent_assisted"]


@dataclass(frozen=True)
class SignedSeed:
    """A committed, signed, forkable seed ready to publish to the commons."""

    intent_id: str
    content_hash: str                # hex SHA-256 of JCS canonical bytes
    ecdsa_p256_signature_hex: str    # RFC 6979 deterministic
    signer_key_id: str
    archived_path: str               # path inside agent-managed commons
    provenance: Provenance
    license: str                     # always "GSPL-OSL-1.0" + content CC-BY-4.0
    lineage_parent_uris: tuple[str, ...]


@dataclass
class Stage6Output:
    signed_seed: SignedSeed | None = None
    receipt: StageReceipt | None = None


def run(
    envelope: IntentEnvelope,
    seed: GrownSeed,
    provenance: Provenance,
    archivist: MemoryArchivist,
    signer: SovereignSigner,
) -> Stage6Output:
    """Execute Stage 6.

    Archives then signs. Both sub-agents are purely deterministic:
    the archivist uses content-addressed paths, the signer uses
    RFC 6979 so the signature is byte-identical on any compliant host.
    """
    archived_path = archivist.write_commons(
        intent_id=envelope.intent_id,
        content_hash=seed.content_hash,
        jcs_bytes=seed.jcs_canonical_bytes,
    )

    signature = signer.sign_rfc6979_p256(
        content_hash_hex=seed.content_hash,
    )

    signed = SignedSeed(
        intent_id=envelope.intent_id,
        content_hash=seed.content_hash,
        ecdsa_p256_signature_hex=signature.signature_hex,
        signer_key_id=signature.key_id,
        archived_path=archived_path,
        provenance=provenance,
        license="GSPL-OSL-1.0 (spec) + CC-BY-4.0 (content)",
        lineage_parent_uris=tuple(envelope.substrate_libraries),
    )

    return Stage6Output(
        signed_seed=signed,
        receipt=StageReceipt(
            stage_id="stage_6_archive_and_sign",
            status=StageStatus.OK,
            note=(
                f"archived {envelope.intent_id} at {archived_path}; "
                f"sig={signature.signature_hex[:16]}…; "
                f"provenance={provenance}"
            ),
        ),
    )


__all__ = ["Provenance", "SignedSeed", "Stage6Output", "run"]
