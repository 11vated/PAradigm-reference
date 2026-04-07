# The 8 Specialized Sub-Agents

## What they do

The GSPL Agent's main pipeline (Parse → Resolve → Plan → Assemble → Validate) is supported by **8 specialized sub-agents**, each an expert in one creative domain. Sub-agents are invoked by the main pipeline (especially in Stages 2 and 3) to provide domain-specific reasoning that a generic LLM call cannot reliably produce.

Each sub-agent has its own system prompt, its own tool set, its own retrieval index over Layer 4 memory, and its own quality gate.

## The roster

| # | Agent | Domain | When invoked |
|---|---|---|---|
| 1 | **VisionAgent** | Visual aesthetics | Whenever the concept involves appearance, style, color, form |
| 2 | **PersonalityAgent** | Character psychology | Whenever the concept involves a character with traits |
| 3 | **MusicTheoryAgent** | Music theory | Whenever the concept involves music, sound, tempo, mood-as-audio |
| 4 | **MechanicsAgent** | Game mechanics | Whenever the concept involves rules, gameplay, win conditions |
| 5 | **NarrativeAgent** | Storytelling | Whenever the concept involves plot, dialogue, lore |
| 6 | **PhysicsAgent** | Physical realism | Whenever the concept involves motion, forces, materials |
| 7 | **StyleAgent** | Artistic style | Whenever the concept references a specific style or era |
| 8 | **CritiqueAgent** | Quality review | Always, in Stage 5 |

## VisionAgent

**Specialty:** Reasoning about visual aesthetics — composition, color theory, lighting, silhouette, contrast, focal point.

**Tools:**
- `lookup_color_palette(mood: string) -> Palette` — retrieves a curated palette for a mood from Layer 4 memory.
- `validate_contrast(palette: Palette) -> ContrastReport` — checks WCAG and aesthetic contrast.
- `suggest_composition(subject: string, setting: string) -> CompositionRule` — picks a rule of thirds / golden ratio / centered composition.

**Output:** A `VisionPlan` with palette IDs, lighting rig type, composition rule, and silhouette guidelines that the Sprite or Character engine can consume.

**Provider:** Claude Opus or GPT-4o (creative tasks).

## PersonalityAgent

**Specialty:** Mapping personality words and archetypes onto the character gene schema.

**Tools:**
- `lookup_archetype(name: string) -> Archetype` — retrieves a Big Five + Jungian archetype profile.
- `compose_archetypes(a: Archetype, b: Archetype, weights: [float; 2]) -> Archetype` — blends two archetypes.
- `validate_personality_coherence(profile: Personality) -> CoherenceReport` — flags contradictions like "warm + cruel + compassionate".

**Output:** A `PersonalityProfile` with Big Five values, dominant archetype, voice characteristics, and behavior tendencies.

**Provider:** Claude Sonnet (cheaper, sufficient).

## MusicTheoryAgent

**Specialty:** Theory-grounded music construction — keys, modes, tempo, time signature, harmonic progression, instrumentation.

**Tools:**
- `mood_to_key(mood: string) -> KeyAndMode` — e.g., "melancholy" → D minor, Aeolian.
- `mood_to_tempo(mood: string, energy: float) -> BPM` — e.g., "melancholy + calm" → 56 BPM.
- `instrument_for_setting(setting: string, era: string) -> [Instrument]` — looks up culturally appropriate instruments.
- `validate_progression(chords: [Chord], key: Key) -> bool` — checks that a chord progression is in-key.

**Output:** A `MusicSpec` with key, tempo, time signature, instrumentation list, and a starting chord progression.

**Provider:** GPT-4o or Claude Sonnet, with retrieval over a music theory knowledge base.

## MechanicsAgent

**Specialty:** Game mechanics design — rule sets, win conditions, progression systems, balance, difficulty curves.

**Tools:**
- `lookup_mechanic_pattern(name: string) -> MechanicTemplate` — retrieves patterns like "platformer", "deck-builder", "match-3".
- `compose_mechanics(a: MechanicTemplate, b: MechanicTemplate) -> MechanicTemplate` — blends two patterns.
- `simulate_play(mechanic: MechanicTemplate, n_runs: int) -> PlayabilityReport` — quick playability check (depth-limited tree search).

**Output:** A `MechanicsSpec` with the rule set, win condition, difficulty curve parameters, and any reference games.

**Provider:** Claude Opus (highest reasoning required).

## NarrativeAgent

**Specialty:** Plot structure, character motivation, dialogue style, lore consistency.

**Tools:**
- `lookup_story_template(genre: string) -> Template` — Hero's Journey, Three-Act, Kishōtenketsu, etc.
- `generate_motivation(character: PersonalityProfile, setting: string) -> Motivation` — produces a goal + obstacle.
- `validate_lore_consistency(facts: [Fact]) -> ConsistencyReport`

**Output:** A `NarrativeSpec` with a logline, character motivations, and a 3-5 beat plot outline.

**Provider:** GPT-4o or Claude Opus.

## PhysicsAgent

**Specialty:** Reasoning about physical plausibility — masses, joint limits, friction, gravity, material properties.

**Tools:**
- `lookup_material(name: string) -> MaterialProperties` — density, friction, elasticity, etc.
- `validate_morphology(creature: Skeleton) -> ViabilityReport` — flags impossible bone proportions or center-of-mass issues.
- `suggest_gait(skeleton: Skeleton, terrain: Terrain) -> Gait` — picks a viable locomotion pattern.

**Output:** A `PhysicsSpec` with gravity setting, material assignments, joint constraints, and gait parameters.

**Provider:** Claude Opus (technical reasoning).

## StyleAgent

**Specialty:** Recognizing and applying named artistic styles — "Studio Ghibli," "Mucha Art Nouveau," "VHS aesthetic," "Heian period scroll painting."

**Tools:**
- `lookup_style(name: string) -> StyleProfile` — retrieves a style's color palette, line weight, composition rules, era, references.
- `match_styles(target: string) -> [StyleProfile]` — fuzzy match user phrasing to known styles.
- `compose_styles(a: StyleProfile, b: StyleProfile, weight: float) -> StyleProfile`

**Output:** A `StyleSpec` ID that propagates through every visual sub-engine.

**Provider:** Claude Sonnet with retrieval over an art-history corpus.

## CritiqueAgent

**Specialty:** Reviewing the output of any other agent for problems before it leaves the pipeline.

**Tools:**
- `check_internal_consistency(spec: AnySpec) -> CritiqueReport`
- `check_against_concept(spec: AnySpec, original_concept: string) -> AlignmentReport`
- `check_quality_axes(seed: Seed) -> QualityVector` — runs the full QualityVector evaluation.

**Output:** A `Critique` with severity-rated issues. If any issue is severity ≥ Major, the calling stage retries with the critique appended.

**Provider:** Claude Opus or GPT-4o.

## Coordination

The main GSPL Agent dispatches sub-agents in parallel when their concerns are independent:

```
fn resolve_stage(parsed: ParsedIntent) -> ResolvedSpec:
    let domains = parsed.primary_domain :: parsed.secondary_domains
    let mut futures = []
    if "Character" in domains:
        futures.push(spawn(PersonalityAgent::run(parsed)))
    if "Music" in domains:
        futures.push(spawn(MusicTheoryAgent::run(parsed)))
    if "Game" in domains or "FullGame" in domains:
        futures.push(spawn(MechanicsAgent::run(parsed)))
    // VisionAgent and StyleAgent always run
    futures.push(spawn(VisionAgent::run(parsed)))
    futures.push(spawn(StyleAgent::run(parsed)))
    let results = await_all(futures)
    let merged = merge_specs(results)
    let critique = CritiqueAgent::review(merged, parsed)
    if critique.has_blocking_issues():
        return retry_with_critique(parsed, critique)
    return merged
```

Sub-agents share their tools' retrievals through a per-run scratchpad to avoid redundant API calls.

## Determinism notes

- Sub-agents are *not* deterministic individually — they make LLM calls.
- Their outputs are cached per `(input_hash, agent_version, model_version)`.
- The composition step (`merge_specs`) is deterministic.
- Once Stage 3's plan is committed, the rest of the pipeline is reproducible regardless of which sub-agents ran.

## Versioning

Each sub-agent has its own semver-tracked prompt, tool set, and memory index. Bumping any of these increments the agent's version, which invalidates the cache. Sub-agent versions are part of the seed's lineage metadata so we always know which agent constellation produced a given seed.
