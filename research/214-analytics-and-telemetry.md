# 214 — Analytics and telemetry

## Question
What is the typed analytics and telemetry surface that enables substrate creators to collect player behavior data, performance metrics, and balance signals across the eight engine targets, with privacy-preserving defaults, creator-controlled data retention, and no centralized substrate-hosted collection service?

## Why it matters (blast radius)
Analytics drive every modern game's iteration loop. Without typed primitives, every creator integrates Mixpanel / Amplitude / GameAnalytics independently, leaks PII, and the substrate's privacy story breaks at the analytics edge. The brief specifies a typed event surface with creator-managed sinks.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 185 — playtest harness (lineage as test fixture).
- Brief 210 — account and identity surface (PII boundary).
- Brief 212 — live content pipeline (A/B testing primitive).

## Findings
1. **Analytics as typed event stream.** `analytics.event.def` declares: typed event name, typed payload schema (no free-form JSON), associated identity scope (anonymous-id-only / authenticated). Substrate runtime emits events as typed gseeds; events sink to a creator-configured destination.
2. **Sink adapter pattern.** `analytics.sink.adapter` typed gseed declares the destination: built-in adapters for Mixpanel, Amplitude, GameAnalytics, PostHog, Plausible, plus a creator-extensible adapter for custom sinks (REST endpoint, S3 bucket, local file). Substrate handles the platform-specific flow per engine target.
3. **Privacy-preserving defaults.** v0.1 ships with telemetry **off by default**. Creators must explicitly enable telemetry, declare which event kinds they collect, and surface the consent prompt to players via a substrate-provided typed UI element. Players can opt out per-session and per-event-kind.
4. **PII boundary.** Identity scope is typed: `anonymous-id-only` events use a per-installation UUID with no link to player identity; `authenticated` events use the Brief 210 identity reference. Substrate validates that no event payload contains PII patterns (email regex, name fields) at sign-time.
5. **Built-in event categories.** Substrate ships ~20 typed event categories covering common analytics needs: session-start, session-end, level-start, level-complete, level-fail, purchase, achievement-unlocked, error, performance-sample, custom-creator-event. Creators extend via `analytics.event.def` for game-specific events.
6. **Lineage-derived analytics.** Brief 185's playtest lineage is itself a high-fidelity analytics source. Substrate provides typed `analytics.from_lineage` query primitive: creators can derive analytics from signed playtest fixtures without runtime telemetry.
7. **Performance telemetry.** Substrate runtime emits typed performance samples (frame time, memory, load time) per session. Sample rate is creator-configurable. Sink adapters route to performance-monitoring tools (Sentry, Datadog) via creator configuration.
8. **A/B test integration.** Brief 212's `update.experiment` cohort assignments emit as typed analytics events automatically, enabling experiment result aggregation in the chosen sink.
9. **Sample rate / aggregation.** Telemetry can be expensive at scale. Substrate provides typed sample rates per event kind and on-device aggregation (count + bucket + flush) to reduce sink calls.
10. **Validation contract.** Sign-time gates: telemetry off by default, all events declared with typed schemas, no PII patterns in payloads, consent UI element present if telemetry enabled, sink adapter declared.
11. **Right to deletion.** Players can request data deletion. Substrate provides typed `analytics.deletion_request` mutation that the creator's sink adapter must honor. GDPR compliance is creator-responsibility but substrate provides the typed primitive.

## Risks identified
- **Creator data hoarding.** Creators may collect excessive data. Mitigation: substrate's typed schemas force declaration; the substrate community can audit which creators collect what.
- **PII leakage in custom events.** Creators can inadvertently log PII in custom events. Mitigation: sign-time pattern detection rejects email/name regex matches; documented as creator responsibility for non-pattern PII.
- **Sink reliability.** Sink failures can crash the game. Mitigation: substrate buffers events locally and retries asynchronously; sink failures never block the game loop.
- **Cross-platform consistency.** Telemetry must work across all eight engines. Mitigation: substrate event emission is engine-agnostic; sink adapters are engine-agnostic via HTTP.
- **Consent fatigue.** Players ignore consent prompts. Mitigation: substrate provides typed minimal-consent UI; creators are responsible for clear copy.

## Recommendation
Specify analytics and telemetry as typed `analytics.event.def` + `analytics.sink.adapter` gseeds with telemetry-off-by-default privacy-preserving stance, 20 substrate-shipped event categories, 5 built-in sink adapters, PII boundary at the substrate edge, lineage-derived analytics as alternative to runtime telemetry, performance sampling, and typed deletion request primitive.

## Confidence
**4 / 5.** Analytics mechanics are well-precedented; the novelty is the typed schema enforcement and the lineage-derived analytics pattern bypassing runtime telemetry entirely. Lower than 4.5 because the creator-extensible sink adapter pattern needs Phase-1 validation for performance under high event volume.

## Spec impact
- New spec section: **Analytics and telemetry specification**.
- Adds typed `analytics.event.def`, `analytics.sink.adapter`, `analytics.from_lineage`, `analytics.deletion_request` gseed kinds.
- Adds the typed consent UI element template.
- Adds telemetry-off-by-default policy.
- Cross-references Briefs 152, 185, 210, 212.

## New inventions
- **INV-914** — Typed `analytics.event.def` with declared payload schemas: analytics events are first-class typed substrate primitives, not free-form JSON streams.
- **INV-915** — Five built-in sink adapters (Mixpanel / Amplitude / GameAnalytics / PostHog / Plausible) shipped per substrate release: sink integration is substrate-managed.
- **INV-916** — Telemetry-off-by-default policy with explicit creator opt-in and player consent UI: privacy is the substrate default, not the substrate exception.
- **INV-917** — Sign-time PII pattern detection in event payloads: email / name regex matches are rejected before runtime, closing inadvertent PII leakage.
- **INV-918** — Lineage-derived analytics via `analytics.from_lineage` query primitive: substrate's signed playtest lineage is a high-fidelity analytics source bypassing runtime telemetry entirely.
- **INV-919** — Local event buffering with async retry preventing sink failures from blocking gameplay: telemetry never affects player experience.
- **INV-920** — Typed `analytics.deletion_request` mutation for GDPR right-to-be-forgotten: deletion is a substrate primitive sinks must honor.

## Open follow-ups
- Phase-1 sink adapter performance under high event volume.
- Server-side event aggregation for multiplayer (Brief 209) — deferred to v0.3.
- Funnel / cohort analysis primitives — deferred to v0.3.
- Real-time dashboards integration — deferred to v0.3.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 185 — Playtest harness.
3. Brief 210 — Account and identity surface.
4. Brief 212 — Live content pipeline.
5. GDPR Article 17 (right to erasure).
6. Mixpanel API documentation.
7. PostHog open-source analytics documentation.
8. Plausible Analytics privacy posture documentation.
