# Vendored dependency: bpm-detector

This directory is an unmodified vendored copy of the `bpm-detector` project named
in `docs/MANIFESTO.md` Section 3 ("Chosen: librosa + bpm-detector").

- **Source:** https://github.com/libraz/bpm-detector
- **Pinned commit:** `9e82ed544edd7f06a5459b8fa8fe539f20335df8` (2026-06-02)
- **Package version:** 1.1.0
- **License:** MIT (full text in `LICENSE`, copyright libraz 2025) — permits commercial
  use, modification, and redistribution with the copyright and permission notice
  retained. This NOTICE file and the retained `LICENSE` file satisfy that condition.
- **Verified:** 2026-09-13, by cloning the repository at the commit above and reading
  `LICENSE` and `pyproject.toml` directly, and by checking every one of its declared
  runtime dependencies' license metadata (see `docs/DEPENDENCY_REGISTER.md`).
- **Why vendored instead of a live `pip install git+...`:** installing directly from a
  mutable branch/HEAD at build or install time is a supply-chain and reproducibility
  risk (manifesto Section 10.4: dependency review; Section 10.12: dependency-change
  gate) — the exact code would not be pinned, reviewed, or reproducible from this
  repository alone. This vendored copy is the reviewed code at a specific commit,
  checked into version control here.
- **Not modified:** the contents of `src/bpm_detector/` are copied verbatim from the
  pinned commit. If a fix or change is ever needed, update by re-vendoring a newer
  reviewed commit (updating this NOTICE and the register), not by hand-editing this
  copy in place.

## Important: real dependency footprint

`bpm_detector/__init__.py` eagerly imports the package's entire analysis suite
(chord, melody, harmony, timbre, structure, rhythm, similarity, and more), not just
BPM/key detection. That import chain requires, at minimum, `scikit-learn` (via
`similarity_engine.py` / `boundary_detector.py`), in addition to librosa/numpy/scipy.
Its full `pyproject.toml` dependency list (used by its CLI and parallel-processing
tooling, not by the BPM/key detection this project actually calls) also includes
`matplotlib`, `seaborn`, `pandas`, and `psutil`. All of these are confirmed
permissively licensed and commercial-use compatible (see
`docs/DEPENDENCY_REGISTER.md`), but this is a materially heavier dependency
footprint than the manifesto's "uses librosa internally" description implies, and it
has not yet been benchmarked on the Raspberry Pi 5 backend. See
`docs/OPEN_ISSUES.md`.
