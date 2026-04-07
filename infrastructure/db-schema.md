# Database Schema

The Paradigm production database is **PostgreSQL 16 with the pgvector extension**. This document specifies every table, column, index, and constraint.

## Conventions

- All timestamps are `TIMESTAMPTZ` and stored in UTC.
- All primary keys are `UUID v7` (time-ordered) generated server-side.
- All `created_at` and `updated_at` columns are auto-managed by triggers.
- `JSONB` is used for flexible-shape columns; everything else is strictly typed.
- All foreign keys have `ON DELETE` rules explicitly specified — no implicit cascades.
- All tables have row-level security enabled where they touch user data.

## Extensions

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";        -- pgvector
CREATE EXTENSION IF NOT EXISTS "pg_trgm";       -- trigram fuzzy search
CREATE EXTENSION IF NOT EXISTS "btree_gin";     -- composite GIN indexes
```

## Tables

### `users`

```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    email           TEXT UNIQUE NOT NULL,
    display_name    TEXT NOT NULL,
    sovereignty_pubkey JSONB NOT NULL,           -- JWK format
    sovereignty_thumbprint TEXT UNIQUE NOT NULL, -- RFC 7638 thumbprint
    stripe_account_id TEXT,                       -- Stripe Connect account
    role            TEXT NOT NULL DEFAULT 'user', -- 'user' | 'curator' | 'admin'
    is_verified     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX users_thumbprint_idx ON users(sovereignty_thumbprint);
CREATE INDEX users_email_idx ON users(email);
```

### `passkeys`

```sql
CREATE TABLE passkeys (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    credential_id   BYTEA NOT NULL UNIQUE,
    public_key      BYTEA NOT NULL,
    counter         BIGINT NOT NULL DEFAULT 0,
    transports      TEXT[],
    nickname        TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_used_at    TIMESTAMPTZ
);

CREATE INDEX passkeys_user_idx ON passkeys(user_id);
```

### `seeds`

The most important table. Each row is one canonical seed.

```sql
CREATE TABLE seeds (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    hash            TEXT UNIQUE NOT NULL,        -- SHA-256 of canonical JSON
    domain          TEXT NOT NULL,                -- 'sprite' | 'character' | ...
    payload         JSONB NOT NULL,               -- the canonical seed JSON
    signature       BYTEA NOT NULL,               -- ECDSA P-256 (r||s)
    author_id       UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    parent_count    INTEGER NOT NULL DEFAULT 0,
    quality_vector  REAL[],                       -- 6-axis QualityVector
    quality_scalar  REAL,                         -- weighted scalar
    embedding       vector(384),                  -- Fisher-Rao or contrastive
    title           TEXT,
    description     TEXT,
    tags            TEXT[],
    license         TEXT NOT NULL DEFAULT 'CC-BY-4.0',
    visibility      TEXT NOT NULL DEFAULT 'private', -- 'private' | 'unlisted' | 'public'
    is_marketplace  BOOLEAN NOT NULL DEFAULT FALSE,
    federation_origin TEXT,                         -- node URL if imported
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX seeds_author_idx ON seeds(author_id);
CREATE INDEX seeds_domain_idx ON seeds(domain);
CREATE INDEX seeds_visibility_idx ON seeds(visibility);
CREATE INDEX seeds_tags_idx ON seeds USING GIN(tags);
CREATE INDEX seeds_payload_idx ON seeds USING GIN(payload jsonb_path_ops);
CREATE INDEX seeds_embedding_idx ON seeds USING hnsw (embedding vector_cosine_ops);
CREATE INDEX seeds_created_idx ON seeds(created_at DESC);
CREATE UNIQUE INDEX seeds_hash_idx ON seeds(hash);
```

`seeds` is partitioned by `created_at` (monthly partitions) starting at 1M rows.

### `lineage_edges`

Directed parent → child edges with optional functor metadata.

```sql
CREATE TABLE lineage_edges (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    parent_seed_id  UUID NOT NULL REFERENCES seeds(id) ON DELETE CASCADE,
    child_seed_id   UUID NOT NULL REFERENCES seeds(id) ON DELETE CASCADE,
    relation        TEXT NOT NULL,                -- 'mutation' | 'crossover' | 'functor' | 'composition'
    functor_id      TEXT,                          -- non-null when relation = 'functor'
    weight          REAL NOT NULL DEFAULT 1.0,    -- for royalty distribution
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (parent_seed_id, child_seed_id, relation)
);

CREATE INDEX lineage_parent_idx ON lineage_edges(parent_seed_id);
CREATE INDEX lineage_child_idx ON lineage_edges(child_seed_id);
```

### `listings`

Marketplace listings.

```sql
CREATE TABLE listings (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    seed_id         UUID NOT NULL REFERENCES seeds(id) ON DELETE CASCADE,
    seller_id       UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    price_cents     INTEGER NOT NULL,
    currency        TEXT NOT NULL DEFAULT 'USD',
    royalty_pct     REAL NOT NULL DEFAULT 0.10,  -- to ancestors on derivative sales
    status          TEXT NOT NULL DEFAULT 'active', -- 'active' | 'sold' | 'unlisted'
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX listings_seller_idx ON listings(seller_id);
CREATE INDEX listings_status_idx ON listings(status);
```

### `sales`

Each sale event.

```sql
CREATE TABLE sales (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    listing_id          UUID NOT NULL REFERENCES listings(id) ON DELETE RESTRICT,
    buyer_id            UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    seller_id           UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    seed_id             UUID NOT NULL REFERENCES seeds(id) ON DELETE RESTRICT,
    gross_cents         INTEGER NOT NULL,
    platform_fee_cents  INTEGER NOT NULL,
    royalty_pool_cents  INTEGER NOT NULL,
    net_seller_cents    INTEGER NOT NULL,
    stripe_payment_intent TEXT NOT NULL UNIQUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX sales_buyer_idx ON sales(buyer_id);
CREATE INDEX sales_seller_idx ON sales(seller_id);
CREATE INDEX sales_seed_idx ON sales(seed_id);
```

### `royalty_payouts`

Royalty distribution to ancestor authors after a derivative sale.

```sql
CREATE TABLE royalty_payouts (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    sale_id         UUID NOT NULL REFERENCES sales(id) ON DELETE RESTRICT,
    recipient_id    UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    ancestor_seed_id UUID NOT NULL REFERENCES seeds(id) ON DELETE RESTRICT,
    weight          REAL NOT NULL,
    cents           INTEGER NOT NULL,
    stripe_transfer_id TEXT,
    status          TEXT NOT NULL DEFAULT 'pending', -- 'pending' | 'paid' | 'failed'
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    paid_at         TIMESTAMPTZ
);

CREATE INDEX royalty_recipient_idx ON royalty_payouts(recipient_id);
CREATE INDEX royalty_status_idx ON royalty_payouts(status);
```

### `agent_runs`

Cached agent invocations for replay and debugging.

```sql
CREATE TABLE agent_runs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    user_id         UUID REFERENCES users(id) ON DELETE SET NULL,
    conversation_id TEXT NOT NULL,
    concept_text    TEXT NOT NULL,
    concept_hash    TEXT NOT NULL,
    parsed_intent   JSONB,
    resolved_spec   JSONB,
    construction_plan JSONB,
    output_seed_id  UUID REFERENCES seeds(id) ON DELETE SET NULL,
    agent_version   TEXT NOT NULL,
    provider        TEXT NOT NULL,
    model           TEXT NOT NULL,
    duration_ms     INTEGER NOT NULL,
    cost_micros     BIGINT NOT NULL,             -- LLM cost in micro-USD
    error           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX agent_runs_user_idx ON agent_runs(user_id);
CREATE INDEX agent_runs_concept_hash_idx ON agent_runs(concept_hash);
CREATE INDEX agent_runs_created_idx ON agent_runs(created_at DESC);
```

### `workspaces`

Team workspaces for shared semantic memory (Layer 3).

```sql
CREATE TABLE workspaces (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    name            TEXT NOT NULL,
    owner_id        UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    semantic_memory JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE workspace_members (
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role            TEXT NOT NULL,                -- 'owner' | 'admin' | 'editor' | 'viewer'
    joined_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (workspace_id, user_id)
);
```

### `federation_peers`

Known federation nodes.

```sql
CREATE TABLE federation_peers (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    url             TEXT UNIQUE NOT NULL,
    pubkey          JSONB NOT NULL,
    is_trusted      BOOLEAN NOT NULL DEFAULT FALSE,
    last_seen       TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### `episodic_memory_entries`

Layer 2 memory: per-user episodic facts.

```sql
CREATE TABLE episodic_memory_entries (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    kind            TEXT NOT NULL,                -- 'preference' | 'fact' | 'pinned' | ...
    content         TEXT NOT NULL,
    embedding       vector(384),
    encrypted_data  BYTEA,                         -- encrypted with per-user key
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX episodic_user_idx ON episodic_memory_entries(user_id);
CREATE INDEX episodic_embedding_idx ON episodic_memory_entries USING hnsw (embedding vector_cosine_ops);
```

### `world_knowledge_topics`

Layer 4 memory: curated public knowledge.

```sql
CREATE TABLE world_knowledge_topics (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    slug            TEXT UNIQUE NOT NULL,
    title           TEXT NOT NULL,
    body            TEXT NOT NULL,                 -- markdown
    embedding       vector(384),
    references      JSONB NOT NULL DEFAULT '[]',   -- citations
    curator_id      UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    version         TEXT NOT NULL,
    approved_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX world_slug_idx ON world_knowledge_topics(slug);
CREATE INDEX world_embedding_idx ON world_knowledge_topics USING hnsw (embedding vector_cosine_ops);
CREATE INDEX world_body_trgm_idx ON world_knowledge_topics USING GIN(body gin_trgm_ops);
```

### `templates`

GSPL Agent template registry (see `intelligence/template-bridge.md`).

```sql
CREATE TABLE templates (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    template_id     TEXT NOT NULL,                 -- e.g., 'musician_archetype'
    version         TEXT NOT NULL,                 -- semver
    engine          TEXT NOT NULL,
    body            JSONB NOT NULL,                -- the template YAML as JSON
    author_id       UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status          TEXT NOT NULL DEFAULT 'draft', -- 'draft' | 'review' | 'approved' | 'deprecated'
    usage_count     BIGINT NOT NULL DEFAULT 0,
    avg_quality     REAL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (template_id, version)
);
```

## Row-level security examples

```sql
ALTER TABLE seeds ENABLE ROW LEVEL SECURITY;
CREATE POLICY seeds_owner_or_public ON seeds
    USING (
        author_id = current_setting('app.current_user_id', true)::uuid
        OR visibility = 'public'
        OR (visibility = 'unlisted' AND current_setting('app.current_user_id', true) IS NOT NULL)
    );

ALTER TABLE episodic_memory_entries ENABLE ROW LEVEL SECURITY;
CREATE POLICY episodic_owner_only ON episodic_memory_entries
    USING (user_id = current_setting('app.current_user_id', true)::uuid);
```

The application sets `app.current_user_id` per connection at session start; all queries are scoped automatically.

## Migration policy

- Migrations are versioned under `migrations/` and applied via `kysely-migrate` or `sqlx migrate`.
- Every migration is paired with an `up.sql` and `down.sql`.
- No migration runs without a backup first.
- Schema changes that block writes (>5s lock) are rejected by CI.

## Backup and PITR

- WAL shipped continuously to S3 (5-minute RPO).
- Daily logical pg_dump for emergency restore.
- PITR tested monthly via restore-to-staging.
