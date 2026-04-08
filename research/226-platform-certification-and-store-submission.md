# 226 — Platform certification and store submission

## Question
What is the typed platform certification and store submission surface that enables substrate creators to package, sign, and submit substrate-built games to Steam, Epic Games Store, GOG, Itch.io, App Store, Google Play, Microsoft Store, Xbox, PlayStation, Nintendo Switch, and Web — meeting each platform's technical and content certification requirements with creator-actionable pre-flight checks?

## Why it matters (blast radius)
Submission requirements differ wildly across platforms. Console certification (TRC / TCR / Lotcheck) is notoriously hard. Without typed certification primitives, creators discover certification failures after weeks of submission cycles. With typed pre-flight gates, the substrate flags certification issues at sign-time before submission, dramatically shortening the iteration loop.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 188-195 — engine export pipelines.
- Brief 213 — monetization primitives.
- Brief 225 — accessibility surface.

## Findings
1. **Typed `submission.target` gseed.** Each store / platform target is a typed `submission.target` gseed declaring: store name, store SKU type, required artifacts (binary / icon / screenshots / metadata), required certifications, content rating system, age rating, manifest format.
2. **Per-platform requirement registry.** Substrate ships typed requirement gseeds for the 11 platforms (Steam, Epic, GOG, Itch, App Store iOS / iPadOS / macOS, Google Play, Microsoft Store, Xbox, PlayStation, Nintendo Switch, Web). Each requirement is a typed sign-time gate.
3. **`gspl certify <target>` subcommand.** CLI subcommand runs the per-platform certification gate set against the project. Reports failures with creator-actionable hints. Supports `--all` to run all targets.
4. **Console certification depth.** For Xbox / PlayStation / Switch, substrate ships TRC / TCR / Lotcheck checklists as typed gates. Examples: required pause behavior on focus loss, controller disconnect handling, save data corruption recovery, error message formatting standards, suspend/resume behavior. Substrate runtime structurally implements many; remainder are sign-time gated.
5. **Content rating integration.** Substrate ships typed `content.rating` gseed referencing IARC (International Age Rating Coalition) questionnaire answers. IARC generates ESRB / PEGI / CERO / USK / ClassInd ratings automatically from one questionnaire. Substrate exports IARC payload per submission.
6. **Store metadata as typed gseed.** Per-store metadata (description, screenshots, video trailers, tags, pricing per region from Brief 213) is typed `store.listing` gseed with per-store schema. One source of truth across stores.
7. **Binary signing per platform.** Each platform requires platform-specific code signing (Apple Developer ID, Windows Authenticode, Xbox certs). Substrate documents the signing flow per platform; substrate runs the signing as a `gspl sign --target <store>` step.
8. **Submission package generation.** `gspl submit <target> --package` generates the platform-specific submission archive (ipa / aab / msix / Steam depot / etc.) with all required artifacts. Output is signed and content-addressed.
9. **EULA and privacy policy gating.** Sign-time gate checks each platform's required legal documents (EULA, privacy policy, COPPA disclosure if applicable). Substrate ships templates; creators customize.
10. **Region-specific compliance.** Typed gates per region: German UCK content rules (no swastikas in non-art context), Australian R18+ rules, China's content rules (no skeletons / no alcohol). Creators flag affected regions; substrate gates.
11. **Crash reporting submission.** Console certification often requires crash data submission. Substrate ships typed `crash.report.adapter` for each platform's crash service.
12. **Pre-flight summary report.** `gspl certify --report` generates an HTML report listing all gates per target with pass / fail / skip / warn status. Useful for sharing with publishing partners.
13. **Validation contract.** Sign-time gates: at least one submission target declared per shippable build, required artifacts present, content rating completed, EULA / privacy policy referenced, store listing complete, signing identity declared.

## Risks identified
- **Console SDK access.** Console certification requires the platform's proprietary SDK (NDA-gated). Mitigation: substrate ships the typed gate definitions publicly; SDK integration is creator's responsibility post-licensing.
- **Requirement drift.** Platforms update requirements frequently. Mitigation: substrate ships requirement gseeds versioned; updates ship as substrate version bumps; creators pin substrate version to lock requirements.
- **False-pass risk.** Substrate gates can pass when platform manual review still rejects. Mitigation: gates are necessary, not sufficient; documentation states this clearly.
- **Web target ambiguity.** Web has no formal cert; substrate documents browser compatibility matrices instead.
- **IARC questionnaire complexity.** IARC has many edge cases. Mitigation: substrate ships the typed questionnaire structure; creators answer; IARC payload generated automatically.

## Recommendation
Specify platform certification as typed `submission.target` + per-platform requirement gseeds + `content.rating` IARC integration + `store.listing` typed metadata + `gspl certify` / `gspl submit` subcommands across the 11 platforms. Substrate gates surface certification failures at sign-time, dramatically shortening the submission iteration loop.

## Confidence
**4 / 5.** Per-platform certification mechanics are well-documented but vary across platforms. The novelty is the typed sign-time gate set unifying the 11 platforms behind one substrate surface. Lower than 4.5 because console SDK integration is NDA-gated and requires Phase-1 partner access.

## Spec impact
- New spec section: **Platform certification and store submission specification**.
- Adds typed `submission.target`, `content.rating`, `store.listing`, `crash.report.adapter` gseed kinds.
- Adds the 11 per-platform requirement gseed sets.
- Adds the `gspl certify` and `gspl submit` subcommand contracts.
- Adds IARC integration.
- Cross-references Briefs 152, 188-195, 213, 225.

## New inventions
- **INV-1016** — Typed `submission.target` with per-platform requirement gseed sets across 11 platforms: store certification is structured creator declaration.
- **INV-1017** — Console TRC / TCR / Lotcheck checklist as typed sign-time gates: console certification is sign-time gated, not post-submission discovered.
- **INV-1018** — IARC questionnaire integration generating ESRB / PEGI / CERO / USK / ClassInd ratings from one source: content rating is one-source-of-truth.
- **INV-1019** — Typed `store.listing` gseed with one-source-of-truth metadata across stores: store description / screenshots / pricing live in substrate, not duplicated per store.
- **INV-1020** — `gspl certify <target>` running typed gate set per platform with creator-actionable hints: certification iteration loop shortens from weeks to minutes.
- **INV-1021** — Region-specific compliance gates (German UCK, Australian R18+, China content): regional content rules are sign-time gated.
- **INV-1022** — Typed substrate-implemented console requirements (pause-on-focus-loss, controller disconnect, suspend/resume): substrate runtime structurally satisfies many cert requirements.
- **INV-1023** — Pre-flight HTML certification report via `gspl certify --report`: certification status is shareable with publishing partners.
- **INV-1024** — Substrate-shipped `crash.report.adapter` per platform crash service: console crash reporting requirements are substrate-handled.

## Open follow-ups
- Phase-1 console SDK partner access.
- Per-platform submission UX testing — Phase 1.
- Auto-screenshot generation from playtest sessions — deferred to v0.3.
- Localized store listings via Brief 224 — Phase 1.
- Marketing asset generation — deferred to v0.4.
- Phase-1 IARC questionnaire UX.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 188-195 — Engine export pipelines.
3. Brief 213 — Monetization primitives.
4. Steam Partner documentation.
5. Apple App Store Review Guidelines.
6. Google Play Developer Policies.
7. Microsoft Store Policies.
8. Xbox Requirements (XR) public documentation.
9. PlayStation TRC public summaries.
10. Nintendo Lotcheck public documentation.
11. IARC International Age Rating Coalition.
12. ESRB / PEGI / CERO / USK / ClassInd rating systems.
