# 026 — UI engine

## Question
What are the seed schema, kernel pipeline, and proof model for the UIEngine — the engine that produces user interfaces, HUDs, menus, and interactive panels — and how does it differ from the Visual2D engine which it superficially overlaps?

## Why it matters
UI is the most contextual and most accessibility-sensitive asset class. Unlike a piece of art or a sound effect, a UI must obey constraints (touch target sizes, contrast ratios, focus order, screen reader semantics) in addition to looking right. The UIEngine is GSPL's bet that *generative* UI can be built with the same proof-bearing rigor as everything else.

## What we know from the spec
- `engines/ui.md` exists as a stub.
- The 17 + 5 gene types include CategoricalGene, ColorGene, RuleGene, GraphGene, EnvelopeGene — the necessary building blocks.

## Findings — schema

### UIEngine

Produces UI specifications: layout trees, design tokens, interaction rules, accessibility semantics. Does not produce a runnable web app — it produces a *spec* that downstream renderers (HTML/CSS, Godot, Unity, native) consume.

**Genes (typical 25-50):**
- `target.platform` (CategoricalGene: web, mobile, console, desktop, vr, generic)
- `target.density` (CategoricalGene: 1x, 2x, 3x, hdpi)
- `target.input` (CategoricalGene: pointer, touch, gamepad, keyboard, mixed)
- `layout.kind` (CategoricalGene: stack, grid, dashboard, hud, modal, page)
- `layout.tree` (GraphGene of layout containers and slots)
- `layout.spacing` (ScalarGene base unit; all spacing is integer multiples)
- `tokens.palette` (SequenceGene<ColorGene>: surface, on-surface, primary, on-primary, accent, danger, success, warning, …)
- `tokens.type_scale` (SequenceGene of type sizes following a modular scale)
- `tokens.radius_scale` (SequenceGene of corner radii)
- `tokens.elevation_scale` (SequenceGene of shadow specs)
- `motion.timing_curves` (SequenceGene<EnvelopeGene>)
- `motion.duration_scale` (SequenceGene of durations)
- `interaction.rules` (RuleGene of focus/hover/active/disabled state transitions)
- `accessibility.contrast_floor` (ScalarGene, default 4.5 for AA, 7 for AAA)
- `accessibility.touch_target_min` (ScalarGene in pt, default 44)
- `accessibility.focus_order` (SequenceGene of focusable element references)
- `accessibility.semantics` (per-node CategoricalGene of ARIA roles)
- Plus the 8 Core genes.

### What separates UIEngine from Visual2D

- **Constraint-first design**: every UIEngine output must pass an accessibility validator (contrast, target size, focus order, semantics) before it leaves the engine. Visual2D has no such gate.
- **Token-based, not pixel-based**: UI is defined by design tokens (semantic colors, spacing scale, type scale) — not raw pixel values. Visual2D operates on raw colors and shapes.
- **Interaction is first-class**: UIEngine has rules for state transitions (hover, focus, active, disabled). Visual2D has none.
- **Layout tree is the structure**: UIEngine's primary genome is a layout tree of containers and slots. Visual2D's is a free-form composition of shapes and layers.

## Pipeline

Standard four-stage:

1. **Seed → Spec IR** (deterministic): produces a JSON-canonical UI spec.
2. **Spec IR → Validation** (deterministic): runs accessibility validators (Brief 014's invariants extended). Hard fails on contrast, touch target, focus order. Warns on advisory issues.
3. **Spec IR → Render preview** (deterministic): produces a screenshot of the UI in its default state for the studio's preview pane.
4. **Spec IR → Code/Asset export** (target-specific writers).

The Spec IR is the proof-bearing artifact. Renders are not.

## Cross-engine bindings

- `UI ← Visual2D`: UI may consume Visual2D backgrounds, illustrations, and decorative elements as slot contents.
- `UI ← Procedural`: UI may consume Procedural seeds for fill patterns, divider textures, and motif backgrounds.
- `UI ⊂ FullGame`: a FullGame seed includes one or more UIEngine seeds for menus, HUDs, and overlays.
- All UI engines bind to Core via the palette and energy genes.

## Accessibility validation

UIEngine ships a normative accessibility validator that runs at IR validation time. The validator enforces:

1. **Contrast**: every text token's foreground/background pair meets the contrast floor.
2. **Touch target**: every interactive element's bounding box meets the touch target minimum.
3. **Focus order**: every focusable element appears in the focus order; the order is a valid topological walk of the layout tree.
4. **Semantics**: every interactive element has an ARIA role from the legal vocabulary; landmarks (header, main, nav, footer) are present where the layout kind requires them.
5. **Motion**: any animation longer than 200ms has a "reduced motion" alternative.
6. **Color independence**: no information is conveyed by color alone; every color-coded element has a redundant icon, label, or pattern.

These validations are *hard* gates, not warnings. A UIEngine seed that fails any of them is `Invalid`.

## Risks identified

- **Generative UI feels uncanny**: machine-designed UIs often look "off" in ways human-designed ones don't. Mitigation: heavy reliance on critic models trained on real UIs (Brief 040), and a tight `tokens` system that constrains the design space.
- **Accessibility vs creative freedom tension**: hard gates restrict what the engine can produce. Mitigation: gates are correct — accessibility is non-negotiable. The constraint *is* the feature.
- **Target platform proliferation**: web, mobile, gamepad UIs are very different. Mitigation: separate exporters per target; the IR is platform-neutral.
- **Token system rigidity**: a forced 8pt grid with modular type scale may feel limiting. Mitigation: configurable but with defaults that match well-known systems (Material 3, Apple HIG, Tailwind).

## Recommendation

1. **Adopt the schema as drafted.**
2. **Spec IR is the proof-bearing artifact**; renders are not.
3. **The accessibility validator is a hard gate**, not a warning. WCAG 2.1 AA at minimum.
4. **Token system is mandatory**: no raw pixel values in genes; all spacing/sizing is via tokens.
5. **Per-target exporters** ship for web (HTML/CSS), Godot, Unity, generic JSON.
6. **Reduced-motion alternatives are required** for any animation > 200ms.
7. **Critic models for generative UI** are a Phase 2 deliverable (Brief 040 cross-reference).

## Confidence
**4/5.** Constraint-based UI generation is well-trodden (HCI literature, design systems literature, Apple/Google's accessibility specs). The 4/5 reflects the unproven assumption that *generative* UI within these constraints feels good to users.

## Spec impact

- `engines/ui.md` — full schema.
- `algorithms/ui-accessibility-validator.md` — the hard-gate validator pseudocode.
- `algorithms/design-tokens.md` — the token system specification.
- `tests/ui-conformance.md` — accessibility test corpus.
- New ADR: `adr/00NN-ui-accessibility-as-hard-gate.md`.

## Open follow-ups

- Decide on the default token scale (likely Material 3-inspired with adjustable base unit).
- Build the per-target exporters in Phase 2.
- Train critic models for "is this UI good" using public UI datasets. Phase 2.
- Define the legal ARIA role vocabulary as a frozen table.

## Sources

- WCAG 2.1 AA Specification.
- Material Design 3 token system.
- Apple Human Interface Guidelines.
- Tailwind CSS design tokens.
- Internal: Briefs 013, 014 (validator), 040 (critic models).
