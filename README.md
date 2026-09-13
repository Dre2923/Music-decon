# Voice-First Music Intelligence Ecosystem

A voice-first app that listens to a musician working — DJing, singing, producing, playing an instrument, mixing live sound, or operating stage lighting — and gives real diagnostic feedback, explanation, guidance, and structured practice, grounded in actual audio measurement rather than generic conversation.

## Governing documents

- **[`docs/MANIFESTO.md`](docs/MANIFESTO.md)** — the master product and engineering manifesto. This is the authoritative source for vision, architecture, licensing decisions, compliance requirements, monetization, privacy, security, accessibility, and release rules. Every implementation decision must trace back to it.
- **[`docs/OPEN_ISSUES.md`](docs/OPEN_ISSUES.md)** — items the manifesto explicitly leaves open (placeholders, decisions pending sign-off). Nothing here may be silently resolved by assumption.
- **[`docs/DEPENDENCY_REGISTER.md`](docs/DEPENDENCY_REGISTER.md)** — license/attribution/redistribution record for every third-party component, per manifesto Section 10.1/13.
- **[`docs/COMPLIANCE_LOG.md`](docs/COMPLIANCE_LOG.md)** — the five-pass verification log required for every security/privacy/child-safety/billing/licensing feature (manifesto Instructions, item 1).

## Status

This repository currently holds the locked governing manifesto and the tracking scaffolding it requires (dependency register, open-issues register, compliance log) plus placeholder module directories reflecting the manifesto's Section 11 build-sequence categories. No product code has been written yet.

The manifesto's own rules (no assumption-filling on open items, no silent scope reduction, compliance gates are blocking not advisory) mean implementation proceeds deliberately, module by module, with the open items in `docs/OPEN_ISSUES.md` resolved by explicit sign-off before the code that depends on them ships.

## Repository layout

```
docs/                   governing documents (see above)
backend/
  audio_diagnostics/    BPM/key/pitch/vocal-DSP analysis (manifesto Sections 3, 4a)
  voice/                local Whisper + Deepgram provider, EN/FR/ES (manifesto Section 4)
  lighting/             DMX output abstraction + fixture loading (manifesto Section 5)
  content_protection/   source-separation / copyright data-minimization (manifesto Section 6)
  data_sync/            local schema, offline queue, reconnect sync (manifesto Section 2, 6b)
  monetization/         credit ledger, reverse trial, store billing (manifesto Section 7)
  compliance/           family profiles, age-screen, consent enforcement, deletion propagation (manifesto Sections 8, 8a, 6b, 10.10)
  core_loop/            LISTEN→DIAGNOSE→EXPLAIN→SHOW→PRACTICE→VERIFY→SAVE orchestrator (manifesto Section 1)
clients/
  ios/
  android/
  windows/
```

Each module directory contains a short README describing its scope and current status until real implementation begins.
