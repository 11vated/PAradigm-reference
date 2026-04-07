# 088 — Cross-art-style rendering and character canon

## Question
How does GSPL render a single character or scene **across every art style** — photoreal, anime, pixel, watercolor, oil painting, claymation, line art, woodcut — with consistent identity, and how does it manage character canon (who is who across forks, derivatives, and time) without ever silently misappropriating real people?

## Why it matters
Two of the highest-leverage creative requests collapse here. **(1)** "Draw my character in 12 art styles" is the single most common cross-style ask in every creative tool, and every other tool fails it because each style is a separate model with no shared identity. **(2)** "This character should be the same character across 200 scenes and 5 styles" is the single hardest consistency problem in generative media, and no other tool ships an identity primitive at substrate level. GSPL must do both — and must do them while **refusing to render real living humans without consent**.

## What we know from the spec
- Brief 073: photoreal humans.
- Brief 083: materials (skin primitive).
- Brief 085: biology (rigs).
- Brief 086H: psychology (performance).

## Findings — what GSPL ships at v1

### 1. The Character gseed
A character is a **signed substrate primitive** with these immutable fields:

- **Identity:** name (creator-chosen), creator signature, lineage hash.
- **Anatomy seed:** reference to Brief 085 rig + measured skeletal proportions, body type, height, weight ranges.
- **Skin seed:** reference to Brief 083 skin primitive with Fitzpatrick type, melanin/hemoglobin maps, freckle/scar/tattoo overlays.
- **Hair seed:** style + color + density + texture (consumes Brief 086G).
- **Face seed:** measured landmark geometry, FACS expression baseline, identity embedding (a substrate-managed face vector that survives style transfer).
- **Voice seed:** F0 range, timbre, accent, prosody (consumes Brief 086C + 086D).
- **Personality seed:** Big Five + appraisal style + cultural context (consumes Brief 086H + 086E).
- **Wardrobe library:** wardrobe gseeds bound to this character (consumes Brief 086G).
- **Style invariants:** the cross-style anchors (see §3 below).
- **Legal flags:** `is_fictional: true` (mandatory at v1), `consent_attestation` (none at v1 — see §6).

### 2. Style adapters
Each supported art style ships as a **signed style adapter gseed** that takes a character + scene and produces a render in that style. v1 ships:

- **Photoreal** (PBR via Brief 072 neural rendering).
- **Anime** (sub-styles: 90s cel, modern Kyoto Animation, Studio Ghibli-adjacent painterly, shōnen, shōjo, seinen, chibi, mecha).
- **Manga** (B&W with screentones, full color, 4-koma simplified).
- **Western comic** (silver-age, modern, indie, Euro bande dessinée, manhwa).
- **3D stylized** (Pixar-adjacent, Aardman claymation, Sony Spider-Verse comic-3D hybrid, Cuphead-rubber-hose, low-poly).
- **Painterly:** watercolor, gouache, oil, acrylic, ink wash, fresco, tempera.
- **Drawn:** line art, ink, pencil, charcoal, pastel, marker, scratchboard, woodcut, engraving, lithograph, linocut.
- **Pixel art** at 16/32/64/128/256/512 px tiers with measured palette constraints.
- **Photographic emulations:** named period film stocks, daguerreotype, tintype, Polaroid, modern digital looks.
- **Children's book illustration** (Quentin Blake-adjacent, watercolor-and-ink, etc.).
- **Editorial illustration** (New Yorker, vector flat, isometric, etc.).
- **Folk and traditional:** Ukiyo-e, Madhubani, Kalighat, Aboriginal dot painting, Inuit print, kente-pattern stylization (with source-culture attribution per Brief 086E).
- **Historical movements:** Impressionist, Cubist, Art Nouveau, Art Deco, Bauhaus, De Stijl, Pop Art, Surrealist, Abstract Expressionist, Memphis.

Total v1 target: **80 style adapters**, each signed, attributed where appropriate, and lineage-tracked.

### 3. Style invariants — the identity that survives style transfer
The hard problem in cross-style consistency is: a character drawn in photoreal and the same character drawn as anime should be **recognizably the same person** even though every pixel changes. GSPL ships these substrate-level invariants that *every* style adapter must respect:

- **Face landmark geometry** (relative positions of inner eye corners, nose tip, mouth corners, jaw points) — preserved within tolerance across styles.
- **Iris color and pattern.**
- **Hair color, length category, parting.**
- **Skin tone mapping** (Fitzpatrick type → style-appropriate palette).
- **Body proportions** (head-to-body ratio scales by style — chibi 1:2, anime 1:7, realistic 1:7.5–8 — but limb ratios within the head-count are preserved).
- **Wardrobe silhouette and color.**
- **Distinguishing marks** (scars, tattoos, freckles, moles, jewelry) preserved as identity tokens.
- **Expression baseline** (resting face from FACS).

These invariants are encoded in the character gseed and **enforced by every style adapter** as a substrate contract. The critic ensemble (Brief 074) verifies preservation per render.

### 4. Identity embedding
The substrate maintains a **face identity embedding** for each character — a learned vector that survives style transfer. It is computed from the character's photoreal render and used by every style adapter as a conditioning input. The embedding is **lineage-tracked**, **federation-shareable** under signed identity, and **never trained on real-person data** at v1 (only synthetic and creator-authored faces).

### 5. Cross-engine character coherence
A character authored once renders coherently across:

- The image engine (still frames).
- The video engine (motion).
- The 3D engine (turntables, scenes).
- The puppet engine (real-time performance).
- The audio engine (voice).
- The text engine (in-character dialogue).

Every engine reads the same character gseed and respects the same invariants. **One character, every engine.**

### 6. Real-person depiction policy at v1
GSPL **refuses** to ship character gseeds modeled on identifiable living people at v1. Specifically:

- The foundation library contains **zero living-person gseeds**.
- The training data for the substrate's identity embedding contains **zero real-person face data**.
- Pre-1928 historical figures may exist as gseeds (Brief 086E) with public-domain portrait sources.
- Users may author original fictional characters with no restriction.
- Users **cannot** publish gseeds claiming to represent identifiable living people through the GSPL Foundation Identity at v1. Federation peers may permit this under their own moderation, but the foundation namespace refuses.
- Look-alike likeness of real people produced by user fiat is the user's responsibility under their jurisdiction; substrate logs the lineage to enable accountability (consumes Brief 077 anonymity tiers).

This is a **substrate-level constitutional commitment**, not a content moderation feature.

### 7. Cross-art-style breeding
A user can take a character authored in style A and **breed** it with style B via INV-101 naturality squares, producing a coherent style-transferred derivative. The derivative is a new gseed lineage-linked to both parents. All cross-style operations are reversible — the time machine (Brief 079) can scrub between styles as a continuous parameter.

### 8. Character ensembles and casts
Characters compose into **casts**: a cast gseed binds N characters with named relationships, scene affordances, group dynamics (Brief 086H), and shared wardrobe/setting context. Casts maintain consistency across scenes spanning years of in-world time.

## Findings — character gseed structure

```
char://aria-vance@v1.0
  identity: { name, signature, fictional:true }
  anatomy: bio://human/skeleton/female-adult@v1
  skin: mat://skin/fitzpatrick-III@v1 + overlay://freckles/light
  hair: hair://style/loose-wave/auburn@v1
  face: face://landmarks/(...)
  voice: voice://(F0:220, timbre:warm, accent:RP)
  personality: psy://big-five/(O75,C60,E45,A70,N40)
  wardrobe: [garment://victorian-walking-dress@v1, ...]
  identity_embedding: <substrate-managed vector>
  signed_by: <creator>
  forever_signed_by: <creator>  ← per Brief 078 INV-303
```

The `forever_signed_by` field is the substrate's constitutional credit line (Brief 078 INV-303): every render of Aria Vance, in any style, in any engine, in any year of the project's life, carries her creator's name in lineage and (when appropriate) on the canvas.

## Inventions

### INV-341: Character as substrate primitive with style invariants
A character is a signed gseed with substrate-enforced identity invariants that every style adapter must respect. The identity survives style transfer, engine boundaries, and lineage forks. Novel because no creative tool ships character identity as a substrate primitive with cross-style enforcement.

### INV-342: Substrate identity embedding from synthetic-only data
The face identity embedding is trained on synthetic and creator-authored faces only — never on real-person scrape data. Identity preservation comes from substrate-level invariants and synthetic-trained embedding rather than from contamination by real biometric data. Novel as an ethically-trained substrate identity primitive.

### INV-343: Constitutional refusal of living-person gseeds in foundation namespace
The GSPL Foundation Identity refuses to sign character gseeds modeled on identifiable living people. This is a substrate constitutional commitment, not a moderation feature — the substrate cannot be patched to allow it without forking the identity. Novel as a substrate-constitutional consent contract.

### INV-344: Cross-engine character coherence contract
One character gseed renders coherently across image, video, 3D, puppet, audio, and text engines via shared substrate-level invariants. Novel as a substrate-level cross-engine identity contract.

## Phase 1 deliverables

- **Character gseed schema** with all invariant fields at v1.
- **80 style adapters** at v1 (photoreal, 8 anime sub-styles, 6 comic sub-styles, 5 3D stylized, 7 painterly, 12 drawn, 6 pixel tiers, 8 photographic, 4 children's/editorial, 12 folk/traditional, 12 historical movements).
- **Identity embedding** trained on synthetic + creator-authored data only at v1.
- **Cross-engine coherence contract** wired through image, video, 3D, puppet, audio engines at v1.
- **Style invariant enforcement** in critic ensemble at v1.
- **Constitutional refusal of living-person gseeds** in foundation namespace at v1.
- **`forever_signed_by`** field on every character gseed at v1.

## Risks

- **Style adapter quality variance.** Mitigation: each adapter ships with its own quality acceptance criteria; critics enforce.
- **Identity preservation fragility under extreme style transfer.** Mitigation: invariants are tunable per style; user can override per-render.
- **Look-alike misuse.** Mitigation: substrate logs lineage; federation peers can deanonymize per Brief 077 INV-224 judicial trigger.
- **Source-culture sensitivity for traditional styles.** Mitigation: source attribution and respect flag per Brief 086E.

## Recommendation

1. **Lock the character gseed schema** at v1.
2. **Sign all 80 style adapters** under GSPL Foundation Identity.
3. **Train identity embedding on synthetic-only data** as a v1 commitment.
4. **Build the constitutional refusal of living-person gseeds** as a v1 commitment.
5. **Wire cross-engine coherence** as a v1 contract.
6. **Engage style-tradition source-culture scholars** for folk and historical adapters.

## Confidence
**4/5.** The schema is novel; style adapter quality at the long tail is the open work.

## Spec impact

- `inventory/character-canon.md` — new doc.
- `inventory/style-adapters.md` — new doc.
- New ADR: `adr/00NN-character-as-substrate-primitive.md`.
- New ADR: `adr/00NN-constitutional-refusal-of-living-person-gseeds.md`.

## Open follow-ups

- Style adapter quality acceptance criteria.
- Identity embedding architecture and synthetic training data sourcing.
- Cross-engine coherence test suite.

## Sources

- Internal: Briefs 072, 073, 074, 077, 083, 085, 086C, 086D, 086E, 086G, 086H, 078, 101.
