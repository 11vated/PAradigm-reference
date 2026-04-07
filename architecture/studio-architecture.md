# Studio Architecture

The Creation Studio is the user-facing surface of Paradigm. It is a React-based single-page application that exposes every Layer 1–6 capability — seeds, language, engines, evolution, intelligence — through a tactile, real-time, "describe and watch" interface.

This document specifies the studio's architecture, its component model, its state management, its rendering pipelines, and its deterministic preview/replay behavior.

## Design Philosophy

The Studio is opinionated about three things:

1. **Genes are the primary object on screen.** Not artifacts. The user always sees the seed (its name, lineage, gene table) alongside the rendered preview. This is what trains intuition for "this is the artifact's source code."
2. **Every interaction must have a deterministic seed-level outcome.** When the user drags a slider, twists a knob, or clicks "evolve," the result is a new seed with a recorded lineage edge. Nothing happens "off the books."
3. **The studio is a thin client over the deterministic substrate.** It does not invent gene values. It does not run the LLM. It does not compute fitness. It dispatches to Layers 1–6 and renders the results.

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    React Studio (UI)                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│  │ Prompt  │ │ Gallery │ │ Gene    │ │ Preview │         │
│  │ Bar     │ │         │ │ Editor  │ │ Viewport│         │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│  │ Lineage │ │ Evolve  │ │ Breed   │ │ Export  │         │
│  │ Tree    │ │ Panel   │ │ Panel   │ │ Panel   │         │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘         │
├──────────────────────────────────────────────────────────┤
│              Studio State (Zustand / Jotai)              │
│   currentSeed, history, gallery, settings, agent state   │
├──────────────────────────────────────────────────────────┤
│                  Studio Service Layer                    │
│   intentToSeed, grow, mutate, breed, evolve, export      │
├──────────────────────────────────────────────────────────┤
│              Web Worker Pool + WebGPU Bridge             │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  Layer 6 — Agent       │
              │  Layer 5 — Evolution   │
              │  Layer 4 — Engines     │
              │  Layer 2 — Seed System │
              │  Layer 1 — Kernel      │
              └────────────────────────┘
```

The Studio is a layered React app: presentational components on top, a state store in the middle, a service layer that calls Layer 1–6 below, and a worker pool that offloads heavy work off the main thread.

## Core Components

### Prompt Bar

The text input. Submits to the GSPL Agent. Streams sub-agent progress as the agent works ("planning…", "personality…", "visuals…", "validating…"). Shows the final seed when done.

### Preview Viewport

A WebGPU- or WebGL-backed renderer that displays the current artifact:

- **Sprite/Visual2D:** PNG drawn into a canvas with zoom/pan and onion-skinning for animation frames.
- **Character/Geometry3D:** Three.js scene with orbit controls.
- **Music/Audio:** WaveSurfer-style waveform with a play head.
- **FullGame:** An iframe that loads the generated HTML5 bundle and lets the user actually play.
- **Narrative:** A formatted reader view.
- **Procedural/Terrain:** Top-down map with layer toggles.

The viewport uses `engine.renderHints` to know which rendering mode to enter.

### Gene Editor

A panel that shows the current seed's gene table. Each gene type has its own editor widget:

- **Scalar gene:** slider with min/max from the schema.
- **Categorical gene:** dropdown.
- **Vector gene:** N sliders with optional 2D pad for pairs.
- **Expression gene:** monaco-style code editor with GSPL syntax highlighting.
- **Field gene:** an SDF preview with isosurface and gradient visualization.
- **Topology gene:** a small graph editor.
- **(etc. for all 17 types)**

Editing a gene immediately produces a new seed (with lineage edge `mutate`) and grows it. With incremental mode enabled, only the affected stages re-run.

### Gallery / MAP-Elites Grid

When evolution is running, the gallery shows the MAP-Elites archive as a grid where each cell is one elite seed. Clicking a cell loads it into the preview. The gallery is the *primary output* of an evolution run — diversity is the win, not a single optimum.

### Lineage Tree

A graph view (force-directed or hierarchical) of the current seed's ancestry. Each node is a seed; each edge is a `mutate`/`breed`/`compose` operation. Clicking an ancestor reverts the preview to that seed (without losing the descendants).

### Evolve Panel

Configures and starts an evolution run:

- Algorithm (GA / MAP-Elites / CMA-ES / Novelty / AURORA / DQD / POET).
- Population size (10–10,000).
- Termination (generations or time).
- Fitness emphasis (which QualityVector axes to weight).

The evolution loop runs in a Web Worker so it doesn't block the UI.

### Breed Panel

Pick two seeds. Run `breed(a, b)`. Show the child. Optionally batch-breed (sample N children).

### Export Panel

Choose target format from `engine.exportHints` (PNG, glTF, WAV, MIDI, HTML5 zip, .gseed). Download or copy the URL. Optionally publish to the marketplace.

## State Management

The studio uses **Zustand** (or equivalent) with a few small stores:

```ts
const useSeedStore = create((set) => ({
  current: null as Seed | null,
  history: [] as Seed[],
  setCurrent: (seed: Seed) => set({ current: seed }),
  push: (seed: Seed) => set((s) => ({ current: seed, history: [...s.history, seed] })),
  undo: () => set((s) => {
    const h = s.history.slice(0, -1);
    return { history: h, current: h[h.length - 1] ?? null };
  }),
}));

const useGalleryStore = create((set) => ({
  archive: new Map<DescriptorKey, Seed>(),
  insert: (key: DescriptorKey, seed: Seed) => set((g) => {
    const a = new Map(g.archive);
    a.set(key, seed);
    return { archive: a };
  }),
  clear: () => set({ archive: new Map() }),
}));

const useAgentStore = create((set) => ({
  pipelineStage: 'idle' as PipelineStage,
  parsedIntent: null as ParsedIntent | null,
  pendingSubagents: [] as SubAgentName[],
}));
```

State is intentionally **flat and explicit**. There is no global mutable singletons, no React Context spaghetti. Stores are subscribed by hooks in the components that need them.

## The Service Layer

Between the React components and the Layer 1–6 modules sits a thin service layer that:

1. Wraps Layer 1–6 calls in promise APIs.
2. Posts work to Web Workers when appropriate.
3. Catches and types errors for the UI.
4. Streams progress events for long-running operations.

```ts
class StudioService {
  constructor(private kernel: Kernel, private workers: WorkerPool) {}

  async generateFromPrompt(text: string): Promise<Seed> { ... }
  async grow(seed: Seed): Promise<Artifact> { ... }
  async mutate(seed: Seed, rate: number): Promise<Seed> { ... }
  async breed(a: Seed, b: Seed): Promise<Seed> { ... }
  async evolve(config: EvolveConfig, onUpdate: (e: EvolveEvent) => void): Promise<EvolveResult> { ... }
  async export(seed: Seed, format: string): Promise<Blob> { ... }
}
```

The service layer is the only place that imports from Layer 1–6. The React components only see the service interface.

## Web Worker Pool

Heavy work — engine `grow`, evolution loops, fitness evaluation, large mutations — runs in Web Workers off the main thread. The pool has:

- A small fixed number of workers (typically `navigator.hardwareConcurrency - 1`).
- A job queue with priority levels (interactive preview > evolution > export).
- Cancellation tokens so the user can abort a long evolution.
- Structured-clone postMessage with shared `ArrayBuffer` for large gene data.

## WebGPU Bridge

Engines marked `@gpu` execute their fitness or rendering kernels on the GPU via WebGPU. The studio's WebGPU bridge:

1. Detects WebGPU support and falls back to CPU workers if absent.
2. Compiles WGSL kernels lazily.
3. Manages GPU buffer allocation and reuse.
4. Caches compiled pipelines by `(engine.name, engine.version, kernel.name)`.

A typical fitness evaluation moves a batch of seeds onto the GPU, runs the WGSL kernel, reads back a `Float32Array` of QualityVector components, and uses those for selection. Speedup is 10–50× vs CPU.

## Interactive Mode vs Batch Mode

The studio operates in two modes:

- **Interactive mode** (default): population sizes 10–50, sub-second per-generation latency. The user sees evolution happen in real time.
- **Batch mode**: population sizes 100–10,000, runs in the background, the user can do other work and check back later. Notifications when complete.

Both modes use the same algorithm code; only the population container differs.

## Determinism in the Studio

The studio is held to the same determinism standard as the rest of the platform:

- A user who clicks "Generate" with the same prompt and the same RNG seed gets the same seed (modulo the LLM call, which is captured at the seed boundary).
- A user who clicks "Evolve 50" with the same starting seed and config gets the same final archive.
- A user who exports the same seed gets the same bytes.

The studio achieves this by:

- Always passing an explicit RNG seed to operations (defaulting to `kernel.hash(currentSeed)` if the user didn't specify).
- Tagging every operation with a deterministic operation ID derived from the inputs.
- Storing operation results in a content-addressed cache (per-session) so re-displays are instant.

## Federation in the Studio

A **federation panel** lets the user opt into the planet-scale evolution model. When enabled:

1. The studio establishes WebSocket connections to a small set of peer Studios (selected by the federation router for diversity).
2. The local evolution loop periodically exchanges 1–5% of its elites with peers.
3. Imported elites appear in the gallery with a 🌐 marker showing they came from federation.

The user can revoke federation at any time without losing local work; federated seeds remain locally because they're full seeds, not references.

## Marketplace Integration

The Studio has a marketplace pane that lets users:

- **Browse** seeds by domain, archetype, style, popularity.
- **Preview** any seed (it grows locally, deterministic, no trust required).
- **Buy** a seed (Stripe Connect flow).
- **Sell** a seed (set price, royalty terms, license).
- **Breed** a purchased seed with their own (royalties propagate automatically).

The economic model is documented in [`spec/05-sovereignty.md`](../spec/05-sovereignty.md).

## Accessibility

The Studio targets WCAG 2.1 AA:

- Keyboard navigation for every action.
- Screen-reader-friendly seed descriptions (the gene editor announces gene changes with audio descriptions).
- Color-blind safe defaults in palette and chart components.
- Adjustable text size, motion-reduced animations.
- Captions on every audio preview (using the music engine's metadata).

## Performance Targets

| Operation | Target |
|---|---|
| Cold start to first prompt | < 2 s |
| Prompt → seed (no LLM cache) | < 5 s |
| Prompt → seed (with cache) | < 200 ms |
| Single grow (sprite) | < 100 ms |
| Single grow (3D mesh) | < 500 ms |
| Single grow (full game bundle) | < 30 s |
| Evolution generation (50 pop, sprite) | < 500 ms |
| Lineage tree render (1k nodes) | < 100 ms |
| Export to PNG/glTF/WAV | < 1 s for typical sizes |

These targets drive engineering priorities. Anything that misses a target gets a profiling pass.

## File Layout

```
studio/
├── src/
│   ├── components/         # React components, one per UI area
│   ├── stores/             # Zustand stores
│   ├── services/           # Service layer
│   ├── workers/            # Web Workers
│   ├── webgpu/             # WebGPU bridge and WGSL kernels
│   ├── routes/             # SPA routes
│   └── main.tsx            # App entry
├── public/
└── package.json
```

The studio is its own package and can be replaced wholesale (e.g., with a CLI, VS Code extension, Figma plugin, native app) as long as the replacement consumes the same Layer 6 API.
