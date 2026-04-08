# 187 — Mod and plugin surface specification

## Question
What is the creator-and-player-facing mod and plugin surface that authors signed `mod.gseed` packages, sandboxes their execution, and distributes them through federation (Brief 100) with the same lineage and trust guarantees as the substrate?

## Why it matters (blast radius)
Mods are the creator-after-creator surface — they're how a finished game becomes a platform. If mods aren't signed, the trust chain breaks. If sandboxing isn't substrate-native, malicious mods compromise players. If distribution isn't federated, the substrate ships a closed marketplace at the most-extensible surface.

## What we know from the spec
- Brief 019 — plugin ABI v1.
- Brief 042 — key management lifecycle.
- Brief 045 — anti-piracy and leak resilience.
- Brief 046 — IP rights and licensing.
- Brief 100 — federation peer protocol.
- Brief 187 inherits all of Brief 19 plus the substrate-wide signing discipline.

## Findings
1. **Mod = signed gseed bundle.** A typed `mod.package` gseed bundles: a mod manifest (id, version, target game id, target game version range, dependencies, capabilities, license), a set of `level.scene` / `ecs.component` / `ai.behavior_tree` / `ui.theme` / `audio.clip` / etc. gseeds, and an optional plugin binary conforming to Brief 019's ABI v1. The whole package is signed by the mod author's key.
2. **Capability declarations.** A mod declares the capabilities it needs in its manifest: read scene, write scene, spawn entities, modify items, modify AI, modify economy, modify save state, render UI overlay, play audio, network access, file system access. Capabilities outside Brief 019's allow-list are rejected at sign time.
3. **Sandboxed execution.** Plugin binaries run in the substrate's deterministic sandbox (Brief 019). They can call only the typed APIs declared in their manifest. Network and filesystem access are denied by default and require explicit player consent at install time.
4. **Player consent UX.** When a player installs a mod, the substrate displays the mod's typed capability set in plain language ("This mod can: modify save state, render UI overlay") and requires explicit consent per capability. Consent is recorded as a signed `mod.consent` gseed in the player's profile.
5. **Mod compatibility check.** At install, the substrate validates the mod's target game version range against the installed game version. Mismatch produces a typed error with the version expectation. The mod author can declare a "compatible-with-newer" range up to which the substrate trusts the mod across upgrades.
6. **Mod composition order.** Multiple installed mods are composed in a typed `mod.load_order` declared by the player. Conflicts (two mods modifying the same gseed differently) are surfaced with a typed `mod.conflict` warning showing both mods' contributions. The player chooses a winner via a typed merge policy.
7. **Mod signing chain.** Mod authors register a signing key with the federation (Brief 042 key lifecycle). The substrate verifies signatures against the federation's key registry on install. Self-signed mods are accepted but flagged with a warning at install.
8. **Distribution via federation.** Mods are published as gseeds to a federation peer (Brief 100). Discovery is via federated search across peers. The substrate's mod browser is a typed view over federation queries. There is no central marketplace — peers host what they choose.
9. **Anti-piracy alignment.** Per Brief 045, mods cannot bypass DRM. The substrate's signing chain verifies that a mod modifies only gseeds inside its declared scope and rejects mods that attempt to inject unsigned binaries into the runtime.
10. **License inheritance.** Per Brief 046, every mod declares a typed `license` field. The substrate enforces compatibility with the base game's license at install (e.g., a CC-BY-NC mod can't be installed in a commercial game without the creator's opt-in).
11. **Mod telemetry opt-in.** Mods that want to collect telemetry must declare it as a capability and route it through the substrate's telemetry namespace (Brief 056). PII handling is identical to the base game's contract.
12. **Hot-reload.** Mods can be hot-reloaded in the playtest harness (Brief 185) for fast iteration. Hot-reload is a typed `mod.reload` mutation that re-runs sign-time validation and re-applies the mod against the live runtime at the next tick boundary.
13. **Mod authoring workflow.** Creators author mods in the same Studio surface as base games — there is no separate "mod editor". The Studio "publish as mod" action wraps the current scene/component selection in a `mod.package` gseed and signs it.

## Risks identified
- **Capability creep.** Authors over-declare capabilities to be safe. Mitigation: substrate displays capability *usage* statistics ("This mod declares network but never uses it") so players spot over-claims.
- **Mod conflict resolution UX.** Players can't reason about merge policy choices. Mitigation: typed merge policies have plain-language descriptions and a "preview merged result" view.
- **Sandbox escape.** Brief 019's deterministic sandbox is the primary defense; if it leaks, every mod becomes risky. Mitigation: the sandbox is the core trust surface and gets maximum security review.
- **Federation moderation.** Peers can host malicious mods. Mitigation: federation peers can blocklist key fingerprints; substrate maintains a creator-controlled blocklist; flagged mods surface as warnings during discovery.
- **Mod author key compromise.** Stolen key signs malicious mods. Mitigation: Brief 042 key revocation propagates through federation; substrate refuses to install mods signed with revoked keys; previously-installed mods are flagged with a typed warning.

## Recommendation
Specify the mod surface as a signed-gseed-bundle inheriting Brief 019's plugin ABI, Brief 042's key lifecycle, Brief 100's federation, and Briefs 045/046's IP discipline. Ship typed capability declarations with player consent UX, federation-only distribution, hot-reload through the playtest harness, and Studio's "publish as mod" action at v0.1. Defer multi-mod merge policy UX polish to v0.2.

## Confidence
**4.5 / 5.** Mod platforms have decades of precedent (Bethesda, Skyrim, Garry's Mod, Roblox, Steam Workshop). The novelty is the signed-bundle-with-capabilities contract, the federation-only distribution, the substrate-native sandbox via Brief 019, and the unified Studio authoring (no separate mod tool). Lower than 5 because the merge policy UX needs Phase-1 user testing.

## Spec impact
- New spec section: **Mod and plugin surface specification**.
- Adds `mod.package`, `mod.manifest`, `mod.consent`, `mod.load_order`, `mod.conflict`, `mod.reload` typed primitives.
- Cross-references Briefs 019, 042, 045, 046, 056, 100, 185.

## New inventions
- **INV-769** — Signed mod-package gseed with typed capability manifest: mods are first-class signed bundles with explicit, player-visible capability declarations.
- **INV-770** — Capability-usage tracking with over-claim surfacing: substrate measures which declared capabilities a mod actually uses and warns players about unused-but-claimed permissions.
- **INV-771** — Federation-only mod distribution with peer blocklists: no central marketplace; peers choose what they host; reputation flows through federation.
- **INV-772** — Unified Studio authoring with "publish as mod" action: creators don't context-switch to a mod tool; the same Studio surface produces both base games and mods.
- **INV-773** — Hot-reload of mods through playtest harness with sign-time re-validation at tick boundary: iteration speed without sacrificing trust chain.

## Open follow-ups
- Mod merge policy UX polish (deferred to v0.2).
- Mod-of-mod (mods modifying other mods) — deferred to v0.3 as a composition surface.
- Crowd-rated mod reputation (deferred to v0.3 with federation maturity).
- Paid mods (deferred — Brief 044 marketplace economics applies; opt-in per peer).
- Mod auto-update on base game version change (deferred to v0.2 — adversarial design needed).

## Sources
1. Brief 019 — Plugin ABI v1.
2. Brief 042 — Key management lifecycle.
3. Brief 044 — Marketplace economics.
4. Brief 045 — Anti-piracy and leak resilience.
5. Brief 046 — IP rights and licensing.
6. Brief 056 — Observability, telemetry, privacy.
7. Brief 100 — Federation peer protocol.
8. Brief 185 — Playtest harness specification.
9. Bethesda Creation Kit documentation.
10. Steam Workshop integration documentation.
