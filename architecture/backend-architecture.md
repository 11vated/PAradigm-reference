# Backend Architecture

The Paradigm backend is the persistence, indexing, federation, and commerce layer behind the Studio. It is **stateless at the request level**, **horizontally scalable**, and **federated by default**. This document specifies the canonical production stack, the request lifecycle, the data stores, the federation protocol's server side, and the deployment topology.

## Stack at a Glance

| Concern | Choice | Rationale |
|---|---|---|
| Runtime | Node.js ≥ 20 | Same TypeScript codebase as Studio + engines; uniform stack |
| HTTP framework | Fastify | 2× throughput vs Express, schema-validated routes, plugins-first |
| Primary database | PostgreSQL ≥ 15 with `pgvector` | Relational for users/payments; vector index for similarity |
| Search | Meilisearch | Sub-100ms full-text on millions of seeds, typo-tolerant |
| Vector search | Qdrant | Dedicated vector DB for style/embedding queries when pgvector hits limits |
| Cache / queue | Redis 7 | Session cache, rate limiting, Bull job queue |
| Object storage | S3-compatible (R2 / S3 / MinIO) | `.gseed`, exported artifacts, large blobs |
| Payments | Stripe Connect | Marketplace transactions, royalty splits, payouts |
| Federation transport | WebSocket (uWebSockets.js) | Low-latency, bidirectional, scalable |
| Auth | Passwordless email + WebAuthn (passkey) | Modern, no password storage |
| Observability | OpenTelemetry → Grafana stack | Traces, metrics, logs unified |
| Container | Docker + Kubernetes | Standard deploy target; can also run on Fly.io / Render |

The whole backend was migrated from `Express + better-sqlite3` to `Fastify + PostgreSQL + Redis + Meilisearch + Qdrant` in v3.0.0; the migration is complete and the legacy paths are removed.

## Service Topology

```
              ┌────────────────────────────┐
              │       Edge / CDN           │
              │   (Cloudflare / Fastly)    │
              └─────────────┬──────────────┘
                            │
                ┌───────────┼───────────┐
                ▼                       ▼
        ┌──────────────┐        ┌──────────────┐
        │ API Service  │        │ WS Federation│
        │  (Fastify)   │        │   Service    │
        └───────┬──────┘        └───────┬──────┘
                │                       │
                └───────────┬───────────┘
                            │
        ┌───────────┬───────┼───────┬───────────┐
        ▼           ▼       ▼       ▼           ▼
   ┌────────┐  ┌────────┐ ┌────┐ ┌────────┐ ┌────────┐
   │Postgres│  │  Redis │ │ S3 │ │Meili-  │ │ Qdrant │
   │ +pgvec │  │        │ │    │ │ search │ │        │
   └────────┘  └────────┘ └────┘ └────────┘ └────────┘
```

The API service and federation service are both stateless and scale horizontally behind a load balancer. State lives in the data plane (Postgres, Redis, S3, Meilisearch, Qdrant). A Bull worker pool processes background jobs (export rendering, federation reconciliation, payout sweeps).

## Data Model (Postgres)

Core tables:

```sql
-- Users
CREATE TABLE users (
  id            UUID PRIMARY KEY,
  email         TEXT UNIQUE NOT NULL,
  display_name  TEXT NOT NULL,
  identity_pk   BYTEA NOT NULL,           -- public key (DER)
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Seeds (content-addressed)
CREATE TABLE seeds (
  hash          BYTEA PRIMARY KEY,        -- 32 bytes, sha256 of canonical
  domain        TEXT NOT NULL,
  gst_version   TEXT NOT NULL,
  owner_user_id UUID REFERENCES users(id),
  payload       JSONB NOT NULL,           -- the full seed
  embedding     VECTOR(768),              -- pgvector style embedding
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX seeds_domain_idx ON seeds (domain);
CREATE INDEX seeds_owner_idx ON seeds (owner_user_id);
CREATE INDEX seeds_embedding_idx ON seeds USING ivfflat (embedding vector_cosine_ops);

-- Lineage edges
CREATE TABLE lineage_edges (
  child_hash    BYTEA REFERENCES seeds(hash),
  parent_hash   BYTEA REFERENCES seeds(hash),
  operation     TEXT NOT NULL,            -- "mutate" | "breed" | "compose:<functor>"
  generation    INT NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (child_hash, parent_hash)
);
CREATE INDEX lineage_parent_idx ON lineage_edges (parent_hash);

-- Marketplace listings
CREATE TABLE listings (
  id            UUID PRIMARY KEY,
  seed_hash     BYTEA REFERENCES seeds(hash),
  seller_id     UUID REFERENCES users(id),
  price_cents   INT NOT NULL,
  currency      TEXT NOT NULL DEFAULT 'usd',
  royalty_pct   NUMERIC(5,2) NOT NULL,    -- e.g., 5.00 = 5%
  active        BOOLEAN NOT NULL DEFAULT true,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Sales (ledger)
CREATE TABLE sales (
  id              UUID PRIMARY KEY,
  listing_id      UUID REFERENCES listings(id),
  buyer_id        UUID REFERENCES users(id),
  amount_cents    INT NOT NULL,
  platform_fee_cents INT NOT NULL,
  seller_share_cents INT NOT NULL,
  lineage_pool_cents INT NOT NULL,
  stripe_payment_intent TEXT NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Royalty payouts
CREATE TABLE royalty_payouts (
  id              UUID PRIMARY KEY,
  sale_id         UUID REFERENCES sales(id),
  ancestor_hash   BYTEA REFERENCES seeds(hash),
  recipient_id    UUID REFERENCES users(id),
  amount_cents    INT NOT NULL,
  generation_distance INT NOT NULL,
  paid_at         TIMESTAMPTZ
);
```

Additional tables for sessions, audit logs, federation peer state, C2PA manifests, and project organization. See [`infrastructure/db-schema.md`](../infrastructure/db-schema.md) for the complete migration set.

## Request Lifecycle

A typical user action (publish a seed) flows like this:

```
Client → POST /api/seeds
  → Fastify routes
    → Schema validation (the JSON body must match the seed JSON schema)
    → Auth middleware (verify signed cookie / session token)
    → Rate limit (Redis token bucket)
    → Service.publishSeed(seed, user_id)
      → Verify seed signature (sovereignty)
      → Verify content hash matches body
      → Insert into Postgres seeds table
      → Insert lineage edges into lineage_edges
      → Compute embedding vector (call embedding service)
      → Index in Meilisearch (full-text)
      → Index in Qdrant (vector)
      → Upload .gseed binary to S3 (content addressed)
      → Emit federation event to WS service
      → Return 201 + seed hash
```

Every step is observable via OpenTelemetry. Failures are typed and bubble up as structured 4xx/5xx with actionable error codes.

## Federation Service

The federation service runs in its own process. It maintains:

- A pool of WebSocket connections to peer Paradigm instances.
- A small-world graph topology (Watts–Strogatz) over peers.
- A migration queue of elite seeds to send and receive.

The protocol is described in [`architecture/evolution-stack.md`](evolution-stack.md). On the server side:

1. New peers register via a discovery API and exchange identity public keys.
2. The graph router selects 5–20 peer connections per node for low diameter and high clustering.
3. Migration messages are signed by the originating peer; receivers verify signatures before accepting.
4. Reconciliation jobs deduplicate seeds by hash (content-addressed → no conflict possible).

Federation never trusts incoming seeds blindly. Every received seed is re-grown locally (or its content hash is verified against a cached growth) before being shown in the gallery.

## Search

Two complementary search engines power discovery:

**Meilisearch** indexes the human-facing fields:

- `$name`, `$metadata.description`, archetype, domain, tags.
- Fast full-text with typo tolerance and prefix matching.
- Used in the studio's "browse the marketplace" pane.

**Qdrant** indexes vector embeddings:

- 768-dim style/embedding vectors derived from the seed's gene values.
- Cosine similarity search ("find seeds like this one").
- Used for "more like this" and recommendation.

The two are kept in sync by a background indexer that subscribes to Postgres logical replication and pushes changes into both engines.

## Caching Strategy

| Cache | TTL | Purpose |
|---|---|---|
| Seed payload by hash (Redis) | 1h | Hot read of marketplace listings |
| Embedding by seed hash (Redis) | 24h | Avoid recomputing embeddings |
| User session (Redis) | 7d sliding | Auth fast path |
| Rate limit buckets (Redis) | rolling 1m | Per-user QPS enforcement |
| Federated peer status (Redis) | 30s | Don't hammer peers on health checks |
| Compiled WGSL kernels (S3 + edge cache) | infinite | Studio downloads them at startup |

Content-addressed caching (everything keyed by seed hash) makes invalidation trivial: the data never changes for a given key, so no invalidation is needed. New content gets new hashes.

## Background Jobs (Bull / BullMQ)

| Queue | Job |
|---|---|
| `embed` | Compute embedding vector for a new seed |
| `index` | Push new seed to Meilisearch + Qdrant |
| `federate` | Send a seed to federation peers |
| `payout` | Compute and execute royalty payouts after a sale |
| `export` | Render an export artifact (e.g., 4K PNG, glTF) and upload to S3 |
| `audit` | Verify lineage chain integrity for a sample of seeds |

Jobs are idempotent and use seed hashes as deduplication keys.

## Payments

Stripe Connect is the only payments integration. The flow:

1. Sellers complete Stripe Connect onboarding the first time they list.
2. Buyers pay via Stripe checkout.
3. Stripe webhooks notify the API on payment success.
4. The `payout` job computes the royalty split per the algorithm in [`spec/05-sovereignty.md`](../spec/05-sovereignty.md).
5. Each ancestor's recipient gets a Stripe transfer.
6. The platform retains 10% as a marketplace fee.

The platform never holds raw card data; everything passes through Stripe.

## Auth

Passwordless email + WebAuthn passkey. No passwords are stored anywhere. The flow:

1. User enters email → server emails a magic link.
2. User clicks link → server exchanges for a session cookie.
3. On first login, user is prompted to register a passkey for future fast logins.
4. The session cookie is signed and stored client-side; server-side state in Redis.

User identity (the public key used to sign seeds) is **separate** from their account auth. A user can rotate their auth credentials without invalidating signed seeds.

## Compliance

| Requirement | Mechanism |
|---|---|
| C2PA (provenance) | Every uploaded artifact has a C2PA manifest in its `.gseed` appendix; verifier exposed at `/api/c2pa/verify` |
| EU AI Act Article 50 (Aug 2026) | Watermark all AI-generated outputs; manifest declares "AI-generated"; user-facing disclosure |
| California SB 942 (Jan 2026) | Same as above + AI detection tool exposed publicly |
| GDPR / CCPA | Right to delete, right to export, region-aware data residency |
| WCAG 2.1 AA | Studio accessibility (see studio-architecture) |

A `compliance/` module in the codebase enforces these checks at the API boundary; nothing reaches Postgres without passing validation.

## Observability

OpenTelemetry instruments the API service, federation service, and Bull workers. Spans, metrics, and structured logs all flow into a Grafana stack (Tempo for traces, Mimir for metrics, Loki for logs). Key dashboards:

- Request rate, latency, error rate (golden signals) per route.
- Federation peer connectivity and message flow.
- Payment success rate and payout backlog.
- Search query latency (Meilisearch and Qdrant).
- Worker queue depth per job type.
- GPU compute utilization (when fitness runs server-side).

Alerts page on-call when error rate > 1% sustained, federation peer count drops below threshold, or payout backlog grows beyond 1h.

## Deployment

Production deployment targets Kubernetes (or any container orchestrator). The deploy bundle:

```
deploy/
├── api/                    # Fastify API service Helm chart
├── federation/             # WebSocket federation service Helm chart
├── workers/                # Bull worker Helm chart
├── postgres/               # Managed (or operator) Postgres
├── redis/                  # Managed Redis cluster
├── meilisearch/            # Meilisearch StatefulSet
├── qdrant/                 # Qdrant StatefulSet
├── prometheus/             # Metrics
├── grafana/                # Dashboards
└── nginx-ingress/          # Ingress
```

The simplest valid deploy is a single-region setup. Multi-region deploys add a global load balancer in front, region-replicated Postgres (logical replication), and federation links between region clusters.

## Testing

| Layer | Test type |
|---|---|
| Unit | Service layer functions, every utility |
| Integration | Postgres + Redis + S3 against ephemeral containers |
| Contract | API routes against the schema, both directions |
| E2E | Studio flows via Playwright |
| Determinism | Re-grow sample seeds and byte-compare on every commit |
| Federation | Two-node peer simulation in CI |
| Load | k6 scripts simulating publish/browse/buy at target QPS |

Production targets at MVP:

- **1M users / 500K seeds by end of 2027.**
- **Sustained 1k req/s on the API service across read paths.**
- **p95 search latency < 100 ms.**
- **p95 grow latency depends on engine but < 1 s for fast engines.**
