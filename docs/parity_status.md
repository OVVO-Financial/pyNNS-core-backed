# Parity Status

## Current status

- The parity suite lives in `tests/parity/` and compares public PyNNS behavior to R NNS-compatible cached fixtures.
- CI-compatible parity runs use `PYNNS_R_CACHE_ONLY=1` and the committed `tests/_r_cache.json` cache.
- Native-vs-fallback coverage lives in `tests/invariants/test_native_original_src_coverage.py`.
- The PR #6 non-finite native-routing fix is preserved in `src/pynns/core.py` through `_native_safe(...)` checks in `lpm`, `upm`, `lpm_ratio`, and `upm_ratio`.

## Skipped or deferred cases

- Live R regeneration is not required in CI because many runners do not have `Rscript` or R NNS installed.
- Cache regeneration remains optional and developer-local via `scripts/regenerate_r_cache.py`.
- The NNS-python migration remains out of scope for this branch.

## Regression coverage

- `tests/invariants/test_native_original_src_coverage.py` verifies native smoke behavior only for symbols exported by the currently built optional extension.
- The same file verifies public fallback behavior when native is disabled or unavailable.
- Non-finite partial-moment inputs are covered by a focused regression that monkeypatches native dispatch and proves NaN inputs use the Python fallback.
