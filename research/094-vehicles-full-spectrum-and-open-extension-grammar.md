# 094 — Vehicles across the full spectrum and the substrate open-extension grammar (the "anything I forgot to ask for" guarantee)

## Question
How does GSPL ship with **the full spectrum of vehicles humanity has ever imagined** — every era, every culture, every art style, every level of stylization from photoreal Bugatti to anthropomorphic Pixar tow truck to Ghibli flying-castle to Star-Wars-grade starfighter archetype to steampunk dirigible to magical broomstick to mecha to submarine to chariot to camel caravan — *and* how does the substrate guarantee that **anything the creator (or the user, or the agent, or the founder) failed to mention** still composes as a first-class signed substrate primitive, without the foundation team needing to write a new brief every time someone imagines something new?

## Why it matters
Brief 086F enumerated 150 vehicle classes as substrate primitives. That was the floor. The creator's actual imagination is unbounded: they want a sentient pickup with eyes and a southern drawl rolling through a desert canyon at golden hour, *and* a five-rotor coaxial tilt-wing VTOL with chrome and decals, *and* a Mars-colony rover with solar wings, *and* a horse-drawn imperial Roman chariot, *and* a bone-chariot pulled by skeletal direwolves, *and* a magical girl's transforming scooter, *and* a Voltron-style five-lion combiner, *and* a cyberpunk hover-bike with neon underglow, *and* a Studio Ghibli cat-bus, *and* a 1973 Lincoln Continental in butter-yellow, *and* a Mongol war-cart, *and* a coracle. The substrate must own all of it — and it must own *the next thing the creator hasn't thought of yet* without needing a foundation patch.

This brief does two things at once:

1. **Lifts the vehicle substrate to full-spectrum coverage** with stylization, era, culture, narrative role, and propulsion-system parameterization.
2. **Establishes the substrate's open-extension grammar** — the substrate-level mechanism by which any creator can add a new category that the foundation team didn't ship, and have it instantly become a first-class signed substrate citizen with full lineage, reference fetching, federation, validation, and composition.

The first guarantees breadth. The second guarantees future-proofing.

## What we know from the spec
- Brief 086F: built world, 150 vehicle classes, trademark non-overlap zone (INV-335).
- Brief 083: materials.
- Brief 084: particles and fields.
- Brief 086C: audio (engine sounds, propulsion sounds, signature horn vocabulary).
- Brief 086H: psychology (anthropomorphic personality binding for sentient vehicles).
- Brief 088: character canon (vehicles as `char://` when sentient).
- Brief 088A: canonical seed armory.
- Brief 089: conversion pipeline.
- Brief 090: web reference fetcher.
- Brief 091: federated knowledge graph.
- Brief 092: power systems (six character interaction operators including `pilot_bind` and `weapon_bind`).
- Brief 093: studio techniques and art frameworks.

## Findings — Part A: vehicle substrate v2 (full spectrum)

### A.1 The vehicle gseed schema (`vehicle://`) v2
A vehicle gseed in v2 declares a complete substrate-level definition across these axes:

- **Class taxonomy** — land / water / air / space / amphibious / hybrid / underground / sub-surface / interdimensional / pocket-dimensional / metaphysical (souls, spirits, dream-vessels).
- **Subclass** — wheeled / tracked / legged / hovering / sailing / propeller / jet / rocket / ion / warp / FTL / sail / paddle / oar / rowed / pulled-by-animal / carried / magical / pneumatic / clockwork / steam / electric / solar / nuclear / antimatter / soul-powered / muscle-powered / wind / current / gravity-driven / pedaled / pushed.
- **Era** — stone-age, bronze-age, iron-age, classical, medieval, early-modern, industrial, pre-WW1, interwar, WW2, post-war, atomic-age, cold-war, space-age, modern, near-future, mid-future, far-future, post-singularity, post-apocalyptic, mythic-timeless, alternate-history, mythological-eternal.
- **Culture / regional grammar** — every culture's vehicle traditions seeded with respect contracts (Brief 086E): Indigenous canoes (Polynesian outriggers, Iroquois birchbark, Inuit umiak, Inuit kayak, Yaghan canoe), African watercraft (Egyptian reed boat, Bantu dugout, Madagascan vintana outrigger), Middle Eastern (dhow, sambuk), South Asian (catamaran, kettuvallam, jhelum boat), Southeast Asian (junk, jong, prahu, sampan), East Asian (Chinese junk, sampan, Korean turtle ship, Japanese kobaya), Central Asian (yurt-cart, war chariot), European (longship, cog, carrack, galleon), Americas (mound-builder bull-boat, Mesoamerican litter, Andean caravan), Arctic (dog sled, reindeer sled).
- **Stylization range** — photoreal / hyperreal / industrial-realistic / illustrative / cel-shaded / cartoon / chibi / pixar-anthropomorphic / ghibli-soft / aardman-clay / anime-mecha / shonen-cool / seinen-grimy / cyberpunk-neon / steampunk-brass / dieselpunk-rivet / atompunk-chrome / solarpunk-organic / biopunk-fleshy / magicpunk-runes / decopunk-streamline / vaporwave-pastel / mythological-gilded / horror-bone / dream-impossible. Stylization is selectable per render via the Brief 088 style adapters and Brief 093 art-framework lanes.
- **Propulsion-system gseed** (`propulsion://`) — the substrate primitive that powers the vehicle. Seeded propulsion systems: muscle (human, animal, slave-galley, cycling, paddle, oar, sail, kite), wind (sail, kite, rotor, prop, balloon), wave-current, animal-pulled (horse, ox, dog, reindeer, camel, elephant, dragon, mammoth, dire-wolf, mythical), steam (piston, turbine, traction, locomotive), internal combustion (gasoline, diesel, rotary, turbine, two-stroke, four-stroke, V-twin, V8, V12, W16, flat-six, inline-six, radial), electric (battery, fuel cell, hybrid, wireless, solar), nuclear (fission reactor, RTG, nuclear thermal, NERVA), fusion (tokamak, inertial, cold), ion (gridded, Hall-effect, magnetoplasmadynamic), plasma, antimatter, warp / FTL / hyperspace / jump-drive (substrate-typed with conservation flags), gravity-drive, anti-gravity, magical (mana-engine, prayer-engine, soul-engine, demon-bound), psionic (mind-driven, thought-piloted), summoned, alchemical (transmutation propulsion), clockwork, pneumatic, hydraulic, magnetic (rail, mag-lev, coilgun-launched), solar-sail, photon-sail, dreamfold, runic.
- **Movement model** — substrate-typed kinematic and dynamic model. Wheeled-Ackermann, tracked-skid-steer, legged-walker (bipedal, quadrupedal, hexapodal, octopedal, n-legged, mech-piloted), boat-displacement, boat-planing, boat-hydrofoil, ground-effect, helicopter-rotor, multi-rotor, tilt-rotor, fixed-wing, lifting-body, glider, balloon, dirigible, blimp, rocket-thrust, ion-drift, space-coast, space-orbit, hyperspace-jump, magical-glide, magical-warp, dimensional-shift. The model is differentiable so the substrate can simulate physics or hand-key animation depending on the target medium.
- **Crew slots** — pilot, co-pilot, gunner, navigator, mechanic, passenger, cargo, officer, captain, helmsman, signaler, summoner, mage, spirit-medium. Each slot has a binding signature so a `char://` can `pilot_bind` (Brief 092) into it.
- **Loadout slots** — weapon mounts, sensor mounts, cargo bays, fuel tanks, life-support tanks, modular hardpoints, decorative hardpoints (decals, banners, trophies, charms).
- **Performance envelope** — substrate-typed top speed, acceleration, turning radius, climb rate, dive rate, range, payload, crew capacity, armor, shield, life-support duration, fuel capacity, power generation, signature emissions (heat, light, sound, radio, magic, ki, chakra, soul). Performance is bound to art framework — the same vehicle gseed can declare a "cinematic performance" envelope (anything goes for narrative) and a "simulation performance" envelope (physics-realistic) (Brief 092 INV-362 multi-ruleset balance proofing applies).
- **Material loadout** — body panels, frame, glass, tires, treads, sails, ropes, deck, interior fabric, dashboard, paint, decals, weathering layer, dirt layer, blood layer, magical-glow layer (Brief 083).
- **Audio loadout** — engine idle, engine rev, engine redline, gear shift, brake squeal, tire screech, turbine whine, rotor thump, sail flap, hull creak, footstep (for walkers), thruster ignition, hyperspace whoosh, magical hum, signature horn, signature siren, signature theme stinger (Brief 086C).
- **Visual signature loadout** — exhaust trail, contrail, wake, dust trail, ion trail, hyperspace streak, magical aura, ki aura, headlight cone, taillight glow, neon underglow, holographic decal, banner cloth physics, cape physics, flag physics (Brief 084).
- **Sentient flag** — `false` for non-sentient props; `true` for anthropomorphic vehicles. When `true`, the vehicle is also a `char://` (Brief 088) with a face-binding (eyes-on-windshield, mouth-on-grille, expression channel via Brief 086H FACS adapted to vehicle topology), a personality gseed (Brief 086H), a voice slot (Brief 086C), and a power system gseed (Brief 092 — many sentient vehicles have a built-in propulsion power system that *is* their power system).
- **Transformation slots** — `form://` references (Brief 092). Used for transforming vehicles: car → robot, motorcycle → mech, jet → mech, magical scooter → magical girl mount, train → battle-train, sub → carrier, mecha-combiner (five-lion → big-lion, three-mecha → super-mecha). Combiner support uses the Brief 092 `fuse` operator.
- **Refusal flag** — substrate-level refusal commitments inherit from Brief 086F INV-335 (no trademarked-specific named vehicles in the foundation namespace), Brief 092 INV-365 (no trademarked-specific named characters), and Brief 089 INV-350 (no weapon manufacturing schematics — depiction-grade only, no real-world weapons engineering data even on military vehicles).

### A.2 Seeded coverage at v1
The foundation namespace ships at least:

- **600 archetype vehicle gseeds** across all classes / subclasses / eras / cultures / stylizations.
- **80 propulsion system gseeds** spanning the full propulsion spectrum (muscle through magic).
- **30 movement model gseeds** (Ackermann, skid-steer, legged-walker variants, displacement, planing, rotor, fixed-wing, rocket, ion, warp, magical-glide, etc.).
- **40 transformation rigs** (car ↔ robot, jet ↔ mech, motorcycle ↔ mech, train ↔ battle-train, combiner-3, combiner-5, magical-girl-mount, henshin-cycle, etc.).
- **120 cinematography presets** for vehicle sequences (chase cam, cockpit cam, dogfight cam, drift cam, hyperspace push-in, dramatic three-quarter-low-angle hero shot, helicopter following car, drone-pull-back reveal, etc.).
- **200 vehicle armory seeds** added to the canonical armory (Brief 088A).

Every vehicle gseed exposes its full composition graph (Brief 088A INV-346) so creators learning the substrate can fork, mutate, restyle, re-era, re-culture, re-propulsion, and re-medium without losing identity.

### A.3 Sentient-vehicle examples (archetypes only, no trademarks)
- `vehicle://anthropomorphic/red-rusty-tow-truck-with-buck-teeth-and-southern-drawl` — sentient vehicle archetype with Pixar-grade craft stack (Brief 093) and personality gseed (Brief 086H).
- `vehicle://anthropomorphic/overconfident-hotshot-race-car-protagonist` — race-car protagonist archetype.
- `vehicle://anthropomorphic/wise-old-sky-pirate-airship-with-grumbling-ai` — airship-with-personality archetype.
- `vehicle://magical/cat-shaped-living-public-transit-with-glowing-eyes` — Ghibli-grade craft stack (Brief 093) magical-creature-vehicle archetype.
- `vehicle://magical/childhood-bedroom-bed-that-flies-on-moonlight` — dreamfold-propulsion archetype.

Each archetype is composable into a creator-namespaced character. The substrate provides the lane; the creator provides the name.

## Findings — Part B: the substrate open-extension grammar

This is the substrate-level guarantee that **anything the creator failed to mention still composes as a first-class citizen** without a foundation patch.

### B.1 The extension protocol
Every substrate URL scheme (`chem://`, `phys://`, `mat://`, `fx://`, `bio://`, `earth://`, `astro://`, `math://`, `audio://`, `lang://`, `culture://`, `arch://`, `urban://`, `vehicle://`, `propulsion://`, `textile://`, `garment://`, `food://`, `psy://`, `char://`, `power://`, `form://`, `move://`, `henshin://`, `evolution://`, `progression://`, `status://`, `medium://`, `studio-technique://`, `art-framework://`, `pipeline://`, `beat://`, `color-script://`, `performance://`, `cinematography://`, `seed://`, `ref://`) is **open-set**. New URL schemes are first-class citizens of the substrate the moment a creator signs one and publishes it through the federated knowledge graph (Brief 091).

A new substrate-extension is itself a signed gseed:

```
ext://<scheme-name>@vN
  scheme: <scheme-name>
  parent_schemes: [<schemes this extends>]
  fields: <typed schema for nodes under this scheme>
  invariants: <substrate-checkable invariants>
  validators: [<gseed validators that must pass>]
  composition_rules: <how nodes under this scheme compose with existing schemes>
  refusal_envelope: <constitutional commitments for nodes under this scheme>
  attribution: <source-culture credits if applicable>
  signed_by: <creator identity>
  forever_signed_by: <creator identity (Brief 078)>
```

The substrate **does not gate-keep** new schemes. Anyone with a federation identity can publish an extension. The federation knowledge graph stores extensions with full lineage. Other creators can adopt them by composing against them.

### B.2 Promotion to foundation namespace
An extension scheme published by a creator can be **promoted** to the foundation namespace through a transparent process:

1. **Adoption metric** — the federation tracks how many distinct creator identities compose against the extension. When adoption crosses a published threshold the extension becomes a candidate.
2. **Quality review** — the foundation critic ensemble (Brief 074) runs the extension through substrate-level quality checks: invariant clarity, composition compatibility, refusal envelope completeness, source attribution, validator coverage.
3. **Constitutional check** — the foundation refusal envelope (the eleven Round 4 constitutional commitments) is applied to the extension; if it fails, the extension remains creator-namespace only.
4. **Public RFC** — the candidate extension is published as a public RFC for federation comment.
5. **Promotion** — if the RFC passes, the extension is signed under the foundation identity, the original creator's identity is preserved as `forever_signed_by` (Brief 078), and the extension becomes a foundation-namespace primitive.

This is how the substrate grows. The foundation team writes the seed; the federation grows the rest. **The substrate is built to outlast its founders.**

### B.3 The "I forgot to ask for it" workflow
When the user mentions something the substrate doesn't have a primitive for, the agent runs:

```
NEED → SEARCH armory → SEARCH knowledge graph → SEARCH federation extensions
     → if still not found → FETCH references (Brief 090)
     → COMPOSE candidate gseed from existing primitives
     → if no existing primitive composes → PROPOSE extension scheme
     → SHOW user the proposed extension and the candidate gseed
     → user accepts → SIGN under user's identity
     → STORE in knowledge graph (Brief 091)
     → if user opts in → PUBLISH to federation
     → if adoption grows → CANDIDATE for foundation promotion
```

The user's "I forgot to ask for X" becomes a substrate extension. The substrate's coverage *grows by use*.

### B.4 Open extension examples
- A creator wants an `aroma://` substrate scheme for olfactory primitives (vanilla, petrichor, ozone, gunpowder, jasmine) so their writing tools and immersive media can compose smell. They publish `ext://aroma@v1` with field schemas grounded in the perfumery and food-science literature.
- A creator wants a `tactile://` substrate scheme for haptic primitives (rough, smooth, pebbled, slick, sticky, fuzzy, prickly, warm, cool, vibrating, throbbing) for haptic-feedback controllers. They publish `ext://tactile@v1`.
- A creator wants a `taste://` substrate scheme for flavor primitives (sweet, sour, salty, bitter, umami, kokumi, metallic, astringent, fatty) composing with `food://` (Brief 086G).
- A creator wants a `social-norm://` substrate scheme for cultural-protocol primitives (greeting forms, taboo avoidance, hospitality rituals, mourning protocols) composing with `culture://` (Brief 086E).
- A creator wants a `weather-emotion://` substrate scheme for the way weather binds to character mood across narrative (rain → melancholy, sunrise → hope, fog → uncertainty) composing with `earth://` (Brief 086) and `psy://` (Brief 086H).
- A creator wants a `political-system://` substrate scheme for government and faction primitives.
- A creator wants a `magic-system://` substrate scheme for hard-magic and soft-magic system definitions composing with `power://` (Brief 092).
- A creator wants a `monster://` substrate scheme for original creature designs composing with `bio://` (Brief 085) and `power://` (Brief 092).
- A creator wants a `currency://` substrate scheme for economic primitives in their fictional setting.
- A creator wants a `calendar://` substrate scheme for fictional time systems.
- A creator wants a `language-evolution://` substrate scheme for con-lang historical phonological shifts composing with `lang://` (Brief 086D).

None of these require a foundation patch. The substrate ships open. The federation grows them in. The foundation curates the best.

### B.5 Constitutional commitments carried into the open extension grammar
- **All Round 4 refusal commitments** apply to extensions. An extension that publishes a scheme for "deepfake-living-person-likeness" is refused at the federation mirror layer; it cannot be promoted to the foundation namespace under any adoption threshold.
- **Source-culture attribution** is enforced for extensions rooted in living cultural traditions (Brief 086E).
- **Trademark refusal** is enforced for extensions targeting trademarked-specific named entities (Briefs 086F, 088, 092, 093).
- **Care contracts** are enforced for extensions targeting clinical, mental-health, medical, or vulnerable-population content (Brief 086H INV-339).
- **Consent + privacy** are enforced for extensions ingesting user data (Brief 089 + Brief 077 + Brief 091 tombstone deletion).
- **Lineage preservation** is enforced — every extension carries `forever_signed_by` to its original author (Brief 078).
- **Anti-hallucination grounding** is enforced — extension fields with measured semantics must declare their measurement source (Brief 091 INV-357).

The open extension grammar is **not a free-for-all**. It is a transparent, lineage-bearing, constitutionally-bounded growth surface.

## Inventions

### INV-375: Vehicle gseed v2 with full-spectrum stylization, era, culture, and propulsion parameterization
The vehicle substrate is lifted from the 150-class floor of Brief 086F to a v2 schema covering land/water/air/space/amphibious/hybrid/underground/sub-surface/interdimensional/pocket-dimensional/metaphysical classes, every era from stone-age through post-singularity, every cultural vehicle tradition with respect contracts, every stylization lane from photoreal through anthropomorphic-cartoon through magical-creature, with separable propulsion-system gseeds and substrate-typed movement models. Novel as a substrate-level vehicle grammar that covers the full creator imagination space.

### INV-376: Propulsion system as substrate primitive
Every propulsion system — muscle, wind, animal, steam, internal combustion, electric, nuclear, fusion, ion, plasma, antimatter, warp, gravity, magical, psionic, summoned, alchemical, clockwork, pneumatic, magnetic, solar-sail, photon-sail, dreamfold, runic — is a signed `propulsion://` substrate primitive declaring resource consumption, signature emissions, conservation flags, and material/audio/visual bindings. Novel as a substrate-level propulsion grammar independent of vehicle class.

### INV-377: Sentient vehicle as character × vehicle × power system composition
A sentient vehicle is a single signed entity that is simultaneously a `char://` (Brief 088), a `vehicle://`, and a `power://` (Brief 092), with a substrate-level binding that maps face channels to vehicle topology, personality to behavior, and propulsion to power resource. Novel as a substrate-level uniform treatment of anthropomorphic vehicles.

### INV-378: Substrate open-extension protocol
Every substrate URL scheme is open-set. New schemes are signed as `ext://` gseeds with typed field schemas, substrate-checkable invariants, validators, composition rules, and refusal envelopes. Anyone with a federation identity can publish an extension; the foundation does not gate-keep. Novel as a substrate-level open growth protocol that does not require foundation patches.

### INV-379: Foundation promotion pathway with forever-signed creator credit
An extension can be promoted from creator-namespace to foundation namespace via adoption metric → quality review → constitutional check → public RFC → promotion, with the original creator's identity preserved as `forever_signed_by` (Brief 078). Novel as a substrate-level meritocratic growth pathway with permanent attribution.

### INV-380: "I forgot to ask for it" workflow as substrate-level coverage guarantee
The agent's response when the user mentions something with no existing primitive is a deterministic workflow: search armory → search knowledge graph → search federation extensions → fetch references → compose candidate from existing primitives → if no composition possible, propose extension scheme → user accepts → sign under user identity → store in knowledge graph → optional federation publish. The substrate's coverage grows by use. Novel as a substrate-level guarantee that no creator request bottoms out at "the substrate doesn't support that yet."

### INV-381: Constitutional bounds on the open extension grammar
All Round 4 constitutional commitments (refusal envelopes for living-person likeness, trademarked named entities, sacred-restricted symbols, weapon schematics, fabricated documentary content, mental-health depiction without care contract, copyright laundering) apply to extension schemes. The federation refuses to mirror extensions that violate them, and they cannot be promoted to foundation namespace under any adoption threshold. Novel as a substrate-level guarantee that openness does not weaken the constitutional layer.

## Phase 1 deliverables

- **`vehicle://` v2 schema** with all 12 axes at v1.
- **600 archetype vehicle seeds** in the foundation namespace at v1.
- **`propulsion://` schema** with 80 seeded propulsion systems at v1.
- **30 movement model gseeds** at v1.
- **40 transformation rig gseeds** (car ↔ robot, jet ↔ mech, combiners) at v1.
- **120 cinematography presets** for vehicle sequences at v1.
- **Sentient vehicle binding contract** wiring `char://` ↔ `vehicle://` ↔ `power://` at v1.
- **`ext://` schema** with the full extension protocol at v1.
- **Federation extension publish + mirror flow** at v1.
- **Foundation promotion pathway** (adoption metric, quality review, constitutional check, public RFC, signed promotion with creator credit) at v1.
- **"I forgot to ask for it" agent workflow** wired through Brief 089 + Brief 090 + Brief 091 at v1.
- **Constitutional refusal layer** for extensions at v1.
- **Armory contribution:** 200 vehicle seeds added to the canonical armory (Brief 088A).

## Risks

- **Trademark gravity (vehicles).** Mitigation: lane + archetype naming, foundation namespace refusal of trademarked named vehicles, creator-namespace fan-work signing under creator identity (Brief 086F INV-335 carried forward).
- **Real-world weapon engineering leakage on military vehicles.** Mitigation: depiction-grade only — substrate refuses to ship internal weapon-system schematics on real military vehicles, only the visible/exterior depiction (Brief 089 INV-350 carried forward).
- **Open extension protocol abuse.** Mitigation: constitutional refusal layer at the federation mirror layer (INV-381); critic ensemble review on promotion (Brief 074).
- **Extension scheme collision.** Mitigation: scheme names are namespaced under creator identity until promotion; promoted schemes are content-addressed by canonical hash and versioned.
- **Foundation promotion bias.** Mitigation: adoption metric is published, RFC is public, critic ensemble is multi-perspective, original-author credit is constitutional.
- **Sentient-vehicle uncanny valley.** Mitigation: face channel mapping is calibrated per stylization lane (Pixar-grade vs Ghibli-grade vs anime vs photoreal); the substrate refuses to render photoreal sentient-vehicle face channels by default and requires the creator to explicitly opt into uncanny territory.

## Recommendation

1. **Lock the `vehicle://` v2 schema, the `propulsion://` schema, and the `ext://` schema at v1.**
2. **Seed the 600 archetype vehicles, 80 propulsion systems, 30 movement models, 40 transformation rigs, and 120 cinematography presets** in the foundation namespace.
3. **Wire the sentient-vehicle binding contract** so anthropomorphic vehicles compose uniformly.
4. **Implement the open extension protocol** including the federation publish + mirror flow.
5. **Publish the foundation promotion pathway** with the adoption metric, RFC format, critic ensemble process, and creator-credit constitutional commitment.
6. **Wire the "I forgot to ask for it" agent workflow** as a substrate-level guarantee — *no creator request ever bottoms out at "not supported"*.
7. **Apply all eleven Round 4 constitutional commitments** to extensions; refuse to mirror or promote violations.
8. **Add 200 vehicle seeds to the armory** (Brief 088A).
9. **Engage cultural-vehicle consultancies** (Indigenous canoe builders, dhow shipwrights, traditional cartwrights, etc.) for the culturally-rooted vehicle archetypes.

## Confidence
**4/5.** Architecture composes cleanly with every Round 4 brief. The open extension grammar is the most consequential addition because it gives the substrate a future-proof growth surface that does not depend on the foundation team to keep up with creator imagination.

## Spec impact

- `inventory/vehicles-v2.md` — new doc.
- `inventory/propulsion-systems.md` — new doc.
- `inventory/movement-models.md` — new doc.
- `inventory/transformation-rigs.md` — new doc.
- `inventory/sentient-vehicles.md` — new doc.
- `inventory/extension-protocol.md` — new doc.
- `inventory/foundation-promotion-pathway.md` — new doc.
- New ADR: `adr/00NN-vehicle-substrate-v2.md`.
- New ADR: `adr/00NN-propulsion-as-substrate-primitive.md`.
- New ADR: `adr/00NN-sentient-vehicle-binding-contract.md`.
- New ADR: `adr/00NN-substrate-open-extension-protocol.md`.
- New ADR: `adr/00NN-foundation-promotion-pathway.md`.
- New ADR: `adr/00NN-constitutional-bounds-on-extension-grammar.md`.

## Open follow-ups

- 600-vehicle seed authoring across all classes / eras / cultures / stylizations.
- 80-propulsion seed authoring with measured emission profiles.
- 40-transformation rig authoring with substrate-level rig topology.
- Cultural-vehicle consultancy outreach.
- Foundation promotion adoption-threshold calibration.
- Extension RFC format and federation comment surface.
- Sentient-vehicle face-channel calibration per stylization lane.
- Studio UI for vehicle composer, propulsion picker, and extension authoring.

## Sources

- Internal: Briefs 074, 077, 078, 083, 084, 085, 086, 086C, 086E, 086F, 086G, 086H, 088, 088A, 089, 090, 091, 092, 093.
