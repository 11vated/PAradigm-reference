# 180 — Dialogue and quest editor specification

## Question
What is the creator-facing editor surface that authors `dialogue.graph` (Brief 171) and `quest.definition` (Brief 170) gseeds with branching visualization, condition expression authoring, and localization-aware string editing?

## Why it matters (blast radius)
Dialogue and quest content is the densest narrative-creator surface, with the highest cross-namespace coupling (binds to Briefs 159 FSM, 160 AI, 167 combat, 168 enemies, 169 loot, 173 procgen). If the editor cannot validate cross-namespace references at sign time, creators ship broken quests. If condition expressions are typed in raw, creators write syntax errors instead of stories. If localization is bolted on, the substrate violates Brief 050's i18n commitment.

## What we know from the spec
- Brief 170 — `quest.definition` + 8 objective primitives + state machine binding.
- Brief 171 — `dialogue.graph` + 5 node types + ICU MessageFormat strings.
- Brief 159 — typed FSM as quest state machine substrate.
- Brief 050 — accessibility and i18n.
- Brief 052 — lineage time machine.
- Brief 057 — modifier-surface DSL.
- Brief 177 — scene editor inheritance.

## Findings
1. **Unified node graph view.** Dialogue and quest both author as typed node graphs over a single editor canvas. The two share node-graph chrome (pan/zoom/connect/multi-select) and differ only in palette and node type set. This is the same modifier-surface contract as Brief 177.
2. **Dialogue node palette.** Five node types per Brief 171: line / choice / condition / action / jump. Each renders as a distinct shape with typed input slots. Drag-from-palette compiles to a `dialogue.graph.add_node` mutation.
3. **Quest node palette.** Eight objective primitives per Brief 170: kill / fetch / escort / defend / explore / collect / interact / dialogue, plus state nodes (start / objective / branch / completion / failure) and edges (typed transitions binding to Brief 159 FSM events).
4. **Condition expression authoring.** Conditions in both dialogue and quest are written in a typed expression DSL (the same one as Brief 165 progression composition and Brief 168 enemy.encounter validation). The editor offers an autocomplete dropdown driven by the cross-namespace symbol table (entity refs, faction refs, inventory item refs, progression flag refs, dialogue choice log refs, etc.). Conditions compile at sign time to typed predicates rejected on type mismatch.
5. **Action node authoring.** Action nodes in dialogue execute typed mutations (grant item per Brief 169, change faction standing per Brief 170, set narrative beat per Brief 171, emit event to Brief 152 scheduler). Each action is a typed function with sign-time-checked arguments — no free-form scripting.
6. **String authoring with ICU MessageFormat.** Every player-facing string is an ICU MessageFormat (Brief 171). The editor renders the string with a typed parameter form (parameter name / type / sample value) and previews the resolved string for the active locale. Sign-time validation: every parameter referenced in the string must be declared, every declared parameter must be referenced.
7. **Localization workflow.** Strings are stored in a typed `localization.bundle` keyed by string ID, with the source locale marked. The editor surfaces locale coverage per dialogue: green if all locales translated, yellow if partial, red if source-only. Translation can be hand-edited or routed through the universal pipeline (Brief 089 + Brief 050).
8. **Choice log binding.** Brief 171's `dialogue.choice_log` is exposed as a queryable namespace in the condition autocomplete (`choice_log.lifetime("npc_amelia.first_meeting") == "rude"`). The editor highlights choice log references as cross-graph dependencies and warns if the referenced choice id does not exist anywhere.
9. **Branch visualization.** Dialogue branches render as edges between nodes; the editor auto-layouts on commit but lets the creator manually pin nodes via editor-runtime metadata (excluded from the determinism hash, like Brief 177's editor_metadata).
10. **Quest state preview.** The editor can simulate a quest from start by stepping through the FSM (Brief 159) with a typed `quest.simulator` ephemeral. Each step shows the active state, available transitions, and required predicate evaluations. This is the quest equivalent of Brief 179's animation preview.
11. **Cross-quest dependency view.** A quest's prerequisites (other quest completions, faction levels, narrative beats) render as upstream nodes in a separate dependency graph. The editor refuses to commit a quest with a circular prerequisite chain.
12. **Voice attachment.** A dialogue line can carry a typed `audio.clip_ref` slot for voice. The editor lets the creator drag a voice file from the asset palette (Brief 089 import) onto a line; the resulting `audio.clip` gseed is signed and bound to the line. Subtitle text falls back to the ICU string when voice is unavailable.

## Risks identified
- **Condition expression complexity.** Creators with no programming background might struggle. Mitigation: visual condition builder (drag-and-drop boolean trees) is an alternate surface that compiles to the same DSL — opt-in per creator.
- **Cross-namespace reference rot.** A dialogue refs an item that gets renamed; the dialogue silently breaks. Mitigation: sign-time validation across the full namespace graph rejects dangling references at commit, surfacing a typed error pointing at the offending node.
- **Localization drift.** Source locale changes invalidate translations. Mitigation: the bundle records a content hash per source string; translations carry the hash they were translated against. Editor surfaces "stale translation" warnings when hashes drift.
- **Quest simulator state explosion.** A quest with N branches has 2^N path combinations to validate. Mitigation: simulator is interactive, not exhaustive; sign-time validation only checks reachability of every state (cheap), not every path.
- **Voice + subtitle desync.** Voice file longer than ICU string suggests. Mitigation: editor surfaces duration mismatch as a warning; subtitle pacing is computed from voice length when available, from word-count when not.

## Recommendation
Specify the dialogue and quest editor as a unified node-graph surface with per-flavor palettes, a typed expression DSL with autocomplete-driven authoring, ICU-MessageFormat string editing with locale coverage indicators, and a quest simulator that steps through the FSM. Reject every dangling cross-namespace reference at commit. Ship the visual condition builder as an alt surface from v0.1 to lower the bar for non-programmer creators.

## Confidence
**4.5 / 5.** Visual narrative tools have rich precedent: Twine, Ink/Inky, YarnSpinner, articy:draft, Chat Mapper, Dialogue System for Unity. The novelty is the typed-DSL-with-autocomplete pattern, the sign-time cross-namespace validator, the quest simulator binding to Brief 159 FSM, and the locale-coverage indicator. Lower than 5 because the visual condition builder UX needs Phase-1 user testing with non-programmers.

## Spec impact
- New spec section: **Dialogue and quest editor surface specification**.
- Adds the typed expression DSL grammar (referenced by Briefs 165, 168, 170, 171).
- Adds the `localization.bundle` typed gseed structure.
- Adds the source-string content hash and stale-translation contract.
- Cross-references Brief 050 (i18n) for the source-of-truth-in-gseed commitment.

## New inventions
- **INV-734** — Unified node-graph editor with per-flavor palettes: one editor canvas authors dialogue, quest, behavior tree (Brief 181), and visual scripting (Brief 218) graphs with shared chrome and per-flavor node sets.
- **INV-735** — Typed expression DSL with cross-namespace autocomplete: conditions and actions are authored against a symbol table populated from every namespace, with sign-time type checking.
- **INV-736** — Locale-coverage indicator with content-hash translation freshness: each translation records the source-string hash it was translated against, surfacing stale translations as the source drifts.
- **INV-737** — Interactive quest simulator over Brief 159 FSM: the editor steps through quest states with predicate evaluation visible, without trying to enumerate every combinatorial path.
- **INV-738** — Visual condition builder as alt surface compiling to the same DSL: drag-and-drop boolean tree editor for non-programmer creators, producing identical signed predicates.

## Open follow-ups
- Auto-translation pipeline integration (deferred — depends on Brief 089 universal pipeline maturity for natural language).
- Voice synthesis integration for placeholder voice (deferred to v0.2).
- Multi-creator simultaneous dialogue editing (deferred to v0.3).
- Storylet authoring surface (deferred to v0.5 with Brief 171 narrative.storylet runtime).
- Branching visualization at scale (1000+ node graphs) — empirical, Phase 1 measurement.

## Sources
1. Brief 050 — Accessibility and internationalization.
2. Brief 089 — Universal anything-to-gseed pipeline.
3. Brief 159 — State machines and behavior trees.
4. Brief 165 — Progression system patterns.
5. Brief 168 — Enemy and creature taxonomies.
6. Brief 170 — Quest and mission patterns.
7. Brief 171 — Dialogue and narrative patterns.
8. Brief 177 — Scene and level editor specification.
9. Inkle Studios — Ink scripting language reference.
10. YarnSpinner documentation (yarnspinner.dev/docs).
11. ICU MessageFormat specification (unicode-org.github.io/icu/userguide/format_parse/messages/).
