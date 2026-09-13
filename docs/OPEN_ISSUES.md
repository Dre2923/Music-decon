# Open Issues Register

Per `MANIFESTO.md` Section 14, every unresolved item in the manifesto must be tracked here as an **OPEN ISSUE** rather than silently resolved by assumption. Nothing in this file may be converted to a completed design decision without explicit sign-off from the product owner, logged with a date and decision below.

Do not delete a row when work starts on it — move it to "Resolved" with the decision and date once sign-off is recorded.

## Blocking — must be resolved before related code ships

| # | Issue | Manifesto ref | Why it's open | Blocks |
|---|---|---|---|---|
| 1 | Exact retention period (in days) for child-profile personal data | 8a | Manifesto explicitly forbids inventing a number without sign-off | Any code that expires/purges under-13 profile data |
| 2 | Verifiable-parental-consent method for a future Deepgram child-data disclosure | 8a | Six preconditions listed, none yet satisfied | Enabling Deepgram for any under-13 profile (must stay disabled otherwise) |
| 3 | Final exact `ConsentState` enum values/transitions | 8a | "May change during implementation" but must be decided deliberately, not improvised mid-build | Data-access-layer consent enforcement |
| 4 | Spleeter pretrained-weight commercial redistribution/use rights | 6 | Licensing questions were still open upstream as of 2026; release gate | Shipping any Spleeter model weights |
| 5 | Open-Unmix non-`umxl` model artifact licenses | 6 | Requires individual artifact-level verification; `umxl` itself is confirmed CC BY-NC-SA 4.0 and is already excluded | Packaging any Open-Unmix pretrained model besides an already-cleared one |
| 6 | PyDMX vs. DmxPy final selection | 5 | Manifesto says license/hardware support must be reconfirmed "at integration time" | Building the DMX output abstraction against a concrete library |
| 7 | Windows/Microsoft Store certification lead time for this app's package type | 6a | Not quantified in the manifesto; affects release scheduling | Windows release-date planning |
| 8 | Vendored `bpm-detector`'s real dependency footprint (scikit-learn, matplotlib, seaborn, pandas, psutil pulled in by its own `__init__.py`) has not been runtime-benchmarked on physical Raspberry Pi 5 hardware | 3, 10.12 | **Partially checked 2026-09-13:** every one of the 14 runtime dependencies (librosa, numpy, scipy, soundfile, audioread, tqdm, colorama, scikit-learn, matplotlib, seaborn, pandas, psutil, resampy, sounddevice) has an official prebuilt `manylinux*_aarch64` wheel on PyPI, confirmed by actually downloading each with `pip download --platform manylinux2014_aarch64 --python-version 311 --abi cp311` from this session — so they install on 64-bit Raspberry Pi OS without compiling C/Fortran extensions on-device. Combined wheel download size is ~81 MB. **Still open:** this confirms ARM64 *installability*, not runtime performance — actual import time, BPM/key detection latency, and memory usage under load on physical Pi 5 hardware have not been measured, because this session has no physical Pi to measure them on. Do not treat this module as performance-verified for the Pi 5 backend until that measurement exists, per the same principle the manifesto already applies to loqa-voice-dsp in Section 4a (Apple M-series benchmarks are not a Pi guarantee; here, x86_64 wheel-availability checks are not a Pi runtime-performance guarantee either). **⚠️ NOTE FOR THE PRODUCT OWNER (you have a physical Raspberry Pi 5 to check this on):** run `python3 backend/audio_diagnostics/benchmark_pi.py` on the actual device and record the result in `docs/PI_BENCHMARKS.md`, then mark this row resolved here. Nobody else can close this one — it needs the real hardware. | Treating `backend/audio_diagnostics/bpm_key_pitch.py` BPM/key detection as performance-verified (not just installable) on the Pi 5 backend |
| 9 | `backend/voice/local_whisper.py`'s real end-to-end path (`whisper.load_model` + `transcribe`) has never actually run — model-weight download is blocked in this build environment | 4, 12 | **Checked 2026-09-13:** `openaipublic.azureedge.net` (Whisper's own model host) and `huggingface.co` (checked as a possible alternate source) are both blocked by this session's network egress policy, confirmed by direct connection attempts (403 from the egress proxy). Everything in the module that doesn't require the actual model weights is tested (resampling, the confidence-proxy math, the result model); the real download + transcribe call is a `@pytest.mark.skip`'d test in `backend/voice/tests/test_local_whisper.py`, not silently omitted. **⚠️ NOTE FOR THE PRODUCT OWNER:** on your Raspberry Pi 5 (or any machine with normal internet access), run `pip install -r backend/voice/requirements.txt` then un-skip and run `test_transcribe_real_speech_end_to_end` in that file against a real short speech clip, to confirm the download and transcription actually work before relying on this module | Treating local Whisper transcription as working, not just unit-tested around the edges |
| 10 | EN/FR/ES domain-vocabulary testing for Whisper (manifesto Section 4: "real DJ, production, mixing, and vocal terminology... general speech benchmarks are not sufficient") has not been done | 4, 12 | No real audio in any language has been run through this module yet (see #9 — the model itself hasn't even been downloaded in this session) | Claiming the voice module understands music-domain vocabulary in any of the three launch languages |
| 11 | Default Whisper model size (`"tiny"`, set in `backend/voice/local_whisper.py`) is an unvalidated implementation choice | 4, 14 | Chosen only by reasoning that Pi 5 is CPU-only ARM64 and larger models (1.5-3GB) are impractical there — not validated against real transcription accuracy or real latency. A larger model (`base`/`small`) might still be viable and more accurate; only benchmarking on the real device (once #9 is unblocked) can settle this | Treating `tiny` as a final, validated choice rather than a placeholder default |
| 12 | `faster-whisper` (CTranslate2-based) was not used despite being a commonly recommended CPU-optimized alternative for devices like the Pi | 4 | It is not named in the manifesto ("Baseline engine: OpenAI Whisper"), so per the no-substitution rule this project now follows, it was not silently swapped in. If real Pi 5 benchmarking (once #9/#11 are resolved) shows `openai-whisper` is too slow to be usable, this is a candidate **PROPOSED CHANGE** to bring to the product owner explicitly — not something to switch to unilaterally | Any future decision to change the manifesto's named speech-recognition engine |

## Deferred by design (not blocking, but not in scope without a deliberate decision to un-defer)

| # | Item | Manifesto ref | Note |
|---|---|---|---|
| D1 | Teacher/coach dashboard | 8 | Explicitly deferred; must not be built by quietly reusing family-profile permissions |

## Shortcuts taken, pending authorization

Per manifesto Section 0: a shortcut must be identified explicitly, its risks explained, and the full-standard alternative presented — it may not silently replace the approved design.

_(none currently outstanding — S1 below was resolved, not authorized as-is)_

## Standing mechanism (not a single item — ongoing)

| # | Item | Manifesto ref | Cadence |
|---|---|---|---|
| M1 | Re-verify Apple/Google/Microsoft/FTC/OWASP/NIST/WCAG sources and all dependency licenses | 10.2, 13, 16 | Before every major milestone, beta, and production submission — see `DEPENDENCY_REGISTER.md` and `COMPLIANCE_LOG.md` |

## Resolved

| # | Item | Resolution | Date |
|---|---|---|---|
| S1 | `bpm_key_pitch.py` used `librosa.beat.beat_track` directly + a self-written key-correlation function instead of the named `bpm-detector` package | User explicitly rejected the shortcut. The real `libraz/bpm-detector` (MIT) was found, reviewed, pinned at commit `9e82ed544edd7f06a5459b8fa8fe539f20335df8`, and vendored into `backend/audio_diagnostics/vendor/bpm-detector/`. `bpm_key_pitch.py` now calls its real `BPMDetector`/`KeyDetector` classes. See `DEPENDENCY_REGISTER.md` "Resolved: bpm-detector shortcut" | 2026-09-13 |

---

If the earlier 32-section voice-session draft mentioned in the manifesto's preamble is ever recovered, diff it against `MANIFESTO.md` and add any genuinely missing requirement as a new row here first — do not merge it directly into the manifesto without deliberate reconciliation.
