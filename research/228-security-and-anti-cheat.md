# 228 — Security and anti-cheat

## Question
What is the typed security and anti-cheat surface that protects substrate-built games against memory tampering, replay forgery, score manipulation, save file editing, mod injection, and network exploitation — across the eight engine targets — without resorting to invasive kernel-level anti-cheat that creates user-trust and platform-distribution problems?

## Why it matters (blast radius)
Multiplayer (Brief 209), leaderboards (Brief 211), monetization (Brief 213), and ranked matchmaking (Brief 215) all create cheating incentives. Kernel-level anti-cheat (BattlEye, Easy Anti-Cheat, Vanguard) is invasive, often blocked on Linux / Steam Deck, and a privacy / trust burden. Substrate's signed deterministic kernel provides a fundamentally different anti-cheat posture: cheat-resistance through structural typed gates and replay verification, not surveillance.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 209 — multiplayer transport and replication.
- Brief 211 — leaderboards and achievements.
- Brief 215 — matchmaking and lobby.
- Brief 216 — moderation and safety.

## Findings
1. **Replay-verified score submission.** Per Brief 211, scores are accepted only with valid replay gseeds whose lineage is signed and reproducible. Forging a score requires forging a complete signed deterministic replay — structurally hard.
2. **Server-authoritative state.** Per Brief 209 client-server replication, the substrate runtime treats server state as canonical. Client mutations are validated through typed gates server-side; impossible mutations are rejected.
3. **Typed mutation rate limits.** Substrate runtime enforces typed `mutation.rate.limit` per mutation kind. Excessive submission (e.g., 1000 inputs per second from a client) is structurally throttled. Rate limit values are typed substrate config, not creator-implemented.
4. **Save file integrity.** Per Brief 152, saves are signed gseeds. Tampering invalidates the signature. Substrate runtime refuses to load saves with broken lineage. Optional `save.tamper.policy` allows creator to soft-warn vs hard-reject.
5. **Memory protection (limited).** Substrate runtime exposes typed `protect.field` markers on critical state (player health, currency, inventory). Substrate runtime stores protected fields with checksum + obfuscation. Cheat Engine-style memory edits trigger checksum failure on next read. Documented as "raises the bar," not absolute defense.
6. **Anti-replay (network).** Multiplayer messages are signed with monotonic typed `seq.num`. Replayed packets are dropped. Combined with Brief 209 lockstep / rollback semantics, packet-replay attacks are structurally blocked.
7. **Server-side anomaly detection.** Substrate ships typed `anomaly.detector.def` rules: statistical outliers (player ranking jumps 1000 places overnight), impossible inputs (movement faster than max speed), correlation patterns (multiple accounts with identical inputs). Substrate runtime fires typed `anomaly.flagged` mutation; creators choose response (review queue / soft ban / hard ban via Brief 216).
8. **Mod sandboxing.** Per Brief 187, mods declare typed capability manifests; substrate runtime gates mod state mutations against declared capabilities. Mod injection attacks are structurally limited to declared capability surface.
9. **Federated trust model.** No centralized anti-cheat authority. Federated leaderboards (Brief 211) verify replays independently per node; consensus across federation nodes resolves disputes.
10. **No kernel driver.** Substrate explicitly does NOT ship kernel-level anti-cheat. Documents the trade-off: substrate's anti-cheat is structural / deterministic, not surveillance-based. Cheaters who bypass typed gates exist, but the cost-of-cheating curve is much steeper than client-side memory hacks suggest.
11. **Encrypted assets (limited).** Optional typed `asset.encrypt` flag encrypts assets at rest. Symmetric key derived from substrate runtime; raises bar against asset rip but not absolute. Documented as "raises the bar."
12. **Validation contract.** Sign-time gates: replication model declared per Brief 209, mutation rate limits declared per kind, save tamper policy declared, anomaly detector rules valid for declared game mode, server build present for client-server replication, no mod has capability beyond Brief 187 maximum.

## Risks identified
- **Determined cheaters defeat structural defense.** Skilled attackers can forge replays with engineering effort. Mitigation: substrate honestly documents that no anti-cheat is perfect; structural defense raises cost dramatically without surveillance.
- **Server-side anomaly false positives.** Statistical detectors flag legitimate exceptional players. Mitigation: anomalies trigger review queue by default, not auto-ban.
- **Rate limit tuning.** Per-mutation rate limits need tuning per game. Mitigation: substrate ships sensible defaults; creators tune via typed override.
- **Federation trust drift.** Federation nodes may disagree on anomaly thresholds. Mitigation: per-federation trust signals are creator-opt-in.
- **Memory protection cost.** Checksum + obfuscation costs CPU. Mitigation: protection is opt-in per field; hot-path fields can opt out.

## Recommendation
Specify security and anti-cheat as typed `mutation.rate.limit` + `protect.field` + `anomaly.detector.def` + `save.tamper.policy` + `asset.encrypt` + signed replay verification + server-authoritative replication. Substrate's anti-cheat is structural and deterministic, not surveillance-based — explicitly no kernel driver. Trade-off documented honestly.

## Confidence
**4 / 5.** The structural anti-cheat patterns are well-grounded in deterministic-game architecture (Starcraft replays, fighting game rollback, lockstep RTS). The novelty is the typed substrate-wide application across all game kinds. Lower than 4.5 because tuning anomaly detection without false positives needs Phase-1 measurement against real player data.

## Spec impact
- New spec section: **Security and anti-cheat specification**.
- Adds typed `mutation.rate.limit`, `protect.field`, `anomaly.detector.def`, `save.tamper.policy`, `asset.encrypt`, `seq.num`, `anomaly.flagged` gseed kinds.
- Adds substrate's no-kernel-driver position statement.
- Cross-references Briefs 152, 187, 209, 211, 215, 216.

## New inventions
- **INV-1034** — Replay-verified score submission as structural anti-cheat: forging scores requires forging signed deterministic replays — cost-of-cheating is structural.
- **INV-1035** — Typed `mutation.rate.limit` per mutation kind enforced substrate-runtime-wide: rate-limit attacks are structurally blocked, not creator-implemented.
- **INV-1036** — Server-authoritative state with typed gate validation per Brief 209: impossible client mutations are structurally rejected.
- **INV-1037** — Typed `protect.field` checksum + obfuscation for memory tampering resistance: bar-raising memory protection without invasive techniques.
- **INV-1038** — Anti-replay via signed monotonic `seq.num`: packet replay attacks are structurally blocked.
- **INV-1039** — Typed `anomaly.detector.def` server-side rule set with `anomaly.flagged` mutation feeding Brief 216 moderation: statistical anomalies are first-class substrate primitives.
- **INV-1040** — Brief 187 capability sandboxing as anti-cheat against mod injection: mod attack surface is bounded by typed capability manifest.
- **INV-1041** — Substrate's no-kernel-driver explicit position with structural-deterministic anti-cheat trade-off documented: anti-cheat without surveillance is the substrate posture.
- **INV-1042** — Federated anti-cheat with creator-opt-in trust signals: no centralized anti-cheat authority — federation analogous to Brief 210 / 215.
- **INV-1043** — Save file lineage signature verification with creator-tunable tamper policy: save editing is structurally detectable.

## Open follow-ups
- Phase-1 anomaly detector tuning against player data.
- Speedrun-friendly anti-cheat exemptions — Phase 1 (speedrunners use exotic input timing legitimately).
- Replay verification scaling for high-volume leaderboards — Phase 1 (Brief 211 sampling).
- DDOS protection on substrate dedicated server — Phase 1.
- Bot detection heuristics — deferred to v0.3.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 187 — Mod and plugin surface.
3. Brief 209 — Multiplayer transport and replication.
4. Brief 211 — Leaderboards and achievements.
5. Brief 216 — Moderation and safety.
6. Lockstep RTS anti-cheat patterns (Starcraft / Age of Empires).
7. Rollback netcode anti-cheat properties (GGPO).
8. EOS Easy Anti-Cheat documentation.
9. BattlEye documentation.
10. Riot Vanguard public discussion of trade-offs.
11. Cheat Engine memory hacking patterns (defensive references).
