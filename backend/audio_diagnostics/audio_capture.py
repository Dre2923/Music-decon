"""Chunked audio capture.

Manifesto Section 3: capture and analysis are separate responsibilities.
librosa is never wired up as an always-open streaming engine -- each
call captures one finite chunk and returns it for a downstream analyzer
to process.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass
from datetime import datetime, timezone

import numpy as np


@dataclass(frozen=True)
class AudioChunk:
    samples: np.ndarray  # mono float32 in [-1, 1], shape (n_samples,)
    sample_rate: int
    captured_at: datetime

    @property
    def duration_seconds(self) -> float:
        return len(self.samples) / float(self.sample_rate)


class ChunkedAudioCapture(abc.ABC):
    """Captures one finite chunk of audio per call -- not a stream."""

    @abc.abstractmethod
    def capture_chunk(self, duration_seconds: float) -> AudioChunk:
        raise NotImplementedError


class BufferAudioCapture(ChunkedAudioCapture):
    """Serves chunks from an in-memory buffer or a loaded audio file.

    Used for offline analysis (e.g. a previously recorded practice take)
    and for tests, where there is no live microphone to read from.
    """

    def __init__(self, samples: np.ndarray, sample_rate: int):
        if samples.ndim != 1:
            raise ValueError("BufferAudioCapture expects mono samples (1-D array)")
        self._samples = samples.astype(np.float32, copy=False)
        self._sample_rate = sample_rate
        self._position = 0

    @classmethod
    def from_wav_file(cls, path: str) -> "BufferAudioCapture":
        import soundfile as sf

        samples, sample_rate = sf.read(path, dtype="float32", always_2d=False)
        if samples.ndim > 1:
            samples = samples.mean(axis=1)
        return cls(samples, sample_rate)

    def capture_chunk(self, duration_seconds: float) -> AudioChunk:
        n = int(round(duration_seconds * self._sample_rate))
        end = min(self._position + n, len(self._samples))
        chunk_samples = self._samples[self._position : end]
        self._position = end
        return AudioChunk(
            samples=chunk_samples,
            sample_rate=self._sample_rate,
            captured_at=datetime.now(timezone.utc),
        )

    @property
    def exhausted(self) -> bool:
        return self._position >= len(self._samples)


class MicrophoneAudioCapture(ChunkedAudioCapture):
    """Captures a chunk from the default input device via sounddevice.

    STATUS: implemented against the sounddevice API but not yet
    exercised against physical hardware or the target Raspberry Pi 5 --
    this environment has no audio input device to test against. Per
    manifesto Section 12, do not treat this class as verified until a
    hardware capture test has actually run and its result is recorded
    as pre-release evidence.
    """

    def __init__(self, sample_rate: int = 22050, device: int | str | None = None):
        self._sample_rate = sample_rate
        self._device = device

    def capture_chunk(self, duration_seconds: float) -> AudioChunk:
        import sounddevice as sd

        n = int(round(duration_seconds * self._sample_rate))
        recording = sd.rec(
            n,
            samplerate=self._sample_rate,
            channels=1,
            dtype="float32",
            device=self._device,
        )
        sd.wait()
        return AudioChunk(
            samples=recording[:, 0],
            sample_rate=self._sample_rate,
            captured_at=datetime.now(timezone.utc),
        )
