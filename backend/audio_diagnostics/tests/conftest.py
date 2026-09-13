"""Synthetic-signal fixtures.

There is no real recorded reference audio in this repository yet (see
manifesto Section 12: reference test clips are pre-release evidence to
be gathered separately). These fixtures generate signals with a known
ground truth -- a pure tone at a known frequency, a click train at a
known tempo, a triad at a known key -- so the analysis functions can be
checked against something verifiable without needing a hardware mic or
external audio files.
"""

from __future__ import annotations

import numpy as np
import pytest

from backend.audio_diagnostics.audio_capture import AudioChunk

SAMPLE_RATE = 22050


def _make_chunk(samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> AudioChunk:
    from datetime import datetime, timezone

    return AudioChunk(
        samples=samples.astype(np.float32),
        sample_rate=sample_rate,
        captured_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def sine_440hz_chunk() -> AudioChunk:
    duration = 1.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    samples = 0.5 * np.sin(2 * np.pi * 440.0 * t)
    return _make_chunk(samples)


@pytest.fixture
def silence_chunk() -> AudioChunk:
    return _make_chunk(np.zeros(int(SAMPLE_RATE * 1.0)))


@pytest.fixture
def click_track_120bpm_chunk() -> AudioChunk:
    rng = np.random.default_rng(seed=0)
    duration = 8.0
    n = int(SAMPLE_RATE * duration)
    samples = np.zeros(n)
    click_len = int(0.01 * SAMPLE_RATE)
    interval = 60.0 / 120.0
    position = 0.0
    while position < duration:
        idx = int(position * SAMPLE_RATE)
        if idx + click_len < n:
            samples[idx : idx + click_len] = rng.standard_normal(click_len) * 0.8
        position += interval
    return _make_chunk(samples)


@pytest.fixture
def c_major_chord_chunk() -> AudioChunk:
    duration = 3.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    chord = np.zeros_like(t)
    for freq in (261.63, 329.63, 392.00):  # C4, E4, G4
        for harmonic in range(1, 4):
            chord += (0.3 / harmonic) * np.sin(2 * np.pi * freq * harmonic * t)
    chord = chord / np.max(np.abs(chord)) * 0.7
    return _make_chunk(chord)
