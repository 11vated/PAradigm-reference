# Tool Layer — The GSPL Full-Capacity Agent Execution Runtime

**Status:** Draft, load-bearing for `intelligence/gspl-agent-full-capacity.md`.
**Audience:** implementers building the local-first sovereign agent that populates the Seed Commons.
**Constraint spine:** GSPL Open Specification License. 100% free forever. No paywalls. No rate limits. Forkable. Self-hostable. No cloud dependency. Runs on commodity hardware the user owns.

This document is the **concrete execution-runtime spec** for the GSPL Full-Capacity Agent. It consumes the prior research on LangGraph, AutoGen, CrewAI, OpenAI Agents SDK, Cursor/Windsurf, and Devin-class autonomous coders, and binds each pattern to GSPL's non-negotiable constraints. Everything here is implementable with open-source components a user can apt-install on a laptop.

The agent spec (`gspl-agent-full-capacity.md`) describes *what the agent does*. This document describes *how it runs*: the runtime, the tool interface, the code-execution sandbox, the memory system, the multi-agent topology, and the self-improvement loop. It is the missing middle between the architecture doc and a working binary.

## 0. Design principles inherited from `gspl-agent-full-capacity.md`

1. **LLM confined to the Intent stage.** No sub-agent except IntentOracle is allowed to emit `.gspl` source directly from LLM output. Every token that ends up in a signed seed passes through a deterministic compiler first.
2. **Every tool invocation is lineage.** Web fetch, code execution, and database queries are recorded as `dimensional` or `symbolic` genes inside the resulting seed's lineage, so any reader can re-audit the provenance.
3. **Sandboxed by default.** No sub-agent runs with host-level privileges. Tools mediate every effect.
4. **Air-gap mode is mandatory.** The agent MUST be able to populate the commons with the internet unplugged. Network tools are optional, not load-bearing.
5. **Determinism is the output contract.** Two runs with identical inputs + identical tool receipts MUST produce byte-identical `.gseed` files.

## 1. Runtime topology

```
+------------------------------------------------------------+
|                    Host operating system                   |
|   Linux / macOS / Windows (WSL2). Commodity hardware.       |
+------------------------------------------------------------+
                        |
+------------------------------------------------------------+
|              GSPL Agent Process (single binary)             |
|                                                             |
|   +-----------------+     +--------------------------+      |
|   |  LLM Provider   | <-> |  IntentOracle sub-agent  |      |
|   |  (local)        |     +--------------------------+      |
|   +-----------------+              |                         |
|                                    v                         |
|                          +---------------------+              |
|                          |   Agent Kernel      |              |
|                          |  (LangGraph-style   |              |
|                          |   state machine)    |              |
|                          +---------------------+              |
|                           |           |      |                |
|              +------------+           |      +------------+   |
|              v                        v                   v   |
|   +-----------------+   +-----------------+   +------------+  |
|   | Tool Layer      |   | GSPL Compiler   |   | Memory     |  |
|   | (sandboxed)     |   | (deterministic) |   | Stores     |  |
|   +-----------------+   +-----------------+   +------------+  |
|         |                                                      |
|         v                                                      |
|   +-----------------------------+                              |
|   | Execution Sandbox (Docker / |                              |
|   | Firecracker / bubblewrap)   |                              |
|   +-----------------------------+                              |
+------------------------------------------------------------+
```

The host runs one agent process. The agent process holds the kernel state machine, the LLM provider handle, the memory stores, and the tool dispatcher. The execution sandbox is a short-lived child namespace spawned per tool call. Nothing leaks across calls except what the kernel explicitly commits to memory.

## 2. LLM provider layer

The agent does **not** ship a bundled model. It ships a provider interface.

### 2.1 Required providers

| Provider | Binding | Air-gap compatible | Notes |
|---|---|---|---|
| `ollama` | HTTP localhost | **yes** | Default. Ships with `deepseek-coder:33b`, `codellama:34b`, `mistral-large-123b`, `llama-3.3-70b-instruct` as recommended models; user installs whichever their RAM supports. |
| `llama.cpp` | embedded GGUF runner | **yes** | For users who cannot run a daemon. GGUF files are user-owned. |
| `vllm` | HTTP localhost | **yes** | For users with multi-GPU boxes. |
| `anthropic` | HTTPS api.anthropic.com | no | Optional convenience provider. Disabled in air-gap mode. Never required. |
| `openai`    | HTTPS api.openai.com    | no | Optional convenience provider. Disabled in air-gap mode. Never required. |

The default provider in the shipped config is `ollama` with `deepseek-coder:33b`. A user with a 24 GB GPU can swap to a 70B class model without touching any other config.

### 2.2 Provider contract

```
trait LlmProvider:
    fn name() -> String
    fn supports_streaming() -> Bool
    fn infer(req: InferenceRequest) -> Result<InferenceResponse, LlmError>
    fn embed(texts: Array<String>) -> Result<Array<Vector>, LlmError>

struct InferenceRequest:
    system: String
    messages: Array<Message>
    stop: Array<String>
    max_tokens: Int
    temperature: Float
    seed: u64           # REQUIRED. No call is made without a seed. Determinism.
    tools: Array<ToolSchema>  # provider-side tool calls are disallowed in agent mode
```

Providers that do not accept a `seed` parameter are wrapped in a deterministic-sampling shim that pins temperature to 0 and re-runs on non-deterministic output. Providers that emit tool calls directly are rejected; the agent kernel owns the tool loop.

## 3. Agent kernel — a LangGraph-style state machine

The kernel is not LangGraph. The kernel is a minimal, auditable state machine inspired by LangGraph, rewritten in Rust for a single-binary distribution, with every transition recorded as a lineage event.

### 3.1 Kernel states

```
enum KernelState:
    Idle
    Intent { request: SeedRequest }
    Plan { intent: NormalizedIntent }
    Research { plan: Plan }
    Draft { plan: Plan, research: ResearchBundle }
    Validate { draft: DraftSeed }
    Reflect { draft: DraftSeed, report: ValidationReport }
    Evolve { draft: DraftSeed }
    Sign { seed: ValidatedSeed }
    Archive { signed: SignedSeed }
    Error { previous: KernelState, cause: KernelError }
```

Every state transition is a pure function:

```
fn step(state: KernelState, event: KernelEvent) -> (KernelState, Array<SideEffect>)
```

Side effects are tool calls, memory writes, and final file writes. The kernel never touches the disk or the network directly — it emits `SideEffect::ToolCall(ToolRequest)` and waits for `KernelEvent::ToolResult(ToolResponse)`.

This is the LangGraph pattern stripped to its essentials and rewritten for auditability. Every state transition is logged to the lineage store before the next step runs, so an interrupted agent can resume byte-identically.

### 3.2 Reflection loop

Reflection is not a heuristic — it is a typed edge in the state graph. The canonical loop:

```
Draft --validate--> Validate
Validate --pass--> Sign
Validate --fail--> Reflect
Reflect --patch--> Draft       # bounded: max 5 patch attempts
Reflect --escalate--> Error    # after 5 failures, the kernel gives up and archives the failure for training
```

Failure archives are **first-class training data**. Every failure becomes an entry in the self-bootstrapping corpus under `data/failures/<session_id>.jsonl`, where the next fine-tune pass learns from it.

### 3.3 Determinism contract

Given the same `(SeedRequest, model_version, tool_receipts, rng_seed)`, two kernel runs MUST produce byte-identical signed output. This is enforced by:

- All LLM calls pinned to `temperature = 0` and seeded.
- All RNG calls routed through a kernel-owned xoshiro256** instance seeded from the session name.
- All tool calls recorded with their exact request + response so a replay can skip network I/O.
- All `.gseed` payloads canonicalized via JCS (RFC 8785) before signing.

The kernel ships a `replay` subcommand that takes a session ID and re-runs it without network access using only the recorded tool receipts. Replay must produce a byte-identical seed or the binary is considered broken.

## 4. Tool layer — concrete specification

Every tool is a typed, sandboxed, revocable capability. A tool is defined by:

```
trait Tool:
    fn name() -> &'static str
    fn schema() -> ToolSchema          # JSON Schema for args + result
    fn capabilities() -> Capabilities  # which sandbox permissions the call needs
    fn invoke(args: Value, ctx: ToolContext) -> Result<Value, ToolError>
```

### 4.1 Required tools (v1 — ship in the default build)

| Tool | Capabilities | Purpose | Implementation |
|---|---|---|---|
| `fs.read_file` | `fs(readonly, path_allowlist)` | Read a project file. | std filesystem, bounded to user-configured allowlist. |
| `fs.write_file` | `fs(write, path_allowlist)` | Write an agent-authored file inside the project tree. | std filesystem, atomic write + fsync. |
| `fs.list_dir` | `fs(readonly, path_allowlist)` | Directory listing. | std filesystem. |
| `fs.glob` | `fs(readonly, path_allowlist)` | Pattern search. | `globset` crate. |
| `terminal.run` | `proc(sandboxed)` | Run a command in the execution sandbox. | Docker / podman / bubblewrap per host. |
| `git.status` | `proc(sandboxed, git)` | Git status in the project tree. | `git2-rs` in a read-only worktree copy. |
| `git.diff` | `proc(sandboxed, git)` | Git diff. | `git2-rs`. |
| `git.commit` | `proc(sandboxed, git, write)` | Commit. Disabled by default in agent mode; requires explicit user enable. | `git2-rs`. |
| `test.run` | `proc(sandboxed)` | Run a project's test suite. | Language detection + standard runners (`pytest`, `vitest`, `cargo test`, `go test`). |
| `lint.run` | `proc(sandboxed)` | Run a project's linter. | `ruff`, `eslint`, `clippy`, `mypy`. |
| `code.execute` | `proc(sandboxed, ephemeral)` | Run a short code snippet in an ephemeral sandbox and capture stdout/stderr. | Docker image with Python/Node/Rust pre-installed. See §5. |
| `chem.lookup` | `read(chem_library)` | Look up a primitive from `seed-commons/libraries/chemistry.gspl` substrate cache. | In-process content-addressed store. |
| `seed.grow` | `compute` | Grow a `.gspl` source to a `.gseed.json` payload using the kernel compiler. | In-process GSPL compiler. No LLM. |
| `seed.validate` | `compute` | Run the 6-check validator (grow-twice + JCS hash + signature + round-trip + commons-lint + graph). | In-process. |
| `commons.query` | `read(seed_commons)` | Similarity search against the local seed commons via dimensional embeddings. | Qdrant embedded or `tantivy` + `hnsw` for pure-Rust. |
| `memory.recall` | `read(memory)` | Pull a prior session's lineage bundle for replay or learning. | RocksDB. |
| `memory.archive` | `write(memory)` | Store a signed seed's full lineage capsule. | RocksDB + `.gcapsule` file. |
| `web.search` | `net(domain_allowlist)` | Typed web search. **Optional**. Air-gap mode disables. | `searxng` instance, local or user-hosted. |
| `web.fetch` | `net(domain_allowlist)` | Fetch a URL and extract text + metadata. **Optional**. | `reqwest` + `readability-rs`. |
| `web.browse` | `net(domain_allowlist)` | Headless browser for JS-heavy pages. **Optional**. | `playwright` with a pinned Chromium. |
| `multimodal.analyze` | `compute` | Run a local vision/audio model against a local file (never the network). **Optional**. | `llama.cpp` multimodal or `whisper.cpp`. |

### 4.2 Sandbox capabilities

```
struct Capabilities:
    fs_readonly_paths: Array<Path>
    fs_write_paths:    Array<Path>
    proc_allow:        Bool
    proc_network:      NetworkPolicy   # None | DomainAllowlist | Unrestricted(off-by-default)
    max_runtime_ms:    Int
    max_memory_mb:     Int
    max_open_files:    Int
```

No tool call runs without an explicit Capabilities record. The kernel rejects a tool request whose capabilities exceed the session's policy. The default session policy is:

```
fs_readonly_paths = [project_root, seed_commons_cache, chemistry_cache]
fs_write_paths    = [project_root/seed-commons/work/, session_tmp]
proc_allow        = true
proc_network      = NetworkPolicy::None   # air-gap default
max_runtime_ms    = 120_000
max_memory_mb     = 4096
max_open_files    = 256
```

A user enables network by flipping one config flag. The agent will then expose `web.search`, `web.fetch`, `web.browse` as available tools. The default ships with network **off**.

### 4.3 Tool invocation pipeline

```
IntentOracle emits ToolCallIntent
  -> Kernel validates against session capabilities
  -> Kernel writes pre-call audit row to lineage store
  -> Kernel spawns sandbox (Docker/bubblewrap/firecracker)
  -> Tool runs with enforced capabilities
  -> Kernel reads stdout/stderr/exit_code
  -> Kernel writes post-call audit row (including sha256 of output)
  -> Kernel feeds ToolResult back into the state machine
  -> Every tool receipt is added to the lineage capsule of any seed that results
```

If the sandbox crashes, the kernel records the failure and routes to `Reflect`. It does not propagate host faults.

## 5. Execution sandbox

The execution sandbox is the single most dangerous component of the agent. It runs code generated by the LLM. It must be capability-scoped, ephemeral, and impossible to escape.

### 5.1 Backend selection (per host)

| Host | Primary | Fallback | Notes |
|---|---|---|---|
| Linux | `bubblewrap` + user namespaces | `firejail` | No root required. Fast. |
| Linux (preferred when available) | `firecracker` microVM | `podman` rootless | Better isolation, slightly slower spawn. |
| macOS | `podman machine` | `docker desktop` | Requires a VM. |
| Windows | `wsl2 + bubblewrap` | `docker desktop` | Runs inside WSL2. |

The agent detects the host at startup and picks the strongest available backend. All backends satisfy the same Sandbox contract:

```
trait Sandbox:
    fn spawn(spec: SandboxSpec) -> Result<SandboxHandle, SandboxError>
    fn stdin(handle: SandboxHandle, bytes: Bytes) -> Result<(), SandboxError>
    fn wait(handle: SandboxHandle, timeout_ms: Int) -> Result<SandboxOutcome, SandboxError>
    fn kill(handle: SandboxHandle) -> Result<(), SandboxError>
```

### 5.2 Sandbox spec

```
struct SandboxSpec:
    image_ref:       Symbolic          # "gspl/exec:py3.12-node20-rust1.82" (content-addressed)
    command:         Array<String>
    env:             Map<String, String>
    mount_readonly:  Array<(HostPath, GuestPath)>
    mount_writable:  Array<(HostPath, GuestPath)>
    network:         NetworkPolicy
    memory_mb:       Int
    cpu_quota_pct:   Int
    timeout_ms:      Int
```

Images are content-addressed. The default image ships Python 3.12, Node 20, Rust 1.82, git 2.45, ruff, eslint, mypy, pytest, vitest, the GSPL compiler, and nothing else. It weighs ~650 MB. A user can build a custom image by writing a `image.toml` — there is no Dockerfile DSL the agent is coupled to.

### 5.3 Execution safety invariants

- No sandbox ever shares a writable mount with another sandbox.
- Every sandbox is spawned fresh and destroyed after `wait` returns.
- The agent enforces a per-session sandbox count quota (default 200 spawns/session) to prevent runaway loops.
- All sandbox stdout/stderr is size-capped (default 16 MiB) before being fed back to the kernel.
- The kernel treats sandbox output as **untrusted**. It is piped through the same injection-defense filter as web content: instructions found in sandbox output never become new kernel commands.

## 6. Memory system

Three tiers, each with an explicit lifetime.

### 6.1 Short-term: session scratchpad

- **Store:** in-memory `BTreeMap<SessionId, SessionState>`.
- **Lifetime:** single `grow` invocation.
- **Contents:** kernel state, current draft, in-flight tool calls, reflection history.
- **Privacy:** never written to disk unless the session completes and archives.

### 6.2 Mid-term: project brain

- **Store:** RocksDB at `~/.paradigm/brain/<project_id>/`.
- **Lifetime:** until the user deletes it.
- **Contents:** project DNA (naming, patterns, conventions from `project-dna` skill), recent sessions, local fine-tune dataset deltas.
- **Privacy:** local-only. The Foundation never has access. Ever.

### 6.3 Long-term: lineage + commons cache

- **Store:** content-addressed `.gcapsule` files at `~/.paradigm/lineage/`.
- **Lifetime:** append-only, bounded by disk quota. LRU eviction of leaf capsules; internal (referenced) capsules never evicted.
- **Contents:** every signed seed the agent has produced or consumed, with full lineage graphs.

### 6.4 Retrieval

The agent does RAG with two indexes:

1. **Dimensional index (similarity search).** A local HNSW index built on `dimensional` gene embeddings. Default backend: embedded Qdrant. Fallback: `hnsw_rs` + `tantivy` for a zero-daemon build. Query tool: `commons.query`.

2. **Symbolic index (exact match).** A `tantivy` full-text index over seed names, citations, IUPAC strings, KEGG IDs, etc. Query tool: `commons.query` with `mode: "symbolic"`.

Qdrant vs Chroma vs Weaviate tradeoffs the shipped build considered:

| Store | Local-first | Runs without daemon | Pure Rust | Verdict |
|---|---|---|---|---|
| Qdrant | yes | embedded mode | partial | **Default.** Mature, local, embedded mode shipped. |
| Chroma | yes | requires Python | no | Rejected: Python coupling contradicts single-binary goal. |
| Weaviate | yes | requires daemon | no | Rejected: daemon is a cloud-shaped pattern. |
| `hnsw_rs` | yes | yes | yes | Shipped as the zero-daemon fallback. |

## 7. Multi-agent topology

The agent ships 8 sub-agents, inherited from `gspl-agent-full-capacity.md`. The runtime realises them as in-process actors, **not** as separate LLM processes, because the LLM is only ever invoked by IntentOracle and CodeSmith (and CodeSmith is allowed zero LLM tokens in the final pass). Every other sub-agent is a pure function over typed state.

### 7.1 Sub-agent actor table

| Sub-agent | LLM use | Tools used | Deterministic? |
|---|---|---|---|
| IntentOracle | **yes**, bounded | none | No (LLM non-determinism quarantined here) |
| Researcher | no | `web.search`, `web.fetch`, `chem.lookup`, `commons.query` | Yes (given fixed tool receipts) |
| CodeSmith | no (template-driven) | `fs.read_file`, `seed.grow` | Yes |
| Validator | no | `seed.validate`, `seed.grow`, `test.run`, `lint.run` | Yes |
| Evolver | no | `seed.grow` (many times), `commons.query` | Yes |
| Composer | no | `seed.grow`, `chem.lookup`, `commons.query` | Yes |
| MemoryArchivist | no | `memory.archive` | Yes |
| SovereignSigner | no | (in-process ECDSA-P256) | Yes |

The "LLM is confined to Intent" rule means the agent's determinism surface is as small as it can possibly be. Everything past IntentOracle is a deterministic compiler over typed intent.

### 7.2 Coordination pattern

Actors do not message each other directly. They post events to the kernel's event queue, and the kernel dispatches the next state. This is the AutoGen "topology is code" pattern done in-process, without the cloud-shaped message-bus assumption CrewAI bakes in.

```
IntentOracle --Intent--> Kernel
Kernel --Plan--> Researcher
Researcher --Bundle--> Kernel
Kernel --Draft--> CodeSmith
CodeSmith --Draft--> Kernel
Kernel --Validate--> Validator
Validator --Report--> Kernel
Kernel --(pass)--> SovereignSigner --Signed--> MemoryArchivist
Kernel --(fail)--> Reflect --> CodeSmith (patch)
```

## 8. Self-improvement loop

The agent improves itself three ways, all compatible with 100% local execution.

### 8.1 Corpus growth

Every signed seed the agent produces is appended to a local training corpus at `~/.paradigm/training/seeds.jsonl`. Every failure is appended to `~/.paradigm/training/failures.jsonl`. Both are plain newline-delimited JSON with full lineage capsules.

### 8.2 Local fine-tune passes (QLoRA + Unsloth)

Per `gspl-agent-full-capacity.md` §6, the agent runs QLoRA fine-tunes on the local corpus against a user-chosen base model. The runtime exposes a single command:

```
paradigm agent fine-tune --base deepseek-coder:33b --dataset ~/.paradigm/training/ --output ~/.paradigm/adapters/
```

This launches Unsloth in the execution sandbox with the local GPU passed through. Fine-tune output is a LoRA adapter file that the agent signs as a `.gseed` (the adapter itself is a seed, subject to the same sovereignty rules). The user loads the adapter by name at inference time.

### 8.3 Evaluation — a GSPL-native SWE-bench

Standard agent benchmarks (SWE-bench, AgentBench) don't measure what matters for this agent. The runtime ships a **GSPL eval harness** instead:

```
paradigm agent eval --suite commons-v1 --adapter none
paradigm agent eval --suite commons-v1 --adapter fine-tune-2026-04.gseed
```

The `commons-v1` suite is a fixed set of ~200 prompts ("generate a melancholy bard sprite," "grow a candle flame from the chemistry library," "breed two character seeds and validate lineage") with expected output hashes. Every adapter is scored against:

1. **Compile pass rate.** Did `seed.grow` succeed?
2. **Determinism pass rate.** Did grow-twice produce byte-identical output?
3. **Signature pass rate.** Did the output sign cleanly with ECDSA-P256 over JCS?
4. **Commons-lint pass rate.** Did the 8-point contract checklist pass?
5. **Similarity-to-reference.** Cosine similarity of the output seed's `dimensional` gene to a reference seed embedding (for prompts with canonical expected outputs).

A fine-tune pass is accepted only if it strictly dominates the previous adapter on metrics 1-4 and does not regress more than 2% on metric 5. Otherwise the adapter is rolled back.

## 9. IDE integration — how this surfaces to a human

The runtime is invisible to users who only ever call the CLI. For IDE integration the agent exposes an LSP-compatible server on a local Unix socket:

```
paradigm agent serve --lsp
```

An editor plugin (VS Code, Zed, Neovim, Helix, Emacs) connects via LSP and gets:

- **Inline grow.** Cursor inside a `.gspl` file, trigger `Paradigm: Grow`, the editor calls `seed.grow`, the kernel returns a diagnostic list of validation issues inline.
- **Seed search.** A fuzzy finder over `commons.query` lets the user jump to any seed in the commons.
- **Agent chat.** A sidebar chat routes to IntentOracle and streams the kernel state transitions live.
- **Lineage viewer.** Open any `.gseed.json` in the editor and the plugin renders the lineage DAG.

The LSP integration does not require Continue.dev, Cursor, or any third-party plugin. It ships as a first-party VS Code extension in `sdks/vscode/` (to be written in a later pass — tracked in the Gap Audit under P1-3).

## 10. What this runtime is **not**

- **Not a generic coding assistant.** It is purpose-built for GSPL. It compiles intent into signed seeds. It does not ship a general-purpose "write any code" mode.
- **Not Cursor.** Cursor is a closed IDE fork with a hosted backend. This runtime is a local agent with an LSP front-end that plugs into any editor. No fork, no hosting, no cloud.
- **Not Devin.** Devin runs in a datacenter-side container with internet-scale tool access and a hosted browser. This runtime runs in a user's laptop with an optional, off-by-default, domain-allowlisted browser.
- **Not an orchestration framework.** It does not expose LangGraph/AutoGen/CrewAI-style APIs for building arbitrary agent pipelines. It ships one agent and one topology, because the topology is the product.
- **Not a cloud service.** There is nothing to sign up for. The Foundation does not run this for you. You run it for yourself.

## 11. Framework debt — what we explicitly do not borrow

| Framework | Borrowed | Rejected | Why |
|---|---|---|---|
| LangGraph | State-machine topology, reflection-as-edge pattern | Python runtime, LangChain ecosystem coupling, implicit cloud assumptions | We need a single-binary, sandboxed runtime with deterministic replay. LangGraph's state model is brilliant; its dependency surface is not. |
| AutoGen | Actor-model multi-agent coordination, "topology is code" | Message-bus cloud orientation, GroupChat abstraction | Message-bus is a cloud-shaped pattern. We run in-process actors over a typed event queue. |
| CrewAI | Role-based sub-agent decomposition (Architect/Builder/Reviewer inspired our 8 sub-agents) | Opinionated task DSL, YAML-driven wiring | We need Rust-typed state transitions, not YAML. |
| OpenAI Agents SDK | Tool-schema + structured output pattern | Provider coupling to openai.com | Our tool schemas are the same shape; the provider is swappable. |
| Claude Agent SDK | Task-planner + executor split | Cloud-only execution, no local fine-tune path | We take the split and put it in a local binary. |
| Cursor / Windsurf | Repo-wide context awareness | Closed fork of VS Code, hosted backend | We reproduce the UX with an LSP plugin over the open VS Code fork. |
| Devin | Full-autonomy pipeline | Datacenter execution, closed runtime | We reproduce the autonomy locally with a sandboxed runtime the user owns. |

The through-line: every framework above is excellent at one thing and assumes a cloud-shaped deployment for the rest. This runtime takes the excellent parts and rewrites the deployment assumptions for local-first, single-binary, sovereign execution.

## 12. Implementation roadmap

| Week | Milestone |
|---|---|
| 1 | Kernel state machine scaffold (Rust). LLM provider trait with ollama + llama.cpp backends. Deterministic RNG. |
| 2 | Tool trait, Capabilities, bubblewrap sandbox on Linux, tests. |
| 3 | fs.* tools, terminal.run, test.run, lint.run, git.* tools. |
| 4 | GSPL compiler in-process (`seed.grow`, `seed.validate`). |
| 5 | IntentOracle sub-agent with ollama backend. CodeSmith, Validator, SovereignSigner (ECDSA-P256, JCS, SHA-256 per ADR-009). |
| 6 | Memory tier 1+2+3. Qdrant embedded index. Lineage capsule format. |
| 7 | Researcher + commons.query + chem.lookup. Web tools behind the `--enable-net` flag. |
| 8 | Multimodal.analyze (optional). Evolver sub-agent. |
| 9 | LSP server + VS Code extension skeleton. |
| 10 | QLoRA fine-tune sandbox + `paradigm agent fine-tune` command. |
| 11 | `commons-v1` eval suite + `paradigm agent eval`. |
| 12 | Hardening: injection-defense filter on every untrusted surface, replay test harness, 0.1.0 tag. |

## 13. Success criteria

A shipped runtime satisfies all of:

1. **Single binary.** One executable, no daemons required for the default build.
2. **Air-gap grow.** `paradigm agent grow "melancholy bard in wool cloak"` produces a signed `.gseed` on an unplugged laptop.
3. **Determinism parity.** `paradigm agent replay <session_id>` reproduces the original seed byte-for-byte.
4. **Commons-v1 eval ≥ 99% pass** on metrics 1–4 with the default model (deepseek-coder:33b).
5. **No cloud dependency.** `grep -r 'paradigm.app\|amazonaws\|googleapis' release-binary/` returns zero matches.
6. **Free forever.** The license in the binary's `--license` command returns the GSPL Open Specification License text verbatim.

## 14. Open follow-ups (queued for future passes)

- `intelligence/execution-sandbox.md` — per-backend sandbox implementation details with threat model.
- `intelligence/memory-system.md` — schema of RocksDB column families and capsule layout.
- `intelligence/lsp-protocol.md` — concrete wire protocol for the editor integration.
- `intelligence/eval-harness.md` — how prompts are authored for `commons-v1` and how the reference embeddings are computed.
- `adr/0NN-execution-sandbox-choice.md` — ADR recording the bubblewrap/firecracker/podman decision.
- `sdks/vscode/` — the first-party VS Code extension implementing the LSP client.

---

**The agent is the population engine for the commons. The commons is the network effect that turns GSPL from a specification into a substrate the world actually runs. This runtime is the concrete machinery that makes that population possible on hardware every reader already owns.**
