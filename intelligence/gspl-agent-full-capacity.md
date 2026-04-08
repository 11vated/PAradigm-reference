# GSPL Agent — Full Capacity Specification (v1.0)

**Title:** Sovereign GSPL Agent — Concept-to-Seed with Full Internet, Tool Use, Self-Bootstrapping, and Unlimited Scale
**Status:** Ready for implementation (Phase 3 MVP)
**License:** GSPL Open Specification License (free forever, no limits)
**Depends on:** `intelligence/gspl-agent.md` (base architecture), `intelligence/8-sub-agents.md`, `intelligence/memory-system.md`, `intelligence/template-bridge.md`, `intelligence/adjective-normalization.md`, `intelligence/intent-taxonomy.md`, `spec/02–07`, `seed-commons/CONTRIBUTING-seeds.md`.
**Goal:** Make the native GSPL Agent the undisputed best GSPL code generator on the planet — the only one that is truly sovereign, self-improving, and capable of populating the entire `seed-commons/` autonomously.

This spec extends — it does not replace — `gspl-agent.md`. Every sub-agent, stage, and type declared in the base doc remains; this doc adds the tool layer, the internet layer, the self-bootstrapping loop, and the local fine-tuning pipeline that turn the base agent into a full-capacity sovereign creator.

## 1. Non-negotiable principles

These are inherited from the GSPL Open Specification License and the determinism spec. They cannot be relaxed by any implementer, integrator, or operator.

1. **100% free and sovereign.** The Agent runs locally via Ollama / LM Studio / llama.cpp / any OpenAI-compatible endpoint. No cloud dependency. No API keys required. No rate limits. No billing. No telemetry except what the operator opts into.
2. **Deterministic output guarantee.** The LLM influences only the **intent** stage (Stage 1 in `gspl-agent.md`). Every gene, every developmental stage, and every final `.gseed` is produced by the deterministic kernel + engines. Re-running the same prompt with the same RNG seed produces bit-identical output; re-running the same prompt with a different seed produces a variant, not a different definition.
3. **Typed internet access.** The Researcher sub-agent can fetch web content, but every fetch is recorded in the lineage as a typed `dimensional` gene with provenance, timestamp, and content hash — not as free-form LLM context. The substrate remains auditable.
4. **Full capacity, sandboxed.** Internet, code execution, filesystem, evolution runners, multimodal analysis, and arbitrary tool use are all available — and all run inside sandboxes with typed inputs and typed outputs.
5. **Self-bootstrapping closed loop.** The Agent improves itself using only GSPL's own genetic substrate. No external data poisoning. Every training example is a validated seed from `seed-commons/` with a deterministic proof-of-validity.
6. **Air-gap mode.** Every tool is optional. The Agent must run with all tools disabled — producing valid GSPL from the local `seed-commons/` alone — on a completely disconnected machine.

## 2. Architecture overview

```
┌────────────────────────────────────────────────────────────────────────┐
│                           Full-Capacity Agent                          │
│                                                                        │
│  Stage 0: Live context ingestion    (Researcher, optional)             │
│  Stage 1: Intent resolution         (IntentOracle + Researcher)        │
│  Stage 2: GSPL code generation      (CodeSmith)                        │
│  Stage 3: Deterministic growth      (kernel + engine readers)          │
│  Stage 4: Validation                (Validator)                        │
│  Stage 5: Evolution & composition   (Evolver + Composer, optional)     │
│  Stage 6: Archival & signing        (MemoryArchivist + SovereignSigner)│
│                                                                        │
│  Tool layer (all optional, all sandboxed, all typed)                   │
└────────────────────────────────────────────────────────────────────────┘
```

The stages are a strict superset of the 5-stage Concept-to-Seed pipeline in `gspl-agent.md`. Stage 0 and Stage 6 are the new endpoints; Stages 1–5 are refined versions of the base spec's stages.

## 3. Sub-agents (8, with tool-use privileges)

These extend the 8 sub-agents defined in `intelligence/8-sub-agents.md`. Only the tool-use column is new.

| # | Sub-agent | Model type | Tools it may call |
|---|---|---|---|
| 1 | IntentOracle | Any LLM (pluggable) | `seed_inventory_query`, `fetch_real_world_data` (via Researcher) |
| 2 | Researcher | Any LLM + tools | `web_search`, `browse_page`, `multimodal_analyze`, `fetch_real_world_data` |
| 3 | **CodeSmith** | Fine-tuned GSPL model | No tools — CodeSmith is code-generation only. This is the one sub-agent that writes `.gspl`. Tool-free for purity. |
| 4 | Validator | No LLM | `code_execution`, determinism diff |
| 5 | Evolver | No LLM | `evolution_run` (MAP-Elites, CMA-ES, Novelty, POET, DQD) |
| 6 | Composer | Any LLM | `seed_inventory_query` |
| 7 | MemoryArchivist | No LLM | filesystem (write into `seed-commons/inventories/`) |
| 8 | SovereignSigner | No LLM | crypto (ECDSA-P256, RFC 6979 deterministic) |

**Design rule:** Only Stages 0, 1, and 5's Composer may use LLMs. CodeSmith is fine-tuned and has no tool access. Validator, MemoryArchivist, and SovereignSigner are purely deterministic. The LLM's blast radius is strictly bounded to *intent*, *research*, and *composition suggestion* — never to gene emission.

## 4. Tool layer specification

Every tool takes typed inputs and returns typed outputs. Every tool is optional. Every tool records its invocation into the seed's lineage as a `dimensional` gene with provenance.

### 4.1 `web_search(query: string, num_results: int = 10) -> SearchResult[]`

- Wraps a search provider (SearXNG, Brave Search API, Kagi, etc.). Operator chooses.
- Returns `{ title, url, snippet, source_hash }[]`.
- Each result is hashed with SHA-256 at fetch time for later audit.
- Rate-limited only by the operator's search provider, not by the Agent.

### 4.2 `browse_page(url: string, instructions: string) -> PageSummary`

- Fetches and summarizes a web page.
- Returns `{ url, title, summary, full_text_hash, fetched_at }`.
- Respects robots.txt and rate-limits per the Agent's operator policy.

### 4.3 `code_execution(gspl_source: string, rng_seed: string) -> ExecutionReceipt`

- Runs the deterministic kernel in a sandbox (Wasm-isolated by default).
- Returns `{ render_hash, duration_ms, trace }`.
- Used by Validator to grow and re-grow seeds. Never allowed to touch the filesystem outside the sandbox.

### 4.4 `seed_inventory_query(category: string, tags: string[]) -> SeedId[]`

- Searches the local `seed-commons/` for matching seeds.
- Returns seed IDs + composition graph summaries.
- Pure filesystem + graph walk; no LLM.

### 4.5 `evolution_run(seed_ids: SeedId[], generations: int, algorithm: AlgorithmId) -> EvolutionResult`

- Launches MAP-Elites / CMA-ES / Novelty Search / DQD / POET per Brief 035–041.
- Returns `{ population, archive, fitness_curve, best_seed_ids }`.
- Pure and deterministic given the RNG seed.

### 4.6 `fetch_real_world_data(domain: string, query: object) -> DataPack`

- Pulls live data from registered domains: weather (NOAA), astronomy (JPL Horizons, TLE), science (arXiv), chemistry (PubChem), news (RSS), stocks, climate (Copernicus), etc.
- Returns typed data + content hash.
- Every domain connector is declared in `intelligence/data-sources.yaml` so operators can see exactly what the Agent may fetch.

### 4.7 `multimodal_analyze(url_or_path: string) -> MultimodalReport`

- Local multimodal model (LLaVA, Qwen-VL, or equivalent). Reads images, PDFs, audio, video.
- Returns `{ modality, description, salient_features, content_hash }`.
- Used by Researcher to ingest reference images when the user says "make something like this."

### 4.8 `self_fine_tune_trigger() -> TrainingJob`

- Triggers a local fine-tuning run on the accumulated validated-seed corpus.
- Returns `{ job_id, base_model, dataset_hash, eta }`.
- Requires the operator's explicit opt-in (training is CPU/GPU-heavy).

## 5. The six-stage pipeline (with Stage 0 and Stage 6)

### Stage 0 — Live context ingestion (optional)

If the prompt references real-world context ("make a seed based on today's climate data for Jakarta"), the Researcher sub-agent pulls live data via `fetch_real_world_data` and `web_search`. Results are hashed and attached to the intent envelope.

**Air-gap mode:** skip. Agent proceeds with Stage 1 using only the local commons.

### Stage 1 — Intent resolution

IntentOracle parses the user's natural-language prompt against the intent taxonomy (`intelligence/intent-taxonomy.md`) and runs the adjective normalizer (`intelligence/adjective-normalization.md`). Produces a structured JSON intent envelope:

```json
{
  "intent_id": "sprite.character.melancholy_bard",
  "domain": "sprite",
  "archetype": "humanoid.character.bard",
  "adjectives": [
    {"raw": "melancholy", "normalized": "mood.sadness.0.7"},
    {"raw": "wooden", "normalized": "material.wood.0.9"}
  ],
  "constraints": {
    "canvas": {"w": 1024, "h": 1024},
    "determinism": true,
    "is_fictional": true
  },
  "live_context": null
}
```

### Stage 2 — GSPL code generation (CodeSmith only)

CodeSmith takes the intent envelope and emits a `.gspl` source file. CodeSmith is trained exclusively on validated seeds from `seed-commons/` plus the full `spec/` directory, `language/grammar.ebnf`, and `language/stdlib.md`. It has never seen invalid GSPL, so its failure mode is "doesn't know how" rather than "hallucinates something broken."

Output: one `.gspl` source file, ready for Stage 3.

### Stage 3 — Deterministic growth

The kernel + the relevant engine readers grow the seed. Output: a candidate `.gseed.json` payload and a render artifact.

### Stage 4 — Validation

Validator runs:

1. `code_execution` twice with the same RNG seed → diff → must be byte-identical.
2. Re-canonicalize the payload via JCS and recompute the SHA-256 content hash → must match `$hash` in the payload.
3. Placeholder-sign the payload with a test key → verify → must pass.
4. Run the round-trip test: encode to `.gseed` binary → decode → canonicalize → hash → must match.
5. Run `commons-lint` against the 8-point contract checklist.

If any step fails, Validator returns the failure trace to CodeSmith with an explicit error code. CodeSmith retries up to 3 times; if all 3 fail, the run is escalated to Evolver for structural search.

### Stage 5 — Evolution & composition (optional)

If the user prompt asked for variations, breeding, or cross-domain fusion:

- Evolver runs MAP-Elites / CMA-ES / Novelty Search / DQD / POET over the candidate seed and its neighborhood in the commons.
- Composer proposes functor chains (`sprite → music`, `character → level`, etc.) from `seed-commons/inventories/cross-domain/`.

Every derived seed goes through Stage 3 and Stage 4 independently.

### Stage 6 — Archival & signing

MemoryArchivist writes the validated `.gspl` + `.gseed.json` into `seed-commons/inventories/<category>/<slug>.{gspl,gseed.json}`. SovereignSigner signs the payload with the operator's key (ECDSA-P256, RFC 6979 deterministic, SHA-256 over JCS canonical payload per `spec/05`). Lineage is updated.

If the operator has opted into Foundation submission, the archived pair is proposed as a PR to the Foundation's commons branch; the PR includes the agent's session lineage hash in `$metadata.agent_session`.

## 6. Self-bootstrapping closed loop

This is the compounding mechanism that turns the Agent into the undisputed best GSPL code generator on Earth.

### Phase A — Gold dataset creation (one-time bootstrap)

1. Ingest every validated seed in `seed-commons/` + `examples/` + `language/examples/`. This is the gold corpus.
2. Generate 10M+ synthetic prompts by parameterizing `intelligence/template-bridge.md` against `intelligence/intent-taxonomy.md`.
3. For each synthetic prompt:
   - Run the current Agent through Stages 1–4.
   - If Validator passes, store `(prompt, gold_gspl, seed_hash, render_proof)` as a training example.
   - If Validator fails, store `(prompt, broken_gspl, failure_trace)` as a *negative* training example (used for contrastive fine-tuning).
4. Deduplicate by seed hash. Strip PII. Canonicalize.

### Phase B — Continuous self-bootstrapping loop

```gspl
// pseudo-GSPL, runs on the Agent's own substrate
loop {
  new_prompts = researcher.generate_synthetic_prompts(1000);
  for each prompt in new_prompts {
    candidate = code_smith.generate_gspl(prompt);
    receipt = validator.validate(candidate);
    if (receipt.ok) {
      memory_archivist.archive_to_commons(candidate);
      training_corpus.add(prompt, candidate, receipt);
    } else {
      training_corpus.add_negative(prompt, candidate, receipt.trace);
    }
  }
  if (training_corpus.size() >= next_fine_tune_threshold) {
    self_fine_tune_trigger();
  }
}
```

### Phase C — Local fine-tuning stack

- **Base models:** Llama-3.3-70B, Mistral-Large, Qwen-2.5-72B, or any Ollama-compatible open-weights model. Operator chooses.
- **Method:** QLoRA (4-bit quantization + LoRA adapters) via Unsloth. Fits on a single 24 GB GPU for 7B–13B; on a single 80 GB H100 for 70B-class.
- **Dataset format:** ShareGPT-style conversations. System prompt includes the full GSPL grammar (`language/grammar.ebnf`), the 17 kernel gene types (`spec/02-gene-system.md`), and the sovereignty canonicalization rules (`spec/05-sovereignty.md`). Assistant turn is the `.gspl` source; user turn is the intent envelope.
- **Evaluation:** held-out set of 10,000 seeds from the commons that the model has never seen. Pass criteria: 100% Validator pass rate on first attempt.
- **Cadence:** triggered when the corpus grows by ≥ 50,000 validated examples or when the Validator pass rate on the held-out set drops below 98%.

### Phase D — Model governance

- Fine-tuned adapters are released as signed `.gseed` artifacts themselves (domain: `agent`, payload: LoRA weights + metadata). Users can federate the agent's weights the same way they federate seeds.
- No central model registry. Every operator chooses which adapter version to run. Foundation publishes reference adapters; federation peers publish their own.
- Every adapter carries its training corpus hash so users can verify provenance.

## 7. Integration with `seed-commons/`

The Agent is now the **primary population engine** for the commons.

- On first run against a fresh `seed-commons/`, the Agent auto-generates bootstrap foundational seeds for every inventory category using the Round 4 libraries (`seed-commons/libraries/*.gspl`) as grounding.
- Daily, the Agent runs evolutionary expansion loops that add novel seeds to each inventory category under strict quality gates.
- On user request ("populate the narrative inventory with 200 canonical story seeds grounded in Brief 086D linguistics and Brief 086E culture"), the Researcher pulls relevant real-world narrative theory, CodeSmith emits the seeds, Validator certifies each one, MemoryArchivist files them under `seed-commons/inventories/scene/` with full lineage.

Every seed the Agent contributes carries `provenance: fully_agentic` or `agent_assisted` in its `.gseed.json` payload and a back-reference to the agent session that produced it.

## 8. Sovereignty, license, and provenance guarantees

- **Every Agent-produced seed is signed** with the operator's key under ECDSA-P256 RFC 6979 + SHA-256 over JCS canonical payload. No exceptions. No placeholder signatures in production.
- **Every Agent tool invocation is recorded** in the seed's lineage as a `dimensional` gene. An auditor can reconstruct exactly which web pages, which real-world data, and which commons seeds the Agent consulted.
- **No Agent seed may claim human authorship.** `provenance` must honestly declare `fully_agentic` or `agent_assisted`. This is a hard contract enforced by `commons-lint`.
- **License on Agent-produced seeds defaults to CC-BY-4.0** (or whatever the operator configures). The GSPL Open Specification License covers the substrate; individual seeds carry their own content licenses.

## 9. Implementation roadmap (90 days to full capacity)

| Weeks | Milestone | Deliverables |
|---|---|---|
| 1–2 | Tool layer + sub-agent harness | `intelligence/tool-layer.md`, TypeScript stubs for all 8 tools, CodeSmith/Researcher/Validator as live processes |
| 3–4 | Self-bootstrapping loop | `intelligence/self-bootstrapping-loop.md`, the closed-loop runner, corpus persistence |
| 5–6 | Local fine-tuning pipeline | `intelligence/local-fine-tune.md`, QLoRA recipes, evaluation harness |
| 7–8 | First commons auto-population pass | Agent generates and validates the first 500 missing seeds across 20 categories |
| 9–10 | Cross-engine parity validation | Brief 196 fixtures run against agent-produced seeds; 100% pass required |
| 11–12 | Studio integration | Agent available as the default GSPL assistant inside the MVP studio (P0-3 in `STRATEGIC_GAP_AUDIT.md`) |

## 10. Success metrics

The Agent is at full capacity when all five hold:

1. **Any natural-language request returns a fully signed, breedable, royalty-ready UniversalSeed in under 60 seconds on consumer hardware.**
2. **Zero external service dependencies.** The Agent runs end-to-end on a disconnected laptop with only the local commons and a local model.
3. **`seed-commons/` grows by ≥ 1,000 validated seeds per day** under a single running instance, without human intervention.
4. **First-try Validator pass rate ≥ 99.5%** on held-out prompts after the third fine-tuning cycle.
5. **Determinism parity** — any seed produced by the Agent, when re-grown by any compliant kernel + engine reader, produces bit-identical output.

## 11. What this agent is not

- It is not a generic coding assistant. CodeSmith writes only `.gspl`.
- It is not a cloud service. There is no Agent API hosted by the Foundation. Every operator runs their own.
- It is not authoritative over the commons. Every Agent-produced seed goes through the same validation and curation pipeline as a human PR.
- It is not a replacement for human curation. The Foundation's curation board retains the final say on what enters the Foundation-signed commons. The Agent accelerates, not decides.
- It is not allowed to mutate sovereignty genes. The sovereignty gene is forbidden from mutation and crossover per `spec/02-gene-system.md`; the Agent inherits that prohibition.

## 12. Open follow-ups

- `intelligence/tool-layer.md` — the detailed tool definitions with request/response JSON schemas.
- `intelligence/self-bootstrapping-loop.md` — the loop runner, corpus layout, negative-example handling.
- `intelligence/local-fine-tune.md` — the QLoRA recipe, base-model selection rubric, evaluation harness.
- `intelligence/data-sources.yaml` — declared real-world data connectors.
- `adr/00NN-full-capacity-agent.md` — the ADR that accepts this spec into the substrate's authority layer.

## 13. Why this spec is the 5T engine

Every other creative platform treats its AI assistant as a feature layered on top of a closed product. Paradigm treats the Agent as a first-class substrate citizen that runs locally, improves itself, and populates the commons while honoring the same determinism and sovereignty guarantees that bind every other seed.

The result is a compounding loop no competitor can copy without also reinventing the determinism substrate, the 17-gene kernel, the sovereignty propagation system, and the seed commons — in that order. That is the moat. This spec activates it.
