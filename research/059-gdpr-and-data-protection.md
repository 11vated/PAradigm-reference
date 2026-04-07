# 059 — GDPR and data protection

## Question
What are GSPL's GDPR obligations as a data controller / processor — across the studio (local), the marketplace (peer-to-peer), and the federation (peer-to-peer) — and how does the local-first architecture make compliance easier or harder?

## Why it matters
GDPR is the most stringent and most enforced data protection law in the world. It applies to any personal data of EU residents, regardless of where the processor is. Fines are up to 4% of global revenue or €20M. The local-first architecture (Brief 053) makes most of GDPR moot — there is no central database to leak — but the marketplace, federation, and any optional aggregate metrics still touch personal data and require diligence.

## What we know from the spec
- Brief 053: local-first storage.
- Brief 056: opt-in aggregate telemetry.
- Brief 044: marketplace.
- Brief 043: federation.

## Findings — GDPR scope and roles

### What is personal data in GSPL?
- **Identity public keys** (Brief 042) — these are pseudonymous identifiers but, when linked to a real person, become personal data.
- **Display names and emails** in profiles (optional).
- **Marketplace transaction history** (buyers and sellers).
- **Federation peer addresses.**
- **Bug reports** with user-edited content.
- **Aggregate metrics** (after k-anonymity, arguably no longer personal data, but still treated cautiously).

### What is *not* personal data?
- **Seeds, lineage entries, render outputs.** These are creative works, not personal data, unless they encode personal information about identifiable individuals (e.g., a sprite of a real person — see Brief 046 likeness rights).
- **Diagnostic logs without PII** (after PII filtering).

### GSPL's role
- **For local data:** GSPL is *not* a controller or processor — the user is. The studio operates entirely on the user's device under their control.
- **For aggregate metrics (opt-in):** GSPL is the controller. Strict GDPR compliance applies.
- **For bug reports:** GSPL is the controller. Strict GDPR compliance applies.
- **For the marketplace:** GSPL is *not* a controller or processor. Buyers and sellers are joint controllers of their transaction data; payment processors are processors. GSPL is just a discovery and signing layer.
- **For the federation:** GSPL is *not* a controller or processor. Peers are independent controllers of their own data.

This is a major advantage of the architecture: GSPL itself has minimal GDPR exposure.

## GDPR obligations where GSPL is the controller

### Article 5: Principles
- **Lawfulness:** consent for aggregate metrics; legitimate interest for bug reports.
- **Purpose limitation:** metrics for product improvement only.
- **Data minimization:** k-anonymity, DP, PII filtering.
- **Accuracy:** users can review before sending.
- **Storage limitation:** aggregates retained 12 months max.
- **Integrity and confidentiality:** encrypted in transit (Tor, HTTPS) and at rest.
- **Accountability:** documented compliance posture (this brief + Brief 056).

### Article 6: Lawful basis
- **Aggregate metrics:** Article 6(1)(a) consent.
- **Bug reports:** Article 6(1)(a) consent (the user explicitly submits).

### Article 7: Consent
- **Explicit, granular, withdrawable.**
- **Withdrawing consent does not affect prior lawful processing.**
- **The studio's metrics opt-in is** *opt-in*, *explicit*, *granular* (per metric category), and *withdrawable* (one click).

### Articles 13-14: Information to data subjects
- **Privacy policy** in plain language, available in all v1 EU languages.
- **In-product disclosure** before any data leaves the device.
- **Contact information** for the controller (11vatedTech LLC).

### Articles 15-22: Data subject rights
For data GSPL controls (aggregate metrics, bug reports):
- **Right of access:** users can request what GSPL has on them. Practical: minimal because everything is anonymized; the response is "we have aggregate counts that may include your contributions, but we cannot identify them."
- **Right to rectification:** N/A for aggregate metrics; possible for bug reports.
- **Right to erasure:** practical for bug reports; impractical for aggregate metrics (they're already anonymized). The privacy policy explains this.
- **Right to restriction:** N/A.
- **Right to data portability:** the studio exports everything locally (Brief 053); the user has full data portability for their own data.
- **Right to object:** users can opt out of metrics at any time.
- **Automated decision-making:** N/A. The studio's agent does not make automated decisions producing legal effects.

### Article 25: Data protection by design and by default
The local-first architecture is the canonical example. Privacy by design.

### Article 30: Records of processing
GSPL maintains a register of processing activities for the metrics and bug report data flows. Published in `compliance/processing-register.md`.

### Article 32: Security
- **Encryption in transit and at rest.**
- **Access controls** (only the metrics pipeline operators have access).
- **Incident response plan** (Brief 062).

### Article 33-34: Breach notification
- **72-hour notification to supervisory authority.**
- **User notification if high risk.**
- **Documented breach response procedure** (Brief 062).

### Article 35: Data protection impact assessment (DPIA)
A DPIA is mandatory for high-risk processing. GSPL's metrics processing is not high-risk (anonymized, opt-in, minimal). A DPIA is *not* required, but a lightweight assessment is documented voluntarily for transparency.

## GDPR obligations where the user is the controller

The user owns their projects, lineage, and marketplace data. They are the controller. GSPL:
- **Provides tooling** for them to manage their own GDPR obligations (export, deletion, anonymization).
- **Documents user-as-controller responsibilities** in the user manual.
- **Does not assume GDPR responsibility** for user-controlled data.

This is unusual but defensible because GSPL never has access to the user's data in the first place.

## International data transfers

- **Aggregate metrics** are uploaded to GSPL's infrastructure. If GSPL infrastructure is in the US, EU-US data transfers apply.
- **Mitigation:** the upload is anonymized (k-anonymity + DP), so arguably no personal data crosses borders. Conservative approach: rely on EU-US Data Privacy Framework or SCCs.
- **EU-hosted infrastructure is preferred** for aggregate metrics; v1 plan is to host in the EU.

## Risks identified

- **Mistaken classification:** if GSPL is later classified as a controller for federation data, scope expands. Mitigation: legal review pre-launch; clear documentation of the architectural separation.
- **User confusion about responsibility:** users don't realize they're the controller. Mitigation: clear in-product explanation; user manual; FAQ.
- **Bug report PII leakage:** users include personal data in bug reports. Mitigation: review-before-send; PII filtering.
- **Aggregate metric re-identification:** technically possible despite DP. Mitigation: conservative ε; k-anonymity threshold; published methodology.
- **EU-US transfer disruption:** the Data Privacy Framework could be invalidated again. Mitigation: SCCs as backup; EU hosting.
- **Children's data:** under-13s require parental consent (Article 8). Mitigation: terms require 13+; the studio is not marketed to children.

## Recommendation

1. **Adopt this brief as the GDPR operational reference** in `compliance/gdpr.md`.
2. **GSPL is controller only for aggregate metrics and bug reports**, both opt-in.
3. **User is controller for all local data**, with GSPL providing tooling.
4. **Privacy policy in all v1 EU languages.**
5. **DPIA-lite published voluntarily** for transparency.
6. **EU-hosted infrastructure** for the aggregate metrics endpoint.
7. **Article 30 processing register** published.
8. **Breach response procedure** documented (Brief 062).
9. **Terms require age 13+**, no marketing to children.
10. **Legal review pre-launch** for the controller/processor classification.

## Confidence
**4/5.** The local-first architecture makes GDPR compliance unusually clean. The 4/5 reflects the risk of regulatory reclassification.

## Spec impact

- `compliance/gdpr.md` — full GDPR operational reference.
- `compliance/processing-register.md` — Article 30 register.
- `compliance/dpia-lite.md` — voluntary DPIA-lite.
- `compliance/privacy-policy.md` — public privacy policy.
- New ADR: `adr/00NN-user-as-controller.md`.

## Open follow-ups

- Legal review of the controller/processor classification.
- Translate the privacy policy into all v1 EU languages.
- Set up EU-hosted infrastructure for aggregate metrics.
- Build the data subject access request flow.
- Document the breach response procedure (Brief 062).

## Sources

- Regulation (EU) 2016/679 (GDPR).
- EDPB guidelines on consent, anonymization, DPIAs.
- Schrems II decision (CJEU C-311/18).
- Internal: Briefs 042, 043, 044, 053, 056, 058, 062.
