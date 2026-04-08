"""SovereignSigner sub-agent.

Deterministic (non-LLM). Signs the content hash of every grown seed
using ECDSA over NIST P-256 with RFC 6979 deterministic nonces (per
ADR-009). Output is byte-identical across compliant hosts so the
lineage graph is cryptographically reproducible.

The sovereign signing key is managed locally — never uploaded, never
exported to an HSM under someone else's control. The agent is fully
self-sovereign.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Signature:
    key_id: str
    signature_hex: str        # DER-encoded ECDSA-P256, hex
    algorithm: str = "ecdsa-p256-rfc6979-sha256"


@dataclass
class SovereignSigner:
    """Deterministic ECDSA-P256 signer per RFC 6979."""

    key_id: str
    private_key_path: str     # local file; never transmitted

    def sign_rfc6979_p256(self, *, content_hash_hex: str) -> Signature:
        """Return a deterministic ECDSA-P256 signature over the hex digest.

        Because RFC 6979 eliminates the random nonce, repeated calls
        with the same (private_key, content_hash) produce byte-identical
        output on any compliant host.
        """
        raise NotImplementedError(
            "SovereignSigner.sign_rfc6979_p256 is implemented by the "
            "runtime crypto binding; see ADR-009 and agent/tools/"
            "ecdsa_p256_rfc6979_sign."
        )


__all__ = ["SovereignSigner", "Signature"]
