# 027 — The 11 planned engines: feasibility and priority matrix

## Question
Beyond the 15 engines covered in Briefs 021-026 (humanoid 3, sound 2, interactive 3, visual 3, simulation 3, UI 1) GSPL has reserved space for 11 additional planned engines. What are they, in what order should they be built, and which can be deferred without harming the v1 promise?

## Why it matters
Scope discipline. A solo founder building 26 engines simultaneously ships none. The priority matrix decides which 4-6 engines launch with v1, which are Phase 2, and which are reserved for Phase 3+. Deferring an engine is fine; *promising* an engine GSPL can't deliver in v1 is a credibility leak.

## What we know from the spec
- The 26-engine roster is mentioned in the README and `architecture/cross-domain-composition.md`.
- 15 engines are covered in detail in Briefs 021-026.
- The remaining 11 are listed below.

## The 11 planned engines

Drawn from the README's roster minus the 15 already covered:

1. **WorldEngine** — large-scale world generation (continents, climates, biomes at planetary scale). Differs from EcosystemEngine: world is the *substrate*, ecosystem is the *inhabitants*.
2. **VFXEngine** — particle systems, shaders, post-processing chains. Differs from Visual2D and Procedural: VFX is *temporal* and *systemic*.
3. **VideoEngine** — temporal sequences of generated frames. Bridges Visual2D outputs into edited videos with cuts, transitions, motion.
4. **DialogueEngine** — branching dialogue trees with persona-aware lines. Differs from Narrative: Narrative is *structure*, Dialogue is *line-level*.
5. **EconomyEngine** — in-game economies: currencies, sinks, sources, prices, inflation. RuleGene-heavy.
6. **AIEngine** — non-trivial NPC/agent AI: planners, behavior trees, learned controllers. Differs from BehaviorGene-as-a-type: AIEngine is the *production* engine for whole agents.
7. **InputEngine** — input mappings, gesture recognizers, control schemes. Differs from UI: input is the *bridge* between user and game state.
8. **NetworkingEngine** — multiplayer protocols, sync strategies, lobby systems. Likely the most decoupled engine.
9. **AnalyticsEngine** — telemetry schemas and dashboards generated alongside a game/product. Meta-engine.
10. **ToolsEngine** — content tools (level editors, asset browsers) generated for a project. Meta-engine.
11. **DocsEngine** — documentation, tutorials, onboarding flows generated for a project. Meta-engine.

## Feasibility and priority matrix

| Engine | Tier | Feasibility | Composition leverage | v1 ship? | Notes |
|---|---|---|---|---|---|
| WorldEngine | Simulation | High | High (biomes feed Ecosystem, Procedural) | **Yes** | Spatial primitive most other engines need |
| VFXEngine | Visual | High | High (every Game wants VFX) | **Yes** | Builds cleanly on Procedural |
| VideoEngine | Visual | Medium | Medium | Phase 2 | Requires temporal coherence story |
| DialogueEngine | Interactive | Medium | High (Narrative + Game both need it) | **Yes** | Tight scope: branching only, no NLG |
| EconomyEngine | Interactive | Medium | Medium (FullGame needs it) | Phase 2 | RuleGene-heavy, cleanly extends Game |
| AIEngine | Interactive | Low | High | Phase 2 | Hard problem; v1 uses BehaviorGene |
| InputEngine | UI/Interactive | High | High | **Yes** | Trivial schema, immediate value |
| NetworkingEngine | Infra | Low | Low for v1 (offline-first) | Phase 3 | Defer; offline use is enough |
| AnalyticsEngine | Meta | Medium | Low | Phase 3 | Defer; not critical to creative loop |
| ToolsEngine | Meta | Low | Low | Phase 3 | Defer; bootstrapping complexity |
| DocsEngine | Meta | High | Medium | Phase 2 | Cheap to build, useful for marketplace |

**Feasibility rubric:**
- High = the engine can be built in ≤ 4 weeks by a solo founder, leveraging existing libraries.
- Medium = 4-12 weeks; nontrivial but bounded.
- Low = research-grade or 3+ months of work.

**Composition leverage rubric:**
- High = many other engines need this one; absence forces ugly workarounds.
- Medium = some engines benefit; absence is annoying but not blocking.
- Low = standalone or downstream; defer-friendly.

## v1 final engine roster (proposed)

Counting the 15 from Briefs 021-026 plus the four "Yes" rows here (World, VFX, Dialogue, Input), v1 ships **19 engines**. This is ambitious but achievable because most v1 engines are *thin schemas + a single reference renderer + the export pipeline*, not full studio products.

Phase 2 adds Video, Economy, AI, Docs (23 engines).

Phase 3 adds Networking, Analytics, Tools (26 engines, complete roster).

## Risks identified

- **19 engines at v1 is still a lot for a solo founder.** Mitigation: each engine is mostly a schema + the universal kernel + a small reference renderer; the heavy code (kernel, evolution, proof, breeding) is shared.
- **DialogueEngine NLG temptation**: it would be easy to scope-creep into "generate the actual lines with an LLM." Resist; v1 dialogue is *structural* (branching tree of placeholders), not generative.
- **NetworkingEngine deferral may bite if multiplayer becomes a marketplace ask**. Mitigation: ship a Phase 3 commitment with a clear scope, and design the runtime spec format to be network-neutral so it can be wrapped later.
- **AIEngine Phase 2 means v1 game NPCs are dumb**. Mitigation: BehaviorGene + RuleGene at v1 can produce credible NPCs for arcade/puzzle/roguelike scopes; smarter NPCs land in Phase 2.

## Recommendation

1. **v1 ships 19 engines**: 15 from Briefs 021-026 + WorldEngine, VFXEngine, DialogueEngine, InputEngine.
2. **Phase 2 adds 4 more** (Video, Economy, AI, Docs) for 23 total.
3. **Phase 3 adds the final 3** (Networking, Analytics, Tools) for the full 26.
4. **Engine briefs for the 11 follow the same pattern as 021-026**: schema, IR, pipeline, cross-engine bindings, risks, recommendation. Briefs to be written as each engine enters its build phase.
5. **Marketing communicates the staged roster honestly**: "26 engines planned, 19 at v1." No hand-waving.
6. **Each engine's v1 schema is intentionally minimal** to fit the solo-founder budget; expansion is via post-v1 ADRs.

## Confidence
**4/5.** The engine count and feasibility ratings are based on direct experience with the existing 182K-LOC codebase and Sprite Forge. The 4/5 reflects the unmeasured difficulty of integrating 19 schemas with the breeding system simultaneously.

## Spec impact

- `architecture/engine-roster.md` — embed the matrix as the normative roster.
- `engines/world.md`, `vfx.md`, `dialogue.md`, `input.md` — write v1 schemas (Phase 1 task; sketches in this brief).
- New ADR: `adr/00NN-engine-roster-and-phasing.md`.

## Open follow-ups

- Write the four v1 schema briefs for World, VFX, Dialogue, Input as Phase 1 deliverables.
- Decide whether DialogueEngine v1 supports localization slots (recommended: yes, as TextGene with locale tags).
- Validate WorldEngine spatial scale assumptions against existing world-generation libraries (e.g., libnoise, FastNoise2).
- Re-evaluate Phase 3 deferrals after v1 ships and user demand is measured.

## Sources

- Internal: README engine roster, Briefs 021-026.
- Existing 182K-LOC codebase (engine prototypes).
