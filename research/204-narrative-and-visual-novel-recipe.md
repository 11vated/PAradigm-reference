# 204 — Narrative and visual novel genre recipe

## Question
What is the typed genre composition recipe that produces a complete signed narrative or visual novel gseed bundle (Disco Elysium / Phoenix Wright / Doki Doki / interactive fiction class) from substrate primitives, with branching dialogue, character portraits, choice consequences, and save-anywhere?

## Why it matters (blast radius)
Narrative games are the canonical proving ground for the dialogue / quest / locale stack from Brief 180. They are also the lowest-cost-to-produce genre — a recipe that gets a creator from idea to playable VN in minutes is the highest-leverage onboarding path for non-coding creators.

## What we know from the spec
- Brief 180 — dialogue and quest editor.
- Brief 174 — UI / HUD pattern library.
- Brief 158 — save snapshot model.
- Briefs 197-203 — recipe template precedent.

## Findings
1. **Recipe inherits frame.**
2. **Required primitives.** `dialogue.tree` (heavy use), `quest.graph` (optional, story state tracking), `character.def` (typed portrait + emotion states), `scene.background` (typed backdrop), `audio.bus` (BGM + voice + SFX), `ui.element` (dialogue box + choice menu + save/load UI), `save.snapshot` (story progress).
4. **Character portrait system.** `character.def` declares a portrait set: typed emotion states (neutral / happy / sad / angry / surprised / etc.) each pointing at a sprite asset. Dialogue nodes typed-reference an emotion to show.
5. **Backgrounds.** `scene.background` declares a list of typed backdrop images and the dialogue node references which is active. Crossfade transitions are typed.
6. **Choice consequences.** Choices in `dialogue.tree` mutate typed `story.state` fields (flags, counters, character relationship scores). Quest graphs gate on typed conditions over story.state.
7. **Save-anywhere.** Narrative games save on every dialogue node. `save.snapshot` chunks the dialogue tree position + story.state into a small typed blob; auto-save runs on every node transition.
8. **Locale support.** Dialogue text is locale-keyed per Brief 180. Recipe declares supported locales; sign-time validates each dialogue node has a translation in every declared locale (or surfaces a warning).
9. **Voice acting.** Optional typed `voice.line` field per dialogue node referencing an audio asset. Substrate provides voice/text desync detection at sign-time (audio length vs estimated read time).
10. **Sub-recipes.** Pure VN (no choices, just narration), Choice-driven VN (Doki Doki / Steins;Gate-class), Investigation (Phoenix Wright-class with evidence inventory), CYOA / interactive fiction (text-only, no portraits — minimal sub-recipe).
11. **Validation contract.** Sign-time gates: at least one `dialogue.tree`, at least one `character.def`, at least one starting dialogue node, story.state schema declared, all dialogue node references resolve.

## Risks identified
- **Localization coverage.** Creators forget to translate. Mitigation: locale coverage indicator from Brief 180; missing translations are warnings not errors.
- **Branching complexity.** Choice-heavy VNs become unmanageable. Mitigation: Brief 180's interactive quest simulator surfaces unreachable nodes and dead ends.
- **Asset volume.** Portraits and backgrounds at scale. Mitigation: default sub-recipes ship with placeholder assets; creators source independently.
- **Voice/text desync.** Voice acting is hard to time. Mitigation: typed warning at sign-time when audio length exceeds estimated read time by >50%.

## Recommendation
Specify the narrative / VN recipe as a `recipe.gseed` heavily leveraging Brief 180's dialogue/quest stack with `character.def` portrait emotion sets, typed backdrop transitions, choice-mutates-story-state pattern, save-anywhere auto-save, locale coverage gating, and four sub-recipes. Default sub-recipe (choice-driven VN) produces a playable narrative game in under 60 seconds.

## Confidence
**4.5 / 5.** VN mechanics are simple and well-precedented; Brief 180's dialogue stack does most of the work. Lower than 5 because voice/text desync detection needs Phase-1 audio measurement against real recordings.

## Spec impact
- New spec section: **Narrative and visual novel genre recipe specification**.
- Adds typed `character.def` with portrait emotion-state schema.
- Adds typed `scene.background` and crossfade transition primitive.
- Adds the typed `voice.line` voice-acting binding.
- Cross-references Briefs 158, 174, 180, 197.

## New inventions
- **INV-854** — Typed `character.def` with portrait emotion-state set: characters are first-class typed gseeds with structured emotion vocabularies.
- **INV-855** — Typed `scene.background` with crossfade transition primitive: backdrops are signed gseeds, not opaque image references.
- **INV-856** — Save-anywhere auto-save on every dialogue node transition with typed snapshot chunking: narrative games guarantee no progress loss as a substrate-level primitive.
- **INV-857** — Voice/text desync detection at sign-time via audio length vs estimated read time: substrate catches voice acting timing issues before player exposure.
- **INV-858** — Story.state typed schema with quest-graph condition gating: story progress is structured typed state, not opaque flags.

## Open follow-ups
- Procedural narrative generation — deferred to v0.4.
- Speech-to-text dialogue authoring — deferred to v0.4.
- Branching narrative analytics — deferred to v0.3.
- Investigation sub-recipe evidence inventory primitive — Phase 1.

## Sources
1. Brief 158 — Save snapshot model.
2. Brief 174 — UI / HUD pattern library.
3. Brief 180 — Dialogue and quest editor.
4. Brief 197 — 2D platformer recipe.
5. Disco Elysium narrative design talks — ZA/UM.
6. Steins;Gate / visual novel design literature.
7. Twine / interactive fiction conventions (twinery.org).
