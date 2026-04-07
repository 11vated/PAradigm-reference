# 093 — Full media spectrum and studio technique substrate (anime, cartoons, TV, film, Pixar/CGI, stop-motion, the works)

## Question
How does GSPL guarantee that **every form of visual storytelling humanity has invented** — anime, Western cartoons, live-action TV, theatrical film, Pixar / DreamWorks / Illumination / Sony Imageworks / Studio Ghibli / Aardman / Laika style CG and stop-motion, music videos, commercials, motion comics, web shorts, machinima, documentaries, mockumentaries, animated shorts, indie experimental film — composes into the substrate as a first-class library of **studio techniques**, **art frameworks**, **production pipelines**, and **specialized signed seeds**, so a creator can ask for "Pixar-style coffee shop scene at sunrise" and get one that respects the actual craft — color script, key-light rim, subsurface scattering, story-beat framing, animation principles — rather than a cargo-cult approximation?

## Why it matters
Brief 088 gives the substrate cross-art-style character coherence at the visual layer. Brief 092 gives it power systems and movesets. But style is more than a render filter, and storytelling is more than a moveset. **Studios are recipes** — Pixar's look comes from a specific stack of subsurface scattering choices, soft key + warm rim lighting, color scripts that map emotion to palette across an entire film, art-directed compositing, and the 12 principles of animation applied with specific intensities. Studio Ghibli's look comes from hand-painted backgrounds, limited animation cycles with selective full-animation moments, naturalistic ambient sound design, and ma (negative space) timing. Anime's look comes from limited animation conventions, smear frames, banked-shot conventions, and impact-frame editing. Aardman's look comes from clay-puppet armature limits, two-frame timing, fingerprint texture, and zooms-not-pans cinematography.

A creator who says "make this scene Pixar-style" does not want a Pixar logo. They want **the craft**. The substrate must own the craft as signed primitives so the creator can compose it into anything — and the substrate must be honest about the trademark and IP boundary the way Brief 092 (INV-365) is honest about character power systems. Mechanics yes; trademarked named studios, films, and characters no. A creator can compose a "Pixar-grade family-comedy short with fish protagonists in a coral reef" without ever needing to type the word *Pixar* and without ever needing to launder any specific film.

This brief makes the substrate **studio-literate** and **medium-complete**.

## What we know from the spec
- Brief 083: materials (subsurface scattering, anisotropic hair, cloth).
- Brief 084: particles and fields (water, fire, dust, hair sim).
- Brief 086C: music and audio (score, foley, sfx).
- Brief 086H: psychology and FACS (performance acting).
- Brief 087: visual phenomena coverage atlas (120 phenomena across 12 categories).
- Brief 088: character canon, 80 style adapters, identity invariants.
- Brief 088A: canonical seed armory.
- Brief 089: conversion pipeline.
- Brief 090: web reference fetcher.
- Brief 091: knowledge graph.
- Brief 092: character power systems, forms, moves, the six interaction operators.

## Findings — the architecture

### 1. The medium gseed (`medium://`)
Every medium of visual storytelling is a signed `medium://` gseed declaring its production constraints, default conventions, and substrate compositions. URL pattern:

```
medium://<medium-id>@vN
```

Seeded media at v1 (45 minimum):

- **Animation media:** anime (TV, OVA, theatrical), Western 2D animated TV, Western 2D animated theatrical, CG animated theatrical (the Pixar-grade lane), CG animated TV, 2.5D cutout (paper / Flash / Toon Boom), rotoscope, motion-capture-driven CG, stop-motion claymation, stop-motion puppet, stop-motion silicone, stop-motion mixed-media, Aardman-style claymation lane, Laika-style hybrid replacement-face stop-motion, anime-CG hybrid, Studio Ghibli-style hand-painted background lane, sakuga-rich limited animation, full animation, motion comic, lyric video, music video (live action, animated, hybrid), animatic, storyboard reel.
- **Live-action media:** theatrical feature film, indie feature film, episodic prestige TV, multi-cam sitcom, single-cam sitcom, soap opera, telenovela, K-drama, J-drama, C-drama, anthology series, miniseries, documentary (observational, talking-head, archival, hybrid), mockumentary, reality TV, game show, news broadcast, livestream, vlog, found footage, YouTube short-form, TikTok short-form, commercial (15s/30s/60s), music video (live action), trailer, teaser, behind-the-scenes / making-of.
- **Hybrid and experimental media:** machinima, virtual production (LED volume), AR film, VR experience, 360 video, interactive film, CYOA branching narrative, motion capture short, game cutscene, in-game cinematic, real-time previs, real-time volumetric capture.

A medium gseed declares:

- **Default frame rate** (24, 23.976, 25, 30, 60, mixed) and the substrate-typed temporal grid.
- **Default aspect ratios** (1.33, 1.66, 1.85, 2.39, 2.0, 1.43 IMAX, 9:16 vertical).
- **Default color pipeline** (BT.709, BT.2020, ACES, sRGB, P3-D65, log encodings).
- **Default audio bus layout** (stereo, 5.1, 7.1, Atmos, binaural).
- **Production pipeline** as a substrate workflow gseed (storyboarding → animatic → layout → blocking → animation → lighting → effects → compositing → grade → audio → mastering, each as a substrate-recognized stage).
- **Cinematography conventions** — typical lens kits, typical shot lengths, typical camera moves.
- **Editing conventions** — cut rhythm, transition vocabulary, montage grammar.
- **Sound conventions** — score density, foley density, ambient density, dialogue mix space.
- **Story-beat conventions** — typical pacing, act structure, scene length distribution.
- **Performance conventions** — acting register (subtle, broad, anime-stylized, theatrical, naturalistic, deadpan), FACS intensity range (Brief 086H).
- **Refusal envelope** — what the substrate refuses to compose under this medium (e.g., `medium://documentary` refuses fabricated quotes attributed to identifiable real people).

### 2. The studio technique gseed (`studio-technique://`)
A studio is not a brand — it is a stack of techniques. Every reusable technique is a signed `studio-technique://` gseed. URL pattern:

```
studio-technique://<technique-id>@vN
```

Seeded technique families at v1:

- **Animation principles** (Disney 12: squash and stretch, anticipation, staging, straight-ahead and pose-to-pose, follow-through and overlapping action, slow in and slow out, arcs, secondary action, timing, exaggeration, solid drawing, appeal). Each principle is a signed substrate primitive with a substrate-typed intensity slider, and animation-curve operators that consume the principle and apply it to a rig channel (Brief 085).
- **Pixar-grade CG craft stack** (the lane, not the brand): physically based subsurface scattering for skin and translucent materials, art-directed soft-key + warm-rim lighting, color script as a film-length palette curve, anisotropic hair shading, art-directable cloth simulation, story-beat shot framing, "appeal-first" character silhouettes, compositing-stage atmospheric fill, micro-expression performance acting through FACS (Brief 086H), grounded weight in animation timing.
- **Studio Ghibli-style hand-painted background craft stack:** watercolor-luminance background plates, naturalistic atmospheric perspective, character cels rendered with limited highlight steps over fully painted environments, ma (negative space) timing, ambient sound design with selective musical silence, cycle animation for environment elements (wind, water, foliage), pillow-shot inserts.
- **Anime craft stack:** limited animation with held cels for talking, sakuga bursts for action, smear frames, multi-plane panning, banked-shot conventions, impact frames (white flash, single-color silhouette, shock lines), bokashi gradient skies, sound effect glyphs, dialogue-driven framing.
- **Aardman / Laika stop-motion craft stack:** clay armature limits, fingerprint texture preservation, two-frame timing rhythm, replacement-face animation libraries, in-camera depth-of-field, miniature set scale conventions, practical lighting only.
- **Western TV cartoon craft stack:** flat-color cel-shaded vector animation (Toon Boom / Flash conventions), squash-and-stretch caricature, broad acting register, timing-driven gag construction, character-pose silhouette tests, limited-palette backgrounds.
- **Pixar-grade story craft stack:** the 22 story rules attributed to Emma Coats (substrate-encoded as story-beat constraints, not a checklist), three-act structure variants, the Pixar-style "what does the protagonist need vs what they think they want" core, Braintrust-style critique pass (Brief 088 §8 critic ensemble) wired against story-beat gseeds.
- **Live-action craft stacks:** prestige cinematic (Roger Deakins-tier naturalism), single-cam sitcom (three-walls-and-fourth-wall convention), multi-cam sitcom (proscenium with audience laugh track), soap (locked camera, dialogue-heavy, slow zoom), documentary (vérité handheld, talking head with B-roll, archival splice), mockumentary (Office-style talking head with reactive cutaways), found footage (in-world camera operator).
- **CG VFX craft stacks:** photoreal integration (HDR-lit CG into live action), creature replacement, environment extension, set extension, digital double, de-aging, time slicing, bullet-time, simulation-driven destruction.

A studio-technique gseed declares:

- **Stage of pipeline it applies to** (animation, lighting, compositing, story, performance, editing, sound).
- **Substrate primitive bindings** (which `mat://`, `fx://`, `bio://`, `audio://`, `psy://`, `move://` primitives it composes).
- **Intensity slider(s)** with substrate-typed units.
- **Compatibility matrix** — which media (`medium://`) it composes naturally with, which it can be ported to, which it conflicts with.
- **Reference exemplars** — `ref://` gseeds (Brief 090) from public-domain or open-license sources that ground the technique with measured evidence (e.g., a public-domain rotoscope frame, an open-license painted background, a CC0 hair-simulation reference).
- **Acceptance criteria** — substrate-checkable invariants the technique must satisfy when composed into a render (e.g., `subsurface-scattering-skin-pixar-lane` requires skin BSDF SSS radius ≥ N, key-light-warm-rim ratio in [0.4, 0.7], hair anisotropy ≥ N).

### 3. The art framework gseed (`art-framework://`)
An art framework is a higher-level composition of studio techniques + media + style adapter (Brief 088) + audio palette + performance register, expressing a complete *look and feel* a creator can apply with one composition. URL pattern:

```
art-framework://<framework-id>@vN
```

Seeded frameworks at v1 (target 80):

- `art-framework://pixar-grade-feature-cg` — CG animated theatrical medium + Pixar-grade craft stack + appeal-first character silhouette + warm-rim lighting + color-script palette + 24 fps + 2.39 aspect + ACES color + Atmos audio bus + grounded timing.
- `art-framework://ghibli-grade-hand-painted` — 2D animated theatrical medium + Ghibli craft stack + hand-painted backgrounds + limited cel highlights + naturalistic ambient sound + ma timing + 24 fps + 1.85 aspect.
- `art-framework://shonen-anime-action` — Anime TV medium + sakuga bursts + impact frames + speed-line vocabulary + chiptune-rock score + dialogue-driven framing + 24 fps + 16:9.
- `art-framework://slice-of-life-anime` — Anime TV medium + limited animation + ambient slice-of-life sound + naturalistic FACS register + soft-pastel palette + 24 fps + 16:9.
- `art-framework://shojo-anime` — bokashi gradients + sparkle particle vocabulary + soft-pastel palette + romance-focused performance register.
- `art-framework://90s-saturday-morning-cartoon` — Western TV cartoon medium + broad caricature + bright primary palette + gag-driven timing + theme-song-loud audio.
- `art-framework://prestige-tv-drama` — episodic prestige medium + Deakins-tier naturalism + minimal score + naturalistic FACS register + 24 fps + 2.0 aspect.
- `art-framework://multi-cam-sitcom` — multi-cam medium + three-camera proscenium + studio-audience laugh track + broad performance register + 24 fps + 1.78.
- `art-framework://aardman-claymation-comedy` — stop-motion claymation medium + Aardman craft stack + miniature set scale + practical lighting + understated British comedic timing.
- `art-framework://laika-replacement-face-stop-motion` — Laika craft stack + replacement-face library + in-camera DOF + somber-palette grading.
- `art-framework://disney-renaissance-2d` — 2D animated theatrical medium + classical Disney craft stack + Broadway-musical score + appeal-first silhouettes + 24 fps + 1.66 or 1.85.
- `art-framework://dreamworks-irreverent-cg` — CG animated theatrical medium + irreverent comedic timing + pop-needle-drop score + caricatured human proportions.
- `art-framework://illumination-broad-comedy-cg` — CG animated theatrical medium + broad slapstick + bright primary palette + minion-style sidekick conventions.
- `art-framework://sony-imageworks-graphic-cg` — CG animated theatrical medium + graphic comic-book line work + paint-on-3D shading + selective frame-rate manipulation.
- `art-framework://machinima-game-cinematic` — real-time engine medium + cutscene grammar + game-engine lighting limits + stylized voice acting.
- `art-framework://documentary-observational` — observational doc medium + handheld vérité + sync sound + minimal score + naturalistic acting (i.e. real subjects).
- `art-framework://mockumentary-office-style` — mockumentary medium + talking-head reactions + handheld B-roll + comedic awkward pauses.
- ... and 60+ more across global traditions (Bollywood masala, K-drama melodrama, Hong Kong wuxia film, Mexican telenovela, Korean variety show, Japanese tokusatsu, British panel show, Nordic noir, Italian neorealism, French nouvelle vague, Soviet montage, Bollywood item number, magical-girl mahō shōjo, mecha super-robot, mecha real-robot, isekai, cyberpunk noir, kaiju monster movie, slasher horror, found-footage horror, body horror, J-horror, K-horror, slow cinema, surrealist short, experimental abstract animation, music video performance-piece, music video narrative-piece, lyric video, web cartoon shorts era, Newgrounds-style flash animation, motion graphics explainer, infographic animation, motion comic).

A creator picks one art-framework gseed and the substrate composes the entire pipeline — medium, techniques, palette, performance register, audio bus, frame rate, aspect ratio, story conventions, FACS intensity range, lighting recipe — into a single signed configuration their scene inherits.

### 4. The production pipeline gseed (`pipeline://`)
A pipeline is the substrate's executable workflow for taking a scene from idea to finished render under a chosen medium and art framework. URL pattern:

```
pipeline://<pipeline-id>@vN
```

A pipeline gseed is a signed DAG of substrate stages:

```
beat → board → animatic → layout → blocking → animation → fx → lighting → compositing → grade → sound → master
```

Each stage is a substrate-recognized operation that consumes prior gseeds and emits new gseeds. The DAG is content-addressed and replayable. Two creators with the same scene gseeds and the same pipeline gseed produce bit-identical masters across machines.

Pipelines are seeded for the major media:

- `pipeline://pixar-grade-cg-feature` — full CG feature pipeline.
- `pipeline://ghibli-grade-2d` — 2D hand-painted pipeline with separate background and cel passes.
- `pipeline://anime-tv-weekly` — limited-animation TV pipeline.
- `pipeline://aardman-stop-motion` — stop-motion pipeline with armature build and shot logging.
- `pipeline://prestige-tv-episodic` — live-action episodic pipeline with shot list and edit timeline.
- `pipeline://music-video` — music video pipeline.
- `pipeline://documentary-vérité` — documentary pipeline with interview log and archival management.
- `pipeline://machinima` — game-engine cinematic pipeline.

Pipelines compose with the conversion pipeline (Brief 089) and the federated knowledge graph (Brief 091), so every stage's intermediate gseeds are signed and lineage-tracked.

### 5. Story-beat gseeds (`beat://`)
Story is a substrate primitive. A `beat://` gseed declares a single story beat with:

- **Beat type** — opening image, theme stated, setup, catalyst, debate, break into two, B story, fun and games, midpoint, bad guys close in, all is lost, dark night of the soul, break into three, finale, final image, *or* anime arc beats, *or* sitcom A/B/C plot beats, *or* documentary chapter beats.
- **Beat function** — what changes for the protagonist, what the audience learns, what is set up for later.
- **Emotional register** — Brief 086H emotion model output for the beat.
- **Visual register** — palette delta from the color script, framing register, lighting register.
- **Audio register** — score density, sound register.
- **Compositional invariants** — what must remain true for the beat to read.

Beats compose into act structures, which compose into full stories, which compose into episodes/films/series. The substrate's "story" is a typed graph, not a free-text screenplay. Free-text screenplays are valid input to the conversion pipeline (Brief 089) and the substrate can extract beat gseeds from them.

### 6. Color script substrate (`color-script://`)
Pixar's color script is the master tool for emotional cinematography. A `color-script://` gseed is a film-length curve mapping each story beat to a palette gseed (Brief 088 style adapter palettes), with substrate-enforced continuity rules: beats that share an emotional register must share palette family; beats that pivot the story may pivot the palette; beat-to-beat transitions are blendable. The substrate auto-derives a candidate color script from a story-beat sequence and lets the creator override per beat. The color script is reusable across art frameworks — a single color script can drive a Pixar-grade CG feature *and* a Ghibli-grade 2D feature with the substrate handling the per-medium translation.

### 7. Acting performance substrate (`performance://`)
Building on Brief 086H FACS, a `performance://` gseed is a per-character per-beat acting take: FACS Action Units over time, body language curves, vocal affect curves (Brief 086C), eye-line target, breath rate, posture, micro-expression timing. Performances are signed and reusable across renders — the same performance can drive a Pixar-grade CG render, a Ghibli-grade 2D render, an anime limited-animation render, and a live-action mocap-driven render with the substrate translating across media. This is what makes a creator-owned character's *acting* coherent across every retelling.

### 8. Cinematography substrate (`cinematography://`)
Camera framing, lens choice, focal length, focus rack, dolly path, crane move, handheld jitter, Dutch tilt, push-in, pull-back, whip pan, snap zoom, banked shot, master shot, OTS, POV, insert, cut-away, two-shot, three-shot, group shot, establishing shot, transition shot — every cinematography convention is a signed primitive. A `cinematography://` shot gseed declares the lens, the move, the framing, the focus envelope, the lighting binding, and the compositional invariants. Shot gseeds compose into shot lists, shot lists compose into sequences, sequences compose into scenes.

### 9. Refusal envelope (carried from Briefs 088, 089, 092)
- **No trademarked-specific named studio gseeds in the foundation namespace.** Pixar, DreamWorks, Disney, Warner, Studio Ghibli, Toei, Madhouse, Trigger, MAPPA, Bones, Aardman, Laika, A24, Netflix, HBO, BBC are *not* substrate primitives. The substrate provides the **craft lanes** (`art-framework://pixar-grade-feature-cg`, `art-framework://ghibli-grade-hand-painted`, `art-framework://shonen-anime-action`, `art-framework://aardman-claymation-comedy`) and the **techniques** (`studio-technique://subsurface-scattering-skin-pixar-lane`, `studio-technique://hand-painted-background-watercolor-luminance`). Creators compose lanes and techniques into their own work under their own identity.
- **No trademarked-specific named film, TV show, or character gseeds in the foundation namespace.** Same rule as Brief 092 INV-365. Mechanics yes, names no.
- **No fabricated documentary content attributed to identifiable real people.** Documentary medium gseeds enforce this constitutionally. Mockumentary medium gseeds enforce that all subjects are fictional.
- **No deepfake performances of identifiable real people** (Brief 088 INV-343). Performance gseeds may be authored only against fictional characters or against the creator's own identity (creator may give permission for their own face).
- **Source-craft attribution** — when an art framework is rooted in a specific cultural tradition (Bollywood, K-drama, telenovela, wuxia, tokusatsu), Brief 086E source-attribution and respect contracts apply. Frameworks that draw on living traditions carry source-culture credit edges in the knowledge graph.

### 10. Armory contributions (Brief 088A)
At least 300 new canonical seeds added to the armory at v1 across these categories:

- 45 medium gseeds.
- 80 art-framework gseeds.
- 100 studio-technique gseeds.
- 8 production-pipeline gseeds.
- 30 cinematography shot gseeds (the universal vocabulary: master, OTS, POV, push-in, dolly out, crane, whip pan, snap zoom, Dutch, etc.).
- 30 archetype color-script gseeds.
- 20 archetype story-beat gseeds.

Each seed exposes its full composition graph (Brief 088A INV-346) so creators learning the substrate can fork, mutate, and discover the craft.

## Inventions

### INV-366: Medium as substrate primitive
Every medium of visual storytelling — anime, cartoon, prestige TV, theatrical film, CG feature, stop-motion, documentary, music video, machinima, motion comic, vlog, sitcom, soap, K-drama, J-drama, telenovela, mockumentary, found footage, virtual production, AR/VR, 360, interactive — is a signed `medium://` substrate primitive declaring frame rate, aspect, color pipeline, audio bus, production pipeline, cinematography conventions, editing conventions, performance register, and refusal envelope. Novel as a substrate-level grammar of media itself, not just styles within one medium.

### INV-367: Studio technique as substrate primitive with checkable invariants
Every reusable craft technique — Pixar's subsurface-scattering skin lane, Ghibli's watercolor-luminance background lane, Aardman's two-frame timing, anime's impact frames, Laika's replacement-face library, Disney's 12 animation principles, Deakins-tier naturalism, banked shots — is a signed `studio-technique://` gseed with substrate-checkable acceptance criteria (BSDF parameters, lighting ratios, timing windows). Novel as a substrate-level codification of studio craft as measurable, composable primitives.

### INV-368: Art framework as composed lane (mechanics yes, brand no)
A complete look-and-feel — Pixar-grade CG feature, Ghibli-grade hand-painted, shonen anime action, slice-of-life anime, Aardman claymation comedy, Laika replacement-face stop-motion, prestige TV drama, multi-cam sitcom, K-drama melodrama, found-footage horror, motion comic, lyric video — is a signed `art-framework://` gseed composing medium + techniques + style adapter + palette + audio bus + performance register + frame rate + aspect, with the brand boundary held at the foundation namespace. Novel as a substrate-level honest answer to "how do I make it look like a Pixar film" without using the trademark.

### INV-369: Production pipeline as substrate workflow gseed
A `pipeline://` gseed is a signed DAG of substrate stages (beat → board → animatic → layout → blocking → animation → fx → lighting → compositing → grade → sound → master). Two creators with the same scene gseeds and the same pipeline gseed produce bit-identical masters. Novel as a substrate-level reproducible production pipeline, not a proprietary studio workflow.

### INV-370: Story beat as typed substrate primitive
A `beat://` gseed declares a story beat with typed function, emotional register, visual register, audio register, and compositional invariants. Stories are typed graphs of beats, not free text. The substrate can extract beats from screenplays via the conversion pipeline. Novel as a substrate-level story representation that composes with cinematography, color, and performance gseeds.

### INV-371: Color script as reusable substrate curve
A `color-script://` gseed is a film-length palette curve mapping beats to palette gseeds with continuity rules. Color scripts are reusable across art frameworks — one color script can drive a CG feature, a 2D feature, a stop-motion feature with substrate-handled per-medium translation. Novel as a substrate-level cross-medium emotional cinematography substrate.

### INV-372: Performance gseeds reusable across media
A `performance://` gseed is a per-character per-beat acting take (FACS curves + body language + vocal affect + eye-line + breath + posture). Performances are signed and reusable across CG, 2D, anime, stop-motion, and live-action mocap renders. Novel as a substrate-level cross-medium acting reuse contract.

### INV-373: Cinematography vocabulary as substrate primitives
Every shot type and camera move (master, OTS, POV, dolly, crane, whip pan, snap zoom, banked shot, push-in, pull-back, Dutch, insert) is a signed `cinematography://` gseed composing into shot lists, sequences, and scenes. Novel as a substrate-level cinematography vocabulary as composable primitives.

### INV-374: Mechanics-yes-studio-no constitutional commitment for media
The substrate constitutionally provides every craft technique of every famous studio as `studio-technique://` and `art-framework://` gseeds in the foundation namespace, while refusing to sign trademarked named studios, films, TV shows, or characters under the foundation identity. Creator-namespaced fan works are creator-signed and federation-visibility-controlled. Novel as a substrate-level honest answer to the studio trademark boundary, parallel to Brief 092 INV-365 for character power systems.

## Phase 1 deliverables

- **`medium://` schema** with at least 45 seeded media at v1.
- **`studio-technique://` schema** with at least 100 seeded techniques at v1, including the Pixar-grade craft stack, Ghibli-grade craft stack, anime craft stack, Western TV cartoon stack, Aardman/Laika stop-motion stacks, the Disney 12 animation principles, and at least 12 live-action craft stacks.
- **`art-framework://` schema** with at least 80 seeded frameworks at v1.
- **`pipeline://` schema** with 8 seeded production pipelines at v1.
- **`beat://` schema** with at least 50 seeded beat archetypes across structure systems (Save the Cat, Hero's Journey, Anime Arc, Sitcom A/B/C, Documentary Chapter, K-drama 16-episode arc).
- **`color-script://` schema** with 30 seeded archetype scripts and the substrate-level continuity validator.
- **`performance://` schema** with FACS-curve representation and cross-medium translation pass.
- **`cinematography://` schema** with 30 seeded shot types and shot-list composition.
- **Foundation refusal envelope** at v1 (no trademarked studios/films/shows/characters under foundation identity).
- **Source-craft attribution** wired through Brief 086E for culturally-rooted frameworks.
- **Armory contribution:** 300+ canonical seeds added.

## Risks

- **Trademark gravity (studios this time, not characters).** Mitigation: lane-based naming, foundation-namespace refusal, creator-namespace signing, federation visibility controls (INV-374).
- **Craft-stack accuracy drift over time** as live studios evolve their pipelines. Mitigation: stacks are versioned and the federation knowledge graph (Brief 091) supports `refutes`/`supersedes` edges so the substrate's understanding of craft can be updated without overwriting history.
- **Cultural-tradition attribution gaps** for frameworks rooted in living traditions (Bollywood, K-drama, telenovela, wuxia). Mitigation: Brief 086E source-culture contracts apply; respect-flag mandatory.
- **Pipeline complexity explosion.** Mitigation: 8 seeded pipelines at v1, creator extension under creator-namespaces, knowledge graph reuses common subgraphs.
- **Acceptance-criterion calibration.** Mitigation: each technique gseed ships with a test fixture and a public reference render under fair-use disclosure; tests are versioned.
- **Live-action realism vs constitutional refusals.** Mitigation: documentary medium and live-action mocap medium gseeds enforce no fabricated quotes/likenesses of identifiable real people; mockumentary medium enforces all subjects fictional.

## Recommendation

1. **Lock the eight schemas at v1** (`medium://`, `studio-technique://`, `art-framework://`, `pipeline://`, `beat://`, `color-script://`, `performance://`, `cinematography://`).
2. **Seed the 45 media + 100 techniques + 80 frameworks + 8 pipelines + 30 shot types + 30 color scripts + 50 beat archetypes** in the foundation namespace.
3. **Wire the Pixar-grade craft stack acceptance criteria** as substrate-checkable invariants (BSDF SSS radius, key-rim ratio, hair anisotropy, color-script continuity, animation timing).
4. **Wire the Ghibli-grade craft stack acceptance criteria** (watercolor luminance, limited cel highlights, ma timing, ambient sound density).
5. **Wire the anime craft stack** (limited-animation timing, sakuga-burst markers, impact-frame composition).
6. **Wire the Aardman / Laika craft stacks** (two-frame timing, fingerprint texture preservation, replacement-face libraries, in-camera DOF).
7. **Engage the cross-style invariant test suite** (Brief 088 §3, Brief 092 INV-360) for studio techniques.
8. **Publish the constitutional refusal commitment** (INV-374) in the spec and the studio onboarding alongside Brief 092 INV-365.
9. **Add 300 canonical seeds to the armory** (Brief 088A).
10. **Engage cultural-craft consultancies** (Bollywood industry historians, K-drama veterans, wuxia film historians, telenovela writers) for the culturally-rooted frameworks.

## Confidence
**4/5.** Architecture composes cleanly with every Round 4 brief. Engineering work is in the acceptance-criterion calibration, the cross-medium performance translation, the cultural-craft consultancies, and the seed curation.

## Spec impact

- `inventory/media.md` — new doc.
- `inventory/studio-techniques.md` — new doc.
- `inventory/art-frameworks.md` — new doc.
- `inventory/production-pipelines.md` — new doc.
- `inventory/story-beats.md` — new doc.
- `inventory/color-scripts.md` — new doc.
- `inventory/performances.md` — new doc.
- `inventory/cinematography.md` — new doc.
- New ADR: `adr/00NN-medium-as-substrate-primitive.md`.
- New ADR: `adr/00NN-studio-technique-as-substrate-primitive.md`.
- New ADR: `adr/00NN-art-framework-as-composed-lane.md`.
- New ADR: `adr/00NN-production-pipeline-as-substrate-workflow.md`.
- New ADR: `adr/00NN-mechanics-yes-studio-no-commitment.md`.

## Open follow-ups

- 100-technique seed authoring (the calibration of the Pixar-grade BSDF parameters, the Ghibli watercolor luminance, the Aardman two-frame timing, the anime impact-frame composition).
- 80-framework composition authoring.
- 8-pipeline DAG authoring with stage-validation contracts.
- Cultural-craft consultancy outreach.
- Studio UI for the color-script editor and the story-beat graph editor.
- Cross-medium performance translation acceptance tests.
- Acceptance-criterion test suite versioning policy.
- Brief 088 style adapter expansion to cover all 80 art frameworks (Brief 088 currently has 80 style adapters; we may need to expand to 120 to cover the new framework lanes).

## Sources

- Internal: Briefs 083, 084, 085, 086C, 086E, 086H, 087, 088, 088A, 089, 090, 091, 092.
