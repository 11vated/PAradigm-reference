# 086A — Cosmology and astronomy library

## Question
What astronomy and cosmology data — stars, planets, moons, galaxies, nebulae, orbital mechanics, celestial coordinates — must GSPL ship at v1 so that any sky, space scene, or cosmic phenomenon a creator invokes is grounded in measured astronomy?

## Why it matters
"A starry night over the Sahara on March 14, 2027." "Saturn's rings as seen from Titan." "The Milky Way over a beach in Bali." "A black hole accretion disk." Every space and night-sky scene is an astronomy problem. Stellarium and Celestia ship sky models for science use; no creative substrate ships astronomy as composable signed primitives. GSPL does — so a creator can specify a scene by *date and place* and the substrate produces the actual sky.

## What we know from the spec
- Brief 082: physics (gravitation, relativity).
- Brief 086: earth sciences (consumes solar/lunar position).

## Findings — what GSPL ships at v1

### 1. Star catalog
- **Hipparcos + Tycho-2** (~2.5 million stars) for general sky.
- **Gaia DR3** (~1.8 billion stars) on demand from federation.
- **Bright Star Catalogue** (HR, ~9,100 stars) for naked-eye accuracy.
- Each star carries: RA, Dec, parallax, proper motion, magnitude (V, B, J, H, K), spectral type, B-V color, radius, mass, age estimates where available.
- **88 IAU constellations** with boundary lines, line figures, names, mythological references (links to Brief 086E culture library).
- **Variable stars** (Cepheids, RR Lyrae, eclipsing binaries) with light curves from AAVSO.

**Source:** ESA Hipparcos/Gaia, Yale BSC, AAVSO, IAU constellation definitions.

### 2. Solar system
- **Sun** with full physical data, granulation, sunspot cycle parameters, prominence/CME templates, spectrum.
- **8 planets + dwarf planets** (Pluto, Eris, Haumea, Makemake, Ceres) with full orbital elements (JPL HORIZONS), physical properties, atmospheric models where applicable, surface texture maps from spacecraft missions, ring systems (Saturn, Jupiter, Uranus, Neptune).
- **200+ moons** with orbital and physical data, surface maps where available (Earth's Moon, Phobos, Deimos, Io, Europa, Ganymede, Callisto, Titan, Enceladus, Triton, Charon, etc.).
- **Asteroid belt** representative population.
- **Comet templates** with coma and tail physics.
- **Kuiper belt and Oort cloud** statistical models.

**Source:** NASA JPL HORIZONS, Planetary Data System (PDS), USGS Astrogeology, IAU MPC.

### 3. Orbital mechanics
- **Keplerian orbital element propagation** with full perturbation models (J2, third-body, drag where applicable).
- **SGP4/SDP4** for satellite orbits (consumes Celestrak TLE).
- **Lunar phase computation** (ELP-2000 or DE-series ephemerides).
- **Eclipse computation** (solar, lunar, transit) for any (date, location).
- **Conjunction and opposition** events.
- **Meteor shower templates** (Perseids, Geminids, Leonids, etc.) with radiants and ZHR profiles.

**Source:** JPL DE440 ephemeris, SGP4 reference implementation, Meeus *Astronomical Algorithms*.

### 4. Deep sky
- **Messier catalog** (110 objects) with type, distance, size, photometric data.
- **NGC/IC catalog** (~13,000 objects).
- **Galaxy types** (Hubble sequence E0–Sd, Irr, dwarf) with morphological models.
- **Nebula taxonomy** (emission, reflection, planetary, dark, supernova remnant) with composition (links to chem://) and emission spectra.
- **Star clusters** (open and globular) with HR diagrams.
- **Famous deep-sky objects** with high-resolution reference imagery from Hubble/JWST/ESO (open licensed).

**Source:** NASA/IPAC Extragalactic Database (NED), SIMBAD, Messier catalog, NGC 2000.0, Hubble Legacy Archive, JWST MAST.

### 5. Cosmology
- **Big Bang to present** templated timeline with cosmological parameters (H₀, Ω_m, Ω_Λ from Planck 2018).
- **Cosmic microwave background** texture maps (Planck).
- **Large-scale structure** models (filaments, voids).
- **Black hole rendering** primitives — Schwarzschild and Kerr metrics, photon ring, accretion disk physics, gravitational lensing (consumes Brief 082 GR).
- **Neutron star, magnetar, pulsar** templates.
- **Supernova templates** by type (Ia, Ib/c, II) with light curves.
- **Galactic merger** templates.

**Source:** Planck Collaboration 2018, Sloan Digital Sky Survey, Event Horizon Telescope, Caltech/MIT LIGO.

### 6. Celestial coordinates and time
- **Coordinate systems:** equatorial (J2000, JNow), ecliptic, galactic, horizontal — with full transformation matrices.
- **Time scales:** UTC, TAI, TT, TDB, UT1, sidereal — with conversion to/from Julian Date.
- **Precession, nutation, aberration, refraction** corrections.
- **IAU 2006/2000A precession-nutation model.**

**Source:** IAU SOFA library, USNO Astronomical Almanac.

## Findings — astronomy gseed structure

```
astro://star/HIP-32349@v1.0    → Sirius
astro://planet/saturn@v1.0
astro://moon/europa@v1.0
astro://constellation/orion@v1.0
astro://nebula/M42@v1.0
astro://galaxy/andromeda@v1.0
astro://event/eclipse/2024-04-08@v1.0
astro://sky/(lat,lon,date,time)@v1  → resolved sky
```

A "sky from Lat 36°N, Lon 115°W, on August 12 2027 at 22:30 local" composes star positions, lunar phase, planetary positions, Milky Way orientation, and atmospheric extinction (consumes Brief 086) into a single rendered sky.

## Inventions

### INV-324: Coordinate-resolved sky substrate
A (lat, lon, date, time) coordinate resolves to a complete physically-correct sky composed from star catalog, ephemeris, and atmospheric optics gseeds. Novel because no creative substrate ships astronomy as a coordinate-resolvable primitive — every other tool requires the artist to fake the sky.

### INV-325: Substrate-native general relativistic rendering
Schwarzschild and Kerr metrics are encoded as substrate-callable forms; renderers integrate null geodesics for accurate black hole and neutron star visualization without per-project reimplementation. Novel as substrate-level GR rendering.

## Phase 1 deliverables

- **Hipparcos + Tycho-2** (2.5M stars) at v1.
- **88 constellations + Bright Star Catalogue** at v1.
- **Sun + 8 planets + dwarf planets + 200 moons** at v1.
- **Messier + 1000 NGC/IC** at v1.
- **JPL DE440 ephemeris** integration at v1.
- **Eclipse, conjunction, meteor shower** computation at v1.
- **Schwarzschild/Kerr black hole rendering** at v1.
- **Coordinate and time conversions** via IAU SOFA at v1.

## Risks

- **Catalog size at scale.** Mitigation: ship Hipparcos locally; pull Gaia DR3 from federation on demand.
- **GR rendering performance.** Mitigation: precomputed lookup tables for common scene types.

## Recommendation

1. **Lock v1 catalogs** to Hipparcos, Tycho-2, BSC, Messier, NGC.
2. **Sign all gseeds** under GSPL Foundation Identity.
3. **Wrap IAU SOFA + JPL HORIZONS** as substrate engines.
4. **Build the coordinate-resolved sky API** as a v1 contract.

## Confidence
**5/5.** Sources are open, authoritative, NASA/ESA/IAU-grade.

## Spec impact

- `inventory/cosmology.md` — new doc.
- `inventory/sky-coordinate-schema.md` — new doc.
- New ADR: `adr/00NN-coordinate-resolved-sky.md`.

## Open follow-ups

- Gaia DR3 federation pull pipeline.
- Black hole render lookup table generation.
- Reference imagery licensing audit (Hubble/JWST).

## Sources

- ESA Hipparcos and Gaia missions.
- Yale Bright Star Catalogue.
- NASA JPL HORIZONS.
- JPL DE440 planetary ephemeris.
- Planetary Data System (PDS).
- USGS Astrogeology Science Center.
- IAU constellation definitions and SOFA library.
- USNO Astronomical Almanac.
- NASA/IPAC Extragalactic Database (NED).
- SIMBAD astronomical database.
- AAVSO variable star database.
- Hubble Legacy Archive, JWST MAST.
- Planck Collaboration 2018 cosmological parameters.
- Event Horizon Telescope Collaboration.
- Meeus *Astronomical Algorithms*.
- Celestrak TLE.
- Internal: Briefs 082, 086, 086E.
