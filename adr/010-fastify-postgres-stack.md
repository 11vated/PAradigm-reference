# ADR-010: Build the Backend on Fastify + PostgreSQL + pgvector

**Status:** Accepted
**Date:** 2024-12-01
**Layer:** Layer 6 (Studio & Marketplace) — Backend infrastructure

## Context

The Paradigm backend has to support:

1. User accounts, sovereignty-key management, and passkey auth.
2. Seed storage with content-addressable hashing and lineage edges.
3. Vector similarity search over the seed manifold (Fisher-Rao embeddings).
4. Full-text search over seed metadata, tags, and descriptions.
5. Stripe Connect for marketplace royalty payouts.
6. WebSocket federation for real-time peer-to-peer seed exchange.
7. Background job queues for evolution batches and exports.

It needs to scale from "1 founder + early adopters" to "1M users / 500K seeds by end of 2027."

## Decision

The backend stack is:

- **Runtime:** Node.js LTS (≥20)
- **HTTP framework:** Fastify (for raw speed and schema-based validation)
- **Primary database:** PostgreSQL 16 with the **pgvector** extension for vector similarity
- **Cache / pub-sub:** Redis 7
- **Full-text search:** Meilisearch (small footprint, fast, easy to self-host)
- **Vector search:** pgvector inside PostgreSQL for joins; Qdrant as a separate vector index for very-large-scale recall queries
- **Background jobs:** Bull (Redis-backed)
- **Payments:** Stripe Connect Custom (for marketplace payouts)
- **Auth:** Passwordless email magic links + WebAuthn passkeys
- **Realtime:** uWebSockets.js for federation channels
- **Deployment:** Kubernetes (DigitalOcean or Fly.io for MVP, AWS EKS for scale)
- **Observability:** OpenTelemetry → Tempo / Loki / Prometheus / Grafana

See [`architecture/backend-architecture.md`](../architecture/backend-architecture.md) for the full topology, schema, and request lifecycle.

## Consequences

**Positive:**

- Fastify is 2-3× faster than Express, with built-in JSON-schema validation and a plugin ecosystem mature enough for production.
- PostgreSQL is the safest possible choice for the primary store. We get ACID transactions, JSONB columns for the flexible parts, foreign keys for the strict parts, and pgvector for the vector parts — all in one database.
- pgvector supports HNSW and IVF indexes; recall is excellent up to ~10M vectors before we need a dedicated vector store.
- Single-database simplicity for the MVP. No microservice fragmentation. We can shard later if needed.
- Stripe Connect handles KYC, tax, and payout compliance for us — we cannot afford to build a payments stack ourselves.
- Passkeys are user-friendly and phishing-resistant; magic links are the universal fallback.
- Open-source observability stack means no per-MB log charges.

**Negative:**

- Node.js has well-known weaknesses for CPU-bound work. We push CPU-bound work (evolution, mesh extraction, hashing of large blobs) into Rust services accessed via HTTP/gRPC or WebAssembly modules.
- pgvector recall degrades above ~20M vectors. Migration to Qdrant or Weaviate will be required at scale.
- Single-DB architecture means a Postgres outage takes the whole platform down. We mitigate with managed Postgres + read replicas + frequent backups.

## Alternatives Considered

- **Rust backend (Axum / Actix):** Faster, more efficient. Strongly considered. Rejected for the MVP because the Node ecosystem is far richer for the full-stack web work (Stripe SDK, WebAuthn, Meilisearch client). We may rewrite hot paths in Rust as needed.
- **Go backend:** Same arguments as Rust, slightly weaker library ecosystem. Same conclusion.
- **Supabase / Firebase:** Faster to ship but locks us into a vendor and limits our control over Postgres extensions and federation behavior. Rejected.
- **Microservices from day one:** Modular but operationally complex for a solo founder. Rejected. We will split services along clean seams (evolution worker, federation node, payments) only when scale demands it.
- **MongoDB / Cassandra:** No transactions or referential integrity. Rejected; lineage and royalty graphs need foreign keys.

## Reassessment triggers

We will revisit this ADR when:

- DAU exceeds 100K — may need read replicas and queue partitioning.
- Vector index exceeds 20M entries — migrate to dedicated vector store.
- Federation traffic exceeds 10K msgs/sec/node — consider Rust rewrite of the federation gateway.

## References

- *Fastify Benchmarks*: https://www.fastify.io/benchmarks/
- *pgvector*: https://github.com/pgvector/pgvector
- *Stripe Connect Custom*: https://stripe.com/docs/connect/custom-accounts
