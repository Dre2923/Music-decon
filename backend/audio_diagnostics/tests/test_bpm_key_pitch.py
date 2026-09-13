from __future__ import annotations

import pytest

from backend.audio_diagnostics.bpm_key_pitch import analyze_bpm, analyze_key, analyze_pitch


def test_analyze_pitch_detects_known_frequency(sine_440hz_chunk):
    result = analyze_pitch(sine_440hz_chunk)

    assert result.value == pytest.approx(440.0, abs=2.0)
    assert result.confidence > 0.9
    assert result.algorithm == "librosa.pyin"
    assert result.input_characteristics["sample_rate"] == sine_440hz_chunk.sample_rate


def test_analyze_pitch_on_silence_reports_no_pitch(silence_chunk):
    result = analyze_pitch(silence_chunk)

    assert result.value is None
    assert result.confidence == 0.0


def test_analyze_bpm_detects_known_tempo(click_track_120bpm_chunk):
    result = analyze_bpm(click_track_120bpm_chunk)

    # librosa's beat tracker snaps to its own tempo grid, so this is a
    # tolerance band around the true 120 BPM rather than an exact match.
    assert 100.0 <= result.value <= 140.0
    assert result.confidence > 0.5


def test_analyze_key_detects_known_triad(c_major_chord_chunk):
    result = analyze_key(c_major_chord_chunk)

    assert result.value == "C major"
    assert result.confidence > 0.5


def test_diagnostic_result_carries_confidence_and_provenance(sine_440hz_chunk):
    result = analyze_pitch(sine_440hz_chunk)

    assert 0.0 <= result.confidence <= 1.0
    assert result.algorithm
    assert result.algorithm_version
    assert result.analyzed_at is not None
