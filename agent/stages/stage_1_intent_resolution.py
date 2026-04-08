"""Stage 1 — Intent resolution.

The IntentOracle sub-agent parses the user's natural-language prompt
against the intent taxonomy (`intelligence/intent-taxonomy.md`) and runs
the adjective normalizer (`intelligence/adjective-normalization.md`),
producing a structured JSON intent envelope that downstream stages
consume.

The envelope is the *only* thing Stage 2 CodeSmith sees; the raw prompt
and any Stage 0 live-context records are deliberately walled off so the
code-generation model cannot be manipulated by untrusted text.

License: GSPL Open Specification License (GSPL-OSL-1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from agent.stages._shared import StageReceipt, StageStatus
from agent.stages.stage_0_live_context import LiveContextRecord
from agent.sub_agents.intent_oracle import IntentOracle


@dataclass(frozen=True)
class NormalizedAdjective:
    """A raw adjective from the prompt resolved to a taxonomy tag."""

    raw: str
    normalized: str  # e.g. "mood.sadness.0.7", "material.wood.0.9"
    confidence: float


@dataclass(frozen=True)
class IntentEnvelope:
    """Structured, deterministic description of what the user wants.

    This is the canonical hand-off contract between the LLM-bearing
    IntentOracle and the purity-contracted CodeSmith. No free text
    survives past this point.
    """

    intent_id: str                      # e.g. "sprite.character.melancholy_bard"
    domain: str                         # e.g. "sprite", "scene", "creature"
    archetype: str                      # e.g. "humanoid.character.bard"
    adjectives: tuple[NormalizedAdjective, ...]
    constraints: dict[str, Any]         # canvas, determinism, fictionality, etc.
    live_context: tuple[LiveContextRecord, ...] = ()
    substrate_libraries: tuple[str, ...] = ()  # libraries this intent may touch


@dataclass
class Stage1Output:
    envelope: IntentEnvelope | None = None
    receipt: StageReceipt | None = None


def run(
    prompt: str,
    live_context: list[LiveContextRecord],
    oracle: IntentOracle,
) -> Stage1Output:
    """Execute Stage 1.

    Calls the IntentOracle to classify the prompt's domain and archetype,
    normalize every adjective against the taxonomy, and attach any Stage
    0 live-context records. Returns a Stage1Output whose envelope is
    deterministic given (prompt, live_context, oracle.deterministic_seed).
    """
    classification = oracle.classify(prompt)
    normalized = tuple(
        NormalizedAdjective(
            raw=adj.raw,
            normalized=adj.normalized_tag,
            confidence=adj.confidence,
        )
        for adj in oracle.normalize_adjectives(prompt)
    )

    constraints = oracle.extract_constraints(prompt)
    # Every seed produced by the agent MUST be deterministic.
    constraints.setdefault("determinism", True)
    # Default fictionality is true unless the oracle determines the
    # prompt references a real, nameable person or protected IP.
    constraints.setdefault("is_fictional", oracle.is_fictional(prompt))

    envelope = IntentEnvelope(
        intent_id=classification.intent_id,
        domain=classification.domain,
        archetype=classification.archetype,
        adjectives=normalized,
        constraints=constraints,
        live_context=tuple(live_context),
        substrate_libraries=tuple(classification.substrate_libraries),
    )

    return Stage1Output(
        envelope=envelope,
        receipt=StageReceipt(
            stage_id="stage_1_intent_resolution",
            status=StageStatus.OK,
            note=(
                f"intent={envelope.intent_id} "
                f"domain={envelope.domain} "
                f"adjectives={len(envelope.adjectives)} "
                f"libs={len(envelope.substrate_libraries)}"
            ),
        ),
    )


__all__ = [
    "NormalizedAdjective",
    "IntentEnvelope",
    "Stage1Output",
    "run",
]
