# Compliance

Paradigm is a globally distributed, AI-driven generative system. Three classes of regulation apply to it directly:

1. **Content provenance** — laws requiring that AI-generated content be labeled and traceable.
2. **AI transparency** — laws requiring disclosure that AI was used and how.
3. **Accessibility** — laws requiring that the user interface itself be accessible.

This directory documents how Paradigm complies with each.

| File | Topic |
|---|---|
| [`c2pa.md`](c2pa.md) | C2PA content credentials in `.gseed` and exports |
| [`eu-ai-act.md`](eu-ai-act.md) | EU AI Act Article 50 (synthetic content disclosure) |
| [`ca-sb-942.md`](ca-sb-942.md) | California SB 942 (AI Transparency Act) |
| [`wcag.md`](wcag.md) | WCAG 2.2 AA accessibility for the Studio |

## Compliance principles

1. **Compliance by construction.** Every export, every API response, every UI surface that produces or shows AI content carries the appropriate disclosure automatically. There is no opt-out and no manual step.
2. **Single source of truth.** The disclosures are derived from the `seeds` table fields (`provider`, `model`, `agent_version`, `parent_count`). They are not maintained separately.
3. **Verifiable, not just claimed.** Wherever the regulation permits, disclosure is cryptographically verifiable (C2PA + ECDSA signature) rather than a free-text label.
4. **Auditable.** Every compliance-relevant decision (e.g., "why was this seed labeled AI-generated?") is logged in `agent_runs` and replayable.
5. **Conservative by default.** When a jurisdiction is ambiguous, we apply the strictest rule globally.

## Jurisdictional matrix

| Jurisdiction | Regime | Effective | Paradigm response |
|---|---|---|---|
| EU | AI Act Art. 50 | Aug 2026 | C2PA + visible label on Studio + machine-readable provenance |
| California | SB 942 | Jan 2026 | C2PA + manifest disclosure tool + visible label |
| US Federal | (no federal AI labeling law as of 2026) | — | Default to EU/CA rules globally |
| UK | Online Safety Act | enforced | Same as EU posture |
| China | Generative AI Measures | enforced | Out of scope: no PRC service |

The default global posture is **EU + California**, both of which require provenance labeling for synthetic content. Applying both globally is simpler and strictly safer than per-region routing.

## What is "AI-generated" in Paradigm

Not every seed in Paradigm is AI-generated in the regulatory sense. The classification rule is:

- **AI-generated**: any seed produced via the GSPL Agent pipeline (i.e., LLM call in Stages 1-3).
- **AI-assisted**: any seed produced by deterministic evolution starting from an AI-generated parent.
- **Human-authored**: any seed produced by a human via direct gene editing in the Studio with no LLM assistance.

The `seeds.payload.provenance` field carries one of these three values; the C2PA manifest reflects the same classification.

For regulatory purposes, both *AI-generated* and *AI-assisted* trigger disclosure. *Human-authored* seeds do not require AI labeling, but they still receive a C2PA "human-edited" assertion so the provenance chain is unbroken.

## Internal compliance review

A scheduled task runs nightly:

1. Pulls all seeds created in the last 24h.
2. Verifies each export has a valid C2PA manifest.
3. Verifies each Studio render carries the correct visible label.
4. Verifies the provenance classification matches the actual `agent_runs` history.
5. Files an alert in PagerDuty if any check fails.

The check is logged to `compliance_audits` (see `infrastructure/db-schema.md` future addition).
