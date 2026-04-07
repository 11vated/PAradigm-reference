# 078 — Platform visual identity and design language

## Question
What does GSPL look like, sound like, move like, and feel like? What is the visual identity that makes a stranger glance at the screen and immediately know "this is GSPL" — and that makes the user inside the studio feel they are operating a cathedral instrument, not a configuration panel?

## Why it matters
Round 3 closed every architectural concession. The substrate is structurally unsurpassable. What's left is the difference between a powerful tool that nobody uses and a powerful tool people *want* to spend their nights inside. That difference is overwhelmingly aesthetic: visual identity, motion language, sound, typography, color, the *feel* of every interaction. Houdini is unloved partly because it looks like a control room. Blender's redesign 10 years ago doubled its adoption. Figma and Linear are billion-dollar companies whose core advantage over their competitors is taste. GSPL must enter the world with a visual identity as deliberate as Apple's first OS X transparency, as cohesive as Stripe's documentation, as reverent as Bret Victor's prototypes.

## What we know from the spec
- Brief 048: studio IDE design.
- Brief 049: marketplace UX.
- Brief 050: lineage walker UX.
- Brief 051: federation browser UX.
- Briefs 070, 074: positioning and sovereignty narrative.

## Findings — design principles

GSPL's visual identity is built on five principles. Each principle is a constraint on every visual decision the platform makes.

### 1. Lineage is the world model
The substrate's structural truth is that everything is descended from something. The visual identity makes that visible in every screen. The user is always able to see "where this came from" without an explicit query. The lineage is rendered as living, branching, breathing graph that ambient-animates when the user's attention rests on it. It is not a debug view; it is the **primary world model** that other panels overlay onto.

### 2. Substrate over chrome
GSPL is the opposite of skeuomorphic. There are no fake wood panels, no fake metal sliders, no fake paper notebooks. The interface is honest about its substrate-ness: every surface declares "I am a content-addressed, signed, lineage-bearing object" through its visual treatment. Hashes appear as small, beautiful, color-coded glyphs. Signatures glow faintly when fresh. Forks branch visibly. Federation peers are visible as named, faintly luminous nodes at the periphery of the workspace.

### 3. Time is visible
Every gseed has a history. The interface makes time legible: timestamps are typographic, lineage edges age (saturate over time), recent edits leave a soft trail that fades. The "time machine" (Brief 071) is not a hidden feature; it is the **default reading mode** for any artifact — the user can scrub time without leaving their current view.

### 4. Federation is ambient, not modal
The federation is always present in the periphery. The user always feels the rest of the network — whose work is nearby, whose compute is offering itself, whose marketplace listings are new — without being interrupted. The studio is single-player by default but never feels alone.

### 5. Cathedral, not control room
The studio is reverent. It uses generous whitespace, deep contrast, restrained color, and slow, considered motion. Nothing is loud. Nothing is gamified. There are no badges, no streaks, no notification dots demanding the user's attention. The studio assumes the user is doing serious creative work and acts accordingly. **The studio is quiet so the work can be loud.**

## Findings — color system

### Primary palette
GSPL's primary palette is built on three "substrate colors":

- **Substrate Ink** — `oklch(0.18 0.02 260)`. The deep base color of every studio surface. Not pure black; a barely-blue near-black with a slight cool cast. Resembles deep ocean at night. This is the canvas color and the dominant tone.
- **Substrate Bone** — `oklch(0.96 0.01 80)`. The light-mode equivalent. A warm near-white with a slight cream cast. Resembles aged paper or unbleached cotton.
- **Substrate Lineage** — `oklch(0.72 0.18 145)`. A muted but luminous chartreuse-to-jade, used for lineage edges, signatures, and "this is alive and trustworthy" affirmations. This is GSPL's signature color — instantly recognizable.

### Accent palette (semantic)
Six accents, each with semantic meaning. None are arbitrary brand colors:

- **Pulse Red** — `oklch(0.65 0.22 25)` — recent edits, breaking changes, AUP violations.
- **Bloom Magenta** — `oklch(0.68 0.22 340)` — derived works, royalty flow, breeding events.
- **Coda Cyan** — `oklch(0.78 0.16 220)` — federation events, peer activity, network health.
- **Embers Amber** — `oklch(0.78 0.18 75)` — compute-in-progress, simulation running, training jobs.
- **Strata Indigo** — `oklch(0.55 0.18 280)` — provenance and authorship attestation.
- **Veil Lavender** — `oklch(0.78 0.10 305)` — anonymous publications and tier-3-and-above authorship.

### Color science commitments
- All colors are specified in **OKLab/OKLCH** (perceptually uniform), never sRGB hex codes. This is the same color science (Brief 021) the sprite engine uses internally.
- All palettes pass **WCAG AAA** contrast ratios for body text on substrate base colors.
- All palettes are paired with **scientifically chosen complement palettes** for protanopia, deuteranopia, and tritanopia color blindness — not as a toggle, but as parallel themes the user picks once at onboarding.
- All gradients are perceptually uniform OKLCH interpolations, not RGB.
- Dark mode and light mode are **first-class siblings**, not theme variants. The substrate's signature look exists in both.

## Findings — typography

### Type system
- **Display:** **Söhne Breit** (alt: **Inter Display**) at heavy weights for hero numbers, gseed IDs, and mark-of-authorship moments. The visual signature of GSPL's headers.
- **UI:** **Inter** (variable axis) for all interface text. Battle-tested, accessible, free, beautiful.
- **Mono:** **JetBrains Mono** (with ligatures off in code, on in identifiers) for hashes, addresses, signatures, parameter names. The mono face is treated as **first-class typography**, not relegated to dev tools.
- **Reading:** **Source Serif 4** for long-form content — brief reading, ADRs, documentation, lineage commit messages.

### Type scale
A perceptual scale (1.250 ratio) anchored at 16px UI / 18px reading. Headings step up; captions step down. Every step is in the OKLCH-paired color and weight system.

### Numerals
**Tabular figures everywhere** — every number column lines up. Hex hashes are shown in 4-character chunks with hair spaces. Timestamps are shown in ISO-relative form ("2 days ago" / "2026-03-12") that the user can switch globally.

## Findings — motion language

### Motion principles
- **Slow when serious, fast when reactive.** Lineage walks animate in 600ms; clicks respond in 80ms. Never the reverse.
- **Eased, never linear.** Every animation uses cubic-bezier or spring physics. Substrate Ink uses a custom ease called "Substrate" — a slow start, fast middle, slow end with slight overshoot.
- **Particles are real.** Where motion suggests particles (e.g., a breeding event), they are simulated with a small particle solver, not faked with CSS keyframes. The substrate dogfoods its own particle library (Brief 084).
- **Time scrubbing is direct manipulation.** Holding shift while moving the cursor scrubs lineage time across whichever artifact the cursor is over. No modal, no panel.
- **Reduced-motion is a first-class theme.** Users with vestibular sensitivities get a substrate-coherent alternative, not a degraded version.

### Signature motion: the lineage breath
The lineage graph **breathes** when idle — a 4-second sine-wave gentle pulse where freshly-created edges glow slightly more than ancient ones, then fade back. This is GSPL's signature ambient motion and instantly recognizable in any screenshot or video.

## Findings — sound design

### Sound principles
- **The studio is quiet.** No constant ambient hum, no notification sounds, no UI clicks by default. The user can opt into a subtle sound layer.
- **Sounds are real.** Where sounds exist, they are real recorded sources processed in OKLab-equivalent audio space (Bark scale), not synthesizer beeps. A "fresh signature" sound is a real bell struck in a real room.
- **Sounds are tied to substrate events**, not UI events. A fork happening in a peer's session can be heard if the user has federation audio on. A render completing has a distinctive sound. A new lineage attestation has its own.
- **Sound is composable.** Users can layer their own substrate sound packs from the marketplace, each one a gseed with full provenance.

### Signature sound: the substrate hum
A barely-audible 60Hz sub-bass with slow harmonic shimmer that the user can opt into. When federation activity rises, the hum gains harmonic content. When their gseed is forked by a peer, a subtle high overtone joins. The hum is the user's ambient awareness of the network, audible like wind.

## Findings — iconography

### Icon system
- **Custom icon library**, not a third-party set. GSPL's icons are recognizably its own.
- **Drawn at multiple weights** (1, 1.5, 2px stroke) and **multiple sizes** (16, 20, 24, 32, 48, 64, 96, 128) — never auto-scaled.
- **Geometric but hand-tuned.** Built on a 24px grid with hand-corrected curves at small sizes for crispness.
- **Lineage-aware icons.** Some icons (lineage node, federation peer, gseed) animate when the underlying state is active.

### Signature icon: the gseed glyph
A stylized double-helix-meets-ring shape that represents a gseed. Always shown in Substrate Lineage color when fresh, fading toward Substrate Bone as the gseed's age increases. The glyph appears wherever a gseed is referenced and is the most-displayed icon in the entire interface.

## Findings — language and tone

### Voice principles
- **Plainspoken, never marketing.** "Render finished" not "Your masterpiece is ready!"
- **Honest about uncertainty.** "Confidence: 0.84" not "AI-powered analysis."
- **Reverent toward the user.** The studio addresses the user as a peer, not a customer. No "Welcome back, creator!" — just "12 gseeds since Tuesday."
- **Substrate-literate.** The language uses gseed, lineage, federation, attestation, signature, fork, breed, critic, peer. The user is taught these terms in onboarding and they become part of their vocabulary.
- **Never gamified.** No streaks. No XP. No badges. No leaderboards (except optional federation reputation, which is opt-in).

### Signature phrase: "Forever signed."
Every gseed bears a small label at the bottom-right of any preview: **"Forever signed by [author]"** in Substrate Lineage color, with a faint glow when the signature is fresh. This is GSPL's catchphrase. Visible everywhere. Unmistakable.

## Findings — visual identity off-platform

### Brand applications
- **Logo:** the gseed glyph with the wordmark "GSPL" in Söhne Breit beside it, locked-up in three orientations.
- **Wordmark:** "Paradigm" in display weight, "GSPL" in display weight, "Engine" in regular. Together: "Paradigm GSPL Engine."
- **Tagline:** "The substrate where things come from."
- **Marketing site:** monochrome dark substrate with single accent of Substrate Lineage; hero animation is the lineage breath.
- **Documentation:** dark substrate with serif body text and tabular code samples; the docs feel like a philosophy book published by MIT Press.
- **Social and video:** consistent application of the substrate palette, lineage motion, and signature phrase.

## Findings — what makes this feel decisively GSPL

Three signature elements together create an instantly recognizable identity:

1. **The lineage breath** — the 4-second ambient pulse on the lineage graph.
2. **Substrate Lineage color** — the chartreuse-jade glow on every signature and lineage edge.
3. **"Forever signed by"** label on every artifact preview.

A user who has spent any time in GSPL will recognize these three elements in any screenshot, even at thumbnail size, even years later. This is the visual fingerprint.

## Inventions

### INV-300: Lineage breath as ambient world model
The lineage graph is the primary world view of the studio, and it breathes — animating with a 4-second sine wave that emphasizes recent edges and fades older ones. This is the interface's signature motion and the user's continuous awareness of how their work has come to be. Novel because no creative tool treats lineage as an ambient, always-visible, animated world model.

### INV-301: Federation-as-peripheral-presence
Federation peers, marketplace activity, and compute lending are visible at the periphery of the workspace as named luminous nodes, never modal, never demanding attention. The user is always aware of the network without being interrupted by it. Novel because every social/multiplayer creative tool currently uses notifications, dots, banners — modal interruptions. GSPL uses ambient peripheral presence.

### INV-302: Substrate-event-tied soundscape
Sound is tied to substrate events (signature, fork, attestation, render complete, peer fork) not UI events (button click, notification). The user's auditory awareness mirrors the substrate's actual state. Sound packs are gseeds with full provenance. Novel because no creative tool treats sound as a substrate-event channel composable through the marketplace.

### INV-303: Forever-signed visible label as substrate constant
Every artifact preview, everywhere in the platform, carries the "Forever signed by [author]" label in Substrate Lineage color. The label is non-removable, non-customizable, and the same across all surfaces. It is the platform's permanent reminder that authorship is mathematically preserved. Novel as a substrate-constitutional UI element.

## Phase 1 deliverables

- **Color tokens** in OKLCH with WCAG AAA verification and 3 color-blindness-paired themes.
- **Type system** with Inter, JetBrains Mono, Source Serif 4, and a chosen display face (Söhne Breit license or open alternative like Inter Display).
- **Custom icon library** drawn at multiple weights and sizes — minimum 200 icons at v1.
- **Motion library** with the Substrate ease and the lineage breath animation as named, reusable primitives.
- **Sound library** with substrate-event sounds and the substrate hum, all real recordings, all licensed CC-BY or owned.
- **Brand kit** with logo, wordmark, marketing site templates, and documentation theme.

## Risks

- **Display face licensing.** Söhne Breit is not free. Mitigation: use Inter Display as the open alternative; only license Söhne if a budget allows post-launch.
- **Sound design budget.** Real recorded sounds are expensive to commission. Mitigation: launch with a 12-sound starter library; expand via marketplace.
- **Motion can become precious.** Slow motion that users want to skip becomes friction. Mitigation: every animation is interruptible and the substrate detects reduced-motion preference.
- **The "lineage breath" must be performant.** A 4-second animation across thousands of nodes can stutter. Mitigation: GPU-accelerated, with LOD culling beyond 200 visible nodes.

## Recommendation

1. **Adopt the five design principles** as substrate-level commitments.
2. **Lock the color system** in OKLCH with full color-blindness pairings at v1.
3. **Lock the typography system** with open-license alternatives.
4. **Build the custom icon library** at v1 — 200 icons minimum.
5. **Implement the lineage breath, Substrate Lineage color, and Forever-Signed label** as the three signature identity elements at v1.
6. **Build the sound library** — 12 substrate event sounds + the substrate hum at v1.
7. **Hire or commission** a single design lead to own the visual identity end-to-end. (Realistic for a solo founder via fractional contract.)
8. **Publish the brand book** at v1 for federation peers and marketplace creators to extend in their own work.

## Confidence
**4/5.** The principles and palette are sound; the risks are budget and execution speed for a solo founder. Mitigation paths exist for each.

## Spec impact

- `design/visual-identity.md` — new doc.
- `design/color-system.md` — new doc.
- `design/typography.md` — new doc.
- `design/motion-language.md` — new doc.
- `design/sound-design.md` — new doc.
- `design/icon-library.md` — new doc.
- `design/brand-book.md` — new doc.
- Update Brief 048 to reference these design tokens as the substrate-mandated source of truth.
- New ADR: `adr/00NN-visual-identity-lock.md`.

## Open follow-ups

- License negotiation for Söhne Breit vs commitment to Inter Display.
- Motion library prototyping in WebGPU for the lineage breath at scale.
- Sound design commission for the 12 substrate event sounds.
- Color blindness pair palettes — formal validation against Coblis simulator.
- Custom icon library scoping (200 icons → 8 weeks of contract design work).

## Sources

- OKLab and OKLCH color science (Björn Ottosson).
- Inter font family (Rasmus Andersson).
- JetBrains Mono.
- Source Serif 4 (Adobe / Frank Grießhammer).
- Söhne Breit (Klim Type Foundry).
- WCAG 2.2 contrast ratio guidelines.
- Refactoring UI (Adam Wathan, Steve Schoger).
- Apple Human Interface Guidelines.
- Material Design 3.
- Linear, Figma, Stripe, Bret Victor design references.
- Coblis color blindness simulator.
- Internal: Briefs 021, 048, 049, 050, 051.
