# 025 — Simulation family: Physics + Ecosystem + ALife engines

## Question
What are the seed schemas, kernel pipelines, and proof models for the three simulation engines: PhysicsEngine (rigid/soft body dynamics), EcosystemEngine (multi-agent biome simulations), and ALifeEngine (artificial life and emergent evolution)?

## Why it matters
Simulations are GSPL's claim to *open-ended* generation. Static images are dead artifacts; a simulation is a generator that keeps producing novelty after the seed is fixed. This is the engine family that lets a single seed produce hours of distinct content. Spore is the closest reference point and the spiritual ancestor of these three engines.

## What we know from the spec
- `engines/physics.md`, `engines/ecosystem.md`, `engines/alife.md` exist as stubs.
- The 17 + 5 gene types include SwarmGene, BehaviorGene, RuleGene, DistributionGene — the simulation primitives.

## Findings — schemas

### PhysicsEngine

Produces parameterized physics simulations: rigid bodies, soft bodies, fluids, cloth, ropes, particle systems, joint chains.

**Genes (typical 25-50):**
- `world.dim` (CategoricalGene: 2D, 3D)
- `world.gravity` (VectorGene<2 or 3>)
- `world.bounds` (VectorGene)
- `solver.method` (CategoricalGene: pbd, xpbd, impulse, sequential_impulse, semi-implicit-euler)
- `solver.iterations` (IntGene)
- `solver.timestep` (ScalarGene)
- `bodies.spawn` (SwarmGene over body archetypes)
- `bodies.shapes` (CategoricalGene per archetype: box, sphere, capsule, polygon, mesh, sdf)
- `bodies.material` (MaterialGene with extra fields: density, friction, restitution, drag)
- `joints.graph` (GraphGene of joint constraints)
- `forces.fields` (SequenceGene of force-field descriptions: gravity wells, vortices, drag zones)
- `damping.envelope` (EnvelopeGene over time)
- Plus the 8 Core genes.

**IR**: a typed world description + body table + constraint graph + force-field list. Proof-bearing. The actual simulation is a pure function of (IR, rng_seed, duration).

### EcosystemEngine

Produces *biomes*: spatially distributed populations of interacting species with environmental conditions, food webs, and population dynamics.

**Genes (typical 30-60):**
- `biome.archetype` (CategoricalGene: forest, desert, reef, tundra, swamp, alien, custom)
- `biome.spatial_layout` (GridGene of zone tags or a continuous DistributionGene)
- `climate.params` (DistributionGene)
- `climate.seasonality` (EnvelopeGene over a year cycle)
- `species.list` (SwarmGene over species archetypes)
- `species.metabolism` (per-species RuleGene)
- `species.reproduction` (per-species RuleGene)
- `food_web.edges` (GraphGene of predator-prey-resource edges with weights)
- `disturbance.events` (SequenceGene of fire/flood/drought triggers with frequencies)
- `population.initial` (per-species DistributionGene)
- Plus the 8 Core genes.

**IR**: a typed ecosystem description + species table + food web + climate envelope. Proof-bearing.

### ALifeEngine

Produces *evolving populations* that change over the course of a simulation. The distinction from EcosystemEngine is that ALifeEngine treats individuals as having *evolvable genomes* — agents inherit, mutate, and select within the simulation itself.

**Genes (typical 20-40, generative):**
- `world.geometry` (CategoricalGene: 2D_grid, 2D_continuous, 3D_continuous)
- `world.params` (DistributionGene)
- `genome.template` (a small typed schema for what each individual's genome contains — a sub-seed schema)
- `selection.pressure` (RuleGene)
- `mutation.rate_envelope` (EnvelopeGene over generations)
- `crossover.rate` (ScalarGene)
- `population.cap` (IntGene)
- `niches.count` (IntGene)
- `evaluation.fitness_fn` (RuleGene)
- `seed.population` (SwarmGene of starting genomes)
- Plus the 8 Core genes.

**IR**: a typed ALife world description + population template + selection rules. Proof-bearing.

## Cross-engine bindings

- `Ecosystem ⊃ Physics`: ecosystems with physical agents (predator-prey chase) consume a PhysicsEngine seed for the underlying body dynamics.
- `ALife ⊃ Physics`: ALife worlds with embodied agents likewise.
- `Ecosystem ⊃ ALife`: an ecosystem may host an ALife population as a sub-system, letting some species evolve while others are fixed.
- `FullGame ⊃ Physics, Ecosystem, ALife`: any simulation engine can power a region of a full game.
- All three bind to Core for cross-domain composition.

## Pipeline

Each simulation engine has a four-stage pipeline:

1. **Seed → IR** (deterministic)
2. **IR → Initial state** (deterministic)
3. **Initial state → Trajectory** (deterministic given fixed solver, rng_seed)
4. **Trajectory → Output** (visualization, metric extraction, export)

Proof lives on stages 1-3. Stage 4 is the perceptual/runtime stage.

**Determinism in simulation:**
- All three engines must support a *deterministic mode* where step-by-step state is reproducible bit-for-bit on the proof-bearing kernel (Brief 001's fixed-point integer kernel).
- A *non-deterministic mode* runs faster on GPU and is allowed for interactive use; outputs from this mode are flagged in metadata.
- Brief 001's Q16.16 integer kernel is the proof substrate for all simulation math.

## Risks identified

- **Open-ended drift**: long simulations diverge between implementations even with fixed-point math due to integer overflow management. Mitigation: explicit overflow handling (saturating arithmetic) and a documented step budget.
- **Ecosystem balance**: tuning the food web so populations don't crash is hard. Mitigation: critics and self-stabilizing dynamics in the rule library; not a v1 perfect-balance promise.
- **ALife state explosion**: an evolving population's state grows. Mitigation: state checkpointing every N steps with hash chains so a verifier can spot-check rather than full-replay.
- **Physics solver portability**: the same XPBD solver in two libraries does not match bit-for-bit. Mitigation: GSPL ships *one* reference solver per engine, and that solver is the only proof-bearing implementation. Other solvers can be used in non-deterministic mode.

## Recommendation

1. **Adopt the three-engine schemas as drafted.**
2. **All three engines have a deterministic mode running on Brief 001's fixed-point kernel** for proof-bearing replay.
3. **Each engine ships exactly one reference solver** (PBD/XPBD for Physics, discrete-time agent step for Ecosystem, discrete-time ALife step). Other solvers are non-proof.
4. **State checkpointing** every N steps with hash chains is mandatory for ALife and Ecosystem.
5. **Step budgets are part of the seed**, not an external runtime parameter. Prevents "infinite simulation" abuse.
6. **Saturating arithmetic** for fixed-point overflow handling, documented in the kernel spec.

## Confidence
**3/5.** Physics is 4/5 (XPBD is well-understood). Ecosystem is 3/5 (food web stability is hard). ALife is 2/5 (open-ended evolution is a research problem). Average 3/5.

## Spec impact

- `engines/physics.md`, `engines/ecosystem.md`, `engines/alife.md` — full schemas.
- `algorithms/reference-solvers.md` — the three reference solvers.
- `algorithms/state-checkpointing.md` — hash-chain checkpoint protocol.
- `tests/simulation-conformance.md` — bit-for-bit replay tests.
- New ADR: `adr/00NN-deterministic-simulation-mode.md`.

## Open follow-ups

- Build the reference XPBD solver in Rust against the fixed-point kernel. Phase 1.
- Decide on the ALife genome template format (probably itself a UniversalSeed schema with restricted gene types).
- Investigate whether the existing 182K-LOC codebase has reusable physics or ecosystem code.
- Define the step-budget table per engine.

## Sources

- Macklin et al., *XPBD: Position-Based Simulation of Compliant Constrained Dynamics*.
- Yaeger, *PolyWorld* (early ALife reference).
- Ackley, *The Tierra Approach*.
- Internal: Brief 001 (fixed-point kernel), Brief 020 (Swarm/Rule gene types).
