# 086G — Lifestyle library (fashion, textile, food, decor, daily life)

## Question
What clothing, textile, food, decor, grooming, and daily-life data must GSPL ship at v1 so that any character's outfit, every meal on a table, and every domestic detail a creator invokes is grounded in real material culture across the world's cultures and periods?

## Why it matters
A character's clothes tell you who they are before they speak. A meal on a table tells you the period, the region, the season, the class, the religion, and the occasion. A bowl on a shelf tells you the household. If GSPL ships only generic "shirt and pants," every character looks like a stock model. If it ships **the world's textiles, garments, foods, dishes, hairstyles, and domestic objects as signed substrate gseeds**, the lived texture of every scene becomes available as substrate.

## What we know from the spec
- Brief 083: materials (textile properties).
- Brief 085: biology (food chemistry).
- Brief 086E: culture (period, region).
- Brief 086F: built world (vessels, furniture).

## Findings — what GSPL ships at v1

### 1. Textiles
- **Fibers:** cotton (Egyptian, Pima, Sea Island, upland), linen, hemp, jute, ramie, sisal, wool (merino, cashmere, alpaca, mohair, angora, qiviut), silk (mulberry, tussah, eri, muga), leather (cattle, goat, sheep, deer, exotic), fur (with ethics flag), synthetics (polyester, nylon, acrylic, spandex, viscose, rayon, modal, lyocell, aramid).
- **Weaves:** plain, twill, satin, sateen, basket, jacquard, brocade, damask, velvet, corduroy, terry, fleece, knit (jersey, rib, cable, intarsia), crochet, lace, felt, nonwoven.
- **Patterns:** stripes (Bengal, candy, pinstripe, awning), checks (gingham, tartan, houndstooth, glen, windowpane, madras), florals (chintz, calico, Liberty), paisley, ikat, batik, kente, kuba, mud cloth, shibori, tie-dye, block print, kalamkari, suzani, kilim, ajrak, adire.
- **Dyes:** natural (indigo, madder, weld, cochineal, kermes, murex, logwood, henna, walnut, woad, saffron, turmeric, lac, brazilwood) and synthetic (with safety/lightfastness data).
- **Surface treatments:** embroidery (200+ named stitches and traditions), beadwork, applique, quilting, smocking, pleating, gathering.

Each shipped with mechanical properties (drape, stretch, shear, bending), thermal properties, optical properties (links to Brief 083 PBR), and aging/wear models.

**Source:** V&A Textile Collection, Met Costume Institute, Cooper Hewitt textile collection, Cotsen Textile Traces archive, World Textile Industry references.

### 2. Garments by culture and period
- **Western:** chiton, peplos, toga, stola, tunic, hose, doublet, kirtle, farthingale, panniers, crinoline, bustle, frock coat, tailcoat, suit (lounge/morning/evening), shirt (dress/sport/T), trousers, jeans, skirt, dress, gown.
- **East Asian:** hanfu (dynasty variants), qipao, changshan, kimono (furisode/tomesode/yukata/nōgi), juni-hitoe, hakama, hanbok (jeogori, chima, baji), ao dai.
- **South Asian:** sari (regional draping styles), salwar kameez, lehenga, churidar, dhoti, lungi, sherwani, kurta, achkan, pagdi.
- **Southeast Asian:** sarong, kebaya, longyi, áo dài, baro't saya, malong.
- **Central Asian/Mongolian:** deel, chapan, tubeteika.
- **Middle Eastern:** thobe, dishdasha, abaya, chador, hijab, turban, keffiyeh, agal, jubba, caftan, djellaba.
- **African:** boubou, agbada, dashiki, kente cloth, kanga, kitenge, gele, isiagu, shuka, leather skirt, beaded collar.
- **Indigenous Americas:** ribbon shirt, jingle dress, regalia, ribbon skirt, manta, poncho, ruana, huipil, rebozo, parka, mukluks.
- **Oceania:** lavalava, pareu, ta'ovala, korowai, grass skirt.

Each shipped as a **parametric gseed** that drapes correctly on Brief 085 anatomy via the differentiable rigger. Cultural attribution and respect-flag from Brief 086E.

**Source:** V&A Costume, Met Costume Institute, Kyoto Costume Institute, FIDM Museum, Cotsen, Berg Encyclopedia of World Dress and Fashion.

### 3. Footwear, accessories, jewelry
- **Footwear:** sandal (Roman, Japanese geta/zōri, huarache, jūta), boot (riding, combat, work, fashion), shoe (oxford, derby, brogue, loafer, pump, flat, heel), slipper, moccasin, mukluk, geta, espadrille, clog, cleat, sneaker, mojari.
- **Headwear:** hat (top hat, bowler, fedora, cloche, beret, cap, bonnet), helmet (period-accurate), turban, hijab, keffiyeh, gele, mantilla, fascinator, headband.
- **Jewelry:** ring, necklace, bracelet, anklet, earring, brooch, pendant, tiara, crown, torc, fibula, lip plate, nose ring, ear gauge — with metals (Brief 083), gemstones (Brief 081), and cultural attribution (Brief 086E).

### 4. Hair, grooming, body modification
- **Hairstyles** by culture and period: 500+ named styles with rigging-friendly hair gseeds (links to Brief 085 strand particles).
- **Beard styles, mustache styles.**
- **Tattoos** by tradition (Maori ta moko, Polynesian tatau, Japanese irezumi, Ainu, Sak Yant, henna mehndi, blackwork, neotraditional) — with **source-culture attribution and restricted-use flag** for sacred patterns (Brief 086E INV-333).
- **Scarification, piercing, body painting.**
- **Cosmetics** by period (kohl, geisha makeup, court paint, modern).
- **Nails** (length, color, art).

**Source:** Berg Encyclopedia, peer-reviewed body-art literature, museum costume collections.

### 5. Food and cuisine
- **Ingredients:** 5,000 ingredients with botanical/zoological identification (links to Brief 085 biology), nutritional data (USDA FoodData Central), seasonality, regionality, and storage.
- **Dishes:** 10,000 dishes from world cuisines with ingredients, preparation, plating, regional variants, source culture, period, and reference imagery.
- **Cooking techniques:** raw, ferment, dry, salt, smoke, pickle, boil, steam, simmer, poach, blanch, fry (shallow/deep/stir), sauté, sear, grill, broil, roast, bake, braise, stew, sous-vide, cure.
- **Tableware sets** by culture and period.
- **Beverages:** water, milk, juice, soft drinks, coffee (preparations), tea (preparations), beer, wine, cider, mead, sake, spirit, cocktail.
- **Bread, cheese, sausage, pickle, condiment** sub-libraries.

**Source:** USDA FoodData Central, Oxford Companion to Food, FAO ingredient database, Wikimedia Commons food imagery, Open Food Facts.

### 6. Domestic objects
- **Kitchen tools, dining ware, drinkware, serving ware** by period/culture.
- **Personal effects:** purse, bag, wallet, watch (mechanical/digital), eyeglasses, sunglasses, umbrella, fan, parasol, walking stick.
- **Home decor:** vase, picture frame, clock, candle holder, incense burner, prayer mat, family altar, Lares shrine, butsudan, kamidana.
- **Hygiene objects:** soap, washbasin, mirror, comb, brush, razor, toothbrush.
- **Bedding, towels, curtains.**

### 7. Daily-life activities and props
- **Activity templates:** cooking, eating, sleeping, washing, dressing, working, studying, reading, writing, drawing, painting, sewing, knitting, gardening, farming, hunting, fishing, herding, weaving, building, traveling, praying, dancing, playing, fighting.
- **Props for each activity** as composable bundles.

## Findings — lifestyle gseed structure

```
textile://fiber/silk/mulberry@v1.0
textile://weave/twill/3-1@v1.0
textile://pattern/kente/asantehene@v1.0  [source:Asante, citation, restricted:false]
garment://south-asia/sari/nivi-drape@v1.0
garment://east-asia/hanbok-female-summer@v1.0
food://dish/jollof-rice/nigerian@v1.0
food://ingredient/turmeric@v1.0
hair://style/cornrow/box-braid@v1.0  [source-culture, attribution]
deco://object/butsudan/edo@v1.0
```

A "Yoruba woman cooking jollof rice in 1970s Lagos" composes garment://yoruba-iro-buba@v1.0, hair://yoruba-suku@v1.0, food://dish/jollof-rice/nigerian@v1.0, ingredient gseeds, deco://lagos-1970s-kitchen@v1.0, lighting from Brief 082, and the architectural setting from Brief 086F — all signed, all attributed.

## Inventions

### INV-336: Parametric culturally-attributed garment substrate
Garments are parametric gseeds that drape correctly on the differentiable rigger (Brief 085 INV-208), tagged with source culture, period, and respect flag. Novel because no creative tool ships culturally-attributed garments as substrate-level parametric primitives.

### INV-337: Coherent ingredient → dish → meal composition
Ingredients link to biology gseeds (Brief 085) and chemistry gseeds (Brief 081); dishes compose ingredients with techniques and yield realistic plated outcomes; meals compose dishes with tableware and cultural context. Every level signed and attributed. Novel as a substrate-level food coherence chain from molecule to plate.

## Phase 1 deliverables

- **Textile fiber + weave + pattern + dye library** at v1.
- **Garments for 30 cultures across major periods** at v1.
- **Footwear, jewelry, hair, body-art** with source attribution at v1.
- **5,000 ingredients + 10,000 dishes** at v1.
- **Domestic object library** by period/culture at v1.
- **Daily-life activity templates** at v1.

## Risks

- **Cultural appropriation harm.** Mitigation: source attribution and restricted flags universal (Brief 086E INV-333).
- **Coverage breadth.** Mitigation: top 30 cultures depth-first.
- **Image licensing.** Mitigation: museum open-access only.

## Recommendation

1. **Lock v1 to 30 culture-period sets.**
2. **Sign all gseeds** under GSPL Foundation Identity with source attribution mandatory.
3. **Wire ingredient → biology → chemistry** coherence at substrate level.
4. **Engage V&A, Met, Kyoto Costume Institute, USDA FoodData, Oxford Companion** as upstream partners.

## Confidence
**4/5.** Sources are open and rich; curation breadth is the work.

## Spec impact

- `inventory/lifestyle.md` — new doc.
- `inventory/garment-schema.md` — new doc.
- `inventory/food-schema.md` — new doc.
- New ADR: `adr/00NN-coherent-food-substrate-chain.md`.

## Open follow-ups

- Garment drape rigging integration with Brief 085.
- Source-culture scholar engagement for textile traditions.
- Restricted body-art pattern audit.

## Sources

- V&A Costume and Textile Collections.
- Met Museum Costume Institute (Open Access).
- Kyoto Costume Institute.
- FIDM Museum.
- Cotsen Textile Traces archive.
- *Berg Encyclopedia of World Dress and Fashion*.
- USDA FoodData Central.
- *Oxford Companion to Food*.
- FAO ingredient database.
- Open Food Facts.
- Wikimedia Commons.
- Internal: Briefs 081, 083, 085, 086E, 086F.
