# 202 — Card game and deckbuilder genre recipe

## Question
What is the typed genre composition recipe that produces a complete signed card game or deckbuilder gseed bundle (Hearthstone / Slay the Spire / Magic-class) from substrate primitives, with typed card definitions, deck composition rules, and turn-based state?

## Why it matters (blast radius)
Deckbuilders are a top-3 indie genre by revenue (Slay the Spire, Inscryption, Monster Train). They are the canonical proving ground for typed effect composition: every card is a typed mutation against game state. A working recipe demonstrates that the substrate composes typed effects into a creator-instantiable card game without per-card code.

## What we know from the spec
- Brief 159 — state machines / behavior trees.
- Brief 174 — UI / HUD pattern library.
- Brief 158 — save snapshot model.
- Brief 201 — roguelite recipe (deckbuilder sub-recipe reference).
- Briefs 197-201 — recipe template precedent.

## Findings
1. **Recipe inherits frame.**
2. **Required primitives.** `card.def` (typed card definition), `card.deck` (typed deck container), `card.zone` (hand / draw / discard / exhaust), `effect.def` (typed effect with target selector + mutation), `entity.archetype` (player + enemies), `stats.sheet`, `state.machine` (turn FSM), `ui.element` (card hand UI), `audio.bus`, `vfx.system` (card play feedback).
3. **Card as typed gseed.** A `card.def` declares: name, cost, type (attack / skill / power / curse / etc.), rarity, target selector type, and an ordered list of typed `effect.def` references. No code per card — all behavior is typed effect composition.
4. **Effect catalog.** Substrate ships ~30 typed effect kinds covering the deckbuilder vocabulary: deal-damage, gain-block, draw-cards, discard, exhaust, apply-status, gain-energy, scry, search-deck, copy-card, modify-cost, conditional-branch, etc. Creators compose these into cards; new effect kinds are creator extensions via the mod surface (Brief 187).
5. **Target selector types.** Single-enemy, all-enemies, random-enemy, self, any-target, deck-search, hand-search. Typed selectors gate which cards can be played and against what.
6. **Turn FSM.** Start-of-turn → Draw → Player-actions → End-of-turn → Enemy-turn → Start-of-turn loop. Each phase emits typed events that effects can hook.
7. **Deck composition rules.** `card.deck` enforces creator-defined typed rules: max copies per card, deck size min/max, banned card list. Sign-time validator gates rule satisfaction.
8. **Status effects.** Buffs / debuffs are typed `status.def` instances with stack count, duration, and tick semantics. Cards apply statuses via the apply-status effect.
9. **Sub-recipes.** Slay-the-Spire-style (single-player roguelite, layered with Brief 201), Hearthstone-style (PvP collectible card game, requires Brief 209 multiplayer), Inscryption-style (mixed deckbuilder + narrative), Magic-style (stack-based priority and complex interactions — flagged as advanced).
10. **Validation contract.** Sign-time gates: at least one `card.def`, at least one starting `card.deck`, deck composition rules satisfied, turn FSM present, effect references resolve.
11. **Card art binding.** Cards reference Brief 088A seed armory pack art by typed asset id. Default pack provides programmer-art card backs and frames.

## Risks identified
- **Effect composition explosion.** 30 typed effects × selector types × condition modifiers create exponential combinatorial space. Mitigation: validation contract gates effect references resolve; runtime errors are typed and recoverable.
- **Magic-style complexity.** Stack-based priority systems are extremely hard. Mitigation: flag Magic-style as advanced; v0.1 ships only the simpler sub-recipes; revisit in v0.3.
- **Multiplayer card games.** Hearthstone-class requires Brief 209 multiplayer surface; the sub-recipe is structurally complete but the multiplayer surface lands in v0.3.
- **Card art volume.** Card games need lots of art. Mitigation: default to programmer-art; creators source art independently.

## Recommendation
Specify the card game / deckbuilder recipe as a `recipe.gseed` with typed `card.def` / `card.deck` / `card.zone` / `effect.def` primitives, ~30 substrate-shipped typed effect kinds, typed target selectors, turn FSM, deck composition rule validation, and four sub-recipes. Default sub-recipe instantiation (Slay-the-Spire-style, layered with Brief 201) produces a playable single-player deckbuilder.

## Confidence
**4 / 5.** Card game mechanics are well-precedented; the novelty is the typed effect catalog as substrate primitive. Lower than 4.5 because the 30-effect catalog needs Phase-1 validation against real card designs to confirm coverage.

## Spec impact
- New spec section: **Card game and deckbuilder genre recipe specification**.
- Adds typed `card.def`, `card.deck`, `card.zone`, `effect.def`, `status.def` gseed kinds.
- Adds the 30-effect catalog as substrate-shipped library.
- Cross-references Briefs 159, 174, 187, 197, 201.

## New inventions
- **INV-844** — Typed `card.def` with ordered effect composition replacing per-card code: cards are pure data, all behavior emerges from typed effect composition.
- **INV-845** — 30-effect substrate-shipped catalog covering the deckbuilder vocabulary: substrate provides the card-game effect primitives; creators compose, mods extend.
- **INV-846** — Typed target selector primitives gating playability: selectors are first-class typed gseeds enforcing valid card play at sign-time and runtime.
- **INV-847** — Typed `status.def` stacking and tick semantics as substrate primitive: buffs/debuffs are structured gseeds with declarative semantics, not creator scripts.
- **INV-848** — Typed deck composition rule validation at sign-time: deck-building rules are gates on the deck gseed, not runtime checks.

## Open follow-ups
- Multiplayer card games (Hearthstone-class) — deferred to v0.3 with Brief 209.
- Magic-style stack/priority — deferred to v0.3.
- Procedural card generation — deferred to v0.4.
- Deck-importer for popular card formats — deferred to v0.4.

## Sources
1. Brief 159 — State machines and behavior trees.
2. Brief 187 — Mod and plugin surface.
3. Brief 197 — 2D platformer recipe.
4. Brief 201 — Roguelike recipe.
5. Slay the Spire postmortem — Mega Crit.
6. Inscryption design talks — Daniel Mullins.
7. Magic: The Gathering Comprehensive Rules.
