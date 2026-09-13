from __future__ import annotations

from backend.audio_diagnostics.diagnostic_result import DiagnosticResult
from backend.audio_diagnostics.explanation import explain_bpm, explain_key, explain_pitch


def _result(value, confidence):
    return DiagnosticResult(
        value=value,
        confidence=confidence,
        algorithm="test",
        algorithm_version="0",
        analyzed_at=DiagnosticResult.now(),
        input_characteristics={},
    )


def test_explain_bpm_high_confidence_has_no_caveat():
    text = explain_bpm(_result(128.0, 0.9))
    assert "128.0 BPM" in text
    assert "low confidence" not in text


def test_explain_bpm_low_confidence_adds_caveat():
    text = explain_bpm(_result(128.0, 0.2))
    assert "low confidence" in text


def test_explain_bpm_none_value():
    assert "Could not estimate tempo" in explain_bpm(_result(None, 0.0))


def test_explain_key_reports_value():
    text = explain_key(_result("C major", 0.8))
    assert "C major" in text


def test_explain_pitch_reports_hz():
    text = explain_pitch(_result(440.0, 0.95))
    assert "440.0 Hz" in text


def test_explanations_never_use_medical_language():
    # Manifesto Section 4a: acoustic measurements are described as
    # measurements, never as medical diagnoses.
    banned_terms = ["disease", "disorder", "pathology", "diagnosis of"]
    texts = [
        explain_bpm(_result(120.0, 0.9)),
        explain_key(_result("A minor", 0.7)),
        explain_pitch(_result(220.0, 0.6)),
    ]
    for text in texts:
        for term in banned_terms:
            assert term not in text.lower()
