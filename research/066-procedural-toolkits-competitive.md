# 066 — Procedural toolkits: Houdini, Blender Geometry Nodes, WFC

## Question
GSPL is positioned as the next generation of procedural creation. The current generation is Houdini (commercial procedural king), Blender Geometry Nodes (open-source procedural in a DCC), and Wave Function Collapse / constraint-based tile systems (academic + indie procedural). How does GSPL relate, what does it absorb, and where is it structurally different?

## Why it matters
Procedural creation is GSPL's intellectual lineage. Houdini SOPs, Geometry Nodes, and WFC are the proven techniques the field knows. GSPL must show it understands them deeply enough to absorb their best ideas, while articulating what is *fundamentally new* about a generative-substrate approach. Without this, GSPL looks like "Houdini with AI bolted on" instead of a paradigm shift.

## What we know from the spec
- Brief 002: shipped engines include procedural pipelines.
- Brief 015: gseed format is content-addressed, parameter-based.
- Brief 026: deterministic kernel.
- Briefs 036-041: novelty, evolution, DQD.

## Findings — competitor profiles

### Houdini (SideFX)
**Operator:** SideFX; commercial; free Apprentice and Indie tiers.
**Architecture:** Node-based procedural DCC; SOPs (Surface Operators), DOPs (Dynamics), VEX scripting, HDA (Houdini Digital Assets).
**Strengths:**
- Industry-standard for procedural VFX, terrain, simulation.
- Node graph is the gold standard for procedural workflows.
- HDAs are reusable, parameterized procedural recipes.
- Deep simulation: pyro, fluids, rigids, cloth, hair.
- VEX gives low-level control.
- Used in every major film studio.

**Weaknesses:**
- Commercial; expensive at the indie tier let alone production.
- Steep learning curve.
- Closed source.
- AI features minimal; ML SOPs are basic.
- No first-class lineage of decisions; the node graph is the workflow but not the *history*.
- No marketplace for HDAs comparable to engine asset stores.
- No federation; HDAs are file-based.

### Blender Geometry Nodes
**Operator:** Blender Foundation; open source (GPL).
**Architecture:** Node-based procedural geometry inside Blender; Python scripting; integrates with rest of Blender.
**Strengths:**
- Free and open source.
- Excellent integration with Blender's modeling, sculpting, animation, and rendering.
- Active community; rapid iteration.
- Python API for extensibility.
- Strong for procedural modeling, scattering, and instancing.

**Weaknesses:**
- Less powerful than Houdini for simulation.
- Locked to Blender; no headless or standalone mode for the node graph.
- AI features mostly community plugins.
- No lineage tracking.
- No marketplace for node groups beyond community sharing.

### Wave Function Collapse and constraint-based tiling
**Operator:** academic + indie; multiple implementations (Maxim Gumin's original, Oskar Stålberg, GitHub forks).
**Architecture:** Constraint propagation over a tile grid; collapses possibilities to a consistent solution.
**Strengths:**
- Elegant theoretical foundation.
- Deterministic with seed.
- Used in commercial games (Caves of Qud, Bad North, etc.).
- Open implementations everywhere.
- Composes with other procedural techniques.

**Weaknesses:**
- Academic, not productized; tooling is sparse.
- Hard to author tile sets and constraints.
- No quality control beyond hand-tuned constraints.
- No identity, no provenance, no marketplace.

## Axis-by-axis comparison

| Axis | Houdini | Geo Nodes | WFC | GSPL |
|---|---|---|---|---|
| Open source | ❌ | ✅ | varies | ✅ |
| Procedural depth | 10/10 | 7/10 | 6/10 (narrow) | 7/10 v1 → 9/10 |
| Simulation | 10/10 | 6/10 | ❌ | varies by engine |
| AI integration | 2/10 | 2/10 | ❌ | 10/10 |
| Lineage of decisions | ❌ | ❌ | ❌ | ✅ |
| Reusable units | HDA | node groups | tile sets | gseeds |
| Marketplace | minimal | community | none | ✅ |
| Provenance | ❌ | ❌ | ❌ | ✅ |
| Identity | ❌ | ❌ | ❌ | ✅ |
| Federation | ❌ | ❌ | ❌ | ✅ |
| Critique loop | ❌ | ❌ | ❌ | ✅ |
| Evolution operators | ❌ | ❌ | ❌ | ✅ |
| Determinism | partial | partial | ✅ | ✅ |
| Content-addressed | ❌ | ❌ | ❌ | ✅ |
| Conversational interface | ❌ | ❌ | ❌ | ✅ |
| Cross-modal | partial | partial | ❌ | ✅ |

## What GSPL absorbs

### From Houdini
- **HDA pattern → gseeds**: a parameterized procedural recipe that can be reused, shared, and composed. GSPL's gseed format (Brief 015) is the spiritual successor with content-addressing, signed identity, and lineage built in.
- **Node graph as workflow** → modifier surfaces (Brief 049) and the lineage DAG (Brief 052). GSPL's user does not write nodes by hand; the agent does, and the user inspects and modifies.
- **VEX-style low-level access** → engine plugin API. Power users can drop down to the engine layer.
- **Simulation depth** → engine plugin model lets GSPL ship simulation engines (cloth, fluid, rigids) in v2/v3.
- **HDA marketplace** → GSPL marketplace is the spiritual successor with provenance, royalties, and federation.

### From Blender Geometry Nodes
- **Open-source DCC integration** → GSPL ships a Blender plugin and treats Blender as a first-class export target.
- **Node group reusability** → modular gseed composition (Brief 014).
- **Python API extensibility** → GSPL's plugin model allows external scripting languages in v2.

### From WFC
- **Constraint-based generation** → constraint solver as a v1.5 engine for tile-based content.
- **Deterministic with seed** → already a GSPL constitutional property (Brief 015).
- **Tile set authoring** → GSPL's modifier surfaces can wrap tile authoring as a friendly UI.
- **Composition with other techniques** → cross-engine breeding (Brief 014) is the natural superset.

## What is structurally impossible for them to copy

### AI as native, not bolt-on
Houdini and Blender are both adding ML features, but they are bolted onto a node graph that was not designed for ML. GSPL's substrate (Brief 015) is *content-addressed and parameter-based by design* — every artifact can be embedded, every parameter can be optimized, every decision can be searched.

### Lineage as data
The Houdini node graph is *workflow*, not *history*. If you change a node, the previous state is gone (unless you remember to version). GSPL's lineage is permanent and queryable.

### Conversational interface
Houdini's UI is for technical artists. GSPL's conversational interface (Brief 049) opens procedural creation to non-technical users for the first time.

### Federation and marketplace with provenance
Houdini HDAs are sold on Gumroad with no provenance. WFC tile sets are passed around as zips. GSPL's marketplace (Brief 044) with c2pa, signed identity, and royalty flow is structurally different.

### Critique loop and evolution
Houdini and Blender have no critique system; the artist is the critic. GSPL ships ensemble critics (Brief 040) and evolution operators (Brief 041) that close the optimization loop the procedural community has wanted for decades.

## Where Houdini still wins (honest)

- **Simulation depth.** GSPL doesn't ship cloth/fluid/pyro simulation at v1. Houdini will be better at hard simulation for years.
- **Production VFX integration.** Houdini is wired into the studio pipeline (Maya, Nuke, Renderman). GSPL is a sovereign tool, not a pipeline component.
- **Low-level control.** VEX is mature; GSPL's plugin model is younger.
- **Community of technical artists.** Decades of HDAs and tutorials.

GSPL accepts these gaps. The strategy is not to replace Houdini for VFX studios; it's to be the procedural tool for everyone who isn't a VFX studio.

## Where Geometry Nodes still wins

- **Blender integration.** Sculpt, model, render in one tool.
- **Free and complete.** GSPL is free but is not a full DCC.
- **Mature for 3D modeling.** GSPL's 3D engine is v2.

Mitigation: GSPL ships a Blender plugin and respects Blender as a complementary tool. Brief 065 covers Blender as an export target.

## What GSPL invents that none have

### Lineage-aware procedural DAG
The lineage DAG is *both* the procedural workflow and the decision history. Time-travel, branch, what-if, replay are all first-class (Brief 052). No procedural toolkit has this.

### Generative substrate
GSPL is the first procedural toolkit where the unit of work (gseed) is content-addressed, signed, lineage-tracked, and federation-distributable from day one. Houdini's HDAs are local files; gseeds are network objects.

### Conversational + agent
The procedural workflow is driven by an LLM agent that writes the node graph based on user intent. This is the missing layer between "I want a desert dune with windswept ripples" and the SOP graph that produces it.

### Critique loop on procedural output
Ensemble critics rate generated procedural output and feed back into the parameter space. This closes a loop that has been open for thirty years.

## Risks identified

- **Houdini adds AI/lineage features.** Probability: medium. Mitigation: GSPL's substrate-level integration is years ahead; Houdini would be retrofitting onto a closed-source commercial product.
- **Blender Foundation adds lineage.** Probability: low (focus is on traditional DCC). Mitigation: GSPL's Blender plugin keeps the door open.
- **WFC implementations get better tooling.** Mitigation: GSPL ships its own WFC-style engine in v1.5 and integrates it with the broader substrate.
- **VFX community dismisses GSPL as toy.** Mitigation: GSPL is not targeting VFX; the positioning is broader.
- **Procedural purists dismiss AI as cheating.** Mitigation: GSPL exposes the procedural layer for those who want it; the AI is opt-in.

## Recommendation

1. **Position GSPL as "the next generation of procedural — substrate, not just node graphs."**
2. **Ship a Blender plugin at v1.** Treat Blender as the closest sympathetic ecosystem.
3. **Houdini import (HDA → gseed wrapper) at v1.5** as a migration path.
4. **WFC engine at v1.5** as a constraint-based tile generator.
5. **Reference Houdini, Blender, and WFC respectfully** in marketing — these are spiritual ancestors.
6. **Engage with the Procjam community** as a cultural fit.
7. **Marketing language**: "Houdini taught us procedural. GSPL is what comes next: procedural + AI + lineage + federation."

## Confidence
**4/5.** The competitive picture is clear; GSPL's structural advantages are real and hard to copy. The 4/5 reflects honest uncertainty about how fast Houdini and Blender will catch up on AI features.

## Spec impact

- `architecture/procedural-substrate.md` — articulates GSPL as procedural-substrate.
- `marketing/competitive-procedural.md` — public positioning.
- `protocols/hda-import.md` — Houdini HDA import format.
- New ADR: `adr/00NN-procedural-substrate-positioning.md`.

## Open follow-ups

- Build the Blender plugin.
- Plan the WFC engine for v1.5.
- Plan the HDA importer for v1.5.
- Engage Procjam community.
- Publish a "procedural substrate" white paper.

## Sources

- Houdini documentation (SideFX).
- Blender Geometry Nodes documentation.
- Maxim Gumin, "WaveFunctionCollapse" GitHub repo.
- Oskar Stålberg's Townscaper and Bad North talks.
- *Procedural Generation in Game Design* (Short, Adams).
- Procjam community resources.
- Internal: Briefs 002, 014, 015, 026, 036-041, 044, 049, 052, 065.
