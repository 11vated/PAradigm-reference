# 084 — Particles, fields, and effects library

## Question
What particle systems, force fields, fluid models, and effect primitives must GSPL ship at v1 so that fire, smoke, water, dust, sparks, magnetism, gravity, electric arcs, plasma, and every other dynamic phenomenon can be composed at substrate level with real physics — not faked with sprites?

## Why it matters
Every visually impressive moment in cinema and games — explosions, magic effects, water, weather, atmospheric haze, character abilities — is built on particle systems and field interactions. Houdini's particle and Pyro tools dominate VFX because they couple solvers correctly. GSPL must ship a particle and field substrate that consumes the physics (Brief 082) and chemistry (Brief 081) libraries directly, runs on the differentiable substrate (Brief 071), and is composable across engines.

## What we know from the spec
- Brief 071: differentiable simulation substrate.
- Brief 081, 082, 083: chemistry, physics, materials.
- Brief 086: earth sciences (atmosphere, weather).

## Findings — what GSPL ships at v1

### 1. Particle classes (substrate primitives)
- **Point particles** (mass, position, velocity, lifetime, color) — universal foundation.
- **Rigid particles** (full 6-DOF, oriented).
- **Sprite particles** (textured planes for billboard effects).
- **Mesh particles** (instanced geometry).
- **Fluid particles** (SPH or PIC/FLIP).
- **Smoke/gas particles** (continuum field on grid).
- **Plasma particles** (charged, EM-coupled).
- **Strand/hair particles** (linked, with bending stiffness).
- **Cloth particles** (mesh with constraints).

Each particle class is a signed substrate primitive with a defined update kernel.

### 2. Force fields
- **Constant gravity** (vector).
- **Point gravity** (1/r²).
- **Inverse-square attraction/repulsion.**
- **Linear drag, quadratic drag.**
- **Wind fields** (uniform, turbulent, Perlin-modulated).
- **Vortex fields** (with definable axis and strength).
- **Curl noise fields** (for natural turbulence).
- **Magnetic and electric fields** (full Lorentz force coupling).
- **Spring forces** (for constraints).
- **Custom fields** defined by user-supplied differentiable function.

All fields are **composable**: a particle can be subject to multiple fields whose forces sum.

### 3. Fluid solvers
- **SPH** (Smoothed-Particle Hydrodynamics) for water and incompressible liquids.
- **PIC/FLIP** for stable, controllable fluid sims.
- **MPM** (Material Point Method) for snow, sand, mud, soft solids.
- **Eulerian grid** for smoke, fire, gases, fog.
- **Position-Based Dynamics** for fast, stable real-time fluid.
- **Lattice Boltzmann** for high-Reynolds gas flow.

All solvers run on the differentiable substrate so gradients flow through the simulation for inverse problems and critic-driven optimization.

**Source:** Genesis, DiffTaichi, PhiFlow, Brax, Warp, Nvidia FleX (open subset), HOUDINI documentation for solver concepts.

### 4. Combustion and pyrotechnics — chemistry-grounded
The library ships pre-built combustion primitives that consume chemistry (Brief 081):

- **Methane, propane, butane combustion** (gas stove, lighter, blowtorch).
- **Hydrocarbon combustion** (candle wax, paraffin, oil).
- **Wood combustion** (cellulose pyrolysis + char).
- **Black powder, smokeless powder** (explosions).
- **Magnesium ignition** (white-hot flare).
- **Sodium and potassium combustion** (in air, in water).
- **Thermite** (iron oxide + aluminum reduction).
- **Fireworks colorants** (strontium → red, barium → green, copper → blue, sodium → yellow, magnesium → white).

Each combustion primitive consumes the real reaction kinetics (Arrhenius rates), the real heat of combustion (ΔH), the real product gases, and the real emission spectra. A fire **looks right** because it is doing the right physics, not because an artist tuned a sprite sheet.

**Source:** NIST Combustion Database, NFPA standards, peer-reviewed combustion literature.

### 5. Atmospheric and weather effects
- **Rain** (droplet size distributions from NOAA, terminal velocity model).
- **Snow** (crystal habits from atmospheric temperature and humidity).
- **Hail** (size distribution + density).
- **Fog and mist** (Mie scattering parameters by droplet size).
- **Lightning** (Dielectric Breakdown Model + L-system bolt structure).
- **Clouds** (volumetric noise + Mie scattering).
- **Tornado, hurricane, dust storm** (large-scale vorticity templates).
- **Aurora** (charged particle excitation in upper atmosphere).
- **Sandstorm, ash fall, volcanic plume.**

**Source:** NOAA, NASA atmospheric models, peer-reviewed atmospheric physics.

### 6. Magic and stylized effect primitives — for creative range
GSPL ships physics-grounded **but stylized** effect primitives so creators making fantasy and game work have ready-made high-quality starting points:

- **Magic flame** (combustion with shifted color spectrum).
- **Fairy dust** (metallic particles with bloom).
- **Slash trails** (motion-blurred ribbons with falloff).
- **Lightning magic** (DBM with stylized branching).
- **Ice formation** (anisotropic crystal growth via reaction-diffusion).
- **Healing aura** (volumetric scattering with perceptual color cycling).
- **Portal swirl** (vortex field on a textured disk).

Each is built on real physics primitives so it can be physically tuned, but with art-directable defaults.

### 7. Differentiability and reproducibility
- Every particle solver runs on the differentiable substrate (Brief 071).
- Every solver is **deterministic** given the same seed and parameters (Brief 026 contract).
- Every particle simulation is **lineage-cached** (INV-200) — re-runs with unchanged parameters skip computation.
- Every solver runs at **all four execution tiers** (T0 CPU, T1 iGPU, T2 dGPU, T3 federated).

## Findings — composition

A particle effect in GSPL is built by composing primitives:

```
fx://fire/campfire@v1
  particles:
    smoke: smoke_grid(combustion=wood_pyrolysis)
    flame: emission_field(spectra=ch4_combustion)
    sparks: rigid_particles(forces=[gravity, wind, drag])
    heat: heat_field(coupling=convection)
  composition: layered
  signed_by: gspl_foundation
```

The composition is a gseed. Users fork it, breed it with other effects, tune any parameter directly on the canvas, and the lineage records every change.

## Inventions

### INV-318: Composable substrate-native particle and field primitives
Particle classes, force fields, and solvers are signed substrate primitives that compose like Lego. A user assembles complex effects by composing primitives without writing code. Every primitive consumes real physics and chemistry data; every composition is lineage-tracked. Novel because no creative tool ships particles and fields as composable substrate primitives with cross-domain physical coherence.

### INV-319: Chemistry-grounded combustion library
Pre-built combustion primitives (candle, wood fire, methane, magnesium, fireworks colorants) consume real reaction kinetics and emission spectra from the chemistry library. Fires look right because they are right. Novel as a substrate-level pre-built combustion library grounded in measured chemistry.

## Phase 1 deliverables

- **9 particle classes** as signed primitives at v1.
- **10 force field types** at v1.
- **6 fluid solvers** (SPH, PIC/FLIP, MPM, Eulerian grid, PBD, LBM) at v1.
- **20 chemistry-grounded combustion primitives** at v1.
- **15 weather and atmospheric effects** at v1.
- **30 stylized effect templates** at v1.
- **Differentiable, deterministic, tier-routable** for every solver.

## Risks

- **Solver complexity for solo founder.** Mitigation: integrate Genesis, PhiFlow, Brax, Warp as substrate-wrapped engines rather than reimplementing.
- **Real-time performance on T1 hardware.** Mitigation: each solver ships with a coarse real-time mode and a high-quality offline mode.

## Recommendation

1. **Wrap Genesis, PhiFlow, Brax, Warp** as v1 solver engines under the substrate.
2. **Build the composition schema** as a v1 contract.
3. **Ship 20 combustion primitives** grounded in real chemistry at v1.
4. **Ship 30 stylized effects** for immediate creative use at v1.
5. **Engage Genesis, PhiFlow, Brax authors** as upstream collaborators.

## Confidence
**4/5.** The solver ecosystem is mature; the substrate wrapping work is engineering, not research.

## Spec impact

- `inventory/particles.md` — new doc.
- `inventory/effects-library.md` — new doc.
- Update Brief 071 to declare particle solvers as substrate-wrapped engines.
- New ADR: `adr/00NN-composable-particle-substrate.md`.

## Open follow-ups

- Solver license compatibility audit.
- Real-time performance benchmarks per solver per tier.
- Stylized effect template curation.

## Sources

- Genesis, DiffTaichi, PhiFlow, Brax, Warp, FleX documentation.
- *Fluid Simulation for Computer Graphics* (Bridson).
- NIST Combustion Database.
- NOAA atmospheric science publications.
- Müller et al. SPH papers.
- Position-Based Dynamics literature.
- Lattice Boltzmann references.
- Internal: Briefs 026, 071, 081, 082, 083, 086, 200.
