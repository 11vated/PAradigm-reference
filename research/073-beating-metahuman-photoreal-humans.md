# 073 — How GSPL beats MetaHuman at photoreal humans

## Question
Brief 065 conceded that "MetaHuman wins" at photoreal human creation. That concession was premature. How does GSPL surpass MetaHuman — Epic's photoreal-human-creator pipeline — using neural avatars, signed identity, lineage, federated likeness markets, and substrate-level composability that Epic structurally cannot replicate?

## Why it matters
Photoreal humans are the most demanding asset class in interactive media. Every game, film, and ad needs them; every creator wants to make them; the existing tooling is locked to AAA pipelines. If GSPL has a hole here, it cuts itself off from the entire human-character creation market. The right answer is not "we don't do humans"; the right answer is "GSPL does humans in a way Epic structurally cannot."

## What we know from the spec
- Brief 002, 003: shipped engines.
- Brief 008, 009: c2pa, watermarks.
- Brief 042: cryptographic identity.
- Brief 044: marketplace with lineage royalties.
- Brief 046: IP rights and licensing.
- Brief 047: zk anonymous publication.
- Brief 052: lineage time machine.
- Brief 071: differentiable substrate.
- Brief 072: neural rendering.

## Findings — MetaHuman's structural limits

MetaHuman Creator (Epic Games, 2021-) is a remarkable photoreal human pipeline that combines a face library, blendshape rigging, hair grooming, and clothing into a turnkey character generator. But it is locked into four architectural assumptions GSPL does not share:

1. **Closed face library.** MetaHuman's faces come from a fixed set of scanned heads that Epic owns. Users blend within the library; they cannot truly *generate* a new face from a description or a single photo. Epic's library is the artistic and identity ceiling.
2. **Rig-based, not neural.** MetaHuman uses traditional blendshape rigs. The rig is high-quality but doesn't learn from data; it can't be improved by users; it can't be composed with other rigs without engine surgery.
3. **No identity, no provenance, no royalties.** A MetaHuman face is a Maya/Unreal asset. There is no signed identity for the actor whose face was scanned; no royalty flow when the face is used; no cryptographic attestation that the user has rights to that likeness; no built-in c2pa marking.
4. **Single-engine binding.** MetaHumans are Unreal-native. Exporting to Unity, Godot, Blender, or anywhere else loses the rig and the texture quality.

These are not features Epic can add without rewriting MetaHuman. GSPL inherits none of them.

## Findings — what GSPL ships that MetaHuman can't

### 1. Neural avatars as substrate-native primitives
The last three years have produced neural avatar techniques that match or exceed scanned-head quality with a fraction of the data: Codec Avatars (Meta, 2018-2024), Gaussian Avatars (Qian et al. 2024), HumanRF, NeRF avatars, INSTA, MoFaNeRF, SMPL-X-based parametric body models, and the diffusion-based human generators (StableDiffusion human LoRAs, IDM-VTON for clothing). These can generate a photoreal head from a single photo, animate from a video reference, and re-render under arbitrary lighting.

GSPL ships these as **first-class engines on the substrate** (Brief 072 architecture). A human in GSPL is a gseed: signed, content-addressed, lineage-tracked, composable.

**Concrete win:** "Create a photoreal character that looks like a 40-year-old fisherman from Maine" is a prompt in GSPL. In MetaHuman it's manual blending within a fixed library, and the result will not actually look like a Maine fisherman because the library doesn't contain one.

### 2. Signed identity binding for likeness (INV-206)
Every face in GSPL can be cryptographically bound to its source identity. If the face is generated from a real person's photo, GSPL records:
- The source actor's signature (if they consented).
- The license they granted (L1-L5 from Brief 046).
- The royalty rate.
- The c2pa provenance chain.

This is a constitutional answer to deepfake concerns: real-person likeness is *only* usable in GSPL if the real person signed it. If they didn't, the substrate flags it as an unsigned likeness and the user has to declare it as fictional or research. This is structurally impossible in MetaHuman because MetaHuman has no identity layer.

**Concrete win:** Actors can license their likeness on the GSPL marketplace with cryptographic guarantee that they get paid every time their face is used. Game studios can guarantee they have rights to every face in their game. Both are impossible with MetaHuman.

### 3. Federated likeness marketplace
The likeness marketplace (Brief 044) is the killer commercial application of identity-bound humans. Actors, models, and ordinary people can mint signed likenesses; creators license them at L1-L5 tiers; royalties flow through lineage; the substrate guarantees the chain. This is a new economic primitive that Epic cannot offer because Epic does not federate, does not sign, and does not have a marketplace with lineage royalties.

**Concrete win:** A solo creator pays $50 to license a face from an actor, makes a game with it, the actor receives passive royalties on every download. No middleman takes 30%; the lineage-royalty flow is settled by the substrate.

### 4. Lineage of facial decisions
A character in GSPL has a full editing lineage — every change to nose, eye, jaw, expression, hair, clothing is a node. The user can scrub, branch, what-if, and replay (Brief 052). A MetaHuman is a current state with a save file; it has no decision history.

**Concrete win:** "Show me the version of this character from before the redesign" is a one-click navigation in GSPL.

### 5. Cross-engine breeding for character composition (Brief 014)
A face from one gseed, a body from another, motion from a third, clothing from a fourth, voice from a fifth — all composed via the substrate's naturality square (Brief 041 INV-103). The lineage records every contribution. MetaHuman composes a face with a fixed body library; it cannot mix arbitrary body and face sources.

**Concrete win:** Build a character whose face is from a generated portrait, body from a 3D scan, motion from a captured video, voice from a synthesized actor, clothing from a diffusion-generated design. All in one tool, all signed, all with lineage.

### 6. Differentiable avatar editing
GSPL's differentiable substrate (Brief 071, 072) lets users *describe* what they want and have the system optimize the avatar parameters. "Make this character look angrier" gradient-descents through the expression space. "Make this character match this reference photo" inverse-renders to recover the parameters. MetaHuman has manual sliders.

**Concrete win:** "Make her look more like Lupita Nyong'o in Black Panther" (with consent) is a one-line gradient match. In MetaHuman it's an artist tweaking sliders for an hour.

### 7. Neural rigging that learns from user content
GSPL ships an open neural rigger that trains on user-supplied motion capture or video. The rig improves with use. MetaHuman's rig is fixed; users cannot improve it.

**Concrete win:** A character that animates better the more videos you feed it. MetaHuman cannot do this.

### 8. Cross-engine export
A GSPL character exports to Unity, Unreal, Godot, Blender, Maya, glTF, USD with lineage and provenance preserved (Brief 065). MetaHuman is Unreal-first with limited export.

**Concrete win:** Make once, ship anywhere. MetaHuman locks you to Unreal.

### 9. Anonymous-but-signed character publication
A character creator can publish a face under a pseudonymous identity using Brief 047's zk publication. The likeness royalty flow still works, but the creator's real name is hidden. This protects vulnerable creators and is impossible in MetaHuman.

## What GSPL ships at each phase

### v1
- **Diffusion-based portrait engine** for 2D character generation at MetaHuman-comparable photometric quality.
- **Signed identity binding for portraits** (INV-206).
- **Lineage of character editing decisions**.
- **Marketplace for portrait licenses**.
- Honest scope: 2D portraits at v1, 3D at v1.5+.

### v1.5
- **3D Gaussian splat avatars** via open-weight implementations.
- **Neural avatar engine** (INSTA, MoFaNeRF, or successors) for animatable 3D heads.
- **SMPL-X body engine** for full-body parametric humans.
- **Cross-engine character breeding** (face + body + motion + voice + clothing).
- **Open neural rigger** trainable on user mocap.

### v2
- **Production neural avatars** matching MetaHuman quality.
- **Federated likeness marketplace** at scale.
- **Real-time neural avatar rendering** in studio.
- **Inverse avatar editing** ("match this reference") as primitive.
- **Voice + face joint generation**.

### v3
- **Full-body real-time neural avatars** at AAA quality.
- **Codec-Avatars-class fidelity** in fully open implementation.

## Inventions

### INV-206: Signed identity binding for likeness
Every avatar gseed carries a signed identity attestation: who consented to this likeness, under what license, with what royalty rate, with what c2pa chain. The substrate refuses to render or export an unsigned likeness without an explicit fictional-or-research declaration. This is a constitutional answer to deepfake concerns at the substrate level. Novel because no existing avatar pipeline has identity at the substrate.

### INV-207: Federated likeness marketplace with royalty lineage
Likenesses are listed on the marketplace with L1-L5 license tiers (Brief 046). Every use generates a royalty event that flows through the lineage to the original signer. The 10-hop royalty cap (Brief 044) applies. No platform fee. Novel because no avatar marketplace currently offers cryptographically-enforced royalty flow.

### INV-208: Composable neural rigger
The neural rig is a gseed; users can fine-tune it on their own mocap data. The rig improves with use and is shareable with provenance. Novel because all production riggers are static.

### INV-209: Inverse avatar editing
Differentiable rendering through the avatar substrate enables gradient-based reference matching: "make this character match this photo" or "make this expression match this video frame" become primitive operations. Novel as a substrate primitive (academic prototypes exist; production-grade integration does not).

## What MetaHuman still does better at v1

Honest accounting:
- **Production-grade rigs at AAA cinematic quality.** MetaHuman wins until v2.
- **Hair grooming pipeline.** MetaHuman wins; GSPL closes via diffusion + neural rendering at v1.5.
- **Cloth simulation on humans.** MetaHuman + Chaos win until GSPL ships the differentiable cloth from Brief 071.
- **Unreal pipeline integration.** GSPL exports cleanly but doesn't replicate the Unreal-native workflow.
- **Decade of artist familiarity** with rig topology.

These are time and data investments. The architectural ledger favors GSPL because GSPL has identity, lineage, federation, and marketplace primitives that MetaHuman cannot retrofit.

## The strategic claim

The deepfake era requires identity-bound likeness as a constitutional property of any human-creation tool. **GSPL's signed-identity substrate is not a feature; it is the only ethically defensible answer to AI human generation.** Every other tool is one viral incident away from regulatory disaster. GSPL is built around the answer from day one.

## Risks identified

- **Open-weight neural avatars are research-grade.** Mitigation: GSPL contributes to the open ecosystem; engages researchers; ships hybrid v1 (diffusion 2D first, neural 3D later).
- **Likeness marketplace requires actor adoption.** Chicken-and-egg. Mitigation: GSPL launches with curated actor partnerships; signed-identity is valuable enough that early adopters will participate.
- **Legal complexity of likeness licensing.** Right of publicity laws vary by jurisdiction. Mitigation: legal review per region; default to most restrictive.
- **Deepfake misuse.** Mitigation: signed-identity requirement at substrate; CSAM/NCII filters (Brief 061); c2pa on every output (Brief 058).
- **MetaHuman adopts AI features.** Probability: medium. Mitigation: signed identity and federated marketplace are constitutional, not features Epic can copy.

## Recommendation

1. **Reverse the Brief 065 concession.** GSPL competes natively at photoreal humans via neural avatars + signed identity + federated marketplace.
2. **Ship 2D portrait engine + signed identity at v1.**
3. **Launch likeness marketplace at v1.5** with curated actor partnerships.
4. **3D neural avatars at v1.5.**
5. **Implement INV-206 (signed identity binding) as a headline ethical and technical demo.**
6. **Engage actors' guilds, modeling agencies, IP lawyers** on likeness licensing.
7. **Position as "the only ethical AI human creator"** in marketing.
8. **Marketing language**: "MetaHuman gives you their faces. GSPL lets you license real people's faces with their consent and royalties."

## Confidence
**4/5.** The technical trajectory is well-established; the legal and ethical positioning is the strongest in the market. The 4/5 reflects honest uncertainty about open-weight neural avatar quality at v1.5.

## Spec impact

- `architecture/avatar-substrate.md` — new doc.
- `architecture/likeness-marketplace.md` — new doc.
- Update Brief 065 to remove the MetaHuman concession.
- New ADR: `adr/00NN-signed-identity-binding-for-likeness.md`.
- New ADR: `adr/00NN-federated-likeness-marketplace.md`.

## Open follow-ups

- Engage SAG-AFTRA and equivalent on actor likeness licensing.
- Pick v1.5 neural avatar backbone (INSTA, MoFaNeRF, GaussianAvatars).
- Build INV-206 prototype.
- Legal review of likeness licensing per jurisdiction.
- Curate v1.5 actor partner program.

## Sources

- Lombardi et al., "Deep Appearance Models for Face Rendering" (2018) — Codec Avatars.
- Qian et al., "GaussianAvatars" (2024).
- HumanRF and follow-up works.
- Loper et al., "SMPL: A Skinned Multi-Person Linear Model" (2015).
- IDM-VTON and diffusion-based virtual try-on literature.
- Epic Games MetaHuman documentation.
- SAG-AFTRA AI provisions in 2023 contracts.
- Internal: Briefs 002, 003, 008, 009, 014, 042, 044, 046, 047, 052, 058, 061, 065, 071, 072.
