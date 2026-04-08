# 225 — Accessibility surface

## Question
What is the typed accessibility surface that enables substrate creators to ship games meeting WCAG 2.1 AA, CVAA, and platform certification (Xbox / PlayStation / Nintendo) requirements — covering colorblind modes, subtitles and closed captions, remappable controls, screen reader integration, motion reduction, audio cues, and difficulty options — across the eight engine targets without per-creator implementation?

## Why it matters (blast radius)
~20% of players have a disability that affects gameplay. Platform certification requires accessibility features for shipping. The CVAA, EAA, and equivalent regulations make accessibility legally mandatory in many regions. Without typed primitives, every creator implements ad-hoc accessibility (or doesn't). With typed primitives, accessibility is structurally provided and the substrate's gates make missing features visible.

## What we know from the spec
- Brief 174 — UI and HUD pattern library.
- Brief 180 — dialogue and quest editor.
- Brief 184 — UI and HUD layout editor.
- Brief 216 — moderation and safety.

## Findings
1. **Typed `accessibility.profile` gseed.** Each player carries a typed profile declaring active accessibility settings: colorblind mode (none / protanopia / deuteranopia / tritanopia / achromatopsia), high contrast, font scale, reduce motion, screen shake disabled, subtitle settings, audio description, control remap, difficulty modifier set.
2. **Subtitles and closed captions.** Typed `subtitle.def` and `caption.def` gseeds. Subtitles transcribe speech; captions add non-speech audio cues ("[door creaks]"). Both reference Brief 224 `string.def` for localization. UI element template ships rendering with creator-customizable position / size / background opacity / per-speaker color.
3. **Colorblind palettes.** Substrate runtime applies typed colorblind transformation matrices to rendered output (post-process). Three palette types pre-shipped (deuteranopia / protanopia / tritanopia). Critical UI elements carry typed `color.critical` flag and substrate verifies sufficient contrast in each colorblind palette at sign-time.
4. **High contrast and font scaling.** UI element template (Brief 184) supports typed `contrast.profile` and `font.scale` fields. High contrast swaps to creator-declared high-contrast variant; font scale 0.75x to 2.0x without layout breakage (UI element template has typed reflow behavior).
5. **Remappable controls.** Brief 184 input bindings are typed gseeds. Players remap via typed `input.binding.override` mutation on their profile. Substrate runtime resolves bindings through the override layer at runtime. Multiple controller schemes (default, left-handed, one-handed) ship as substrate templates.
6. **Screen reader integration.** Substrate runtime exposes a typed `screen.reader.surface` per engine target: UI element label / role / state are queryable by platform screen readers (UIA on Windows, NSAccessibility on macOS, AccessKit on Linux, native Switch / PS / Xbox APIs). Substrate ships AccessKit wrapped per engine target.
7. **Reduce motion.** Typed `motion.profile` field on animation gseeds (Brief 179) declares: full / reduced / none. Player profile selects motion level; substrate runtime gates animations accordingly. Camera shake, screen flashes, and parallax effects respect the motion profile.
8. **Audio cues.** Typed `audio.cue` gseeds tag critical visual events with optional audio cue alternatives. When `accessibility.profile.audio_description = on`, substrate plays the cue. Useful for players with visual impairments.
9. **Photosensitivity protection.** Typed `flash.policy` gate flags content exceeding the W3C photosensitive epilepsy threshold (>3 flashes per second). Sign-time gate fires at validation; ship-time forces creator acknowledgment.
10. **Difficulty modifiers.** Typed `difficulty.def` gseed declares typed modifier set: damage taken, damage dealt, time scale, auto-aim strength, infinite resources, etc. Players select modifier combinations from the substrate-provided UI. Creators declare which modifiers their game supports.
11. **Cognitive accessibility.** Typed `cognitive.profile` declares: simplified language, reduced complexity, longer time limits, skip-puzzle option, reading speed adjustment for dialogue (Brief 180).
12. **Sign-time accessibility audit.** `gspl validate --accessibility` runs the accessibility audit: missing subtitles, missing colorblind variants, photosensitive content, missing alt text, missing remap support. Reports with creator-actionable hints.
13. **Validation contract.** Sign-time gates: dialogue gseeds have subtitle gseeds, UI elements declare role / label / state, critical color elements pass colorblind contrast check, animations declare motion profile, control bindings remappable.

## Risks identified
- **Per-engine screen reader integration.** Eight engine targets, each with platform-specific screen reader API. Mitigation: AccessKit wrapper provides cross-platform abstraction; engine export pipelines integrate AccessKit per target.
- **Difficulty modifier balance.** Modifiers can break game balance. Mitigation: substrate documents typed difficulty composition rules; creators define which modifier combinations are supported.
- **Photosensitivity false positives.** Gate may flag non-harmful flashes. Mitigation: gate is advisory by default with typed creator override; ship-time gate forces explicit acknowledgment.
- **Audio description authoring burden.** Audio cues per visual event are creator effort. Mitigation: substrate ships default cue library for common events; creators add custom cues for unique events.

## Recommendation
Specify accessibility as typed `accessibility.profile` + `subtitle.def` + `caption.def` + `colorblind.palette` + `motion.profile` + `audio.cue` + `flash.policy` + `difficulty.def` + `cognitive.profile` gseeds with substrate-shipped AccessKit screen reader integration per engine target, sign-time accessibility audit, and player-controllable settings UI. Substrate makes accessibility structural, not optional.

## Confidence
**4.5 / 5.** Accessibility patterns are well-precedented (W3C WCAG, Game Accessibility Guidelines, AccessKit). The novelty is the sign-time accessibility audit gating ship and the typed colorblind contrast verification. Lower than 5 because per-platform certified screen reader integration needs Phase-1 measurement.

## Spec impact
- New spec section: **Accessibility surface specification**.
- Adds the 9 typed accessibility gseed kinds.
- Adds AccessKit dependency per engine target.
- Adds typed colorblind transformation matrices.
- Adds the `gspl validate --accessibility` audit subcommand mode.
- Cross-references Briefs 174, 179, 180, 184, 224.

## New inventions
- **INV-1004** — Typed `accessibility.profile` gseed unifying all accessibility settings as substrate-managed player state: accessibility is first-class typed primitive.
- **INV-1005** — Typed `subtitle.def` / `caption.def` with Brief 224 string integration: all speech / audio events have structural subtitle paths.
- **INV-1006** — Substrate-applied colorblind palette transformations with typed `color.critical` flag and sign-time contrast verification: critical UI is colorblind-correct by structural gate.
- **INV-1007** — UI element template with typed `contrast.profile` and `font.scale` fields with reflow guarantees: high-contrast and large-text are first-class without layout breakage.
- **INV-1008** — Typed `input.binding.override` on player profile with substrate-resolved binding chain: control remapping is substrate-managed, not creator-implemented.
- **INV-1009** — AccessKit wrapped per engine target as substrate's screen reader integration: cross-platform screen reader support is substrate-provided.
- **INV-1010** — Typed `motion.profile` field on animation gseeds with player-profile-driven runtime gating: motion-sickness accommodation is structural.
- **INV-1011** — Typed `audio.cue` alternative tags on critical visual events: audio description is a substrate primitive.
- **INV-1012** — Typed `flash.policy` photosensitivity gate with sign-time creator acknowledgment: epilepsy protection is structural, not opt-in.
- **INV-1013** — Typed `difficulty.def` modifier composition with player-controllable modifier UI: difficulty options are substrate-provided, not creator-implemented.
- **INV-1014** — Typed `cognitive.profile` for simplified language, time extensions, skip-puzzle: cognitive accessibility is first-class.
- **INV-1015** — `gspl validate --accessibility` audit with creator-actionable hint output: missing accessibility features are visible at sign-time.

## Open follow-ups
- Per-platform certification documentation (Xbox / PS / Nintendo) — Phase 1.
- Lip-sync visualization for deaf players — deferred to v0.3.
- Sign language video integration — deferred to v0.4.
- Auto-difficulty adjustment from player behavior — deferred to v0.4.
- Eye-tracking input adapter — deferred to v0.4.

## Sources
1. Brief 174 — UI and HUD pattern library.
2. Brief 184 — UI and HUD layout editor.
3. WCAG 2.1 (W3C).
4. CVAA (US Communications and Video Accessibility Act).
5. Game Accessibility Guidelines (gameaccessibilityguidelines.com).
6. AccessKit cross-platform accessibility library.
7. Microsoft Inclusive Design Toolkit.
8. Xbox Accessibility Guidelines (XAG).
9. PlayStation 5 accessibility certification requirements.
10. W3C photosensitive epilepsy guidelines.
