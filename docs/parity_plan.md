# Parity plan before NNS-python migration

This prototype repository is the staging area for parity hardening before any code is moved to the clean `NNS-python` repository. The migration itself is out of scope for this branch.

## Definition of parity

Parity covers four public-contract layers:

1. **Python fallback parity**: existing Python implementations remain stable and keep their current public behavior.
2. **Native C++ parity**: any public function routed through `_nnscore` must match the Python fallback with the same keys, shapes, matrix orientation, index bases, and scalar/vector conventions.
3. **R NNS parity**: Python public outputs match R package outputs where equivalent R functions exist and R behavior is stable enough to treat as a contract.
4. **Fixture parity**: committed golden fixtures let CI validate known R-compatible outputs without requiring `Rscript`.

## Completed in this branch

- Created the parity fixture layout under `tests/parity/fixtures/` and optional regeneration scripts under `tests/parity/r_scripts/`.
- Added committed golden fixtures for partial moments, central tendencies, and the verified `NNS.reg` example.
- Added native-vs-fallback tests for the public native-routed partial moment APIs:
  - `lpm`
  - `upm`
  - `lpm_ratio`
  - `upm_ratio`
  - `co_lpm`
  - `co_upm`
  - `d_lpm`
  - `d_upm`
  - `pm_matrix`
- Added direct native binding parity/smoke tests for private backend helpers:
  - `lpm_v`, `upm_v`, `lpm_ratio_v`, `upm_ratio_v`
  - `co_lpm_v`, `co_upm_v`, `d_lpm_v`, `d_upm_v`
  - `clpm_nd`, `cupm_nd`, `dpm_nd`, `clpm_nd_batch`
  - `fast_lm`, `fast_lm_mult`
  - `stochastic_superiority`
  - `vec_sd`, `col_sd`, `is_discrete`, `factor_2_dummy`, `factor_2_dummy_fr`
  - `generate_vectors`, `generate_lin_vectors`
- Added central-tendency parity coverage for `nns_gravity`, `nns_mode`, and `nns_rescale`. `nns_rescale` remains Python-only by design.
- Added fast linear model helper coverage and regression shape coverage around monotonic, nonlinear, repeated-`x`, and extrapolation samples.
- Updated CI to install the package with `.[dev]`, run invariant tests, run parity tests, run Ruff, run mypy, and build distributions.

## Fixture strategy

Committed fixtures are the default source for CI. Optional R regeneration scripts live in `tests/parity/r_scripts/` and are tested only when `Rscript` is available. If `Rscript` is unavailable, regeneration tests skip and the committed fixtures remain authoritative.

## Rule for new native routing

No additional public API may be routed through native C++ unless all are true:

- The Python fallback has tests.
- Python output matches a committed R fixture where R has an equivalent public function.
- Native output matches the Python fallback.
- Native output matches the R fixture where applicable.
- Shape, keys, orientation, index bases, scalar/vector behavior, and list/dictionary payloads match the current Python public API.
- CI passes.

## Deferred or blocked work

The following areas remain Python-only until their existing Python-vs-R parity is fully documented and native-vs-fallback tests are added:

- Dependence (`nns_dep`, `nns_cor`, `co_lpm_nd`, `co_upm_nd`, `dpm_nd`): matrix orientation, normalization, discrete/factor behavior, and result keys must remain stable.
- Distance (`nns_distance`, `nns_distance_bulk`): rescaling, weighting, k/path output, class handling, and index bases require dedicated fixtures.
- Partition (`nns_part`): row order, labels, regression-point payloads, horizontal/vertical segments, and index bases require exact R-compatible fixture coverage.
- Seasonality (`nns_seas`): modulo behavior, detected periods, keys, and output order require exact fixture coverage.
- Stochastic dominance (`fsd_uni`, `ssd_uni`, `tsd_uni`, `fsd`, `ssd`, `tsd`): dominance matrix orientation and tie/equal-sample conventions must be fixture-tested before routing.
- ARMA and MEBoot: stochastic seed behavior, reproducibility, and tolerance policy must be documented before any native routing of mutable or stochastic helpers.

## Out of scope

- Renaming `pynns` to `nns`.
- Touching `OVVO-Financial/NNS-python`.
- Publishing to PyPI or TestPyPI.
- Migrating code into `NNS-python`.
