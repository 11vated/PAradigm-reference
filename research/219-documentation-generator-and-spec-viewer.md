# 219 — Documentation generator and spec viewer

## Question
What is the typed documentation generator and spec viewer that derives complete substrate documentation, recipe documentation, and project documentation from substrate schemas and signed gseeds — eliminating doc drift by making the substrate schemas the single source of truth and rendering them into browsable HTML/Markdown surfaces?

## Why it matters (blast radius)
Substrate has hundreds of typed primitives (Briefs 152-218) and growing. Hand-written documentation drifts from spec the moment a schema changes. A typed doc generator turns schemas themselves into docs, so the documentation cannot drift. Creators get a browsable spec viewer for their project; substrate maintainers get auto-generated reference docs; AI agents get a structured doc surface to query.

## What we know from the spec
- Brief 217 — CLI and headless toolchain.
- Brief 218 — Language server and IDE integration.
- Briefs 152-216 — substrate primitives with schema-embedded doc strings.

## Findings
1. **`gspl docs` subcommand.** CLI subcommand `gspl docs build` generates a static documentation site from the project's gseeds and substrate schemas. `gspl docs serve` runs a local HTTP server with hot reload.
2. **Substrate reference docs.** The substrate ships its own auto-generated reference site built from substrate schemas: every primitive, field, mutation, and gate is documented from its schema annotation. Updated automatically when substrate version bumps.
3. **Project docs.** Creator projects generate project-specific docs covering: gseeds in the project, recipe compositions used, mod dependencies, validation gates active, export targets configured. Generated from the project's signed gseeds + `gspl.toml` manifest.
4. **Schema-embedded annotations.** Substrate primitive schemas carry typed doc-string fields (description, examples, see-also references). Schema is the single source of truth; docs are rendered from the schema.
5. **Cross-references.** Doc generator follows typed cross-references between gseeds and substrate primitives. Clicking a field type navigates to its primitive doc; clicking a recipe navigates to the recipe gseed.
6. **Multiple output formats.** Doc generator emits: HTML static site (default), Markdown (for embedding in repos / wikis), JSON (for AI agent consumption), PDF (via headless Chrome export).
7. **Search index.** Generated docs ship a typed search index (lunr.js compatible) covering all primitives, fields, and example snippets. Offline-searchable.
8. **Example extraction.** Substrate schemas include typed example fields. Doc generator renders examples as syntax-highlighted snippets with copy-to-clipboard.
9. **API surface diff.** `gspl docs diff <prev-version> <next-version>` generates a typed changelog showing added / removed / changed primitives and fields. Drives substrate release notes automatically.
10. **Recipe walkthrough generation.** For recipes (Briefs 197-208), doc generator renders the recipe's parameter slots, sub-recipe variants, and validation contract as a guided walkthrough with example invocations.
11. **Validation contract documentation.** Sign-time gates (declared per primitive) are auto-rendered as a validation reference, so creators see exactly which gates apply to their gseeds.
12. **AI agent doc surface.** `gspl docs query <topic>` returns a typed JSON response suitable for LLM consumption. Agents query the doc surface programmatically without scraping HTML.
13. **Validation contract.** Sign-time gates: schema doc-string fields present on every primitive, examples valid against the schema, cross-reference targets resolve.

## Risks identified
- **Doc-string verbosity.** Embedding rich doc strings in schemas inflates schema files. Mitigation: doc strings are typed string-or-fileref fields; long-form docs reference external markdown files.
- **Generation cost.** Large projects generate large doc sites. Mitigation: incremental generation; only re-render changed gseeds.
- **Doc rendering accessibility.** Auto-generated HTML may have a11y issues. Mitigation: doc generator uses accessible HTML templates by default; substrate ships templates that pass WCAG 2.1 AA.
- **Localization.** Doc strings are English-only by default. Mitigation: typed `doc.locale` field on schemas allows creator-supplied translations; v0.1 ships English only.

## Recommendation
Specify the doc generator as a `gspl docs` subcommand (build / serve / diff / query) generating HTML / Markdown / JSON / PDF documentation from substrate schemas as single source of truth, with cross-references, search index, example extraction, recipe walkthroughs, validation contract documentation, and AI agent doc surface.

## Confidence
**4.5 / 5.** Doc generation from schemas is well-precedented (rustdoc, godoc, JSDoc). The novelty is the recipe walkthrough generator and the AI-agent doc query surface. Lower than 5 because the diff-based changelog needs Phase-1 schema-evolution measurement.

## Spec impact
- New spec section: **Documentation generator and spec viewer specification**.
- Adds the `gspl docs` subcommand contract with build / serve / diff / query verbs.
- Adds typed schema doc-string field requirements.
- Cross-references Briefs 152-218.

## New inventions
- **INV-952** — `gspl docs` subcommand generating substrate and project documentation from schemas as single source of truth: documentation cannot drift from spec.
- **INV-953** — Schema-embedded typed doc-string fields with cross-reference targets: substrate primitives carry their own documentation as part of the typed surface.
- **INV-954** — Multi-format doc emission (HTML / Markdown / JSON / PDF) from a single source: documentation reaches all surfaces (web, repo, agent, print).
- **INV-955** — Recipe walkthrough generator rendering parameter slots and sub-recipe variants as guided walkthroughs: recipes self-document their composition surface.
- **INV-956** — Validation contract auto-documentation: sign-time gates appear in docs alongside the primitives they constrain, so creators see the rules they must satisfy.
- **INV-957** — AI-agent doc query surface via `gspl docs query`: agents consume structured JSON doc responses without HTML scraping.
- **INV-958** — Substrate version diff changelog generator: substrate release notes are auto-derived from schema diffs, eliminating release-note drift.

## Open follow-ups
- Localization beyond English — deferred to v0.3.
- Interactive playground embedded in docs — deferred to v0.3.
- Video doc embedding — deferred to v0.4.
- Phase-1 doc generation performance for large projects.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 217 — CLI and headless toolchain.
3. Brief 218 — Language server and IDE integration.
4. rustdoc design — rust-lang.
5. godoc design — Go team.
6. TypeDoc / JSDoc generators.
7. Docusaurus / mkdocs static site generators.
