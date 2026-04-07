# 086F — Built world library (architecture, transportation, urbanism, objects)

## Question
What architecture, transportation, urbanism, and object data must GSPL ship at v1 so that any building, vehicle, street, room, tool, or everyday object a creator invokes is grounded in real construction, real engineering, and real material culture across periods and cultures?

## Why it matters
Half of every scene is the *built* world. A character lives in a house. They walk down a street. They sit on a chair. They pick up a phone, a sword, a wrench. They board a train, a longship, a Boeing 747. If GSPL ships only generic "house" and "car," every scene looks like a stock-image collage. If it ships **the world's architectural traditions, vehicle taxonomies, urban patterns, and object catalogs as signed substrate gseeds**, the built world stops being a backdrop and becomes a substrate creators compose with.

## What we know from the spec
- Brief 083: materials.
- Brief 086: earth sciences (terrain).
- Brief 086E: culture (period, sacred architecture).

## Findings — what GSPL ships at v1

### 1. Architectural traditions
- **Western:** Egyptian, Greek (Doric/Ionic/Corinthian), Roman, Romanesque, Byzantine, Gothic, Renaissance, Baroque, Rococo, Neoclassical, Beaux-Arts, Victorian, Arts and Crafts, Art Nouveau, Art Deco, Bauhaus, International, Mid-Century Modern, Brutalist, Postmodern, Deconstructivist, Contemporary.
- **Islamic:** Umayyad, Abbasid, Fatimid, Mamluk, Ottoman, Mughal, Persian, Andalusian, Maghrebi, Sub-Saharan Sahel.
- **East Asian:** Chinese (dynastic variants from Han through Qing), Japanese (Heian/Kamakura/Edo/Meiji), Korean (hanok), Vietnamese, Mongolian (ger).
- **South Asian:** Vedic, Mauryan, Dravidian temple architecture (Chola/Pallava/Pandyan), Nagara, Vesara, Indo-Saracenic.
- **Southeast Asian:** Khmer, Burmese, Thai, Javanese, Balinese, Filipino bahay kubo / bahay na bato.
- **African:** Ancient Egyptian, Nubian, Aksumite, Swahili coastal, Great Zimbabwe, Mali (Djenné mud architecture), Yoruba, Ashanti, Zulu, Maasai.
- **Indigenous Americas:** Pueblo, Anasazi cliff dwellings, Mississippian mounds, longhouse, tipi, igloo, Maya, Aztec, Inca.
- **Oceania:** Maori marae, Polynesian fale, Aboriginal humpy.
- **Vernacular:** earthworks, cob, adobe, log, wattle-and-daub, half-timber, sod, ice, bamboo.

Each tradition ships as a **composable architectural grammar**: structural system (post-and-lintel, arch, vault, dome, truss, frame), material palette (links to Brief 083), proportion system (golden ratio, ken modular, Vitruvian, Le Corbusier's Modulor), ornament catalog, and **canonical example buildings** with citations.

**Source:** Banister Fletcher's *History of Architecture*, Spiro Kostof, UNESCO World Heritage Centre, ArchNet (Aga Khan Documentation Center), CyArk 3D scans, OpenStreetMap building footprints.

### 2. Building components
- **Structural:** column, beam, truss, arch, vault, dome, foundation, wall (load-bearing, curtain, shear), floor, roof (gable, hip, mansard, gambrel, flat, butterfly, sawtooth, thatch, tile, slate, shingle, sod).
- **Openings:** door, gate, window (sash, casement, oriel, lancet, rose, picture, transom, fanlight), portal, lattice (mashrabiya, shoji, jaali).
- **Stairs:** straight, L, U, spiral, helical, ladder.
- **Ornament:** molding, frieze, cornice, capital, pilaster, balustrade, gargoyle, finial, tracery.
- **Interior:** hearth, fireplace, stove, kang, ondol, hammam, sauna, bath, kitchen, pantry, scullery.

Each component is a parametric gseed sized in real units, structurally validated against the chosen tradition.

### 3. Building types
- **Residential:** apartment, house, mansion, longhouse, hut, palace, castle.
- **Religious:** church, cathedral, basilica, chapel, mosque, synagogue, temple (Hindu/Buddhist/Jain/Sikh), pagoda, stupa, gurdwara, shrine.
- **Civic:** town hall, courthouse, palace, parliament, library, museum, theater, opera house, stadium, arena.
- **Commercial:** market, bazaar, souq, mall, shop, restaurant, café, tavern, inn, hotel.
- **Industrial:** factory, mill, warehouse, foundry, dock, granary.
- **Educational:** school, university, madrasa, gurukula, monastery.
- **Defensive:** wall, gate, tower, keep, bastion, fortress.
- **Infrastructural:** bridge, aqueduct, canal, dam, lighthouse, water tower, power station.
- **Agricultural:** barn, silo, stable, kraal, terrace, paddy.

### 4. Urbanism
- **Street patterns:** grid (Hippodamian, Manhattan), radial, organic medieval, picturesque, garden city, modernist, hutong, cul-de-sac suburban.
- **Plot patterns:** burgage, longlot, ranchería, hutong courtyard.
- **Public space:** plaza, agora, forum, maidan, piazza, padang, durbar square, central park.
- **Density tiers** from rural → small town → city → megacity.
- **Real city footprints** for 50 reference cities sampled from OpenStreetMap.
- **Historical city models** (Imperial Rome, Tang Chang'an, Ottoman Istanbul, Edo Tokyo, Tenochtitlan).

**Source:** OpenStreetMap, UN-Habitat, Spiro Kostof *The City Shaped*, *The City Assembled*.

### 5. Transportation
- **Pre-modern:** chariot, oxcart, palanquin, sedan chair, dogsled, travois, sled, raft, dugout canoe, dhow, junk, longship, galley, trireme, cog, carrack, galleon, clipper.
- **Industrial:** steam locomotive, ironclad, dirigible, biplane.
- **Modern road:** bicycle, motorcycle, scooter, sedan, hatchback, SUV, pickup, van, bus, truck, tractor.
- **Modern rail:** locomotive (steam/diesel/electric), passenger car, freight car, high-speed rail, light rail, metro, monorail, tram.
- **Modern air:** propeller plane, jet airliner, helicopter, eVTOL, drone, balloon, glider.
- **Modern sea:** sailing yacht, motor yacht, container ship, tanker, cruise liner, ferry, hydrofoil, hovercraft, submarine.
- **Space:** rocket (Saturn V, Falcon 9, SLS, Long March), capsule, shuttle, space station modules.

Each shipped as a parametric gseed with measured dimensions, mass, propulsion model, and **period and source-culture attribution**. Modern named-brand vehicles ship as *generic class* gseeds (sedan, hatchback) rather than trademarked specific models, with explicit non-overlap with active trademarks.

**Source:** Smithsonian Air and Space, V&A transport collection, Imperial War Museums, Janes (open subset), Wikipedia rolling stock and vehicle data, NASA spacecraft references.

### 6. Furniture and interior objects
- **Furniture taxonomies** by period and culture: chair (5,000 distinct historical types), table, bed, chest, cabinet, desk, sofa, bench, stool, throne.
- **Lighting:** torch, candle, oil lamp, gas lamp, incandescent, fluorescent, LED — links to Brief 082 spectra.
- **Textiles:** rugs (Persian/Anatolian/Berber/Navajo with measured patterns), tapestries, curtains, bedding.
- **Vessels:** pottery, glassware, metalware, basketry by period/culture.

**Source:** V&A Museum collection (open), Met Museum Open Access, Cooper Hewitt collection, Brooklyn Museum collection.

### 7. Tools and weapons
- **Tools:** hand tools (hammer, saw, plane, chisel, awl, drill), power tools, agricultural tools, kitchen tools, scientific instruments by period.
- **Weapons:** stone-age, bronze-age, iron-age, medieval (sword/axe/spear/bow/crossbow/mace by region), early gunpowder (matchlock/wheellock/flintlock), industrial (rifle/pistol/cannon by period), modern (with restraint — no detailed schematics enabling manufacture; depiction-grade only).

Modern firearms ship as **depiction gseeds with appearance and basic action class only**, never with detailed mechanisms or modifications. Brief 088 character canon enforces appropriate-context use.

**Source:** Met Museum arms and armor, Royal Armouries (Leeds), Smithsonian.

### 8. Clothing-adjacent built objects
- **Bags, packs, scabbards, holsters, harnesses** as object gseeds (clothing proper lives in Brief 086G).

## Findings — built-world gseed structure

```
arch://tradition/gothic/cathedral@v1.0
arch://component/column/corinthian@v1.0
arch://building/notre-dame-de-paris@v1.0
urban://city/edo-tokyo-1850@v1.0
vehicle://sailing/dhow@v1.0
vehicle://aircraft/jet-airliner-class@v1.0
furniture://chair/ming-yokeback@v1.0
tool://hand/hammer/claw@v1.0
weapon://bladed/katana@v1.0
```

A "Heian-period courtesan in her chamber" composes Heian palace architecture (arch://tradition/heian-shinden@v1.0), tatami flooring (mat://organic/tatami@v1.0), shoji screens (arch://component/shoji@v1.0), futon and pillow (furniture://heian/...), oil lamp (light://oil-lamp@v1.0) — all measured, attributed, and lineage-tracked.

## Inventions

### INV-334: Composable architectural grammars as substrate
Architectural traditions are signed substrate primitives encoding structural system, proportion, material palette, ornament, and canonical examples. Buildings are composed from grammar rather than modeled from scratch. Novel because no creative tool ships architectural traditions as substrate-level grammars with cross-cultural breadth.

### INV-335: Trademark-non-overlap zone for vehicles and objects
Modern vehicles and objects ship as generic-class gseeds (sedan, hatchback, jet-airliner-class) explicitly non-overlapping with active trademarks. The substrate refuses to ship trademarked specific named models. Novel as a substrate-level IP-respect contract for the built world.

## Phase 1 deliverables

- **40 architectural traditions** with grammars at v1.
- **All major building components and types** at v1.
- **50 reference cities + 10 historical cities** at v1.
- **150 vehicle classes across all eras** at v1.
- **Furniture and interior objects** by period/culture at v1.
- **Tools and weapons** with period-respectful restraint at v1.
- **Trademark-non-overlap contract** wired through substrate at v1.

## Risks

- **Coverage breadth.** Mitigation: depth-first on top 20 cultures, breadth on long tail with citation flags.
- **Trademark/IP risk.** Mitigation: hard non-overlap zone at substrate level.
- **Weapon depiction misuse.** Mitigation: depiction-grade only, no mechanism schematics.

## Recommendation

1. **Lock v1 to 40 traditions and 150 vehicle classes.**
2. **Sign all gseeds** under GSPL Foundation Identity.
3. **Build the trademark-non-overlap contract** as a v1 commitment.
4. **Engage UNESCO, ArchNet, OpenStreetMap, V&A, Met, Smithsonian** as upstream partners.

## Confidence
**4/5.** Sources are deep and open; curation is the engineering work.

## Spec impact

- `inventory/built-world.md` — new doc.
- `inventory/architecture-grammar.md` — new doc.
- New ADR: `adr/00NN-trademark-non-overlap-contract.md`.

## Open follow-ups

- Architectural grammar formalization.
- Trademark non-overlap audit pipeline.
- Weapon depiction-grade boundary definition.

## Sources

- Banister Fletcher's *A History of Architecture*.
- Spiro Kostof *The City Shaped*, *The City Assembled*, *A History of Architecture*.
- UNESCO World Heritage Centre.
- ArchNet (MIT/Aga Khan).
- CyArk heritage 3D scans.
- OpenStreetMap.
- UN-Habitat.
- Smithsonian National Air and Space Museum.
- Imperial War Museums.
- V&A Museum, Met Museum, Cooper Hewitt, Brooklyn Museum (Open Access).
- Royal Armouries (Leeds).
- Janes (open subset).
- Wikipedia transport, building, and weapon corpora.
- Internal: Briefs 083, 086, 086E, 086G, 088.
