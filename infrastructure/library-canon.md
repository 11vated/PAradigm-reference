# Library Canon

This is the canonical list of every third-party library Paradigm depends on. Each entry is pinned to a major version and carries a one-line rationale. New dependencies require an ADR.

## Backend (Node.js)

| Library | Purpose | Version | Why |
|---|---|---|---|
| `fastify` | HTTP framework | 4.x | Fastest mature Node framework with schema validation built in. |
| `@fastify/jwt` | JWT auth | 8.x | First-party plugin, no surprises. |
| `@fastify/cors` | CORS | 9.x | Standard. |
| `@fastify/rate-limit` | Rate limiting | 9.x | Standard. |
| `pg` | Postgres driver | 8.x | Most-used Node driver, battle-tested. |
| `pgvector-node` | pgvector client | 0.x | Direct pgvector type bindings. |
| `kysely` | Type-safe SQL builder | 0.27.x | TypeScript-native, generates query types from schema. |
| `redis` | Redis client | 4.x | Official client, supports streams. |
| `bullmq` | Job queue | 5.x | Best Redis-backed queue with priorities and retries. |
| `meilisearch` | Search client | 0.40.x | Official Meilisearch client. |
| `@qdrant/js-client-rest` | Vector index client | 1.x | Official Qdrant REST client. |
| `stripe` | Payments | 16.x | Official Stripe Node SDK. |
| `nodemailer` | Email | 6.x | Standard for transactional email. |
| `@simplewebauthn/server` | Passkey auth | 10.x | Best-maintained WebAuthn library. |
| `pino` | Logging | 9.x | Fast, structured, JSON-native. |
| `@opentelemetry/sdk-node` | Tracing | 0.50.x | Official OTel for Node. |
| `zod` | Schema validation | 3.x | The TypeScript-native schema validator. |
| `msgpackr` | MessagePack | 1.x | Fastest MessagePack codec for Node. |
| `@noble/curves` | Crypto (ECDSA) | 1.x | Audited, dependency-free elliptic curves. |
| `@noble/hashes` | Crypto (SHA-256) | 1.x | Audited, dependency-free hashes. |
| `c2pa-node` | C2PA manifest writing | 0.x | Wraps the official c2pa-rs library. |
| `uWebSockets.js` | WebSockets | 20.x | Fastest WS library for Node. |

## Frontend (Studio web app)

| Library | Purpose | Version | Why |
|---|---|---|---|
| `react` | UI framework | 19.x | Largest ecosystem; concurrent features matter for studio interactivity. |
| `react-dom` | DOM renderer | 19.x | Pair with react. |
| `vite` | Build tool | 5.x | Fast HMR, simple config. |
| `typescript` | Type system | 5.6.x | Required by every other choice. |
| `zustand` | State management | 4.x | Tiny, hookable, no boilerplate. |
| `@tanstack/react-query` | Server state | 5.x | The standard for server state. |
| `wouter` | Routing | 3.x | Tiny router; we don't need React Router's complexity. |
| `tailwindcss` | Styling | 3.x | Productivity multiplier in design-iterative work. |
| `radix-ui` | Primitives | latest | Headless, accessible UI primitives. |
| `lucide-react` | Icons | latest | Comprehensive, consistent icon set. |
| `framer-motion` | Animation | 11.x | Best React animation library. |
| `three` | 3D rendering | 0.16x.x | The standard browser 3D engine. |
| `@react-three/fiber` | React bindings for Three | 8.x | React-friendly Three.js. |
| `tone` | Audio | 14.x | Best browser audio library. |
| `pixi.js` | 2D rendering | 8.x | For Sprite engine previews. |
| `comlink` | Web Worker RPC | 4.x | Cleanest Worker bridge. |
| `idb` | IndexedDB wrapper | 8.x | Simple promises for IndexedDB. |
| `@simplewebauthn/browser` | Passkeys (client) | 10.x | Pair with the server library. |
| `msgpackr` | MessagePack | 1.x | Same as backend; shared. |

## Engine implementations (Rust workers)

| Library | Purpose | Version | Why |
|---|---|---|---|
| `tokio` | Async runtime | 1.x | The Rust async standard. |
| `axum` | HTTP framework | 0.7.x | Tokio-native, ergonomic. |
| `serde` | Serialization | 1.x | Required for everything. |
| `serde_json` | JSON | 1.x | Standard. |
| `rmp-serde` | MessagePack | 1.x | Serde-integrated MessagePack. |
| `p256` | ECDSA P-256 | 0.13.x | Pure-Rust ECDSA, audited. |
| `sha2` | SHA-256 | 0.10.x | Standard. |
| `pgvector` | pgvector client | 0.x | Rust pgvector bindings. |
| `wgpu` | GPU compute | 0.x | The Rust WebGPU implementation. |
| `image` | Image codecs | 0.25.x | Rust image library, pinned to a deterministic feature set. |
| `nalgebra` | Linear algebra | 0.32.x | More mature than glam for our matrix-heavy workloads. |
| `kiddo` | k-d tree | 4.x | Fastest k-d tree for Rust; novelty search and FIM. |
| `c2pa` | C2PA manifests | 0.x | Official Adobe c2pa-rs. |
| `opentelemetry` | Tracing | 0.24.x | OTel for Rust. |

## GSPL compiler (also Rust)

| Library | Purpose | Version | Why |
|---|---|---|---|
| `chumsky` | Parser combinators | 0.9.x | Best parser combinator lib for Rust with good error messages. |
| `ariadne` | Diagnostics | 0.4.x | Beautiful compiler error rendering. |
| `rustc-hash` | Fast hashing | 2.x | Deterministic FxHash for compiler internal maps. |
| `lasso` | String interning | 0.7.x | For compiler symbol tables. |
| `salsa` | Incremental computation | 0.16.x | For incremental type checking and codegen. |

## Infrastructure / DevOps

| Library / Tool | Purpose | Version |
|---|---|---|
| `Postgres` | Primary DB | 16 |
| `pgvector` | Vector extension | 0.7+ |
| `Redis` | Cache + queue | 7 |
| `Meilisearch` | Full-text search | 1.x |
| `Qdrant` | Vector DB (scale tier) | 1.x |
| `Kubernetes` | Orchestration | 1.30+ |
| `Helm` | K8s packaging | 3.x |
| `Grafana` | Dashboards | 11.x |
| `Loki` | Logs | 3.x |
| `Tempo` | Traces | 2.x |
| `Prometheus` | Metrics | 2.x |
| `cert-manager` | TLS automation | 1.x |
| `external-dns` | DNS automation | 0.14.x |

## Testing

| Library | Purpose |
|---|---|
| `vitest` | TypeScript unit tests |
| `playwright` | E2E browser tests |
| `cargo-nextest` | Rust test runner |
| `proptest` | Rust property-based testing |
| `fast-check` | TypeScript property-based testing |
| `criterion` | Rust benchmarks |

## Update policy

- **Major versions:** require an ADR. Often contain breaking changes.
- **Minor versions:** auto-applied weekly via Renovate, gated on CI passing.
- **Patch versions:** auto-applied within 24h via Renovate (security CVEs trigger immediate apply).
- **Pinning:** all dependencies pinned to exact versions in lockfiles. No floating ranges in production.

## Forbidden libraries

Some libraries are explicitly *not* allowed:

- **lodash** — bloated; use native ES2024 equivalents.
- **moment.js** — deprecated; use `date-fns` or native `Intl.DateTimeFormat`.
- **request** — deprecated; use `undici`.
- **left-pad** — historical lesson in dependency hygiene.
- Any library without an audited license (must be MIT, Apache-2.0, BSD, or similar permissive).

## License compliance

We track licenses with `license-checker` (Node) and `cargo-deny` (Rust). The CI fails if any new dependency carries a copyleft license (GPL, AGPL, LGPL beyond v3.0 with exception). Paradigm itself is published under Apache-2.0.
