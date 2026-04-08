# 184 — UI and HUD layout editor

## Question
What is the creator-facing editor surface that authors `ui.element`, `ui.layout`, and `ui.theme` (Brief 174) gseeds with anchor/constraint editing, theme preview, and sign-time accessibility (WCAG) checks?

## Why it matters (blast radius)
UI is the creator's contact surface with the player. If accessibility checks aren't sign-time, creators ship inaccessible games. If theme preview is approximate, what creators see ≠ what players see. If anchor/constraint editing is bolted on, creators learn position math instead of declaring intent.

## What we know from the spec
- Brief 174 — `ui.element` root, 30 default kinds, 5 layout primitives (flow / grid / stack / absolute / constraint), 4 default themes, deterministic UI layout solver, sign-time WCAG 2.1 AA contrast validation.
- Brief 050 — accessibility and i18n.
- Brief 154 — input abstraction (action-bound navigation).
- Brief 177 — modifier-surface contract.
- Brief 180 — locale coverage indicators (string editing).

## Findings
1. **Editor surface = canvas + element tree + property inspector + theme picker.** The canvas renders the UI hierarchy at the chosen viewport size. The element tree mirrors the `ui.element` hierarchy. The property inspector edits typed fields per element kind. The theme picker swaps the active `ui.theme` for preview.
2. **Element placement.** Drag-from-palette compiles to a `ui.element.add` mutation. The element is parented under the current selection. The 30 element kinds (Brief 174) are organized in palette categories: text (label, paragraph), input (button, toggle, slider, text field, dropdown), container (panel, group, scrollview), display (image, icon, progress bar, gauge, meter), game-specific (healthbar, ammo counter, minimap, ability slot, hotbar, inventory grid, dialogue box, subtitle area, hud-pip, crosshair, damage number, tooltip).
3. **Layout primitives.** Five layout primitives per Brief 174 with typed parameters: flow (direction / wrap / justify / align), grid (columns / rows / gap), stack (axis / spacing), absolute (xy offset), constraint (anchor edges to parent or sibling with offsets). Layout type is a typed enum on the container.
4. **Anchor and constraint editing.** Anchor mode renders nine handles (corners + edges + center) on the selected element. Dragging an anchor compiles to a `ui.element.set_anchor` mutation. Constraint mode renders typed constraint lines between elements; clicking a line edits the constraint expression in the property inspector.
5. **Resolution preview.** A typed `editor.viewport_size` ephemeral controls preview canvas dimensions with presets (1080p, 1440p, 2160p, mobile portrait/landscape, ultrawide). The deterministic UI layout solver from Brief 174 runs on every preview change — no editor approximation.
6. **Theme preview.** Switching themes in the editor swaps active `ui.theme` reference. Preview re-runs the layout solver and the WCAG contrast checker. The four default themes (light / dark / high_contrast / colorblind_safe) are always available; creators can author additional themes as typed `ui.theme` gseeds.
7. **Sign-time WCAG check.** Per Brief 174, every commit runs WCAG 2.1 AA contrast validation across all text/background pairs in the active themes. Failures produce typed errors with the offending element ID and the measured contrast ratio. The editor surfaces the failure with a fix-up suggestion (e.g., "increase text color luminance to L >= 0.65 for AA at body-text size").
8. **Localization-aware text.** Text elements bind to `localization.string_ref` (Brief 180). The editor surfaces locale coverage per element. Long-text wrap and overflow are computed per locale at preview time so creators see worst-case wrap before commit.
9. **Action-bound navigation graph.** Per Brief 174, focus navigation is action-bound (input.action.ui_navigate_*). The editor renders the navigation graph as edges between focusable elements; creators can drag-edit the graph or accept the auto-generated graph from Brief 174's solver.
10. **Theme-binding indicators.** Hardcoded color/font/size values are flagged at edit time with a "use theme token instead" warning. Creators can promote a hardcoded value to a theme token via one click.
11. **Game-specific element editors.** Some element kinds have specialized editors: minimap (drag region, scale), inventory grid (cell size, capacity), hotbar (slot count). Each is a typed sub-editor over the element's kind-specific schema.
12. **Responsive variants.** A `ui.element` can declare typed variants per viewport breakpoint. The editor exposes a "add breakpoint variant" action that creates a delta over the base element, similar to Brief 177's prefab variants.
13. **Scrollview content overflow.** Scrollview elements declare typed content size and overflow policy. Sign-time validation rejects scrollviews with infinite content size and no scroll axis.

## Risks identified
- **WCAG check false positives over images.** Text over an image background can't be statically analyzed for contrast. Mitigation: editor accepts a typed `min_background_luminance_assertion` field on the text element that the creator declares, validated at sign time against the asserted floor.
- **Layout solver performance under deep trees.** Hundreds of nested constraint elements can slow the editor. Mitigation: solver caches subtree layouts; invalidation propagates only along touched edges.
- **Theme combinatorial explosion.** N themes × M elements × P breakpoints = a lot. Mitigation: WCAG check runs per theme but only on affected elements per commit.
- **Locale wrap divergence.** German is 30% longer than English; Japanese is shorter. Editor only previews the active locale. Mitigation: a typed "worst-case wrap" preview mode runs the layout against the longest known string per element across all bound locales.
- **Action-bound navigation rot.** Adding/removing focusable elements invalidates auto-generated navigation. Mitigation: regeneration happens on commit; manual overrides survive regeneration unless creator explicitly resets.

## Recommendation
Specify the UI editor as a canvas + tree + inspector + theme picker surface inheriting Brief 177's modifier-surface contract. Ship the 5 layout primitives, 30 element kinds, 4 default themes, sign-time WCAG check, and locale-aware text editing at v0.1. Defer 3D worldspace UI to v0.4. Make hardcoded values a warning, not a rejection — creators iterate fast in early stages.

## Confidence
**4.5 / 5.** UI editor patterns converged across Unity UI Toolkit, Godot Control, Unreal UMG, Figma, web inspector tools. The novelty is the sign-time WCAG gate, the locale-worst-case wrap preview, and the runtime-equals-preview layout solver. Lower than 5 because Phase-1 will measure solver performance under deep trees.

## Spec impact
- New spec section: **UI and HUD layout editor surface specification**.
- Adds the typed `min_background_luminance_assertion` escape for image backgrounds.
- Adds the typed `editor.viewport_size` ephemeral.
- Cross-references Brief 174 for the layout solver and WCAG validator.

## New inventions
- **INV-754** — Canvas + tree + inspector + theme picker UI editor with runtime-equals-preview layout solver: same solver runs at edit and runtime.
- **INV-755** — Sign-time WCAG 2.1 AA contrast gate with creator-asserted background luminance escape: text-on-image is handled via creator assertion, not silent skip.
- **INV-756** — Locale worst-case wrap preview: layout runs against the longest known string across bound locales so creators see overflow before commit.
- **INV-757** — Hardcoded-value warning with one-click theme token promotion: hardcoded colors/fonts/sizes are surfaced as warnings with an inline upgrade path.
- **INV-758** — Action-bound navigation graph editor with auto-generation and manual override survival: the focus graph is editable and regenerable, with manual overrides preserved across regenerations.

## Open follow-ups
- 3D worldspace UI (deferred to v0.4).
- Animated UI transitions library (deferred to v0.2 — leverages Brief 179's animation editor).
- Custom shader effects on UI elements (deferred to v0.4).
- Auto-generated UI from data schemas (deferred to v0.3 as a power tool).
- Multi-creator simultaneous UI editing (deferred to v0.3).

## Sources
1. Brief 050 — Accessibility and i18n.
2. Brief 154 — Input abstraction.
3. Brief 174 — UI and HUD pattern library.
4. Brief 177 — Scene editor modifier surface.
5. Brief 180 — Locale coverage indicators.
6. WCAG 2.1 AA specification (w3.org/TR/WCAG21/).
7. Unity UI Toolkit documentation.
8. Godot 4.x Control node reference.
9. Unreal UMG documentation.
