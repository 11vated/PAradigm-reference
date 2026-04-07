# 088A — Canonical seed armory (the pre-crafted research-backed seeds)

## Question
What pre-crafted, research-backed gseeds must GSPL ship at v1 so that a new user — and the GSPL agent — opens the substrate and finds an **armory of working, production-grade seeds** ready to use, fork, breed, and learn from? Not mockups, not prototypes, not "demo content" — actual seeds that do exactly what they say, grounded in the libraries of Round 4.

## Why it matters
Every other creative tool ships with "sample projects" that are demo wrappers around a hollow engine. GSPL ships **the armory**: a library of canonical seeds that *are* the substrate's frontier, that compose the libraries (Briefs 081–087, 088) into working artifacts a user can immediately invoke, fork, and ship. The armory is how a new user understands GSPL within minutes — by seeing the substrate's full power working. It is how the GSPL agent learns the full range of the substrate — by reading the canonical compositions. **The armory is the substrate's first-person voice.**

## What we know from the spec
- All Round 4 library briefs (081–087).
- Brief 088: character canon.
- Brief 091: knowledge graph and federation.

## Findings — armory structure

The armory is organized by **what the seed produces**, not by which library it consumes. Every armory seed is:

1. **Real.** It runs. It produces a canonical, validated artifact.
2. **Composed of measured library primitives** — never hand-waved.
3. **Signed by the GSPL Foundation Identity** with full lineage to source libraries.
4. **Forkable.** Users see the composition graph and can derive their own version with one click.
5. **Documented** with the canonical use, the design notes, and the breeding affordances.
6. **Tested** with reference renders and acceptance criteria.

## Findings — armory inventory at v1

Target: **1,000 canonical seeds at v1**, distributed across categories below.

### A. Atmospheric and lighting (50 seeds)
- `seed://lighting/golden-hour-coastal@v1` — full sun-position + atmospheric scattering + warm CCT.
- `seed://lighting/blue-hour-urban@v1`
- `seed://lighting/overcast-soft@v1`
- `seed://lighting/candle-only-interior@v1`
- `seed://lighting/sodium-streetlight-night@v1`
- `seed://lighting/firelight-flickering@v1` — links combustion physics + warm spectrum.
- `seed://lighting/moonlit-snow@v1`
- `seed://lighting/dappled-forest-noon@v1`
- `seed://lighting/window-light-rembrandt@v1`
- `seed://lighting/stage-three-point@v1`
- (40 more covering the lighting axis of Brief 087)

### B. Weather and environment (60 seeds)
- `seed://weather/light-spring-rain-on-leaves@v1`
- `seed://weather/heavy-tropical-monsoon@v1`
- `seed://weather/december-snowfall@v1`
- `seed://weather/desert-heat-shimmer-noon@v1`
- `seed://weather/coastal-fog-bank@v1`
- `seed://weather/thunderstorm-approaching@v1`
- `seed://weather/aurora-borealis-arctic@v1`
- `seed://weather/sandstorm-saharan@v1`
- `seed://weather/wildfire-distant-orange-sky@v1`
- `seed://weather/morning-mist-on-pond@v1`
- (50 more covering Brief 086 weather)

### C. Materials (showcase, 80 seeds)
- `seed://material/wet-cobblestone-night@v1`
- `seed://material/aged-copper-roofing-patina@v1`
- `seed://material/crisp-linen-shirt-fresh@v1`
- `seed://material/raw-silk-sari@v1`
- `seed://material/oxidized-iron-railing@v1`
- `seed://material/polished-cherry-wood@v1`
- `seed://material/freshly-poured-concrete@v1`
- `seed://material/gold-leaf-on-icon@v1`
- `seed://material/fish-scales-rainbow-trout@v1`
- `seed://material/human-skin-fitzpatrick-IV-natural@v1`
- (70 more — every "show off the substrate" material from Brief 083)

### D. Combustion and effects (50 seeds)
- `seed://fx/campfire-pine@v1` — wood pyrolysis + spark particles + heat field.
- `seed://fx/candle-on-table@v1`
- `seed://fx/blacksmith-forge@v1`
- `seed://fx/firework-strontium-red@v1`
- `seed://fx/firework-copper-blue@v1`
- `seed://fx/welding-arc@v1`
- `seed://fx/lightning-cloud-to-ground@v1`
- `seed://fx/explosion-tnt-grounded@v1`
- `seed://fx/dust-cloud-collapsing-wall@v1`
- `seed://fx/steam-rising-from-mug@v1`
- (40 more covering Brief 084 effects)

### E. Liquids and fluids (40 seeds)
- `seed://fluid/poured-coffee-into-cup@v1`
- `seed://fluid/wave-breaking-on-rock@v1`
- `seed://fluid/wine-swirl-in-glass@v1`
- `seed://fluid/honey-drip@v1`
- `seed://fluid/blood-droplet-on-cloth@v1`
- (35 more)

### F. Characters — exemplar fictional cast (60 seeds)
- `seed://character/aria-vance-victorian-detective@v1` — fully-realized fictional character with anatomy, skin, hair, voice, personality, wardrobe across 4 seasons.
- `seed://character/kenji-tanaka-edo-craftsman@v1`
- `seed://character/amara-okonkwo-1970s-lagos-tailor@v1`
- `seed://character/eira-thorvaldsdottir-norse-skald@v1`
- `seed://character/dr-rosa-mendoza-2030-marine-biologist@v1`
- `seed://character/lin-wei-tang-dynasty-poet@v1`
- `seed://character/eli-the-baker-american-1950s@v1`
- (53 more — all original fictional characters with complete cross-style support per Brief 088, mandatory `is_fictional:true`)

### G. Creatures and animals (60 seeds)
- `seed://creature/wolf-alpha-male-running@v1`
- `seed://creature/red-fox-curious@v1`
- `seed://creature/snowy-owl-flying@v1`
- `seed://creature/atlantic-puffin-perched@v1`
- `seed://creature/great-white-shark-cruising@v1`
- `seed://creature/honey-bee-foraging@v1`
- `seed://creature/dragon-eastern-coiling@v1` — composable rig from Brief 085.
- `seed://creature/unicorn-grazing-meadow@v1`
- `seed://creature/griffin-soaring@v1`
- `seed://creature/phoenix-rebirth-ignition@v1`
- (50 more covering Brief 085)

### H. Plants and ecosystems (50 seeds)
- `seed://plant/oak-200-years-summer@v1`
- `seed://plant/cherry-blossom-full-bloom@v1`
- `seed://plant/banana-tree-tropical@v1`
- `seed://plant/saguaro-cactus-flowering@v1`
- `seed://plant/wheat-field-pre-harvest@v1`
- `seed://ecosystem/temperate-deciduous-forest-autumn@v1`
- `seed://ecosystem/coral-reef-pacific@v1`
- `seed://ecosystem/savanna-dry-season@v1`
- (42 more)

### I. Architecture and interiors (80 seeds)
- `seed://building/gothic-cathedral-interior-evening@v1`
- `seed://building/edo-period-tea-house@v1`
- `seed://building/swahili-coast-coral-stone-house@v1`
- `seed://building/yoruba-compound-courtyard@v1`
- `seed://building/maya-pyramid-temple@v1`
- `seed://interior/parisian-apartment-1920s@v1`
- `seed://interior/japanese-tatami-room-meiji@v1`
- `seed://interior/scandinavian-fjord-cabin-modern@v1`
- `seed://interior/mughal-palace-bedchamber@v1`
- `seed://interior/depression-era-american-kitchen@v1`
- (70 more covering Brief 086F and Brief 086G)

### J. Vehicles (40 seeds)
- `seed://vehicle/dhow-arabian-sea@v1`
- `seed://vehicle/viking-longship-storm@v1`
- `seed://vehicle/steam-locomotive-1880@v1`
- `seed://vehicle/biplane-1918@v1`
- `seed://vehicle/sedan-class-1970s-suburban@v1`
- (35 more)

### K. Food and table scenes (50 seeds)
- `seed://food/jollof-rice-nigerian-served@v1`
- `seed://food/hand-pulled-noodles-shanxi@v1`
- `seed://food/feijoada-brazilian-feast@v1`
- `seed://food/sourdough-loaf-fresh-from-oven@v1`
- `seed://food/sashimi-platter-edomae@v1`
- `seed://table/breakfast-french-cafe@v1`
- `seed://table/iftar-spread-cairo@v1`
- `seed://table/diwali-mithai-platter@v1`
- (42 more)

### L. Music and audio scenes (40 seeds)
- `seed://music/bach-cello-suite-prelude-G@v1` — measured solo cello in cathedral reverb.
- `seed://music/west-african-djembe-ensemble@v1`
- `seed://music/sitar-raga-yaman-evening@v1`
- `seed://music/jazz-quartet-blue-note-late-night@v1`
- `seed://soundscape/temperate-forest-dawn-chorus@v1`
- `seed://soundscape/lagos-market-noon@v1`
- (34 more)

### M. Camera and cinematography (40 seeds)
- `seed://camera/anamorphic-1.85-cinemascope@v1`
- `seed://camera/handheld-documentary-shaky@v1`
- `seed://camera/locked-off-tripod-static@v1`
- `seed://camera/dolly-push-in-slow@v1`
- `seed://camera/drone-aerial-orbit@v1`
- (35 more)

### N. Style adapters as runnable seeds (80 seeds)
- `seed://style/photoreal/cinematic-color-grade@v1`
- `seed://style/anime/90s-cel@v1`
- `seed://style/anime/ghibli-painterly@v1`
- `seed://style/manga/seinen-screentone@v1`
- `seed://style/comic/silver-age@v1`
- `seed://style/painterly/watercolor-loose@v1`
- `seed://style/painterly/oil-glazed@v1`
- `seed://style/pixel-art/16-color-32px@v1`
- `seed://style/folk/ukiyo-e-edo@v1`
- (71 more — every Brief 088 adapter as a runnable showcase)

### O. Composite scenes (the showpieces, 100 seeds)
The most important armory seeds. Each is a **fully-composed scene** that demonstrates the substrate's full coherence.

- `seed://scene/heian-courtesan-writing-letter-by-candlelight@v1` — character + interior + props + lighting + audio + script + style options.
- `seed://scene/yoruba-market-lagos-1970-noon@v1` — crowd cast + market stalls + ambient soundscape + cooking smoke + period vehicles.
- `seed://scene/viking-funeral-pyre-coastal-sunset@v1`
- `seed://scene/edo-tea-ceremony-quiet-spring@v1`
- `seed://scene/maya-temple-festival-night@v1`
- `seed://scene/parisian-cafe-rainy-evening-1923@v1`
- `seed://scene/martian-research-base-dust-storm@v1`
- `seed://scene/coral-reef-cleaning-station-pacific-noon@v1`
- `seed://scene/depression-era-front-porch-evening@v1`
- `seed://scene/forge-workshop-medieval-blacksmith-dawn@v1`
- (90 more — the showcase library that proves the substrate's coherence)

### P. Frameworks (the meta-seeds, 80 seeds)
The frameworks are the substrate's *templates* — not single artifacts but composable workflows:

- `seed://framework/character-creation-pipeline@v1` — guided composition from anatomy → skin → face → voice → personality → wardrobe → cross-style.
- `seed://framework/short-film-production@v1` — script → storyboard → shotlist → render → cut → score → mix.
- `seed://framework/album-cover-design@v1`
- `seed://framework/childrens-book-spread@v1`
- `seed://framework/game-character-with-animations@v1`
- `seed://framework/architectural-walkthrough@v1`
- `seed://framework/music-video-editorial@v1`
- `seed://framework/scientific-illustration@v1`
- `seed://framework/historical-recreation-scene@v1`
- (71 more — the substrate's first-class workflows)

### Q. Algorithms and patterns (40 seeds)
- `seed://algorithm/wave-function-collapse-tile@v1`
- `seed://algorithm/l-system-tree-generation@v1`
- `seed://algorithm/poisson-disk-sampling@v1`
- `seed://algorithm/perlin-terrain@v1`
- `seed://algorithm/marching-cubes-isosurface@v1`
- (35 more — the substrate's procedural primitives as runnable seeds)

## Findings — armory governance

- **Curation board:** the GSPL Foundation curates the armory; community contributions go through provenance and quality review.
- **Versioning:** every seed is `@v1`; updates ship as `@v1.1`, `@v2`, etc.; old versions remain immutable and retrievable.
- **Lineage:** every armory seed declares the libraries it composes — users can read the composition graph as a learning surface.
- **Quality contract:** every armory seed ships with reference render(s), acceptance criteria, and a critic-ensemble pass record.
- **Federation:** the armory is mirrored across federation peers (Brief 091).
- **Forkability:** every seed has a one-click "fork to my workspace" affordance; the fork lineage is recorded.

## Inventions

### INV-345: The canonical seed armory as substrate first-person voice
The armory is not sample content. It is the substrate speaking in the first person — a curated library of working, validated, signed seeds that demonstrates the full range of the substrate. New users learn GSPL by browsing the armory; the GSPL agent learns GSPL by reading the armory's composition graphs. Novel because no creative tool treats its sample library as a substrate-level first-person curriculum.

### INV-346: Composition graph as learning surface
Every armory seed exposes its composition graph — every library primitive it consumes, every parameter, every lineage edge. Users learn the substrate by reading these graphs. The GSPL agent uses them as in-context training examples for composition. Novel as a substrate-level didactic surface.

### INV-347: Forking the armory as the default learning loop
The armory is designed to be forked, not used as-is. Every seed has a one-click fork affordance; every fork is lineage-tracked and federation-shared. The default loop "browse → fork → modify → ship → re-fork" makes the substrate self-reinforcing. Novel as a substrate-level curriculum-via-fork loop.

## Phase 1 deliverables

- **1,000 canonical signed armory seeds** at v1, distributed across the categories above.
- **Composition graphs** exposed for every seed at v1.
- **Reference renders + acceptance criteria** for every seed at v1.
- **One-click fork affordance** wired through the studio (Brief 079) at v1.
- **Federation mirroring** at v1 (consumes Brief 091).
- **Curation board governance** at v1.

## Risks

- **Quality consistency at scale.** Mitigation: critic ensemble (Brief 074) gates every seed; manual review for the top 100 showpieces.
- **Cultural sensitivity at the long tail.** Mitigation: source-culture attribution per Brief 086E; review by source-culture consultants.
- **Authoring effort.** Mitigation: the armory is the substrate's frontier work — it justifies dedicated curation effort.
- **Overlap with creator originality.** Mitigation: the armory is the *starting point*, not the creative ceiling; the studio's affordances make personal extension obvious.

## Recommendation

1. **Lock the v1 armory at 1,000 seeds** with the category distribution above.
2. **Sign every seed** under GSPL Foundation Identity.
3. **Build the composition graph viewer** as a v1 studio affordance.
4. **Build the one-click fork** as a v1 substrate primitive.
5. **Engage source-culture consultants** for the 100+ culturally-attributed seeds.
6. **Treat the armory as the substrate's first-person voice** — not an afterthought, not a marketing surface, the substrate's own demonstration of itself.

## Confidence
**4/5.** The schema and governance are clear; the curation effort is the work.

## Spec impact

- `inventory/canonical-armory.md` — new doc.
- `inventory/armory-governance.md` — new doc.
- New ADR: `adr/00NN-canonical-armory-as-first-person-voice.md`.
- Update Brief 079 to add composition graph viewer + fork affordance.

## Open follow-ups

- 1000-seed curation plan and timeline.
- Source-culture consultant engagement.
- Composition graph viewer UX.
- Quality acceptance criteria per category.

## Sources

- Internal: All Round 4 briefs (078–087, 088), Brief 074, 091.
