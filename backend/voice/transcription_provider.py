"""Transcription provider interface.

Manifesto Section 10.11 (AI-vendor isolation): "Deepgram or any future
cloud AI/transcription vendor must sit behind an internal provider
interface so core logic isn't structurally dependent on one vendor."

This interface exists from the first provider (local Whisper), not
added later once a second vendor shows up -- so nothing calling a
provider ever needs to know or care which one it's talking to.
"""

from __future__ import annotations

import abc
from typing import Optional

from backend.audio_diagnostics.audio_capture import AudioChunk

from .transcription_result import TranscriptionResult


class TranscriptionProvider(abc.ABC):
    """A speech-to-text engine, local or cloud."""

    @abc.abstractmethod
    def transcribe(
        self, chunk: AudioChunk, language: Optional[str] = None
    ) -> TranscriptionResult:
        """Transcribe one captured audio chunk.

        Args:
            chunk: a finite, already-captured chunk (see
                backend/audio_diagnostics/audio_capture.py -- capture
                and transcription are separate concerns here too).
            language: an ISO 639-1 code (e.g. "en", "fr", "es") to force
                the provider to a specific language, or None to let the
                provider auto-detect it.
        """
        raise NotImplementedError
