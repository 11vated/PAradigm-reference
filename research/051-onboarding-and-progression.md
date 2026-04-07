# 051 — Onboarding and progression

## Question
How do new users go from "first launch" to "productive solo creator" to "GSPL power user" — without being lectured, without being overwhelmed, and without skipping the steps that matter (like backing up their key)?

## Why it matters
GSPL is conceptually deep. Engines, lineage, critics, federation, and the marketplace are all unfamiliar. A bad onboarding kills adoption before the user touches anything interesting. A good onboarding gets them generating something they're proud of in under 10 minutes — and quietly handles the must-do operational steps (key generation, recovery file, identity setup) without making them feel like compliance steps.

## What we know from the spec
- Brief 042: key management lifecycle.
- Brief 048: studio architecture.
- Brief 049: Compose UX three modes.

## Findings — five-stage progression

### Stage 1: First launch (0-10 minutes)
**Goal: produce one delightful artifact and have a backed-up identity.**

- **Splash screen** with three options: "Try a quick example", "Start from scratch", "Restore from backup".
- **The "quick example"** generates a sprite or music track from a single sentence. The user types "a friendly forest fox", presses enter, sees four pixel-art foxes within 5 seconds. *This is the demo.*
- **Identity creation** happens *after* the wow moment, framed as "let's save this work":
  - Display name (skippable).
  - Passphrase (mandatory; strength meter; minimum acceptable).
  - Recovery file (mandatory; the studio refuses to proceed without it being saved).
- **One-click backup** to USB or chosen cloud folder.
- **No "tour" pop-ups.** The studio surfaces tooltips on hover, not modal walls.

### Stage 2: First project (10-60 minutes)
**Goal: complete one small project end-to-end.**

- **The "Start a project" flow** asks one question: "What are you making?" and offers six default templates (game character, music loop, level, story scene, UI mockup, mixed). Selecting a template configures the engine, the workspace, and the initial Compose context.
- **The first project has guardrails:** the agent suggests next steps proactively. "You've made 4 sprites. Want to animate one?" "You've made an idle animation. Want to add a walk cycle?"
- **The agent introduces concepts in context.** First time the user sees the lineage view: a small popover explains it. Same for critics, variants, exports.
- **The first project export** is celebrated (small confetti animation; subtle but rewarding).

### Stage 3: Repeated use (1-10 days)
**Goal: build muscle memory.**

- **The studio remembers.** Last project, last engine, last variant grid layout — all restored.
- **The exemplar feedback loop** kicks in: the studio learns user preferences (Brief 031, Brief 032). The user notices (after a week) that defaults look more like *their* style.
- **Vocabulary overrides** start accumulating from "↗" interactions.
- **Progressive feature unlocks:** the studio surfaces one new feature per session ("Tip: try the lineage view to see how this evolved").
- **Optional tutorials** in the Help pillar — never modal, always discoverable.

### Stage 4: Power user (10-90 days)
**Goal: unlock advanced features and start producing publishable work.**

- **The user discovers Studio mode** (Brief 049) by trying it once.
- **Critic dashboards** become visible — the user starts reading scores.
- **Lineage navigation** becomes a habit.
- **First marketplace listing** flow — guided but not hand-held. The user understands what they're publishing because they made it.
- **Federation invite** arrives from a friend or community — opt-in, fully explained.

### Stage 5: Sovereign creator (90+ days)
**Goal: full mastery of the substrate.**

- **The user toggles Deep mode** when they want to.
- **They write their own custom critic ensemble weights.**
- **They publish to the marketplace regularly.**
- **They have a backup home server** running federation.
- **They know enough to be dangerous.**

## Tutorial system

GSPL's tutorial system has three layers:
- **Inline tooltips** — small explanations on hover, dismissable.
- **Discoverable tutorials** — short interactive walkthroughs in the Help pillar, never forced.
- **Long-form documentation** — written tutorials, video tutorials, community recipes.

No tutorial is *modal*. The user is never blocked from doing what they want.

## Anti-patterns deliberately avoided

- **Forced multi-step modals** at first launch. Onboarding is in the actual UI, not a wizard.
- **Empty states with no content.** Every empty state has a "try this" CTA.
- **Achievements/gamification.** GSPL is a tool, not a game.
- **Push notifications for "engagement."** The studio doesn't beg for attention.
- **Marketing-style "what's new" popovers.** Release notes are in Help, not in your face.
- **Forced account creation before value.** Identity is created *after* the first wow moment.

## Key onboarding metrics

The studio tracks (locally, not transmitted) onboarding completion to surface help:
- **Time to first artifact:** target ≤ 5 minutes.
- **Time to recovery file saved:** target ≤ 10 minutes.
- **First project completed:** target ≤ 60 minutes.
- **Returning the next day:** target ≥ 50%.
- **First federation peer added:** target ≤ 30 days for opted-in users.

These metrics inform UX iteration, not user-facing pressure.

## Risks identified

- **Recovery file friction:** users skip it given any chance. Mitigation: refusal to proceed past day 1 without it; clear consequences explained ("if you lose this, your work is irrecoverable").
- **First-launch latency:** local LLM cold start hurts the demo. Mitigation: ship a small embedded model that loads in <2s; full LLM warms in background.
- **Concept overload:** explaining lineage, critics, federation upfront kills momentum. Mitigation: just-in-time explanation; concepts introduced when relevant.
- **Template selection paralysis:** six options is too many for some, too few for others. Mitigation: A/B test 4 vs 6 vs 8 templates.
- **Power-user discoverability:** users who never leave Conversational mode never see the depth. Mitigation: gentle nudges at appropriate milestones; dedicated "explore more" surface.
- **Tutorial obsolescence:** tutorials reference UI that changes. Mitigation: tutorials versioned with releases; broken tutorials surfaced for community fix.

## Recommendation

1. **Adopt the five-stage progression model** in `architecture/onboarding.md`.
2. **First wow moment in ≤ 5 minutes**; identity setup *after*.
3. **Recovery file is mandatory before day 2** of use.
4. **No modal walls.** Onboarding is in-place.
5. **Six default templates** at launch (game character, music loop, level, story scene, UI mockup, mixed).
6. **Inline tooltips + discoverable tutorials**; no forced walkthroughs.
7. **Progressive feature unlocks** at most one per session.
8. **Local-only onboarding metrics** for UX iteration.
9. **First-launch model loads in ≤ 2s.**
10. **No engagement-style notifications** ever.

## Confidence
**4/5.** Onboarding is well-trodden in product design and the principles are clear. The 4/5 reflects the unmeasured local LLM cold-start latency and template selection.

## Spec impact

- `architecture/onboarding.md` — full onboarding spec.
- `ux/onboarding-flows.md` — first launch, first project, progression.
- `ux/tutorial-system.md` — three-layer tutorial spec.
- `ux/empty-states.md` — empty state catalog.
- New ADR: `adr/00NN-no-modal-walls.md`.

## Open follow-ups

- Build the first launch demo (sprite + music + level).
- A/B test template count.
- Decide on the embedded first-launch model.
- Build the recovery file enforcement flow.
- Plan the localization of onboarding (Brief 050).

## Sources

- Linear's onboarding (a strong reference for in-place introduction).
- Figma's "first design in 60 seconds" pattern.
- Notion's empty-state CTAs.
- *The Design of Everyday Things* on progressive disclosure.
- Internal: Briefs 031, 032, 042, 048, 049, 050.
