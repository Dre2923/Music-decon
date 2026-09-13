# Audio Diagnostics

Chunked audio capture, BPM/key/pitch analysis (librosa + bpm-detector), vocal DSP (loqa-voice-dsp: pitch contour, formants, HNR, H1-H2, vibrato), and diagnostic-explanation generation. See manifesto Sections 3 and 4a.

**Status:** not yet implemented.

Key rules from the manifesto this module must honor:
- Analyze completed buffers/chunks; librosa is not an always-open streaming engine.
- Every diagnostic result carries confidence, source algorithm/version, and time analyzed — never presented as bare certainty.
- Acoustic measurements are described as measurements ("increased breathiness measurement," "unstable pitch"), never as medical diagnoses.
- Any Rust/FFI path for vocal DSP must be benchmarked on real Raspberry Pi 5 hardware before being trusted — the upstream benchmarks are Apple M-series only.
