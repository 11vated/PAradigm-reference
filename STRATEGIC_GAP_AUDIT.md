# Strategic Gap Audit — Reference Repository → 5T-Scale Platform

**Scope:** what the `gspl-reference` repository currently contains vs. what it needs to ship to unlock planetary-scale adoption and realize the Paradigm / GSPL / GOE vision at trillion-dollar platform magnitude.

**Date anchor:** April 2026 (7 commits into the live reference repo).

**Audience:** every implementer, contributor, and AI agent that reads this repo. This doc sets execution priorities for the next 90 days and names every file that still needs to exist.

**Non-negotiable constraints (inherited from the GSPL Open Specification License):**
- 100% free forever. No paywalls, no rate limits, no usage caps.
- Fully forkable and self-hostable. No cloud dependency required.
- Runs locally on any commodity hardware the user owns.
- Users supply their own compute for growth/evolution.
- Open spec + open reference implementation.

Nothing in this audit relaxes those constraints. Everything proposed below is designed to compound within them.

---

## 1. What the repo already nails

Before the gap list, name the strengths. These are load-bearing and should not be touched.

| Asset | Status | Notes |
|---|---|---|
| `spec/00–07` | Complete, locked | Universal Seed, 17 kernel gene types, kernel, GSPL language, sovereignty, .gseed format, determinism. |
| `adr/` | ADR-009 Accepted | .gseed binary format locked; SHA-256 over JCS canonical payload, ECDSA-P256 per RFC 6979. |
| `research/001–231` | 1,064 inventions catalogued | Seven rounds of research, every brief traces back to a specific invention number. |
| `engines/` | 15 of 26 implemented in mirror | Humanoid, sprite, music, sculpt-3d, texture, physics, fluid, particle, etc. |
| `intelligence/gspl-agent.md` | Skeleton | 5-stage Concept-to-Seed pipeline and 8 sub-agents defined at architecture level. |
| `compliance/` | C2PA, EU AI Act groundwork | Brief 007 and Brief 010 are the canonical risk calls. |
| `MVP_DEFINITION.md` | Recently corrected | Establishes that every brief is load-bearing. BLAKE3 slip and kernel/content-domain collision were fixed on April 8. |
| `examples/` | 8 sample `.gspl` seeds + 1 `.gseed.json` | Proves the grammar is real, not hypothetical. |
| License & governance | GSPL Open Specification License | The constraint spine. Every new asset inherits it. |

This is an extraordinarily clean reference substrate. The gap list below is about **execution layers the spec can't carry alone**.

---

## 2. Gap categories, in priority order

### Priority tier P0 — unblock adoption today

These are the gaps that, if unfilled, leave the repo as a brilliant but unusable specification. Fill these in the next 90 days.

#### P0-1. Seed Commons (materialized canonical armory)

**State:** Brief 088A describes a 1,000-seed canonical armory. `examples/` ships ~8 demonstration seeds. The gap between 8 and 1,000 is total.

**Required files:**
- `seed-commons/README.md` ✅ *(added in this pass)*
- `seed-commons/CONTRIBUTING-seeds.md` ✅ *(added in this pass)*
- `seed-commons/primitives/` — 17-gene base building blocks, one file per kernel type.
- `seed-commons/libraries/` — runnable GSPL modules that materialize Briefs 081–094 (chemistry, physics, materials, biology, music, culture, etc.).
- `seed-commons/inventories/{lighting,weather,materials,fx,fluid,character,creature,plant,building,vehicle,food,music,camera,style,scene,framework,algorithm,cross-domain}/` — 1,000 canonical seeds distributed per Brief 088A's category targets.
- `seed-commons/recipes/{basic-compositions,evolutionary-loops,domain-fusion,advanced-templates}/` — reusable GSPL programs that combine, breed, and evolve seeds.
- `seed-commons/validation/` — CI harness (determinism, round-trip, signature, lint).

**Why P0:** Without materialized seeds, "ship GSPL" means "ship a PDF." With 1,000 canonical seeds, every new user — and every AI agent — opens the repo and sees the substrate's full range working on real hardware. This is the single highest-leverage asset for network effects.

**Effort:** Round 4 libraries are described prose; converting to GSPL is mechanical. The 1,000 seeds are the work — but the Full-Capacity Agent (see P0-2) can generate and validate the bulk autonomously once the 50–100 exemplar seeds per category exist as training anchors.

#### P0-2. Full-Capacity GSPL Agent

**State:** `intelligence/gspl-agent.md` and siblings (`8-sub-agents.md`, `memory-system.md`, `template-bridge.md`, `adjective-normalization.md`, `intent-taxonomy.md`) define the architecture at a high level. Tool layer, internet access, code execution, self-bootstrapping, and local fine-tuning are not specified to the level where an implementer can build them.

**Required files:**
- `intelligence/gspl-agent-full-capacity.md` — sovereign self-bootstrapping agent spec.
- `intelligence/tool-layer.md` — web_search, browse_page, code_execution, evolution_run, multimodal_analyze, fetch_real_world_data, seed_inventory_query, self_fine_tune_trigger.
- `intelligence/self-bootstrapping-loop.md` — the closed-loop training pipeline that uses only validated GSPL seeds.
- `intelligence/local-fine-tune.md` — QLoRA + Unsloth stack on commodity GPUs, dataset format, evaluation rules.

**Why P0:** The agent is the population engine for the commons. Without it, the 1,000-seed target is a hand-curation marathon. With it, the commons expands exponentially while the agent simultaneously gets better at GSPL — a compounding moat no competitor can copy without reinventing the determinism substrate.

**Effort:** Agent spec is a 1-day write. Tool layer implementation is 2–3 weeks on top of the existing kernel. Self-bootstrapping loop is 1–2 weeks. Fine-tuning run (QLoRA on a 70B base) is 7–14 days of wall clock on a single 24 GB GPU.

#### P0-3. Live public MVP (web studio)

**State:** No live demo. No CLI the user can `npm install` and run. No one-click "try a seed" experience.

**Required files:**
- `roadmap/phase-3-mvp-studio.md` — 90-day sprint plan for a web-based studio that runs 3–4 engines + basic agent + breed/sign/export.
- `codebase/studio/` — a minimal, fully open-source studio implementation (local-first, no servers required).
- `scripts/try-a-seed.sh` — one-command bootstrap that grows the `melancholy_bard` example and writes a .gseed.

**Why P0:** The current repo is a specification + partial mirror. Adoption curves do not bend for specs. They bend for things a creator can open in a browser and use in 60 seconds. This is the difference between a reference the world admires and a platform the world runs.

**Effort:** 60–90 days engineering sprint. Target: prompt → grow → sign → export → download a `.gseed` + `.png` + `.mp3` round-trip.

#### P0-4. Validation & CI for the commons

**State:** No CI harness for commons contributions. Community PRs would have nothing to fail against.

**Required files:**
- `seed-commons/validation/grow.ts` — grow any .gspl file and regenerate its .gseed.json payload hash.
- `seed-commons/validation/determinism.ts` — grow twice, diff, fail on any byte difference.
- `seed-commons/validation/signature.ts` — verify ECDSA-P256 over JCS canonical payload hash.
- `seed-commons/validation/commons-lint.ts` — enforce the 8-point contract checklist in `CONTRIBUTING-seeds.md`.
- `seed-commons/validation/graph.ts` — extract the composition graph for a seed.
- `.github/workflows/commons-ci.yml` — run all four on every PR touching `seed-commons/`.

**Why P0:** Without CI, the commons drifts into invalid state within days of opening PRs. With CI, the commons is self-policing and the Foundation curators spend their time on creative judgment, not boilerplate review.

**Effort:** 1–2 weeks. All four validators are thin wrappers around existing kernel code.

---

### Priority tier P1 — unblock growth over the next 6 months

#### P1-1. The 11 remaining engine bootstraps

**State:** Brief 027 names the 11 planned engines (shader, particle, vehicle, fashion, narrative, ui, physics, accessibility, voice, fonts, motion). Each is described but not mirrored into `engines/`.

**Required files:**
- `engines/{shader,particle,vehicle,fashion,narrative,ui,physics,accessibility,voice,fonts,motion}/README.md` — minimum viable engine doc.
- `engines/{…}/stdlib.gspl` — minimum primitives the engine consumes.
- `seed-commons/inventories/{…}/*.gspl` — 20–50 bootstrap foundational seeds per engine (this is a subset of the 1,000-seed target).

**Why P1:** Completes the 26-engine count claimed throughout the repo. Every missing engine is a credibility gap.

**Effort:** 1–2 weeks per engine with the Full-Capacity Agent doing the bulk generation.

#### P1-2. Money machine — business model doc

**State:** `LICENSE` and `MVP_DEFINITION.md` explain the open-spec and technical completeness story. Nothing in the repo explains how 11vatedTech LLC generates sustainable revenue while honoring the "100% free forever" constraint.

**Required files:**
- `docs/business-model.md` — non-extractive revenue ladder that respects the open license. Examples (all compatible with the constraint):
  - Optional hosted inference for users who don't want to run their own model. Free tier with compute limits; paid tier with more compute. The substrate remains free; only the convenience is billed.
  - Optional federation peer hosting for creators who want someone else to run the peer. Free to self-host; paid SLA to outsource.
  - Optional paid Foundation curation of custom seed armories for enterprise (e.g., "our studio's branded character canon").
  - Optional paid secondary-market marketplace fees on breed-derived seeds, where the royalty split goes to the author by default. The marketplace is free to run yourself; the hosted marketplace collects a small fee for payment processing.
  - Enterprise SLA and support contracts for studios that want the Foundation on-call.
  - Trademark licensing (the Paradigm name and logo are trademarks; the substrate is open).
- `docs/unit-economics.md` — COGS per active creator, CAC, LTV, TAM breakdown.
- `docs/go-to-market.md` — first vertical (recommend: full-game seeds), second vertical, distribution plan.

**Why P1:** Adoption at 5T scale requires capital to reach it. Capital requires a revenue story. This doc does not compromise the free forever constraint — it lists the non-extractive, optional services creators can pay for if they choose.

**Effort:** 1 week to draft, iterate with advisors.

#### P1-3. Ecosystem & distribution flywheel

**State:** No SDKs, no engine plugins, no community infrastructure, no public landing page, no viral hooks.

**Required files:**
- `sdks/unity/` — Unity package that imports a `.gseed` as a native Unity asset.
- `sdks/unreal/` — Unreal plugin, same.
- `sdks/godot/` — Godot plugin, same.
- `sdks/blender/` — Blender importer for `topology` and `field` gene types.
- `sdks/web/` — a browser-side reader that renders a .gseed from a shareable URL.
- `docs/shareable-seeds.md` — the viral hook: a URL that renders the seed instantly in any browser, no install.
- `docs/community.md` — Discord/Matrix server, Twitter/X, beta list signup.

**Why P1:** SDKs are the distribution layer. A Unity developer who can drop a `.gseed` into their scene is a convert. A Blender artist who can sculpt with a `topology` gene is a convert. Shareable URLs are how the commons goes viral.

**Effort:** 2–4 weeks per SDK. Full set in 4–6 months.

#### P1-4. Patents on the core inventions (while keeping the spec open)

**State:** Zero IP protection beyond the open license. Open spec licenses do not prevent a competitor from claiming priority on the underlying mechanism.

**Recommended files:**
- `docs/ip-strategy.md` — the ARM/Dolby/Qualcomm playbook: patent the mechanisms, license them openly via the GSPL Open Specification License, but retain the right to pursue bad-faith actors (patent trolls, closed forks claiming priority).
- Candidate claims: 17-gene composition closure; sovereignty as a first-class gene type; lineage-preserving mutation; deterministic growth via canonicalized RNG seeding; federated non-monopoly surfaces; cryptographic royalty propagation through breeding.

**Why P1:** This is the only defensive moat that works with an open license. Without patents, a closed competitor can adopt the spec, close their fork, and sue you. With patents filed and the open license in place, the world can use GSPL freely and bad actors face real consequences.

**Effort:** 4–6 weeks with a patent attorney. Not the work of this repo — a parallel track.

---

### Priority tier P2 — unblock scale over the next 12–24 months

#### P2-1. Marketplace + federation reference implementation
`roadmap/phase-4-marketplace.md` exists at a planning level. Needs: reference marketplace server (self-hostable), federation protocol implementation (Brief 091), reputation system, breed-derived royalty split propagation.

#### P2-2. Full 1,000-seed armory populated
Target: the entire Brief 088A inventory materialized. Agent-driven bulk generation after the first ~100 exemplars per category are human-curated.

#### P2-3. Cross-engine parity test suite
Brief 196: 60 fixtures × 8 engines. Every engine reader must produce byte-identical .gseed output for the same .gspl source. This is the determinism guarantee's enforcement layer.

#### P2-4. Round 4 libraries all materialized
- `seed-commons/libraries/chemistry.gspl`
- `seed-commons/libraries/physics.gspl`
- `seed-commons/libraries/materials.gspl`
- `seed-commons/libraries/biology.gspl`
- `seed-commons/libraries/earth-sciences.gspl`
- `seed-commons/libraries/cosmology.gspl`
- `seed-commons/libraries/mathematics.gspl`
- `seed-commons/libraries/music.gspl`
- `seed-commons/libraries/linguistics.gspl`
- `seed-commons/libraries/culture.gspl`
- `seed-commons/libraries/built-world.gspl`
- `seed-commons/libraries/lifestyle.gspl`
- `seed-commons/libraries/psychology.gspl`

Each corresponds to a Round 4 brief (081–086H). The first one, `chemistry.gspl`, lands in this same pass as a canonical template.

#### P2-5. Team & capital scaling
Out of scope for this repo, but named explicitly: reaching 5T requires funded execution (target: $20–50M seed/Series A for a $1B milestone; hundreds of millions for escape velocity). This repo is the asset that justifies the raise.

---

## 3. Dependency graph

```
P0-2 (Full-Capacity Agent)
  └─ enables P0-1 (bulk commons population)
       └─ enables P1-1 (11 engine bootstraps, mostly agent-authored)
            └─ enables P2-2 (full 1,000-seed armory)

P0-1 (Seed Commons scaffolding)
  └─ enables P0-4 (validation/CI against real files)
       └─ enables community PRs at scale

P0-3 (Live MVP studio)
  └─ enables P1-3 (SDKs distribute the studio's .gseed output)
       └─ enables P2-1 (marketplace on top of working studio)

P0-1, P0-2, P0-3 ship in parallel over 90 days.
P0-4 ships week 2 so the commons has gates from day one.
```

## 4. What 5T means operationally

Trillion-dollar platforms share four properties. This audit's goal is to make GSPL satisfy all four.

1. **A substrate competitors cannot fork cheaply.** GSPL has this: the 17-gene kernel + determinism guarantee + sovereignty propagation is hard to reproduce. Moat: solid. Action: file patents (P1-4).

2. **A network effect that compounds with usage.** Realized by the commons + breeding + lineage: every new seed is a parent for thousands of derivatives. Moat: **pending** until the commons materializes (P0-1) and the agent populates it (P0-2).

3. **A distribution layer that meets creators where they are.** Realized by the SDKs + shareable URLs + a live studio. Moat: **pending** until P0-3 and P1-3 ship.

4. **A revenue engine that funds execution without compromising the substrate.** The GSPL Open Specification License is non-negotiable. The business model must be optional services layered on top (P1-2). Moat: **pending** until the doc is written and a first vertical proves the model.

Every item in this audit maps back to one of these four.

## 5. What this audit does not do

- Does not propose changing the license.
- Does not propose adding paywalls, rate limits, or cloud lock-in.
- Does not propose centralizing governance. The Foundation curates; federation peers are first-class.
- Does not override any spec. Everything here consumes the existing spec; nothing here modifies it.
- Does not add new kernel gene types. The 17 are locked.
- Does not change the SHA-256 + JCS + ECDSA-P256 sovereignty primitives.

## 6. Next concrete action

After this audit, the next physical artifacts to land in the repo (in order):

1. `intelligence/gspl-agent-full-capacity.md` *(queued in the same pass as this audit)*
2. `seed-commons/libraries/chemistry.gspl` *(queued; materializes Brief 081 as runnable GSPL)*
3. `seed-commons/inventories/lighting/` first batch of 10 exemplar seeds + matching `.gseed.json` files *(queued)*
4. `seed-commons/inventories/materials/` first batch of 10 exemplar seeds + matching `.gseed.json` files *(queued)*
5. `seed-commons/validation/` four-file CI skeleton *(queued)*

These five deliverables together form the **proof-of-method**: they demonstrate the exact pattern the Agent will use to scale the commons to 1,000 seeds and then to the hundreds of thousands that a 5T platform requires.

---

**The invention is done. The spec is done. What's missing is execution — and this audit is the execution plan.**
