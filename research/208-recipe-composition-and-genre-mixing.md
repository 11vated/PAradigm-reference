# 208 — Recipe composition and genre mixing

## Question
What is the typed mechanism that enables creators to compose multiple genre recipes (Briefs 197-207) into hybrid games (e.g., platformer + roguelike + deckbuilder = Slay-the-Spire-action-platformer), and how does the substrate validate the resulting gseed bundle is internally consistent?

## Why it matters (blast radius)
The most successful indie games of the last decade are genre hybrids: Hades (action + roguelite + narrative), Stardew (sim + RPG + narrative), Inscryption (deckbuilder + narrative + horror), Cult of the Lamb (action + management). Single-genre recipes (Briefs 197-207) are necessary but not sufficient — the *composition* mechanism is what makes the recipe library feel like a creative tool rather than a template gallery.

## What we know from the spec
- Briefs 197-207 — single-genre recipes.
- Brief 152 — substrate signing and lineage.
- Brief 187 — mod and plugin surface (compositional precedent).

## Findings
1. **Recipe is a typed gseed graph node.** Each recipe from Briefs 197-207 is a `recipe.gseed` with declared imports, parameter slots, and validation contract. Composition is a typed graph: a parent `composite.recipe.gseed` declares which recipes it composes and how their primitives merge.
2. **Composition primitives.** Three composition operations: (a) **union** — merge two recipes' primitive sets; conflicts (same primitive type) require resolution. (b) **layer** — add one recipe's primitives on top of another, with the layered recipe's parameters overriding the base. (c) **gate** — one recipe runs only when typed condition holds (e.g., "deckbuilder phase only during combat").
3. **Conflict resolution rules.** When two recipes declare conflicting primitives (e.g., both declare a player FSM), the composite recipe must declare an explicit resolution: pick-one, merge-states, or wrap (one FSM contains the other as a sub-state). Sign-time validator gates that all conflicts are resolved.
4. **Cross-recipe parameter unification.** When two recipes declare parameters with the same typed semantic tag (e.g., both have `gravity`), the composite recipe inherits one value. Conflicting numeric defaults surface a typed warning; creator picks.
5. **Validation contract intersection.** The composite gseed must satisfy *all* component recipes' validation contracts simultaneously. If a contract becomes unsatisfiable (e.g., platformer requires gravity > 0, top-down RPG requires gravity = 0), validator surfaces the contradiction with a creator-actionable error.
6. **Layered recipes pattern.** Most hybrids use the layer composition: action-platformer-roguelite is platformer (Brief 197) base + roguelite (Brief 201) layered on top. Layering inherits the base's primitives and adds roguelite's run-state/meta-state separation, permadeath mutation, and procgen.
7. **Gated recipes pattern.** Hades-style action+deckbuilder uses gating: action-RPG (Brief 198) base + deckbuilder (Brief 202) gated on the typed condition "in-combat-room". Card draws happen only during combat phase.
8. **Composite as first-class artifact.** A `composite.recipe.gseed` is signed and reusable; creators can publish composites for others to instantiate. Compositions are appendable in lineage like any other gseed.
9. **Genre identity downgrade.** The composite's resulting genre identity is the intersection of component identities; if the composite no longer satisfies any single genre's identity, the result is downgraded to a generic "game" gseed with the component identities listed in metadata.
10. **Composition examples shipped with v0.1.** Substrate ships ~10 reference composites: Hades-clone (action-RPG + roguelite + narrative), Stardew-clone (sim + RPG + narrative), Slay-the-Spire-clone (deckbuilder + roguelite), Cult-of-the-Lamb-clone (action + management), Dead-Cells-clone (platformer + roguelite), Disco-Elysium-clone (narrative + RPG), Terraria-clone (voxel + RPG + sandbox), Spelunky-clone (platformer + roguelike + procgen), Crypt-of-the-NecroDancer (rhythm + roguelike — note: rhythm primitives needed, may be sub-recipe of Brief 200), Slay-the-Spire-action (deckbuilder + action — gated composite).

## Risks identified
- **Conflict explosion.** N recipes can conflict in ~N² ways. Mitigation: typed conflict surface is bounded by the number of named primitives; reference composites cover the common cases.
- **Validation contract contradictions.** Some genre combinations are structurally impossible (top-down + platformer). Mitigation: explicit error with the contradicting contracts cited; creator chooses which to drop.
- **Parameter inheritance ambiguity.** Multiple recipes declaring the same parameter create confusion. Mitigation: typed warnings; creator picks; substrate documents inheritance order rules.
- **Composite testing burden.** Each new composite needs validation. Mitigation: ship 10 reference composites tested in Brief 196 parity suite; creator-authored composites are creator-tested via Brief 185 playtest harness.

## Recommendation
Specify recipe composition as a typed `composite.recipe.gseed` kind with three composition operations (union / layer / gate), explicit conflict resolution rules, validation contract intersection, parameter unification with typed warnings, and 10 substrate-shipped reference composites. Composites are first-class signed gseeds.

## Confidence
**4.5 / 5.** The composition pattern is structurally clean and the reference composite list covers the canonical hybrid genres. Lower than 5 because the conflict resolution UX in Studio (Brief 177) needs Phase-1 validation against creator workflow.

## Spec impact
- New spec section: **Recipe composition and genre mixing specification**.
- Adds typed `composite.recipe.gseed` kind with union / layer / gate operations.
- Adds the conflict resolution rules schema.
- Adds the 10 reference composites as substrate-shipped artifacts.
- Cross-references Briefs 152, 187, 197-207.

## New inventions
- **INV-874** — Typed `composite.recipe.gseed` kind with three composition operations (union / layer / gate): hybrid genres are first-class composable substrate artifacts, not template forks.
- **INV-875** — Sign-time conflict resolution contract for composite recipes: primitive conflicts between component recipes must be explicitly resolved (pick / merge / wrap) before signing.
- **INV-876** — Validation contract intersection across composed recipes with explicit contradiction surfacing: structural impossibilities (e.g., gravity = 0 vs gravity > 0) are caught at sign-time with creator-actionable errors.
- **INV-877** — Cross-recipe parameter unification by typed semantic tag with inheritance order rules: shared parameters (gravity, max-speed) unify across composed recipes following documented inheritance.
- **INV-878** — 10 reference composites as substrate-shipped artifacts (Hades-clone / Stardew-clone / Slay-the-Spire-clone / Cult-of-the-Lamb-clone / Dead-Cells-clone / Disco-Elysium-clone / Terraria-clone / Spelunky-clone / Crypt-of-the-NecroDancer / Slay-the-Spire-action): canonical hybrid genres are creator-instantiable starting points, not blank-page problems.
- **INV-879** — Genre identity downgrade pattern for composites: composites that no longer satisfy any single genre's identity downgrade to a generic "game" with component identities listed in metadata, preserving substrate honesty.

## Open follow-ups
- Studio UX for conflict resolution — Phase 1 with Brief 177.
- Composite recipe federation publishing — covered by Brief 187 mod surface.
- Custom composition operations beyond union/layer/gate — deferred to v0.3.
- Parametric composites (instantiate composite N times with parameter sweeps) — deferred to v0.4.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 177 — Scene and level editor.
3. Brief 187 — Mod and plugin surface.
4. Briefs 197-207 — single-genre recipes.
5. Hades GDC postmortem — Supergiant Games.
6. "Genre hybridization in indie games" — game design literature.
