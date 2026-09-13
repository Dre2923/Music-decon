# Voice & Language

Local offline speech recognition (Whisper) as the baseline, with an isolated Deepgram provider for connected-mode transcription, provider switching by connectivity, and EN/FR/ES domain-vocabulary support. See manifesto Section 4 and Section 10.11.

**Status:** not yet implemented.

Key rules from the manifesto this module must honor:
- Deepgram sits behind an internal provider interface (Section 10.11) — core logic must never be structurally dependent on it.
- Every applicable Deepgram request sets the training-data opt-out; this is enforced at the integration layer, not left as a dashboard setting.
- Deepgram is never reachable from an under-13 profile (see `backend/compliance/`), regardless of family-subscription status.
- Domain testing (DJ/production/mixing/vocal terminology) is required in all three launch languages — general speech benchmarks are not sufficient evidence.
