"""Raspberry Pi 5 benchmark for the audio diagnostics module.

RUN THIS ON THE ACTUAL RASPBERRY PI 5 -- results from any other machine
(a dev laptop, this build environment, etc.) are not valid evidence for
manifesto Section 12's pre-release evidence requirement or for closing
docs/OPEN_ISSUES.md #8.

Usage (on the Pi, inside the project's Python environment):

    pip install -r backend/audio_diagnostics/requirements.txt
    pip install -e backend/audio_diagnostics/vendor/bpm-detector
    python3 backend/audio_diagnostics/benchmark_pi.py

It prints a report and also writes it as JSON to
docs/pi_benchmarks/<timestamp>.json. Paste the printed report (or the
JSON) into docs/OPEN_ISSUES.md #8 and docs/PI_BENCHMARKS.md so the
result is recorded, not just observed once and forgotten.
"""

from __future__ import annotations

import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _measure_rss_mb() -> float | None:
    try:
        import psutil

        return psutil.Process().memory_info().rss / (1024 * 1024)
    except Exception:
        return None


def _make_test_signal(sr: int, duration: float) -> np.ndarray:
    rng = np.random.default_rng(seed=0)
    n = int(sr * duration)
    samples = np.zeros(n)
    click_len = int(0.01 * sr)
    interval = 60.0 / 120.0
    position = 0.0
    while position < duration:
        idx = int(position * sr)
        if idx + click_len < n:
            samples[idx : idx + click_len] = rng.standard_normal(click_len) * 0.8
        position += interval
    return samples.astype(np.float32)


def main() -> None:
    report: dict = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python_version": sys.version,
        "rss_mb_at_start": _measure_rss_mb(),
    }

    t0 = time.perf_counter()
    from backend.audio_diagnostics.audio_capture import BufferAudioCapture
    from backend.audio_diagnostics.bpm_key_pitch import (
        analyze_bpm,
        analyze_key,
        analyze_pitch,
    )

    report["import_seconds"] = time.perf_counter() - t0
    report["rss_mb_after_import"] = _measure_rss_mb()

    sr = 22050
    duration = 30.0  # a representative practice-take length, not a 1s toy clip
    samples = _make_test_signal(sr, duration)
    capture = BufferAudioCapture(samples, sr)
    chunk = capture.capture_chunk(duration)

    timings = {}
    for name, fn in (
        ("bpm", analyze_bpm),
        ("key", analyze_key),
        ("pitch", analyze_pitch),
    ):
        t0 = time.perf_counter()
        result = fn(chunk)
        elapsed = time.perf_counter() - t0
        timings[name] = {
            "seconds": elapsed,
            "value": result.value,
            "confidence": result.confidence,
        }

    report["input_duration_seconds"] = duration
    report["analysis_timings"] = timings
    report["rss_mb_after_analysis"] = _measure_rss_mb()

    print(json.dumps(report, indent=2, default=str))

    out_dir = Path(__file__).resolve().parents[2] / "docs" / "pi_benchmarks"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.json"
    out_path.write_text(json.dumps(report, indent=2, default=str))
    print(f"\nWrote {out_path}")
    print(
        "\nNext step: copy this report's numbers into docs/PI_BENCHMARKS.md and "
        "update docs/OPEN_ISSUES.md #8 so this is a recorded result, not just "
        "something that ran once on a terminal."
    )


if __name__ == "__main__":
    main()
