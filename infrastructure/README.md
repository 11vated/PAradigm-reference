# Infrastructure

This directory documents the production infrastructure of Paradigm — the libraries we depend on, the database schema, the GPU compute kernels, and the observability stack. These docs are aimed at engineers who need to spin up, modify, or operate a Paradigm deployment.

## Index

| File | Topic |
|---|---|
| [`library-canon.md`](library-canon.md) | The pinned set of third-party libraries with rationale |
| [`production-stack.md`](production-stack.md) | Runtime topology, scaling targets, deployment |
| [`db-schema.md`](db-schema.md) | Postgres schema with all tables, indexes, constraints |
| [`gpu-kernels.md`](gpu-kernels.md) | WGSL compute shaders for hot paths |
| [`gseed-format.md`](gseed-format.md) | Binary spec for the .gseed file format |

## Principles

1. **Every dependency is pinned and justified.** No library is used without a written rationale that explains why it was chosen and what was rejected. See `library-canon.md`.
2. **Reproducibility over convenience.** When two libraries are equivalent and one is more deterministic, the deterministic one wins.
3. **Open source first.** A paid SaaS is only acceptable if there is no viable open-source alternative (Stripe is the canonical example).
4. **Boring tech wins.** Postgres, Redis, Fastify, Kubernetes — all proven, all hireable, all stable.
5. **Each layer is independently deployable.** No layer can require a coordinated rollout of two services.
