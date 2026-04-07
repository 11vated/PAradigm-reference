# Production Stack

## Goal

Run Paradigm at scale: from solo founder + early adopters today to **1M users / 500K seeds by end of 2027**, with a clear path to 10M users without re-architecture.

## Topology

```
                ┌────────────────────────────────────────┐
                │             CloudFlare CDN             │
                └──────────────────┬─────────────────────┘
                                   │
                ┌──────────────────▼─────────────────────┐
                │       Ingress (NGINX / Traefik)        │
                └──────────────────┬─────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
┌───────▼─────────┐    ┌───────────▼──────────┐    ┌──────────▼──────────┐
│  Studio (web)   │    │   API gateway        │    │  Federation gateway │
│  React/Vite SPA │    │   Fastify (Node)     │    │  uWebSockets (Node) │
└─────────────────┘    └───────────┬──────────┘    └──────────┬──────────┘
                                   │                          │
            ┌──────────────────────┼──────────────────┐       │
            │                      │                  │       │
   ┌────────▼────────┐  ┌──────────▼──────┐  ┌────────▼───────┴──┐
   │  Engine workers │  │  Agent workers  │  │ Federation nodes  │
   │  (Rust + WGPU)  │  │  (Node + LLMs)  │  │ (Node, peers)     │
   └────────┬────────┘  └────────┬────────┘  └────────┬──────────┘
            │                    │                     │
            └────────┬───────────┴─────────────────────┘
                     │
        ┌────────────┴─────────────┐
        │                          │
┌───────▼───────┐         ┌────────▼────────┐
│  Postgres 16  │         │     Redis 7     │
│  + pgvector   │         │  cache + queue  │
└───────┬───────┘         └─────────────────┘
        │
        ▼
┌─────────────────┐    ┌─────────────────┐
│  Meilisearch    │    │     Qdrant      │
│  (full-text)    │    │ (vector index)  │
└─────────────────┘    └─────────────────┘
```

## Service inventory

| Service | Tech | Replicas (MVP / Scale) | Purpose |
|---|---|---|---|
| `studio-web` | React + Vite (static) | n/a (CDN) | The studio SPA. |
| `api-gateway` | Fastify | 2 / 20 | All HTTP API endpoints. |
| `federation-gateway` | uWebSockets.js | 1 / 8 | WebSocket peer federation. |
| `engine-worker` | Rust + WGPU | 2 / 32 | Runs domain engines for evolution and exports. |
| `agent-worker` | Node + LLM SDKs | 2 / 16 | Runs the GSPL Agent pipeline. |
| `compiler-worker` | Rust | 1 / 4 | GSPL → IR → WGSL compilation. |
| `postgres-primary` | Postgres 16 | 1 / 1 | Source of truth. |
| `postgres-replica` | Postgres 16 | 0 / 4 | Read replicas (scale tier only). |
| `redis` | Redis 7 | 1 / 3 (cluster) | Cache + queue + pub-sub. |
| `meilisearch` | Meilisearch 1.x | 1 / 2 | Full-text search. |
| `qdrant` | Qdrant 1.x | 0 / 3 | Vector index for very-large recall (scale tier only). |
| `prometheus` | Prometheus | 1 / 1 | Metrics. |
| `loki` | Loki | 1 / 2 | Logs. |
| `tempo` | Tempo | 1 / 2 | Traces. |
| `grafana` | Grafana | 1 / 1 | Dashboards + alerting. |

The MVP runs on a single Kubernetes cluster with ~16 vCPU / 64 GB RAM. The scale tier needs ~256 vCPU / 1 TB RAM across multiple nodes.

## Request lifecycle

A typical "create a sprite" request flows like this:

1. **Studio → CDN → Ingress → API gateway** — HTTP `POST /v1/agent/create` with the user's concept.
2. **API gateway** — JWT verification, rate-limit check, schema validation.
3. **API gateway → BullMQ queue** — enqueue an `agent_create` job with the user's concept and conversation context.
4. **Agent worker** — picks up the job, runs the 5-stage GSPL Agent pipeline. Stages 1-3 call LLM providers; stages 4-5 are local. The output is a draft seed.
5. **Agent worker → Engine worker** — validation pass: run the engine on the draft seed to verify it.
6. **Engine worker → Postgres** — write seed row, lineage edges, embeddings.
7. **Agent worker → Redis pub-sub** — emit `seed_created` event.
8. **Federation gateway** — receives the event, forwards to subscribed peers if the user has opted in to federation.
9. **API gateway → Studio** — long-poll or WebSocket response with the new seed.

End-to-end: 4-12 seconds for a basic sprite, dominated by LLM call time and engine evaluation.

## Scaling targets

| Metric | MVP (today) | End of 2027 |
|---|---|---|
| Active users | <1K | 1M |
| Total seeds | <10K | 500K |
| Seeds created/day | 100 | 50K |
| Federation messages/day | 1K | 10M |
| Agent runs/day | 200 | 100K |
| Database size | <10 GB | ~2 TB |
| Vector index size | <100K | 5M |

The path from MVP to scale is **horizontal scaling only** — every service is stateless except Postgres, Redis, and the search/vector indexes, all of which scale by sharding or read replicas.

## Database scaling plan

- **0-100K seeds:** single Postgres primary, no replicas. ~10 GB.
- **100K-1M seeds:** add 2 read replicas, route reads through pgbouncer. ~50 GB.
- **1M-10M seeds:** add 4 read replicas, partition the `seeds` table by `created_at`. ~500 GB.
- **10M+ seeds:** evaluate Citus or shard manually by user_id; migrate vector index to Qdrant.

Postgres handles the entire range comfortably with proper indexing and partitioning.

## Caching layers

| Cache | TTL | Storage | Hit rate target |
|---|---|---|---|
| HTTP responses (API gateway) | 60s | Redis | 30% |
| Engine renders (by seed hash) | 24h | Redis + S3 blob | 80% |
| Agent intent classifications | 1h | Redis | 50% |
| Template lookups | 15m | Redis | 95% |
| User session | 30d | Redis | 99% |
| Functor pathfinding results | persistent | In-process | 99.9% |

## Background job queues

BullMQ on Redis. Three queues with priorities:

- `interactive` (priority 1) — agent runs, single-seed evolution steps. Target latency: <10s.
- `batch` (priority 2) — bulk evolution, exports, large-archive computations. Target latency: <5min.
- `maintenance` (priority 3) — backups, index rebuilds, cleanup. Off-peak only.

Each queue has its own worker pool sized independently. Workers are autoscaled by queue depth via a custom HPA controller.

## Observability

- **Metrics:** Prometheus scrapes every service. Service-level objectives:
  - `api_p95_latency < 200ms`
  - `agent_p95_latency < 12s`
  - `engine_p95_latency < 5s`
  - `error_rate < 0.1%`
- **Logs:** structured JSON via pino, shipped to Loki via promtail.
- **Traces:** OpenTelemetry, sampled at 10% (100% for errors), shipped to Tempo.
- **Dashboards:** Grafana with one dashboard per service plus a top-level "Service Health" overview.
- **Alerting:** Grafana → PagerDuty → on-call engineer.

## Deployment

- Source of truth: GitOps via ArgoCD watching the `gspl-deploy` Git repo.
- Container registry: GitHub Container Registry (ghcr.io).
- Image signing: Sigstore Cosign, verified at admission control by Kyverno.
- Rollouts: Argo Rollouts with canary strategy (10% → 50% → 100%) over 30 minutes.
- Rollbacks: automatic on SLO breach detected by Prometheus alerts.

## Disaster recovery

- **RPO:** ≤ 5 minutes (continuous WAL shipping to S3).
- **RTO:** ≤ 1 hour (warm standby region with managed Postgres + Redis).
- **Backups:** daily full + hourly incremental, retained 30 days. Tested monthly via restore-to-staging.
- **Multi-region:** single-region for MVP. Multi-region promotion when DAU > 100K.

## Cost projections

| Tier | Monthly cost (USD) |
|---|---|
| MVP (1K users) | ~$300 (single small VPS cluster) |
| Early growth (10K users) | ~$1,800 |
| Mid (100K users) | ~$12,000 |
| Scale (1M users) | ~$60,000 |

LLM costs are *not* in these numbers; they are passed through as platform fees per agent run.

## Security baseline

- TLS 1.3 everywhere; cert-manager + Let's Encrypt.
- mTLS between services inside the cluster (Linkerd or Istio sidecar mesh).
- Secrets in Kubernetes via External Secrets Operator → 1Password / AWS Secrets Manager.
- Vulnerability scanning: Trivy on every image build.
- Dependency scanning: Renovate + Dependabot + cargo-audit.
- Pen testing: annual third-party assessment starting at 10K users.
