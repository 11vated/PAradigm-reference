# 071 — How GSPL beats Houdini at hard simulation

## Question
Brief 066 conceded that "Houdini will be better at hard simulation for years." That concession was premature. How does GSPL surpass Houdini at hard simulation — not match, not complement, *surpass* — using the substrate, the lineage, the federation, and the critic loop that Houdini structurally cannot have?

## Why it matters
Hard simulation (pyro, FLIP fluids, Vellum cloth, Bullet/Chaos rigid bodies, hair, soft bodies) is the crown jewel of procedural creation and the area where Houdini has had a 30-year head start. If GSPL's positioning is "the next generation of procedural" (Brief 066), it cannot have a hole where the deepest procedural problem lives. The right answer is not "we don't simulate"; the right answer is "we simulate in a way Houdini structurally cannot."

## What we know from the spec
- Brief 015: gseed format is content-addressed, parameter-based.
- Brief 026: deterministic kernel.
- Brief 037: differentiable quality diversity.
- Brief 040: critic ensemble.
- Brief 041: GSPL-native evolution operators.
- Brief 043: federation.
- Brief 052: lineage time machine.
- Brief 054: rendering pipeline (three tiers: deterministic / native fast / differentiable).

## Findings — Houdini's structural limits

Houdini's simulation pipeline is brilliant but trapped in three architectural assumptions that GSPL does not share:

1. **Solver-as-tool, not substrate-citizen.** A Houdini solver runs, produces a cache, and that cache is an opaque blob. The solver doesn't know its inputs are part of a larger procedural lineage; the cache doesn't know it could be reused if a sub-graph hasn't changed; the parameters don't carry gradients back into the broader system.
2. **Single-machine execution.** Houdini's distributed simulation is HQueue or Tractor — a job scheduler over a render farm, not a federated peer network. There is no concept of *borrowing* compute from a peer, and no cryptographic verification that a remote sim ran the right thing.
3. **Hand-tuned, not critic-guided.** A technical artist tunes pyro parameters by hand for hours. Houdini has no critic ensemble that ranks variants. The optimization loop closes through human eyes, which is the bottleneck.

These are not features Houdini can add without rewriting itself. GSPL inherits none of them.

## Findings — what GSPL ships that Houdini can't

### 1. Differentiable simulation as substrate-native
The last decade of academic work — DiffTaichi (Hu et al. 2020), Brax (Freeman et al. 2021), Genesis (2024), JAX-MD, Warp (NVIDIA), PhiFlow, Nimble, Tiny Differentiable Simulator — has produced simulation solvers that backprop through physics. You can compute the gradient of a loss (e.g., "the cloth should drape like this reference") with respect to any simulation parameter (cloth stiffness, gravity, initial position) and optimize via SGD or higher-order methods.

GSPL's three-tier rendering (Brief 054) already includes a differentiable tier. The same architecture extends to simulation: every simulation engine is a *gseed* whose parameters can be optimized through backprop. This is impossible in Houdini because Houdini's solvers are written in C++ for maximum speed, not autograd compatibility, and retrofitting autograd onto FLIP or Vellum would mean rewriting them.

**Concrete win:** "Make this character's hair drape exactly like this reference photo" becomes a one-line loss minimization in GSPL. In Houdini it's two days of an expert tuning Vellum parameters by hand.

### 2. Lineage-aware simulation caching (INV-200)
Houdini caches a sim by writing a .bgeo sequence to disk. If you change *anything* upstream, you typically resimulate the whole thing. The cache is a leaf, not a graph.

GSPL caches by content-addressed lineage. Every simulation step is a node in the lineage DAG keyed by a hash of (input gseed, parameters, solver version, frame index). When the user changes an upstream parameter, the lineage walker identifies which sub-graphs are still valid and reuses them; only the dirty sub-graph re-simulates. The cache is shareable across the federation: if your friend already simulated this exact configuration, GSPL pulls their cached result (with cryptographic attestation that it ran the right kernel — see Brief 075).

**Concrete win:** A pyro sim that takes 3 hours in Houdini after every parameter change runs in seconds in GSPL on the second iteration, because 90% of the simulation tree didn't change. This is a 100×+ iteration-speed advantage on revision loops.

### 3. Federated simulation compute (depends on Brief 075)
Houdini's render farm is a corporate asset. GSPL's federation is a peer-to-peer compute substrate. Any GSPL user can borrow simulation cycles from any other peer who's offering them, with two cryptographic guarantees: (a) the borrower's lineage hash proves what they wanted simulated, (b) the lender's signed attestation proves what they actually ran. Settlement (CPU/GPU-hours) flows through the marketplace (Brief 044).

**Concrete win:** A solo creator can run a 10-million-particle FLIP simulation by federating across 50 peers, paying them in marketplace credits. Houdini cannot do this without Tractor, a license server, and a corporate IT department.

### 4. Critic-guided simulation parameter search
GSPL's critic ensemble (Brief 040) ranks generated artifacts. Apply it to simulation: the user specifies a high-level goal ("explosive but not chaotic," "drapes naturally," "feels heavy"), and the critic ensemble scores variants. The bandit-driven evolution operators (Brief 041) explore the parameter space. Within minutes the system converges on a tuning that a Houdini artist would take hours to find.

**Concrete win:** Pyro tuning, currently a multi-day skilled-labor task, becomes minutes of automated search with the user as the final arbiter on the top 4-8 variants.

### 5. Compositional simulation via cross-engine breeding (Brief 014)
Houdini composes by wiring node outputs into other node inputs — but the composition is at the data level. GSPL composes at the gseed level via the naturality square (Brief 014, Brief 041 INV-103). Sprite physics, fluid simulation, cloth, hair, and rigid bodies all share the same substrate; you can breed a fluid simulation with a sprite-style art treatment, or a physically-accurate cloth simulation with a procedural pattern engine, without writing glue.

**Concrete win:** Stylized fluids that look like Studio Ghibli watercolors with physically correct flow are a one-line composition in GSPL. In Houdini this is a custom shader and a custom solver.

### 6. Time machine for simulation
Brief 052's lineage-aware time machine extends naturally to simulation. Scrub through a 1000-frame sim and branch at frame 437; GSPL keeps the simulation state at every frame as a lineage node. Houdini's checkpoint feature exists but it's per-session, lossy, and not first-class.

**Concrete win:** "What if the explosion had gone left instead of right at this frame?" is a one-click branch in GSPL. In Houdini it's a manual checkpoint reload and a re-sim.

### 7. Provenance for simulation results (Brief 008, Brief 058)
Every cached frame is c2pa-attested. A simulation result is cryptographically tied to the inputs that produced it and the solver version that ran it. Houdini has nothing remotely like this. For any production where reproducibility matters (VFX, scientific viz, robotics), GSPL's provenance is a hard win.

## What GSPL ships at each phase

### v1
- **Differentiable rigid-body** simulation engine via Genesis or Brax (open weights, MIT/Apache).
- **Differentiable cloth** via Nimble or PhiFlow.
- **Lineage-aware caching infrastructure** with content-addressed simulation results.
- **Critic-guided parameter search** for cloth and rigid bodies.
- **Houdini parity pitch:** match Vellum cloth and Bullet rigids on quality, beat them on iteration speed.

### v1.5
- **Differentiable fluids** (FLIP-style) via Genesis or PhiFlow.
- **Federated simulation compute** (depends on Brief 075).
- **Differentiable pyro** via Warp-style autograd if NVIDIA's licensing allows; else PhiFlow.
- **Hair/soft body** via Vellum-equivalent open implementation.

### v2
- **Production-grade pyro** matching Houdini quality with the GSPL substrate advantages.
- **Coupled multi-physics** (fluid + cloth + rigid) via cross-engine breeding.
- **Plasma, magnetohydrodynamics, granular** for scientific use cases.

### v3
- **End-to-end differentiable inverse simulation** — "give me the initial conditions that produce this final state" as a primitive operation.

## Inventions

### INV-200: Lineage-aware simulation caching with hash-based skip
The cache key is `hash(input_gseed || parameters || solver_version || frame_index)`. The cache is content-addressed and federated. On parameter change, a lineage walker computes which sub-graphs are still valid via dependency analysis on the parameter graph. This is novel because no other simulation system treats sim cache as a node in a content-addressed lineage; Houdini, Maya, Blender all treat it as opaque per-take output.

### INV-201: Differentiable-substrate simulation
The substrate exposes the gseed parameter space as a tangent space; gradients flow through any differentiable engine via autograd. Combined with the critic ensemble, this enables direct optimization of simulation parameters against high-level perceptual losses. Novel because no other procedural tool exposes the entire substrate as a differentiable manifold.

### INV-202: Cross-physics breeding via naturality square
Brief 041 INV-103 (cross-engine breeding) applied specifically to physics: a fluid sim and a cloth sim can be bred into a coupled simulation without writing coupling code, because the substrate operator preserves the categorical structure. Novel application of category-theoretic substrate composition to multi-physics.

## What Houdini still does better at v1

Honest accounting:
- **Production-grade pyro at film quality.** Houdini wins until v2.
- **Vellum cloth depth and stability** for AAA cinematics. Houdini wins until v1.5.
- **Studio pipeline integration** (Maya, Nuke, RenderMan). GSPL is a sovereign tool; pipeline integration is a v2 conversation.
- **Decades of HDAs and tutorials.** GSPL community starts at zero.

These are not architectural disadvantages; they are time-and-investment disadvantages. The architectural ledger favors GSPL on every axis except installed-base.

## Risks identified

- **Differentiable simulation is academic.** Few production users. Mitigation: GSPL ships both differentiable and non-differentiable engines; the differentiable mode is the optimization advantage, but users don't have to engage with it.
- **Open-weight differentiable physics is fragmented.** Multiple research libraries, none production-grade. Mitigation: GSPL chooses one as v1 backbone (Genesis or Brax); ships an abstraction layer; can swap underneath.
- **GPU memory for large sims.** Federated compute (Brief 075) is the answer.
- **Stability of differentiable solvers.** Numerical issues are real. Mitigation: ship non-differentiable fallbacks; use differentiable mode only where it converges.
- **Houdini adds AI features and lineage.** Probability: medium. Mitigation: GSPL's substrate-level integration is a years-long engineering moat; Houdini retrofitting is harder than greenfield.

## Recommendation

1. **Reverse the Brief 066 concession.** GSPL beats Houdini at hard simulation via differentiable, lineage-aware, federated, critic-guided substrate-native physics.
2. **Ship differentiable rigid + cloth at v1.** Genesis or Brax as the backbone.
3. **Implement INV-200 (lineage-aware sim caching) as the headline performance demo** — 100× iteration speedup is a meme-worthy benchmark.
4. **Federated simulation compute at v1.5** when federation matures.
5. **Pyro at v2** with full differentiability.
6. **Engage academic differentiable-physics community** as advisors (DiffTaichi, Genesis, Brax teams).
7. **Marketing language**: "Houdini's solver runs once. GSPL's substrate runs once and remembers."

## Confidence
**4/5.** The architecture is defensible; the open-weight differentiable physics ecosystem is real and improving fast. The 4/5 reflects honest uncertainty about whether differentiable solvers reach production stability for fluids and pyro by v2.

## Spec impact

- `architecture/simulation-substrate.md` — new doc.
- Update Brief 066 to remove the simulation concession.
- New ADR: `adr/00NN-differentiable-simulation-as-substrate.md`.
- New ADR: `adr/00NN-lineage-aware-sim-cache.md`.

## Open follow-ups

- Pick v1 differentiable physics backbone (Genesis vs Brax vs PhiFlow vs Nimble).
- Build INV-200 prototype.
- Engage Genesis and Brax teams.
- Plan federated sim compute with Brief 075.
- Quarterly benchmark vs Houdini Vellum on cloth iteration speed.

## Sources

- Hu et al., "DiffTaichi: Differentiable Programming for Physical Simulation" (2020).
- Freeman et al., "Brax — A Differentiable Physics Engine" (2021).
- Genesis simulator (2024).
- Holl & Thuerey, "PhiFlow" (2020).
- NVIDIA Warp documentation.
- Werling et al., "Fast and Feature-Complete Differentiable Physics for Articulated Rigid Bodies via Nimble" (2021).
- SideFX Houdini documentation.
- Internal: Briefs 014, 015, 026, 037, 040, 041, 043, 044, 052, 054, 058, 066, 075.
