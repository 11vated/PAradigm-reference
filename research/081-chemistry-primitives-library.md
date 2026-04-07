# 081 — Chemistry primitives library

## Question
What chemistry data must GSPL ship with at v1 so that any user or agent can compose chemically-accurate gseeds — molecules, reactions, materials, biochemistry, photochemistry — without ever writing fake data?

## Why it matters
A user asks GSPL to render "rust forming on iron in salt water," "a candle flame," "champagne bubbles," "blood oxygenating in a lung," "a sodium-potassium pump in a neuron." Every one of these is a chemistry problem. If the substrate ships with a hand-waved "fire material," every result is a fake. If it ships with real combustion thermodynamics, real iron oxidation kinetics, real CO₂ solubility data — the result is **mathematically correct reality**, and the user can compose chemistry into any visual without leaving the substrate.

## What we know from the spec
- Brief 084: particles and fields (consumes chemistry data).
- Brief 083: materials library (uses chemistry for optical and mechanical).
- Brief 085: biology and anatomy (uses biochemistry).
- Brief 091: knowledge graph (where chemistry data lives).

## Findings — what GSPL ships at v1

### 1. Periodic table — complete and authoritative
All 118 elements with full property data:

- **Atomic data:** atomic number, mass, isotopes (atomic mass + half-life + decay mode for each), electron configuration, electronegativity (Pauling, Mulliken, Allred-Rochow), ionization energies (1st through 8th where measured), electron affinity, atomic and ionic radii.
- **Physical:** density (solid, liquid, gas at STP), melting and boiling points, heat capacity, thermal/electrical conductivity, magnetic susceptibility, sound speed, Mohs hardness.
- **Chemical:** common oxidation states, allotropes (e.g., carbon: diamond, graphite, graphene, fullerene, nanotube, amorphous), reactivity series position.
- **Optical:** color in pure form, flame test color, atomic emission/absorption spectra (line lists from NIST ASD).
- **Crystallographic:** crystal structures (e.g., BCC, FCC, HCP), lattice parameters.
- **Provenance:** every value carries an uncertainty bound and a citation to NIST, IUPAC, or peer-reviewed source.

**Source:** NIST Chemistry WebBook, IUPAC Periodic Table 2021, NIST Atomic Spectra Database (ASD), CODATA, Wolfram ElementData.

### 2. Molecular database — minimum 50,000 molecules at v1, scalable to all of PubChem
Each molecule carries:

- **Identifiers:** PubChem CID, InChI, InChIKey, SMILES, IUPAC name, common name, CAS Registry Number where available.
- **Structure:** 2D and 3D coordinates (force-field optimized), bond list with bond orders, stereochemistry, conformer ensemble for flexible molecules.
- **Properties:** molecular weight, exact mass, formula, charge, spin multiplicity, dipole moment, polarizability, HOMO/LUMO energies (where computed), logP, pKa.
- **Spectra:** UV-Vis absorption (where measured), IR vibrational modes, NMR chemical shifts, mass spectrum, Raman.
- **Color and appearance:** if a colorant or pigment, the absorption spectrum and resulting CIE color.
- **Safety:** GHS hazard classification, NFPA 704 ratings, TLV/PEL exposure limits.

**Source:** PubChem (open, ~115M compounds available; ship 50K curated subset at v1), ChEMBL (drug-like), ChemSpider, NIST WebBook for spectra, EPA CompTox, RCSB PDB for biochemistry.

**v1 curated subset includes:** all common gases (78 molecules), common solvents (50), pigments and dyes (300), drugs and medications (1000), natural product fragrances (200), polymers (100), explosives (40 — for accurate film/game depictions), metals and alloys (200), minerals (500), neurotransmitters (50), hormones (40), amino acids (20 + 22 less common), nucleotides (8), lipids (300), carbohydrates (100), vitamins (30), and ~46,000 other molecules drawn from PubChem's most-cited curated subset.

### 3. Reaction database — minimum 5,000 reactions at v1
Each reaction carries:

- **Reactants and products** with stoichiometry, balanced.
- **Conditions:** temperature, pressure, catalyst, solvent, light requirements.
- **Kinetics:** rate law form, pre-exponential factor (Arrhenius A), activation energy (Eₐ), order in each reactant.
- **Thermodynamics:** ΔH (enthalpy), ΔS (entropy), ΔG (Gibbs free energy) at STP, equilibrium constant.
- **Mechanism:** elementary steps with arrow-pushing where known.
- **Hazards and byproducts.**

**Categories:** combustion (50), oxidation/reduction (200), acid/base (100), precipitation (200), photochemistry (300 — including photosynthesis pathways), electrochemistry (200), polymerization (150), enzyme catalysis (1000 — KEGG core), atmospheric chemistry (200 — including ozone, NOx, SOx), aqueous geochemistry (150), pyrolysis (50), corrosion (100), explosions (50 — for film/game accuracy), organic name reactions (300 — Diels-Alder, Grignard, Wittig, etc.), and ~1750 metabolic and industrial reactions.

**Source:** Reaxys (commercial — defer or use open alternatives), NIST Kinetics Database, KEGG Reaction (open), MetaCyc, RHEA (EBI), USPTO Reaction Corpus (open), Open Reaction Database.

### 4. Biochemistry — KEGG-aligned at v1
- **All 20 standard amino acids** + 22 non-standard with full data.
- **All 8 standard nucleotides** with base pairing geometry.
- **Lipid taxonomy** from LIPID MAPS (8 categories).
- **Carbohydrate taxonomy** with monosaccharides, disaccharides, polysaccharides.
- **Protein structures** sampled from RCSB PDB (10,000 representative structures).
- **Metabolic pathways** from KEGG (glycolysis, TCA cycle, oxidative phosphorylation, photosynthesis, urea cycle, fatty acid synthesis/oxidation, gluconeogenesis, pentose phosphate pathway, etc.).
- **Enzyme classification** (EC numbers).

**Source:** UniProt, RCSB PDB, KEGG, LIPID MAPS, ENZYME, BRENDA.

### 5. Force fields and simulation parameters
For dynamic chemistry simulation:

- **GAFF / GAFF2** for general organic.
- **OPLS-AA / OPLS4** for organic and biomolecular.
- **AMBER** force fields (ff14SB, ff19SB) for proteins.
- **CHARMM** force fields (CHARMM36, CHARMM36m) for biomolecular.
- **MMFF94** for small organic.
- **ReaxFF** for reactive molecular dynamics.
- **Tersoff, Stillinger-Weber, EAM** for materials.

**Source:** AMBER, CHARMM, GROMACS, LAMMPS open distributions; OpenMM, RDKit, ASE for integration.

### 6. Photochemistry and color
The library includes the chemistry of color:

- **Pigments:** 300 historic and modern pigments with absorption spectra, lightfastness, opacity, oil/water vehicles, historical use periods. (For Brief 088 cross-art-style rendering and historical accuracy.)
- **Dyes:** synthetic and natural dyes with substantivity to fibers and absorption spectra.
- **Fluorophores:** 200 fluorescent compounds with excitation/emission spectra (for biology rendering).
- **Phosphors:** 50 phosphorescent compounds with afterglow curves.
- **Bioluminescence:** firefly luciferin, jellyfish GFP family, dinoflagellate, fungal — full quantum yield and emission spectra.

**Source:** Color of Art Pigment Database, FPbase (fluorophores), Wikipedia bioluminescence references, Lumosity database.

### 7. Atmospheric and environmental chemistry
- **Air composition** at sea level and as a function of altitude.
- **Standard atmosphere model** (US Standard Atmosphere 1976).
- **Trace gas concentrations** (CO₂, CH₄, N₂O, O₃, etc.).
- **Aerosol classes** with size distributions and refractive indices.
- **Cloud microphysics** parameters (droplet size distributions, ice crystal habits).
- **Water chemistry** for fresh, brackish, salt, including pH, dissolved oxygen, salinity, ion composition.

**Source:** NOAA, NASA GISS, HITRAN spectroscopic database, NIST.

## Findings — how the data is structured as gseeds

Every chemistry primitive is a **signed gseed** with a stable substrate ID. Examples:

```
chem://element/iron@v1.0    → Fe with all properties
chem://molecule/water@v1.0  → H2O with full data
chem://molecule/PubChem-CID/2244@v1.0 → aspirin
chem://reaction/combustion-methane@v1.0
chem://pathway/glycolysis@v1.0
chem://pigment/ultramarine-blue@v1.0
chem://forcefield/OPLS-AA@v1.0
```

These gseeds are **immutable, content-addressed, and signed by the GSPL Foundation Identity**, the same identity that signs the constitutional spec. Users can fork them (e.g., to add a custom force field parameter), and the lineage records the fork properly.

The chemistry library is loaded into the user's substrate cache on first launch (~200 MB) and incrementally extended on demand from the federated knowledge graph (Brief 091).

## Findings — how engines consume chemistry data

- **Particle engine (Brief 084)** consumes molecule + reaction data to drive accurate combustion, fluid behavior, and reactive simulation.
- **Materials engine (Brief 083)** consumes element + pigment data to derive optical properties from real chemistry.
- **Biology engine (Brief 085)** consumes biochemistry pathways to render metabolic processes accurately.
- **Differentiable simulation (Brief 071)** consumes force field parameters for molecular dynamics with gradients.
- **Image generators** receive chemistry context as conditioning ("water" carries with it dipole moment, refractive index, surface tension, color, IR absorption, hydrogen bonding network — not just the word).

The chemistry library is the **first reality grounding** of the substrate. Every "this looks real" claim downstream depends on it.

## Inventions

### INV-310: Substrate-native chemistry as signed gseeds
Every chemistry primitive — element, molecule, reaction, pathway, pigment, force field — is a signed gseed under the GSPL Foundation Identity, immutable, content-addressed, forkable, and federated. Engines consume chemistry as substrate, not as configuration. Novel because no creative tool ships chemistry as first-class substrate primitives with cryptographic provenance.

### INV-311: Chemistry-as-conditioning for generative engines
Image, video, and 3D generators receive chemistry context as part of their conditioning input. When the prompt contains "water," the conditioning includes water's actual physical properties, which the substrate uses to bias rendering toward physically-correct output. Novel as a substrate-mediated grounding mechanism for generative models.

## Phase 1 deliverables

- **All 118 elements** with full periodic table data signed at v1.
- **50,000 molecules** with structure, properties, and spectra at v1.
- **5,000 reactions** with kinetics and thermodynamics at v1.
- **All KEGG core metabolic pathways** at v1.
- **5 major force fields** packaged for differentiable simulation at v1.
- **300 pigments + 200 fluorophores** for photochemistry at v1.
- **Atmospheric chemistry baseline** (US Standard Atmosphere + HITRAN subset) at v1.
- **Chemistry-as-conditioning protocol** wired into the image engine at v1.

## Risks

- **Database size.** Full PubChem is ~50 GB. Mitigation: ship 200 MB curated subset; pull additional molecules on demand from federated knowledge graph.
- **Licensing.** PubChem is open. KEGG has restrictions for redistribution; use RHEA or MetaCyc as alternative. Reaxys is commercial — avoid.
- **Force field compatibility.** Force fields have subtle version differences. Mitigation: ship multiple versions; lineage records which version was used.
- **Data quality variation.** Open chemistry databases have inconsistent quality. Mitigation: every value carries uncertainty + citation; substrate displays both.

## Recommendation

1. **Lock the v1 chemistry library** to the curated subset above (~200 MB).
2. **Sign the entire library** under the GSPL Foundation Identity at v1 release.
3. **Build the federation pull** so users can extend their local cache from the knowledge graph on demand.
4. **Wire chemistry-as-conditioning** into the v1 image engine.
5. **Engage RDKit, OpenBabel, ASE, and OpenMM** as upstream open-source partners.
6. **Avoid commercial databases** (Reaxys, SciFinder) in favor of open alternatives.

## Confidence
**5/5.** The data sources are all open, authoritative, and stable. Curation is engineering work, not research risk.

## Spec impact

- `inventory/chemistry.md` — new doc.
- `inventory/chemistry-schema.md` — new doc with the gseed schema for chemistry primitives.
- Update Brief 084 to consume chemistry library.
- Update Brief 083 to consume chemistry for materials.
- Update Brief 085 to consume biochemistry.
- New ADR: `adr/00NN-chemistry-as-substrate-primitive.md`.

## Open follow-ups

- Curation of the 50K molecule v1 subset (engineering task).
- Force field license review.
- Chemistry-as-conditioning implementation in the image engine.
- KEGG vs RHEA vs MetaCyc choice for v1 metabolic pathways.

## Sources

- NIST Chemistry WebBook (https://webbook.nist.gov/chemistry/).
- NIST Atomic Spectra Database.
- IUPAC Periodic Table 2021.
- CODATA 2018 fundamental constants.
- PubChem (NCBI).
- ChEMBL (EBI).
- KEGG (Kanehisa Labs).
- RHEA (EBI).
- MetaCyc.
- RCSB Protein Data Bank.
- UniProt.
- LIPID MAPS.
- Open Reaction Database.
- HITRAN spectroscopic database.
- AMBER, CHARMM, GROMACS, LAMMPS, OpenMM, RDKit, ASE documentation.
- FPbase (fluorescent protein database).
- Color of Art Pigment Database.
- US Standard Atmosphere 1976 (NASA).
