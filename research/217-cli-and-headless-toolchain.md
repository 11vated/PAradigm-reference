# 217 — CLI and headless toolchain

## Question
What is the typed CLI and headless toolchain that enables substrate creators (and AI coding agents) to author, sign, validate, export, and deploy gseed bundles from the command line without launching the Studio GUI, with scriptable workflows for CI integration and bulk operations?

## Why it matters (blast radius)
Studio (Briefs 177-187) is the GUI authoring surface. The CLI is the second authoring surface — required for AI coding agents, CI/CD pipelines, automation scripts, and creators who prefer text-based workflows. Without a complete CLI, the substrate is GUI-locked and cannot integrate with modern dev workflows or be driven by Claude Code itself.

## What we know from the spec
- Briefs 152-187 — substrate primitives and authoring surfaces.
- Briefs 188-196 — engine export pipelines.
- Brief 185 — playtest harness with replay verifier.

## Findings
1. **Single binary `gspl`.** Substrate ships a single CLI binary `gspl` per host platform (Linux / macOS / Windows). All operations are subcommands. No additional installs required.
2. **Subcommand surface.** Top-level subcommands: `init` (scaffold new project), `validate` (sign-time validate gseeds), `sign` (sign a gseed bundle), `export` (run engine export), `playtest` (run playtest harness), `replay` (verify a replay), `parity` (run parity test suite from Brief 196), `lint` (typed schema lint), `inspect` (dump gseed structure), `migrate` (apply schema migrations), `mod` (mod publishing per Brief 187), `recipe` (instantiate recipe from Briefs 197-208), `compose` (compose recipes per Brief 208), `serve` (run substrate dev server with hot reload).
3. **Stdin/stdout idiomatic.** Subcommands read gseed bundles from stdin and write to stdout where applicable, enabling Unix-style pipelines. JCS canonical JSON encoding ensures pipe-safety.
4. **Typed exit codes.** Each subcommand exits with typed exit codes per substrate convention: 0 success, 1 generic failure, 2 validation error, 3 sign-verification failure, 4 unsupported pattern, 5 export error, etc. Documented in `gspl --exit-codes`.
5. **Machine-readable output.** Default output is human-readable; `--json` flag emits structured JSON for programmatic consumption. CI integrations consume `--json`.
6. **Headless engine launch.** `gspl playtest` launches the substrate runtime in headless mode without any engine target — pure substrate kernel execution. Useful for CI determinism tests that don't need a render surface.
7. **AI agent integration.** CLI is designed to be driven by AI coding agents (Claude Code, etc.). Each subcommand surfaces structured input/output schemas via `gspl <subcommand> --schema`. Agents discover the CLI's full capability surface programmatically.
8. **Project file format.** Substrate projects have a typed `gspl.toml` manifest declaring: substrate version, dependencies (recipes, mods, asset packs), default export targets, default test config. Mirrors `Cargo.toml` / `package.json` conventions.
9. **Workspace mode.** `gspl` supports multi-package workspaces (one repo, multiple gseed bundles) via typed `gspl.workspace.toml`. Common for studios with shared substrate libraries.
10. **Plugin discovery.** CLI auto-discovers locally installed substrate plugins (Brief 187 mods with capability `cli-extension`) and exposes their subcommands inline. Enables creator extensions without forking the binary.
11. **Cross-compile.** CLI supports cross-compilation: invoking `gspl export --target unity --host-os linux` from Linux produces a Unity project tree consumable on macOS / Windows. Eliminates Mac dependency for iOS-targeting macOS-only builds where possible.
12. **Validation contract.** Sign-time gates: `gspl.toml` valid, declared substrate version matches installed binary, dependencies resolve.

## Risks identified
- **Subcommand surface bloat.** 14+ subcommands risk a sprawling CLI. Mitigation: typed subcommand schemas + autocomplete shells + clear documentation; structure mirrors `cargo` / `git` for familiarity.
- **Cross-platform single binary.** Statically linking everything inflates binary size. Mitigation: ~50 MB binary acceptable for v0.1; future versions can split.
- **Plugin security.** CLI plugins run with full local filesystem access. Mitigation: capability manifest from Brief 187 applies; CLI plugins must declare which paths they touch.
- **Stdout pipe-safety.** Mixing JSON output with progress logs corrupts pipes. Mitigation: progress goes to stderr; stdout is pure data.
- **AI agent error handling.** Agents need actionable error messages. Mitigation: typed exit codes + structured `--json` errors with creator-actionable hints.

## Recommendation
Specify the CLI as a single `gspl` binary per host platform with 14 typed subcommands, JCS-canonical stdin/stdout, typed exit codes, machine-readable `--json` output mode, headless engine launch, AI agent integration via schema introspection, `gspl.toml` project manifest, multi-package workspaces, plugin auto-discovery, and cross-compilation support.

## Confidence
**4.5 / 5.** CLI design is well-precedented (cargo / git / npm). The novelty is the AI-agent-first design with schema introspection. Lower than 5 because cross-compilation across all eight engine targets has platform-specific quirks needing Phase-1 measurement.

## Spec impact
- New spec section: **CLI and headless toolchain specification**.
- Adds the `gspl` binary contract with 14 typed subcommands.
- Adds the `gspl.toml` project manifest schema.
- Adds typed exit codes table.
- Cross-references Briefs 152-216.

## New inventions
- **INV-937** — Single-binary `gspl` CLI with 14 typed subcommands covering the full substrate surface: substrate authoring is CLI-complete, not GUI-only.
- **INV-938** — JCS-canonical stdin/stdout pipe-safe CLI design: substrate gseeds compose via Unix pipelines.
- **INV-939** — Typed exit codes per substrate convention: CI integrations and AI agents consume structured failure semantics.
- **INV-940** — AI-agent-first CLI design with `--schema` introspection: agents discover the substrate's full surface programmatically without documentation parsing.
- **INV-941** — Typed `gspl.toml` project manifest mirroring Cargo / npm conventions: substrate projects are familiar text-based artifacts.
- **INV-942** — Multi-package workspace support via `gspl.workspace.toml`: studios with shared substrate libraries get monorepo-friendly tooling.
- **INV-943** — CLI plugin auto-discovery via Brief 187 mod capability: creators extend the CLI surface without forking the binary.
- **INV-944** — Cross-compilation across engine targets from any host OS where possible: substrate eliminates host-OS lock-in for export pipelines.

## Open follow-ups
- iOS / Apple platform export from non-Mac hosts — Phase 1 (likely deferred to v0.3).
- CLI shell autocomplete (bash / zsh / fish / PowerShell) — v0.2.
- CLI telemetry (creator opt-in usage signals) — deferred to v0.3 with Brief 214.
- TUI (text UI) interactive mode — deferred to v0.3.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 187 — Mod and plugin surface.
3. Brief 196 — Cross-engine parity test suite.
4. Brief 197 — 2D platformer recipe.
5. Brief 208 — Recipe composition.
6. Cargo CLI design — rust-lang.
7. JCS specification (RFC 8785).
8. Git CLI design conventions.
