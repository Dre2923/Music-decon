# Audio Diagnostics

Chunked audio capture, BPM/key/pitch analysis (librosa), vocal DSP (loqa-voice-dsp: pitch contour, formants, HNR, H1-H2, vibrato), and diagnostic-explanation generation. See manifesto Sections 3 and 4a.

## Status

**Implemented and tested:** chunked capture (`audio_capture.py`), BPM/key/pitch analysis (`bpm_key_pitch.py`), the confidence-carrying result model (`diagnostic_result.py`), and deterministic (non-AI) explanation text (`explanation.py`). 15 tests in `tests/` pass against synthetic signals with a known ground truth (a 440 Hz tone, a 120 BPM click track, a C major triad) — see the test files for the exact tolerances used and why.

**Not yet implemented:**
- Vocal DSP integration (loqa-voice-dsp: formants, HNR, H1-H2) and vibrato derivation — manifesto Section 4a.
- Source-separation / content-minimization — blocked on the open model-weight licensing items in `docs/OPEN_ISSUES.md` (#4, #5).
- `MicrophoneAudioCapture` in `audio_capture.py` is written against the `sounddevice` API but has **not been exercised against real hardware** (this environment has no audio input device). Per manifesto Section 12, treat it as unverified until a real capture test has run on target hardware (including the Raspberry Pi 5 backend) and that result is recorded as pre-release evidence.
- No reference test clips from real recordings exist yet (manifesto Section 12) — only synthetic signals with a known ground truth are covered so far. Reference-clip accuracy testing is still open.

## Setup

```
pip install -r backend/audio_diagnostics/requirements.txt
python3 -m pytest backend/audio_diagnostics/tests
```

## Key rules from the manifesto this module must honor

- Analyze completed buffers/chunks; librosa is not an always-open streaming engine (`ChunkedAudioCapture.capture_chunk` returns one finite chunk per call).
- Every diagnostic result carries confidence, source algorithm/version, and time analyzed — never presented as bare certainty (`DiagnosticResult`).
- Acoustic measurements are described as measurements ("increased breathiness measurement," "unstable pitch"), never as medical diagnoses — enforced by convention in `explanation.py` and checked by `test_explanations_never_use_medical_language`.
- Explanation text is deterministic template output, not AI-generated, and must never be presented to a user as if it were (manifesto Section 6a AI-content labeling rule).
- Any Rust/FFI path for vocal DSP must be benchmarked on real Raspberry Pi 5 hardware before being trusted — the upstream loqa-voice-dsp benchmarks are Apple M-series only.
