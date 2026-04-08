# 216 — Moderation and safety

## Question
What is the typed moderation and safety surface that enables substrate creators to handle player reports, content moderation (chat / user-generated content), block and mute lists, ban enforcement, and child safety obligations across the eight engine targets, with federation-friendly distribution and audit trails?

## Why it matters (blast radius)
Multiplayer and user-generated content (Brief 187 mod surface) create moderation obligations the substrate cannot ignore. COPPA, the UK Online Safety Act, the EU DSA, and platform store policies all impose legal duties. Without typed primitives, every creator implements moderation independently, often badly. The brief specifies the typed moderation surface as substrate-provided structure with creator-managed enforcement.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 187 — mod and plugin surface.
- Brief 209 — multiplayer transport.
- Brief 210 — account and identity surface.
- Brief 215 — matchmaking and lobby.

## Findings
1. **Report as typed gseed.** `report.def` declares: typed report kind (harassment / cheating / inappropriate-content / spam / safety-concern / other), reporter identity reference, target identity or content reference, evidence (screenshot / chat log / replay gseed), timestamp, signed by reporter.
2. **Block and mute as typed mutations.** `player.block` and `player.mute` are typed mutations on player identity (Brief 210). Substrate runtime gates communication and matchmaking against blocked players. Block lists are local-first (per-player) by default; creators can opt into federated block lists for cross-game persistence.
3. **Chat moderation pipeline.** Optional `chat.filter.def` declares moderation pipeline: built-in profanity filter (creator-extensible word lists), built-in toxicity classifier (creator-trained or third-party API), or creator custom filter. Substrate provides the typed pipeline; creators choose strictness.
4. **Content moderation for user-generated content.** Brief 187 mods carry typed `content.classification` field declaring: age rating, content warnings, violence/sexual/language flags. Federation distribution gates mod visibility based on player profile.
5. **Ban enforcement.** Typed `ban.action` mutation on player identity declares: scope (per-game / per-creator / federated), duration (timed / permanent), evidence reference. Bans are signed by the creator's identity (Brief 210); federation nodes propagate bans across cooperating creators.
6. **Audit trail.** All moderation actions append to a signed audit log gseed. Audit logs are queryable by creators (and by players for their own actions, per GDPR transparency).
7. **Appeal mechanism.** Typed `ban.appeal` mutation enables players to dispute bans. Appeals are creator-managed; substrate provides the typed channel.
8. **Child safety primitives.** Optional `coppa.profile` field on identity declares the player as under-13 (or regional equivalent). When set, substrate runtime gates: chat is disabled or filtered to whitelist, user-generated content visibility filtered to age-appropriate, telemetry restricted, advertising disabled. Creators with COPPA obligations enable this gate.
9. **Reporting surface UI.** Substrate provides typed UI element template (per Brief 184) for the in-game report flow. Creators get reporting UI for free.
10. **Validation contract.** Sign-time gates: report kinds declared, block / mute / ban primitives present, audit log declared, child-safety profile declared if recipe targets child audiences (typed `recipe.audience` field).
11. **Federation moderation propagation.** Bans, blocks, and mod content classifications propagate via signed federation messages per Brief 210 / 215 federation pattern. Creators choose which other federation nodes to trust for moderation signals.

## Risks identified
- **Toxicity classifier accuracy.** Automated classifiers have false positives. Mitigation: substrate ships the typed pipeline; creators tune strictness; appeals mechanism handles errors.
- **Federation moderation drift.** Creators may disagree on moderation standards. Mitigation: federation propagation is opt-in per signal source; no centralized authority.
- **Legal obligation complexity.** Moderation laws vary by region. Mitigation: substrate documents the typed primitives and the legal landscape; creators are responsible for compliance.
- **Child safety detection.** No reliable way to verify player age. Mitigation: COPPA profile is creator-declared based on creator's compliance posture; substrate provides the gate, not the detection.
- **Reporter abuse.** Mass-reporting can be weaponized. Mitigation: typed rate limits on report submission; report validity verifiable post-hoc via attached evidence.

## Recommendation
Specify moderation and safety as typed `report.def` + `player.block` + `player.mute` + `chat.filter.def` + `ban.action` + `ban.appeal` + `coppa.profile` + `audit.log` gseeds with substrate-shipped reporting UI, creator-tunable filter pipelines, federated moderation propagation, child-safety gates, and audit trails. Creator responsibility for legal compliance is documented.

## Confidence
**4 / 5.** Moderation mechanics are well-precedented; the novelty is the federated moderation propagation pattern with creator-controlled trust signals. Lower than 4.5 because the COPPA profile gating depth needs Phase-1 legal review per region.

## Spec impact
- New spec section: **Moderation and safety specification**.
- Adds typed `report.def`, `player.block`, `player.mute`, `chat.filter.def`, `content.classification`, `ban.action`, `ban.appeal`, `coppa.profile`, `audit.log`, `recipe.audience` gseed kinds.
- Adds the substrate reporting UI element template.
- Adds federation moderation propagation contract.
- Cross-references Briefs 152, 184, 187, 209, 210, 215.

## New inventions
- **INV-928** — Typed `report.def` with structured kinds and signed evidence: player reports are first-class substrate primitives with auditable evidence chains.
- **INV-929** — Typed `player.block` / `player.mute` mutations on identity with local-first default and federated opt-in: block lists are substrate-managed, federation-aware.
- **INV-930** — Typed `chat.filter.def` pipeline with built-in profanity / toxicity classifiers and creator-extension: chat moderation is structured creator choice with substrate-shipped defaults.
- **INV-931** — Typed `content.classification` field on Brief 187 mods with federation visibility gating: user-generated content is age-flagged as a substrate primitive.
- **INV-932** — Typed `ban.action` with scope (per-game / per-creator / federated) and signed audit: bans are first-class substrate state, propagable via federation.
- **INV-933** — Typed `coppa.profile` gate disabling chat / UGC / telemetry / advertising for under-13 players: child safety is a substrate primitive enabled per recipe audience declaration.
- **INV-934** — Substrate reporting UI element template via Brief 184: in-game report flow is provided, not creator-built.
- **INV-935** — Federation moderation propagation with opt-in trust per signal source: cross-creator moderation is federation-friendly, no centralized authority.
- **INV-936** — Typed `audit.log` gseed for all moderation actions with player-readable transparency per GDPR: moderation is auditable.

## Open follow-ups
- Phase-1 legal review per region (US / EU / UK / Asia).
- Toxicity classifier model selection — deferred to v0.2.
- Voice chat moderation primitives — deferred to v0.3.
- Streamer mode (anonymized opponents) — deferred to v0.3.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 184 — UI / HUD layout editor.
3. Brief 187 — Mod and plugin surface.
4. Brief 210 — Account and identity surface.
5. COPPA (Children's Online Privacy Protection Act, US).
6. UK Online Safety Act 2023.
7. EU Digital Services Act (DSA).
8. Perspective API (Google Jigsaw toxicity classifier).
9. ESRB / PEGI age rating systems.
