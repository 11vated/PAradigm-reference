# 210 — Account and identity surface

## Question
What is the typed account and identity surface that enables substrate gseeds to support player accounts, persistent identity, cross-device save sync, and federation across substrate creators without locking creators into a centralized identity provider?

## Why it matters (blast radius)
Live-service games and any multiplayer requires player identity. The substrate's federation philosophy (Brief 152, 187) means there is no central marketplace, so there is also no central identity provider. The brief specifies a typed identity surface that creators can implement against any backend (their own, a third-party, or a federated substrate-provided default) without code changes to the game.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 187 — mod and plugin surface (federation precedent).
- Brief 209 — multiplayer transport.
- Briefs 197-208 — single-player recipes.

## Findings
1. **Identity as typed gseed.** `identity.def` declares: typed identity provider reference, public identifier (UUID or creator-chosen string), display name, signed identity proof (per Brief 152), capability set.
2. **Provider abstraction.** `identity.provider.def` declares the implementation: built-in providers (local-anonymous, federated-substrate, OAuth-via-third-party), or creator-defined provider via mod surface (Brief 187). Recipes select a provider via typed `identity.provider.id` field.
3. **Local-anonymous default.** v0.1 ships local-anonymous as default — generates a UUID stored locally with no server roundtrip. Single-player games never need more.
4. **Federated substrate identity.** Optional substrate-hosted identity service (single-sign-on across substrate-creator games) shipped as a creator-deployable substrate server build, not a centralized monopoly. Creators run their own federation node; nodes can cross-trust via signed federation proofs.
5. **OAuth third-party.** Built-in OAuth providers ship for: Google, Apple, Discord, Steam, Epic. Creators select from typed enum; substrate handles the OAuth flow per engine target. PII never crosses substrate runtime — only opaque tokens.
6. **Cross-device save sync.** `save.snapshot` (Brief 158) gains a typed `sync.policy` field declaring: local-only (default), substrate-federation-sync, or creator-backend-sync. Sync uses content-addressed chunks per Brief 158, signed per Brief 152.
7. **Capability set.** Identity gseed declares typed capabilities the player has: own-content, publish-mod, server-host, admin-action. Capabilities gate substrate operations at runtime.
8. **Privacy by default.** Substrate identity contains only public identifier + display name + capabilities. PII (real name, email, address) is never substrate state. Creators wanting PII must implement via their own backend with explicit user consent.
9. **Anonymous-to-authenticated migration.** Local-anonymous identities can upgrade to authenticated identities via typed `identity.merge` mutation that signs the upgrade and preserves prior playthrough lineage.
10. **Validation contract.** Sign-time gates: at most one active identity provider per player session, identity proofs sign-verifiable per Brief 152, capability set declared.

## Risks identified
- **Federation complexity.** Running a federation node is operational overhead. Mitigation: substrate ships a Docker-image federation server with sane defaults; creators can opt out and stay local-anonymous.
- **OAuth provider churn.** OAuth providers change APIs. Mitigation: substrate ships per-provider adapters versioned with substrate releases; creators get adapter updates via substrate updates.
- **Account recovery.** Lost local-anonymous accounts can't be recovered. Mitigation: explicit warning at instantiation; recommend OAuth for any creator wanting recovery.
- **PII inadvertent capture.** Display names can contain real names. Mitigation: substrate documents the PII boundary explicitly; creators are responsible for moderation.
- **Federation trust drift.** Federation nodes may misbehave. Mitigation: typed signed federation proofs let any node verify another's identity claims; bad actors can be untrusted by removing the federation proof.

## Recommendation
Specify the account and identity surface as a typed `identity.def` + `identity.provider.def` gseed pair with built-in providers (local-anonymous default + federated-substrate + 5 OAuth providers), typed capability sets, save sync via Brief 158 chunked saves, anonymous-to-authenticated migration, and PII boundary at the substrate edge. Defer creator-backend-sync implementation guidance to v0.2.

## Confidence
**4 / 5.** Identity surface design is well-precedented; the novelty is the federation-not-monopoly pattern with creator-runnable identity nodes. Lower than 4.5 because federation operational characteristics need Phase-1 measurement.

## Spec impact
- New spec section: **Account and identity surface specification**.
- Adds typed `identity.def`, `identity.provider.def`, `identity.merge` gseed kinds.
- Adds the federation-substrate identity server as substrate-deployable.
- Adds the PII boundary at the substrate edge.
- Cross-references Briefs 152, 158, 187, 209.

## New inventions
- **INV-887** — Typed `identity.def` + `identity.provider.def` pair with creator-selectable provider: identity is a first-class typed substrate primitive with pluggable providers.
- **INV-888** — Federation-not-monopoly identity pattern: substrate ships a deployable identity node, creators run their own; cross-node trust via signed federation proofs.
- **INV-889** — PII boundary at the substrate edge: substrate identity contains only public identifier / display name / capabilities; PII is creator-backend responsibility with explicit user consent.
- **INV-890** — Typed `identity.merge` mutation for anonymous-to-authenticated upgrade preserving prior playthrough lineage: identities are mergeable substrate primitives.
- **INV-891** — Built-in OAuth provider adapters (Google / Apple / Discord / Steam / Epic) shipped per substrate release: OAuth complexity is substrate-managed.
- **INV-892** — Typed `sync.policy` field on save.snapshot enabling local-only / federation-sync / creator-backend-sync: save sync is structured creator choice.

## Open follow-ups
- Federation operational guide — Phase 1 with first creator deployments.
- Two-factor authentication — deferred to v0.3.
- Family-sharing identity model — deferred to v0.4.
- Account deletion / GDPR right-to-be-forgotten — deferred to v0.2.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 158 — Save snapshot model.
3. Brief 187 — Mod and plugin surface.
4. Brief 209 — Multiplayer transport.
5. OAuth 2.0 specification (RFC 6749).
6. WebFinger specification (RFC 7033).
7. ActivityPub federation specification (W3C).
8. Steam OAuth documentation (partner.steamgames.com).
