# Seed Commons — The Canonical GSPL Armory

The **Seed Commons** is GSPL's first-person voice: an open, evolvable, cryptographically-signed library of foundational seeds, recipes, and substrate libraries that a creator (human or agent) can open, fork, breed, and ship from day one.

It realizes **Brief 088A (Canonical Seed Armory)** and materializes the Round 4 library briefs (081–094) as runnable GSPL code — not descriptive documentation, not sample wrappers, but real, deterministic, signable `.gspl` / `.gseed.json` artifacts that produce bit-identical output across every compliant reader.

## Layout

```
seed-commons/
├── primitives/           # 17-gene base building blocks (color, shape, rhythm, envelope, …)
├── libraries/            # Round 4 briefs as runnable GSPL modules (chemistry, physics, materials, biology, music, …)
├── inventories/          # The 1,000-seed armory from Brief 088A, organized by what the seed produces
│   ├── lighting/         #   A. Atmospheric and lighting (50)
│   ├── weather/          #   B. Weather and environment (60)
│   ├── materials/        #   C. Materials showcase (80)
│   ├── fx/               #   D. Combustion and effects (50)
│   ├── fluid/             #  E. Liquids and fluids (40)
│   ├── character/        #   F. Exemplar fictional cast (60, is_fictional:true mandatory)
│   ├── creature/         #   G. Creatures and animals (60)
│   ├── plant/            #   H. Plants and ecosystems (50)
│   ├── building/         #   I. Architecture and interiors (80)
│   ├── vehicle/          #   J. Vehicles (40)
│   ├── food/             #   K. Food and table scenes (50)
│   ├── music/            #   L. Music and audio scenes (40)
│   ├── camera/           #   M. Camera and cinematography (40)
│   ├── style/            #   N. Style adapters as runnable seeds (80)
│   ├── scene/            #   O. Composite showpieces (100)
│   ├── framework/        #   P. Meta-seed workflows (80)
│   ├── algorithm/        #   Q. Algorithmic primitives as seeds (40)
│   └── cross-domain/     #   Functor bridges (sprite → music, character → level, …)
├── recipes/
│   ├── basic-compositions/       # One-shot compose + breed examples
│   ├── evolutionary-loops/       # MAP-Elites, CMA-ES, Novelty Search, DQD templates
│   ├── domain-fusion/            # Functor chains across engines
│   └── advanced-templates/       # Full-game seeds, IP-empire scaffolds
└── validation/           # CI harness: determinism + signature + round-trip tests
```

## Contracts every commons artifact must satisfy

Every `.gspl` source in this tree MUST:

1. Be **pure** — no `Network`, `Time`, or wall-clock effects; all randomness seeded by `name:version`.
2. Compile under the GSPL grammar defined in `language/grammar.ebnf`.
3. Reference only the 17 kernel gene types from `spec/02-gene-system.md` (`scalar`, `categorical`, `vector`, `expression`, `struct`, `array`, `graph`, `topology`, `temporal`, `regulatory`, `field`, `symbolic`, `quantum`, `gematria`, `resonance`, `dimensional`, `sovereignty`).
4. Declare its lineage: a non-primordial seed MUST list its parents; a primordial seed MUST list the `libraries/` modules it consumes.
5. Ship with a matching `.gseed.json` that conforms to `spec/06-gseed-format.md` payload schema. Content hash is **SHA-256 over the JCS canonical payload** per `spec/05-sovereignty.md` and ADR-009. No BLAKE3 anywhere on signature path.
6. Carry a **sovereignty gene** declaring author thumbprint, royalty split (default 7.5% to author, customizable), license, and a signature slot (placeholder acceptable for community PRs; Foundation-signed on merge).
7. Include a `quality_vector` with coherence, fidelity, novelty, aesthetics, constraint, performance in [0,1].
8. Pass `validation/determinism.ts` (growing the same seed twice must produce byte-identical output).

## Terminology — kernel vs content-domain

GSPL has **two** distinct "17-category" taxonomies. Do not confuse them:

- **17 kernel gene types** (spec/02): the closed algebra of value types every seed is built from. Invariant, load-bearing, locked.
- **17 content-domain categories** (Tier A/B compositions like `visual.image`, `audio.music`, `interactive.game`): domain-level engine targets. These are *compositions* of kernel gene types, not new primitives.

When this tree says "gene," it always means the kernel meaning.

## Relationship to the 26 engines

Every engine listed in `engines/` can consume seeds from this commons. Seeds in `inventories/` are tagged with the engines they target (`@targets: [sprite, sculpt-3d, music]`); recipes in `recipes/domain-fusion/` name the functors they cross.

The 11 planned engines (shader, particle, vehicle, fashion, narrative, ui, physics, accessibility, voice, fonts, motion) each get a minimum 20-seed bootstrap under `inventories/` as Phase 1 deliverables.

## The genetic flywheel

The commons is populated by **three converging streams**:

1. **Curated**: Foundation-authored canonical seeds from Brief 088A's 1,000-seed list.
2. **Community**: Pull requests under `CONTRIBUTING-seeds.md` with automatic CI validation.
3. **Agent**: The Full-Capacity GSPL Agent (`intelligence/gspl-agent-full-capacity.md`) runs a self-bootstrapping loop that generates, validates, and archives new seeds autonomously. Every validated agent seed enriches the training corpus, which improves the Agent, which generates better seeds.

This is the closed loop that turns the commons into a **compounding moat**: no other creative substrate has a genetically self-improving, open, deterministic creator agent populating its canonical library at planetary scale.

## License

Every artifact in this tree is released under the **GSPL Open Specification License**: free forever, no paywalls, no usage limits, forkable, self-hostable, no cloud dependency. Run it on your laptop, your server, a federation peer, or nothing at all — the substrate is yours.

## See also

- `research/088A-canonical-seed-armory.md` — the curation blueprint
- `spec/02-gene-system.md` — the 17 kernel gene types
- `spec/05-sovereignty.md` — canonicalization, hashing, signing
- `spec/06-gseed-format.md` — `.gseed` binary format (ADR-009 locked)
- `intelligence/gspl-agent-full-capacity.md` — the agent that populates this commons
- `CONTRIBUTING-seeds.md` — how to add your own seed to the commons
