# 086 — Earth sciences library

## Question
What earth-science data — geology, terrain, soils, hydrology, oceans, atmosphere, weather, climate, seasons, day/night — must GSPL ship at v1 so that any planet, landscape, sky, or weather phenomenon a creator invokes is grounded in measured earth science rather than artist guesses?

## Why it matters
Half of every visual ever made is *the world the subject stands in*. "A foggy moor at dawn," "a desert at noon," "a tropical storm rolling in," "a glacier calving," "volcanic ash drifting over a city," "monsoon rain on a banana leaf." If GSPL ships hand-waved skies and fake terrain, every outdoor scene is a fake. If it ships USGS-grade geology, NOAA-grade weather, and NASA-grade atmospheric models as signed substrate primitives, the world a creator invokes is **the actual world** — and the whole substrate gains a coherent planet to stand on.

## What we know from the spec
- Brief 081: chemistry (atmosphere composition, water chemistry).
- Brief 082: physics (atmospheric optics, fluid dynamics).
- Brief 084: particles and fields (weather effects).
- Brief 086A: cosmology and astronomy (consumes earth orbit, day/night).

## Findings — what GSPL ships at v1

### 1. Geology and rocks
- **Rock taxonomy:** all 3 major classes (igneous, sedimentary, metamorphic) with 200 named rock types. Granite, basalt, gabbro, obsidian, pumice, andesite, rhyolite, diorite, peridotite (igneous); sandstone, limestone, shale, mudstone, conglomerate, breccia, chalk, chert, coal, evaporite (sedimentary); marble, slate, schist, gneiss, quartzite, phyllite, hornfels, amphibolite, eclogite (metamorphic).
- **Mineral library:** 500 minerals with composition (linked to chem://element gseeds), Mohs hardness, density, optical properties (refractive index, birefringence, pleochroism), crystal system, cleavage, color and streak.
- **Ore bodies and gemstones** with formation contexts.
- **Tectonic plate models** for geologically accurate worldbuilding.

**Source:** USGS Mineral Resources, Mindat.org, IUGS rock classification, RRUFF mineral database.

### 2. Soils and substrates
- **USDA Soil Taxonomy** — all 12 soil orders (Alfisols, Andisols, Aridisols, Entisols, Gelisols, Histosols, Inceptisols, Mollisols, Oxisols, Spodosols, Ultisols, Vertisols) with horizons, texture, color (Munsell), drainage, pH ranges, organic content, and biome correlation.
- **Sand, silt, clay, peat, loam, gravel, scree, talus.**
- **Procedural distribution maps** that match real biome-soil pairings.

**Source:** USDA NRCS, FAO Soil Atlas, ISRIC SoilGrids.

### 3. Terrain and landforms
- **Landform taxonomy:** 100 named landform types — mountain, ridge, plateau, mesa, butte, canyon, valley, gorge, fjord, delta, beach, dune (barchan, transverse, star, parabolic), bajada, alluvial fan, oxbow, esker, drumlin, moraine, kettle, sinkhole, karst, hoodoo, arch, sea stack, atoll, etc.
- **Procedural terrain generators:** real DEM-trained heightfield primitives (not Perlin guesses) — eroded mountain, riverine plain, glacial valley, volcanic island, coastal cliff, desert basin, etc.
- **Erosion models:** thermal, hydraulic, glacial, aeolian — running on the differentiable substrate so terrain can be aged.
- **Real-world DEM samples** at multiple resolutions for reference scenes (Grand Canyon, Mt. Fuji, Sahara, Iceland, Himalayas, Yosemite, Patagonia, Norwegian fjords, etc.) sourced from SRTM/ASTER/Copernicus.

**Source:** USGS National Map, NASA SRTM, ASTER GDEM, Copernicus DEM, ESRI ArcGIS reference layers (open subset).

### 4. Hydrology — rivers, lakes, glaciers, groundwater
- **River morphologies** (straight, meandering, braided, anastomosing) with measured channel geometries.
- **Lake taxonomy** (tectonic, volcanic, glacial, oxbow, playa, salt lake) with stratification and seasonal turnover.
- **Glacier types** (alpine, valley, piedmont, ice cap, ice sheet) with flow models, crevasse geometry, calving behavior.
- **Wetland classes** (bog, fen, marsh, swamp, mangrove, vernal pool).
- **Groundwater and aquifer models** for cave and spring rendering.
- **Waterfall geometries.**

**Source:** USGS Water Resources, World Glacier Monitoring Service, Ramsar wetland classifications.

### 5. Oceans and seas
- **Bathymetry models** from GEBCO at 15-arcsecond resolution.
- **Ocean current systems** (Gulf Stream, Kuroshio, ACC, etc.) as field gseeds.
- **Wave models:** JONSWAP, Pierson-Moskowitz, Trochoidal, Gerstner — all parameterized by wind speed, fetch, and depth.
- **Tides:** harmonic constituent model (M2, S2, K1, O1, etc.) for any latitude/longitude.
- **Salinity, temperature, density profiles** by ocean basin and depth (WOA — World Ocean Atlas).
- **Coral reef, kelp forest, abyssal, hydrothermal vent** ecosystem primitives.
- **Sea ice models** for polar regions.

**Source:** NOAA, GEBCO, WOA, Argo float network, Copernicus Marine Service.

### 6. Atmosphere — layers, composition, optics
- **Layered atmosphere model:** troposphere → stratosphere → mesosphere → thermosphere → exosphere with measured T/p/ρ profiles (US Standard Atmosphere 1976).
- **Composition** at every altitude (O₂, N₂, Ar, CO₂, H₂O, O₃, trace gases) — links to chem:// gseeds.
- **Atmospheric optics primitives:** Rayleigh scattering, Mie scattering, ozone absorption, aerosol extinction — all wavelength-dependent. Sky color emerges from physics, not artist tuning.
- **Sun/moon position** for any latitude, longitude, date, time (consumes Brief 086A astronomy).
- **Twilight phases** (civil, nautical, astronomical) with correct color temperatures.
- **Atmospheric phenomena:** rainbow (primary, secondary, supernumerary), halo (22°, 46°, sun dog, parhelic circle, circumzenithal arc), corona, glory, fata morgana, green flash, alpenglow, crepuscular rays, anticrepuscular rays.

**Source:** US Standard Atmosphere 1976 (NASA), HITRAN, Bruneton/Neyret precomputed atmospheric scattering, libRadtran.

### 7. Weather and climate
- **Köppen-Geiger climate classification** (all 30 sub-types) with biome and vegetation correlations.
- **Weather systems** as composable templates: high/low pressure systems, fronts (cold, warm, occluded, stationary), extratropical cyclones, tropical cyclones (with Saffir-Simpson categories), monsoons, derechos, squall lines, mesoscale convective systems.
- **Cloud library:** all 10 WMO genera (cirrus, cirrocumulus, cirrostratus, altocumulus, altostratus, nimbostratus, stratocumulus, stratus, cumulus, cumulonimbus) with species and varieties, plus measured altitude ranges and microphysical parameters.
- **Precipitation:** drizzle, rain, freezing rain, sleet, snow, graupel, hail, virga — all with droplet/crystal size distributions from NOAA.
- **Wind models** at multiple scales: global circulation cells (Hadley, Ferrel, Polar), jet streams, prevailing winds, local thermals, katabatic winds, foehn winds, sea breezes.
- **Severe weather:** tornado, supercell, microburst, dust storm, sandstorm, blizzard, ice storm, tropical cyclone — each with measured wind/pressure profiles.
- **Lightning:** intracloud, cloud-to-ground, sprite, jet, elve — Dielectric Breakdown Model parameters.

**Source:** NOAA, WMO, ECMWF, NCEI Climate Atlas, Köppen-Geiger 2018 update.

### 8. Seasons, day/night, light
- **Solar position** for any (lat, lon, date, time) via Reda-Andreas Solar Position Algorithm (NREL SPA).
- **Day length, civil twilight, golden hour, blue hour** as parameterized gseeds.
- **Seasonal vegetation cycles** (deciduous leaf-out → growth → coloring → fall → bare) tied to latitude and Köppen climate.
- **Snow cover models** with accumulation, metamorphism, melt.
- **Phenology library** for plant species (consumes Brief 085 plant data).
- **Lunar phases** (consumes Brief 086A).

**Source:** NREL SPA, USA-NPN phenology network, MODIS land surface phenology.

### 9. Volcanism and seismicity
- **Volcano types** (shield, stratovolcano, cinder cone, caldera, fissure) with eruption styles (Hawaiian, Strombolian, Vulcanian, Plinian, Surtseyan).
- **Lava rheology** (basaltic, andesitic, rhyolitic) for accurate flow simulation.
- **Pyroclastic flow, lahars, ash plumes.**
- **Earthquake source models** (point source, finite fault) for shaking simulation.

**Source:** USGS Volcano Hazards Program, Smithsonian GVP, Global CMT.

## Findings — earth gseed structure

```
earth://rock/granite@v1.0
earth://soil/USDA/mollisol@v1.0
earth://terrain/grand-canyon@v1.0
earth://hydro/glacier/alpine@v1.0
earth://ocean/wave/jonswap@v1.0
earth://atmosphere/standard-1976@v1.0
earth://weather/hurricane@v1.0
earth://cloud/cumulonimbus@v1.0
earth://climate/koppen/Cfa@v1.0
earth://volcano/stratovolcano/plinian@v1.0
```

Each is signed by GSPL Foundation, immutable, and lineage-tracked. A "scene at sunset on the Mongolian steppe in October" composes climate (Köppen BSk), terrain (steppe), atmosphere (standard 1976 with autumn aerosol), solar position (computed), vegetation (autumn-colored steppe grasses) — every parameter measured, none guessed.

## Inventions

### INV-322: Coherent planet substrate
Earth gseeds compose into a coherent planet model: a single (lat, lon, date, time) coordinate resolves to terrain, soil, climate, vegetation, atmospheric profile, solar position, and weather distribution — all consistently. Novel because no creative tool ships a coherent earth model as substrate; every other tool requires the artist to invent the world.

### INV-323: Differentiable terrain aging
Erosion models (hydraulic, thermal, glacial, aeolian) run on the differentiable substrate so terrain can be aged forward or backward by millions of years as a single parameter sweep. Novel as a substrate-level temporal-state for terrain.

## Phase 1 deliverables

- **200 rock types, 500 minerals** at v1.
- **All 12 USDA soil orders** at v1.
- **100 landform types + 20 reference DEM scenes** at v1.
- **River, lake, glacier, wetland** primitives at v1.
- **Bathymetry, current, wave, tide** models at v1.
- **US Standard Atmosphere + atmospheric optics** at v1.
- **All 10 WMO cloud genera + 30 Köppen climates** at v1.
- **Weather system templates** (cyclones, fronts, severe weather) at v1.
- **Solar position + seasonal cycles + phenology** at v1.
- **Volcanism + seismicity** primitives at v1.

## Risks

- **DEM data licensing.** Mitigation: SRTM, ASTER, Copernicus, GEBCO are open.
- **Weather model complexity.** Mitigation: ship templates, not full NWP runs; defer real forecasting to Brief 091 federation.
- **Library size.** Mitigation: lazy load DEMs from federation knowledge graph.

## Recommendation

1. **Lock the v1 earth library** to the inventory above.
2. **Sign all primitives** under GSPL Foundation Identity.
3. **Build the planet-coordinate resolver** as a v1 substrate contract.
4. **Engage USGS, NOAA, NASA, Copernicus** as upstream data partners.
5. **Wire earth-as-conditioning** into the v1 image engine.

## Confidence
**4.5/5.** Sources are open, authoritative, stable. Engineering effort is curation and coherence schema design.

## Spec impact

- `inventory/earth-sciences.md` — new doc.
- `inventory/planet-schema.md` — new doc.
- Update Brief 084 to consume weather library.
- New ADR: `adr/00NN-coherent-planet-substrate.md`.

## Open follow-ups

- DEM curation pipeline.
- Köppen-vegetation correlation tables.
- Procedural terrain generator training on real DEMs.

## Sources

- USGS National Map, Mineral Resources, Volcano Hazards.
- USDA NRCS Soil Taxonomy, FAO Soil Atlas, ISRIC SoilGrids.
- NASA SRTM, ASTER GDEM, MODIS.
- ESA Copernicus DEM, Copernicus Marine Service.
- GEBCO bathymetry.
- NOAA (weather, climate, oceans).
- WMO International Cloud Atlas.
- Köppen-Geiger 2018 update (Beck et al.).
- NREL Solar Position Algorithm.
- US Standard Atmosphere 1976.
- HITRAN, libRadtran.
- Bruneton & Neyret precomputed atmospheric scattering.
- World Ocean Atlas (NOAA).
- World Glacier Monitoring Service.
- Smithsonian Global Volcanism Program.
- Mindat.org, RRUFF mineral database.
- USA-NPN phenology network.
- Internal: Briefs 081, 082, 084, 085, 086A.
