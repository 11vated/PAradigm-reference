# 056 — Observability, telemetry, and privacy

## Question
How does GSPL get the operational visibility it needs to fix bugs, improve UX, and prove reliability — without violating the sovereignty commitment that says no user data leaves the device?

## Why it matters
You cannot improve what you cannot measure. Most software fixes this with telemetry: send everything to a server, analyze, ship improvements. GSPL cannot. The sovereignty commitment is not negotiable. But blind operation produces buggy software. The solution is *local-first observability with explicit, bounded, opt-in sharing* — a discipline that almost no consumer software practices well.

## What we know from the spec
- Brief 042: identity is local, encrypted.
- Brief 048: studio architecture.
- Brief 055: no telemetry to GSPL about LLM use.

## Findings — three observability layers

### Layer 1: Local diagnostics (always on)
The studio collects rich diagnostics on the local device. These never leave the device unless the user explicitly shares them.
- **Performance metrics:** per-operation latency, memory use, GPU usage.
- **Error logs:** structured errors with stack traces and context.
- **Operation timeline:** what the user did, when, what the result was.
- **Critic scores:** historical scores over time per project.
- **Storage growth:** disk use trends.
- **Crash dumps:** with PII filtering applied.

Stored in `~/.paradigm/diagnostics/`. Bounded size (default 100MB; oldest evicted).

### Layer 2: Anonymized aggregate metrics (opt-in)
The user can opt into sharing aggregate, anonymized metrics with the GSPL project. This is *strictly off by default* and explicitly enabled in settings with full disclosure.
- **What gets shared:** aggregate per-engine usage counts, aggregate per-operator success rates, aggregate latency percentiles, aggregate crash rates.
- **What does NOT get shared:** seed contents, lineage, identity, project names, prompts, user vocabulary, file paths, IP addresses (uses Tor or similar), exact timestamps (rounded to day), any per-user identifier.
- **The aggregation is local first:** the studio computes daily aggregates locally and uploads only the aggregates (k-anonymity ≥ 100 enforced).
- **Differential privacy** noise added before upload (ε = 1.0 default).
- **Upload via Tor** (built-in onion service) so the GSPL project never sees the user's IP.
- **User can review every upload** before it leaves; "show me what's being sent" button.

### Layer 3: Bug reports (explicit per-incident)
When the user encounters a bug, they can submit a bug report.
- **The studio gathers context:** error logs, recent operations, system info, anonymized seed metadata.
- **The user reviews and edits the report** before sending.
- **The user can attach a project zip** if they want to (not required).
- **Submission is via signed POST** to a GSPL bug tracker.
- **Each bug report is one-shot**, not a recurring channel.

## Privacy mechanisms

### PII filtering
- **Path normalization:** absolute paths → `~/...` form.
- **Identity filtering:** identity hashes replaced with placeholder.
- **Prompt filtering:** user-typed text excluded by default.
- **Exception filtering:** stack traces have line numbers and file names but not variable values.

### k-anonymity
For aggregate metrics, no value is uploaded if fewer than k=100 users have that exact value. This prevents re-identification through unusual configurations.

### Differential privacy
For aggregate counts, Laplace noise is added before upload. ε=1.0 is the default (moderate privacy).

### Tor transport
Aggregate uploads use the studio's built-in Tor client (libonion or arti). The GSPL project sees an onion address, not an IP.

## What the GSPL project gets

Even with these constraints, the GSPL project can see (in aggregate, opt-in only):
- **Engine usage popularity** — which engines are heavily used.
- **Operator success rates** — which operators frequently fail.
- **Performance distributions** — p50/p95/p99 latency per operation.
- **Crash classes** — what's crashing most often.
- **Feature adoption** — which UX surfaces are reached.

This is enough to prioritize fixes and improvements.

## What the GSPL project deliberately does NOT get

- **Per-user data of any kind.**
- **Project contents.**
- **Lineage.**
- **Prompts.**
- **Marketplace transactions.**
- **Federation peers.**
- **API keys.**
- **Identity hashes.**

## Local diagnostics UX

The studio has a Diagnostics view (in the Help pillar) that shows:
- **Recent errors** with explanations.
- **Performance trends** as small charts.
- **Storage breakdown** by project.
- **Operation timeline** for the current session.
- **One-click "export diagnostics"** for sharing with support or community help forums.

Users can debug their own issues without sharing anything.

## Risks identified

- **Aggregate metrics can leak via correlation.** Mitigation: k-anonymity + DP noise.
- **Tor is sometimes blocked.** Mitigation: aggregate sharing is opt-in; non-blocking if upload fails.
- **Bug reports may contain PII users miss.** Mitigation: review-before-send; filtering applied.
- **No telemetry = harder to fix bugs.** Mitigation: local diagnostics + opt-in aggregates + bug reports cover most cases.
- **Crash dumps can contain memory contents.** Mitigation: PII filter scrubs known sensitive structures; user reviews before sharing.
- **User confusion about what's shared.** Mitigation: explicit "show me what's being sent" UI; plain-language explanation in settings.
- **Trust degradation if a leak ever happens.** Mitigation: external audit of the metrics pipeline pre-launch; bug bounty.

## Recommendation

1. **Adopt the three-layer observability model** in `architecture/observability.md`.
2. **Local diagnostics always on**, bounded size, never auto-shared.
3. **Aggregate metrics strictly opt-in** with full disclosure and review-before-send.
4. **k-anonymity ≥ 100 + differential privacy ε=1.0** for aggregates.
5. **Tor transport** for aggregate uploads.
6. **Bug reports are explicit per-incident** with user review.
7. **PII filtering** at every layer.
8. **Diagnostics view in the studio** for self-debug.
9. **External audit of the metrics pipeline pre-launch.**
10. **No silent telemetry. Ever.**

## Confidence
**4/5.** The mechanisms (k-anonymity, DP, Tor) are mature. The 4/5 reflects honest uncertainty about how much the opt-in rate will be — without enough opt-in, the aggregates aren't useful.

## Spec impact

- `architecture/observability.md` — full observability spec.
- `protocols/aggregate-metrics.md` — k-anonymity, DP, and upload format.
- `protocols/bug-report-format.md` — bug report structure and review.
- `architecture/local-diagnostics.md` — local diagnostics storage and UX.
- `crypto/differential-privacy.md` — DP parameters and noise spec.
- New ADR: `adr/00NN-no-silent-telemetry.md`.

## Open follow-ups

- Build the local diagnostics view at v1.
- Decide on the DP library (likely OpenDP).
- Build the Tor integration (arti or torrs).
- External audit of the aggregate metrics pipeline.
- Bug bounty program for the metrics pipeline.
- UX test the "show me what's being sent" view.

## Sources

- Apple's differential privacy paper.
- OpenDP library documentation.
- Tor Project documentation; arti (Rust Tor client).
- Dwork & Roth, *The Algorithmic Foundations of Differential Privacy*.
- Internal: Briefs 042, 048, 055.
