"""Diagnostic result data model.

Manifesto Section 3, accuracy rule: no musical diagnostic is represented
as certainty when the underlying analyzer only produces a confidence
estimate. Every result records what produced it, which version, and
when -- so a later algorithm upgrade is never silently attributed to
historical results it didn't produce.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping


@dataclass(frozen=True)
class DiagnosticResult:
    value: Any
    confidence: float  # 0.0-1.0; the analyzer's own confidence estimate
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
