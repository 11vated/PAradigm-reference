# 220 — Debugger and time-travel inspector

## Question
What is the typed debugger and time-travel inspector that enables substrate creators to step through gseed mutations, inspect substrate state at any lineage frame, set typed breakpoints on mutation kinds, and replay-debug across the eight engine targets — turning the substrate's signed lineage into a first-class debugging surface?

## Why it matters (blast radius)
Substrate state is signed and lineage-tracked (Brief 152). That lineage IS a perfect time-travel debugging trace — every mutation, every gate, every state. Without a typed debugger, creators can't easily exploit it. With one, the substrate becomes the most debuggable runtime ever built: every bug has a complete, deterministic, replayable history with provenance.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 185 — playtest harness with replay verifier.
- Brief 217 — CLI and headless toolchain.
- Brief 218 — Language server and IDE integration.

## Findings
1. **`gspl debug` subcommand.** CLI subcommand `gspl debug <replay.gseed>` opens an interactive debugger session against a recorded replay. TUI by default; `--gui` launches the GUI inspector window.
2. **Lineage as debug trace.** The signed lineage chain (Brief 152) is the debug trace. Every frame is a typed mutation with full state delta. Stepping forward / backward through lineage is constant-time relative to lineage length.
3. **Typed breakpoints.** Breakpoints are typed: break on mutation kind, break on gate violation, break on field value change, break on entity creation/destruction, break on lineage hash mismatch (parity test debugging).
4. **State inspection.** At any frame, the inspector renders: full substrate state tree (browsable JSON), typed entity list, recent mutations (last 100), upcoming mutations (next 100), validation gate state.
5. **Time-travel.** Step forward / backward by 1 frame, by N frames, by mutation kind, by tagged checkpoint. Reverse execution is exact (lineage is signed and deterministic).
6. **Differential view.** Compare two frames side-by-side; the inspector highlights typed field deltas. Useful for "what changed between frame 1000 and frame 1100".
7. **Mutation injection (advanced).** Optional debugger mode allows injecting typed mutations at the current frame to explore alternative state. Injection is sandboxed; the modified replay is forked into a new branch with new lineage signature.
8. **Engine attach mode.** Debugger can attach to a running engine target via the substrate runtime's debug socket. Live engine state is streamed to the inspector; breakpoints pause the engine.
9. **Replay marking.** During playtest sessions, players or QA can press a typed marker key to drop a labeled marker into the lineage. Markers appear in the inspector timeline for fast bug navigation.
10. **Crash replay.** When a creator-shipped game crashes (with player consent), the substrate runtime can save the recent lineage window to a typed crash replay gseed. Creators load it in the debugger to reproduce the crash deterministically.
11. **AI agent debug surface.** Debugger exposes structured JSON state to AI agents via a typed `gspl debug query` subcommand. Agents like Claude Code can inspect crashes and propose fixes with full state context.
12. **Validation contract.** Sign-time gates: replay gseed lineage signature valid, debug socket protocol version matches runtime, mutation injection branches signed independently.

## Risks identified
- **Lineage size.** Long replay sessions produce massive lineage chains. Mitigation: typed lineage compression with checkpoint-and-delta encoding; full state at checkpoints, deltas between.
- **Reverse-execution determinism.** Reverse stepping must reconstruct prior state exactly. Mitigation: lineage is signed; reverse step is deterministic by construction.
- **Engine attach overhead.** Live attach streams state across debug socket. Mitigation: typed bandwidth budget; default streams only deltas, not full state.
- **Mutation injection security.** Injection could be misused to forge replays. Mitigation: forked branches signed with creator identity; original lineage signature preserved as parent.

## Recommendation
Specify the debugger as a `gspl debug` subcommand operating against signed replay gseeds (or live engine attach), with typed breakpoints, time-travel stepping, differential view, mutation injection sandbox, crash replay, replay marking, and AI agent debug query surface. Lineage is the debug trace; substrate is the most debuggable runtime by construction.

## Confidence
**4.5 / 5.** Time-travel debugging is well-precedented (rr, Pernosco, Replay.io). The novelty is the substrate's signed lineage being the debug trace natively, requiring no instrumentation. Lower than 5 because mutation injection sandboxing needs Phase-1 security review.

## Spec impact
- New spec section: **Debugger and time-travel inspector specification**.
- Adds the `gspl debug` subcommand contract.
- Adds the typed debug socket protocol for engine attach.
- Adds typed breakpoint kinds.
- Adds the typed marker mutation for replay annotation.
- Cross-references Briefs 152, 185, 217, 218.

## New inventions
- **INV-959** — `gspl debug` subcommand using signed lineage as native debug trace: substrate state is debuggable without instrumentation, by construction.
- **INV-960** — Typed breakpoint kinds (mutation / gate / field / entity / lineage hash): breakpoints are first-class typed primitives, not opaque address conditions.
- **INV-961** — Exact reverse execution via signed deterministic lineage: time-travel is provably correct, not approximated.
- **INV-962** — Differential frame view with typed field-delta highlighting: state diffs are structured, not text-blob.
- **INV-963** — Sandboxed mutation injection forking lineage into signed branches: hypothetical state exploration is auditable.
- **INV-964** — Engine attach mode via typed debug socket protocol with bandwidth-budgeted state streaming: live debugging across all eight engine targets uses one protocol.
- **INV-965** — Typed replay marker mutation for QA / playtester annotations: bug navigation in long replays is structured.
- **INV-966** — Player-consented crash replay capture saving lineage window as typed gseed: creator-shipped crashes are reproducible deterministically.
- **INV-967** — AI-agent debug query surface for structured state inspection: agents diagnose crashes with full state context, not stack traces alone.

## Open follow-ups
- Reverse-execution UX refinement — Phase 1.
- GUI inspector visual design — Phase 1.
- Multi-replay diffing — deferred to v0.2.
- Phase-1 lineage compression measurement.
- Watchpoint expressions on derived state — deferred to v0.3.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 185 — Playtest harness with replay verifier.
3. Brief 217 — CLI and headless toolchain.
4. rr (Mozilla record-and-replay debugger).
5. Pernosco time-travel debugger.
6. Replay.io browser time-travel.
7. Elm Debugger (time-travel UX precedent).
