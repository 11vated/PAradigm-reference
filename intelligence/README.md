# Intelligence Layer (Layer 6)

The Intelligence layer is the *agentic* part of Paradigm — the system that turns natural-language descriptions into deterministic seeds. This is where LLMs live, and the layer is carefully designed so that all non-determinism is bounded inside it. Once the agent emits a seed, every layer below is reproducible bit-for-bit.

## Why a separate layer

Layers 0–5 are pure, deterministic, and reproducible. Layer 6 is none of those: LLM calls are stochastic, expensive, and depend on third-party services that change over time. Mixing the two would compromise the determinism guarantee that the rest of Paradigm is built on.

The Intelligence layer is therefore a **bounded boundary**:

- Inputs to the layer can be free-form natural language.
- Outputs from the layer are *always* fully-formed, signable, deterministic seeds.
- The layer's own behavior is *not* required to be reproducible (we cache and replay agent runs as a recovery mechanism, not a guarantee).

Once a seed leaves the Intelligence layer, every operation downstream is bit-stable.

## Index

| File | Topic |
|---|---|
| [`gspl-agent.md`](gspl-agent.md) | The 5-stage Concept-to-Seed pipeline |
| [`8-sub-agents.md`](8-sub-agents.md) | The 8 specialized sub-agents (Vision, Personality, MusicTheory, …) |
| [`memory-system.md`](memory-system.md) | The 4-layer memory architecture |
| [`template-bridge.md`](template-bridge.md) | How agents convert plans into engine-specific gene assignments |
| [`adjective-normalization.md`](adjective-normalization.md) | Mapping natural-language adjectives to gene values |
| [`intent-taxonomy.md`](intent-taxonomy.md) | The taxonomy of user intents the agent recognizes |

## Multi-provider abstraction

The Intelligence layer is provider-agnostic. It supports OpenAI (gpt-4o, gpt-4-turbo), Anthropic (claude-sonnet-4, claude-opus-4), Google (gemini-2.5-pro), and any local model exposed via the OpenAI-compatible API. The provider is selected per call by routing rules (described in `gspl-agent.md`), and a single agent run may use multiple providers for different sub-stages.

Provider failures are handled by a fallback chain — if Anthropic is down, the same call is retried against OpenAI with the same prompt and the same temperature.

## What lives outside this layer

These are explicitly *not* in the Intelligence layer:

- Engine code (Layer 3) — pure, deterministic, no LLM access.
- Evolution algorithms (Layer 4) — pure, deterministic.
- The studio UI (Layer 6 frontend) — calls into the Intelligence layer but does not contain it.
- The federation gateway — knows nothing about LLMs.

This separation is **architectural**, not just stylistic. Mixing them up has been the failure mode of every "AI creative tool" we have seen.
