# Brief 104 — The first-user experience: the critical first ten minutes

## Question

What does a new GSPL creator experience in their first ten minutes — from sign-in to first signed gseed — such that they cross at least three designed Woah Moments (Brief 080), encounter the substrate's grounding floor, fork an armory seed, and walk away with a personally-signed creation, without ever hitting a placeholder, a confusing constitutional refusal, or a flat onboarding video?

## Why it matters

The first ten minutes decide whether a creator believes the substrate's promise. Every Round 1–4 invention is invisible to a first-time user unless this path is choreographed. The Foundation Kernel from Brief 095 and the Woah Moments from Brief 080 only earn their keep if they appear in the right order at the right moment in the first session.

Comparable platforms' time-to-first-meaningful-action benchmarks: Figma ~3 minutes, Canva ~2 minutes, Blender ~30 minutes (and this is acknowledged as a problem), Notion ~5 minutes, Substack ~4 minutes, Roblox Studio ~10 minutes, GitHub ~6 minutes. GSPL's target: **first signed gseed in ≤ 8 minutes, first Woah Moment within 90 seconds**.

## What we know from spec

- Brief 080: the Woah Moments (first sprite, first lineage walk, first cross-engine breed, first federated render, first time machine).
- Brief 088A: the canonical seed armory as the substrate's first-person voice.
- Brief 089: the universal anything-to-gseed pipeline.
- Brief 095: the Foundation Kernel of 200 seeds.
- Brief 103: the composition graph viewer and provenance panel.

## Findings

### Finding 1: The first 90 seconds determine retention more than the next 90 minutes

Repeated industry data (Mixpanel benchmarks, RetentionEngine reports, public retention curves from Figma, Notion, Roblox Studio, Substack, Hugging Face) shows that creator-tool first-session abandonment is concentrated in the first 60–120 seconds. If the user hits a meaningful "this is different" moment in that window, retention to session 2 doubles or triples.

### Finding 2: First-action latency matters more than first-action complexity

Users tolerate complex creative environments (Blender, Houdini) when first action is **fast**. Users abandon simple environments when first action is **slow** (long forms, account verification before any UI). The Foundation Kernel armory must be visible and forkable on the first screen after sign-in, before any payment, account customization, or onboarding video.

### Finding 3: The Woah Moments must be honest, not performative

The first lineage walk only feels woah if the lineage is real — if it traces back to actual measured chemistry, actual material science, actual cultural attribution. A staged demo lineage that looks deep but isn't will feel like marketing the moment the user inspects it. The substrate's honesty *is* the magic.

### Finding 4: First constitutional refusal must be a teaching moment, not a wall

A user's first refusal will likely be accidental (e.g., they type a famous trademarked character name when forking a Foundation Kernel character). The refusal surface (INV-439) must teach them what the substrate does and doesn't do, suggest the creator-namespace alternative, and let them continue. A first session that ends in an unexplained refusal is a churned user.

### Finding 5: The first ten minutes need a designed end state

Most onboarding flows end in "you can do anything now, go explore." This is wrong — first sessions need a clear completion: a signed gseed, a confirmed save, a "your work is in your namespace" moment that makes the user feel they have created something durable. The signing event itself should feel ceremonial.

## Inventions

### INV-445 — The 8-minute critical path

A choreographed first-session path with explicit time budgets:

| Minute | Step | Designed Woah | Constitutional touchpoint |
|---|---|---|---|
| 0:00–0:30 | Sign in (SSO or passwordless), land on Foundation Kernel browser | — | Privacy posture visible |
| 0:30–1:30 | Browse Kernel; click any seed to see provenance panel | **Woah #1: real lineage** (Brief 080 first sprite) | Grounding state visible |
| 1:30–3:00 | Fork a seed; name it; modify one parameter | — | Namespace assignment visible |
| 3:00–4:30 | Walk lineage of fork backward to source | **Woah #2: lineage walker animation** (Brief 080 first lineage walk) | Forever-signed-by edges visible |
| 4:30–6:00 | Render the fork in two style adapters; see invariants preserved | **Woah #3: cross-style coherence** (Brief 080 cross-engine breed) | Style invariant check |
| 6:00–7:00 | Sign the fork to user namespace; receive forever-signed-by acknowledgment | — | Signing ceremony |
| 7:00–8:00 | First gap: agent surfaces an ungrounded field; user picks negotiate / fetch / unbound | — | Gap-surfacing in action |

If the user hits all four within 8 minutes, they have personally seen: lineage, grounding, cross-style coherence, signing, gap-surfacing, and creator namespace. They have crossed the threshold.

### INV-446 — The Kernel-first landing screen

The post-sign-in landing is the Foundation Kernel browser, not a dashboard. 200 seeds organized by category, filterable, searchable. Each seed has a "fork in one click" affordance. No tutorial overlay. The seeds themselves are the teaching surface.

### INV-447 — The signing ceremony

When a user signs their first gseed under their identity, the studio renders a brief animation (≤ 2 seconds) showing:

- The seed entering the user's namespace.
- The forever-signed-by edge being created.
- The lineage to the upstream Kernel seed visible.
- A confirmation: "This work is yours. It cannot be erased without preserving your credit."

The animation is celebratory but bounded — no skip required. It happens once, the first time.

### INV-448 — The first-refusal teaching card

The first time a user encounters a constitutional refusal, the surface is augmented:

- Standard refusal explanation (INV-439).
- Plus a teaching paragraph: "This is one of GSPL's 13 constitutional commitments. You can read the full list, see why each one exists, or always work in your creator namespace where the rule is relaxed."
- Plus an example of what the refusal would have produced if the user had stayed within bounds.

The first refusal teaches the substrate's honesty rather than feeling like a block.

### INV-449 — The first ungrounded field as a feature

Users will hit an ungrounded field early because the Foundation Kernel is composed honestly. The first time this happens, the gap-suggestion panel (INV-443) is augmented with a brief explanation:

- "This field is not grounded yet — the substrate doesn't know its value with confidence. Other tools would silently guess. GSPL never guesses. Here are your options."

This turns what would feel like a flaw in a competitor into a Woah Moment.

### INV-450 — The 8-minute success metric

Every first session is measured against the INV-445 path. Success is defined as completing all 7 steps within 8 minutes. The metric is:

- Tracked anonymously per session.
- Reported in a `first-session://` aggregate gseed monthly.
- Used to tune the path (without ever bypassing constitutional surfaces).

If the success rate drops below threshold, the path is reviewed, not bypassed.

### INV-451 — The "what you made" persistent panel

After the signing ceremony, the user's namespace becomes a persistent left-rail panel showing every gseed they have ever signed, lineage-walkable, exportable, federated if they choose. This panel is the user's creative home and replaces the typical "files" sidebar.

### INV-452 — Designed exit at 10 minutes, not 8

The 8-minute path is the critical floor; the designed full first session ends at ~10 minutes with the user having created a second seed (a derivative or a fresh fork) and seeing the federation publish option. The 9th and 10th minutes are reserved as "do whatever you want" — explore freely after the spine of the experience is complete.

## Phase 1 deliverables

**Months 0–2**
- INV-446 Kernel-first landing screen.
- INV-451 user namespace panel.
- 8-minute path infrastructure (timing, metrics, anonymous reporting).

**Months 2–4**
- INV-447 signing ceremony.
- INV-445 critical path with all 7 steps wired through to real Kernel data.
- INV-448 first-refusal teaching card.

**Months 4–6**
- INV-449 first ungrounded field surface.
- INV-450 success metric reporting.
- INV-452 designed full first session.
- First-cohort user testing against the 8-minute target.

## Risks

- **Kernel not ready in time.** Mitigation: the path is gated on Brief 095's Kernel ship; first session cannot launch before Kernel v0.1.
- **Style adapter quality blocking Woah #3.** Mitigation: at least 5 adapters must be at full Brief 096 acceptance before first session opens; degrade gracefully if not.
- **Refusal teaching card feeling preachy.** Mitigation: copy is plain and brief, not lecturing; full constitutional list is one click away, not in your face.
- **Signing ceremony feeling gimmicky.** Mitigation: ≤ 2 seconds, no skip required, happens once. Test with first cohort and tune.
- **8-minute target feels artificial.** Mitigation: 8 minutes is a measurement target, not a UX constraint; the path can take longer for some users without failure.

## Recommendation

**Adopt INV-445 through INV-452.** The 8-minute critical path is the single most important UX decision Round 5 makes. Treat it as the spine of the entire studio experience and refuse to launch foundation v1.0 until first-cohort testing shows the path completes for at least 70% of new users within 12 minutes (the soft floor; 8 minutes is the target).

## Confidence

**4/5.** The structure is sound and grounded in industry retention data. The main execution risk is achieving the 8-minute target with real Kernel content, which depends on Brief 095 and Brief 096 hitting their gates.

## Spec impact

Briefs 080, 088A, 089, 095, 096, 097, 103 gain eight new inventions (INV-445..452). No new substrate primitives. The 8-minute path becomes a launch gate in Brief 105.

## Open follow-ups

- A/B testing methodology for the path (without compromising grounding floor or constitutional surfaces).
- Returning-user experience design (first session for session 2, 5, 20).
- Mobile-first session adaptation.
- Internationalization of teaching cards.

## Sources

- Mixpanel and Amplitude product retention benchmarks.
- Figma, Notion, Roblox Studio, Substack first-session retention case studies.
- Blender community onboarding postmortems.
- Hugging Face Spaces and Diffusers first-touch metrics.
- Round 3 Briefs 078, 079, 080.
- Round 4 Briefs 088A, 089, 095, 097.
- Round 5 Briefs 095, 096, 103.
