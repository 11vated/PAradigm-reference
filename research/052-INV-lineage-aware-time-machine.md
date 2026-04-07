# 052 — INV: Lineage-aware time machine

## Question
Can GSPL invent a "time machine" UX that lets users navigate, branch from, and replay any past state of their project — leveraging the content-addressed lineage DAG to make this fast, deterministic, and free — in a way no other creator tool can?

## Why it matters
Conventional creator tools have *undo* (a flat stack) and *version control* (manual snapshots). Both lose context. GSPL has something better available for free: every state is content-addressed, every operation is a signed lineage edge, every random decision is HKDF-deterministic. This means *every state ever produced* is replayable at zero storage cost (just the seed hashes) and zero compute cost beyond replay. The time machine is the user-facing payoff of all that infrastructure.

## What we know from the spec
- Brief 017: content-addressed lineage with operator history.
- Brief 018: immutable operator IDs.
- Brief 042: signed identities.
- Brief 048: studio architecture with lineage pillar.

## Findings — the time machine in five capabilities

### 1. Navigate
The user can scrub through the project's history like a video timeline.
- **Timeline view:** horizontal axis is time (or generation count); vertical axis is lineage branches. Each node is a generation; each edge is an operator.
- **Scrub bar** at the top of the studio (always visible in Studio mode).
- **Left-arrow / right-arrow** moves to previous/next generation.
- **Jump-to-state** by typing a hash or selecting a node.
- **Navigation is reversible at zero cost** because nothing is destroyed.

### 2. Inspect
At any past state, the user can see exactly what existed:
- **All seeds** in the project at that generation.
- **The exact operator that was applied** to produce the next generation.
- **The exact operator parameters** (random seeds, mutation magnitudes, parent IDs).
- **The exact critic scores** at the time.
- **The user input** (prompt, modifier, button click) that triggered it.

This is *full reproducibility*, not just "git log" history.

### 3. Branch
From any past state, the user can branch a new line of evolution.
- **One-click "branch from here."**
- **The branch becomes a new lineage subtree** alongside the existing one.
- **The user can switch between branches** like git branches but with no working-tree conflicts (everything is content-addressed).
- **Branches can be named** for clarity.
- **Branches can be merged** via the cross-engine composition operators (Brief 028).

### 4. Replay
Any operator from any past state can be re-run with the same inputs and produce the same output. This is the determinism guarantee from Brief 001 + Brief 017 made user-visible.
- **"Replay this generation"** re-runs the exact operator with the exact rng_seed; produces the exact same output.
- **"Replay with different rng"** re-runs the operator with a fresh rng_seed; produces a sibling output.
- **"Replay with modified params"** lets the user tweak operator parameters and see what would have happened.
- **"Replay all"** re-runs the entire lineage from scratch — useful for migration to a new engine version (Brief 018).

### 5. What-if
The killer feature. The user picks a past state and asks "what if I'd chosen the *other* variant here?"
- **The system highlights the dismissed variant** at that generation.
- **The user can re-pick that variant** as the parent for everything downstream.
- **The downstream lineage is re-evolved** using the same operators with the new parent.
- **A side-by-side comparison** shows old timeline vs new timeline.

This turns evolution into *exploration* instead of a one-way trip.

## Storage and compute cost

### Storage
- **Lineage DAG entries:** ~1KB each. A 1000-generation project = ~1MB of lineage.
- **Seed files:** content-addressed; deduplicated; the same gene produces the same hash.
- **Rendered outputs:** stored only for pinned variants; transient outputs are regenerated on demand.
- **Total cost for a heavy power user:** < 100MB per project.

### Compute
- **Navigation is free** (just DAG lookups).
- **Inspection is free** (read from disk).
- **Branching is free** (create a new edge).
- **Replay costs whatever the original operation cost** (1-5 seconds for most engines).
- **What-if costs the replay cost × the number of downstream generations** (typically 10-100 seconds for a "what if" 20 generations back).

The studio surfaces these costs proactively: "What-if from generation 47 will take ~30 seconds and re-run 23 operations. Continue?"

## UX integration

The time machine has three entry points:
- **Scrub bar at the top** (always visible).
- **Lineage pillar** (full DAG view).
- **Right-click any artifact → "Show in time machine."**

The time machine respects the three modes (Brief 049):
- **Conversational:** simple back/forward; "what if" available as a button on dismissed variants.
- **Studio:** scrub bar + lineage tree + replay button.
- **Deep:** full DAG view + operator parameter editor + replay-with-modifications.

## Killer demos

- **"What if I'd kept the blue palette?"** — branch back to the palette decision, pick the other variant, watch downstream re-evolve.
- **"Replay this song with a different tempo seed."** — produces a sibling song.
- **"Show me how this character was made."** — full lineage timeline with operator labels.
- **"Reset to what it looked like an hour ago."** — navigate, then branch.
- **"Migrate this project to engine v2."** — replay-all with new operators; the system shows differences.

## Risks identified

- **DAG explosion:** millions of lineage entries get unwieldy. Mitigation: pruning rules from Brief 017; DAG compression; viewport-based rendering.
- **Replay determinism failures:** floating-point drift, missing engine versions. Mitigation: fixed-point kernel (Brief 001); engine version pinning (Brief 018); replay verification with hash checks.
- **What-if compute cost:** replaying many generations is slow. Mitigation: surface cost upfront; partial replay; cache intermediate results.
- **Visual complexity of the DAG view:** dense graphs are unreadable. Mitigation: collapsed views; focus+context; layout algorithms tuned for evolutionary trees.
- **User confusion:** "where am I?" Mitigation: persistent breadcrumbs; the current generation is always visible.
- **Data loss on prune:** pruned branches can't be replayed. Mitigation: pruning is opt-in and reversible within a window.

## Recommendation

1. **Adopt the time machine** as a v1 first-class studio feature in `architecture/time-machine.md`.
2. **Five capabilities** at v1: navigate, inspect, branch, replay, what-if.
3. **Always-visible scrub bar** in Studio and Deep modes.
4. **Cost preview before expensive operations** ("this will take 30s").
5. **Determinism enforced** via fixed-point kernel + version pinning.
6. **Replay verification** via hash checks; mismatches surface as errors.
7. **DAG view uses focus+context layout** for large lineages.
8. **What-if is the headline demo feature** for marketing materials.
9. **Branches are first-class** with naming and persistence.
10. **Pruning is opt-in and reversible**.

## Confidence
**4/5.** All the substrate exists (lineage, determinism, content addressing). The 4/5 reflects the unmeasured UX complexity of large DAG visualization.

## Spec impact

- `architecture/time-machine.md` — full time machine spec.
- `ux/scrub-bar.md` — scrub bar interaction.
- `ux/lineage-tree-view.md` — DAG visualization.
- `ux/what-if.md` — what-if interaction.
- `algorithms/replay.md` — deterministic replay algorithm.
- New ADR: `adr/00NN-time-machine-as-v1.md`.

## Open follow-ups

- Prototype the scrub bar and lineage tree at three sizes (100, 1K, 10K generations).
- Decide on the DAG layout algorithm.
- Empirically measure replay determinism on three engines.
- UX test the what-if interaction.
- Design the cost preview UI.

## Sources

- Apple's Time Machine (the inspiration, kind of, though it's much simpler).
- Pijul and Darcs (content-addressed VCS).
- Figma's version history feature.
- *The Visual Display of Quantitative Information* on time-series visualization.
- Internal: Briefs 001, 017, 018, 028, 042, 048, 049.
