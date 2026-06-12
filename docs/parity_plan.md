# Parity Plan

This branch completes the pre-migration parity suite for `pyNNS-core-backed` while keeping the `NNS-python` migration out of scope.

## Scope

- Preserve public-behavior parity tests against R NNS 12.1 through `tests/parity/`.
- Keep R calls isolated in the test harness and cache tooling.
- Allow CI to run parity checks without `Rscript` by using committed cache fixtures with `PYNNS_R_CACHE_ONLY=1`.
- Preserve native-vs-Python fallback coverage for partial moments and related helpers.
- Preserve the merged PR #6 fix that blocks non-finite partial-moment inputs from native dispatch.

## Cache workflow

- `tests/_r_cache.json` is the committed R-compatible cache used by CI.
- `PYNNS_R_CACHE_ONLY=1` forces cache-only parity and must be used in CI.
- To refresh cache entries on a workstation with R and NNS installed, run:

```bash
python scripts/regenerate_r_cache.py
```

Pass pytest selectors after `--` to refresh a narrower subset, for example:

```bash
python scripts/regenerate_r_cache.py -- tests/parity/test_core.py
```

## Guardrails

- Do not require `Rscript` in CI.
- Do not reintroduce stale native expectations for partial moments.
- Do not import `pynns.pm_matrix` through the package-level public function when module access is required; use `importlib.import_module("pynns.pm_matrix")`.
- Do not route `NaN` or infinite partial-moment inputs through native `lpm`, `upm`, `lpm_ratio`, or `upm_ratio` dispatch.
