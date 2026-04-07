# Contributing to gspl-reference

This repository is the **normative specification** for the Paradigm GSPL Engine. It is not the implementation. Contributions here change the contract that implementations must satisfy. Treat every change with that weight.

## Ground rules

1. **Spec first, code never.** This repo contains specs, ADRs, examples, and reference pseudocode. It does not contain a build system, runtime code, or compiled artifacts. If you find yourself wanting to add a `Cargo.toml` or `package.json`, you are in the wrong repo — that belongs in the implementation repo.

2. **Boring tech wins.** New dependencies, formats, or libraries require an ADR explaining why an existing primitive will not suffice. See `adr/0000-boring-tech.md`.

3. **One source of truth.** Every concept lives in exactly one place. Cross-reference with relative links; never duplicate. If a sentence appears in two files, one of them is wrong.

4. **Determinism is non-negotiable.** Any change that introduces a source of nondeterminism (floating-point reordering, wall-clock time, OS-dependent iteration order, unpinned dependencies) must call it out explicitly and either eliminate it or quarantine it behind a documented escape hatch.

5. **Compliance is built in, not bolted on.** Changes that touch the seed format, agent surface, or export pipeline must consider C2PA, EU AI Act Article 50, California SB 942, and WCAG 2.2 AA implications. See `compliance/`.

## How to propose a change

Small fixes (typos, broken links, clarifications) — open a PR directly. Substantive changes follow this flow:

1. **Open an issue** describing the problem, not the solution. Wait for triage.
2. **Draft an ADR** under `adr/NNNN-short-title.md` using the Nygard template (Status / Context / Decision / Consequences). Even if the change does not feel "architectural," writing the ADR forces the question "does this fit the rest of the spec?"
3. **Update the spec** in the same PR. The ADR records the why; the spec files record the what.
4. **Update examples** if the change affects observable behavior. Re-derive any expected hashes in example header comments.
5. **Update the roadmap** if the change affects what ships in which phase.

## Style

- **Language:** plain English, present tense, active voice. Write for an engineer at a different company who has never met you.
- **Code blocks:** language-tagged. Pseudocode uses ` ```text` or ` ```rust` depending on what reads more clearly. Real Rust must be `cargo check`-clean if pasted into a crate.
- **Tables for matrices, prose for arguments.** A bulleted list is rarely the right answer in a spec.
- **No marketing language.** "Powerful," "seamless," "next-generation" — none of these belong in a spec.
- **No emoji.** Anywhere.
- **Line length:** soft 100, hard 120. Don't reflow paragraphs unless you're editing them.

## Hash-bearing examples

Files under `examples/` carry expected SHA-256 hashes in header comments. These are the regression contract for the implementation. If you change an example's content, you must:

1. Re-derive the hash by running the example through the canonicalization pipeline (`gspl run --hash-only path/to/example.gspl`).
2. Update the header comment.
3. Note in the PR description that the hash changed and why.

CI rejects PRs where an example's content changed but the hash did not.

## ADR process for new dependencies

Every external library, format, or service that the implementation will depend on requires an ADR. The ADR must answer:

- What problem does this solve?
- What are the alternatives (minimum 3)?
- Why is the chosen option better on the dimensions that matter (correctness, determinism, license, maintenance, supply-chain risk)?
- What is the exit cost if we have to replace it later?

See `adr/0001-rust-and-wgsl.md` and `adr/0006-postgres-only.md` for the expected shape.

## Review checklist

Before requesting review, verify:

- [ ] All cross-references resolve (no broken relative links)
- [ ] No duplicated content across files
- [ ] ADR exists for any architectural change
- [ ] Examples have correct expected hashes
- [ ] Compliance section updated if seed format / agent surface / export touched
- [ ] No new dependencies without an ADR
- [ ] No marketing language
- [ ] No emoji

## Code of conduct

Be exact. Be kind. Disagree with the idea, not the person. Cite sources. Show your work. If you don't know, say so.

## License

By contributing you agree that your contribution is licensed under the Apache License 2.0 (see `LICENSE`).
