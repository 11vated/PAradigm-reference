# 083 — Materials library (PBR, optical, acoustic, mechanical, thermal)

## Question
What measured-data material library must GSPL ship at v1 so that any rendered surface, simulated body, or generated material is grounded in real-world measurements rather than artist guesses?

## Why it matters
"Brushed aluminum," "wet asphalt at night," "human skin under candlelight," "raw silk," "old leather," "polished marble," "ceramic glaze" — every material a creator invokes is a measurable physical thing. Houdini and Unreal ship with libraries of artist-tuned materials that *look* right; GSPL ships with libraries of measured materials that *are* right, with optical, acoustic, mechanical, and thermal properties all bound to the same gseed so a single material drives lighting, sound, simulation, and heat behavior consistently.

## What we know from the spec
- Brief 071: differentiable simulation.
- Brief 072: neural rendering.
- Brief 081: chemistry library.
- Brief 082: physics library.
- Brief 084: particles and fields.

## Findings — what GSPL ships at v1

### 1. PBR optical material library
**1,000+ measured materials** at v1 with full PBR data:

- **Metals (200):** iron, steel (multiple grades), aluminum, copper, brass, bronze, gold, silver, platinum, titanium, nickel, zinc, lead, tin, chrome, stainless steel variants, anodized aluminum, oxidized variants. Each carries complex IOR (n + ik) at sampled wavelengths from 380–780 nm, anisotropy parameters where applicable, surface roughness distributions from real samples.
- **Dielectrics (300):** glass (crown, flint, BK7, fused silica, lead crystal, soda-lime), water, ice, oils, plastics (PE, PP, PS, PVC, PET, PMMA, PC, ABS, nylon variants), ceramics, gemstones (diamond, ruby, sapphire, emerald, opal, amethyst, topaz, garnet), salt crystals, sugars.
- **Organic (200):** human skin (Type I–VI Fitzpatrick), animal hides, hair, fur (mouse, cat, dog, bear, sheep, alpaca), feathers, leaves, bark, petals, fruit skins, vegetable surfaces, meat, fat, blood, bone, shell, ivory, tortoise shell, pearl.
- **Fabrics (100):** cotton, linen, silk, wool, polyester, nylon, leather (multiple finishes), suede, velvet, denim, lace, chiffon, satin, corduroy, tweed.
- **Building materials (100):** concrete (multiple finishes), brick, stone (granite, marble, sandstone, slate, limestone, basalt), wood (50 species with grain), drywall, stucco, asphalt (dry and wet), tile, terrazzo.
- **Industrial and synthetic (100):** carbon fiber, fiberglass, kevlar, rubber, foam, plastics, composites, painted surfaces (matte, satin, gloss, automotive, military).

**Source:** **MERL BRDF database** (100 measured isotropic materials at full hemisphere), **RGL EPFL BRDF database** (anisotropic measurements), **Disney's BRDF Explorer dataset**, **Unity HDRP measured library**, **Adobe Substance Source measured assets** (where openly licensed), **SkinFaceMatte database**, **NIST measured optical materials**, **RefractiveIndex.info** for IOR curves, **Khronos glTF sample materials**.

### 2. Acoustic material properties
For every PBR material, the library also carries acoustic data:

- **Acoustic impedance** (ρc).
- **Absorption coefficient** at standard octave bands (125, 250, 500, 1k, 2k, 4k Hz).
- **Diffusion coefficient.**
- **NRC (Noise Reduction Coefficient).**
- **Reverberation contribution** in the Sabine model.
- **Surface texture-to-scattering mapping** for specular vs diffuse audio reflection.

This allows the same material gseed to drive both visual rendering and audio simulation. A wood floor reflects light at GGX(α=0.2) and reflects sound at NRC=0.10 simultaneously.

**Source:** Acoustic Society of America measurements, ASTM C423, IBANE measurements, FreeFieldTechnologies, Building Materials Acoustic Database (Concordia), peer-reviewed acoustics literature.

### 3. Mechanical properties
Every material carries mechanical data for simulation:

- **Density** (kg/m³).
- **Young's modulus** (Pa).
- **Poisson's ratio.**
- **Shear modulus.**
- **Bulk modulus.**
- **Yield strength.**
- **Ultimate tensile strength.**
- **Hardness** (Mohs and Vickers).
- **Coefficient of friction** (static and kinetic, dry and wet) against canonical reference surfaces.
- **Elasticity vs plasticity model** parameters (linear, hyperelastic, plastic).
- **Fracture toughness** (K_IC) where measured.

This drives the differentiable simulation engines (Brief 071) — when a user breaks glass, the substrate uses real glass fracture parameters, not a faked particle effect.

**Source:** **MatWeb**, **NIST Materials Database**, **CES EduPack** (open subset where licensed), **ASM Handbook Online** (where openly licensed), **CRC Handbook**, peer-reviewed materials science literature.

### 4. Thermal properties
- **Thermal conductivity** (W/m·K).
- **Specific heat capacity** (J/kg·K).
- **Thermal expansion coefficient** (1/K).
- **Melting point, boiling point** (where applicable).
- **Latent heat of fusion and vaporization.**
- **Emissivity** (for IR rendering and heat-transfer simulation).
- **Glass transition temperature** (for polymers).

### 5. Aging and weathering models
A material is not only what it is when new. The library also includes **aging and weathering parameter curves** so a material can be rendered at any "age":

- **Metal oxidation rates** (e.g., copper → patina over years).
- **Wood weathering** (UV bleaching, grain raising, splitting).
- **Stone erosion** (rate per cm/century by stone type and climate).
- **Fabric fading** (lightfastness curves from textile literature).
- **Paint chalking and color shift.**
- **Organic decay rates.**

Users invoke a material with an "age" parameter and the substrate produces the correctly weathered version.

**Source:** Conservation literature, ICOMOS, AATCC textile fading standards, ASTM weathering standards.

### 6. Skin material — first-class
Human skin is shipped as a **dedicated, first-class material primitive** with the depth competitors lack:

- **Multi-layer BSSRDF** (epidermis, dermis, subcutaneous) with measured per-Fitzpatrick-type parameters.
- **Melanin and hemoglobin maps** as composable texture inputs.
- **Sweat and oil layer** as a separable optical layer.
- **Wrinkle and pore microgeometry** at multiple scales.
- **Aging parameter** that drives all of the above.
- **Lighting reference** under common illuminants (D65, D50, candle, sodium, fluorescent, LED).

This is the foundation for the photoreal human work (Brief 073).

**Source:** Penner *PracticalSubsurfaceScatteringForRealtime*, ICT Light Stage measurements, Donner *Light Diffusion in Multi-Layered Translucent Materials*, RealSkin and other open SSS datasets.

## Findings — material gseed structure

```
mat://metal/copper/polished@v1.0
  optical: { ior_re: [...], ior_im: [...], roughness: 0.05, anisotropy: 0 }
  acoustic: { impedance: 4.4e7, absorption: {125:0.01, ..., 4k:0.05}, ... }
  mechanical: { density: 8960, young: 110e9, poisson: 0.34, ... }
  thermal: { k: 401, cp: 385, alpha: 16.5e-6, emissivity: 0.04, ... }
  aging_curve: copper://patina@v1
  signed_by: gspl_foundation
  source: "NIST + RefractiveIndex.info + MatWeb"
```

A single material gseed serves rendering, audio, simulation, and thermal — coherently. Engines reference materials by gseed ID and the substrate guarantees consistency.

## Findings — neural materials

For materials too complex to measure directly (e.g., specific designer fabrics, weathered urban surfaces), GSPL ships **neural BRDF gseeds** trained on photographic captures. Each neural material is a small MLP with declared training provenance and a fallback measured-material approximation if the user wants to leave the neural runtime.

**Source:** Sztrajman et al. *Neural BRDF Representation*, NeuMIP, NeRF-related neural material work.

## Inventions

### INV-315: Coherent multi-domain material gseeds
A material gseed binds optical, acoustic, mechanical, and thermal properties to a single signed identity. Engines querying the same material for any domain receive consistent data. Novel because no creative tool ships materials as cross-domain coherent objects — Houdini's optical materials and audio reflection coefficients live in unrelated systems with no shared identity.

### INV-316: Substrate aging and weathering parameter
Every material gseed accepts an "age" parameter that drives a measured aging model (oxidation, fading, weathering, decay). Materials render at any historical state from new to ancient. Novel as a substrate-level temporal-state parameter for materials.

### INV-317: First-class skin primitive
Human skin is shipped as a dedicated material primitive with multi-layer BSSRDF, melanin/hemoglobin composability, aging curves, and per-Fitzpatrick-type measured data. Novel because no creative tool treats skin as a substrate primitive with the depth required for ethical photoreal humans (Brief 073).

## Phase 1 deliverables

- **1,000 PBR materials** with optical + acoustic + mechanical + thermal data signed at v1.
- **Skin primitive** with all 6 Fitzpatrick types at v1.
- **Aging curves** for the top 100 most-used materials at v1.
- **Material gseed schema** with cross-domain coherence at v1.
- **Neural material runtime** for 50 high-fidelity captured materials at v1.

## Risks

- **Acoustic data sparsity for many visual materials.** Mitigation: ship measured data where available; computed estimates from impedance otherwise; explicit confidence flag.
- **Measured data licensing.** Some commercial libraries are restricted. Mitigation: ship open-licensed only; build a community contribution pipeline for measured submissions.
- **Library size.** 1000 materials with full multi-domain data ≈ 500 MB. Mitigation: lazy load from federation knowledge graph.

## Recommendation

1. **Lock v1 to 1000 materials** with all four domains.
2. **Sign all materials** under GSPL Foundation Identity.
3. **Build the multi-domain coherence schema** as a substrate contract.
4. **Ship the skin primitive** with full Fitzpatrick coverage at v1 — non-negotiable for photoreal humans.
5. **Engage MERL, EPFL RGL, NIST, MatWeb** as upstream data partners.
6. **Build community contribution pipeline** for measured material submissions with provenance.

## Confidence
**5/5.** Sources are open, measured, and stable. Engineering effort is curation and schema design.

## Spec impact

- `inventory/materials.md` — new doc.
- `inventory/materials-schema.md` — new doc.
- Update Briefs 071, 072, 073, 082, 084.
- New ADR: `adr/00NN-multi-domain-material-coherence.md`.

## Open follow-ups

- Curation of v1 material list.
- Acoustic measurement gap-filling protocol.
- Neural material training pipeline.

## Sources

- MERL BRDF database (Mitsubishi Electric Research Labs).
- RGL EPFL BRDF database.
- Disney BRDF Explorer dataset.
- Khronos glTF Sample Materials.
- RefractiveIndex.info.
- NIST Materials Database.
- MatWeb.
- ASM Handbook Online.
- CRC Handbook of Chemistry and Physics.
- ASTM C423 acoustic absorption standard.
- AATCC textile fading standards.
- ICOMOS conservation literature.
- ICT Light Stage research.
- Penner, Donner subsurface scattering papers.
- Sztrajman et al. *Neural BRDF Representation*.
- Internal: Briefs 071, 072, 073, 081, 082, 084.
