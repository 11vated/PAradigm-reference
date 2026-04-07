# 086E — Culture, history, mythology, and folklore library

## Question
What cultural, historical, mythological, and folkloric data must GSPL ship at v1 so that any setting, period, character, ritual, garment, weapon, or symbol a creator invokes is grounded in real cultural and historical scholarship — and so that mythological creatures, deities, and stories from world traditions are available as composable, attributed gseeds?

## Why it matters
A creator says "a Heian-period courtesan," "a Yoruba market in 1910," "Thor with Mjölnir," "a Roman legionary at Zama," "an Inca quipu keeper," "a 1970s disco." Every one is a culture-and-history problem. A substrate that ships only Western default settings is parochial. A substrate that ships **the world's cultures, periods, mythologies, and folklores as signed, attributed gseeds — with provenance, source-culture identification, and respectful sourcing** is the only one that lets every creator find their story already partially grounded.

## What we know from the spec
- Brief 085: biology (mythological composite rigs).
- Brief 086D: language (named entities, idioms).
- Brief 086F: built world (architecture, transportation).
- Brief 086G: lifestyle (fashion, food, decor).

## Findings — what GSPL ships at v1

### 1. Historical periods and timelines
- **Global periodization** by region: Africa, Americas, East Asia, South Asia, Southeast Asia, Central Asia, Middle East, Europe, Oceania, Arctic.
- **Time depths:** prehistory (Paleolithic → Mesolithic → Neolithic), early civilizations, classical antiquity, medieval, early modern, modern, contemporary — each with regional variants.
- **Major events** (consensus history): kingdoms, empires, wars, plagues, migrations, voyages, revolutions — each as a dated, geo-tagged event gseed with cited sources.
- **Dynasties and rulers:** lists with reign dates from authoritative sources.

**Source:** Encyclopedia Britannica (CC subset), Wikipedia history corpora, Stanford Encyclopedia of Philosophy, OpenHistoricalMap, Pleiades (ancient places), Seshat Global History Databank.

### 2. Cultures and ethnographies
- **HRAF Outline of World Cultures** taxonomy (~400 societies) with kinship systems, subsistence, religion, social structure, material culture pointers.
- **Source-culture identification** is mandatory for every cultural gseed: who originated this, where, when, with what citation.
- **Living vs historical** flag.
- **Sacred/restricted** flag for materials that the source culture treats as not-for-general-use (substrate respects this and surfaces the restriction to creators; never silently censors).

**Source:** Human Relations Area Files (Yale), eHRAF World Cultures, Ethnologue, Endangered Languages Project.

### 3. World mythology
- **Pantheons:** Greek, Roman, Norse, Celtic, Egyptian, Mesopotamian (Sumerian/Akkadian/Babylonian), Hindu, Buddhist, Shinto, Chinese folk, Korean folk, Vietnamese, Thai, Khmer, Yoruba/Ifa, Akan, Vodun, Maya, Aztec, Inca, Lakota, Inuit, Maori, Aboriginal Australian, Polynesian, Slavic, Finnish, Basque, Sami.
- Each deity ships as a gseed with attributes, iconography, associated animals/colors/symbols, mythological role, source texts, and **source-culture attribution**.
- **Mythological creatures:** dragon (Western, Eastern, Mesoamerican variants), unicorn, phoenix, griffin, sphinx, centaur, minotaur, hydra, kraken, leviathan, basilisk, chimera, manticore, kitsune, tengu, oni, naga, garuda, qilin, baku, tanuki, jinn, ifrit, anansi, mami wata, thunderbird, sasquatch, yeti, banshee, leprechaun, troll, dwarf, elf, fae, demon, angel, valkyrie, einherjar, etc. — each with **source culture, citation, and consumption rules** documented.
- Composable rig identities link to Brief 085 biology mythological composite rigs.

**Source:** Theoi.com (CC), Encyclopedia Mythica, Encyclopedia of World Mythology references, source-culture publications, scholarly editions of primary texts (Edda, Mahabharata, Popol Vuh, Kojiki, etc.).

### 4. Religions and belief systems
- **Major living traditions:** Christianity (denominations), Islam (schools), Judaism (movements), Hinduism (sampradayas), Buddhism (Theravada/Mahayana/Vajrayana), Sikhism, Jainism, Zoroastrianism, Bahá'í, Shinto, Taoism, Confucianism, indigenous spiritualities.
- **Iconography** with source-tradition attribution.
- **Sacred architecture** types (church, mosque, synagogue, temple, gurdwara, pagoda, shrine, etc.) — links to Brief 086F.
- **Liturgical objects, vestments, calendars.**
- **Sacred texts** as referenced primary-source pointers (never reproduced wholesale).
- **Restricted/sacred** flag is universal and respected.

**Source:** Pew Research religious atlases, Encyclopedia of World Religions, Stanford Encyclopedia of Philosophy.

### 5. Folklore and oral tradition
- **Tale type indices:** Aarne-Thompson-Uther (ATU) tale type system.
- **Motif index:** Stith Thompson Motif-Index of Folk-Literature.
- **Regional folktale collections** with attribution.
- **Folk songs and ballads** referenced through Roud Folk Song Index.

**Source:** ATU index, Stith Thompson Motif-Index, Roud Folk Song Index, folklore society publications.

### 6. Symbolic systems
- **Heraldry** (tinctures, charges, ordinaries, blazon grammar).
- **Flags** of every nation and most subnational regions, with historical variants.
- **Vexillology** primitives.
- **Iconography:** zodiac (Western, Chinese, Vedic), Tarot (Major Arcana with art-historical sources), I Ching hexagrams, runes (Elder/Younger/Anglo-Saxon Futhark), Ogham, Adinkra symbols, Kolam patterns.
- **Symbols of nation, faith, profession** with source attribution.

### 7. Historical persons
- **Public-domain figures only** at v1: pre-1928 figures with established biographies. Living and recent figures are explicitly excluded from the gseed library to avoid identity-rights issues (Brief 088 character canon enforces this rule).
- Each historical figure ships as a gseed with dates, role, region, citation, public-domain portraits where available, and a **clearly-marked confidence and provenance**.

**Source:** Wikipedia, Wikidata, Project Gutenberg author corpora, Library of Congress public-domain portrait collection.

### 8. Cultural events and rituals
- **Calendrical observances:** religious (Eid, Diwali, Hanukkah, Christmas, Easter, Lunar New Year, Obon, Day of the Dead, Solstice, Equinox, etc.) and civil (Independence Days, Memorial Days, harvest festivals).
- **Lifecycle rituals:** birth, naming, coming-of-age, marriage, funerary practices — with regional variants.
- Each shipped with source-culture attribution and respect-flag.

## Findings — culture gseed structure

```
culture://period/heian-japan@v1.0
culture://event/hejira-622-CE@v1.0
culture://deity/yoruba/sango@v1.0  [source: Yoruba religion, citation, sacred:true]
culture://creature/japanese/kitsune@v1.0
culture://symbol/heraldry/lion-rampant@v1.0
culture://figure/pubdom/cleopatra-VII@v1.0
culture://ritual/dia-de-los-muertos@v1.0
```

Every culture gseed carries: source culture identifier, citation, confidence rating, restricted flag, living-vs-historical flag, and lineage to the scholarly source.

## Inventions

### INV-332: Source-attributed culture substrate
Every cultural gseed carries mandatory source-culture attribution, citation, confidence, and restriction flag. The substrate refuses to ship cultural primitives without attribution. Novel because no creative tool ships culture as substrate primitives with mandatory provenance and source-culture respect.

### INV-333: Sacred/restricted respect contract
Cultural materials that the source culture identifies as sacred or restricted are surfaced to creators with the restriction visible at substrate level — never silently censored, never silently used. Creators see the source culture's wishes and decide consciously. Novel as a substrate-level cultural-rights contract.

## Phase 1 deliverables

- **HRAF cultural taxonomy** at v1.
- **30 major mythologies** with deity, creature, and primary-text attribution at v1.
- **All major living religions** with iconography and architecture pointers at v1.
- **ATU tale type + motif index** at v1.
- **Heraldry, flags, zodiac, runes, tarot** symbolic systems at v1.
- **Pre-1928 historical figures** with citations at v1.
- **Major cultural events and rituals** with attribution at v1.
- **Sacred/restricted contract** wired through substrate at v1.

## Risks

- **Cultural appropriation harm.** Mitigation: source-culture attribution and restricted flags are non-negotiable; substrate surfaces them to every creator.
- **Scholarly disputes.** Mitigation: every entry cites source; conflicting interpretations shipped as separate gseeds with `source` field.
- **Living-figure identity rights.** Mitigation: hard exclusion of post-1928 named figures from the gseed library (Brief 088).
- **Coverage bias toward Western canon.** Mitigation: explicit non-Western coverage targets at v1; engage non-Western scholars.

## Recommendation

1. **Lock v1 mythology coverage** to 30 traditions with non-Western majority.
2. **Sign all gseeds** under GSPL Foundation Identity with source attribution mandatory.
3. **Build the restricted-flag substrate contract** as a v1 commitment.
4. **Engage HRAF, eHRAF, Stanford Encyclopedia, source-culture scholars** as upstream partners.
5. **Ban living-figure gseeds** from the foundation library (enforce in Brief 088).

## Confidence
**4/5.** Sources are open and rich; the cultural-respect work is non-trivial and ongoing.

## Spec impact

- `inventory/culture.md` — new doc.
- `inventory/cultural-attribution-schema.md` — new doc.
- New ADR: `adr/00NN-source-culture-attribution.md`.
- New ADR: `adr/00NN-sacred-restricted-respect-contract.md`.

## Open follow-ups

- Non-Western coverage gap audit.
- Source-culture scholar engagement plan.
- Restricted-flag UX design.

## Sources

- HRAF Outline of World Cultures (Yale).
- eHRAF World Cultures.
- Ethnologue.
- Theoi.com.
- Stanford Encyclopedia of Philosophy.
- Pew Research religious atlases.
- ATU Tale Type Index (Uther 2004).
- Stith Thompson Motif-Index of Folk-Literature.
- Roud Folk Song Index.
- Pleiades ancient places.
- Seshat Global History Databank.
- Wikidata.
- Library of Congress public-domain collections.
- Project Gutenberg.
- Internal: Briefs 085, 086D, 086F, 086G, 088.
