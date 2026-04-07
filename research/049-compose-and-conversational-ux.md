# 049 — Compose surface and conversational UX

## Question
How does the Compose surface — the chat-style interface where users describe what they want — actually work, and what UX patterns make it feel like *composing*, not *prompting*?

## Why it matters
Most generative tools today are "prompt boxes." The user types a prompt, gets a result, types another prompt, gets another result. There is no *compositional* feel: each interaction is standalone. GSPL is different — every interaction is part of a *lineage* the user can navigate, replay, and refine. The Compose surface must convey this without overwhelming the user. Get this UX right and GSPL feels like an instrument; get it wrong and it feels like every other prompt box.

## What we know from the spec
- Brief 029: planner+executor agent.
- Brief 032: adjective normalization.
- Brief 033: 5s/15s budgets.
- Brief 048: Compose is one of the six studio pillars.

## Findings — six UX principles

### 1. The conversation is the lineage
The chat history *is* the lineage view. Every user turn produces one or more lineage entries; every assistant turn corresponds to a generation. The chat is not a separate UI from the lineage browser — it's the same data, presented differently.
- **Hovering a chat message** highlights the corresponding lineage nodes.
- **Clicking a generated artifact** opens its lineage entry in the Lineage pillar.
- **Branching the conversation** creates a lineage branch; the chat shows a tree, not a flat list.

### 2. Latency masking via streaming previews
Brief 033 set a 5-second budget for first preview. The Compose surface achieves this with **progressive streaming**:
- **Token 1 (≤ 200ms):** acknowledgment + parsed intent ("Pixel-art knight, action stance, warm palette — searching exemplars...")
- **Token N (≤ 1.5s):** plan ("I'll generate 4 variants with different shield shapes and palette warmth.")
- **Frame 1 (≤ 3s):** first low-resolution preview placeholder.
- **Frame N (≤ 5s):** first full preview.
- **Frame N+M (≤ 15s):** all variants ready.

The user is *never* staring at a blank screen.

### 3. Modifier surfaces
Adjective normalization (Brief 032) is invisible by default but inspectable on demand:
- **The chat shows the user's words verbatim.**
- A small "↗" icon next to each interpreted modifier expands to show "you said *moody*; I read this as Energy=−0.4, Valence=−0.5, Brightness=−0.3. Adjust?"
- Adjustments are immediate and re-trigger generation.
- Per-user vocabulary overrides (Brief 032) accumulate from these adjustments.

### 4. Variant grids over single results
The default is *4-8 variants*, not one result. The user picks, dismisses, or refines.
- **Grid layout** with thumbnails sized to the engine (square for sprites, waveforms for music).
- **One-click pin** keeps a variant for later comparison.
- **One-click breed** uses the pinned variants as parents.
- **One-click critique** shows critic scores.
- **Keyboard navigation** for power users (arrow keys + space to pin).

### 5. Progressive disclosure of complexity
The Compose surface has three modes:
- **Conversational (default):** chat box, variant grid, modifier surfaces. ~5 controls visible.
- **Studio:** chat + lineage tree + critic dashboard side-by-side. ~20 controls visible.
- **Deep:** chat + lineage + critics + raw seed editor + operator history. ~50 controls visible.

Mode is a single setting; the user can toggle freely. The assistant adapts: in conversational mode it explains less; in deep mode it surfaces gene-level reasoning.

### 6. Reversibility and forgiveness
Every action is undoable. Every generation produces a lineage entry, so "undo" is just "navigate back."
- **Undo and redo** are global keyboard shortcuts.
- **Deleted variants are trashed, not destroyed** (recoverable for 30 days).
- **Project snapshots** at every "save" preserve the entire state.
- **The studio never silently overwrites** anything.

## Specific UX patterns

### Intent restatement
The assistant restates the user's intent in its first response: "Got it — pixel-art knight, action pose, warm palette. Generating now." This catches misinterpretations immediately.

### Reference upload
Users can drag-drop reference images, audio clips, or other seeds. The assistant treats these as *inspiration anchors* — they steer generation but are not directly copied.
- **Reference handling is explicit:** the assistant says "I'll use this as a style reference, not copy it directly. Want me to copy it directly?"
- **Reference content provenance is recorded** in the lineage.

### Inline editing of generated artifacts
The Forge pillar (Brief 048) is the engine-specific editor. Compose surfaces a "tweak this" button on every variant that opens it in Forge.

### Critique-driven refinement
Users can ask "make this better" without specifying what. The assistant:
1. Runs the critic ensemble.
2. Identifies the lowest-scoring critic.
3. Mutates along the gradient of that critic.
4. Shows "I improved silhouette readability from 0.4 to 0.7."

### Failure modes
- **Validation failure:** the assistant explains the failed invariant in plain language and proposes a fix.
- **Critic disagreement:** the assistant surfaces it: "Two critics disagree. Here's option A (high learned-critic score) and option B (high preference-critic score)."
- **Out-of-distribution intent:** the assistant says so: "I'm not confident on this — here are 4 wildly different interpretations."

## Risks identified

- **Chat-first UX excludes power users:** keyboard shortcuts and grid views are essential. Mitigation: Studio and Deep modes.
- **Streaming previews are visually busy:** placeholders flickering can be disorienting. Mitigation: smooth transitions; placeholder design with deliberate calm.
- **Variant grid is overwhelming:** 8 variants × 5 modifiers = decision paralysis. Mitigation: default to 4 variants; "show more" for additional.
- **Modifier inspection is buried:** the "↗" icon is small. Mitigation: accessibility audit; alternative entry points for the modifier surface.
- **Mode toggling resets state:** a user in Deep mode wouldn't want their layout reset on toggle. Mitigation: per-mode persistent state.
- **Reference uploads have IP risks:** copying without permission. Mitigation: provenance recording; user is responsible for upload rights.

## Recommendation

1. **Adopt the six UX principles** in `architecture/compose-ux.md`.
2. **Conversation is the lineage view**, not a separate window.
3. **Streaming previews are mandatory** to meet the 5s budget.
4. **Modifier surfaces are inspectable on demand.**
5. **Variant grid (4-8 variants) is the default result presentation.**
6. **Three modes: Conversational, Studio, Deep.**
7. **Every action is undoable**; deleted is trashed.
8. **Intent restatement is the first assistant response** to every user turn.
9. **Reference uploads are explicit and provenance-tracked.**
10. **Failure modes have plain-language explanations** with proposed fixes.

## Confidence
**3/5.** The UX patterns are conventional for creator tools but unproven for the specific compositional-lineage feel GSPL is going for. The 3/5 reflects the high UX-test requirement before launch.

## Spec impact

- `architecture/compose-ux.md` — full UX architecture.
- `ux/streaming-previews.md` — streaming spec.
- `ux/variant-grid.md` — grid layout and interaction.
- `ux/modifier-surfaces.md` — adjective inspection UI.
- `ux/three-modes.md` — Conversational/Studio/Deep specification.
- New ADR: `adr/00NN-conversation-as-lineage.md`.

## Open follow-ups

- UX prototype of streaming preview latency masking.
- A/B test variant grid sizes (4 vs 6 vs 8).
- Build the modifier surface inspector.
- Decide on the keyboard shortcut map.
- Accessibility audit (Brief 050).

## Sources

- Figma's UX patterns for live multiplayer composition.
- Notion's conversational + structural duality.
- itch.io's variant-grid pattern for game previews.
- Internal: Briefs 029, 032, 033, 048, 050.
