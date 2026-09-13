# Data & Sync

Local-first schema (including per-profile consent-status field), safe database-write layer, offline operation queue, and reconnect synchronization. See manifesto Section 2 and 6b.

**Status:** not yet implemented.

Key rules from the manifesto this module must honor:
- The local data layer must support core product operation with no network present.
- Sync must handle: offline mutation, reconnect, server temporarily unreachable, duplicate transmission, partial completion, multi-device conflict, stale client, app termination mid-sync (Section 10.8) — all with tests, not just handling code.
- Every mutation is validated, has error handling, and is idempotent for repeatable network operations, with particular care for payment/credit/consent/sync mutations (Section 10.6).
- Sensitive local data remains encrypted/secured even while offline — offline-first does not relax OWASP MASVS secure-storage requirements.
