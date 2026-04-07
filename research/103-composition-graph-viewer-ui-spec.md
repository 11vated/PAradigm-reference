# Brief 103 — Studio composition graph viewer and reference transparency UI

## Question

What is the concrete UI specification for the studio's composition graph browser, reference transparency panel, and constitutional refusal surface — such that every user can see, at a glance, what every gseed is composed of, where every value comes from, what is grounded, what is ungrounded, and why the agent refused anything it refused?

## Why it matters

Every Round 4 invention's credibility lives or dies in this UI. The grounding floor (INV-357), the lineage system (INV-356), the cross-engine character coherence contract (INV-344), the curation decision lineage (INV-385), the four-axis style metric (INV-388), the gap-surfacing UX contract (INV-398), the freshness metadata (INV-431), the conflict edge preservation (INV-415) — all of them only matter if a creator can actually see them in the studio without burrowing through six menus.

## What we know from spec

- Brief 079: studio IDE look-and-feel.
- Brief 088A: every armory seed carries its full composition graph as a learning surface (INV-346).
- Brief 091: 10-edge ontology, content-addressed nodes, lineage-preserving tombstones.
- Brief 097 INV-398: gap-surfacing UX contract.
- Brief 100 INV-415: edge-conflict preservation as visible feature.
- Brief 101 INV-423: tier-source labeling on every cached value.
- Brief 102 INV-431: freshness label on every `ref://`.

## Findings

### Finding 1: Graph viewers fail when they show too much at once

Every successful graph viewer in production (Figma's component tree, Houdini's node graph, Blender's geometry nodes, Substance Designer's graph, IDA Pro's flowgraph, Neo4j Bloom) uses progressive disclosure: show one focal node and a 1-hop neighborhood by default; let the user expand outward; collapse on demand. Showing all 200 edges of a complex armory seed at once produces an unreadable tangle.

### Finding 2: Color and typography carry the grounding state

The four response states (grounded / partially grounded / ungrounded / refused, INV-395) need distinct visual encoding. Color alone fails accessibility; the encoding should combine color + iconography + typography weight so the state is unambiguous even in grayscale or for color-blind users. Anchor the encoding to the platform visual identity (Brief 078).

### Finding 3: Provenance must be one click deep, not three

Houdini's "show parameter expression source" pattern is the gold standard — right-click any value and see exactly where it came from, all the way back to the source. GSPL's reference transparency panel must match this affordance: any value, one click, full provenance chain visible.

### Finding 4: Refusals must explain themselves with constitutional citations and creator-namespace alternatives

When the agent refuses a request, the surface must show:

- Which constitutional commitment was triggered.
- A plain-language explanation of why.
- The specific element of the request that triggered it.
- What creator-namespace alternative exists (if any).
- A path to appeal or escalate (governance review).

A refusal with no explanation is indistinguishable from a bug.

### Finding 5: Conflict edges should be presented as perspective, not error

When two federation peers disagree about an edge, the UI should present both as legitimate perspectives. The user picks which to compose against. This is not a degraded experience; it is a feature that competitors literally cannot offer because they are not federated.

## Inventions

### INV-436 — The composition graph viewer with progressive disclosure

The viewer's default state shows the focal gseed at center with its 1-hop neighborhood (direct compositions and direct references). Users expand outward by clicking edges; the layout re-flows. Maximum visible nodes is bounded (default 50) to prevent collapse. Search-and-jump lets users navigate large graphs by node name. The viewer remembers expansion state per gseed per user.

### INV-437 — The four-state visual encoding

Grounding state visualization, anchored to platform visual identity:

| State | Color | Icon | Typography |
|---|---|---|---|
| Grounded | Verified-green | Checkmark in circle | Regular weight |
| Partially grounded | Caution-amber | Triangle with checkmark | Regular weight, asterisk on ungrounded fields |
| Ungrounded | Caution-amber | Triangle with question mark | Italic |
| Refused | Refusal-charcoal | Octagon with hyphen | Bold |

Colors are accessible (WCAG AA compliant) and supplemented with icons so encoding survives grayscale.

### INV-438 — One-click provenance panel

Right-click any value in the studio → "Show provenance" → panel slides out showing:

- The value itself.
- Its grounding state.
- Its tier-source label (live / hot cache / warm / cold / partner-unreachable).
- Its freshness label.
- The chain of `ref://` and library primitives that ground it.
- The confidence score chain.
- The signing identities at every step.
- A "fork from this value" affordance.

### INV-439 — The refusal explanation surface

Every constitutional refusal renders as a card with:

- Plain-language headline ("This request would compose a trademarked named character in the foundation namespace.")
- Cited commitment ("Commitment #4: No trademarked-specific named gseeds in the foundation namespace.")
- The specific input that triggered the refusal.
- The substrate alternative ("You can compose this same mechanic with a creator-namespaced character; the substrate offers `move://` and `power://` primitives that match.")
- Path to appeal ("Open governance review for this refusal.")

Refusals are never just "I can't do that."

### INV-440 — Conflict edges as perspective UI

When the graph contains conflicting edges from different signers, the viewer renders both edges side by side with their signer identities. The user explicitly picks which perspective to compose against. The choice is recorded as a `perspective-pick://` gseed in the user's lineage so their composition history is reproducible.

### INV-441 — The lineage walker

A dedicated "walk lineage" mode that animates the composition graph backward from any seed: focal seed → its compositions → their compositions → their primitives → their references. The walker is bounded to a depth budget (default 6) and surfaces the full chain in a scrollable timeline. This is the "fork an armory seed and learn by watching the substrate think" UX from Brief 095.

### INV-442 — Freshness and partner status badges

Every `ref://` displays a badge showing:

- Partner of origin (with link to the partner's transparency report).
- Freshness label (live / recent / aged / stale / legal-hold).
- Tier-source label (live / cached).
- A click-to-refresh affordance subject to the per-query budget.

### INV-443 — The gap-suggestion panel

When a query produces ungrounded fields, the studio surfaces a gap panel suggesting how to ground them:

- "Fetch references from the British Library for Heian-era court costumes" (with a one-click trigger).
- "Upload a photo of the locket to negotiate properties" (link to the conversion pipeline).
- "Switch to a creator-namespace seed where this field can remain unbound" (with the constitutional alternative).
- "Mark the field unbound with confidence zero" (the explicit unbound option).

The gap panel is the practical operationalization of commitment #1 (no silent guesses).

### INV-444 — The composition graph fork affordance

Every node in the viewer has a "fork from here" button. Forking creates a creator-namespace gseed inheriting the focal node's composition with the user's modifications, recording the fork as a `refines` edge. The forked seed automatically credits the upstream creator via the `forever_signed_by` edge. This is the one-click learning surface from Brief 088A INV-346.

## Phase 1 deliverables

**Months 0–3**
- Composition graph viewer v0.1 with progressive disclosure (INV-436).
- Four-state visual encoding implemented across all studio surfaces (INV-437).
- One-click provenance panel (INV-438).

**Months 3–6**
- Refusal explanation surface (INV-439).
- Lineage walker (INV-441).
- Freshness and partner status badges (INV-442).

**Months 6–12**
- Conflict edges UI (INV-440) — requires real federation traffic from Brief 100.
- Gap-suggestion panel (INV-443).
- Fork affordance integrated with creator namespace (INV-444).
- Accessibility audit at WCAG AA.

## Risks

- **Visual complexity overwhelming first-time users.** Mitigation: progressive disclosure, default 1-hop view, hide-by-default for advanced affordances.
- **Performance under large graphs.** Mitigation: bounded visible nodes, server-side neighborhood queries, layout caching.
- **Refusal surfaces feeling like censorship.** Mitigation: every refusal cites the commitment and offers an alternative; the substrate's honesty is the trust anchor.
- **Provenance panel becoming a wall of text.** Mitigation: panel is structured (state, tier, freshness, chain) with progressive expand on each section.
- **Accessibility regressions.** Mitigation: WCAG AA gate before any UI ships; the four-state encoding combines color + icon + typography.

## Recommendation

**Adopt INV-436 through INV-444.** The composition graph viewer and provenance panel are the most important UI surfaces in the entire studio — they make every Round 4 invention visible. Build them first, before any other studio refinement.

The lineage walker (INV-441) is a designed Woah Moment per Brief 080 and should be polished to that bar.

## Confidence

**4/5.** The UI patterns are well-proven (Houdini, Figma, Blender, Substance Designer). The main execution risk is making composition graph viewing performant and accessible at the same time, which is a real engineering effort but bounded.

## Spec impact

Briefs 079, 080, 088A, 091, 097, 100, 101, 102 gain nine new inventions (INV-436..444). No new substrate primitives. `perspective-pick://` joins the user-namespace lineage schemes. Visual identity (Brief 078) constrains the four-state color palette.

## Open follow-ups

- Mobile / tablet adaptation of the composition graph viewer.
- Keyboard navigation for accessibility.
- High-density 4K display optimization.
- Internationalization of refusal explanation copy.
- User testing with first-cohort creators to validate progressive disclosure boundaries.

## Sources

- Houdini node graph UI documentation and community reviews.
- Figma component tree and instance swap UI patterns.
- Blender Geometry Nodes editor design retrospective.
- Substance Designer graph editor best practices.
- Neo4j Bloom progressive disclosure UI.
- WCAG 2.1 AA color contrast and non-color encoding guidelines.
- Round 3 Briefs 078, 079, 080.
- Round 4 Briefs 088A, 091, 095.
- Round 5 Briefs 097, 100, 101, 102.
