# 079 — Studio IDE look-and-feel and interaction design

## Question
What does the GSPL Studio IDE actually look like on screen, where is every panel, how do users move through it, and what makes the daily-driver experience feel — not just functional — but inevitable?

## Why it matters
The studio is where every gseed is born. It is the user's home for creative work that must outlast the user. If the studio is competent but uninspiring, GSPL will be respected and ignored, like Houdini. If the studio is delightful and clear, GSPL will be loved and lived in, like Figma. The architectural wins of Rounds 1–3 only matter if the daily experience of using GSPL is one users seek out.

## What we know from the spec
- Brief 048: studio IDE design.
- Brief 050: lineage walker UX.
- Brief 049: marketplace UX.
- Brief 051: federation browser UX.
- Brief 078: visual identity, color, type, motion, sound.

## Findings — the studio's spatial model

The studio is **one continuous canvas**, not a collection of panels. The user is always inside a single coherent space; panels are foldable views *into* the canvas, not windows over it. The model is closer to Figma's infinite canvas than VSCode's gridded panels.

### The five regions

The canvas is divided into five regions whose layout is fixed but whose content scales. The user cannot reconfigure them — the studio's principle is **one true layout** that the user learns once and thereafter feels at home in any GSPL session anywhere.

```
┌────────────────────────────────────────────────────────┐
│  HEADER  ·  ◇ gseed-id  ·  forever signed by you      │
├────┬──────────────────────────────────────────┬────────┤
│ ╱  │                                          │  ╲     │
│ N  │                                          │  P     │
│ A  │                                          │  E     │
│ V  │             CANVAS                       │  R     │
│ I  │     (the work, fully)                    │  I     │
│ G  │                                          │  P     │
│ A  │                                          │  H     │
│ T  │                                          │  E     │
│ E  │                                          │  R     │
│    │                                          │  Y     │
├────┴──────────────────────────────────────────┴────────┤
│         LINEAGE BREATH (the world model)               │
└────────────────────────────────────────────────────────┘
```

1. **Header (top, 56px).** Gseed identity, forever-signed label, mode switches (preview/render/time-machine), federation peer presence ring at right.
2. **Navigate (left, 280px collapsible).** Project tree, library, breeds, marketplace bookmarks, all rendered as a single tree of substrate objects with hash glyphs and lineage edges shown inline.
3. **Canvas (center, fluid).** The work itself — gseed preview at full quality, with floating tool palettes that summon themselves where the cursor is.
4. **Periphery (right, 320px collapsible).** Federation peers, compute lenders, marketplace activity, fork notifications. Always visible, never modal.
5. **Lineage Breath (bottom, 120px expandable to full canvas).** The lineage graph for the current artifact, breathing. Click any node to scrub time. Drag any node to fork. The world model.

### Why this layout is non-negotiable

Every other creative tool gives users dockable panels and ends up with thousands of variant layouts that are individually broken. GSPL ships **one layout**. New users learn it in 90 seconds. Veterans never have to relearn it. Tutorials and screenshots from any era still look correct. The studio chooses **legibility across time** over per-user configuration.

## Findings — the canvas itself

### Canvas behavior
- **Infinite zoom.** From planet-scale (the lineage of all GSPL forever) down to a single pixel of a single sprite frame. The same gesture (Ctrl+wheel or pinch) zooms continuously across 12 orders of magnitude.
- **Always-on lineage edges.** Even at maximum zoom into a single artifact, faint lineage edges remain visible at the periphery, a reminder that this artifact exists in a network.
- **Direct manipulation everywhere.** Every parameter the gseed exposes is also a direct-manipulation handle on the canvas. Drag a character's arm, the IK solver runs and the gseed updates. Drag a fluid simulation's vortex point, the sim re-runs.
- **Real-time critic feedback.** A faint, dismissible critic panel floats at the bottom-right of the canvas, showing the critic ensemble's quality scores for the current state. Not modal, not loud, but always available.

### Floating palettes
Tool palettes summon themselves with a tap of `space` at the cursor location. They contain only context-relevant tools (a different palette for sprite editing vs simulation editing vs lineage walking). The palette is dismissed by clicking outside or tapping `space` again.

Palettes are **the only modal element in the studio**. Every other interaction is direct.

## Findings — the navigate region

### Navigate is a single tree
The left region is a single, navigable tree. Top-level nodes:
- **Recent** — the last 12 gseeds the user touched.
- **Library** — the user's full collection, lazily loaded, sortable by name/age/type/lineage-depth.
- **Breeds** — gseeds that are crosses of two or more parents.
- **Forks** — derivations the user has made.
- **Marketplace bookmarks** — saved listings.
- **Federation watch** — peers whose work the user follows.
- **Time machine** — saved time-machine snapshots.
- **Trash** — soft-deleted gseeds (with full recoverability).

Every node in the tree displays its **gseed glyph**, **forever-signed author**, **age (typographic)**, and a **2px lineage thread** that connects it to its parent if visible. Hover any node and the lineage breath in the bottom region highlights its full ancestry.

### No filenames
Gseeds do not have filenames. They have **gseed IDs** (a content-addressed hash) and **author-given titles**. The studio displays the title; the ID is a small glyph beside it. This decouples organization from filesystem assumptions and matches the substrate truth.

## Findings — the periphery region

### Periphery shows the network
The right region is a vertical scroll of "things happening on the federation that you might care about":
- **Peers active now** — federation members whose studio is open. Each shows their current focus (privacy-respectful: only the gseed type, not the content).
- **Forks of yours** — when a peer forks something you authored.
- **Marketplace activity** — listings recently added in categories you watch.
- **Compute offers** — peers offering GPU cycles, with rates in marketplace credits.
- **Critic disagreements** — gseeds where the critic ensemble has high variance, a signal of either high creativity or low quality.

Each item is **soft, non-demanding, dismissible**. The periphery is a window onto the network, not a notification center. If the user folds the periphery away, no information is lost; it remains queryable on demand.

### Federation presence ring
At the top-right of the header is a small **presence ring** — concentric arcs showing which peers are online, at-a-glance. Hovering reveals names; clicking expands to the full periphery. The ring **glows softly when activity rises**.

## Findings — the lineage breath region

### The world model at the bottom
The bottom region is the lineage graph for whatever artifact is currently in the canvas. It is not a sidebar feature; it is the **world model of the studio**. The user always sees how their current work came to be.

### Breathing animation
The lineage graph breathes with a 4-second sine pulse (Brief 078 INV-300):
- Recent edges glow at 100% Substrate Lineage saturation.
- Edges from the last hour: 80%.
- Last day: 60%.
- Last week: 40%.
- Older: 20%.

The wave makes the gradient *move* across the graph in time, so older work fades in and out subtly. This gives the user an unmistakable sense of "what's alive."

### Direct manipulation of time
- **Click a node** → the canvas jumps to that historical state.
- **Drag a node sideways** → fork the lineage at that point.
- **Hold shift over the graph** → scrub time across all visible artifacts simultaneously.
- **Right-click → "what changed?"** → diff view between two historical states.

## Findings — the modes

The studio has three operational modes, switchable from the header:

### Preview mode (default)
Real-time, low-cost rendering. The user iterates freely. Critic feedback is available but unobtrusive. This is where 95% of work happens.

### Render mode
The user has committed to producing a high-quality final. The studio slows down, displays progress, and may federate the job (Brief 075 INV-215) with explicit user permission. The result is a signed gseed at maximum quality.

### Time machine mode
The studio becomes read-only and the lineage breath expands to fill the lower 60% of the screen. The user navigates history, scrubs, branches, compares. Exiting time machine mode returns to preview mode at whatever point the user last viewed.

The mode is shown by a **single colored dot** in the header (cyan / amber / lavender). No banners. No popups.

## Findings — the breeding board

When the user enters breeding mode (drag two gseeds together on the canvas), a dedicated **breeding board** materializes in the canvas region. The board shows:
- The two parents at top-left and top-right.
- A row of slider controls for which traits to inherit from which parent.
- A grid of preview offspring (4 to 16, depending on canvas size) generated in real time.
- A "save offspring" button that turns any preview into a real signed gseed.

Breeding is **the most used feature in GSPL by design**. It is what makes the substrate generative rather than merely editable. The board is intentionally beautiful — it is the moment users learn what GSPL really is.

## Findings — the marketplace surface

The marketplace is not a separate app. It is a region the user can summon by clicking the marketplace bookmark in the navigate tree. When summoned, the canvas region becomes a **scrollable grid of listings** with the same lineage breath at the bottom. Listings are previewed in their actual lineage context.

Buying a listing **forks it into your library** as a new gseed with proper lineage and royalty flow set up automatically. There is no "downloads folder."

## Findings — onboarding

A new user opens the studio for the first time. Within 90 seconds they:

1. **See an empty canvas** with a single gseed waiting in Navigate: a starter sprite.
2. **A single line of text** at the top of the canvas: "This sprite came from somewhere. Click the lineage breath at the bottom to see."
3. They click. The lineage graph reveals the starter sprite's three ancestors — a primitive shape, a color palette, and a starter motion. The graph breathes.
4. **A second line:** "Now drag any of these ancestors back onto the canvas. You'll fork it."
5. They drag. A fork happens. The new gseed is **theirs**, signed with their identity. The studio shows: "Forever signed by you."
6. They are now inside GSPL and they understand the world model. **Total time: under 90 seconds.**

This is the entire onboarding. There is no tutorial overlay, no tooltips, no modal welcome. The studio teaches itself through its world model.

## Findings — keyboard model

GSPL is keyboard-first for everything that matters. The full keyboard map fits on a single A4 sheet:

- `space` — summon palette at cursor.
- `cmd+1..5` — switch focus between regions.
- `cmd+z / cmd+shift+z` — undo / redo (lineage-aware: undo is *forking back*, not destruction).
- `cmd+f` — find anything (gseed, peer, listing, lineage event).
- `cmd+t` — time machine mode.
- `cmd+r` — render mode.
- `cmd+b` — breeding board with currently selected gseeds.
- `cmd+l` — lineage walker focus.
- `cmd+p` — federation peer presence.
- `cmd+m` — marketplace.
- `cmd+,` — preferences.
- `?` — keyboard map overlay.

The map is **the same on every platform**, **never reconfigurable**, **always discoverable** via `?`.

## Findings — accessibility

- **Full keyboard navigation.** Every action achievable without a mouse.
- **Screen reader compatible.** All regions, all artifacts, all lineage edges have semantic ARIA labels.
- **High-contrast theme** as a sibling, not a hack.
- **Reduced motion theme** that swaps the lineage breath for static-with-color-aging.
- **Dyslexia-friendly font option** (OpenDyslexic or similar) as a sibling theme.
- **Full color-blindness palette pairings** (Brief 078).
- **Magnification compatibility** at all zoom levels.

Accessibility is **not optional and not relegated**. It is part of the visual identity contract.

## Inventions

### INV-304: One-true-layout studio with non-reconfigurable regions
The studio ships with one fixed five-region layout that is the same for every user, every project, every platform forever. No dockable panels. No layout presets. The studio's principle is legibility across time over per-user configuration. Novel because every other professional creative tool offers panel customization and pays the cost in fragmented user experience and broken tutorials.

### INV-305: Lineage breath as bottom-region world model
The lineage graph for the current artifact is permanently the bottom region of the studio, breathing with a 4-second sine pulse, manipulable directly. Not a sidebar, not a tab — the substrate's truth visualized as the screen's foundation. Novel because no creative tool treats lineage as a permanent, ambient, manipulable region of the workspace.

### INV-306: 90-second world-model onboarding
A new user reaches working understanding of GSPL's substrate model (lineage, fork, sign) in under 90 seconds with no tooltips, no modal overlays, and no tutorial. The studio teaches itself through one starter sprite and two lines of inline text. Novel as a substrate-coherent onboarding pattern; competitors typically use 5–30 minute interactive tours.

### INV-307: Direct-manipulation breeding board
Dragging two gseeds together summons a real-time grid of 4–16 offspring previewed in the canvas, with per-trait inheritance sliders and one-click commit-to-library. Breeding becomes the most-used and most-loved feature of the studio. Novel because no creative tool ships breeding as a primary first-class direct-manipulation interaction.

## Phase 1 deliverables

- **One-true-layout shell** with header, navigate, canvas, periphery, lineage breath regions.
- **Lineage breath rendering** at scale (up to 200 visible nodes at 60fps on T1 hardware).
- **Floating palette system** triggered by `space`.
- **Three modes** (preview / render / time machine) with substrate-coherent transitions.
- **Breeding board** with real-time offspring grid.
- **Marketplace surface** as a canvas overlay region.
- **90-second onboarding** with the starter sprite and two-line teaching.
- **Full keyboard model** with `?` overlay.
- **Full accessibility commitments** including reduced-motion theme.

## Risks

- **Lineage breath performance.** Animating thousands of nodes at 60fps on T1 hardware is non-trivial. Mitigation: LOD culling beyond 200 visible; switch to static-aging beyond 1000.
- **One-true-layout pushback.** Power users may demand reconfigurability. Mitigation: hold the line — the principle is exactly the value; reconfigurable studios become Houdini.
- **Direct manipulation discoverability.** Users may not realize every parameter is also a canvas handle. Mitigation: subtle handle dots appear on hover; the 90-second onboarding teaches the model.
- **Onboarding for users without a starter sprite.** What if Navigate is empty? Mitigation: every new identity ships with a starter library of 12 free gseeds across types.

## Recommendation

1. **Lock the five-region layout** as a substrate-level commitment.
2. **Build the lineage breath** as the first studio milestone — it is the visible identity.
3. **Build the breeding board** as the second milestone — it is the most-loved feature.
4. **Build the 90-second onboarding** as the third — it is the conversion driver.
5. **Hold the line on no panel customization.** This is GSPL's most controversial UX choice and the most important.
6. **Ship full accessibility** at v1, not as a follow-up.

## Confidence
**4.5/5.** The layout principles are tested in adjacent products (Linear, Figma, Notion). The unique-to-GSPL pieces (lineage breath, breeding board, 90-second onboarding) are higher risk but proportionally more rewarding. The remaining 0.5/5 is execution speed for a solo founder.

## Spec impact

- `design/studio-layout.md` — new doc.
- `design/keyboard-model.md` — new doc.
- `design/onboarding.md` — new doc.
- `design/accessibility.md` — new doc.
- Update Brief 048 to reference this brief as the authoritative layout source.
- New ADR: `adr/00NN-one-true-layout.md`.
- New ADR: `adr/00NN-lineage-breath-as-world-model.md`.

## Open follow-ups

- Prototype the lineage breath at scale on T1 hardware (Apple M2, Intel iGPU).
- Visual mockups for the five regions in OKLCH color tokens.
- Onboarding starter library design (12 starter gseeds across types).
- Screen reader testing protocol.
- Reduced-motion theme design.

## Sources

- Linear UI design philosophy and changelog.
- Figma's infinite canvas pattern.
- Notion's bidirectional graph as world model.
- Bret Victor — "Inventing on Principle" and "Drawing Dynamic Visualizations."
- Brad Cox and Joel Spolsky on UI consistency.
- Apple Human Interface Guidelines.
- WAI-ARIA Authoring Practices 1.2.
- Internal: Briefs 021, 048, 049, 050, 051, 078.
