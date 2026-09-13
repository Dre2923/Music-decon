# Voice & Language

Local offline speech recognition (Whisper) as the baseline, with an isolated provider interface so a connected-mode vendor (Deepgram) can be added later without touching calling code. See manifesto Section 4 and Section 10.11.

## Status

**Implemented and tested (without a real model download — see limitation below):**
- `transcription_result.py` — the confidence/provider/algorithm/version/timestamp result model, matching the same accuracy discipline as `backend/audio_diagnostics/diagnostic_result.py`.
- `transcription_provider.py` — the `TranscriptionProvider` abstract interface (manifesto Section 10.11: AI-vendor isolation from the start, not bolted on once a second vendor exists).
- `local_whisper.py` — `LocalWhisperProvider`, calling the real `openai-whisper` package (verified MIT for both code and model weights directly from its installed `LICENSE`/README, not assumed from the manifesto text) directly — no alternative engine (e.g. faster-whisper, not manifesto-named) substituted.
- 8 of 9 tests in `tests/` pass: resampling to Whisper's required 16kHz, the duration-weighted confidence-proxy math (Whisper itself only returns per-segment `avg_logprob`/`no_speech_prob`, not one scalar confidence), and the result model's validation.

**Known, disclosed limitation — not silently skipped:** the 9th test (real end-to-end `load_model` + `transcribe`) is marked `@pytest.mark.skip`. Running it requires downloading real Whisper model weights from `openaipublic.azureedge.net`, which this build environment's network egress policy blocks — confirmed by a direct connection attempt, and huggingface.co was also checked and blocked as a possible alternate source. **This has not been verified as actually working end-to-end.** Run the skipped test on a machine with normal internet access (a dev laptop, CI, or the target Raspberry Pi 5 itself) to confirm the real download + transcription path, then record the result in `docs/OPEN_ISSUES.md`.

**Not yet implemented:**
- Deepgram provider — deliberately not started. It has real compliance prerequisites of its own (training-data opt-out enforced on every request, 18+ account-holder requirement, must stay unreachable from under-13 profiles) that need explicit work, not a quick implementation. See manifesto Sections 4, 8a.
- Connectivity-based provider switching (local vs. connected mode).
- EN/FR/ES domain-vocabulary testing (manifesto Section 4: "Domain-specific testing must use real DJ, production, mixing, and vocal terminology... general speech benchmarks are not sufficient"). No real audio in any language has been tested against this module yet — see `docs/OPEN_ISSUES.md`.
- Model-size selection is currently hard-defaulted to `"tiny"` as an **implementation choice** (manifesto Section 14), reasoned from Pi 5 being CPU-only ARM64 where the larger multilingual models (1.5-3GB) are impractical — this has not been validated against real accuracy or latency requirements. See `docs/OPEN_ISSUES.md`.

## Setup

```
pip install -r backend/voice/requirements.txt
python3 -m pytest backend/voice/tests
```

## Key rules from the manifesto this module must honor

- Deepgram (when added) sits behind `TranscriptionProvider`, never called directly by core logic (Section 10.11).
- Deepgram training-data opt-out is set on every applicable request, at the integration layer (Section 4) — to be implemented when the Deepgram provider is built.
- Deepgram must never be reachable from an under-13 profile (Section 8a) — to be enforced when both the Deepgram provider and `backend/compliance/` exist.
- No transcript confidence is presented as certainty (`TranscriptionResult.confidence`, always in [0,1], always attributed to a named algorithm/version).
