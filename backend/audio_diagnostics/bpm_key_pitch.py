"""BPM, key, and pitch analysis over a completed audio chunk.

Manifesto Section 3: "Chosen: librosa (ISC License, permissive) +
bpm-detector (MIT, uses librosa internally)". BPM and key detection
call the actual vendored bpm-detector library (see
backend/audio_diagnostics/vendor/bpm-detector/NOTICE.md for its exact
pinned commit and license) rather than a hand-rolled substitute -- an
earlier version of this file used librosa's beat tracker and a
self-written Krumhansl-Kessler key correlation directly; that was an
undisclosed deviation from the manifesto's named dependency and has
been replaced with the real library.

Pitch estimation uses librosa's own pYIN directly, which is not a
substitution: librosa itself is a manifesto-named dependency and pYIN
is one of its first-class functions, not an invented algorithm.

Capture and analysis remain separate concerns (see audio_capture.py):
every function here analyzes one already-captured chunk. Every
function returns a DiagnosticResult carrying the analyzer's own
confidence; nothing here presents a bare number as certainty.
"""

from __future__ import annotations

import librosa
import numpy as np
from bpm_detector.key_detector import KeyDetector as _VendoredKeyDetector
from bpm_detector.music_analyzer import BPMDetector as _VendoredBPMDetector

from .audio_capture import AudioChunk
from .diagnostic_result import DiagnosticResult

_LIBROSA_VERSION = librosa.__version__

try:
    import bpm_detector as _bpm_detector_pkg

    _BPM_DETECTOR_VERSION = _bpm_detector_pkg.__version__
except ImportError:  # pragma: no cover - import above already requires it
    _BPM_DETECTOR_VERSION = "unknown"


def _input_characteristics(chunk: AudioChunk) -> dict:
    return {
        "sample_rate": chunk.sample_rate,
        "duration_seconds": chunk.duration_seconds,
        "n_samples": len(chunk.samples),
    }


def analyze_bpm(chunk: AudioChunk) -> DiagnosticResult:
    """Estimate tempo (BPM) via the vendored bpm-detector library."""
    detector = _VendoredBPMDetector(sr=chunk.sample_rate)
    tempo_value, confidence_0_100, _top_bpms, _top_hits = detector.detect(
        chunk.samples, chunk.sample_rate
    )

    return DiagnosticResult(
        value=float(tempo_value),
        confidence=float(np.clip(confidence_0_100 / 100.0, 0.0, 1.0)),
        algorithm="bpm_detector.music_analyzer.BPMDetector.detect",
        algorithm_version=_BPM_DETECTOR_VERSION,
        analyzed_at=DiagnosticResult.now(),
        input_characteristics=_input_characteristics(chunk),
    )


def analyze_key(chunk: AudioChunk) -> DiagnosticResult:
    """Estimate musical key via the vendored bpm-detector library."""
    detector = _VendoredKeyDetector()
    key_label, confidence_0_100 = detector.detect(chunk.samples, chunk.sample_rate)

    return DiagnosticResult(
        value=key_label,
        confidence=float(np.clip(confidence_0_100 / 100.0, 0.0, 1.0)),
        algorithm="bpm_detector.key_detector.KeyDetector.detect",
        algorithm_version=_BPM_DETECTOR_VERSION,
        analyzed_at=DiagnosticResult.now(),
        input_characteristics=_input_characteristics(chunk),
    )


def analyze_pitch(chunk: AudioChunk) -> DiagnosticResult:
    """Estimate fundamental frequency via librosa's probabilistic YIN (pYIN)."""
    f0, voiced_flag, voiced_prob = librosa.pyin(
        chunk.samples,
        sr=chunk.sample_rate,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7"),
    )

    voiced_f0 = f0[voiced_flag]
    voiced_confidence = voiced_prob[voiced_flag]

    if voiced_f0.size == 0:
        return DiagnosticResult(
            value=None,
            confidence=0.0,
            algorithm="librosa.pyin",
            algorithm_version=_LIBROSA_VERSION,
            analyzed_at=DiagnosticResult.now(),
            input_characteristics=_input_characteristics(chunk),
        )

    return DiagnosticResult(
        value=float(np.median(voiced_f0)),
        confidence=float(np.mean(voiced_confidence)),
        algorithm="librosa.pyin",
        algorithm_version=_LIBROSA_VERSION,
        analyzed_at=DiagnosticResult.now(),
        input_characteristics=_input_characteristics(chunk),
    )
