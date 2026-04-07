# 048 — Studio/IDE architecture

## Question
What is the architecture of the GSPL Studio — the desktop application that hosts the chat agent, the engines, the lineage browser, the marketplace, and the user's local data — and how is it structured to be reliable, fast, modifiable, and offline-first?

## Why it matters
The studio is *the* product. Everything in the spec is invisible to users without a studio that exposes it well. The studio is also where reliability lives: a flaky or slow studio kills adoption regardless of how good the substrate is. And because GSPL is offline-first and sovereignty-first, the studio cannot lean on cloud services to hide its complexity.

## What we know from the spec
- All previous briefs assume a studio exists.
- Brief 029-034: agent and memory live in the studio.
- Brief 011: reliability stack lives in the studio.

## Findings — six-layer studio architecture

### Layer 1: Kernel
The lowest layer. Pure Rust, no UI, no networking. Hosts:
- The deterministic GPU/CPU kernel (Brief 001).
- The seed file format reader/writer (Brief 015).
- The signing primitives (Brief 004, Brief 042).
- The lineage DAG store (Brief 017).
- The engine plugin loader.

The kernel is a *library*, embeddable in any frontend. It is the first thing that gets stabilized and the last thing that breaks.

### Layer 2: Engines
Each engine (CharacterEngine, MusicEngine, etc.) is a plugin that registers with the kernel. Engines are dynamically loadable so that the studio can ship a small core and let users add engines they need.
- **Engine plugins are signed** by Anthropic (or eventually a community release process).
- **Engine versions are pinned** per project (Brief 018).
- **Each engine ships its own validators, critics, exporters, and reference renderer.**

### Layer 3: Agent
The planner+executor agent (Brief 029) and its sub-agents (Brief 030). Implemented as a tool-using LLM client that talks to the kernel via the standard tool surface.
- **The agent runs in-process by default** for latency.
- **It can also run remotely** (e.g., the user's home server) via the same tool API over RPC.
- **LLM access is configurable**: local (via llama.cpp / mistral.rs / equivalent), Anthropic API, OpenAI-compatible, or Bring-Your-Own.
- **The agent does not have direct file system access**; everything goes through the kernel's bounded file API.

### Layer 4: Local services
A small set of background services run alongside the studio:
- **Federation service** (Brief 043) — libp2p peer.
- **Settlement service** (Brief 044) — handles marketplace transactions.
- **Index service** — maintains the HNSW exemplar index (Brief 031).
- **Backup service** — periodic encrypted backups of the user's profile.
- **Notification service** — surfaces critical events (key rotation due, federation peer message, etc.).

Services are isolated processes communicating via Unix domain sockets / named pipes. Crashes in one service don't take down the studio.

### Layer 5: Frontend
The user-facing UI. Two implementations are planned:
- **Desktop (v1)**: Tauri-based. Rust backend, web frontend (React/Svelte). Native window, native menus. Single binary per OS.
- **Browser (v1.5)**: a thin web frontend that talks to a self-hosted studio backend. Same UI, different shell.
- **Mobile (v2)**: separate native app, talks to a self-hosted backend.

The frontend is *strictly a view layer*. All business logic is in the kernel and agent. The frontend is replaceable.

### Layer 6: Project workspace
A *project* is a directory on disk containing:
- The seed files (`.gseed` per Brief 015).
- The lineage database (a single SQLite file or sled tree).
- Project-level configuration (engines pinned, critics weights, etc.).
- The local exemplar archive.
- Asset references (the studio doesn't move files unnecessarily).

Projects are *content addressed at the directory level*: the project hash is the Merkle root of all included files. This makes "git for projects" trivial.

## Frontend pillars

The studio frontend has six top-level surfaces:
1. **Compose** — the chat interface where users describe what they want.
2. **Forge** — the engine-specific authoring view (sprite editor, music piano roll, level editor, etc.).
3. **Lineage** — the DAG browser showing the project's evolutionary history.
4. **Critique** — the critic dashboard showing scores, ensemble outputs, and feedback.
5. **Vault** — the local archive of finalized seeds and exports.
6. **Bazaar** — the marketplace and federation surface.

Each pillar is a separate route; navigation is keyboard-first and accessible.

## Performance budgets

The studio has hard performance budgets per interaction:
- **First paint to interactive:** < 1.5s.
- **Compose chat response (first token):** < 800ms.
- **Forge view load:** < 500ms.
- **Lineage navigation:** < 200ms per hop.
- **Critique score render:** < 300ms.
- **Vault search:** < 300ms for top-50 results.

These are *hard budgets* — failing them is a release blocker.

## Offline-first requirements

- **Every feature works fully offline.** The studio detects connectivity and gracefully degrades online-only features.
- **All data is local.** No "cloud sync as primary."
- **The agent works offline** if a local LLM is configured. If not, the agent shows a clear offline-mode banner.
- **Federation and marketplace require connectivity** but degrade gracefully.

## Risks identified

- **Tauri immaturity:** Tauri v2 is still maturing. Mitigation: pin to known-stable releases; have an Electron fallback designed but not built.
- **LLM cold-start latency:** local LLMs can take seconds to load. Mitigation: keep loaded in memory; pre-warm on startup.
- **SQLite scaling:** lineage DAGs can grow large. Mitigation: SQLite handles millions of rows fine; sharding is a v2 concern.
- **Engine plugin ABI drift:** dynamic loading is fragile across Rust compiler versions. Mitigation: stable C ABI shim per engine; engines compiled per release.
- **Frontend rewrite risk:** if Tauri or React fails, the rewrite is expensive. Mitigation: business logic is *not* in the frontend; the frontend is small and replaceable.
- **Cross-platform parity:** macOS, Windows, Linux must all work identically. Mitigation: CI on all three; native test suite per release.
- **Mobile latency:** mobile devices are slow. Mitigation: mobile is v2; the v1 mobile experience is "view-only via web frontend."

## Recommendation

1. **Adopt the six-layer architecture** in `architecture/studio.md`.
2. **Tauri is the v1 frontend shell.** Native binary, single-file install.
3. **All business logic in the kernel** (Rust); frontend is view-only.
4. **Engines are signed plugins** with versioned ABI.
5. **Background services are isolated processes** with crash isolation.
6. **Performance budgets are release-blocking.**
7. **Offline-first is constitutional.** No feature requires connectivity.
8. **Local LLM support is mandatory at v1**, with Bring-Your-Own as fallback.
9. **Project workspace is a Merkle-rooted directory.**
10. **Cross-platform CI from day one** for macOS / Windows / Linux.

## Confidence
**4/5.** The architecture is conventional for an offline-first creator tool. The 4/5 reflects the unmeasured complexity of cross-platform engine plugins and Tauri maturity.

## Spec impact

- `architecture/studio.md` — full studio architecture.
- `architecture/studio-frontend.md` — six pillars, navigation, accessibility.
- `architecture/studio-services.md` — background service spec.
- `architecture/studio-performance-budgets.md` — hard budgets.
- `protocols/engine-plugin-abi.md` — stable ABI for engine plugins.
- New ADR: `adr/00NN-tauri-as-studio-shell.md`.

## Open follow-ups

- Tauri v2 vs Electron comparison spike.
- Decide on the frontend framework (React vs Svelte vs SolidJS).
- Build a stable engine plugin ABI prototype.
- Performance budget validation on a low-end target machine.
- Decide on the local LLM library (llama.cpp vs mistral.rs vs candle).

## Sources

- Tauri documentation.
- VS Code's process model (a strong reference for plugin isolation).
- Figma's local-first architecture writeup.
- Internal: Briefs 001, 015, 017, 018, 029-034, 042, 043, 044.
