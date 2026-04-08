"""QLoRA eval harness for CodeSmith adapters.

Runs a candidate adapter against a held-out set of intent prompts and
computes the four canonical metrics required for promotion:

  1. stage_4_first_try_pass_rate  — fraction of prompts where the full
     six-stage pipeline reaches a signed seed on the first attempt.
  2. jcs_round_trip_byte_identity — fraction where the grown payload
     round-trips through JCS canonicalization with byte identity.
  3. lineage_closure_rate         — fraction where every lineage parent
     URI resolves inside the declared substrate.
  4. refusal_calibration          — fraction where CodeSmith refuses
     exactly when and only when the prompt truly is out-of-substrate.

An adapter is promoted only if ALL four metrics >= required_pass_rate
(default 0.995). Partial passes are archived for inspection.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class HeldOutExample:
    intent_id: str
    prompt: str
    expected_envelope_hash: str
    expected_source_hash: str
    is_in_substrate: bool        # ground truth for refusal_calibration


@dataclass(frozen=True)
class EvalMetrics:
    stage_4_first_try_pass_rate: float
    jcs_round_trip_byte_identity: float
    lineage_closure_rate: float
    refusal_calibration: float

    def all_pass(self, threshold: float) -> bool:
        return (
            self.stage_4_first_try_pass_rate >= threshold
            and self.jcs_round_trip_byte_identity >= threshold
            and self.lineage_closure_rate >= threshold
            and self.refusal_calibration >= threshold
        )


@dataclass
class EvalHarness:
    held_out_dir: Path
    required_pass_rate: float = 0.995

    def load_held_out(self) -> list[HeldOutExample]:
        raise NotImplementedError(
            "EvalHarness.load_held_out is implemented by the runtime "
            "corpus binding."
        )

    def evaluate(self, adapter_path: Path) -> EvalMetrics:
        """Load the adapter into CodeSmith, run the full pipeline over
        the held-out set, and return the four canonical metrics.

        Pure given (adapter bytes, held-out set, kernel version)."""
        raise NotImplementedError(
            "EvalHarness.evaluate is implemented by the Unsloth adapter "
            "loader binding; see agent/fine_tune/qlora_recipe.yaml."
        )


__all__ = ["HeldOutExample", "EvalMetrics", "EvalHarness"]
