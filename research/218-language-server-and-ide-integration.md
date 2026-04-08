# 218 — Language server and IDE integration

## Question
What is the typed Language Server Protocol implementation that enables substrate creators to author gseeds in any LSP-compatible editor (VS Code, Cursor, Neovim, Zed, JetBrains) with autocomplete, validation, hover documentation, go-to-definition, and refactoring across the typed substrate surface?

## Why it matters (blast radius)
Many creators (especially AI-augmented creators using Cursor / Claude Code / Copilot) author in code editors, not GUI Studios. Without an LSP, the substrate is invisible to that workflow. With one, every modern editor becomes a substrate authoring surface and the substrate's typed schemas drive autocomplete and validation directly in the editor.

## What we know from the spec
- Brief 217 — CLI and headless toolchain.
- Brief 180 — dialogue editor (typed expression DSL).
- Brief 187 — mod surface.
- Briefs 152-216 — substrate primitives.

## Findings
1. **LSP server as `gspl-lsp` binary.** Substrate ships an LSP server binary `gspl-lsp` per host platform. Editors launch it via standard LSP discovery.
2. **Capabilities supported.** v0.1 LSP supports: textDocument/completion, textDocument/hover, textDocument/definition, textDocument/references, textDocument/publishDiagnostics, textDocument/formatting, textDocument/rename, textDocument/codeAction, workspace/symbol, workspace/configuration. Sufficient for full IDE-level authoring.
3. **File types handled.** `.gspl.json` (gseed bundle JSON), `gspl.toml` (project manifest), `*.gspl.expr` (typed expression DSL files from Brief 180), `*.gspl.recipe.json` (recipe composition files from Brief 208).
4. **Schema-driven autocomplete.** Substrate primitive schemas (Briefs 152-216) drive autocomplete. Typing inside a `level.scene` gseed surfaces valid field names with type signatures and documentation.
5. **Live validation.** LSP runs the substrate validator on save (and on debounced edit) and surfaces typed errors as diagnostics. Errors include the typed gate they violated and a creator-actionable hint.
6. **Hover documentation.** Hovering over a typed field shows the field's documentation, valid value range, and example. Drawn from substrate spec annotations.
7. **Go-to-definition.** Cross-references between gseeds (e.g., entity referencing a component def) navigate via go-to-definition. Recipe references navigate to recipe gseeds.
8. **Refactoring.** Rename a gseed and all references update across the project. Move a gseed between files; references re-resolve automatically.
9. **Inline replay scrubbing (advanced).** Optional editor extension overlays replay state on the gseed file: when a typed mutation is selected, the editor previews the resulting state. Implemented as a custom editor extension that shells out to `gspl playtest` for replay execution.
10. **AI-agent integration.** LSP exposes typed schemas to agents (Claude Code, Cursor, Copilot). Agents author gseeds with substrate validation feedback in the editor — closing the loop between AI generation and substrate correctness.
11. **Editor-specific extensions.** Substrate ships first-class extensions for VS Code, Cursor, Neovim, Zed. Other LSP-compatible editors get the LSP server but no editor-specific UI affordances in v0.1.
12. **Validation contract.** LSP server boot validates: substrate version compatibility, project manifest valid, schema cache fresh.

## Risks identified
- **LSP performance.** Large projects with many gseeds may stress the LSP. Mitigation: incremental validation (only revalidate touched gseeds); schema cache.
- **Editor UI variance.** Different editors render LSP features differently. Mitigation: substrate's first-class editor extensions provide consistent UX in the four supported editors.
- **Custom expression DSL syntax highlighting.** Brief 180 expression DSL needs syntax highlighting. Mitigation: substrate ships TextMate grammar files for editors that support them.
- **Hover doc drift.** Documentation can drift from spec. Mitigation: substrate schemas are the single source of truth; LSP reads doc strings from schemas, not separate docs.

## Recommendation
Specify the LSP as a `gspl-lsp` binary per host platform implementing 10 LSP capabilities, schema-driven autocomplete and validation, hover documentation drawn from substrate spec, go-to-definition across gseed cross-references, full refactoring support, AI-agent integration via schema exposure, and first-class editor extensions for VS Code / Cursor / Neovim / Zed.

## Confidence
**4.5 / 5.** LSP implementation is well-precedented. The novelty is the schema-driven authoring with substrate validation feedback in-editor. Lower than 5 because LSP performance under large projects needs Phase-1 measurement.

## Spec impact
- New spec section: **Language server and IDE integration specification**.
- Adds the `gspl-lsp` binary contract with 10 LSP capabilities.
- Adds the file type associations.
- Adds the four supported editor extension list.
- Cross-references Briefs 180, 187, 208, 217.

## New inventions
- **INV-945** — `gspl-lsp` LSP server binary providing full substrate authoring in any LSP-compatible editor: substrate is editor-agnostic.
- **INV-946** — Schema-driven autocomplete and validation directly from substrate primitive schemas: the substrate's typed schemas are themselves the authoring surface.
- **INV-947** — Hover documentation drawn from substrate spec annotations as single source of truth: doc drift is structurally impossible.
- **INV-948** — Cross-gseed go-to-definition and rename refactoring: substrate references navigate as native code symbols would.
- **INV-949** — Inline replay scrubbing as advanced editor extension overlaying mutation state: editor becomes a debugger for the substrate runtime.
- **INV-950** — AI-agent integration via schema exposure to in-editor agents (Cursor / Claude Code / Copilot): agents generate substrate-correct gseeds with live validation feedback.
- **INV-951** — Four first-class editor extensions (VS Code / Cursor / Neovim / Zed) with consistent UX: substrate provides the canonical IDE experience for the dominant editor stack.

## Open follow-ups
- JetBrains plugin (IntelliJ / Rider) — deferred to v0.2.
- Phase-1 LSP performance under large projects.
- Visual graph editing as VS Code custom editor — deferred to v0.3.
- Replay scrubbing UX refinement — Phase 1.

## Sources
1. Brief 180 — Dialogue and quest editor.
2. Brief 187 — Mod and plugin surface.
3. Brief 208 — Recipe composition.
4. Brief 217 — CLI and headless toolchain.
5. LSP specification (microsoft.github.io/language-server-protocol/).
6. Cursor LSP integration documentation.
7. VS Code extension API documentation.
