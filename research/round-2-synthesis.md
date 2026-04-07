# Round 2 Synthesis — Briefs 023 to 070

## Purpose

Round 2 took the GSPL spec from "principled foundation" (Round 1, briefs 001-022) to "exhaustively defined platform" — every layer of the substrate, every workflow, every operational concern, every competitor, every invention. This synthesis is the cross-brief view: what the 48 new briefs collectively decided, where the inventions are, what the spec impact is, and what the Phase 1 deltas to the build plan are.

## Brief inventory by tier

| Tier | Range | Theme | Briefs |
|---|---|---|---|
| A | 023-028 | Substrate deepening | content-addressing, deterministic kernel, gseed format, modifier surfaces, plugin ABI, naturality squares |
| B | 029-034 | Agent and conversational layer | planner, critic ensemble, refinement loop, modifier UI, agent permissions, observability |
| C | 035 | Renderer pipeline (deferred to G) | renderer architecture |
| D | 036-041 | Evolution layer | novelty/AURORA, DQD, POET, speciation, refinement, GSPL-native operators |
| E | 042-047 | Sovereignty / trust / marketplace | key management, federation, marketplace, anti-piracy, IP rights, ZK anonymous publication |
| F | 048-052 | Studio / UX / accessibility | studio architecture, conversational UX, accessibility, onboarding, time machine |
| G | 053-057 | Backend / infrastructure | local-first storage, rendering pipeline, LLM runtime, observability, release engineering |
| H | 058-062 | Compliance / security / IP | EU AI Act, GDPR, supply chain, content moderation, incident response |
| I | 063-070 | Competitive deep dives | image gens, video gens, game engines, procedural, creator platforms, academic, Spore, master matrix |

48 new briefs. 7 contain inventions explicitly marked **INV**. The remainder are deep research that justify, constrain, or extend existing spec decisions.

## The seven inventions

| ID | Brief | Invention |
|---|---|---|
| INV-100 | 041 | Lineage-aware crossover (cross paths through the DAG, not leaves) |
| INV-101 | 041 | FIM-weighted mutation (Fisher Information Matrix guided parameter search) |
| INV-102 | 041 | Sloppy-direction crossover (project crossover into low-curvature directions) |
| INV-103 | 041 | Naturality-square cross-engine composition (category-theoretic breeding) |
| INV-104 | 041 | Operator-history-aware bandit selection (per-user, per-lineage operator choice) |
| INV-105 | 041 | Critic-gradient reflection (Reflexion through the critic ensemble) |
| INV-106 | 041 | Preference-pairwise crossover (RLHF-style preference signal in evolution) |
| INV-107 | 041 | Lineage-constrained mutation (constrain to plausible regions of lineage history) |
| INV-108 | 041 | Cross-engine symmetry-breaking |
| INV-109 | 041 | Multi-generation replay |
| INV-110 | 047 | zk-SNARK (Plonk) anonymous publication with selective de-anonymization |
| INV-111 | 052 | Lineage-aware time machine (navigate, inspect, branch, replay, what-if) |

That's twelve inventions across three briefs (041, 047, 052). All are net new contributions to the procedural / generative-substrate field.

## Cross-brief decisions (the spec deltas)

### Constitutional commitments
These are now non-negotiable spec properties, established or reinforced in Round 2:

1. **No DRM, ever.** (Brief 045) Sovereignty trumps anti-piracy.
2. **No central operator.** (Brief 043) Federation, no platform.
3. **No platform fee on the marketplace.** (Brief 044) Constitutional, not a pricing decision.
4. **User owns IP and data.** (Briefs 046, 053) Cryptographically enforced.
5. **No backdoors for de-anonymization.** (Brief 047) Even by GSPL itself.
6. **No takedown of already-shared content.** (Brief 061) Revocation cannot un-distribute.
7. **No central content moderation.** (Brief 061) Community blocklists only.
8. **No mandatory telemetry.** (Brief 056) Opt-in, k-anonymity ≥100, DP, Tor transport.
9. **Local-first by default.** (Brief 053) Cloud is opt-in for specific tasks.
10. **Open weights only for shipped models.** (Brief 055) Hosted is opt-in BYO.
11. **C2PA + watermark on every output.** (Briefs 008, 009, 058) AI Act and provenance both.
12. **WCAG 2.1 AA floor.** (Brief 050) Accessibility is constitutional.
13. **Reproducible builds + multi-sig signing.** (Brief 057) Supply chain integrity.
14. **GDPR-compliant by architecture, not policy.** (Brief 059) User is controller for local data.

### Architectural decisions
1. **Six-layer studio architecture.** (Brief 048) kernel/engines/agent/services/frontend/workspace.
2. **Three storage tiers for keys.** (Brief 042) software/keychain/hardware.
3. **libp2p federation with QUIC+Noise.** (Brief 043) Direct invite v1, DHT v1.5.
4. **Five-tier license model L1-L5.** (Brief 046)
5. **Five-track release model.** (Brief 057) stable/beta/nightly/frozen/self-built.
6. **Six-phase incident response.** (Brief 062) detect/triage/investigate/mitigate/disclose/post-mortem.
7. **Six-layer supply chain defense.** (Brief 060) minimization/pinning/vetting/build/runtime/monitoring.
8. **Five-layer content moderation.** (Brief 061) AUP/filters/provenance/blocklists/law enforcement.
9. **Three rendering tiers.** (Brief 054) deterministic/native fast/differentiable.
10. **Three LLM runtime modes.** (Brief 055) local/hosted/hybrid.

### UX decisions
1. **First wow ≤5 min.** (Brief 051) Identity setup *after* the first generation.
2. **Conversational interface as universal authoring layer.** (Brief 049)
3. **Modifier surfaces with "↗" inspector.** (Brief 049)
4. **Three studio modes.** (Brief 049) Conversational/Studio/Deep.
5. **Variant grids 4-8 default.** (Brief 049)
6. **Lineage time machine as headline demo.** (Brief 052)
7. **Six default templates at v1.** (Brief 051)
8. **Ten v1 languages, RTL support.** (Brief 050)

### Business / strategy decisions
1. **No GSPL token ever.** (Brief 044) Anti-NFT.
2. **Off-chain settlement v1, Stripe Connect v1.5, Lightning v2 opt-in.** (Brief 044)
3. **GSPL is "the platform, not the model."** (Brief 063) Pluggable backbones.
4. **GSPL is the substrate for game engines, not a competitor.** (Brief 065)
5. **GSPL is the anti-Roblox / fulfillment of Dreams.** (Brief 067)
6. **No central server dependency, no DRM, no platform cut** as Spore-postmortem-derived constitutional commitments. (Brief 069)

## Phase 1 deltas (changes to the build plan from round 1)

Round 1 outlined a Phase 1 (months 0-6) build plan focused on:
- Sprite engine
- Agent + planner
- Local studio (Tauri)
- Lineage v1
- Marketplace v0 (read-only)

Round 2 changes Phase 1 as follows:

### Added to Phase 1
- **Three-tier key management infrastructure** (Brief 042) — software tier mandatory, keychain best-effort, hardware optional. Recovery file mandatory.
- **C2PA + watermark on all output** (Brief 058) — AI Act compliance from day one.
- **Pre-generation CSAM filter** (Brief 061) — PhotoDNA-style on-device.
- **WCAG 2.1 AA accessibility floor** (Brief 050) — release-blocking.
- **Six default templates** (Brief 051) — first-wow-moment delivery.
- **First wow ≤5 min target** (Brief 051) — measurable, release-blocking.
- **Local-only diagnostics with PII filtering** (Brief 056).
- **Cargo-vet, cargo-deny, cargo-audit in CI** (Brief 060).
- **Reproducible builds + multi-sig signing** (Brief 057).
- **Bug bounty intake channels** (Brief 062) — at v1 launch.
- **Privacy policy in 10 EU languages** (Brief 059).
- **Acceptable Use Policy** (Brief 061) — public legal doc.
- **Default blocklist** (Brief 061) — minimal, replaceable.
- **EU-hosted infrastructure for any opt-in metrics** (Brief 059).

### Deferred from Phase 1 to Phase 1.5
- **Federation DHT** (Brief 043) — direct invite at v1, DHT at v1.5.
- **Marketplace settlement automation** (Brief 044) — manual at v1, Stripe Connect at v1.5.
- **Hosted LLM runtime** (Brief 055) — BYO API key at v1; expanded provider support at v1.5.
- **Anonymous publication** (Brief 047) — v1.5 opt-in, after ZK proving infrastructure stabilizes.
- **Lineage-aware time machine UI** (Brief 052) — basic navigate at v1, full what-if at v1.5.
- **WFC engine** (Brief 066) — v1.5.
- **Houdini HDA importer** (Brief 066) — v1.5.
- **Video engine (storyboard mode)** (Brief 064) — v1.5.

### Deferred to Phase 2+
- **Lightning settlement** (Brief 044) — v2 opt-in.
- **3D mesh engine** (Brief 003) — v2.
- **Long-form video** (Brief 064) — v2.
- **Quantum-resistant crypto migration** (Brief 042) — Phase 3.
- **Bidirectional engine sync** (Brief 065) — v2.
- **Community plugin signing key infrastructure** (Brief 060) — v2.

## Open questions that remain after Round 2

1. **Open-weight video model selection for v1.5** — Mochi, LTX, Hunyuan, Wan? (Brief 064)
2. **PhotoDNA license for on-device CSAM detection** — alternative if not available. (Brief 061)
3. **Reproducible builds reliability in Rust** — operational uncertainty. (Brief 060)
4. **Sandboxing primitive** — Wasmtime, OS sandbox, native containers? (Brief 060)
5. **Galois group for plonk-friendly curve in ZK publication** — engineering decision pending. (Brief 047)
6. **Stripe Connect international coverage** — applicability to non-US sellers. (Brief 044)
7. **Tor as default vs opt-in** for federation. (Brief 043)
8. **EU AI Act guidance drift** on Article 50 marking. (Brief 058)
9. **Whether GSPL accepts external funding** — investor terms could conflict with sovereignty. (referenced in 069)
10. **Foundation model for long-term governance** — at what milestone? (referenced in 069)

These are not blocking; they are ongoing.

## Confidence inventory

| Confidence | Briefs |
|---|---|
| 5/5 | 015, 026, 027, 029, 030, 042, 043, 045, 048, 050, 051, 053, 057, 068, 069 |
| 4/5 | 016, 023, 024, 025, 028, 031, 032, 033, 034, 036, 037, 038, 039, 040, 041, 044, 046, 049, 052, 054, 056, 059, 062, 063, 065, 066, 070 |
| 3/5 | 035, 055, 058, 060, 061, 064, 067 |
| 2/5 | 047 |

**The 2/5 (Brief 047, ZK anonymous publication)** is the highest implementation risk in the spec. It is deferred to v1.5 specifically because of this uncertainty.

**The 3/5 cluster** is concentrated in compliance, video, and creator-platform competition — all areas with genuine external uncertainty rather than internal weakness.

## What is now defensible

After Round 2, GSPL has a defensible answer to every question in this list:

- "How do you handle CSAM?" → Brief 061
- "What about GDPR?" → Brief 059
- "Why not just use Stable Diffusion?" → Brief 063
- "How do you compete with Sora?" → Brief 064
- "Aren't you just Houdini with AI?" → Brief 066
- "How is this not Picbreeder again?" → Brief 068
- "Didn't Spore already try this?" → Brief 069
- "Why not Roblox?" → Brief 067
- "How do you make money without a platform fee?" → Brief 044
- "What if my private key is stolen?" → Brief 042
- "What about supply chain attacks?" → Brief 060
- "How do incidents get handled?" → Brief 062
- "Why is this any safer than other AI tools?" → Briefs 058, 061
- "How do you keep the lineage honest?" → Briefs 015, 042, 052
- "Can I use this offline?" → Brief 053
- "What if Anthropic bans me?" → Brief 055 (BYO)
- "Will my projects survive when GSPL is gone?" → Brief 053 (local-first)
- "How do I know what models you ship are safe?" → Briefs 046, 055, 060
- "What about people who can't see / can't use a mouse?" → Brief 050
- "What does first-time use feel like?" → Brief 051
- "What if I want to undo my last hour of work?" → Brief 052

This list is not exhaustive but it's the headline questions an external reviewer would ask. After Round 2 they all have concrete, principled answers backed by specific briefs.

## Where Round 3 should focus

Round 2 closed the substrate, the workflow, the operational layer, the compliance layer, and the competitive frame. Round 3 should focus on:

1. **Implementation specs.** Each brief identifies "spec impact" files that need to be written (`architecture/*.md`, `protocols/*.md`, `adr/*.md`). Round 3 is the writing of those.
2. **The v1 README and getting-started.** Public-facing documentation.
3. **The first user research session.** Validate the conversational interface and the first-wow-moment target with actual humans.
4. **The model registry v1.** Operational doc for which models ship at v1.
5. **The build plan as a Gantt.** Brief 005 has the team model; Round 3 turns it into dates.
6. **The funding and governance plan.** External funding vs. self-funding; foundation model; eventual governance handoff.
7. **The community manifesto.** Public values document; the constitutional commitments listed above.
8. **Demo videos.** The hardest sales asset for an ambitious project — show the lineage time machine, show the conversational compose, show the cross-engine breeding.

## The headline framing

After 70 briefs, Paradigm GSPL Engine is:

> A sovereign, federated, multi-modal generative substrate. It runs locally on your hardware, ships with open-weight models, signs every artifact with your cryptographic identity, persists every creative decision as queryable lineage, lets a conversational AI agent do the procedural work while you stay in control, exposes ten native evolution operators that no other tool has, hosts a marketplace with no platform fee and creator royalties, federates without a central server, and is structurally impossible for any of its 20+ competitors to match without ceasing to be themselves.

Every clause in that sentence is now backed by at least one brief, often three or four. The spec is no longer an aspiration; it is a defensible architecture.

## Confidence in this synthesis
**4/5.** The synthesis is honest and tracks the source briefs. The 4/5 reflects the inherent uncertainty of any 48-brief integration — somewhere there's a decision that two briefs disagree about and I haven't caught it yet. The Round 3 implementation phase will surface those.

## Sources
- Briefs 023 through 070 (all of Round 2).
- Round 1 synthesis (`synthesis.md`).
- Round 2 plan (`round-2-plan.md`).
