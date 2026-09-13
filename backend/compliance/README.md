# Compliance — Family Profiles, Age Screen, Consent, Deletion

Family profile service, neutral age screen, under-13 locked-down-mode enforcement at the data-access layer, parental consent verification, third-party AI consent, privacy/data-lifecycle enforcement, and account-deletion propagation. See manifesto Sections 6a, 6b, 8, 8a, 10.10.

**Status:** not yet implemented. This module has the most open items in the manifesto — see `docs/OPEN_ISSUES.md` #1, #2, #3 — and per the manifesto's own Instructions, none of those may be filled in by assumption. Do not write enforcement code that depends on a specific retention period or a finalized consent-state enum until those are resolved.

Key rules from the manifesto this module must honor:
- The age screen is neutral: no preselected adult age, no hints for bypassing restrictions, no encouragement to misstate age.
- Under-13 profiles get local-processing-only mode: no Deepgram, no unnecessary third-party analytics, no ad profiling, no unrestricted cloud sync — enforced at the backend/data-access layer, not just hidden UI.
- Deepgram stays disabled for under-13 profiles until all six preconditions in manifesto Section 8a are met and explicitly approved and recorded.
- Email-plus consent may authorize internal-only use of a child's data; it is never sufficient by itself to authorize sending a child's audio to a third party like Deepgram.
- Account/profile deletion propagates to local DB, backend DB, object/audio storage, sync queue, analytics identifiers, third-party processors, and backups per documented retention policy — and is initiable from inside the app (Apple) plus has an external web path (Google).
- Teacher/coach dashboard (manifesto Section 8) is explicitly out of scope here — do not implement it by reusing family-profile permissions.
