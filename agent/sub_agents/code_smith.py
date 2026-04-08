"""CodeSmith sub-agent.

Fine-tuned LLM. Purity contract: emits only valid GSPL source text
bound to the substrate libraries declared in agent/manifest.yaml, or
declines with a structured refusal. NO TOOL ACCESS. NO NETWORK. NO
FILE SYSTEM. NO RAW PROMPT. Only the sanitized IntentEnvelope crosses
this trust boundary.

Trained on seed_commons/ + spec/ + language/. See
agent/fine_tune/qlora_recipe.yaml.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from agent.stages.stage_1_intent_resolution import IntentEnvelope


RefusalReason = Literal[
    "intent_out_of_substrate",
    "intent_requests_real_person",
    "intent_requests_protected_ip",
    "intent_violates_sovereignty",
    "intent_ambiguous",
]


@dataclass(frozen=True)
class Emission:
    source: str                                # GSPL source text, or ""
    refusal: RefusalReason | None
    libraries_referenced: tuple[str, ...]
    token_count: int


@dataclass
class CodeSmith:
    """Purity-bounded GSPL code emitter."""

    model_path: str
    substrate_libraries: tuple[str, ...]
    max_tokens: int = 8192

    def emit(self, envelope: IntentEnvelope) -> Emission:
        """Emit GSPL source or a structured refusal.

        Contract:
          - Every `import` line must reference a library in
            `self.substrate_libraries`.
          - Every emitted identifier must resolve inside the kernel's
            17 declared gene types.
          - The sovereignty gene must be present and immutable.
          - On any doubt, the model declines with a structured reason.
        """
        raise NotImplementedError(
            "CodeSmith.emit is implemented by the fine-tuned backend; "
            "see agent/fine_tune/qlora_recipe.yaml and spec/02-gene-system.md"
        )


__all__ = ["CodeSmith", "Emission", "RefusalReason"]
