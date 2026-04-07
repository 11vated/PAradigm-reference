# 055 — LLM runtime and bring-your-own-model

## Question
How does GSPL integrate LLM inference for the agent (Brief 029-034) — supporting local models for sovereignty, hosted APIs for convenience, and bring-your-own-key configurations — without becoming locked to a single provider or producing wildly inconsistent quality?

## Why it matters
The agent depends on LLM reasoning. The LLM is the most expensive, most variable, and most provider-dependent component in the entire stack. GSPL's sovereignty commitment means *local* must work; GSPL's UX commitment means *hosted* must be one-click; GSPL's economics commitment means *user pays directly* must work too. Threading this needle without three separate code paths is the challenge.

## What we know from the spec
- Briefs 029-034: agent and memory architecture.
- Brief 048: agent runs in-process by default.
- The agent uses tool calling.

## Findings — three runtime modes

### Mode 1: Local LLM
The agent runs against a model loaded into the studio process.
- **Library:** llama.cpp (via llama-cpp-rs binding) at v1 for breadth of model support.
- **Alternative:** mistral.rs and candle as v1.5 backends (pure Rust, easier deployment).
- **Models supported at v1:**
  - Qwen 2.5 7B / 14B (general-purpose default).
  - Mistral Small (3.1 24B) (higher quality).
  - Llama 3.1 8B (broad ecosystem).
  - Gemma 2 9B.
  - DeepSeek Coder 7B (for code-heavy engines).
- **Quantization:** Q4_K_M default; Q5_K_M optional for better quality; Q8 for max quality.
- **Hardware target:** 8GB RAM minimum (Q4 7B), 16GB recommended, 32GB optimal.
- **Cold start:** ≤ 2 seconds for the embedded first-launch model; 5-15s for full models.

### Mode 2: Hosted API
The agent calls a hosted LLM provider via OpenAI-compatible API.
- **Supported providers at v1:** Anthropic (claude.ai), OpenAI, OpenRouter, Together, Groq, DeepInfra, Fireworks, any OpenAI-compatible endpoint.
- **API keys are user-provided and stored encrypted in the profile** (Brief 042 key management).
- **Per-call cost is shown in the studio** so users see what they're spending.
- **No GSPL relay or proxy.** The API call goes directly from the user's studio to the provider.
- **Provider rate limits respected** with backoff.

### Mode 3: Hybrid
The agent dynamically chooses between local and hosted based on the request.
- **Cheap reasoning (intent parsing, modifier interpretation):** local.
- **Expensive reasoning (planning, complex composition):** hosted.
- **User-configurable thresholds.**
- **Privacy-sensitive requests stay local** (the user can mark content as "never send to a hosted API").

## Tool calling abstraction

The agent's tool surface (Brief 029) is *provider-agnostic*. The studio has a `LLMClient` trait with implementations for:
- llama.cpp (local).
- Anthropic API (Claude).
- OpenAI API.
- OpenAI-compatible (catchall).

Each implementation translates the provider's tool-calling format (JSON Schema, function calling, structured output) to GSPL's canonical tool format. The agent itself never sees provider-specific details.

## Quality gating

Different LLMs produce different quality. GSPL has a **quality bar** per task:
- **Intent parsing:** Llama 3.1 8B is sufficient.
- **Variant generation reasoning:** Qwen 2.5 14B or hosted.
- **Critic explanation:** any 7B+ model.
- **Cross-engine composition planning:** hosted recommended; local 14B+ acceptable.

The studio surfaces quality warnings: "this task is recommended for hosted or 14B+ local models. You're using Llama 7B. Continue?"

## Privacy guarantees

- **Local mode:** zero data leaves the device. Period.
- **Hosted mode:** the agent only sends what's necessary for the task (the seed metadata, the user prompt, the relevant lineage entries) — never the entire project, never the identity key, never the user vocabulary.
- **The studio shows what's being sent** before sending; user can audit.
- **No telemetry to GSPL** about LLM use (no metrics, no usage reports).
- **User can opt into anonymized aggregate metrics** for research (Brief 060 compliance).

## Cost transparency

The studio tracks per-LLM-call cost in real time:
- **Token counts** (input and output).
- **Per-1K-token cost** for the configured provider.
- **Running session total.**
- **Daily and monthly totals** (local only, never transmitted).
- **Cost preview** before expensive operations ("this generation will use ~3000 tokens, est. $0.01").

## Model registry

The studio ships with a **model registry** that lists known models with metadata:
- **Name, size, license, recommended use cases.**
- **Quality tier** (1-5).
- **Hardware requirements.**
- **Download URL** (for local models).
- **Provider URL** (for hosted).

Users can install local models with one click; the studio downloads, verifies, and registers them. The registry is updateable per release; users can also add custom entries.

## Risks identified

- **LLM quality variance:** the same prompt produces wildly different results on different models. Mitigation: per-task quality bars; warnings; recommended models per task.
- **Provider lock-in:** if hosted is the easy path, GSPL becomes dependent on Anthropic/OpenAI. Mitigation: local mode is first-class and works for the default use case.
- **API key leakage:** user keys in plaintext are dangerous. Mitigation: keys encrypted with the profile passphrase; keys never leave the studio process.
- **Model license drift:** open-weight licenses change. Mitigation: model registry tracks license; warnings on commercial use of restricted models.
- **Cost surprise:** users don't realize how much hosted is costing them. Mitigation: real-time cost display; per-session warning if running high.
- **Local model staleness:** Qwen 2.5 today is great; Qwen 4 next year is better. Mitigation: registry updates per release; users can switch with one click.
- **Tool calling format drift:** providers change their function-calling APIs. Mitigation: per-provider adapter; tested per release.

## Recommendation

1. **Adopt the three-mode architecture** in `architecture/llm-runtime.md`.
2. **Local LLM via llama.cpp at v1**; mistral.rs and candle at v1.5.
3. **Hosted via OpenAI-compatible API** as the catch-all.
4. **Hybrid mode is opt-in**, defaults to local.
5. **API keys encrypted** with the profile passphrase.
6. **Tool calling is provider-agnostic** via the `LLMClient` trait.
7. **Per-task quality bars** with user-visible warnings.
8. **Cost transparency** is mandatory for hosted use.
9. **Privacy-sensitive marking** for local-only requests.
10. **Model registry** ships with v1 and is updatable.
11. **No GSPL relay or proxy.** Direct user → provider.

## Confidence
**4/5.** Local LLM and hosted API integration are well-trodden. The 4/5 reflects the unmeasured impact of LLM quality variance on the agent's reliability.

## Spec impact

- `architecture/llm-runtime.md` — full LLM runtime architecture.
- `protocols/llm-client-trait.md` — provider-agnostic tool calling.
- `architecture/model-registry.md` — registry format.
- `protocols/cost-transparency.md` — cost display spec.
- `tests/llm-quality-bars.md` — per-task quality conformance.
- New ADR: `adr/00NN-no-llm-relay.md`.

## Open follow-ups

- Empirical quality benchmarks of the v1 supported local models.
- Decide on llama.cpp vs mistral.rs vs candle as the v1.5 default.
- Build the model registry format and tooling.
- Build the cost display UI.
- Decide on the privacy-sensitive marking UX.
- Investigate model license tracking automation.

## Sources

- llama.cpp documentation and ggml format.
- OpenAI function calling specification.
- Anthropic tool use documentation.
- Hugging Face open LLM leaderboards.
- Internal: Briefs 029-034, 042, 048.
