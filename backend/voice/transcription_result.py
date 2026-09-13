"""Transcription result data model.

Mirrors the same accuracy discipline as
backend/audio_diagnostics/diagnostic_result.py (manifesto Section 3):
no transcript is presented as certain when the underlying engine only
produces a probability estimate, and every result records what engine
produced it, which version, and when.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping


@dataclass(frozen=True)
class TranscriptionResult:
    text: str
    confidence: float  # 0.0-1.0; see each provider for how it's derived
    language: str
    provider: str  # e.g. "local_whisper" -- never a vendor name alone,
    # so a caller can tell providers apart without parsing model names
    algorithm: str
    algorithm_version: str
    analyzed_at: datetime
    input_characteristics: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0, 1], got {self.confidence!r}")

    @staticmethod
    def now() -> datetime:
        return datetime.now(timezone.utc)
