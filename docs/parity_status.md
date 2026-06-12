# Parity status

Current status for PR #3 after updating onto latest main:

- Latest main is included, including the refreshed vendored `extern/NNS-core`
  source and the native coverage invariant fixes merged in PR #4.
- The parity suite remains rooted in `tests/parity/` with shared fixtures and the
  R bridge/cache in `tests/_r.py` and `tests/_r_cache.json`.
- Optional native-extension checks remain in
  `tests/invariants/test_native_original_src_coverage.py` and compare public
  native paths against fallback behavior where applicable.
- The `pynns.pm_matrix` monkeypatch tests import the implementation module with
  `importlib.import_module("pynns.pm_matrix")`, preserving the main-branch fix
  that avoids resolving the public `pynns.pm_matrix` function export instead of
  the module.
- The direct native LPM expected value remains `1.25`; the stale `0.3125`
  expectation must not be restored.
- Ratio expectations remain fallback comparisons, not stale fixed constants.
- NNS-python migration remains out of scope. This branch does not rename
  `pynns`, does not touch NNS-python, and does not publish artifacts.

## Running locally

Required verification commands for this branch:

```bash
python -m pytest -q tests/invariants
PYNNS_R_CACHE_ONLY=1 python -m pytest -q tests/parity
ruff check .
mypy
python -m build
```

The parity command may also run without `PYNNS_R_CACHE_ONLY=1` when Rscript and
R `NNS` are installed and cache refreshes are intended.
