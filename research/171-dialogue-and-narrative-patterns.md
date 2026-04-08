# 171 — Dialogue and narrative patterns

## Question

What canonical dialogue and narrative primitives does GSPL ship in `dialogue.*` and `narrative.*` so that any genre can adopt branching dialogue trees, Ink/Yarn-class typed graphs, voice integration, conditional content, and emergent storytelling by composition rather than from scratch, with localization-aware signed gseeds, replay determinism, and v0.1 reach?

## Why it matters (blast radius)

Dialogue is the dominant content surface for narrative games and an essential supplement for almost every other genre. Without typed dialogue primitives, every game reinvents branching trees, condition expressions, and voice/text/face-rig synchronization, breaking cross-game tooling for localization, accessibility, and authoring. Brief 170 (quests) triggers and resolves through dialogue, Brief 174 (HUD) renders dialogue choices, Brief 175 (audio) attaches voice, Brief 176 (cutscenes) often *is* dialogue, Brief 180 (editor) is the dialogue authoring surface, Brief 204 (narrative genre family) is dialogue-first, and Brief 220 (i18n) translates dialogue at scale.

## What we know from the spec

- Brief 153 — ECS substrate; speaker entities, conversation state are typed components
- Brief 158 — save/load; dialogue state and choice history saved
- Brief 159 — FSM/HFSM; dialogue is the canonical FSM consumer
- Brief 161 — animation; lip-sync and gesture cues bound to dialogue
- Brief 170 — quests; dialogue is the primary trigger and resolution layer
- Brief 175 — audio; voice clips attach to dialogue nodes
- Brief 220 — i18n; every dialogue string is a LocalKey

## Findings

1. **`dialogue.graph` as the root primitive.** A conversation is a typed signed gseed `dialogue.graph` containing: `graph_id`, `speakers: set<speaker_ref>`, `nodes: set<node_ref>`, `entry_node: node_ref`, `prerequisites: optional<predicate>`, `localization_set: LocalKey_set`, `signing_authority`. Graphs are typed gseeds; lineage tracks fork history. The runtime traverses the graph in response to player input or scripted advance.

2. **Five canonical node types.** Surveying Ink (inkle), Yarn Spinner, Twine, Witcher 3's REDscript dialogue, Mass Effect dialogue wheel, and Disco Elysium's skill-checked dialogue yields **five irreducible node types**: `dialogue.node.line`, `dialogue.node.choice`, `dialogue.node.condition`, `dialogue.node.action`, `dialogue.node.jump`. Every shipped dialogue system reduces to these five composed.

3. **`dialogue.node.line`.** A speaker line. Parameters: `node_id`, `speaker_ref`, `text: LocalKey`, `voice_clip_ref: optional<audio_ref>`, `face_rig_state: optional<rig_state_ref>`, `body_animation_ref: optional<clip_ref>`, `duration_ticks: optional<u32>`, `auto_advance_after_ticks: optional<u32>`, `next_node: node_ref`. Lines support parametric substitution via ICU MessageFormat (Brief 220) for player-name and dynamic context insertion.

4. **`dialogue.node.choice`.** Player decision point. Parameters: `node_id`, `choices: ordered_set<Choice>` where each Choice has `text: LocalKey`, `precondition: optional<predicate>`, `consequence_actions: set<action_ref>`, `next_node: node_ref`, `tags: set<TagId>` (e.g., `aggressive`, `flirt`, `lie`, `skill_check`), `skill_check: optional<SkillCheck>`. Choices can be hidden, grayed-out (precondition fails), or available; the runtime computes visibility from preconditions at node entry.

5. **`dialogue.node.condition`.** Branch on world state. Parameters: `node_id`, `branches: ordered_set<(predicate, next_node)>`, `else_branch: node_ref`. The runtime evaluates predicates in order; first true branch is taken. Used for "if player is wearing armor X, NPC reacts differently" — invisible to the player.

6. **`dialogue.node.action`.** Side-effect node. Parameters: `node_id`, `actions: set<ActionRef>`, `next_node: node_ref`. Actions are typed gseed references that mutate ECS state, advance quests (Brief 170), grant items (Brief 169), modify factions, apply status effects, etc. Actions are signed events in the per-tick Merkle batch.

7. **`dialogue.node.jump`.** Goto/return for graph reuse. Parameters: `node_id`, `target_graph: optional<graph_ref>`, `target_node: node_ref`, `push_return: bool`. Enables shared sub-conversations (e.g., a "tell me about the world" sub-graph reused by 5 NPCs). The runtime maintains a return stack with depth ≤ 8 (sign-time validated).

8. **Skill checks.** A `SkillCheck` is a typed parameter on a choice: `attribute_ref`, `difficulty: u8`, `roll_kind: enum{auto_pass, auto_fail, dice, threshold, hidden}`, `success_node: node_ref`, `failure_node: node_ref`, `partial_success_node: optional<node_ref>`. Disco Elysium's white/red check pattern is `roll_kind=dice`; Mass Effect's Paragon/Renegade gates are `roll_kind=threshold`. Dice rolls use sub-seeded PRNG (Brief 160) keyed on `(graph_id, node_id, player_id)` for replay determinism.

9. **Speakers.** A `speaker` is a typed gseed `dialogue.speaker` with: `speaker_id`, `display_name: LocalKey`, `portrait_ref: optional<image_ref>`, `voice_set_ref: optional<audio_set>`, `face_rig_ref: optional<rig_ref>`, `default_emotion: emotion_id`, `default_animation_ref: clip_ref`. Speakers are decoupled from world entities; one entity can play multiple speakers (a transformed character).

10. **Conversation state.** Each in-progress conversation is a typed component on the player entity with: `current_graph_ref`, `current_node_ref`, `return_stack: stack<node_ref>`, `seen_nodes: set<node_ref>`, `chosen_choices: set<choice_ref>`. Saved by Brief 158. Replays restore state and replay player choices from signed input events.

11. **Choice history.** The substrate maintains a per-player `dialogue.choice_log` keyed by `(graph_id, choice_id)` for the entire game lifetime. Future dialogue can read history (e.g., "remember when you said X 50 hours ago?") via predicate. This is the substrate-level memory primitive narrative games need; it composes with Brief 127's memory tier system for AI-driven dialogue augmentation later.

12. **Voice integration.** When `voice_clip_ref` is set on a line, audio runtime (Brief 175) plays the clip; line `duration_ticks` should match the clip length (validated at sign time). Lip-sync uses face rig states or auto-extracted phoneme tracks (v0.4+); v0.1 ships clip-only with optional manual face rig keyframes.

13. **Localization.** Every `text: LocalKey` is resolved through Brief 220's i18n pipeline. Voice clips are also locale-keyed: `voice_clip_ref` resolves to a different audio file per locale. The substrate refuses to sign a graph with missing localizations only if the creator opts in to "strict locale" mode; otherwise missing locales fall back to source language with a runtime warning.

14. **Narrative graph (`narrative.*`).** A wider companion namespace for *story-level* (not conversation-level) state: `narrative.beat` (story beat marker), `narrative.arc` (multi-quest story arc), `narrative.character_relationship` (per-pair relationship state), `narrative.world_state` (typed gseed of "what's true in the world right now"). Quests, dialogues, and cutscenes (Brief 176) advance narrative state through `narrative.advance` action references.

15. **Storylet primitive.** Optional `narrative.storylet`: a small content unit with preconditions, content, and post-state. Used by emergent narrative systems (Reigns, Cultist Simulator, Wildermyth). Storylets compose with the rest of `narrative.*` and are surfaced for v0.5 emergent narrative work (Brief 228) but the substrate ships the schema at v0.1.

16. **Replay determinism.** Dialogue is deterministic by construction: choice nodes wait for signed input, condition nodes are pure predicates, action nodes are signed events, skill check rolls use sub-seeded PRNG. Replays from save reconstruct identical conversations.

17. **v0.1 reach.** All 5 dialogue node types ship at v0.1. Skill checks ship. Choice history ship. Speaker primitives ship. Localization integration ships. Voice integration ships (clip-level only; auto lip-sync defers to v0.4). `narrative.*` companion primitives ship. Storylet schema ships, runtime gated to v0.5.

## Risks identified

1. **Graph size explodes for narrative games.** Disco Elysium has ~1M words. Mitigation: editor (Brief 180) supports sub-graph composition, fold/unfold visualization, and search; sign-time validation runs in chunks.

2. **Localization cost.** Every line × N locales = explosion. Mitigation: Brief 220 has machine-translation hooks with human-review tags; the substrate doesn't solve translation cost but exposes structured strings for optimal machine input.

3. **Skill check determinism in shared world.** Two clients in the same conversation could roll different dice. Mitigation: in v0.3+ multiplayer, dialogue is server-authoritative (Brief 210); v0.1 single-player, no problem.

4. **Cyclic jumps.** A jump-to-self creates infinite loops. Mitigation: sign-time validation tracks reachability and flags cycles; explicit cycles allowed only via the return stack with depth cap.

5. **Choice precondition dependency on uninstantiated state.** A choice referencing a quest that doesn't exist yet. Mitigation: sign-time predicate compilation against the project's typed gseed registry; broken refs fail to sign.

6. **Voice/text desync on locale switch.** Player switches language mid-conversation. Mitigation: substrate snapshots active locale at conversation start; switching locale takes effect on next conversation, not mid-conversation.

## Recommendation

Ship `dialogue.*` with `dialogue.graph` root, 5 canonical node types, signed skill check primitive, speaker decoupling, choice log memory, and ICU localization. Ship companion `narrative.*` with beat, arc, character relationship, world state, and storylet schemas. Wire to Brief 170 quests and Brief 175 audio at v0.1. Hold auto lip-sync and storylet runtime to v0.4-v0.5.

## Confidence

**4.5/5.** Dialogue primitives are extremely well-studied: Ink, Yarn, Twine, and 30+ years of CRPG dialogue design converge tightly on this decomposition. The only soft spot is the storylet/narrative.beat primitives, which are deferred runtime anyway.

## Spec impact

- Add `dialogue.*` namespace with graph + 5 node sub-types + speaker
- Add `narrative.*` namespace with beat, arc, character_relationship, world_state, storylet schemas
- Add `dialogue.choice_log` as substrate-level per-player memory primitive
- Cross-link to Brief 153 (conversation state component), Brief 158 (save), Brief 159 (FSM), Brief 160 (PRNG for skill checks), Brief 161 (face rig + body animation hooks), Brief 169 (action item grants), Brief 170 (quest action consumer), Brief 175 (voice clip refs), Brief 220 (LocalKey resolution), Brief 228 (storylet runtime)
- Mark auto lip-sync and storylet runtime deferred per Finding 17

## New inventions

- **INV-690** `dialogue.graph` as typed signed gseed with 5-node-type DAG and depth-bounded return stack
- **INV-691** Skill check primitive with replay-deterministic sub-seeded dice rolls
- **INV-692** Speaker-decoupled-from-entity primitive enabling shared sub-conversations and character transformation
- **INV-693** Lifetime `dialogue.choice_log` as substrate memory primitive for narrative consequence
- **INV-694** Sign-time predicate compilation against typed gseed registry, breaking refs fail to sign

## Open follow-ups

- Auto lip-sync via phoneme extraction (deferred to v0.4)
- Storylet runtime and drama manager (Brief 228 takes this)
- Multilingual voice asset pipeline (Brief 175 + Brief 220 follow-up)
- Specific dialogue density patterns per genre (Brief 230)

## Sources

1. inkle Ink scripting language documentation and *80 Days* postmortem
2. Yarn Spinner documentation and *Night in the Woods* dialogue retrospective
3. Twine documentation and academic interactive fiction papers
4. Disco Elysium narrative system talk, ZA/UM, 2019 — skill-check dialogue
5. Mass Effect dialogue wheel design talk, BioWare, 2014
6. Witcher 3 dialogue authoring talk, CDPR GDC 2017
7. Pentiment dialogue system talk, Obsidian GDC 2023
8. Reigns / Cultist Simulator storylet design retrospectives
9. Wildermyth storylet system talk, Worldwalker GDC 2021
10. *Hamlet on the Holodeck*, Janet Murray
11. Brief 159 (this repo) — FSM substrate
12. Brief 170 (this repo) — quest action consumer
13. Brief 220 (this repo, planned) — i18n / ICU MessageFormat
