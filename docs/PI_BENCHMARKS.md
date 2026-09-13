# Raspberry Pi 5 Benchmark Results

Real, on-device measurements only. Do not paste results from a dev laptop, this
build environment, or any x86_64 machine here — they are not valid evidence for
manifesto Section 12 pre-release evidence or for closing an ARM64/Pi item in
`docs/OPEN_ISSUES.md`.

## How to run

On the actual Raspberry Pi 5:

```
git clone <this repo>   # or copy the working tree over
cd Music-decon
pip install -r backend/audio_diagnostics/requirements.txt
pip install -e backend/audio_diagnostics/vendor/bpm-detector
python3 backend/audio_diagnostics/benchmark_pi.py
```

It prints a JSON report and also saves it to `docs/pi_benchmarks/<timestamp>.json`.
Paste the report below (a new dated entry, don't overwrite prior ones) and update
`docs/OPEN_ISSUES.md` #8 to reference the entry.

## Results log

_(no on-device results recorded yet — this is a placeholder until you run the
benchmark on your Raspberry Pi 5)_

<!--
### 2026-MM-DD — <Pi 5 RAM/OS/SD or SSD details>

```json
<paste the printed report here>
```

Notes: <anything relevant — thermal throttling, SD vs SSD, concurrent load, etc.>
-->
