"""Deterministic diagnostic explanations.

Manifesto Section 6a: the product must accurately distinguish
deterministic DSP measurements from AI-generated content and never
mislabel one as the other. Everything in this module is template-based
string formatting over a DiagnosticResult's own fields -- no language
model is involved, and callers must never present this output to a
user as "AI-generated."
"""

from __future__ import annotations

from .diagnostic_result import DiagnosticResult

_LOW_CONFIDENCE_THRESHOLD = 0.5


def _confidence_caveat(result: DiagnosticResult) -> str:
    if result.confidence < _LOW_CONFIDENCE_THRESHOLD:
        return " (low confidence -- treat as a rough estimate)"
    return ""


def explain_bpm(result: DiagnosticResult) -> str:
    if result.value is None:
        return "Could not estimate tempo from this audio."
    return f"Estimated tempo: {result.value:.1f} BPM{_confidence_caveat(result)}."


def explain_key(result: DiagnosticResult) -> str:
    if result.value is None:
        return "Could not estimate a musical key from this audio."
    return f"Estimated key: {result.value}{_confidence_caveat(result)}."


def explain_pitch(result: DiagnosticResult) -> str:
    if result.value is None:
        return "No clear pitched (voiced) content was detected in this audio."
    return (
        f"Estimated fundamental pitch: {result.value:.1f} Hz"
        f"{_confidence_caveat(result)}."
    )
