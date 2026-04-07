# Phase 4 — GSPL Agent and Studio MVP

**Duration:** Months 8-10 (12 weeks)
**Goal:** A natural-language interface (the GSPL Agent) and a minimal but complete Studio web app on top of it. At the end, a user can sign in, type "make me a melancholy bard," and download a signed sprite atlas.

## Why this is fourth

The agent depends on engines (which produce the seeds), evolution (which lets it iterate), and the kernel (for signing). The Studio depends on the agent. Building either before the foundations would force rework. By month 8 the foundations are stable enough to build a UI on top.

## Deliverables

| Deliverable | Acceptance |
|---|---|
| Intent classifier (Stage 1) | 90%+ accuracy on 200-prompt test set |
| Spec resolver (Stage 2) | Adjective normalization + template selection |
| Planner (Stage 3) | Outputs deterministic construction plans |
| Assembler (Stage 4) | Builds GSPL programs from plans |
| Validator (Stage 5) | Runs the engine and gates output on quality vector |
| 8 sub-agents | All 8 implemented and integration-tested |
| 4-layer memory system | Working, encrypted, RLS-enforced |
| Template Bridge | At least 30 templates across domains |
| LLM provider integrations | Anthropic primary, OpenAI fallback, retry+circuit-breaker |
| Studio web app | Auth, projects, seeds, agent chat, evolution UI, export |
| WCAG 2.2 AA pass | First-pass audit clean |
| API gateway | Fastify with all v1 endpoints |

## Week-by-week plan

### Week 1: Intent classifier + spec resolver

- Stage 1 implementation per `intelligence/intent-taxonomy.md`
- Build a 200-prompt test set covering all 33 sub-intents
- Adjective normalizer per `intelligence/adjective-normalization.md`
- Test: 90%+ classification accuracy

### Week 2: Planner + Assembler + Validator

- Stage 3 planner: from spec → construction plan
- Stage 4 assembler: from plan → GSPL source → compile → seed
- Stage 5 validator: run engine + check quality vector
- End-to-end test: canonical "melancholy bard" prompt → signed `.gseed`

### Week 3: Sub-agents (parallel sub-tasks)

Implement and test each in parallel where possible:
- VisionAgent
- PersonalityAgent
- MusicTheoryAgent
- MechanicsAgent
- NarrativeAgent
- PhysicsAgent
- StyleAgent
- CritiqueAgent

Each per `intelligence/8-sub-agents.md`.

### Week 4: Memory system

- Layer 1 (working): in-memory ConversationContext
- Layer 2 (episodic): Postgres + per-user encryption
- Layer 3 (semantic): workspace-level shared memory
- Layer 4 (world knowledge): curated public topics
- RLS policies enforced
- Cross-layer lookup ordering tests

### Week 5: Template Bridge + LLM integration

- Template registry per `intelligence/template-bridge.md`
- Author 30 templates: 10 sprite, 10 music, 5 sculpt, 5 mixed
- LLM provider abstraction (Anthropic + OpenAI)
- Retry with exponential backoff, circuit breaker, structured-output validation
- Cost tracking + per-user budget

### Week 6: API gateway scaffolding

- Fastify app with: JWT auth, CORS, rate limiting, request logging
- Endpoint groups:
  - `/v1/auth/*` (passkeys)
  - `/v1/seeds/*`
  - `/v1/agent/*`
  - `/v1/evolution/*`
  - `/v1/exports/*`
- OpenAPI spec generated from route definitions
- Postgres + pgvector + Redis wired up
- BullMQ queues for async work

### Week 7: Studio scaffolding

- Vite + React + TS + Tailwind
- Auth flow (passkeys via @simplewebauthn/browser)
- Routing (wouter)
- Layout: sidebar (projects), main (current view), panel (agent chat)
- Project list and project detail pages
- Seed gallery view

### Week 8: Studio — agent chat

- Chat panel with streaming responses
- Display intent classification + plan + draft seed inline
- "Apply" button to accept or "Refine" to iterate
- Loading states, error states, retry flows
- Accessibility pass on the chat panel

### Week 9: Studio — seed detail + evolution

- Seed detail view: 3D viewport (Three.js) + gene tree (DOM)
- Evolution panel: start a run, watch progress, browse archive
- Mutation operator picker
- Quality vector visualization (radar chart)
- Cancel / save run controls

### Week 10: Studio — export + Studio polish

- Export panel: choose format, options (resolution, frames, etc.)
- C2PA badge on export results
- Settings page (profile, preferences, accessibility)
- Empty states, error pages, 404
- Loading skeletons everywhere
- First WCAG 2.2 AA audit pass

### Week 11: End-to-end testing

- Playwright tests covering 20 critical user journeys
- Cross-browser: Chromium, Firefox, WebKit
- Performance budget: page load <2s on 4G, agent first response <12s
- Bug bash with 3 friendly external users

### Week 12: Hardening + deployment

- Deploy to staging on the production stack from `infrastructure/production-stack.md`
- Load test: 100 concurrent users
- Observability dashboards live in Grafana
- Documentation: getting-started, agent prompting tips, accessibility statement
- Tag `paradigm-0.4.0`

## Risks and mitigations

**Risk:** Agent latency exceeds 12s p95 (the SLO).
**Mitigation:** Cache intent classification, run sub-agents in parallel where possible, use smaller/faster models for classification stage, fall back to a "puppet" agent for known templates.

**Risk:** Agent quality is inconsistent — one prompt produces great output, the next garbage.
**Mitigation:** CritiqueAgent in the loop; templated guardrails; confidence-gated retries.

**Risk:** WCAG audit reveals deep accessibility debt.
**Mitigation:** Build on Radix from day one; use axe-core in CI; do a self-audit in week 10 before week 11 testing.

**Risk:** LLM provider outages.
**Mitigation:** Anthropic primary, OpenAI fallback, circuit breaker at 3 consecutive failures, queue-with-retry for batch work.

## What is *not* in Phase 4

- No marketplace (Phase 5)
- No federation (Phase 5)
- No public verifier tool (Phase 5)
- No mobile or native clients (post-v1)
- No fine-tuning of models (post-v1)

## Done definition

1. The canonical "melancholy bard" prompt produces a signed export end-to-end through the Studio.
2. A new user can sign up and produce their first export in <60s.
3. The Studio passes WCAG 2.2 AA self-audit.
4. Staging is up, dashboards green, error rate <1%.
5. Tag `paradigm-0.4.0`.
