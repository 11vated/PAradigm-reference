# 212 — Live content and update pipeline

## Question
What is the typed live-content and update pipeline that enables substrate creators to ship content updates, balance patches, seasonal events, and hotfixes to a deployed game without requiring players to redownload the full client, and with deterministic rollback if an update breaks?

## Why it matters (blast radius)
Live-service games are the largest revenue category in modern games. Without a live-content pipeline, the substrate cannot serve this category and creators face a forced binary between "static game" and "build your own update infrastructure." Brief 187's mod surface gets close — this brief specifies the live-update pattern as a first-class substrate primitive.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 158 — save snapshot model.
- Brief 187 — mod and plugin surface.
- Brief 196 — cross-engine parity test suite.
- Brief 210 — account and identity surface.

## Findings
1. **Update as typed signed gseed bundle.** A live update is a `update.bundle` typed gseed declaring: substrate-version compatibility, content gseeds added, content gseeds replaced, content gseeds removed, balance parameter overrides, server-deployment timestamp, signed creator manifest.
2. **Update delivery channel.** Substrate ships a `update.channel` typed primitive backed by HTTPS + content addressing. Clients poll the channel on launch (and optionally periodically); new bundles download in background; player chooses when to apply.
3. **Reuses Brief 187 mod surface.** Mod surface already specifies signed-gseed-bundle loading with capability manifests. Live updates are functionally a special-case mod published by the original creator with full capability claim.
4. **Hot-reload via playtest harness.** Brief 187's hot-reload through playtest harness extends to live updates: players can reload an update without restarting the game (subject to creator opt-in).
5. **Deterministic rollback.** Each applied update is recorded in the player's lineage as a typed `update.apply` mutation; rollback emits the inverse `update.revert` mutation. Save state is preserved across rollback because save chunks are content-addressed and content-versioned (Brief 158).
6. **Server-side deploy.** Multiplayer games (Brief 209) require server-side deploy synchronization. Substrate ships a typed `server.deploy` workflow ensuring all server instances apply the update before clients can submit gameplay against the new version.
7. **Balance hotfixes as parameter overrides.** Most live updates are balance changes — adjusting numbers, not adding content. Substrate's typed parameter system makes hotfixes structurally simple: an update bundle can ship as a typed parameter override map without any new gseeds.
8. **A/B testing primitive.** `update.experiment` typed gseed declares: cohort assignment rule, parameter override variants, observation metrics. Substrate runtime applies the relevant variant per player. Results aggregate via Brief 211 leaderboard infrastructure.
9. **Seasonal event as scheduled update.** `update.schedule` field declares activation/deactivation timestamps. Seasonal events activate automatically and revert automatically without creator manual intervention.
10. **Validation contract.** Sign-time gates: update bundle is signed by creator with valid identity (Brief 210), substrate-version compatibility declared, replaced gseeds preserve typed schemas (no breaking schema changes without explicit migration).
11. **Migration support.** Schema-breaking updates declare typed migrations: how to convert old save data to new format. Migrations are typed mutations; substrate runtime applies them on first launch with the new bundle.

## Risks identified
- **Update breakage.** A bad update can crash the game. Mitigation: deterministic rollback to prior bundle; substrate runtime falls back automatically on repeated crash detection.
- **Rollback save corruption.** Rollback requires save state to remain compatible with prior bundle. Mitigation: save chunks are content-versioned; updates declare which chunks they touch; rollback only restores compatible chunks.
- **Server/client version skew.** Multiplayer with mixed versions is dangerous. Mitigation: server gates client connections by substrate-version and bundle-version compatibility.
- **A/B test fairness.** Players in different cohorts have different game experiences. Mitigation: leaderboards scope by cohort to prevent cross-cohort comparison; documented as creator responsibility to disclose experimentation.
- **Update channel hosting cost.** CDN bandwidth for content updates costs money. Mitigation: substrate provides the typed primitive but does not host; creators use any HTTPS-accessible CDN.

## Recommendation
Specify the live content and update pipeline as a typed `update.bundle` gseed reusing Brief 187's mod surface mechanics, with HTTPS + content-addressing delivery, deterministic rollback via lineage, server-side deploy synchronization for multiplayer, balance hotfixes via typed parameter overrides, A/B testing primitive, and seasonal scheduling. Substrate provides the typed primitives; CDN hosting is creator-managed.

## Confidence
**4 / 5.** Live-update mechanics are well-precedented; the novelty is the deterministic rollback via lineage and the typed parameter override pattern for balance hotfixes. Lower than 4.5 because rollback save compatibility under heavy modification needs Phase-1 measurement.

## Spec impact
- New spec section: **Live content and update pipeline specification**.
- Adds typed `update.bundle`, `update.apply`, `update.revert`, `update.channel`, `update.experiment`, `server.deploy` gseed kinds.
- Adds the typed schema migration contract.
- Adds the A/B testing cohort primitive.
- Cross-references Briefs 152, 158, 187, 209, 210, 211.

## New inventions
- **INV-899** — Typed `update.bundle` gseed reusing mod-surface mechanics for live content delivery: live updates are first-class signed substrate artifacts, not opaque patch files.
- **INV-900** — Deterministic rollback via lineage: failed updates revert via inverse `update.revert` mutation; save state preserved via content-versioned chunks.
- **INV-901** — Typed parameter override map for balance hotfixes: most live updates ship as structured parameter changes, not new content, enabling lightweight hotfix delivery.
- **INV-902** — Server-side deploy synchronization for multiplayer: substrate enforces server-cluster version consistency before allowing client connections against new versions.
- **INV-903** — Typed `update.experiment` A/B testing primitive with cohort assignment and observation metrics: experimentation is a substrate primitive with leaderboard scoping for fairness.
- **INV-904** — Typed schema migration contract for breaking updates: schema-breaking changes ship with declarative migrations applied automatically on first launch.
- **INV-905** — Typed `update.schedule` for seasonal event activation/deactivation: time-bound content is a substrate primitive, not creator-scheduling code.
- **INV-906** — Automatic crash-detection rollback via repeated crash watchdog: substrate runtime auto-reverts to prior bundle on detected instability.

## Open follow-ups
- Phase-1 rollback under heavy modification.
- Update bundle hosting recommendations (CDN cost analysis) — deferred to v0.2.
- Cross-platform update synchronization (Steam + console) — deferred to v0.4.
- Differential update bundles (only changed bytes) — deferred to v0.3.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 158 — Save snapshot model.
3. Brief 187 — Mod and plugin surface.
4. Brief 209 — Multiplayer transport.
5. Brief 210 — Account and identity surface.
6. Brief 211 — Leaderboards and achievements.
7. Steamworks update API documentation.
8. Apple TestFlight / Google Play update channel models.
