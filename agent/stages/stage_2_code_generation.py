"""Stage 2 — GSPL code generation.

The CodeSmith sub-agent is a fine-tuned LLM whose only capability is
emitting valid GSPL source text against a bounded substrate. It has no
tool access, no network, no file system. Its purity contract says:
"emit valid GSPL referencing only the provided substrate libraries, or
decline with a structured refusal."

The generated source is *not* executed here. Stage 3 parses it through
the deterministic kernel; Stage 4 validates it against the 8-point
contract. CodeSmith is never trusted beyond lexical emission.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from agent.stages._shared import StageReceipt, StageStatus
from agent.stages.stage_1_intent_resolution import IntentEnvelope
from agent.sub_agents.code_smith import CodeSmith


RefusalReason = Literal[
    "intent_out_of_substrate",
    "intent_requests_real_person",
    "intent_requests_protected_ip",
    "intent_violates_sovereignty",
    "intent_ambiguous",
]


@dataclass(frozen=True)
class CodeSmithOutput:
    """Either a block of candidate GSPL source, or a structured refusal.

    Exactly one of `source` and `refusal` is non-empty.
    """

    source: str
    refusal: RefusalReason | None
    substrate_libraries_referenced: tuple[str, ...]
    emitted_tokens: int


@dataclass
class Stage2Output:
    code: CodeSmithOutput | None = None
    receipt: StageReceipt | None = None


def run(envelope: IntentEnvelope, code_smith: CodeSmith) -> Stage2Output:
    """Execute Stage 2.

    Hands the structured intent envelope to CodeSmith and collects its
    emission. Never re-injects the raw user prompt or live-context
    payloads: only the sanitized envelope crosses this trust boundary.
    """
    emission = code_smith.emit(envelope)

    if emission.refusal is not None:
        return Stage2Output(
            code=CodeSmithOutput(
                source="",
                refusal=emission.refusal,
                substrate_libraries_referenced=(),
                emitted_tokens=0,
            ),
            receipt=StageReceipt(
                stage_id="stage_2_code_generation",
                status=StageStatus.FAILED,
                note=f"code_smith refused: {emission.refusal}",
            ),
        )

    output = CodeSmithOutput(
        source=emission.source,
        refusal=None,
        substrate_libraries_referenced=tuple(emission.libraries_referenced),
        emitted_tokens=emission.token_count,
    )

    return Stage2Output(
        code=output,
        receipt=StageReceipt(
            stage_id="stage_2_code_generation",
            status=StageStatus.OK,
            note=(
                f"emitted {output.emitted_tokens} tokens; "
                f"references {len(output.substrate_libraries_referenced)} libraries"
            ),
        ),
    )


__all__ = ["CodeSmithOutput", "Stage2Output", "RefusalReason", "run"]
