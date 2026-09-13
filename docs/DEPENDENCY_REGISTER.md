# Dependency & License Register

Required by `MANIFESTO.md` Section 10.1 and Section 13. Every third-party component used by the build must have a row here. Code license and model/weight license are tracked separately — they are never assumed identical.

**"Date checked" below reflects the manifesto's own Section 17 research baseline (2026-09-12), carried over from the manifesto text, not an independent re-verification performed while writing this register.** Per Section 10.2 / 16, each row must be independently re-checked against the current primary source (repo license file, model card, vendor terms page) before it is relied on for a release milestone, and this table updated with the new date and any change. Source links are intentionally left as "confirm from primary source" rather than guessed — do not fill them in from memory.

| Component | Role | Code license | Model/weight license | Dataset license | Commercial use | Redistribution | Attribution required | Date checked | Source |
|---|---|---|---|---|---|---|---|---|---|
| librosa | BPM / key / pitch analysis | ISC (permissive) | N/A | N/A | Yes | Yes | Per ISC notice | 2026-09-12 (manifesto baseline) | confirm from primary source |
| bpm-detector | BPM detection (wraps librosa) — **not currently vendored; see deviation note below** | MIT | N/A | N/A | Yes | Yes | Per MIT notice | 2026-09-12 (manifesto baseline) | confirm from primary source |
| OpenAI Whisper | Local/offline speech recognition | MIT | MIT (as of manifesto baseline — reconfirm before release) | Not redistributed | Yes | Yes | Per MIT notice | 2026-09-12 (manifesto baseline) | confirm from primary source |
| Deepgram (API/SDK) | Connected-mode cloud transcription | N/A (hosted API) | N/A | N/A | Yes, per current Terms (checked against the Aug 6, 2026 revision per manifesto) — **must reconfirm before each release**; training-data opt-out must be set on every request | N/A (API, not redistributed) | Per Deepgram Terms | 2026-09-12 (manifesto baseline; underlying terms dated Aug 6, 2026) | confirm from primary source |
| loqa-voice-dsp | Deep vocal/pitch DSP (YIN/pYIN, formants, HNR, H1-H2) | MIT | N/A (DSP, not a trained model) | N/A | Yes | Yes | Per MIT notice | 2026-09-12 (manifesto baseline) | confirm from primary source |
| DmxPy / PyDMX (final choice open — see OPEN_ISSUES.md #6) | DMX512 output over Enttec/DMXKing USB hardware | Confirm at integration time | N/A | N/A | Confirm at integration time | Confirm at integration time | Confirm at integration time | Not yet checked | confirm from primary source |
| Open Fixture Library | Lighting fixture definitions | MIT | N/A | MIT | Yes | Yes | Per MIT notice | 2026-09-12 (manifesto baseline) | confirm from primary source |
| Spleeter (code) | Source separation (candidate) | MIT | **BLOCKED — see OPEN_ISSUES.md #4. Do not ship pretrained weights until documented here with confirmed commercial redistribution rights.** | Not yet documented | Code: yes. Weights: blocked | Code: yes. Weights: blocked | Per MIT notice (code) | 2026-09-12 (manifesto baseline) | confirm from primary source |
| Open-Unmix (code) | Source separation (candidate) | MIT | `umxl`: CC BY-NC-SA 4.0 — **non-commercial, must never ship in the commercial product**. Other models: unverified, see OPEN_ISSUES.md #5 | Not yet documented | Code: yes. `umxl` weights: no. Other weights: unverified | Code: yes. `umxl`: no. Other weights: unverified | Per MIT notice (code) | 2026-09-12 (manifesto baseline) | confirm from primary source |
| Demucs (code) | Source separation (candidate) | MIT | Not yet documented | Not yet documented | Confirm; also confirm maintenance status — original repo archived by Meta Jan 2025 | Confirm | Per MIT notice (code) | 2026-09-12 (manifesto baseline) | confirm from primary source |

## Deviation notice — `backend/audio_diagnostics/bpm_key_pitch.py`

**Shortcut taken:** the initial BPM implementation calls `librosa.beat.beat_track` directly instead of depending on the `bpm-detector` package the manifesto names (Section 3: "librosa + bpm-detector").

**Why:** `bpm-detector` is not resolvable as an installable PyPI package under that name in this build environment (`pip index versions bpm-detector` and `pip download` both fail with no matching distribution). Per the manifesto's own description, `bpm-detector` is a thin MIT-licensed wrapper that "uses librosa internally" — calling `librosa.beat.beat_track` directly reaches the same underlying algorithm without introducing an unresolvable dependency.

**Risk/disadvantage:** if the actual upstream `bpm-detector` project (correct package name/source not yet confirmed) adds behavior beyond a thin wrapper — e.g. its own confidence scoring, smoothing, or edge-case handling — this implementation does not benefit from that and instead uses a locally-defined confidence proxy (documented in the code) that is not the same as the analyzer's own probability.

**Full-standard alternative:** locate the exact upstream `bpm-detector` repository referenced by the manifesto, confirm its real package/import name and license, vendor or depend on it directly, and replace the direct `librosa.beat.beat_track` call with it.

**Status:** shortcut in place, not yet authorized as a permanent design change. Needs explicit sign-off before being treated as final, or replacement with the full-standard alternative.

## Process

1. Before adding a new third-party component to the codebase, add a row here first.
2. Before any milestone listed in Section 10.2 of the manifesto (beta, TestFlight, Play internal testing, Windows certification, production submission, vendor replacement), re-check every row's primary source and update "Date checked."
3. A blocked cell (weights, redistribution, etc.) is a release gate per manifesto Section 6/10.14 — code depending on a blocked artifact must not ship until the row is unblocked with a recorded source and date.
