"""Local, offline speech recognition via OpenAI Whisper.

Manifesto Section 4: "Baseline engine: OpenAI Whisper -- code and model
weights currently MIT licensed." Verified directly against the
installed package (openai-whisper 20250625) rather than assumed from
the manifesto text: its `LICENSE` file and README both state "Whisper's
code and model weights are released under the MIT License." See
docs/DEPENDENCY_REGISTER.md for the full verification record.

This module calls the real `whisper` package directly -- no
alternative engine (e.g. faster-whisper/CTranslate2, which is not
named in the manifesto) is substituted, even though such alternatives
are commonly recommended for CPU-only devices like a Raspberry Pi.
That tradeoff is disclosed in docs/OPEN_ISSUES.md rather than decided
here.
"""

from __future__ import annotations

import warnings
from typing import Dict, Optional

import librosa
import numpy as np
import whisper

from backend.audio_diagnostics.audio_capture import AudioChunk

from .transcription_provider import TranscriptionProvider
from .transcription_result import TranscriptionResult

WHISPER_SAMPLE_RATE = whisper.audio.SAMPLE_RATE  # 16000, required by the model

# Raspberry Pi 5 is a CPU-only ARM64 device (manifesto Section 2). The
# large multilingual models (medium/large, 1.5-3GB) are impractical
# there; "tiny"/"base" trade accuracy for something that can plausibly
# run in real time on-device. This default is an IMPLEMENTATION CHOICE
# (manifesto Section 14), not a manifesto requirement, and has not been
# validated against the manifesto's EN/FR/ES domain-vocabulary
# requirement -- see docs/OPEN_ISSUES.md.
DEFAULT_MODEL_NAME = "tiny"


class LocalWhisperProvider(TranscriptionProvider):
    """Transcribes audio entirely on-device via the real `whisper` package."""

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        self._model_name = model_name
        self._model: Optional["whisper.Whisper"] = None

    def _get_model(self) -> "whisper.Whisper":
        if self._model is None:
            self._model = whisper.load_model(self._model_name)
        return self._model

    @staticmethod
    def _resample_to_whisper_rate(chunk: AudioChunk) -> np.ndarray:
        samples = chunk.samples.astype(np.float32)
        if chunk.sample_rate == WHISPER_SAMPLE_RATE:
            return samples
        return librosa.resample(
            samples, orig_sr=chunk.sample_rate, target_sr=WHISPER_SAMPLE_RATE
        )

    @staticmethod
    def _derive_confidence(segments: list) -> float:
        """Whisper doesn't return one scalar confidence for a transcript --
        only per-segment `avg_logprob` (log probability) and
        `no_speech_prob`. This combines them into a single [0,1] proxy:
        exp(avg_logprob) approximates the segment's average per-token
        probability, scaled down by how likely the segment was actually
        silence. This is a derived heuristic over Whisper's own real
        output, not a substitute for Whisper itself, and is labelled as
        such in the returned algorithm name.
        """
        if not segments:
            return 0.0

        weighted_sum = 0.0
        total_duration = 0.0
        for segment in segments:
            duration = max(segment["end"] - segment["start"], 0.0)
            segment_confidence = np.exp(segment["avg_logprob"]) * (
                1.0 - segment["no_speech_prob"]
            )
            weighted_sum += segment_confidence * duration
            total_duration += duration

        if total_duration <= 0:
            return 0.0
        return float(np.clip(weighted_sum / total_duration, 0.0, 1.0))

    def transcribe(
        self, chunk: AudioChunk, language: Optional[str] = None
    ) -> TranscriptionResult:
        audio = self._resample_to_whisper_rate(chunk)
        model = self._get_model()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            result: Dict = whisper.transcribe(
                model, audio, language=language, fp16=False
            )

        confidence = self._derive_confidence(result.get("segments", []))

        return TranscriptionResult(
            text=result["text"].strip(),
            confidence=confidence,
            language=result.get("language", language or "unknown"),
            provider="local_whisper",
            algorithm=f"openai-whisper:{self._model_name}+avg_logprob_confidence_proxy",
            algorithm_version=whisper.version.__version__,
            analyzed_at=TranscriptionResult.now(),
            input_characteristics={
                "sample_rate": chunk.sample_rate,
                "duration_seconds": chunk.duration_seconds,
                "n_samples": len(chunk.samples),
                "model_name": self._model_name,
            },
        )
