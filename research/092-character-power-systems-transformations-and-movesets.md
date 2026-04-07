# 092 — Character power systems, transformations, and movesets (the "anything is possible" substrate)

## Question
How does GSPL guarantee that **anything** a creator imagines about a character — every transformation, every signature move, every power-scaling rule, every stance, every fusion, every henshin sequence, every summons, every contract, every form-stack, every awakened state, every ultimate technique — composes into the substrate as a signed, lineage-bearing, replayable, balanced gseed, **without the substrate ever needing the creator to "ask permission" for a category that wasn't explicitly enumerated**?

## Why it matters
A character canon (Brief 088) without a power system is a portrait. A creator who imagines a character like Naruto needs Sage Mode, Kyuubi Chakra Mode, Six Paths Sage Mode, Sage of Six Paths cloak, Bijuu Mode, Tailed Beast Bomb, Rasengan, Rasenshuriken, Wind Style Rasenshuriken, Multi Shadow Clone Jutsu, Kage Bunshin → Rasengan compositional combos, sealing techniques, contract summons (Gamabunta), and the costume / aura / lighting / camera framing that goes with each form. A creator who imagines a character like Goku needs base, Kaio-ken (×N), Super Saiyan 1/2/3/God/Blue/Blue Kaio-ken/Blue Evolved/Ultra Instinct Sign/Mastered Ultra Instinct, Kamehameha (and every variant: Super, ×10, x20, Father-Son, Instant Transmission, Angry), Spirit Bomb, Dragon Fist, Solar Flare, Instant Transmission, fusions (Vegito, Gogeta — both via Potara and Fusion Dance), and the entire ki-aura material binding for each form.

The substrate must support **all** of this — not as hand-coded special cases for two anime characters, but as a **general substrate primitive layer for power systems** that the creator composes once and reuses for any character, any IP archetype, any future transformation a creator hasn't even invented yet.

This brief makes the "I can build anything" promise of Brief 088 actually true.

## What we know from the spec
- Brief 085: composable rigs and the age parameter.
- Brief 086H: FACS performance substrate, emotion models, personality.
- Brief 088: character gseed schema, style invariants, identity embedding, cross-style coherence, refusal of living-person gseeds.
- Brief 088A: canonical seed armory.
- Brief 084: particles and fields (ki auras, chakra wisps, mana glows).
- Brief 083: materials (cloth, metal, energy plasma).
- Brief 086C: audio (signature attack callouts, transformation jingles).
- Brief 091: federated knowledge graph (movesets compose through edges).
- Brief 089: refusal envelope (the substrate refuses copyrighted-trademark-specific named characters in the foundation namespace; creator-namespaced fan content is the creator's responsibility under their own identity).

## Findings — the architecture

### 1. Power-system gseed (`power://`)
Every power system — ki, chakra, mana, nen, cursed energy, haki, breathing styles, devil fruit, stand, quirk, semblance, persona, alchemy, psionics, force, geass, magic circle, cybernetic loadout, mech link, mutation, blood inheritance, divine pact, soul weapon binding, alchemical transmutation, time manipulation, gravity manipulation, pure-tech gear, summons contract, demon contract, holy contract — is a signed `power://` gseed. URL pattern:

```
power://<system-id>@vN
```

A power system gseed declares:

- **Resource pool(s)** — what is consumed (ki, chakra, mana, stamina, life, sanity, time, breath, ammo, fuel, soul). Each resource has a max, regen rate, regen conditions, drain conditions, overflow rules, and substrate-typed units.
- **State variables** — what mutable character state the system reads and writes (form, stance, mood, alignment, contract bonds, summons active, marks, curses).
- **Composition rules** — how the system stacks with other systems (Goku has both ki and Kaio-ken multiplier and Ultra Instinct dodge override; Naruto has chakra plus Sage Nature Energy plus Bijuu chakra borrow).
- **Constraint laws** — conservation, decay, reflection, absorption, type-effectiveness matrices.
- **Material bindings** — what materials and particle fields the system manifests as (Brief 083 + Brief 084).
- **Audio bindings** — what audio the system manifests with (Brief 086C: charge-up, release, signature callout placeholders).
- **Visual bindings** — aura layers, post-processing, hair physics overrides, eye overrides, iris overrides, voice register shifts.

Power systems are **substrate primitives**, not character properties. A character `composes` one or more power systems. A power system can be reused across thousands of characters without redefinition.

### 2. Transformation gseed (`form://`)
Every transformation — base, Super Saiyan 1/2/3/God/Blue/Blue Kaio-ken/Blue Evolved/Ultra Instinct Sign/Mastered Ultra Instinct, Sage Mode, Kyuubi Chakra Mode, Six Paths Sage Mode, Bijuu Mode, magical girl post-henshin, kamen rider armored, gear-fourth, shikai, bankai, second gear, third gear, snake mode, devil trigger, awakened, berserk, calm, demon form, angel form, beast form, dragon form, mech-piloted, summons-merged, fusion form, absorbed form, possessed form, half-life form, ghost form, time-frozen form, dimension-shifted form — is a signed `form://` gseed. URL pattern:

```
form://<character-namespace>/<form-id>@vN
```

A form gseed declares:

- **Parent form(s)** — what form(s) this is reachable from (a DAG, not a tree; Goku Blue Kaio-ken has parents Blue and Kaio-ken).
- **Activation cost** — resource consumption from one or more power systems.
- **Activation condition** — narrative gate (emotional trigger, allied death, full moon, contract bond strength ≥ N, total cumulative damage ≥ N, first time only, requires meditation, requires verbal incantation, requires hand seals, requires kissing partner, requires belt activation).
- **Sustain cost** — drain per substrate tick.
- **Stat deltas** — multiplicative or additive overrides on speed, strength, durability, ki/chakra max, regen, perception, reaction time, dimensional reach.
- **Visual delta** — hair color/length/style override, eye override, aura override, scleral override, marking override, body proportion override (Brief 088 invariants are preserved unless explicitly broken; identity embedding survives transformation), wardrobe override or augmentation.
- **Audio delta** — voice register, breathing pattern, footstep audio, ambient hum.
- **Personality delta** — Big Five / HEXACO shifts (Brief 086H), restraint loss, calm gain, instinct override, emotion suppression, berserker rage.
- **Moveset delta** — which moves unlock, which moves change behavior in this form, which moves are locked out.
- **Drawback** — life drain, time limit, post-form exhaustion, stamina debt, sanity decay, irreversible damage, scarring, blood debt to a contract holder.
- **Cinematic gseed** — the henshin sequence (animation + audio + camera + lighting + particles, signed independently and reusable).
- **Refusal of cosmetic-only "infinite power" forms.** Substrate constraint laws still apply; a form cannot escape its declared resource budget.

### 3. Move gseed (`move://`)
Every signature attack, ability, technique, jutsu, jutsu-shiki, spell, weapon art, ultimate, super, hyper combo, finisher, breath form, swing, stance transition, magic spell, alchemy circle, devil fruit power, stand ability, hamon, kido, geass command, semblance use, persona summon, gear shift, henshin sequence, fusion dance, focused attack — is a signed `move://` gseed. URL pattern:

```
move://<character-namespace>/<move-id>@vN
```

A move gseed declares:

- **Owner forms** — which `form://` gseeds can use this move.
- **Resource cost** — from declared power systems.
- **Charge time, startup, active, recovery** — frame data in substrate-typed units (works for cinematics, real-time, and turn-based engines because frame data is differentiable and rescalable).
- **Range geometry** — point, ray, cone, sphere, box, beam, line-of-sight, around-self, ground-plane, area-of-effect with falloff.
- **Hit boxes / hurt boxes / clash priority** — substrate-level geometric primitives (Brief 086B).
- **Damage / heal / status** — typed effect (kinetic, thermal, energy, soul, psychic, gravity, time, status, control), magnitude as a function of stat deltas, status effects with durations and stack rules.
- **Material binding** — projectile material (Brief 083), fluid solver if applicable (Brief 084), explosion class, scorch decal class, terrain interaction.
- **Visual binding** — particles, aura, lighting, camera shake, hit-stop, time-dilation envelope, post-processing, screen tint.
- **Audio binding** — charge sound, fire sound, impact sound, voice line slot (the slot is a `lang://` reference; the actual line is creator-supplied or generated under the creator's identity, never under the foundation identity for trademarked characters).
- **Combo edges** — which moves chain into this move, which moves this move chains into, with timing windows.
- **Cancel rules** — what can interrupt this move and at what cost.
- **Compositional invariants** — what must remain true across every art-style render of this move (e.g., Rasengan is always a sphere of swirling chakra in the right palm; Kamehameha is always a two-handed cupped beam from below; Final Flash is always a one-handed forward palm beam — the substrate enforces these invariants across every style adapter from Brief 088).
- **Cinematic moment markers** — frames that should always be camera-prioritized in cinematic mode.

### 4. Combo, stance, and ability graph
Moves are nodes in a per-character combo graph stored in the knowledge graph (Brief 091). Edges are typed:

- `chains_into` — combo follow-up.
- `cancels_into` — interrupt allowed.
- `transitions_form` — move triggers a transformation.
- `requires_form` — gate.
- `unlocks_after` — narrative or training gate.
- `counters` — cancels a specific incoming move type.
- `clashes_with` — produces a substrate-defined clash event.
- `evolved_form_of` — Rasengan → Big Ball Rasengan → Rasenshuriken → Wind Style: Rasenshuriken.
- `taught_by` — lineage edge to a teacher character (Jiraiya taught Rasengan; Master Roshi taught Kamehameha — for characters in the creator's namespace, the teacher chain becomes a creator-owned narrative lineage).

Stance gseeds (`stance://`) hold a subgraph of moves available in that stance plus the transition cost from any other stance the character knows. Stances compose with forms — a character can be in form Ultra Instinct + stance Mastered, with a moveset that is the union of UI-form moves and Mastered-stance moves filtered by clash priority.

### 5. Fusion, absorption, possession, summons, contract, pilot binding
The substrate provides six general composition operators that work for **any** character relationship, not just specific anime mechanics:

- **`fuse(A, B, fusion_kind)`** — produces a new `char://` whose stat deltas, moveset, form list, personality, and visual identity are a substrate-defined merge of A and B. `fusion_kind` enumerates merge laws (Potara: permanent unless time-limited, Fusion Dance: 30 substrate minutes, Magical Girl Cross-Fusion, Pokémon Mega Evolution bond, Persona stack, Stand-merge, Symbiote bond). Fusion produces a child gseed in the federation graph with `derives_from` edges to both parents (Brief 091).
- **`absorb(A, B)`** — A gains a subset of B's moveset and form list, B is consumed (graph: `absorbed`). The substrate enforces that absorbed power cannot exceed declared resource budgets.
- **`possess(A, B)`** — A's body hosts B's mind/personality with hybrid moveset. Creates a temporary fused gseed with a release condition.
- **`summon(A, contract)`** — A calls a separate `char://` into the scene under a contract gseed (`contract://`) declaring duration, cost, loyalty, range, and termination clause. Used for Naruto's toad summons, Persona summons, Stand summoning, alchemical homunculi, demon contracts, divine bargains, mecha launch sequences (the mech is a vehicle-class summon).
- **`pilot_bind(A, vehicle)`** — A enters a vehicle gseed (Brief 086F) and gains its moveset/form list as overlay. The vehicle's HUD, controls, and material loadout become accessible. Used for mechs, fighter jets, magical brooms, war beasts, dragon-rider bonds.
- **`weapon_bind(A, weapon)`** — A bonds with a soul-weapon gseed that has its own form list and moveset (zanpakutō shikai/bankai, holy sword, cursed blade, divine bow, smart-gun, sentient gauntlet). The weapon is itself a `char://` with restricted personhood flags.

These six operators are the substrate's general grammar for "characters interacting through power systems." Anything a creator can imagine about character→character relationships composes through them.

### 6. Cinematic transformation sequences (`henshin://`)
Every transformation can have an attached signed cinematic sequence: animation timeline + camera path + lighting envelope + particle systems + post-processing + audio score + voice slot, all signed as a reusable `henshin://` gseed. The cinematic is **separable from the form** — a creator can swap cinematics without changing the form's stats, or reuse a single cinematic across many forms (every Saiyan goes Super Saiyan with the same camera moves but their own particle palette and audio palette).

Cinematics declare:

- **Duration scaling** — three lengths (instant, short, full) so the same form works for combat, story, and reveal.
- **Skip rules** — players can skip after first viewing (game engine respects this).
- **Camera invariants** — the cinematic is composable into any scene's camera grammar without breaking continuity (Brief 087 visual coverage).
- **Audio bus assignment** — score, voice, sfx routed properly through the audio substrate.

### 7. Power scaling and balance constraint substrate
A power system / form / move can declare itself **balanced under one or more rulesets**:

- **Cinematic ruleset** — narrative power, no balance enforcement, anything goes within the resource budget. Used for stories.
- **Tournament ruleset** — frame-data and resource budgets enforced, clash priority resolved, no narrative overrides. Used for fighting games.
- **JRPG ruleset** — turn-based, stat-curve enforced, level-gated.
- **Roguelike ruleset** — RNG-modulated, escalation curves enforced.
- **Tabletop ruleset** — dice-resolved, GM override permitted.
- **MMO ruleset** — server-authoritative, anti-cheat-friendly determinism (Brief 075).
- **Simulation ruleset** — physics-realistic, energy conservation enforced.

A character composed of forms and moves is **automatically validated** against the ruleset the creator targets. The substrate reports violations as warnings (not refusals — the creator can knowingly break a ruleset and document it as an exception). This is the substrate-level "balance proofing" that makes character power systems portable across engines.

### 8. Evolution lines and progression trees (`evolution://`, `progression://`)
A character can declare an **evolution line** — a DAG of `char://` gseeds where each node is reachable from the previous via a transformation event (level-up, item use, friendship, time of day, location, training arc completion). Pokémon-style evolution, Digimon-style branching evolution, Yokai-fusion evolution, mech upgrade trees, RPG class promotion, magical girl power-up tiers, stand evolution (Star Platinum → The World), and Persona awakening all share the same `evolution://` substrate type.

A character can also declare a **progression tree** — a graph of moves and forms unlocked at specific narrative or stat milestones. This is the substrate-level "skill tree" used by RPGs, action games, and training-arc cinematics. The creator declares the tree once; every engine that consumes the gseed can render it as a UI, gate it during gameplay, or play it back as a cutscene timeline.

### 9. Status, buff, debuff, and condition substrate (`status://`)
Burn, freeze, paralysis, sleep, confusion, charm, fear, silence, blind, slow, haste, regeneration, poison, bleeding, mark, curse, blessing, divine favor, inspired, exhausted, broken, awakened, drunk, hungry, possessed, hexed, time-frozen, gravity-doubled, mass-halved, phase-shifted, dimension-locked. Every status is a `status://` gseed declaring stack rules, duration, cleanse rules, immunity rules, visual delta, audio delta, behavior delta. Status conditions compose with forms and moves uniformly. The substrate is open — a creator can sign a new status (`status://creator-namespace/lovestruck@v1`) and immediately compose it into any character.

### 10. Refusal commitments (carried from Brief 088 and 089)
- **No trademarked-specific named character gseeds in the GSPL Foundation Identity namespace.** The substrate provides **archetypes** (`char://archetype/spiky-haired-saiyan-warrior`, `char://archetype/orange-jumpsuit-ninja-with-fox-spirit`) and **mechanics** (`power://chakra-and-nature-energy`, `power://ki-with-multiplier-stacks`, `form://nine-tail-fusion`, `move://palm-energy-sphere`, `move://forward-cupped-beam`). A creator can compose these into their own creator-namespaced character. The creator owns and signs that character. The substrate never claims the trademarked named character itself.
- **Power systems and movesets that exist in famous IPs are expressible through the substrate primitives**, just as the substrate's chemistry library can express any molecule without licensing chemistry. Mechanics are not copyrightable; specific named characters are. The substrate respects that line constitutionally.
- **Creator-namespaced characters that are clearly fan-made depictions of trademarked figures** carry a `fan-work` flag and the creator's identity is the only signing party — the substrate refuses to sign such a gseed under the foundation identity but does not block the creator from signing it under their own identity (Brief 077 anonymity tiers + Brief 091 federation visibility apply).
- **No gseeds composed against living-person likenesses** (Brief 088 INV-343).

This is the substrate's honest answer to "can I make Goku?" — *the substrate can express every mechanic, every transformation, every move, every cinematic; it cannot launder the trademark, and it will not pretend otherwise. Your creator-signed Goku is yours; the foundation's job is to give you primitives that make him exactly as powerful as you imagine.*

## Inventions

### INV-358: Power system as substrate primitive
Every power system (ki, chakra, mana, nen, cursed energy, breathing, haki, devil fruit, stand, quirk, semblance, persona, alchemy, psionics, force, geass, magic, cybernetic, mech-link, divine pact, soul-bind, summons contract) is a signed `power://` substrate primitive declaring resource pools, state variables, composition rules, constraint laws, and material/audio/visual bindings. Novel as a substrate-level general grammar for power systems independent of any single IP.

### INV-359: Transformation as substrate primitive with separable cinematic
Every form / transformation / awakening is a signed `form://` gseed declaring activation cost, condition, sustain, stat/visual/audio/personality/moveset deltas, drawback, and a separable signed cinematic gseed. Forms compose into a per-character DAG. Identity embedding survives transformations except where explicitly broken. Novel as a substrate-level transformation grammar with cinematic-separable cinematics.

### INV-360: Move as substrate primitive with cross-style invariants
Every move / technique / spell / ability is a signed `move://` gseed with frame data, range geometry, hit/hurt/clash boxes, typed effects, material/audio/visual bindings, combo edges, and **compositional invariants enforced across every art style**. Rasengan is always the same sphere; Kamehameha is always the same two-handed beam; Final Flash is always the same one-handed palm — across photoreal, anime, watercolor, comic, pixel art, every style adapter. Novel as a substrate-level cross-style moveset coherence contract.

### INV-361: Six-operator character interaction algebra
The substrate provides six composition operators — `fuse`, `absorb`, `possess`, `summon`, `pilot_bind`, `weapon_bind` — that express any character → character relationship: fusion dance, Potara, Persona, Stand bond, Pokémon bond, Symbiote, alchemical homunculus, mecha pilot, demon contract, divine pact, soul-weapon binding, summons contract. Novel as a substrate-level general algebra for character interactions.

### INV-362: Multi-ruleset balance proofing
A character composed of forms and moves is automatically validated against one of seven balance rulesets (cinematic, tournament, JRPG, roguelike, tabletop, MMO, simulation). The substrate reports violations as warnings, not refusals, preserving creator sovereignty while making power systems portable across engines. Novel as a substrate-level cross-engine balance proofing surface.

### INV-363: Evolution line and progression tree as substrate primitives
Pokémon-style evolution, Digimon branching evolution, mech upgrade trees, RPG skill trees, magical-girl power-up tiers, Persona awakening, and Stand evolution all share the same `evolution://` and `progression://` substrate types. Creators declare the tree once; any engine consuming the gseed can render it as UI, gate it during gameplay, or play it back as a cutscene. Novel as a substrate-level unified progression grammar.

### INV-364: Open status condition substrate
Status / buff / debuff / condition is a signed `status://` substrate primitive with stack rules, duration, cleanse rules, immunity rules, and visual/audio/behavior deltas. The space is open — creators sign new statuses and compose them into any character without substrate updates. Novel as a substrate-level open-set status grammar.

### INV-365: Mechanics-yes, trademark-no constitutional commitment for character power systems
The substrate constitutionally provides every mechanic of every famous power system (chakra, ki, nen, cursed energy, breathing styles, devil fruits, stands, quirks, semblances, personas, alchemy) as `power://` gseeds in the foundation namespace, while refusing to sign trademarked-specific named characters under the foundation identity. Creators compose archetype + mechanics + their own naming under their own identity, with full anonymity tier and federation visibility controls. Novel as a substrate-level honest answer to the IP boundary question.

## Phase 1 deliverables

- **`power://` schema** with at least 30 seeded power-system archetypes (chakra, ki, mana, nen, cursed-energy, haki, breathing, devil-fruit, stand, quirk, semblance, persona, alchemy, psionics, force, geass, magic-circle, cybernetic, mech-link, divine-pact, soul-bind, summons-contract, alchemical-transmutation, gravity-manipulation, time-manipulation, dimensional-shift, blood-inheritance, mutation, holy-contract, demon-contract).
- **`form://` schema** with seeded archetype forms (base, awakened, berserk, fused, absorbed, possessed, half-life, ghost, beast, dragon, divine, demon, mech-piloted, henshin-armored, summons-merged).
- **`move://` schema** with seeded archetype moves (palm-energy-sphere, two-handed-cupped-beam, one-handed-palm-beam, multi-clone-strike, sealing-array, summons-call, dimensional-cut, breath-form-attack, stand-strike, persona-cast, alchemical-circle-cast, magic-circle-cast, henshin-finisher, super-finisher, ultimate-finisher).
- **Six character interaction operators** (`fuse`, `absorb`, `possess`, `summon`, `pilot_bind`, `weapon_bind`) at v1.
- **Combo / stance / ability graph** as part of every `char://` gseed at v1.
- **Cinematic henshin gseed schema** (`henshin://`) at v1 with three duration scalings.
- **Multi-ruleset balance proofing** at v1 with all seven rulesets.
- **`evolution://` and `progression://` schemas** at v1.
- **`status://` schema** with at least 60 seeded statuses at v1.
- **Foundation refusal envelope** (no trademarked-specific named characters under foundation identity) at v1.
- **Armory contribution (Brief 088A):** at least 200 archetype power-system / form / move seeds added to the canonical armory at v1.

## Risks

- **Trademark gravity.** Mitigation: archetype + mechanics naming, creator-namespace signing, fan-work flags, refusal of foundation-namespace claims to trademarked characters (INV-365).
- **Balance ruleset disagreement between communities.** Mitigation: seven rulesets, warnings not refusals, creator override permitted.
- **Power-system explosion.** Mitigation: substrate primitive layer is small (30 archetypes); creator extension is open under creator-namespaces; armory curates the most-reused.
- **Cross-style invariant drift.** Mitigation: invariants are per-move and substrate-enforced; identity embedding (Brief 088 INV-342) is the floor; style adapters are tested against invariant suites.
- **Creator confusion about the IP boundary.** Mitigation: studio surfaces (Brief 079) clearly explain that mechanics are free, names and likenesses are creator-owned and creator-signed, and the substrate's refusal is constitutional.
- **Combat math abuse.** Mitigation: balance proofing flags violations; tournament ruleset rejects unbalanced gseeds at the validator.

## Recommendation

1. **Lock the `power://`, `form://`, `move://`, `henshin://`, `evolution://`, `progression://`, `status://`, `contract://`, `stance://` URL schemes at v1.**
2. **Seed at least 30 power-system archetypes** in the foundation namespace.
3. **Implement the six character interaction operators** as substrate primitives.
4. **Wire the multi-ruleset balance proofer** into the validator.
5. **Add 200 archetype seeds to the armory** (Brief 088A).
6. **Publish the constitutional refusal commitment** (INV-365) in the spec and the studio onboarding.
7. **Engage the cross-style invariant test suite** (Brief 088 §3) with the new move invariants.

## Confidence
**4/5.** The architecture composes cleanly with every Round 4 brief and the constitutional commitments hold. Engineering work is in the validator, the cinematic camera grammar, and the seed curation.

## Spec impact

- `inventory/power-systems.md` — new doc.
- `inventory/forms-and-transformations.md` — new doc.
- `inventory/moves-and-techniques.md` — new doc.
- `inventory/character-interaction-operators.md` — new doc.
- `inventory/evolution-and-progression.md` — new doc.
- `inventory/status-conditions.md` — new doc.
- New ADR: `adr/00NN-power-system-as-substrate-primitive.md`.
- New ADR: `adr/00NN-six-operator-character-interaction-algebra.md`.
- New ADR: `adr/00NN-multi-ruleset-balance-proofing.md`.
- New ADR: `adr/00NN-mechanics-yes-trademark-no-commitment.md`.

## Open follow-ups

- 30-archetype power-system seed list and authoring.
- 200-archetype move/form seed authoring for the armory.
- Cross-style invariant test suite extensions.
- Studio UI for the combo / stance / progression graph editor.
- Cinematic camera grammar for henshin sequences.
- Balance ruleset engine matrix and partner engine onboarding (Godot, Unity, Unreal, Phaser, Spine, Defold).

## Sources

- Internal: Briefs 075, 077, 079, 083, 084, 085, 086B, 086C, 086H, 087, 088, 088A, 089, 091.
