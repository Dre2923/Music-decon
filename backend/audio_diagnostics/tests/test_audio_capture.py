from __future__ import annotations

import numpy as np
import pytest

from backend.audio_diagnostics.audio_capture import BufferAudioCapture


def test_buffer_capture_returns_requested_duration():
    sr = 22050
    samples = np.zeros(sr * 4, dtype=np.float32)
    capture = BufferAudioCapture(samples, sr)

    chunk = capture.capture_chunk(1.0)

    assert chunk.sample_rate == sr
    assert chunk.duration_seconds == pytest.approx(1.0, abs=1.0 / sr)


def test_buffer_capture_advances_position_across_calls():
    sr = 22050
    samples = np.arange(sr * 2, dtype=np.float32)
    capture = BufferAudioCapture(samples, sr)

    first = capture.capture_chunk(1.0)
    second = capture.capture_chunk(1.0)

    assert not np.array_equal(first.samples, second.samples)
    assert capture.exhausted


def test_buffer_capture_rejects_multichannel_input():
    with pytest.raises(ValueError):
        BufferAudioCapture(np.zeros((100, 2), dtype=np.float32), 22050)


def test_buffer_capture_short_final_chunk_does_not_raise():
    sr = 22050
    samples = np.zeros(int(sr * 0.5), dtype=np.float32)
    capture = BufferAudioCapture(samples, sr)

    chunk = capture.capture_chunk(1.0)  # requests more than remains

    assert chunk.duration_seconds == pytest.approx(0.5, abs=1.0 / sr)
    assert capture.exhausted
