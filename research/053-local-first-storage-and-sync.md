# 053 — Local-first storage and sync

## Question
How does GSPL store user data on disk, sync between a user's own devices, and recover from disk failures — while remaining offline-first, sovereignty-respecting, and not requiring a cloud service?

## Why it matters
A studio that loses your work is dead. A studio that requires the cloud violates GSPL's first principle. The middle path — local-first with optional self-hosted sync — is well-trodden in the database literature (Kleppmann et al.) but rarely well-executed in creator tools. GSPL has the lineage DAG, content addressing, and signed identities that make local-first sync *easier* than for typical apps. We must capitalize.

## What we know from the spec
- Brief 015: gseed binary file format.
- Brief 017: lineage DAG.
- Brief 042: identity keys.
- Brief 043: federation.
- Brief 048: studio architecture.

## Findings — five storage tiers

### Tier 1: Workspace
A workspace is a directory on disk containing one or more projects. Default: `~/Paradigm/`. User-configurable.
- **One workspace per user account on the device.**
- **Cross-device sync** is workspace-level.

### Tier 2: Project
A project is a subdirectory of the workspace. Self-contained, content-addressed, portable.
- **Project layout:**
  ```
  project_name/
    project.toml          # config: engines pinned, critic weights, etc.
    seeds/                # .gseed files, content-addressed
    lineage.db            # SQLite, the lineage DAG
    archive/              # exemplar archive (HNSW index)
    exports/              # rendered outputs
    .meta/                # signatures, version info, locks
  ```
- **Projects are zip-portable.** A `.paradigm-project` is just a zip of the directory.
- **Project hash** = Merkle root of all files. Two projects with the same hash are identical.

### Tier 3: Profile
The user's profile is global to the workspace, not per-project. Contains:
- The identity key (encrypted, Brief 042).
- The user vocabulary overrides (Brief 032).
- The preference critic weights (Brief 040).
- Federation peer list (Brief 043).
- Marketplace transaction history (Brief 044).

Stored in `~/.paradigm/profile/`.

### Tier 4: Cache
Transient data that can be regenerated. Includes:
- Rendered output cache.
- Validator results cache.
- LLM response cache.
- HNSW shadow index.

Stored in OS cache directory; can be wiped without data loss.

### Tier 5: Backups
Encrypted backups of the profile and active projects. Stored at user-chosen locations:
- Local USB drive.
- Network attached storage.
- Self-hosted cloud (Nextcloud, Syncthing).
- Commercial cloud (Dropbox, iCloud, Google Drive — opt-in).

GSPL never operates a backup service.

## Sync between user devices

Same user, multiple devices (laptop + desktop + home server). Two approaches:

### Approach 1: Filesystem sync (default)
The workspace directory is synced via a filesystem sync tool (Syncthing, rclone, Dropbox, etc.). The studio detects and handles concurrent modification:
- **Lineage entries are content-addressed and signed.** Two devices that add new entries simultaneously simply union them — no conflict.
- **Project config conflicts are rare** because config changes are themselves stored as signed lineage entries (config CRDT).
- **The cache is excluded from sync** via gitignore-style rules.
- **Lock files** prevent concurrent writes to the same lineage DB; second device shows a "wait" message.

### Approach 2: Federation sync (Brief 043)
The user runs a small home server with another studio instance and federates with it. The home server syncs incrementally over libp2p. This is the "federation as backup" pattern.

- **Pros:** lineage-aware, end-to-end encrypted, no third party, works over the internet.
- **Cons:** requires a second device with a public-ish address.

### Approach 3: Hybrid
Filesystem sync for active projects + federation sync for backups + manual export for archival.

## Conflict resolution

The lineage DAG is *append-only* and content-addressed, which makes most conflicts impossible. The remaining conflicts:
- **Concurrent operator on same parent:** both devices produce a different child. Result: both are kept; the lineage is a tree (which is fine).
- **Concurrent config edits:** last-writer-wins is unacceptable. Result: config is itself a CRDT (LWW per-field with vector clock; manual merge for collisions).
- **Concurrent identity rotation:** treated as suspected key compromise; both rotations are accepted; the user is notified.

## Backup strategy

The studio enforces a 3-2-1 backup default:
- **3 copies** (live + local backup + offsite backup).
- **2 different media** (disk + USB or disk + cloud).
- **1 offsite** (cloud or remote NAS).

Backups are:
- **Encrypted** with a backup passphrase distinct from the daily passphrase.
- **Incremental** (only changes since last backup are written).
- **Verified** on creation (hash check).
- **Tested** automatically — the studio periodically attempts a restore-to-temp to verify backup integrity.

## Disk failure recovery

When the live data is corrupted:
1. The studio detects the corruption (signature verification or DAG hash mismatch).
2. The user is shown a clear "data corruption detected" screen.
3. Recovery options: restore from latest backup, restore from federation peer (Brief 043), manual file recovery.
4. The studio refuses to silently overwrite anything during recovery.

## Risks identified

- **Filesystem sync conflicts:** Dropbox/etc. can produce ".conflict" files. Mitigation: detection and reconciliation in the studio; lineage-aware merge.
- **SQLite corruption:** rare but possible. Mitigation: WAL mode; periodic integrity checks; backup-driven restore.
- **Backup passphrase loss:** the user can't recover their backups. Mitigation: same recovery story as Brief 042 (recovery file).
- **Cache poisoning:** a corrupt cache produces wrong results. Mitigation: cache entries are content-hash-keyed; mismatched hashes are rejected.
- **Concurrent device write race:** two devices claim a lock simultaneously. Mitigation: distributed lock via the federation peer if available; otherwise file-level lock with timeout.
- **Sync tool dependency:** users without Syncthing/Dropbox/etc. have no easy sync. Mitigation: federation sync as the GSPL-native option.
- **Backup test cost:** restore-to-temp is expensive. Mitigation: weekly cadence; small projects only.

## Recommendation

1. **Adopt the five-tier storage model** in `architecture/storage.md`.
2. **Workspace > project > profile** as the canonical layout.
3. **Projects are zip-portable** content-addressed directories.
4. **Filesystem sync is the v1 default** for cross-device.
5. **Federation sync is v1.5** for cross-device over the internet.
6. **3-2-1 backup default**, enforced by the studio.
7. **Encrypted, incremental, verified backups.**
8. **Periodic backup restore tests.**
9. **No cloud service** operated by GSPL.
10. **Data corruption surfaces as a user-visible recovery flow**, never silent.
11. **Config CRDT** for concurrent device edits.

## Confidence
**4/5.** Local-first storage is mature and the GSPL substrate (content addressing, signed lineage) makes sync particularly clean. The 4/5 reflects the unmeasured complexity of cross-platform filesystem sync.

## Spec impact

- `architecture/storage.md` — full storage architecture.
- `protocols/project-format.md` — project directory layout and zip format.
- `protocols/sync-conflict-resolution.md` — conflict resolution rules.
- `protocols/backup-policy.md` — 3-2-1 default and enforcement.
- `tests/sync-conformance.md` — sync test suite.
- New ADR: `adr/00NN-local-first-storage.md`.

## Open follow-ups

- Empirical sync conflict testing with Syncthing, Dropbox, iCloud.
- Decide on the SQLite vs sled vs custom store for the lineage DB.
- Build the corruption detection + recovery flow.
- UX test the backup setup wizard.
- Investigate restic / Borg as the backup engine.

## Sources

- Kleppmann et al., *Local-first software: You own your data, in spite of the cloud*.
- SQLite documentation on WAL mode and corruption.
- Syncthing protocol documentation.
- Restic backup architecture.
- Internal: Briefs 015, 017, 042, 043, 044, 048.
