"""Tests for local_whisper.py.

IMPORTANT LIMITATION, disclosed rather than hidden: the actual
whisper.load_model(...) + transcribe(...) round trip needs to download
real model weights from openaipublic.azureedge.net. That host (and
huggingface.co, checked as a possible alternate source) is blocked by
this build environment's network egress policy -- confirmed by direct
connection attempts, not assumed. So the full end-to-end path is
marked as a skipped integration test below rather than silently
omitted or faked. Everything else in local_whisper.py that doesn't
require downloading model weights is fully tested.

To actually run the skipped test: on a machine with normal internet
access (a dev laptop, CI, or the target Raspberry Pi 5), remove the
skip decorator and run it once to confirm the real download + transcribe
path works, then note the result in docs/OPEN_ISSUES.md.
"""

from __future__ import annotations

from datetime import datetime, timezone

import numpy as np
import pytest

from backend.audio_diagnostics.audio_capture import AudioChunk
from backend.voice.local_whisper import LocalWhisperProvider
from backend.voice.transcription_provider import TranscriptionProvider
from backend.voice.transcription_result import TranscriptionResult


def _make_chunk(samples: np.ndarray, sample_rate: int) -> AudioChunk:
    return AudioChunk(
        samples=samples.astype(np.float32),
        sample_rate=sample_rate,
        captured_at=datetime.now(timezone.utc),
    )


def test_local_whisper_provider_implements_the_interface():
    provider = LocalWhisperProvider()
    assert isinstance(provider, TranscriptionProvider)


def test_resample_to_whisper_rate_is_identity_at_16khz():
    samples = np.random.default_rng(0).standard_normal(16000).astype(np.float32)
    chunk = _make_chunk(samples, 16000)

    resampled = LocalWhisperProvider._resample_to_whisper_rate(chunk)

    assert len(resampled) == len(samples)
    np.testing.assert_array_equal(resampled, samples)


def test_resample_to_whisper_rate_changes_length_for_other_rates():
    duration_seconds = 2.0
    samples = np.zeros(int(22050 * duration_seconds), dtype=np.float32)
    chunk = _make_chunk(samples, 22050)

    resampled = LocalWhisperProvider._resample_to_whisper_rate(chunk)

    expected_len = int(16000 * duration_seconds)
    assert abs(len(resampled) - expected_len) <= 1


def test_derive_confidence_with_no_segments_is_zero():
    assert LocalWhisperProvider._derive_confidence([]) == 0.0


def test_derive_confidence_high_for_confident_speech_segments():
    segments = [
        {"start": 0.0, "end": 2.0, "avg_logprob": -0.05, "no_speech_prob": 0.01},
        {"start": 2.0, "end": 4.0, "avg_logprob": -0.10, "no_speech_prob": 0.02},
    ]

    confidence = LocalWhisperProvider._derive_confidence(segments)

    assert 0.8 < confidence <= 1.0


def test_derive_confidence_low_for_likely_silence():
    segments = [
        {"start": 0.0, "end": 1.0, "avg_logprob": -2.5, "no_speech_prob": 0.95},
    ]

    confidence = LocalWhisperProvider._derive_confidence(segments)

    assert confidence < 0.1


def test_derive_confidence_is_duration_weighted():
    # A short, confident segment should not dominate a much longer,
    # unconfident one.
    segments = [
        {"start": 0.0, "end": 0.1, "avg_logprob": -0.01, "no_speech_prob": 0.0},
        {"start": 0.1, "end": 10.0, "avg_logprob": -3.0, "no_speech_prob": 0.9},
    ]

    confidence = LocalWhisperProvider._derive_confidence(segments)

    assert confidence < 0.2


def test_transcription_result_rejects_out_of_range_confidence():
    with pytest.raises(ValueError):
        TranscriptionResult(
            text="hello",
            confidence=1.5,
            language="en",
            provider="local_whisper",
            algorithm="test",
            algorithm_version="0",
            analyzed_at=TranscriptionResult.now(),
            input_characteristics={},
        )


@pytest.mark.skip(
    reason=(
        "Requires downloading real Whisper model weights from "
        "openaipublic.azureedge.net, which this build environment's "
        "network policy blocks (verified by direct connection attempt, "
        "including huggingface.co as an alternate source -- also "
        "blocked). Run this on a machine with normal internet access "
        "to actually verify the end-to-end transcribe path, then record "
        "the result in docs/OPEN_ISSUES.md."
    )
)
def test_transcribe_real_speech_end_to_end():
    import soundfile as sf

    samples, sr = sf.read("path/to/a/real/speech/sample.flac", dtype="float32")
    chunk = _make_chunk(samples, sr)
    provider = LocalWhisperProvider(model_name="tiny")

    result = provider.transcribe(chunk, language="en")

    assert result.text
    assert result.confidence > 0.0
