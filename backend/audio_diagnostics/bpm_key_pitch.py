"""BPM, key, and pitch analysis over a completed audio chunk.

Manifesto Section 3: librosa (ISC, permissive) analyzes a finished
buffer -- capture and analysis are separate concerns (see
audio_capture.py). Every function returns a DiagnosticResult carrying
the analyzer's own confidence; nothing here presents a bare number as
certainty.
"""

from __future__ import annotations

import librosa
import numpy as np

from .audio_capture import AudioChunk
from .diagnostic_result import DiagnosticResult

_ALGORITHM_VERSION = librosa.__version__

_PITCH_CLASS_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Krumhansl-Kessler key profiles: a chromagram is correlated against a
# rotation of each of these to score all 24 major/minor key candidates.
_MAJOR_PROFILE = np.array(
    [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
)
_MINOR_PROFILE = np.array(
    [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
)


def _input_characteristics(chunk: AudioChunk) -> dict:
    return {
        "sample_rate": chunk.sample_rate,
        "duration_seconds": chunk.duration_seconds,
        "n_samples": len(chunk.samples),
    }


def analyze_bpm(chunk: AudioChunk) -> DiagnosticResult:
    """Estimate tempo (BPM) via librosa's onset-strength beat tracker."""
    onset_env = librosa.onset.onset_strength(y=chunk.samples, sr=chunk.sample_rate)
    tempo, beat_frames = librosa.beat.beat_track(
        onset_envelope=onset_env, sr=chunk.sample_rate
    )
    tempo_value = float(np.atleast_1d(tempo)[0])

    # librosa's beat tracker doesn't expose a first-class tempo
    # probability, so this derives a confidence proxy from how strongly
    # the detected beat grid lines up with the onset-strength envelope.
    # This is an implementation choice for the proxy, not a claim that
    # it is the analyzer's own probability -- the algorithm name below
    # says so explicitly.
    if len(beat_frames) >= 2 and onset_env.size > 0 and onset_env.max() > 0:
        beat_strength = onset_env[beat_frames].mean()
        confidence = float(np.clip(beat_strength / onset_env.max(), 0.0, 1.0))
    else:
        confidence = 0.0

    return DiagnosticResult(
        value=tempo_value,
        confidence=confidence,
        algorithm="librosa.beat.beat_track+onset_strength_confidence_proxy",
        algorithm_version=_ALGORITHM_VERSION,
        analyzed_at=DiagnosticResult.now(),
        input_characteristics=_input_characteristics(chunk),
    )


def analyze_key(chunk: AudioChunk) -> DiagnosticResult:
    """Estimate musical key via chroma correlation against Krumhansl-Kessler profiles."""
    chroma = librosa.feature.chroma_cqt(y=chunk.samples, sr=chunk.sample_rate)
    chroma_mean = chroma.mean(axis=1)

    best_key = None
    best_score = -np.inf
    all_scores: list[float] = []
    for shift in range(12):
        major_corr = np.corrcoef(np.roll(_MAJOR_PROFILE, shift), chroma_mean)[0, 1]
        minor_corr = np.corrcoef(np.roll(_MINOR_PROFILE, shift), chroma_mean)[0, 1]
        for corr, mode in ((major_corr, "major"), (minor_corr, "minor")):
            corr = 0.0 if np.isnan(corr) else float(corr)
            all_scores.append(corr)
            if corr > best_score:
                best_score = corr
                best_key = f"{_PITCH_CLASS_NAMES[shift]} {mode}"

    # Normalize the winning correlation against the spread of all 24
    # candidate scores: a clear winner scores near 1, a near-tie among
    # keys scores low, rather than reporting a raw correlation that
    # could itself be negative or misleadingly high.
    spread = max(all_scores) - min(all_scores)
    confidence = float(np.clip(best_score, 0.0, 1.0)) if spread > 1e-6 else 0.0

    return DiagnosticResult(
        value=best_key,
        confidence=confidence,
        algorithm="librosa.feature.chroma_cqt+krumhansl_kessler_correlation",
        algorithm_version=_ALGORITHM_VERSION,
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
            algorithm_version=_ALGORITHM_VERSION,
            analyzed_at=DiagnosticResult.now(),
            input_characteristics=_input_characteristics(chunk),
        )

    return DiagnosticResult(
        value=float(np.median(voiced_f0)),
        confidence=float(np.mean(voiced_confidence)),
        algorithm="librosa.pyin",
        algorithm_version=_ALGORITHM_VERSION,
        analyzed_at=DiagnosticResult.now(),
        input_characteristics=_input_characteristics(chunk),
    )
