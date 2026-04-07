# Intelligence Layer

Layer 6 — the Intelligence layer — is the bridge between *human intent expressed in natural language* and *deterministic seeds the platform can grow*. It sits above the deterministic substrate and below the Studio. Its single responsibility is: **convert ambiguous prompts into validated, signed UniversalSeeds that the Layer 4 engines can immediately consume.**

This document specifies the GSPL Agent (the orchestration entity), its 5-stage pipeline, the 8 sub-agents, the 4-layer memory system, the Template Bridge, and the multi-provider LLM abstraction.

## Why a Separate Layer

Layers 1–5 are deterministic. Determinism is the load-bearing wall of the entire economic model (see [`spec/07-determinism.md`](../spec/07-determinism.md)). LLMs are not deterministic and will never be — even at temperature zero, model providers update weights and rerouting changes outputs.

Putting the LLM **inside** an engine (e.g., having a "smart" character engine that asks GPT-4 to invent personality traits) would contaminate the determinism boundary. Instead, the LLM lives in Layer 6, where its only output is a **seed**. Once the seed is created, hashed, and signed, all downstream operations (growing, mutation, evolution, breeding) are bit-deterministic regardless of which LLM produced the seed.

This is why the GSPL language (Layer 3) and the GSPL Agent (Layer 6) are *peers*. Both produce seeds; they just take different inputs.

## The 5-Stage Concept-to-Seed Pipeline

```
User text          ┌───────────┐
"menacing       →  │ 1. Parse  │
 iron warrior"     └─────┬─────┘
                         ▼
                   ┌───────────┐
                   │ 2. Resolve│  ← Template Bridge, Memory
                   └─────┬─────┘
                         ▼
                   ┌───────────┐
                   │ 3. Plan   │  ← Sub-agent dispatch
                   └─────┬─────┘
                         ▼
                   ┌───────────┐
                   │ 4. Assemble │
                   └─────┬─────┘
                         ▼
                   ┌───────────┐
                   │ 5. Validate │
                   └─────┬─────┘
                         ▼
                   UniversalSeed
                   (signed, hashed)
```

### Stage 1 — Parse Intent

Tokenize the user prompt and extract:

- **Domain hints.** "warrior" → character; "song" → music; "level" → fullgame.
- **Modifiers.** Adjectives, adverbs, comparative phrases.
- **Constraints.** "must be playable", "under 60 seconds", "compatible with Godot".
- **Reference to existing seeds.** "like the one I made yesterday" → look up by recency.
- **Polarity.** "menacing" vs "friendly" → personality vector signs.

Output: a `ParsedIntent` struct with normalized fields. This stage uses an LLM call but the result is structured (JSON schema-validated), not free-form text.

### Stage 2 — Resolve Domain and Archetype

Given a parsed intent, look up the most appropriate domain in the **Template Bridge**:

```ts
interface TemplateBridge {
  archetypes: Map<string, Archetype>;       // 26+ archetypes per domain
  resolve(intent: ParsedIntent): ResolvedTemplate;
}

interface Archetype {
  domain: Domain;
  name: string;                              // "warrior", "rogue", "mage", ...
  baseGenes: Partial<GeneTable>;             // sensible defaults
  modifierSlots: ModifierSlot[];             // where adjectives plug in
}
```

The bridge ships with 26+ archetypes per domain. "Warrior" maps to character/warrior with default genes that produce a recognizable warrior; the user's specific adjectives then refine those defaults.

If no archetype matches, the bridge falls back to a domain-default seed and lets the modifiers do all the work.

### Stage 3 — Plan Sub-agent Dispatch

The pipeline routes specialized work to **8 sub-agents**, each focused on one cognitive task:

| Sub-agent | Job |
|---|---|
| **VisionAgent** | Resolve visual descriptors (color, shape, silhouette) into gene values |
| **PersonalityAgent** | Resolve emotional/behavioral descriptors into personality vectors |
| **MusicTheoryAgent** | Resolve musical descriptors (mood, key, tempo) into music genes |
| **MechanicsAgent** | Resolve game mechanic descriptors into FullGame seed structure |
| **NarrativeAgent** | Resolve story descriptors into narrative/character relations |
| **PhysicsAgent** | Resolve physics descriptors into simulation parameters |
| **StyleAgent** | Project style descriptors onto the dimensional embedding space |
| **CritiqueAgent** | Review the assembled seed for coherence and flag issues |

Each sub-agent is a small LLM call with a tight system prompt and a structured output schema. Sub-agents run in parallel when their inputs don't depend on each other.

### Stage 4 — Assemble Seed

Combine the archetype's base genes with the sub-agent outputs into a candidate `UniversalSeed`. This stage is *pure code*, no LLM involved — it's a structured merge of typed gene values into the schema. The merge order matters and is documented per domain.

After merging, the seed is canonicalized and hashed.

### Stage 5 — Validate, Critique, Sign

Run the candidate seed through:

1. **Schema validation.** All required genes present, all values in range, all types correct.
2. **Engine-specific validation.** Call `engine.validate(seed)` to check engine-internal invariants.
3. **CritiqueAgent review.** A final LLM pass that flags incoherence ("you asked for a friendly warrior but the personality has high aggression") with a confidence score.
4. **Signing.** Apply the user's identity key (or the platform's default if none).

If validation fails, the pipeline either *retries* (re-running Stages 3–4 with corrective context) or *bails* with a structured error the Studio can show.

The output is a fully-validated, signed seed ready for `engine.grow`.

## The 4-Layer Memory System

The agent maintains four layers of memory, each with different scope and persistence:

### Memory Layer 1 — Working Memory

Per-conversation. Holds the current parsed intent, the recent prompts in the session, the seeds generated this session. Cleared on session end.

### Memory Layer 2 — User Profile

Per-user, persistent. Holds:

- Style preferences extracted from past creations.
- Frequently-used archetypes.
- Custom vocabulary the user has defined ("when I say 'epic' I mean these specific gene biases").
- Identity keypair for signing.

### Memory Layer 3 — Project Context

Per-project, persistent. Holds:

- The set of seeds in the project.
- Cross-references between seeds (this character is in this story, this music is for this level).
- Project-wide style constraints.
- Naming conventions.

### Memory Layer 4 — Global Knowledge

Shared across all users. Holds:

- The Template Bridge archetype catalog.
- Verified high-quality seeds from the marketplace (used as few-shot examples).
- Domain knowledge documents (color theory, music theory, game design patterns).

Each layer has its own retrieval interface — Layer 1 is in-RAM, Layer 2 is per-user SQLite, Layer 3 is per-project SQLite, Layer 4 is a Qdrant vector store. Sub-agents query the appropriate layer(s) when constructing their LLM prompts.

## Adjective Normalization

The single hardest problem in Stage 1 is mapping fuzzy adjectives ("menacing", "epic", "cute", "ethereal") onto gene-space coordinates. The intelligence layer handles this with a two-step process:

1. **Lookup.** Each adjective has a normalized entry in the **adjective dictionary** that lists which gene types it influences and in which direction (e.g., "menacing" → personality.aggression += 0.7, color.saturation -= 0.2, lighting.contrast += 0.4).
2. **LLM fallback.** If the adjective isn't in the dictionary, an LLM call infers the closest entry plus a confidence score. New high-confidence inferences get added to the dictionary for future use, building up shared vocabulary over time.

The dictionary is part of Memory Layer 4 and is versioned. Users can override entries in their own Layer 2 profile.

## The Template Bridge

The Template Bridge is the single most important Layer 6 asset. Without it, every prompt would have to fully specify a seed from scratch and the agent would essentially be a code generator. With it, the agent can produce a strong default seed from a single noun and refine it with adjectives — making the user experience feel like "describe and watch."

A Template Bridge entry has:

```ts
interface ArchetypeTemplate {
  name: string;                          // "warrior"
  domain: Domain;                        // "character"
  description: string;                   // human-readable
  baseGenes: GeneTable;                  // pre-filled genes
  modifierTaxonomy: Map<string, ModifierEffect>;  // which adjectives apply
  exampleSeeds: SeedHash[];              // few-shot examples for the LLM
  successRate: number;                   // tracked over time
}
```

The 26+ archetypes per domain are seeded from the curated catalog (warrior, mage, rogue, paladin, ranger, monk, etc. for character; orchestra, rock band, EDM, jazz, etc. for music; platformer, RPG, puzzle, racer, etc. for fullgame).

New archetypes can be added by:

- Curators contributing to the open catalog.
- Users opting into "elevate this seed to an archetype" when one of their creations performs well.
- Auto-discovery: if many users prompt the same description that produces similar seeds, the system proposes a new archetype.

## Multi-Provider LLM Abstraction

The intelligence layer can be configured with one or more LLM providers:

```ts
interface LlmProvider {
  readonly name: string;                 // "anthropic" | "openai" | "gemini" | "ollama"
  complete(prompt: Prompt, schema: JsonSchema): Promise<StructuredResult>;
}
```

The orchestrator picks providers based on:

1. **Cost vs latency tradeoffs.** Cheap local models (Ollama) for simple tasks, frontier models for complex critiques.
2. **User preference.** A user can pin "I want all my work to use Claude" in their profile.
3. **Privacy.** Sensitive prompts can be routed to a local Ollama-only path.
4. **Fallback.** If the primary provider is rate-limited, the orchestrator retries on a backup.

Crucially, the LLM provider is recorded in the seed's `$metadata.provenance` field but **does not affect the seed's `$hash`**. Two users on different LLMs can produce semantically identical seeds whose hashes are the same. This is what makes the LLM contamination not propagate downstream.

## Determinism Boundary

The intelligence layer is the **only** layer where non-determinism is allowed, and even there it's contained:

- LLM calls are non-deterministic. Their outputs are captured at the seed-creation boundary.
- Once a seed exists, all further work is deterministic.
- A user replaying a seed gets the same artifact, regardless of which LLM (or even *whether* an LLM) was used to create it originally.

To "replay" an LLM-driven creation, the user replays the **seed**, not the **prompt**. This is a fundamental shift from how generative AI is normally framed: in Paradigm, the prompt is a transient input but the seed is the canonical, durable artifact.

## API Surface

```ts
interface IntelligenceLayer {
  parseIntent(text: string, ctx: AgentContext): Promise<ParsedIntent>;
  intentToSeed(intent: ParsedIntent, ctx: AgentContext): Promise<UniversalSeed>;
  agentStep(state: AgentState): Promise<AgentState>;        // for multi-turn
  llm: LlmProviderRegistry;
  memory: MemorySystem;
  templates: TemplateBridge;
}
```

This is the surface the Studio (Layer 7) consumes. The Studio never sees an LLM directly; it only sees the agent.

## Worked Example

User types: **"a melancholy bard who plays a harp in a forgotten cathedral"**

```
1. Parse:
   ParsedIntent {
     primary_domain: "character",
     secondary_domains: ["music", "architecture"],
     archetype_hint: "bard",
     modifiers: ["melancholy"],
     props: ["harp"],
     setting: "forgotten cathedral",
     constraints: [],
   }

2. Resolve:
   archetype = templates.resolve({domain: "character", name: "bard"})
   → returns the 'bard' archetype with default genes

3. Plan:
   Dispatch:
     - PersonalityAgent("melancholy") → personality.warmth=0.3, personality.melancholy=0.9, personality.aggression=0.1
     - VisionAgent("bard with harp in forgotten cathedral") → outfit, color palette, posture, props
     - MusicTheoryAgent("melancholy bard harp") → minor mode, slow tempo, harp instrument set (held for later cross-domain compose)
     - StyleAgent("forgotten cathedral") → dimensional embedding shift toward "gothic, mossy, abandoned"

4. Assemble:
   character_seed = merge(archetype.baseGenes, agent_outputs)
   character_seed.$hash = sha256(canonicalize(character_seed))

5. Validate:
   characterEngine.validate(character_seed) → OK
   CritiqueAgent.review(character_seed) → coherence: 0.91, no issues
   Sign with user key.
   → Return character_seed
```

The user can now grow it, evolve it, breed it, or (since the MusicTheoryAgent already prepared a music seed inline) use the `character → music` functor to materialize the harp theme as a separate seed in the same compose action.

## Why This Design Works

1. **Determinism is preserved.** The LLM contamination is captured at one boundary (Stage 5 output) and never crosses below Layer 6.
2. **Non-deterministic creativity is valuable.** The LLM lets users describe in natural language; the deterministic substrate makes the result auditable, replayable, and tradable.
3. **The intelligence layer can be replaced.** A user could swap in their own LLM stack, their own template bridge, even their own sub-agents — as long as they conform to the interface, the rest of the platform doesn't need to know.
4. **Memory accumulates value.** Every successful seed expands the archetype catalog and the adjective dictionary, making the next user's prompts succeed more often. This is the "active intelligence bridge" at the heart of the product.
