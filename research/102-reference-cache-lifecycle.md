# Brief 102 — Reference cache lifecycle

## Question

How does GSPL manage the lifecycle of cached `ref://` gseeds fetched from partner archives — retention, eviction, refresh, legal hold, and transparency — so that caching respects partner MOUs (Brief 098), honors removal requests, preserves lineage, and remains user-transparent?

## Why it matters

Brief 090's tiered source ladder and Brief 091's graph depend on caching partner materials. Without cache lifecycle discipline, GSPL risks: (a) serving stale references as fresh, (b) violating partner retention terms, (c) failing removal-on-request obligations, (d) losing provenance when cache evicts a referenced node, or (e) hiding caching state from users.

## What we know from spec

- Brief 090: `ref://` gseeds with provenance.
- Brief 091: content-addressed graph with tombstone deletion preserving lineage.
- Brief 098 INV-402: partner MOU template includes removal-on-request workflow with tombstone lineage preservation.
- Brief 101: three-tier cache with tier-source labeling.

## Findings

### Finding 1: Retention tiers should match partner sensitivity, not a single global policy

Partners in Brief 098 tier as A/B/C/D. Their cache retention terms should match:

- Tier A (bulk permissive: Met, Smithsonian, PubChem): long retention, months to years.
- Tier B (moderate: V&A, BL): partner-specified retention, default 90 days.
- Tier C (source-culture): partner-specified, often much shorter, default 30 days.
- Tier D (reduced-access): per-MOU terms, may be single-request no-cache.

### Finding 2: Removal-on-request must be fast and complete but preserve lineage

When a partner requests removal of a specific material, GSPL must:

1. Tombstone the specific `ref://` gseed (content removed, tombstone remains).
2. Downgrade grounding on any gseed that depended on the removed reference.
3. Notify users who have composed against the removed reference (if they consented to notifications).
4. Preserve the tombstone permanently so credit/attribution lineage remains auditable.
5. Complete within the MOU-specified window (default 30 days for general, 7 days for urgent).

### Finding 3: Freshness visibility matters more than freshness itself

Users don't need every reference to be live; they need to know when a reference is live vs. cached. Brief 101's tier-source labeling covers this; Brief 102 extends it with per-`ref://` freshness metadata.

### Finding 4: Legal hold is orthogonal to normal eviction

Some references become subject to legal hold (ongoing dispute, investigation, court order). Legal hold prevents eviction and prevents removal-on-request from completing until resolved. Legal hold status must be visible to users, to the partner, and to governance.

### Finding 5: Cache size grows unbounded without discipline

Without eviction, cache grows unbounded. With aggressive eviction, references disappear and grounding downgrades. The balance is per-namespace cost budgets (Brief 101 INV-426) combined with a priority score: Foundation Kernel refs > armory refs > active composition refs > inactive refs > unused refs.

## Inventions

### INV-429 — Partner-tiered retention policy

Every `ref://` gseed carries a partner-tier marker and a retention expiration derived from the partner's MOU terms. Eviction cannot proceed on a `ref://` before its retention expiration (absent removal-on-request or legal-hold pathways). Retention is governance-visible and MOU-enforced.

### INV-430 — Removal-on-request workflow as signed gseed sequence

A partner removal request becomes a signed `ref-removal-request://` gseed. The resulting tombstone is a `ref-tombstone://` gseed. The grounding downgrade on dependent seeds is a `grounding-downgrade://` notification gseed. The full workflow is lineage-tracked end-to-end and the SLA is measured against the request timestamp.

### INV-431 — Freshness metadata per `ref://`

Every `ref://` gseed carries:

- `fetched_at` — timestamp of last live fetch.
- `retention_expires_at` — when cache must evict or re-fetch.
- `freshness_label` — live / recent / aged / stale / legal-hold.
- `refresh_trigger` — manual / schedule / on-demand.

Studio surfaces the freshness label on every reference panel (Brief 103).

### INV-432 — Legal hold as orthogonal flag

A `ref://` gseed under legal hold carries a `legal-hold://` sibling gseed with the hold reason (redacted if necessary), the originating authority, and the expected duration. Legal holds block eviction and block removal-on-request. Legal hold status is public (the existence, not necessarily the reason).

### INV-433 — Priority-based eviction scoring

Eviction score combines:

- Age since last access.
- Composition depth (how many downstream gseeds depend on it).
- Namespace priority (Foundation Kernel > armory > active composition > inactive).
- Partner retention status.
- Legal hold status.

Eviction runs as a background sweep honoring the composite score. The sweep is logged and auditable.

### INV-434 — User-visible cache notifications

Users who compose against a `ref://` can opt into notifications for:

- The reference being removed on partner request.
- The reference being tombstoned for constitutional reasons.
- The reference being refreshed and showing a material change.
- The reference entering legal hold.

Notifications are signed `user-notification://` gseeds routed through the user's identity gseed.

### INV-435 — Quarterly cache audit

Every quarter, a signed `cache-audit://` gseed reports:

- Total `ref://` count by partner tier.
- Eviction count and breakdown.
- Removal requests received and SLA performance.
- Legal holds active.
- Downgrade cascades triggered.
- Storage cost per namespace.

Audit is public (aggregated) and shared with partners (per-partner).

## Phase 1 deliverables

**Months 0–3**
- Partner-tiered retention encoded from Brief 098 partner registry.
- Freshness metadata on every `ref://`.
- Studio freshness labels visible.

**Months 3–6**
- Removal-on-request workflow with SLA tracking.
- Priority-based eviction scoring.
- First quarterly cache audit published.

**Months 6–12**
- Legal hold mechanism operational (even without active hold, ready to use).
- User cache notifications wired to identity gseed.
- Second and third cache audits with cross-partner comparison.

## Risks

- **Partner removal request not completing within SLA.** Mitigation: the workflow is lineage-tracked with visible SLA; missed SLAs trigger governance review.
- **Legal hold misuse.** Mitigation: hold requires documented authority; abuse is detectable by audit.
- **Eviction scoring unfair to small contributors.** Mitigation: composition depth in the score protects small seeds with dependencies.
- **User notification fatigue.** Mitigation: opt-in per-reference, not per-notification; aggregation into weekly digests.

## Recommendation

**Adopt INV-429 through INV-435.** Cache lifecycle must be partner-aware from day one — partners are more likely to sign MOUs when they see the lifecycle discipline is already operational.

## Confidence

**4.5/5.** Cache lifecycle is a well-understood operational concern; the main novelty is integration with content-addressed lineage and partner MOUs. Risk is low.

## Spec impact

Brief 090, 091, 098 gain seven new inventions (INV-429..435). `ref-tombstone://`, `ref-removal-request://`, `legal-hold://`, `grounding-downgrade://`, `cache-audit://`, `user-notification://` join the lineage namespace. No substrate primitives change.

## Open follow-ups

- Storage cost modeling at 1M users.
- Encryption at rest for cached partner material.
- Cross-region cache replication tradeoffs.
- Backup and disaster recovery for cache state.

## Sources

- Cache eviction algorithm literature (LRU, LFU, ARC).
- GDPR right-to-erasure legal analysis (applicable to cache removal).
- Partner institutional retention policies (individually researched).
- Round 4 Briefs 090, 091, 098.
- Round 5 Brief 101.
