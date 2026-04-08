# 174 — UI and HUD pattern library

## Question

What canonical UI and HUD primitives does GSPL ship in `ui.*` so that any genre can compose inventories, menus, dialogs, tooltips, minimaps, healthbars, ammo counters, dialog wheels, quest trackers, and pause screens from typed signed primitives, with accessibility-first defaults, signed input bindings, deterministic layout, and v0.1 reach?

## Why it matters (blast radius)

UI is the first thing players see and the last thing developers polish — every game ships dozens of UI panels and HUD widgets. Without typed UI primitives, every game reinvents healthbars, menus, and inventory grids, breaking accessibility, localization, theming, and cross-game tooling. UI is also the most common source of accessibility failures (hardcoded sizes, low contrast, no alt text). Brief 184 (UI editor), Brief 221 (accessibility checks), Brief 220 (i18n string layout), Brief 165 (progression display), Brief 169 (loot popups), Brief 170 (quest tracker), and Brief 171 (dialogue choice rendering) all consume `ui.*`.

## What we know from the spec

- Brief 153 — ECS substrate; UI elements are typed components
- Brief 154 — input; UI navigation is action-driven (rebinding-first per Brief 154)
- Brief 158 — save/load; UI state (open panels, selections) is partially saved
- Brief 050 — accessibility/i18n (Round 2); UI inherits the substrate accessibility-as-structural commitment
- Brief 220 — i18n; every UI string is a LocalKey
- Brief 221 — accessibility check pipeline reads from typed UI gseeds

## Findings

1. **`ui.element` as the root primitive.** Every UI item is a typed signed gseed `ui.element` with: `element_id`, `kind: ui_kind_id`, `transform: ui_transform`, `anchor: AnchorMode`, `pivot: (f32, f32)`, `size_mode: enum{absolute, relative, fit_content, fixed_aspect}`, `style_ref: style_ref`, `state: enum{normal, hover, focus, pressed, disabled}`, `accessibility_props: AccessibilityProps`, `localization_keys: set<LocalKey>`, `signing_authority`. Substrate ships ~30 default kinds; creators can declare custom kinds.

2. **Eighteen canonical UI element kinds.** Surveying Material Design, Apple HIG, Game UI Database (gameuidatabase.com), and shipped game UIs (Persona 5, Destiny 2, Hades, Civilization VI, Stardew Valley) yields **18 irreducible kinds**: `text`, `image`, `button`, `toggle`, `slider`, `dropdown`, `list`, `grid`, `panel`, `dialog`, `tooltip`, `progress_bar`, `radial`, `tab_group`, `scroll_view`, `text_input`, `radial_menu`, `menu_bar`. Plus 12 game-specific kinds: `healthbar`, `resource_pool_display`, `ammo_counter`, `inventory_grid`, `equipment_slot`, `minimap`, `quest_tracker`, `dialog_wheel`, `combo_meter`, `loot_popup`, `damage_number`, `status_effect_strip`. Total **30 default kinds**.

3. **`ui.layout`.** A layout is a typed gseed expressing how children are arranged. Five canonical layout primitives: `ui.layout.flow` (flexbox-class), `ui.layout.grid` (CSS grid-class), `ui.layout.stack` (vertical/horizontal), `ui.layout.absolute` (anchored offsets), `ui.layout.constraint` (Apple AutoLayout-class). Each is parameterized; layouts compose hierarchically. Layout solver is deterministic and runs at fixed-tick boundary, never on render thread.

4. **`ui.style`.** A style is a typed gseed containing visual properties: `style_id`, `colors: ColorPalette`, `font_set: FontSetRef`, `font_size_scale: f32`, `padding`, `margin`, `border`, `corner_radius`, `shadow`, `opacity`, `cursor_hint`, `state_overrides: map<state, style_props>`. Styles cascade like CSS; child elements inherit parent styles unless explicitly overridden.

5. **Theming and skinning.** A `ui.theme` is a top-level signed gseed binding a `ColorPalette`, font set, and base style overrides. Theme switching is deterministic and signed (an event in the per-tick Merkle batch). Substrate ships 4 default themes at v0.1: `light`, `dark`, `high_contrast`, `colorblind_safe`. Creator-defined themes inherit from one of the 4 defaults.

6. **Color accessibility.** Every color in a `ColorPalette` carries optional contrast metadata. The substrate's accessibility check (Brief 221) reads style + color choices and flags WCAG 2.1 AA violations (contrast ratio ≥ 4.5:1 for body text, 3:1 for large text). Sign-time warnings emitted for failing pairs; runtime accessibility mode can auto-elevate to `high_contrast` theme.

7. **Font sizing and scaling.** All font sizes are *relative to a base scale*. Player-side `accessibility.font_scale ∈ [0.8, 2.5]` multiplies the base; layouts must accommodate scale changes. Substrate ships default scaling targets that pass at 2.0× scale.

8. **Layout determinism.** Two clients with the same screen resolution, theme, font scale, and locale produce *identical* layouts. Achieved by: (a) integer-quantized text metrics from a shared font reference; (b) deterministic line-break algorithm (ICU-based); (c) signed layout solver that's pure functional (no side effects, no random tiebreaks). Layout output is part of the per-tick state for replay reproducibility (matters for cross-engine exports).

9. **Localization-aware layouts.** Strings can be 2-3× longer in some languages (German, Russian). The substrate's layout primitives default to `fit_content` for text containers and warn at sign time if a fixed-width text container is shorter than the longest localized string in the project's enabled locale set. RTL languages (Arabic, Hebrew) get layout mirroring via the `auto_mirror_for_rtl` flag on layouts.

10. **Input and navigation.** UI navigation uses Brief 154's action-not-event input. Default navigation actions: `ui.action.up`, `down`, `left`, `right`, `confirm`, `cancel`, `menu`, `tab_left`, `tab_right`. All rebindable. Gamepad navigation, keyboard navigation, and touch all use the same action set. Each `ui.element` declares its `focus_neighbors: (up, down, left, right)` to form a typed navigation graph; the substrate auto-derives neighbors from spatial layout if not specified.

11. **Accessibility props.** Every UI element carries `AccessibilityProps`: `role: AriaRoleId`, `label: LocalKey`, `description: LocalKey`, `live_region: enum{none, polite, assertive}`, `keyboard_focusable: bool`, `screen_reader_visible: bool`, `motion_safe_alternative: optional<element_ref>`. Screen-reader integration uses platform APIs (NVDA/JAWS/VoiceOver) via Brief 050 accessibility primitives.

12. **Inventory grid.** A canonical kind worth specifying. `ui.inventory_grid` parameters: `cell_dims`, `slot_count`, `slot_layout: enum{rectangular, hexagonal, custom}`, `drag_drop_enabled`, `multi_select`, `quick_actions: set<action_ref>`, `tooltip_delay_ticks`, `sort_modes: set<sort_mode_id>`. Reads inventory components from Brief 153 ECS; updates are signed mutations.

13. **Healthbar and resource displays.** `ui.healthbar` parameters: `pool_ref: combat.resource_pool_ref` (Brief 167), `display_mode: enum{bar, segments, hearts, text, radial}`, `damage_lerp_speed`, `flash_on_damage`, `low_health_threshold`, `low_health_visual: optional<vfx_ref>`. Subscribes to pool change events; updates at fixed-tick.

14. **Tooltip discipline.** Tooltips are *opt-in* per element via `ui.element.tooltip_ref`. Substrate enforces a minimum delay (default 500ms / 30 ticks) and a screen-edge clamping rule. Tooltip content can be parametric (`"Damage: {damage_amount}, Cooldown: {cooldown_seconds}s"`) using ICU MessageFormat from Brief 220.

15. **Dialog wheel.** Mass Effect / Witcher style. `ui.dialog_wheel` parameters: `choices: set<choice_ref>` (Brief 171.dialogue.node.choice), `wheel_segments: u8`, `radial_arrangement: enum{full, top_half, bottom_half}`, `keep_on_screen: bool`, `paraphrase_kind: enum{full, summary, icon}`. Substrate's wheel auto-paraphrases long lines using Brief 220 short-form locale keys.

16. **Damage numbers and floating text.** `ui.damage_number` parameters: `value`, `damage_type_ref`, `crit: bool`, `position`, `lifetime_ticks`, `motion_curve: motion_curve_ref`, `font_size_scale`, `color_per_type`. Performance-bounded by a per-frame cap (default 64 floating numbers); excess merge into batch counts.

17. **Save and replay.** UI state (which panels are open, current focus, selection state) is part of save/replay so that players resuming from a save see the exact same UI configuration. Modal dialogs are explicitly saved/restored.

18. **v0.1 reach.** All 30 default kinds ship at v0.1. All 5 layout primitives ship. All 4 default themes ship. Accessibility props, screen reader integration via platform APIs, RTL mirroring, font scaling all ship. The Brief 184 UI editor ships at v0.1 with the visual layout surface for all 30 kinds. Custom font loading and ICU layout integration ship.

## Risks identified

1. **Layout solver determinism is hard.** Floating-point tiebreaks, font hinting differences across platforms. Mitigation: integer-quantized metrics, ICU line-break, scalar reference solver only at v0.1.

2. **Accessibility regressions on creator override.** Creators may override default high-contrast pairings with brand colors that fail WCAG. Mitigation: warning at sign time, runtime auto-elevation, but creator can suppress with explicit acknowledgment per Brief 050.

3. **Inventory grid performance.** Large grids (Path of Exile stash) need virtualization. Mitigation: `scroll_view` kind ships virtualization at v0.1; sign-time warning for un-virtualized grids past 1000 cells.

4. **Tooltip flicker on scrolling.** Mitigation: substrate ships hover-stable detection (200ms hover before tooltip shows).

5. **Minimap is a content category.** Minimaps need scene topology data. Mitigation: `ui.minimap` reads `level.scene` (Brief 172) topology directly; shipped at v0.1 for 2D, gated to v0.4 for 3D.

6. **Damage numbers in horde games.** Vampire Survivors fires hundreds per second. Mitigation: per-frame cap with merge/batch behavior at the cap.

## Recommendation

Ship `ui.*` with `ui.element` root, 30 default kinds, 5 layout primitives, deterministic layout solver, 4 default themes, RTL mirroring, font scaling, full accessibility props, and Brief 154 action-bound navigation. Wire to Brief 184 editor and Brief 221 accessibility check at v0.1. Hold 3D minimap to v0.4. Default to high-contrast and large-font-friendly templates so creators ship accessible UI by default.

## Confidence

**4.5/5.** UI primitives are well-grounded in 30+ years of design systems (Material, Apple HIG), web platform standards (CSS, ARIA, ICU), and shipped game UI catalogs. Held back from 5 by layout determinism across font hinting / OS rendering, which needs Round 8 empirical validation.

## Spec impact

- Add `ui.*` namespace with `element`, `layout`, `style`, `theme` and 30 element kinds
- Add accessibility props to every element kind
- Add deterministic integer-quantized layout solver requirement
- Cross-link to Brief 050 (accessibility), Brief 153 (state component), Brief 154 (action navigation), Brief 158 (save UI state), Brief 165 (progression display), Brief 167 (resource pool ref), Brief 169 (loot popup), Brief 170 (quest tracker), Brief 171 (dialog wheel choices), Brief 172 (minimap scene topology), Brief 184 (editor), Brief 220 (LocalKey + ICU), Brief 221 (a11y check)
- Mark 3D minimap deferred to v0.4

## New inventions

- **INV-705** Thirty-kind canonical `ui.*` substrate vocabulary as signed typed gseeds
- **INV-706** Deterministic UI layout solver with integer-quantized text metrics for cross-engine layout reproducibility
- **INV-707** Sign-time WCAG 2.1 AA contrast and font-scale validation as substrate-level accessibility gate
- **INV-708** Action-bound navigation graph composing Brief 154 input layer with auto-derived spatial neighbors
- **INV-709** Substrate-default high-contrast and large-font templates ensuring accessible-by-default UI ship paths

## Open follow-ups

- Layout determinism empirical validation across OS font renderers (Round 8)
- Platform-specific screen reader integration details (Brief 050 follow-up)
- Custom shader effects on UI elements (deferred to v0.4)
- 3D world-space UI / VR UI primitives (deferred to v0.5)

## Sources

1. Material Design specification, Google
2. Apple Human Interface Guidelines, Apple
3. WCAG 2.1 AA specification, W3C
4. ARIA Authoring Practices Guide, W3C
5. ICU Project — line break, MessageFormat, BiDi
6. Game UI Database (gameuidatabase.com)
7. Persona 5 UI design retrospective, Atlus
8. Destiny 2 UI architecture talk, Bungie GDC 2018
9. *Designing Games*, Tynan Sylvester, ch. on UI affordances
10. Brief 050 (this repo) — accessibility/i18n
11. Brief 154 (this repo) — input action layer
12. Brief 220 (this repo, planned) — i18n / ICU
13. Brief 221 (this repo, planned) — accessibility check pipeline
