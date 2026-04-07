# 124 — Cursor, Aider, Cline, Continue, Roo Code, OpenHands teardown

## Question

What do the leading open-source and hybrid coding agents (Cursor, Aider, Cline, Continue, Roo Code, OpenHands) teach about agent discipline, IDE integration, and open-source agent UX that GSPL must absorb?

## Why it matters (blast radius)

This layer of the market is where the fastest iteration happens. Cursor's editor-native tooling, Aider's terse diff discipline, Cline's live tool watching, Continue's configurability, Roo's fork-friendly posture, and OpenHands' sandboxed agent loops are each battle-tested at scale. Each encodes a lesson GSPL can absorb for free.

## What we know from the spec

- Brief 103 (studio) ships a creator UI layer.
- Brief 017 / 019 (plugin ABI) support extensibility.
- Brief 053 (local-first) commits to local execution.

## Findings

### 1. Cursor: editor-native agent

Cursor is a VS Code fork with the agent baked into the editor. The agent can see the open files, the cursor position, the selection, the terminal, and the diagnostics. Context is ambient, not explicitly built. [1]

- **Strengths:** the best "ambient context" in any coding agent; apply-diff affordance is buttery; multi-file edit works well; Composer mode is powerful.
- **Weaknesses:** not fully open-source; VS Code fork has update lag; the ambient context can leak files the user didn't intend to share.

**GSPL lesson:** ambient context from the editor is a huge UX win. The GSPL studio (Brief 103) and the GSPL CLI need a mechanism to pull ambient signals (open file, selection, recent edits) without forcing the creator to type them.

### 2. Aider: CLI diff discipline

Aider is a Python CLI that pairs with git. Its discipline is: every change is a git commit; every commit has a semantic message; the model emits edits as diffs; the user reviews each one. [2]

- **Strengths:** the tightest git integration of any coding agent; the "edit-as-diff" discipline prevents scope creep; works with any model via LiteLLM.
- **Weaknesses:** CLI-only; no GUI; requires the creator to be comfortable with git.

**GSPL lesson:** the commit-per-change discipline is the right default. GSPL should make every accepted substrate mutation a signed gseed that corresponds to a git commit in the creator's project namespace. One-to-one mapping.

### 3. Cline (formerly Claude Dev): autonomous loop with user veto

Cline is a VS Code extension that runs Claude in an autonomous loop with an explicit user-veto step after every tool call. The user sees the diff or command before it's applied. [3]

- **Strengths:** the clearest "trust but verify" UX; user feels in control; the tool-call preview is the right primitive.
- **Weaknesses:** the verify step adds friction for trusted workflows; scaling to many small changes is tedious.

**GSPL lesson:** the tool-call preview with user veto is the right default for sensitive tasks. The permission model (Brief 033) should support preview-by-default with a per-tool override.

### 4. Continue: the configurable open-source baseline

Continue is a VS Code extension that's deeply configurable via a `config.yaml`. Creators define their own models, context providers, slash commands, and tools. [4]

- **Strengths:** the most flexible OSS agent; the config file is the contract; supports any model backend; the context-provider abstraction is clean.
- **Weaknesses:** the flexibility is overwhelming; few creators configure it meaningfully.

**GSPL lesson:** a config file is the right abstraction for creator-level customization. GSPL's creator config should be a signed gseed in the creator's namespace, not a stray YAML. This gives lineage for free.

### 5. Roo Code: Cline fork with more tools

Roo Code is a community fork of Cline that adds more tools, more modes, and more customization. It's where the OSS community is iterating fastest on Cline's base pattern. [5]

**GSPL lesson:** fork-friendly licenses and extensibility drive adoption. GSPL's Brief 019 plugin ABI must be trivially forkable and the substrate must make forking productive (signed forks, forever-credit lineage).

### 6. OpenHands (formerly OpenDevin): agent in a sandbox

OpenHands runs agents in Docker sandboxes with a browser, file system, and terminal. The agent loop is autonomous and the sandbox is disposable. [6]

- **Strengths:** strong sandboxing; the disposable container is the right isolation primitive; the browser tool expands the action space meaningfully.
- **Weaknesses:** heavy (Docker dependency); slow to start; overkill for small edits.

**GSPL lesson:** sandboxing is a security and reproducibility primitive. Brief 033's permission model should support a "sandbox for untrusted code" mode and Brief 045's leak-resilience work should reuse the sandbox pattern.

### 7. The "apply diff" primitive converged

Every mature coding agent converged on an "apply this diff to this file" primitive. The diff is the unit of work; the model emits it; the runtime applies it with a three-way merge if needed.

**GSPL lesson:** the modifier-surface DSL (Brief 023) should expose a first-class "apply diff" primitive that is git-aware and substrate-aware.

### 8. Context providers as plugins

Continue, Cline, and Cursor all expose "context providers" as plugins: @file, @folder, @url, @docs, @search. The creator can reference external context with a single token.

**GSPL lesson:** GSPL's retrieval should expose a similar `@` syntax in the CLI and studio for explicit context injection. This is an action-space primitive, not a separate tool.

### 9. Live tool watching

Cline, Cursor, and OpenHands all show live tool execution: the creator watches commands run, files change, and errors appear in real time. This is the trust-building UX.

**GSPL lesson:** the studio (Brief 103) must show live substrate mutations: every signed gseed creation, every federation update, every grounding audit. Live substrate watching is the creator's assurance layer.

### 10. Model-agnostic backends

Every open-source agent supports multiple backends (OpenAI, Anthropic, Google, local via Ollama, etc.) via LiteLLM or similar. Backbone-agnosticism is the default.

**GSPL lesson:** confirmed from Brief 122. GSPL's reasoning kernel must be backbone-agnostic.

### 11. The "rules files" pattern

Cursor's `.cursorrules`, Continue's project-level config, and Aider's conventions file all encode "how to work in this project" as a persistent file the agent reads at startup.

**GSPL lesson:** this is exactly what GSPL's signed project-convention gseeds should do. The rules file is a signed gseed in `project://<name>/conventions/` and the agent reads it on every turn.

### 12. The "memory bank" pattern

Cline has a "memory bank" mode where the agent maintains a set of markdown files in `.clinerules/` that capture learned project context. The memory bank is manually curated by the agent with user approval.

**GSPL lesson:** substrate-native memory (Brief 127) replaces the memory bank. GSPL's episodic and procedural tiers capture the same signal with signed lineage and federation support.

### 13. Model Context Protocol as the converging standard

Every agent from 2024 forward added MCP support. MCP has won the tool interoperability layer in the open-source ecosystem.

**GSPL lesson:** MCP compatibility (Brief 117) is table stakes.

### 14. The GitHub Copilot-as-baseline

Copilot's inline completions set the floor: every coding agent must at least match inline completion latency and quality. This is the "table stakes" capability.

**GSPL lesson:** inline completion is a primary UX surface that GSPL's creator tool must offer. This requires a fast tier of the model (Brief 110's expert routing) dedicated to completion latency.

## Inventions to absorb

Tier W hooks for Brief 126 and Brief 128:

- **Ambient context pull from editor signals.** The studio should read open files, selection, recent edits, diagnostics without asking.
- **Commit-per-change discipline.** Every accepted substrate mutation maps to a git commit.
- **Tool-call preview with user veto.** Permission model default.
- **Config-as-signed-gseed.** Creator-level config lives in the substrate.
- **Fork-friendly plugin ABI.** Signed forks are first-class.
- **Sandbox-for-untrusted-code mode.** Docker-style isolation for risky operations.
- **Apply-diff as first-class modifier-surface primitive.**
- **`@` context providers in CLI and studio** for explicit context injection.
- **Live substrate mutation stream** as the studio's trust surface.
- **Backbone-agnostic reasoning kernel** (already confirmed).
- **Signed project-convention gseeds** replace `.cursorrules`-class files.
- **Substrate-native memory** replaces per-agent memory banks.
- **MCP compatibility** as table stakes.
- **Inline completion latency tier** routed through a fast expert (Brief 110).

## Risks identified

- **Editor integration is expensive to maintain.** Mitigation: CLI and studio are primary; editor integration is a Brief 019 plugin, not a product surface.
- **Ambient context can leak private files.** Mitigation: creator explicitly marks namespaces as private; ambient reads are scoped to the active namespace only.
- **Preview-by-default adds friction.** Mitigation: permission tiers (sensitive vs trusted) with per-tool overrides.
- **Sandbox overhead is heavy.** Mitigation: opt-in for untrusted code; native execution is the default.

## Recommendation

1. **Ambient context is a primary studio feature.** Brief 103 must match Cursor's ambient context UX, scoped to the creator's active namespace.
2. **Commit-per-change discipline.** Signed gseed ↔ git commit one-to-one.
3. **Tool-call preview is the default** for sensitive namespaces and modifiable tools.
4. **Config-as-signed-gseed.** No stray YAML; the config is a substrate entity.
5. **Fork-friendly plugin ABI** confirmed (Brief 019).
6. **Sandbox mode for untrusted code** via Brief 033.
7. **`@` context providers** in CLI and studio.
8. **Inline completion latency tier.** Brief 110's expert routing dedicates one expert to completion speed.
9. **MCP compatibility is table stakes.** Brief 117.
10. **Live substrate mutation stream** is the studio trust surface.

Feeds Brief 126 and Brief 128.

## Confidence

**4.5/5.** All six systems are public and inspectable. The converged patterns (diff discipline, preview-with-veto, MCP, context providers) are strong evidence that these are the right primitives. The 3.5/5 piece is the editor-integration cost — a full Cursor-class editor is a significant engineering investment that GSPL may defer.

## Spec impact

- Brief 019 (plugin ABI) needs fork-friendly confirmation.
- Brief 033 (permissions) needs preview-with-veto addendum.
- Brief 103 (studio) needs ambient context and live mutation stream addenda.
- Brief 126 owns the integration.
- Brief 128 owns the tool-use primitives.

## Open follow-ups

- Ambient context scope rules.
- Sandbox mode selection heuristics.
- Inline completion latency budget.

## Sources

1. Cursor documentation and changelog, 2024–2025.
2. Aider documentation, Paul Gauthier, 2023–2025.
3. Cline (Claude Dev) GitHub and documentation, 2024–2025.
4. Continue documentation, continue.dev, 2024–2025.
5. Roo Code GitHub, 2024–2025.
6. OpenHands (OpenDevin) documentation, 2024–2025.
