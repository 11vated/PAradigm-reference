# 147 — Federation-wide adapter review protocol

## Question

When a creator publishes a learned LoRA adapter (router, namespace expert, custom skill) to the federation (Brief 100), what review process determines whether other peers can safely compose it into their own kernel?

## Why it matters (blast radius)

Brief 129 establishes adapters as composable units (base + namespace + creator + task). Brief 100 establishes federation peer publishing. Together they enable cross-creator capability sharing — but without a review protocol, a single malicious or buggy adapter could propagate constitutional violations or quality regressions across the federation. This is the supply-chain security problem for the substrate's intelligence layer.

## What we know from the spec

- Brief 100 specifies the federation peer protocol with signed publishing.
- Brief 129 specifies four-tier LoRA composition.
- Brief 107 specifies the governance council and constitutional amendment process.
- Brief 060 specifies supply chain and dependency security.
- No prior brief specifies the per-adapter review protocol.

## Findings

1. **Three review tiers based on adapter scope.** *Personal* (creator-local, never federated): no review needed. *Federation-shared* (published to peers, opt-in install by other creators): automated review. *Federation-default* (proposed for inclusion in the canonical kernel composition): council review.

2. **Automated review (federation-shared tier) checks five things.**
   (a) Constitutional fence: run the adapter against the Brief 134 constitutional family of the eval battery → must pass 100%.
   (b) Quality non-regression: run the adapter against the held-out canonical battery → must not regress more than 2σ on any family.
   (c) Latency non-regression: must not exceed the floor latency budget for its scope.
   (d) Provenance verification: every training pair the adapter was trained on must be a valid, non-rolled-back gseed in the publisher's lineage.
   (e) Signature: adapter must be signed by the publishing creator's identity.

3. **Adapters that pass automated review are signed with a federation-readiness gseed.** `federation-review://<adapter-id>/passed` carries the review run hash, the eval battery snapshot version, and the reviewer (creator who ran the review, usually the publisher themselves running the canonical battery).

4. **Cross-peer verification is the trust mechanism.** When a peer downloads a federation-shared adapter, their kernel re-runs the automated review locally before installing. This prevents a publisher from cheating the review (they'd have to also cheat every downstream peer's local re-run). Local re-run takes ~5-15 minutes on the floor (depends on adapter size).

5. **Council review (federation-default tier) is the canonical-kernel gate.** Brief 107's council reviews any adapter proposed for inclusion in the default v0.x kernel composition. Quarterly cadence. Council members run the full eval battery + held-out slices, examine training data provenance, and vote. Approved adapters become part of the next signed canonical-kernel release.

6. **Adapters carry semantic version + compatibility metadata.** Each adapter declares: target backbone (Qwen3-14B / Qwen3-30B / etc.), target namespace, target tier (router / reranker / verifier / action / namespace expert), and compatibility version range. The kernel installer rejects incompatible adapters.

7. **Revocation is signed and propagating.** If a federation-shared adapter is later found to violate constitutional or quality bars (e.g., a delayed-action regression), the council can sign a revocation gseed. Federation peers polling the revocation list automatically uninstall revoked adapters at next sync. Revocations are time-stamped and rollback-able like everything else.

8. **Trust scoring.** Each creator carries a `federation-trust` score derived from: (a) number of adapters published, (b) review pass rate, (c) revocation rate, (d) downstream install count, (e) days since first published adapter. The trust score is *informational*, not gating — review is mandatory regardless. But the trust score helps creators choose which peer's adapters to install.

9. **Sandbox-first install for non-default tier.** Even after passing review, a federation-shared adapter installs into a sandbox slot first. The kernel runs both base and base+adapter for the first 100 inferences and only promotes the adapter to the active composition if creator explicitly accepts. This is the user-tier preview-with-veto from Brief 128.

10. **Federation-trust dashboard in Studio.** Brief 048's Studio shows installed adapters, their trust scores, their review status, and revocation history. Creators can roll back any adapter from the UI in one click — the underlying mechanism is Brief 105's signed rollback primitive.

## Risks identified

- **Automated review can be cheated.** A motivated bad actor could craft an adapter that passes the eval battery but misbehaves on the long tail. Mitigation: cross-peer local re-run (finding 4) catches different held-out slices; revocation (finding 7) catches delayed-action regressions; trust scores (finding 8) discourage repeat offenders.
- **Council review queue saturation at scale.** Quarterly council can review only ~5-10 adapters per session. Mitigation: federation-default tier is intentionally narrow; most adapters stay at federation-shared with automated review.
- **Sandbox-first install adds latency to creator experience.** ~100-inference burn-in feels slow. Mitigation: sandbox runs in parallel with active composition, not in series; latency cost is shadow-evaluation only.

## Recommendation

**Adopt three-tier adapter review: personal (no review), federation-shared (automated five-check review with cross-peer local re-run), federation-default (council review per Brief 107). Review checks: constitutional 100%, quality within 2σ, latency within budget, provenance verified, signature valid. Federation-shared adapters install into a sandbox slot for first 100 inferences with shadow evaluation. Revocations are signed gseeds that propagate to all peers and auto-uninstall on sync. Federation-trust scoring is informational, not gating. Studio surfaces all installed adapters with trust scores and one-click rollback.**

## Confidence

**4/5.** Each piece is mechanically straightforward. The unknowns are: (a) creator response to the sandbox-first burn-in, (b) revocation policy edge cases for adapters with deep downstream composition.

## Spec impact

- `gspl-reference/intelligence/adapter-review.md` — new file with the three tiers, five checks, sandbox install, revocation protocol, trust scoring.
- `gspl-reference/research/100-federation-peer-protocol-details.md` — cross-reference; review protocol is the security layer of federation publishing.
- `gspl-reference/research/107-governance-and-constitutional-amendment-process.md` — cross-reference; council review for federation-default tier.
- `gspl-reference/research/060-supply-chain-and-dependency-security.md` — cross-reference; this is the supply-chain security mechanism for adapters.

## New inventions

- **INV-584** — *Three-tier adapter review protocol* (personal / federation-shared / federation-default) with cross-peer local re-run as the cheat-resistance mechanism.
- **INV-585** — *Sandbox-first adapter install with shadow evaluation* over the first 100 inferences before promotion to active composition.
- **INV-586** — *Signed propagating revocation gseed* that auto-uninstalls compromised adapters across all federation peers at next sync.
- **INV-587** — *Federation-trust scoring* (publish count + review pass rate + revocation rate + install count + tenure) as an informational signal alongside the gating review process.

## Open follow-ups

- Exact sandbox burn-in count (100 is a placeholder).
- Whether trust scoring should ever become gating (probably no — review is mandatory regardless).
- Council session adapter throughput sizing (quarterly cadence may need bi-monthly at scale).

## Sources

1. Brief 060 — Supply chain and dependency security.
2. Brief 100 — Federation peer protocol details.
3. Brief 107 — Governance and constitutional amendment process.
4. Brief 128 — GSPL tool-use and modifier-surface intelligence.
5. Brief 129 — GSPL self-improvement loop.
6. SLSA framework, *Supply chain Levels for Software Artifacts*, 2023 (review tier patterns).
