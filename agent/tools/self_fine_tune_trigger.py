"""self_fine_tune_trigger tool.

REQUIRES OPT-IN. When the bootstrap loop has accumulated
>= fine_tune_threshold_new_examples validated positive examples in the
gold corpus, this tool launches a local QLoRA 4-bit fine-tune of
CodeSmith on the combined (seed_commons + spec + language + gold)
dataset, evaluates the new adapter against the held-out set, and —
only if the required pass rate is met — promotes it to production.

Lineage gene: sovereignty (every fine-tune event is recorded as a
sovereignty-gene lineage edge on the agent's identity seed).

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FineTuneResult:
    adapter_path: str
    base_model_id: str
    examples_used: int
    eval_pass_rate: float
    promoted: bool
    reason: str


@dataclass
class SelfFineTuneTriggerTool:
    requires_opt_in: bool = True
    recipe_path: str = "agent/fine_tune/qlora_recipe.yaml"
    eval_harness_path: str = "agent/fine_tune/eval_harness.py"
    required_pass_rate: float = 0.995

    def trigger(self, *, opt_in_confirmed: bool) -> FineTuneResult:
        if not opt_in_confirmed:
            return FineTuneResult(
                adapter_path="",
                base_model_id="",
                examples_used=0,
                eval_pass_rate=0.0,
                promoted=False,
                reason="opt_in_not_confirmed",
            )
        raise NotImplementedError(
            "SelfFineTuneTriggerTool.trigger is implemented by the "
            "Unsloth QLoRA runtime binding; see agent/fine_tune/"
            "qlora_recipe.yaml."
        )


__all__ = ["SelfFineTuneTriggerTool", "FineTuneResult"]
