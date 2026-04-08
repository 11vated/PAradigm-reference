# 224 — Localization and internationalization

## Question
What is the typed localization and internationalization surface that enables substrate creators to author games in multiple languages with translated strings, locale-aware formatting (dates / numbers / currency), bidirectional text (Arabic / Hebrew), CJK font support, and context-tagged translation keys — across the eight engine targets with substrate-shipped fallback semantics?

## Why it matters (blast radius)
Localization touches every text-bearing surface in a substrate game: dialogue (Brief 180), UI (Brief 184), achievements (Brief 211), monetization (Brief 213), error messages (Brief 216), tutorial (Brief 174). Without typed l10n primitives, every creator implements their own string table, translation drifts from source, and bidirectional text breaks UI layout. With typed l10n, every creator-facing string is structurally translatable.

## What we know from the spec
- Brief 180 — dialogue and quest editor.
- Brief 184 — UI and HUD layout editor.
- Brief 211 — leaderboards and achievements.
- Brief 213 — monetization primitives.
- Brief 216 — moderation and safety.

## Findings
1. **Typed `string.def` gseed.** Every creator-facing string is a typed `string.def` with: typed key (namespaced), default-locale text, ICU MessageFormat parameters, context note, max length budget, surface tag (UI / dialogue / achievement / error). Strings authored in code as references to keys, not literal text.
2. **Typed `locale.def` gseed.** Each supported locale is a `locale.def` declaring: BCP 47 tag (e.g., `en-US`, `ja-JP`, `ar-SA`), text direction (LTR / RTL), date format pattern, number format pattern, currency format pattern, plural rule set, fallback locale chain.
3. **Translation gseeds.** Translations are typed `string.translation` gseeds keyed by `(locale, string.def key)` pair. Lineage records translator identity. Diff between source string version and translation version flags stale translations.
4. **ICU MessageFormat.** Substrate uses ICU MessageFormat (industry standard) for parameter substitution and pluralization. `{count, plural, one {1 item} other {# items}}` semantics. Substrate ships an ICU runtime per engine target.
5. **Bidirectional text.** Substrate runtime handles Unicode bidirectional algorithm (UAX #9) for RTL text. UI element layout (Brief 184) flips for RTL locales automatically; creators can override per element via typed `ui.bidi.policy` field.
6. **CJK font handling.** Substrate ships fallback font configuration mapping locale to recommended font set. Creators ship the fonts; substrate handles the per-locale font selection and shaping (HarfBuzz wrapped).
7. **Context tagging.** Each `string.def` carries a typed context note for translators ("button label, max 12 characters" / "error message shown after failed save"). Eliminates the dominant translation-error pattern.
8. **Translation completeness gates.** Sign-time gate checks each declared locale has translations for every string with completeness >= typed threshold (default 100% for ship; 50% for beta locales). Missing translations fall back to next locale in chain.
9. **Pseudolocale.** Substrate ships a typed `pseudo.locale` (`en-XA` style) that wraps strings with accents and expansion to expose layout / truncation bugs. Creators run the pseudolocale build to catch i18n bugs without translators.
10. **Translation export / import.** `gspl translate export <locale>` emits XLIFF or PO format; `gspl translate import <file>` ingests. Industry-standard formats for translator tooling integration.
11. **Locale-aware formatting.** Substrate runtime exposes typed `format.date`, `format.number`, `format.currency` substrate calls that respect the active locale. Eliminates the dominant `MM/DD/YYYY` vs `DD/MM/YYYY` bug class.
12. **Validation contract.** Sign-time gates: every UI text references a `string.def` (no literal strings in shippable surfaces), declared locales have minimum completeness, ICU MessageFormat strings parse, plural rules cover all forms required by locale, fonts available for declared locales.

## Risks identified
- **CJK font size.** CJK fonts can exceed 10MB. Mitigation: substrate ships subset-extraction tooling — only ship glyphs actually used in the project.
- **Pseudolocale coverage.** Pseudolocale catches layout but not semantic bugs. Mitigation: documents the limitation; recommends real translation review for ship locales.
- **Translation drift.** Source strings change after translation completes. Mitigation: typed source-version field on `string.translation`; mismatched versions flagged in build.
- **Plural rule complexity.** Some locales (Arabic, Russian) have 6+ plural forms. Mitigation: ICU MessageFormat handles all CLDR plural rules natively.
- **Font licensing.** Some fonts forbid embedding. Mitigation: substrate documents font licensing categories; creators select appropriately licensed fonts.

## Recommendation
Specify localization as typed `string.def` + `locale.def` + `string.translation` gseeds with ICU MessageFormat parameter substitution, Unicode bidirectional algorithm support, CJK font fallback configuration, context tagging, completeness gates, pseudolocale, XLIFF / PO export-import, and locale-aware formatting calls. Substrate ships ICU and HarfBuzz wrapped per engine target.

## Confidence
**4.5 / 5.** Localization is well-precedented (gettext / ICU / Fluent). The novelty is the typed `string.def` integration with substrate sign-time gates structurally enforcing translation completeness. Lower than 5 because per-engine ICU integration overhead needs Phase-1 measurement.

## Spec impact
- New spec section: **Localization and internationalization specification**.
- Adds typed `string.def`, `locale.def`, `string.translation`, `pseudo.locale` gseed kinds.
- Adds the ICU MessageFormat dependency per engine target.
- Adds the HarfBuzz dependency for CJK / complex script shaping.
- Adds typed `format.date` / `format.number` / `format.currency` substrate calls.
- Cross-references Briefs 180, 184, 211, 213, 216.

## New inventions
- **INV-994** — Typed `string.def` gseed making every creator-facing string a structural primitive: literal strings in shippable surfaces are sign-time forbidden.
- **INV-995** — Typed `locale.def` with BCP 47 tag, text direction, format patterns, plural rules, and fallback chain: locales are first-class substrate primitives.
- **INV-996** — Typed `string.translation` gseed with translator identity in lineage and source-version tracking: translation drift is structurally detectable.
- **INV-997** — ICU MessageFormat as substrate's pluralization and parameter substitution standard: industry-standard semantics, no creator reinvention.
- **INV-998** — Substrate-handled Unicode bidirectional algorithm with auto UI flipping for RTL: bidi correctness is substrate runtime, not creator implementation.
- **INV-999** — Typed context tagging on every translatable string: translator errors from missing context are eliminated.
- **INV-1000** — Sign-time translation completeness gate with typed thresholds per locale: incomplete translations cannot ship accidentally.
- **INV-1001** — Substrate-shipped pseudolocale (`en-XA`) for layout / truncation bug detection: i18n testing without translators is structural.
- **INV-1002** — XLIFF / PO export-import via `gspl translate` for translator tooling integration: substrate composes with the existing translation industry.
- **INV-1003** — Locale-aware `format.date` / `format.number` / `format.currency` substrate calls: locale formatting bugs are eliminated by construction.

## Open follow-ups
- Voice-over localization with lip-sync — deferred to v0.3.
- Regional content gating (e.g., German blood removal) — deferred to v0.3.
- Phase-1 CJK font subset tooling.
- Legal compliance per region (rating boards, content rules) — Phase 1 documentation.
- Machine translation pre-fill for translator tooling — deferred to v0.4.

## Sources
1. Brief 180 — Dialogue and quest editor.
2. Brief 184 — UI and HUD layout editor.
3. ICU User Guide (Unicode Consortium).
4. Unicode Standard Annex #9 (Bidirectional Algorithm).
5. CLDR (Common Locale Data Repository).
6. HarfBuzz documentation.
7. BCP 47 — Tags for Identifying Languages.
8. XLIFF 2.1 specification (OASIS).
9. gettext PO format.
10. Mozilla Fluent localization system.
