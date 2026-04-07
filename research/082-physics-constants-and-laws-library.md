# 082 — Physics constants and natural laws library

## Question
What physics data — constants, units, equations, laws, models — must GSPL ship at v1 so that any simulation, rendering, or generative output is grounded in real physics with no hand-waved values?

## Why it matters
"Realistic gravity," "the right amount of friction," "how light bends through water," "the orbital period of Mars," "how much energy a punch delivers" — every creative output that purports to depict reality is a physics question. A substrate that ships with hand-waved physics ships fakes. GSPL ships with **CODATA-blessed constants, SI-anchored units, and a library of natural laws encoded as differentiable substrate primitives**.

## What we know from the spec
- Brief 071: differentiable simulation substrate.
- Brief 081: chemistry library (consumes physics).
- Brief 084: particles and fields (consumes physics).
- Brief 086: earth sciences (consumes atmospheric physics).
- Brief 086A: cosmology and astronomy (consumes gravitation, relativity).

## Findings — what GSPL ships at v1

### 1. Fundamental constants — CODATA 2018, all of them
The library ships **every CODATA 2018 recommended value** with full uncertainty bounds:

- **Universal:** speed of light *c*, Planck constant *h*, ℏ, Newtonian *G*, vacuum permittivity ε₀, vacuum permeability μ₀, characteristic impedance Z₀.
- **Electromagnetic:** elementary charge *e*, magnetic flux quantum Φ₀, von Klitzing R_K, Josephson K_J, Bohr magneton μ_B, nuclear magneton μ_N.
- **Atomic and nuclear:** fine-structure constant α, Rydberg R_∞, Bohr radius a₀, Hartree energy E_h, electron mass m_e, proton mass m_p, neutron mass m_n, atomic mass unit u, Avogadro N_A.
- **Physico-chemical:** molar gas R, Boltzmann k_B, Faraday F, Stefan-Boltzmann σ, Wien displacement b.
- **Astronomical (IAU 2015):** astronomical unit, parsec, light year, solar mass, solar radius, solar luminosity, Earth mass, Earth radius, Jupiter mass, Jupiter radius.

Every value carries `(value, uncertainty, exponent, units, citation)` and is exposed in **all common unit systems** (SI, Gaussian, Planck, atomic, natural, imperial where applicable).

**Source:** CODATA 2018 (NIST), IAU 2015 nominal values, NIST SP 811.

### 2. Units and conversions — SI-anchored, total
- **All 7 SI base units** (m, kg, s, A, K, mol, cd).
- **All 22 SI derived units** with named symbols (Hz, N, Pa, J, W, C, V, F, Ω, S, Wb, T, H, °C, lm, lx, Bq, Gy, Sv, kat, rad, sr).
- **All SI prefixes** including the 2022 additions (quetta, ronna, ronto, quecto).
- **All common non-SI units accepted for use with SI:** minute, hour, day, degree, arcminute, arcsecond, hectare, litre, tonne, dalton, electronvolt, astronomical unit.
- **Imperial, US Customary, CGS, Planck, atomic, natural systems** with full conversion matrices.
- **Specialized units:** parsec, light year, solar mass, jansky, barn, fermi, ångström, calorie, BTU, horsepower, knot, fathom, mmHg, torr, bar, atmosphere.
- **Non-physical units used in creative work:** pica, em, point, dpi/ppi, frame, semitone, octave, hertz-equivalent for music, decibel (with reference variants).

The unit system is **dimensionally checked at substrate level**: every parameter on every gseed declares its dimensional class (length, time, energy, etc.), and the substrate refuses to compose dimensionally inconsistent inputs unless the user explicitly bridges them.

**Source:** SI Brochure 9th Edition (BIPM), NIST SP 811, IAU 2015.

### 3. Mechanics — laws and models
- **Newtonian mechanics:** Newton's three laws, gravitation, work-energy theorem, momentum and impulse, angular momentum, center of mass, moment of inertia tensors for canonical shapes (sphere, cylinder, box, ring, cone, ellipsoid).
- **Lagrangian and Hamiltonian mechanics:** generalized coordinates, Euler-Lagrange equations, canonical transformations, Poisson brackets — all encoded as substrate-callable forms for arbitrary parameterized systems.
- **Continuum mechanics:** stress and strain tensors, Cauchy-Green deformation, Hooke's law (linear and nonlinear), Navier-Cauchy equations.
- **Fluid mechanics:** Navier-Stokes (compressible and incompressible), Bernoulli, Reynolds number, drag coefficients for canonical shapes, boundary layer theory, turbulence parameters (k-ε, k-ω, LES Smagorinsky).
- **Rigid body dynamics:** Euler equations, gyroscopic precession, contact and friction (Coulomb, Stribeck).

### 4. Thermodynamics
- **Laws:** zeroth through third.
- **Equations of state:** ideal gas, van der Waals, Redlich-Kwong, Peng-Robinson, NIST REFPROP-equivalent for major fluids.
- **Heat transfer:** Fourier conduction, Newton's law of cooling, Stefan-Boltzmann radiation, Wien displacement, view factors for canonical geometries.
- **Phase transitions:** Clausius-Clapeyron, latent heats for common substances.
- **Statistical mechanics:** Boltzmann distribution, Maxwell-Boltzmann velocities, Fermi-Dirac, Bose-Einstein.

### 5. Electromagnetism
- **Maxwell's equations** in differential and integral form, vacuum and material.
- **Coulomb, Gauss, Ampère, Faraday laws.**
- **Lorentz force.**
- **Wave equation, plane waves, polarization.**
- **Reflection, refraction (Snell), Fresnel equations** for unpolarized and polarized light at any angle and any IOR pair.
- **Dispersion** (Sellmeier equation with coefficients for 200+ optical materials from RefractiveIndex.info).
- **Diffraction** (Fraunhofer, Fresnel, slits, gratings, apertures).
- **Black body radiation** (Planck's law, Wien, Stefan-Boltzmann), color temperature mapping.
- **Antenna and cavity modes** for visualization purposes.

### 6. Optics — full PBR-grade
- **Microfacet BRDFs:** GGX, Beckmann, Blinn-Phong, with proper Fresnel and shadowing-masking (Smith).
- **BSDF:** transmission, refraction, multiple-scattering compensation.
- **Subsurface scattering:** dipole, quantized diffusion, BSSRDF with measured human skin parameters.
- **Volumetric scattering:** Henyey-Greenstein, Mie, Rayleigh, Schlick approximations.
- **Polarization:** Stokes vectors, Mueller matrices for wave-tracing renderers.
- **Caustics, dispersion, fluorescence, phosphorescence** as first-class effects.
- **Iridescence:** thin-film interference with measured film stack data.
- **HDR and spectral rendering:** the renderer can operate in spectral mode (8–32 wavelength bins) for color-accurate physics.

**Source:** Physically Based Rendering 4ed (Pharr/Jakob/Humphreys), Disney BRDF, Mitsuba 3, RefractiveIndex.info.

### 7. Quantum, relativity, particle physics — for accurate depiction
GSPL ships these so users can render scientific visualizations correctly even if they don't fully use them at runtime:

- **Quantum mechanics:** Schrödinger equation, hydrogen atom solutions, harmonic oscillator, particle in a box, tunneling, spin algebra, Stern-Gerlach.
- **Special relativity:** Lorentz transformations, time dilation, length contraction, relativistic momentum and energy, Doppler shift, aberration of light. Used for relativistic visualization (e.g., near-light-speed travel scenes).
- **General relativity:** Schwarzschild metric, geodesic equations, gravitational lensing renders (used for accurate black hole visualizations à la *Interstellar*'s Gargantua).
- **Standard Model basics:** particle list (12 fermions, 4 gauge bosons, Higgs), masses, charges, lifetimes, principal decay modes. Used for accurate cloud-chamber and detector visualizations.

**Source:** PDG (Particle Data Group), Wikipedia particle physics references, Penrose/Wald GR texts (free CC versions where available).

### 8. Acoustics
- **Wave equation, speed of sound** in air/water/solids as functions of temperature.
- **Reflection, refraction, diffraction, interference** of sound.
- **Doppler effect.**
- **Room acoustics:** Sabine equation, reverberation time, absorption coefficients for common materials.
- **Psychoacoustics:** equal-loudness contours, Bark scale, mel scale, masking curves.
- **Musical acoustics:** instrument resonance models for major instrument families.

**Source:** Beranek *Acoustics*, IRCAM, peer-reviewed acoustics literature, AES standards.

## Findings — how this is structured as gseeds

```
phys://constant/c@v1.0          → speed of light with CODATA uncertainty
phys://constant/G@v1.0          → Newtonian gravitational constant
phys://unit/SI/joule@v1.0       → joule with full conversion matrix
phys://law/Maxwell/all@v1.0     → Maxwell's equations as differentiable form
phys://model/NavierStokes@v1.0  → NS equations
phys://brdf/GGX@v1.0            → GGX microfacet BRDF
phys://model/black-body@v1.0    → Planck radiation law
phys://particle/electron@v1.0
phys://eos/peng-robinson@v1.0
```

Every law, model, and BRDF is encoded as a **callable, differentiable substrate primitive** (the substrate guarantees autograd through it via Brief 071's differentiable substrate). This means a renderer can call `phys://brdf/GGX` directly and propagate gradients during inverse rendering or critic-driven optimization.

## Findings — how engines consume physics

- **Renderers** call physics directly for BRDFs, BSDFs, atmospheric scattering, refraction, dispersion.
- **Simulation engines** call physics for forces, fluid dynamics, heat, EM.
- **Critic ensemble** uses physics validity as one of its scoring axes.
- **Image generators** receive physics-as-conditioning ("water" comes with refractive index 1.333, surface tension 0.072 N/m, density 1000 kg/m³, IR absorption spectrum, etc., not just the word).

Physics is **the substrate's grounding to objective reality**. Every photorealistic claim downstream depends on it.

## Inventions

### INV-312: Substrate-native physics as differentiable callable forms
Every physical law and model in the library is encoded as a differentiable substrate primitive that any engine can call with full autograd support. Engines do not reimplement physics; they consume the substrate's. Novel because no creative tool ships physics as differentiable substrate-callable forms with formal dimensional checking.

### INV-313: Dimensional substrate checking
Every parameter on every gseed declares its dimensional class. The substrate refuses to compose dimensionally inconsistent inputs without an explicit user bridge. This catches an entire class of "fake numbers" errors that pollute every other creative tool. Novel as a substrate-level dimensional safety contract.

### INV-314: Physics-as-conditioning for generative models
Generative engines (image, video, 3D) receive physics context as part of conditioning. Words that map to physical entities are auto-augmented with their physical properties before reaching the engine, biasing output toward physical correctness. Novel as a substrate-mediated physics grounding for generative models.

## Phase 1 deliverables

- **All CODATA 2018 constants** signed at v1.
- **Complete SI unit system + all major non-SI systems** with conversion matrices and dimensional checking.
- **Mechanics, thermodynamics, electromagnetism, optics, acoustics** as differentiable callable forms.
- **PBR-grade BRDF library** (GGX, Beckmann, Disney, etc.) at v1.
- **Spectral rendering support** with 8–32 wavelength bin operation.
- **Physics-as-conditioning protocol** wired into the image engine at v1.
- **Quantum, relativity, Standard Model basics** for scientific visualization use cases.

## Risks

- **Library size and complexity.** Mitigation: modular packaging — users load mechanics/EM/optics by default; QM/GR loaded on demand.
- **Differentiability edge cases.** Some classical physics has discontinuities (contact, phase transitions). Mitigation: smooth approximations available; exact forms also available; user picks.
- **Dimensional checking false positives.** Mitigation: bridges are explicit but easy.

## Recommendation

1. **Lock the v1 physics library** to CODATA 2018, SI 9th, IAU 2015.
2. **Sign the entire library** under the GSPL Foundation Identity.
3. **Wire physics-as-conditioning** into the v1 image engine.
4. **Implement dimensional substrate checking** as a v1 contract.
5. **Engage Mitsuba 3, PBRT, RefractiveIndex.info** authors as upstream advisors.

## Confidence
**5/5.** Sources are open, authoritative, and stable. Engineering effort is curation and packaging.

## Spec impact

- `inventory/physics.md` — new doc.
- `inventory/units.md` — new doc with dimensional schema.
- Update Brief 071, 084, 086, 086A to consume.
- New ADR: `adr/00NN-physics-as-substrate-primitive.md`.
- New ADR: `adr/00NN-dimensional-substrate-checking.md`.

## Open follow-ups

- Implementation of dimensional checker.
- Spectral rendering integration with the image engine.
- BRDF library packaging.

## Sources

- CODATA 2018 (NIST).
- NIST SP 811 (units guide).
- SI Brochure 9th Edition (BIPM).
- IAU 2015 nominal values.
- *Physically Based Rendering 4ed* (Pharr, Jakob, Humphreys).
- Mitsuba 3 documentation.
- RefractiveIndex.info database.
- Particle Data Group (PDG).
- Beranek *Acoustics*.
- HITRAN spectroscopic database.
- IRCAM acoustic research.
- Internal: Briefs 071, 081, 084, 086, 086A.
