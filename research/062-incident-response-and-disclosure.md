# 062 — Incident response and vulnerability disclosure

## Question
How does GSPL respond to security incidents — vulnerabilities discovered, keys compromised, models found malicious, content moderation failures — across a decentralized userbase, and how does it disclose vulnerabilities responsibly?

## Why it matters
Every security-relevant project will have incidents. The question is whether the response is competent or chaotic. For a decentralized platform with no central operator, incident response is harder than for a SaaS — there's no "deploy a hotfix and move on." Updates take days to propagate; some users are on the frozen channel; the response must work across the diversity of GSPL's deployment.

## What we know from the spec
- Brief 042: key management with rotation/revocation.
- Brief 057: release engineering with five tracks.
- Brief 060: supply chain security and bug bounty.
- Brief 061: content moderation.

## Findings — six-phase incident response

### Phase 1: Detection
Sources of incident reports:
- **Bug bounty program** (Brief 060).
- **Security researchers** via responsible disclosure.
- **Internal monitoring** (CVE feeds, dependency scanners).
- **User reports** (bug reports, community channels).
- **Federation peer warnings** (other GSPL instances).
- **External notification** (CERT, law enforcement, academia).

Each source has a documented intake channel.

### Phase 2: Triage
Within 24 hours of detection:
- **Severity assessment:** Critical / High / Medium / Low based on CVSS + GSPL-specific factors (sovereignty impact, lineage integrity impact, key exposure).
- **Affected component identification:** kernel, engine, agent, model, plugin, infrastructure.
- **Affected version range.**
- **Exploitation status:** in the wild, public PoC, theoretical.
- **Initial mitigation.**

The triage output is a structured incident record with a unique ID.

### Phase 3: Investigation
- **Root cause analysis.**
- **Scope confirmation.**
- **Reproduction.**
- **Fix design** with regression tests.
- **Documentation** of findings (kept private until disclosure).

For incidents involving compromised keys, the investigation also includes:
- Audit of all signing operations under the suspect key.
- Identification of malicious lineage entries (if any).
- Plan for revocation and re-signing.

### Phase 4: Mitigation and patch
- **Patch developed** in a private branch.
- **Patch reviewed** by at least two maintainers.
- **Patch tested** against the regression test.
- **Patch built** through the secure release pipeline (Brief 060 + Brief 057).
- **Mitigation guidance** prepared for users on frozen track who can't immediately update.

### Phase 5: Disclosure and release
- **Coordinated disclosure** with reporters; CVE assigned where applicable.
- **Patch released** through the appropriate release tracks.
- **Security advisory published** with full details: severity, affected versions, mitigation, fix, credits.
- **Notification to users:**
  - Critical: in-product banner on next launch + signed announcement on the federation.
  - High: in-product banner.
  - Medium/Low: changelog only.
- **Frozen track users notified** even if they're not auto-updating.

### Phase 6: Post-mortem
- **Blameless post-mortem** within 2 weeks of disclosure.
- **Published** unless privacy concerns prevent it.
- **Lessons learned** integrated into the security process.
- **Bug bounty payout** if applicable.

## Severity-specific responses

### Critical (key compromise, RCE, CSAM filter failure)
- **Detection-to-patch target:** ≤ 7 days.
- **Detection-to-disclosure target:** ≤ 14 days.
- **Emergency release** outside normal cadence.
- **Federation-wide announcement** signed by the multi-sig key.
- **In-product alert** on next launch.

### High (auth bypass, signature forgery, lineage corruption)
- **Detection-to-patch target:** ≤ 14 days.
- **Detection-to-disclosure target:** ≤ 30 days.
- **Out-of-band release** if needed.

### Medium (DoS, info leak with limited impact)
- **Detection-to-patch target:** ≤ 30 days.
- **Disclosure** at next regular release.

### Low (edge case, low-impact)
- **Detection-to-patch target:** next regular release.
- **Disclosure** in changelog.

## Disclosure policy

### Responsible disclosure window
- **90 days** is the default disclosure window for high/critical findings.
- **Extension possible** if a fix is ready but propagation needs more time.
- **Earlier disclosure** if the vulnerability is being actively exploited.

### Coordinated disclosure
- GSPL participates in coordinated disclosure with reporters.
- **CVE numbers requested** for high/critical findings.
- **Credit given** to reporters in advisories (with their permission).

### Bug bounty rewards
- **Critical:** $5K-$25K.
- **High:** $1K-$5K.
- **Medium:** $200-$1K.
- **Low:** community recognition.

(Numbers subject to GSPL revenue.)

## Incident-specific playbooks

### Playbook A: Compromised release signing key
1. Detection: external notification or unusual signed releases.
2. Triage: confirm key compromise; identify all releases signed since compromise.
3. Mitigation: rotate the key (multi-sig); publish key revocation; emergency advisory.
4. Patch: re-sign affected releases with the new key.
5. Disclosure: federation-wide announcement; CVE; public advisory.
6. Post-mortem: how was the key compromised?

### Playbook B: Malicious model weights
1. Detection: model registry hash mismatch or external researcher.
2. Triage: confirm malice; identify affected users.
3. Mitigation: remove model from registry; emergency model registry update.
4. Patch: replace with verified weights or remove entirely.
5. Disclosure: in-product alert for users with the model installed.
6. Post-mortem: how did the malicious model get registered?

### Playbook C: Engine plugin vulnerability
1. Detection: vulnerability researcher or fuzz testing.
2. Triage: confirm; assess sandbox effectiveness.
3. Mitigation: emergency engine plugin release.
4. Patch: fix + regression test + ABI version bump.
5. Disclosure: advisory.
6. Post-mortem: how did the vulnerability slip through review?

### Playbook D: CSAM filter failure
1. Detection: false negative reported by community or legal.
2. Triage: confirm; assess scale.
3. Mitigation: filter rules update; in-product disable of affected features if needed.
4. Patch: improved filter.
5. Disclosure: legal disclosure as required by law; public advisory after patch.
6. Post-mortem: filter improvement plan.

### Playbook E: Cryptographic primitive failure
1. Detection: external research (e.g., new attack on P-256).
2. Triage: assess impact on existing signatures.
3. Mitigation: migration plan to a new primitive (Brief 042 quantum migration is the model).
4. Patch: implement and test new primitive.
5. Disclosure: long-term migration advisory.
6. Post-mortem: review of cryptographic agility.

## Risks identified

- **Slow propagation:** federated systems update slowly. Mitigation: in-product alerts; federation-wide announcements; mitigation guidance for unpatched users.
- **Frozen track exposure:** users who don't update remain vulnerable. Mitigation: explicit notification; guidance.
- **Coordinated disclosure tension:** researchers want fast disclosure; users need time to update. Mitigation: 90-day default; flexibility for both directions.
- **Bug bounty cost.** Mitigation: tiered budget; community recognition for low-severity.
- **Reputation damage from disclosed vulnerabilities.** Mitigation: blameless post-mortems; transparent process.
- **Incident response capacity:** GSPL is a small team. Mitigation: clear playbooks; community responder corps for low/medium severity.
- **Legal disclosure constraints:** some incidents have mandatory disclosure (GDPR Article 33). Mitigation: legal review built into the response process.

## Recommendation

1. **Adopt the six-phase incident response model** in `architecture/incident-response.md`.
2. **24-hour triage SLA** for all reports.
3. **Severity-specific patch and disclosure SLAs** as documented.
4. **90-day responsible disclosure default.**
5. **Bug bounty program with published reward tiers.**
6. **Five incident playbooks** documented at v1.
7. **Blameless post-mortems** within 2 weeks of disclosure.
8. **Federation-wide announcements** for critical incidents.
9. **In-product alerts** for high/critical severity.
10. **Legal review built into the response process.**
11. **GDPR Article 33 compliance** for personal data incidents (Brief 059).

## Confidence
**4/5.** Incident response is well-understood; the playbooks are conventional. The 4/5 reflects the unproven scale of running this with a small team across a decentralized userbase.

## Spec impact

- `architecture/incident-response.md` — full six-phase model.
- `protocols/incident-playbooks.md` — five playbooks.
- `protocols/disclosure-policy.md` — coordinated disclosure.
- `protocols/bug-bounty.md` — reward tiers and process.
- `tests/incident-drill.md` — quarterly incident drill plan.
- New ADR: `adr/00NN-six-phase-incident-response.md`.

## Open follow-ups

- Build the bug bounty program at v1 launch.
- Set up the incident intake channels (signed email, Tor onion, web form).
- Run a quarterly incident drill.
- Engage external security counsel for legal disclosure obligations.
- Build the in-product alert mechanism.
- Plan the community responder corps.

## Sources

- ISO/IEC 27035 (incident management).
- NIST SP 800-61 (computer security incident handling guide).
- Project Zero's 90-day disclosure policy.
- OASIS CSAF (Common Security Advisory Framework).
- Internal: Briefs 042, 057, 058, 059, 060, 061.
