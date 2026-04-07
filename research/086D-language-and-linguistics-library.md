# 086D — Language and linguistics library

## Question
What language and linguistics data — phonemes, scripts, grammars, dictionaries, named entities, idioms, dialects — must GSPL ship at v1 so that any creative work involving text, speech, naming, or dialogue is grounded in real linguistic data across the world's major languages?

## Why it matters
A character speaks. A sign hangs above a shop. A title card appears. A novel narrates. A song has lyrics. Every creative work eventually touches language — and the moment it does, it must respect *which* language, *whose* dialect, *what* script, and *how* it sounds. If GSPL ships English-only or Latin-script-only, a global creative substrate becomes a parochial one. If it ships **measured phoneme inventories, complete script support, dictionaries, and named entity bases for the world's top 100 languages**, the substrate speaks the world.

## What we know from the spec
- Brief 086C: audio (phoneme synthesis, speech).
- Brief 086E: culture (consumes language for naming, mythology, idiom).
- Brief 088: cross-art-style (consumes language for typography, captions).

## Findings — what GSPL ships at v1

### 1. Phoneme inventories
- **IPA (International Phonetic Alphabet)** complete with measured formant tables for vowels (F1, F2, F3) and consonant articulation features (place, manner, voicing).
- **Phoneme inventories for 100 languages** sourced from PHOIBLE.
- **Allophone tables** for major languages.
- **Tone systems** (Mandarin 4+1, Cantonese 6, Vietnamese 6, Yoruba 3, Thai 5, etc.).
- **Prosody templates:** stress patterns, intonation contours by language family.

**Source:** PHOIBLE (UC Berkeley/Saarland), IPA Handbook, Praat reference data, UCLA Phonetics Lab Archive.

### 2. Scripts and writing systems
- **Unicode 15.1** complete script support — Latin, Greek, Cyrillic, Hebrew, Arabic, Devanagari, Bengali, Gurmukhi, Gujarati, Tamil, Telugu, Kannada, Malayalam, Sinhala, Thai, Lao, Myanmar, Khmer, Tibetan, Hangul, Hiragana, Katakana, Han (CJK Unified Ideographs), Mongolian, Georgian, Armenian, Ethiopic, Cherokee, Inuktitut, N'Ko, Adlam, Vai, etc.
- **Historical scripts:** Egyptian hieroglyphs, cuneiform, Linear A/B, Phoenician, Old Italic, runic, Ogham, Mayan glyphs.
- **Constructed scripts:** Tengwar, Klingon (where licensing permits a permissive subset).
- **Bidirectional rendering** (RTL/LTR) per Unicode BIDI.
- **Script-specific shaping** (Indic conjuncts, Arabic ligatures, CJK vertical text) via HarfBuzz wrapping.
- **OpenType feature coverage** (kerning, ligatures, contextual alternates, stylistic sets).

**Source:** Unicode Consortium, Noto fonts (Google, OFL), HarfBuzz, ICU.

### 3. Dictionaries and lexicons
- **WordNet** (English, with Princeton WordNet 3.1 + Open Multilingual WordNet for 50+ languages).
- **Wiktionary** lexicographic data (open).
- **CMU Pronouncing Dictionary** (English G2P).
- **Grapheme-to-phoneme (G2P) models** for 50 languages.
- **Frequency tables** for top 100 languages from OpenSubtitles and Wikipedia corpora.

**Source:** Princeton WordNet, Open Multilingual Wordnet, Wiktionary dumps, CMU Dict, espeak-ng phoneme rules.

### 4. Grammar and syntax
- **Universal Dependencies** treebanks for 100+ languages with morphology, POS, dependency labels.
- **Morphological analyzers** for top 30 languages.
- **Syntactic templates** (SOV, SVO, VSO, etc.) by language family.
- **Honorifics and politeness systems** (Japanese keigo, Korean speech levels, Thai pronouns, etc.).

**Source:** Universal Dependencies project, UniMorph, Apertium, Stanza.

### 5. Named entities
- **Place names** for ~10M settlements and physical features (GeoNames).
- **Person names** with cultural origin, gender association, frequency (US Census, UK ONS, INSEE, Brazilian IBGE, Korean Statistics, Japanese MoJ, Chinese statistical sources).
- **Organization, brand, fictional names** taxonomies (with restraint — see Brief 088 character canon for trademark rules).
- **Historical names** for period work (Domesday, Roman census fragments, dynasty rosters).

**Source:** GeoNames, national census bureaus, behindthename.com, USPTO trademark non-overlap zone.

### 6. Idioms, proverbs, expressions
- **Idiom databases** for top 30 languages with literal/figurative pairs.
- **Proverb collections** (Wiktionary, Wikiquote where licensing permits).
- **Slang dictionaries** (curated, dated, regionally tagged).
- **Profanity and hate-speech indices** (for filtering, never for generation).

### 7. Dialects and sociolects
- **Major dialect groupings** for top 20 languages (e.g., English: GA, RP, Cockney, AAVE, Indian, Australian, etc.; Spanish: Castilian, Mexican, Rioplatense, Caribbean, Andean; Arabic: MSA, Egyptian, Levantine, Maghrebi, Gulf, Iraqi).
- **Phonetic realization differences** per dialect.
- **Lexical and grammatical differences** per dialect.

**Source:** International Dialects of English Archive (IDEA), eWAVE atlas, peer-reviewed dialect literature.

### 8. Sign languages
- **ASL, BSL, JSL, LIBRAS, ISL** with handshape inventories, movement primitives, facial grammar.
- **HamNoSys notation** for sign-language transcription.

**Source:** ASL Signbank, DGS Korpus, peer-reviewed sign linguistics.

## Findings — language gseed structure

```
lang://phoneme/IPA/i@v1.0       → close front unrounded vowel with formants
lang://script/devanagari@v1.0
lang://lexicon/english/wordnet@v1.0
lang://g2p/japanese@v1.0
lang://dialect/english/AAVE@v1.0
lang://idiom/spanish/no-hay-mal-que-por-bien-no-venga@v1.0
lang://entity/place/lagos-nigeria@v1.0
```

When a creator drops "a market in Lagos at dawn" the substrate composes Lagos place data, Yoruba/English/Pidgin phoneme inventories for sign and speech, Naira typography, market vocal templates, and the appropriate Yoruba/English bilingual signage — all coherent, all signed.

## Inventions

### INV-330: Language as substrate primitive with measured phonetics
Every language is a signed gseed with measured phoneme inventory, prosody, script, lexicon, and dialect tree. Engines do not ship language packs; they consume the substrate's. Novel because no creative tool ships languages as substrate primitives with cross-engine linguistic coherence.

### INV-331: Coherent script + speech binding
A single language gseed binds script rendering (HarfBuzz/OpenType), G2P, prosody, and synthesizable phonemes. A title card and a voiceover for the same line use the same language identity with no possibility of drift. Novel as a substrate-level visual+acoustic linguistic identity.

## Phase 1 deliverables

- **PHOIBLE phoneme inventories** for 100 languages at v1.
- **Unicode 15.1 + Noto fonts** at v1 for full script coverage.
- **WordNet + Open Multilingual WordNet** at v1.
- **Universal Dependencies** treebanks for 100 languages at v1.
- **G2P models** for 50 languages at v1.
- **GeoNames + name databases** at v1.
- **Dialect atlases** for top 20 languages at v1.
- **Sign language primitives** for 5 major sign languages at v1.

## Risks

- **Coverage gaps for low-resource languages.** Mitigation: ship the long tail from PHOIBLE/Wikipedia even if shallow; document confidence per language.
- **Cultural sensitivity.** Mitigation: dialect data is descriptive, never prescriptive; profanity indices are filter-only, never generation hints.
- **Trademark/IP for constructed scripts.** Mitigation: ship only permissively-licensed subsets.

## Recommendation

1. **Lock v1 to top 100 languages** by speaker count.
2. **Sign all gseeds** under GSPL Foundation Identity.
3. **Wrap HarfBuzz, ICU, espeak-ng, Stanza** as substrate engines.
4. **Engage Unicode Consortium, PHOIBLE, UD, GeoNames** as upstream partners.

## Confidence
**4.5/5.** Open linguistic ecosystem is broad and well-curated.

## Spec impact

- `inventory/language.md` — new doc.
- `inventory/linguistic-schema.md` — new doc.
- New ADR: `adr/00NN-language-as-substrate-primitive.md`.

## Open follow-ups

- Low-resource language coverage strategy.
- Sign language gseed schema design.
- Profanity-filter vs generation-block boundary.

## Sources

- PHOIBLE (UC Berkeley, Saarland).
- IPA Handbook, UCLA Phonetics Lab Archive.
- Unicode Consortium, ICU.
- Noto Fonts (Google, OFL).
- HarfBuzz.
- Princeton WordNet, Open Multilingual Wordnet.
- Wiktionary, Wikipedia.
- CMU Pronouncing Dictionary.
- espeak-ng.
- Universal Dependencies.
- UniMorph, Apertium, Stanza.
- GeoNames.
- International Dialects of English Archive (IDEA).
- eWAVE atlas of varieties of English.
- ASL Signbank, DGS Korpus.
- Internal: Briefs 086C, 086E, 088.
