"""Self-bootstrapping loop.

Phase A — Gold corpus seeding.
    A curator script walks seed_commons/ + spec/ + language/ and emits
    a gold corpus of (intent_prompt, expected_envelope, expected_source,
    expected_hash) tuples. These are the ground-truth targets CodeSmith
    is initially trained against.

Phase B — Continuous loop (this module).
    For every cycle (default 1000 synthetic prompts):
      1. SyntheticPromptGenerator samples a domain, archetype, and
         adjective bundle from the taxonomy and emits a natural-language
         prompt.
      2. Runs the full six-stage pipeline.
      3. If Stage 4 passes, the resulting (prompt, envelope, source,
         hash) is archived as a new gold example with provenance
         `fully_agentic`.
      4. If Stage 4 fails after all retries, the defect set is archived
         to the negative corpus as a contrastive example.
      5. Every N cycles, the loop emits a manifest fragment summarizing
         the new examples.

Phase C — Fine-tune trigger.
    When the gold corpus has grown by `fine_tune_threshold_new_examples`
    since the last fine-tune (default 50_000), the loop calls
    SelfFineTuneTriggerTool.trigger(opt_in_confirmed=operator_flag).
    The new adapter is evaluated against a held-out set of 10_000
    examples. If eval_pass_rate >= 0.995 the adapter is promoted;
    otherwise it is archived for inspection and the previous adapter
    stays in production.

Phase D — Federated adapter governance (optional).
    Operators may publish their promoted adapters to a federated
    registry. Adapters are signed by the SovereignSigner and carry
    their gold-corpus manifest so downstream forks can audit every
    example used in training.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BootstrapConfig:
    synthetic_prompts_per_cycle: int = 1000
    gold_corpus_minimum_size: int = 5000
    fine_tune_threshold_new_examples: int = 50_000
    held_out_size: int = 10_000
    required_pass_rate: float = 0.995
    gold_corpus_dir: Path = Path("agent/bootstrap/corpus/gold/")
    negative_corpus_dir: Path = Path("agent/bootstrap/corpus/negative/")
    manifest_path: Path = Path("agent/bootstrap/corpus/manifest.json")


@dataclass
class CycleResult:
    prompts_attempted: int
    prompts_passed: int
    prompts_failed: int
    new_gold_examples: int
    new_negative_examples: int
    fine_tune_triggered: bool


@dataclass
class BootstrapLoop:
    """Drives the closed-loop self-improvement cycle.

    The loop is idempotent: given the same (synthetic seed, cycle
    index), it produces the same prompts and therefore the same
    corpus deltas.
    """

    config: BootstrapConfig
    cycle_index: int = 0

    def run_cycle(self) -> CycleResult:
        raise NotImplementedError(
            "BootstrapLoop.run_cycle is implemented by the runtime "
            "binding; see intelligence/self-bootstrapping-loop.md."
        )

    def run_until(self, stop_after_cycles: int) -> list[CycleResult]:
        """Run cycles until either stop_after_cycles elapses or the
        operator sends SIGINT. Each cycle result is appended to the
        manifest."""
        results: list[CycleResult] = []
        for _ in range(stop_after_cycles):
            results.append(self.run_cycle())
            self.cycle_index += 1
        return results


__all__ = ["BootstrapConfig", "CycleResult", "BootstrapLoop"]
