"""IntentOracle sub-agent.

LLM-bearing. Parses natural-language prompts into classification,
normalized adjectives, and constraints. Backend is pluggable:
ollama, lmstudio, llamacpp, or any OpenAI-compatible endpoint.

Tools allowed: seed_inventory_query, fetch_real_world_data.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Classification:
    intent_id: str
    domain: str
    archetype: str
    substrate_libraries: tuple[str, ...]


@dataclass(frozen=True)
class RawAdjective:
    raw: str
    normalized_tag: str
    confidence: float


class LLMBackend(Protocol):
    """Pluggable LLM backend interface."""

    def generate(self, prompt: str, *, deterministic_seed: int) -> str: ...


@dataclass
class IntentOracle:
    """Parses prompts against the intent taxonomy.

    Determinism: given identical (prompt, backend, deterministic_seed),
    the oracle produces byte-identical classifications.
    """

    backend: LLMBackend
    deterministic_seed: int = 0
    taxonomy_path: str = "intelligence/intent-taxonomy.md"
    normalizer_path: str = "intelligence/adjective-normalization.md"

    def classify(self, prompt: str) -> Classification:
        """Return domain/archetype/intent_id + referenced substrate libs."""
        raise NotImplementedError(
            "IntentOracle.classify is implemented by the runtime binding; "
            "see intelligence/gspl-agent-full-capacity.md §5 for the contract."
        )

    def normalize_adjectives(self, prompt: str) -> list[RawAdjective]:
        """Normalize every adjective in the prompt to a taxonomy tag."""
        raise NotImplementedError

    def extract_constraints(self, prompt: str) -> dict:
        """Extract explicit numeric/categorical constraints from the prompt."""
        raise NotImplementedError

    def is_fictional(self, prompt: str) -> bool:
        """True unless the prompt references a real, nameable person or protected IP."""
        raise NotImplementedError


__all__ = ["IntentOracle", "Classification", "RawAdjective", "LLMBackend"]
