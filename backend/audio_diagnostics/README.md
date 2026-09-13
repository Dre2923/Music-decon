# Audio Diagnostics

Chunked audio capture, BPM/key/pitch analysis (librosa + the real vendored `bpm-detector`), vocal DSP (loqa-voice-dsp: pitch contour, formants, HNR, H1-H2, vibrato), and diagnostic-explanation generation. See manifesto Sections 3 and 4a.

## Status

**Implemented and tested:** chunked capture (`audio_capture.py`), BPM/key/pitch analysis (`bpm_key_pitch.py`), the confidence-carrying result model (`diagnostic_result.py`), and deterministic (non-AI) explanation text (`explanation.py`). 15 tests in `tests/` pass against synthetic signals with a known ground truth (a 440 Hz tone, a 120 BPM click track, a C major triad) — see the test files for the exact tolerances used and why.

BPM and key detection call the actual `bpm-detector` library the manifesto names (Section 3), vendored verbatim at a pinned, reviewed commit in `vendor/bpm-detector/` — see that directory's `NOTICE.md` for the exact source commit, license text, and why it's vendored rather than fetched live. An earlier version of this module substituted a hand-rolled implementation instead of the real library without authorization; that was rejected and replaced — see `docs/DEPENDENCY_REGISTER.md` ("Resolved: bpm-detector shortcut") and `docs/OPEN_ISSUES.md` (S1, resolved).

**Not yet implemented:**
- Vocal DSP integration (loqa-voice-dsp: formants, HNR, H1-H2) and vibrato derivation — manifesto Section 4a.
- Source-separation / content-minimization — blocked on the open model-weight licensing items in `docs/OPEN_ISSUES.md` (#4, #5).
- `MicrophoneAudioCapture` in `audio_capture.py` is written against the `sounddevice` API but has **not been exercised against real hardware** (this environment has no audio input device). Per manifesto Section 12, treat it as unverified until a real capture test has run on target hardware (including the Raspberry Pi 5 backend) and that result is recorded as pre-release evidence.
- No reference test clips from real recordings exist yet (manifesto Section 12) — only synthetic signals with a known ground truth are covered so far. Reference-clip accuracy testing is still open.
- The vendored `bpm-detector` package's real dependency footprint (it pulls in scikit-learn, matplotlib, seaborn, pandas, psutil via its own `__init__.py`) has not been benchmarked on Raspberry Pi 5 — see `docs/OPEN_ISSUES.md` #8.

## Setup

```
pip install -r backend/audio_diagnostics/requirements.txt
pip install -e backend/audio_diagnostics/vendor/bpm-detector
python3 -m pytest backend/audio_diagnostics/tests
```

## Key rules from the manifesto this module must honor

- Analyze completed buffers/chunks; librosa is not an always-open streaming engine (`ChunkedAudioCapture.capture_chunk` returns one finite chunk per call).
- Every diagnostic result carries confidence, source algorithm/version, and time analyzed — never presented as bare certainty (`DiagnosticResult`).
- Acoustic measurements are described as measurements ("increased breathiness measurement," "unstable pitch"), never as medical diagnoses — enforced by convention in `explanation.py` and checked by `test_explanations_never_use_medical_language`.
- Explanation text is deterministic template output, not AI-generated, and must never be presented to a user as if it were (manifesto Section 6a AI-content labeling rule).
- Any Rust/FFI path for vocal DSP must be benchmarked on real Raspberry Pi 5 hardware before being trusted — the upstream loqa-voice-dsp benchmarks are Apple M-series only.
