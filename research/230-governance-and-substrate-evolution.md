# 230 — Governance and substrate evolution

## Question
What is the typed governance model for substrate evolution that enables the substrate to grow over time without becoming captured by a single entity, with a transparent change-proposal process, signed maintainer identities, federation-friendly forks, and clear authority over the substrate's typed surface — analogous to RFC processes (Rust RFCs, Python PEPs, TC39) but native to the substrate's lineage-tracking primitives?

## Why it matters (blast radius)
Every successful substrate ecosystem needs a governance model. Centralized control invites capture; uncoordinated growth fragments the ecosystem. Without typed governance, the substrate's evolution is opaque and contestable. With typed governance, every substrate change has provenance, every decision is auditable, and federation-friendly forks are first-class — protecting against any single failure mode.

## What we know from the spec
- Brief 152 — substrate signing and lineage.
- Brief 210 — federated identity surface.
- Brief 223 — package registry and distribution.
- Brief 229 — substrate versioning and migration.

## Findings
1. **Typed `gsep.def` gseed (GSPL Substrate Evolution Proposal).** Every change to the substrate is a typed `gsep.def` proposal: title, motivation, current state, proposed change, alternatives considered, drawbacks, unresolved questions, prior art references, drafted by an identified author, signed.
2. **Three-stage GSEP lifecycle.** Draft → review → accepted/rejected/withdrawn. Each transition is a typed mutation on the GSEP gseed signed by a maintainer identity. Lineage records every state transition with reason.
3. **Maintainer identities.** Substrate maintainers are typed `maintainer.identity` gseeds with: name, role (core / domain / docs / triage), areas of expertise, public key. Maintainer additions/removals are themselves GSEPs, ratified by existing maintainers.
4. **Acceptance criteria.** GSEPs reach acceptance via consensus-seeking among core maintainers (no formal vote unless contested). Contested GSEPs go to a typed vote among core maintainers; supermajority (2/3) required to pass. Process mirrors Rust RFC process and Python PEP process.
5. **GSEP types.** Typed kinds: substrate primitive change (most common), CLI / tooling change, governance change (meta-GSEPs), deprecation, security advisory. Each kind has typed fields appropriate to its scope.
6. **Implementation linkage.** Accepted GSEPs reference the implementation PR / commits via signed lineage. The substrate version that ships the GSEP is recorded. Ungrounded GSEPs (accepted but unimplemented) are tracked in the typed `gsep.implementation.queue`.
7. **Federation-friendly forks.** Anyone can fork the substrate. Forks declare typed `substrate.fork` declaring: parent substrate identity, divergence point, scope of divergence. Forks are first-class; the upstream and the fork interoperate where compatible.
8. **Trademark and brand separation.** Substrate brand (the name "GSPL") is separately governed from the substrate code. Forks of the code are encouraged; forks of the brand require explicit naming. Documented in a typed `brand.policy.gseed`.
9. **Code-of-conduct.** Substrate community has a typed `coc.gseed` declaring expected behavior, enforcement scope, appeal process. Standard Contributor Covenant variant adapted for typed community substrate.
10. **Security disclosure process.** Typed `security.advisory.def` gseed with embargo period, affected versions, mitigation steps, credit. Security advisories follow CVE / GHSA conventions. Embargo timeline typed (default 90 days).
11. **Sunsetting policy.** Substrate primitives can be sunsetted via typed `gsep.deprecation` proposal. Deprecation cycle minimum two minor versions before removal. Coordinates with Brief 229 migration tooling.
12. **Annual roadmap.** Substrate ships an annual typed `roadmap.year.gseed` listing themes, priorities, accepted GSEPs targeted for the year. Provides predictability without locking commitments.
13. **Validation contract.** Sign-time gates: GSEP proposals are well-formed (typed fields present), maintainer signatures resolve to current `maintainer.identity` gseeds, accepted GSEPs link to implementation, security advisories follow embargo timeline.

## Risks identified
- **Maintainer burnout / capture.** Concentrated maintainer load risks burnout and bus factor. Mitigation: typed maintainer roles distributed across areas; GSEP process encourages new maintainer onboarding; succession planning typed in roadmap.
- **GSEP process overhead.** Heavy process slows iteration. Mitigation: process scales with change scope: trivial fixes go through PR review; substrate primitive changes go through full GSEP. Mirrors Rust's small-RFC vs large-RFC distinction.
- **Fork fragmentation.** Forks dilute ecosystem. Mitigation: substrate's typed lineage makes upstream-fork interop traceable; federation-friendly model treats forks as legitimate, not antagonistic.
- **Vendor capture.** Single company dominating maintainer pool. Mitigation: maintainer affiliations are public (declared in `maintainer.identity`); GSEP process structurally requires multiple maintainer signatures from non-overlapping affiliations.
- **Decision opacity.** Closed-door decisions undermine trust. Mitigation: every decision is a typed signed mutation; lineage is queryable; no decisions exist outside the typed surface.

## Recommendation
Specify governance as typed `gsep.def` proposals through draft → review → accepted/rejected lifecycle, signed maintainer identities, consensus-seeking acceptance with supermajority fallback, GSEP type taxonomy, federation-friendly forks, separate brand governance, code-of-conduct, security disclosure process, sunsetting policy with deprecation cycles, and annual roadmap. Substrate evolution is typed end-to-end and structurally auditable.

## Confidence
**4 / 5.** Governance patterns are well-precedented (Rust RFCs, Python PEPs, TC39, IETF RFCs). The novelty is encoding the entire governance process in the substrate's own typed gseed surface — eating the substrate's own dog food. Lower than 4.5 because real-world governance friction needs Phase-1 community formation experience.

## Spec impact
- New spec section: **Governance and substrate evolution specification**.
- Adds typed `gsep.def`, `maintainer.identity`, `substrate.fork`, `brand.policy.gseed`, `coc.gseed`, `security.advisory.def`, `gsep.deprecation`, `roadmap.year.gseed` gseed kinds.
- Adds the GSEP lifecycle state machine.
- Adds the maintainer role taxonomy.
- Cross-references Briefs 152, 210, 223, 229.

## New inventions
- **INV-1054** — Typed `gsep.def` substrate evolution proposal with full lifecycle as signed lineage: substrate evolution is structurally auditable, mirroring Rust RFCs / Python PEPs natively in the substrate's own surface.
- **INV-1055** — Typed `maintainer.identity` with public roles and area expertise: substrate authority is named, signed, and queryable.
- **INV-1056** — Three-stage GSEP lifecycle (draft / review / accepted-rejected) with signed transition mutations: every governance decision is provenance-tracked.
- **INV-1057** — Consensus-seeking with supermajority fallback for contested GSEPs: governance scales without centralized authority.
- **INV-1058** — GSEP type taxonomy (primitive / tooling / governance / deprecation / security): proposals are typed by impact scope.
- **INV-1059** — Typed `substrate.fork` declarations with parent identity and divergence scope: forks are first-class, federation-friendly, traceable.
- **INV-1060** — Brand-vs-code governance separation via typed `brand.policy.gseed`: trademark and code evolve independently, eliminating fork-naming conflicts.
- **INV-1061** — Typed `security.advisory.def` with embargo timeline and CVE/GHSA conventions: security disclosure is structured substrate primitive.
- **INV-1062** — Typed `gsep.deprecation` with two-minor-version minimum cycle coordinating with Brief 229 migration tooling: sunsetting is structured, never abrupt.
- **INV-1063** — Annual `roadmap.year.gseed` providing predictability without locking commitments: substrate roadmap is typed and auditable.
- **INV-1064** — Affiliation-disclosure requirement on `maintainer.identity` with non-overlapping affiliation gates on GSEP signing: structural protection against single-vendor capture.

## Open follow-ups
- Phase-1 initial maintainer cohort formation.
- GSEP web UI for community discussion — Phase 1.
- Translation of substrate spec to non-English — deferred to v0.3.
- Foundation / nonprofit governance vehicle — deferred to v0.3 evaluation.
- Trademark registration timeline — Phase 1 legal.
- Security disclosure infrastructure (private issue tracker) — Phase 1.

## Sources
1. Brief 152 — Substrate signing and lineage.
2. Brief 210 — Account and identity surface.
3. Brief 223 — Package registry and distribution.
4. Rust RFC process documentation.
5. Python PEP process (PEP 1).
6. TC39 stage process for ECMAScript proposals.
7. IETF RFC process.
8. Contributor Covenant code of conduct.
9. CVE / GHSA vulnerability disclosure conventions.
10. Apache Software Foundation governance model.
11. Linux kernel maintainer hierarchy.
