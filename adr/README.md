# Architecture Decision Records

This directory contains the Architecture Decision Records (ADRs) for Paradigm. Each ADR documents one significant decision: the context, the alternatives considered, the choice made, and the consequences. The format is the [Michael Nygard ADR template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

ADRs are *immutable*: once accepted, they are not edited. If the decision changes, a new ADR is written that supersedes the old one, and both remain in the repository.

## Status meanings

- **Proposed** — under discussion, not yet committed.
- **Accepted** — decision made; the codebase reflects it.
- **Deprecated** — no longer the recommended approach but the old code still uses it.
- **Superseded** — replaced by a newer ADR (which is linked).

## Index

| # | Title | Status |
|---|---|---|
| [001](001-deterministic-kernel.md) | Adopt a deterministic kernel as the foundation | Accepted |
| [002](002-jcs-canonicalization.md) | Use JCS (RFC 8785) for JSON canonicalization | Accepted |
| [003](003-xoshiro256-rng.md) | Use xoshiro256** + splitmix64 for the kernel RNG | Accepted |
| [004](004-ecdsa-p256-signing.md) | Use ECDSA P-256 with RFC 6979 for sovereignty signing | Accepted |
| [005](005-gspl-as-pure-language.md) | Make GSPL a pure functional language with algebraic effects | Accepted |
| [006](006-domain-engine-pattern.md) | Use a staged-pipeline domain engine pattern | Accepted |
| [007](007-map-elites-default.md) | Make MAP-Elites the default evolution algorithm | Accepted |
| [008](008-functor-composition.md) | Use functors for cross-domain composition | Accepted |
| [009](009-gseed-binary-format.md) | Use a custom .gseed binary format with MessagePack core | Accepted |
| [010](010-fastify-postgres-stack.md) | Build the backend on Fastify + PostgreSQL + pgvector | Accepted |
| [011](011-c2pa-compliance.md) | Embed C2PA manifests in all exported artifacts | Accepted |

## How to write a new ADR

1. Copy `_template.md` to `NNN-short-title.md` where NNN is the next free number.
2. Fill in Context, Decision, Consequences, Alternatives Considered.
3. Open a PR. The ADR is reviewed alongside the implementation, not as a separate gate.
4. Once merged, status moves to Accepted. ADRs are not edited after this.

## Why ADRs

Paradigm is a long-lived, multi-decade project. People will join who weren't there when each decision was made. ADRs are how we hand future maintainers the *reasoning* behind today's structure — not just "what" but "why and what we considered." Every accepted ADR represents an option not taken; the trail is as valuable as the choice.
