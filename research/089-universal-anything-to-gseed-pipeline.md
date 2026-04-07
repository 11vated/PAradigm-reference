# 089 — Universal anything-to-gseed conversion pipeline

## Question
How does GSPL convert **anything** a user can supply — a phrase, an image, a sketch, a 3D scan, an audio clip, a video, a real object, a memory described in words — into a signed, lineage-bearing, composable gseed grounded in the libraries of Round 4?

## Why it matters
The substrate is only as wide as its mouth. If a user can only invoke gseeds by browsing the armory, the substrate's reach is the curator's reach. If a user can hand the substrate **anything** — a phone photo of their childhood dog, a hummed melody, a napkin sketch of a dragon, a snippet from a historical photograph, a 3D scan of their grandmother's locket — and walk away with a signed, composable gseed, the substrate's reach is the *world's* reach. Conversion is what turns the substrate from a library into a creative organism.

## What we know from the spec
- Brief 088: character canon and identity invariants.
- Brief 088A: armory.
- Brief 091: knowledge graph.
- Brief 077: anonymity tiers (for upload privacy).

## Findings — input modalities the pipeline accepts at v1

1. **Text** — natural language description, prompt, story fragment, lyric, character bio.
2. **Single image** — photograph, painting scan, screenshot, sketch.
3. **Image set** — multiple views of the same subject for 3D reconstruction.
4. **Sketch / line drawing** — pen on paper, tablet sketch, napkin doodle.
5. **Audio clip** — voice sample, hummed melody, environmental recording, instrument playing.
6. **Video clip** — phone footage, screen recording, archival.
7. **3D scan** — phone LiDAR, photogrammetry, depth sensor.
8. **3D model file** — OBJ, FBX, glTF, USD, STL, PLY.
9. **CAD file** — STEP, IGES, DXF.
10. **Document** — PDF, DOCX, EPUB (script, screenplay, story, technical spec).
11. **Score** — MusicXML, MIDI, MEI.
12. **Motion data** — BVH, FBX skeletal animation, .smpl.
13. **Code** — a script that procedurally generates an artifact.
14. **Reference URL** — a public web page (subject to Brief 090 cross-reference rules).
15. **Memory description** — a richly-described mental image (a special case of text routed through the agent for elaboration).

## Findings — the pipeline architecture

```
INPUT → INGEST → ANALYZE → GROUND → COMPOSE → SIGN → STORE
```

### 1. Ingest
- **Sandbox isolation:** every upload runs in a content sandbox with no network access until classification completes.
- **Metadata strip:** EXIF, GPS, device IDs are stripped by default unless the user explicitly opts in.
- **Consent classifier:** identifies likely real-person faces, copyrighted material, and culturally-sacred symbols; surfaces these to the user *before* the gseed is created. (Consumes Brief 088 INV-343 and Brief 086E INV-333.)
- **Privacy tier:** user selects an anonymity tier per Brief 077 (stealth address → ring sig → ZK).

### 2. Analyze
- **Multi-modal extraction** runs on substrate-wrapped engines:
  - **Vision:** segment, classify, detect, depth-estimate, normal-estimate, material-estimate, lighting-estimate, pose-estimate, face-landmark, OCR.
  - **Audio:** speech transcribe, speaker characterize, music analyze (key/tempo/instruments), event classify.
  - **3D:** mesh repair, retopology, UV unwrap, scale calibrate, rigging hint.
  - **Text:** entity extract, sentiment, style, structure parse.
  - **Reference matching:** cross-reference against the canonical armory and the knowledge graph for similar primitives (Brief 091).

### 3. Ground
This is the substrate's discriminating step. Every extracted feature is **mapped to library primitives** from Round 4:

- A photo of a cup → mat://ceramic/glazed-stoneware@v1 + arch://component/handle + measured volume.
- A hummed melody → audio://scale/(detected key) + audio://rhythm/(detected meter) + transcription as audio://composition/(user-named).
- A 3D scan of a locket → bio://human/jewelry-ref/locket-oval, mat://metal/silver/oxidized, lineage to the upload.
- A sketch of a dragon → bio://creature/dragon-eastern + custom horn count + scale color from sketch palette.

The ground step **never invents data**. If a property cannot be measured or matched with confidence above threshold, it is left unbound and the user is told. **No silent guesses, no placeholders.**

### 4. Compose
The grounded features are composed into a candidate gseed with:

- The right substrate URL pattern (`char://`, `mat://`, `audio://`, `arch://`, etc.).
- Lineage edges to every library primitive consumed.
- Lineage edges to the original upload (with privacy tier respected).
- Confidence scores per field.
- A "ready to fork" affordance.

### 5. Sign
The candidate is signed by the user's identity (or stealth address per Brief 077) and gains a stable substrate ID. The original upload is **not** re-published unless the user explicitly chooses to share it; only the gseed is.

### 6. Store
- Local cache by default.
- Federation publish opt-in (Brief 091).
- Lineage anchoring on Brief 075's federated knowledge graph.

## Findings — interaction with the GSPL agent

The pipeline is exposed to the user through the GSPL agent, which:

1. **Asks** what the user wants the upload to *become* (a character? a material? a scene? a melody?). This guides the analyzer.
2. **Shows** the analysis transparently — every detected feature, every matched library primitive, every confidence score.
3. **Negotiates** ambiguities directly with the user ("the metal here looks like it could be silver or pewter — which?").
4. **Refuses** to invent values; tells the user when a property is unknown.
5. **Offers** the next breeding step (cross-style, time machine, scene composition).

The agent is the substrate's interface to conversion. It is not magic — it is **negotiated, transparent grounding**.

## Findings — refusal cases

The pipeline **refuses** to convert:

- **Identifiable living persons** into character gseeds in the foundation namespace (Brief 088 INV-343).
- **Copyrighted works** into derivative gseeds without an explicit fair-use attestation by the user.
- **Trademarked named brands and vehicles** into specific-named gseeds; only generic-class gseeds (Brief 086F INV-335).
- **Sacred-restricted cultural symbols** without source-culture attribution (Brief 086E INV-333).
- **Weapons schematics** into manufacture-grade detail; only depiction-grade.
- **Mental health diagnostic claims** about identifiable persons (Brief 086H INV-339).

Refusals are **substrate-level constitutional commitments**, not patchable moderation features.

## Inventions

### INV-348: Negotiated transparent grounding pipeline
The conversion pipeline never invents values. It analyzes, matches against measured library primitives, surfaces every confidence score, and negotiates ambiguities with the user. The result is a gseed grounded in real measured data with explicit unknowns, not a hand-waved approximation. Novel because every other generative pipeline silently interpolates; GSPL refuses.

### INV-349: Lineage-tracked upload to gseed conversion with privacy tiers
Every conversion records a lineage edge from the original upload to the resulting gseed, with the user's chosen anonymity tier per Brief 077. The original upload is never re-published unless the user explicitly opts in. Novel as a substrate-level upload-to-creation provenance contract with privacy.

### INV-350: Constitutional refusal envelope for the conversion pipeline
The pipeline's refusals (living persons, copyrighted works, trademarked specifics, sacred-restricted symbols, weapon schematics, diagnostic claims) are substrate constitutional commitments that cannot be patched out. Novel as a substrate-level conversion ethics envelope.

## Phase 1 deliverables

- **15 input modalities** supported at v1.
- **Sandbox + metadata-strip + consent-classifier** at v1.
- **Multi-modal extraction engines** wrapped at v1.
- **Library-primitive grounding** with confidence scores at v1.
- **Candidate gseed composer with lineage** at v1.
- **Identity signing + privacy tier integration** at v1.
- **GSPL agent interface to the pipeline** at v1.
- **Constitutional refusal envelope** at v1.

## Risks

- **Extraction quality variance.** Mitigation: confidence scores are surfaced; low-confidence properties are unbound, not guessed.
- **Privacy leakage from uploads.** Mitigation: sandbox isolation + metadata strip + opt-in publication.
- **Refusal frustration.** Mitigation: refusals are explained transparently with the constitutional rationale; users see *why*, not just *no*.
- **Computational cost on T1.** Mitigation: tier-routable per Brief 075; heavy analysis runs T2/T3.

## Recommendation

1. **Lock the 15 input modalities** for v1.
2. **Build the negotiated grounding loop** as the substrate's signature interaction.
3. **Wire the constitutional refusal envelope** as a v1 substrate commitment.
4. **Sign every converted gseed** with full lineage to upload + library primitives.
5. **Expose the GSPL agent** as the primary user interface to conversion.

## Confidence
**4/5.** Architecture is clear; extraction quality at the long tail is the engineering work.

## Spec impact

- `inventory/conversion-pipeline.md` — new doc.
- `inventory/refusal-envelope.md` — new doc.
- New ADR: `adr/00NN-negotiated-grounding-pipeline.md`.
- New ADR: `adr/00NN-constitutional-refusal-envelope.md`.

## Open follow-ups

- Extraction engine selection per modality.
- Confidence threshold calibration.
- GSPL agent conversation design for negotiation loop.

## Sources

- Internal: Briefs 077, 086E, 086H, 086F, 088, 088A, 091.
