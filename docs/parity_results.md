# Parity Results

## Executive summary

The current prototype has strong fixture-backed parity coverage for the core partial-moment machinery and several original R test areas, plus broad cache-backed parity coverage. Remaining gaps are documented and should be closed before final NNS-python migration.

This report consolidates the merged-state parity evidence from `docs/parity_status.md`, `docs/original_tests_adoption.md`, `tests/parity/`, `tests/fixtures/original_tests_expected.json`, `tests/_r_cache.json`, and `tests/invariants/test_native_original_src_coverage.py`. It does **not** claim full package parity. It also does not introduce native routing, rename `pynns`, touch NNS-python, or move the project toward publication.

## Test commands

The expected verification commands for this state are:

```bash
python -m pytest -q tests/invariants
PYNNS_R_CACHE_ONLY=1 python -m pytest -q tests/parity
PYNNS_R_CACHE_ONLY=1 python -m pytest -q tests/parity/test_original_*
ruff check .
mypy
python -m build
```

`python -m build` is a packaging check only. It should be run when the local environment already has build tooling available. If the `build` module is missing and network access or dependency installation is unavailable, that limitation should be recorded instead of treating it as a parity failure.

## Latest observed results

Local verification for this consolidation branch on 2026-06-12, using the repository virtual environment, observed:

- `python -m pytest -q tests/invariants` produced `314 passed`.
- `PYNNS_R_CACHE_ONLY=1 python -m pytest -q tests/parity` produced `1 failed, 1773 passed, 11 skipped`; the failure was `tests/parity/test_boost.py::test_nns_boost_ivs_test_none_matches_r`, where the current Python `nns_boost` predictions diverged from the committed R cache for the `depth=None` / `feature_importance=False` case.
- `PYNNS_R_CACHE_ONLY=1 python -m pytest -q tests/parity/test_original_*` produced `9 passed`.
- `ruff check .` passed.
- `mypy` passed.
- `python -m build` was blocked because the local virtual environment does not have the `build` module installed.

Historical known results from PR #7:

- `python -m pytest -q tests/invariants` produced `314 passed`.
- `PYNNS_R_CACHE_ONLY=1 python -m pytest -q tests/parity` produced `1765 passed, 11 skipped`.
- `ruff check .` passed.
- `mypy` passed.
- `python -m build` was blocked locally by a missing `build` module / network limits.

Historical known results from PR #8:

- `python -m pytest -q tests/invariants` produced `314 passed`.
- `PYNNS_R_CACHE_ONLY=1 python -m pytest -q tests/parity/test_original_*` produced `9 passed`.
- Original test adoption added fixture-backed parity tests for ANOVA, dependence/copula partial coverage, partial moments, partition, stochastic dominance, SD efficient set, and univariate SD routines.

## Native-vs-fallback coverage

Native-vs-fallback coverage is enforced in `tests/invariants/test_native_original_src_coverage.py` and documented in `docs/parity_status.md` and `docs/native_original_src_coverage.md`.

Current verified native/fallback areas include:

- Native smoke checks for symbols exported by the currently built optional extension.
- Public fallback behavior when native is disabled or unavailable.
- Partial-moment native routing for `lpm`, `upm`, `lpm_ratio`, `upm_ratio`, `co_lpm`, `co_upm`, `d_lpm`, `d_upm`, and `pm_matrix` where finite inputs and supported shapes permit native dispatch.
- Explicit non-finite fallback behavior for `lpm` and `upm`, preserving Python fallback semantics instead of forcing native execution on `NaN` inputs.
- Private/native backend smoke checks for selected original-source helpers such as fast linear-model helpers and internal utility bindings when exported.

This is not a full native-backend claim. Some C++ functions are intentionally unbound, private-only, or deferred while the Python public semantics and parity fixtures mature.

## R-cache parity coverage

The committed cache in `tests/_r_cache.json` is the offline parity source used by `PYNNS_R_CACHE_ONLY=1`. The cache currently records schema version `1`, R NNS version `12.1`, and 2,406 keyed R result entries.

Cache-backed parity covers broad public API behavior across `tests/parity/`, including ANOVA, ARMA, boosting, categorical wrappers, causation, CDF, classical helpers, co-moments, copula bivariate coverage, core partial moments, dependence, differences, distance, Monte Carlo helpers, meboot, multivariate regression, normalization, partitioning, PM matrix, practical examples, public wrappers, regression, regression helpers, SD clustering, seasonality, stack, stochastic dominance, stochastic superiority, and variance helpers.

When `PYNNS_R_CACHE_ONLY=1` is set, missing cache entries remain blocked unless the cache is regenerated in an environment with `Rscript` and R NNS installed. Any such cache miss is a parity-data gap, not evidence that Python and R match.

## Original R tests adoption coverage

`original_tests/` has been inventoried in `docs/original_tests_adoption.md`. The adopted pytest coverage uses committed R-derived fixtures in `tests/fixtures/original_tests_expected.json` and literal deterministic vectors parsed from the original R test files.

Current original-test adoption includes:

- ANOVA certainty and pairwise matrix checks from `test_ANOVA.R`.
- Bivariate continuous copula coverage from `test_Copula.R`.
- Partial-moment scalar coverage for `LPM`, `UPM`, `Co.UPM`, `Co.LPM`, `D.LPM`, `D.UPM`, `LPM.ratio`, and `UPM.ratio`.
- PM matrix covariance outputs and survival CDF behavior from `test_Partial_Moments.R`.
- Partition-map order, row labels, orientation, and regression points from `test_Partition_Map.R`.
- FSD, SSD, and TSD label parity from `test_FSD_SSD_TSD.R`.
- SD efficient-set name/order parity from `test_SD_efficient_Set.R`.
- Univariate FSD, SSD, and TSD routines from `test_Uni_SD_Routines.R`.

The original-test fixture file contains expected values for seven original R test files, including expected values for documented copula gaps that are not yet adopted as full Python API parity.

## Fully adopted functions

The following areas are fully adopted relative to the original R tests currently represented in pytest:

- `NNS.ANOVA` / `pynns.nns_anova` for original certainty and pairwise matrix behavior.
- `NNS.part` / `pynns.nns_part` for the original partition map case.
- `NNS.FSD`, `NNS.SSD`, and `NNS.TSD` / `pynns.fsd`, `pynns.ssd`, and `pynns.tsd` for original dominance-label cases.
- `NNS.SD.efficient.set` / `pynns.sd_efficient_set` for original efficient-set name and order cases.
- `NNS.FSD.uni`, `NNS.SSD.uni`, and `NNS.TSD.uni` / `pynns.fsd_uni`, `pynns.ssd_uni`, and `pynns.tsd_uni` for original unidirectional dominance cases.

These are full adoptions of the current original-test fixtures, not claims that every parameter combination or every R package behavior is complete.

## Partially adopted functions

The following areas are partially adopted and should remain clearly documented:

- `NNS.copula` / `pynns.nns_copula`: bivariate continuous parity is adopted; discrete mode and multivariate / three-column modes are fixture-backed documented gaps.
- `PM.matrix` / `pynns.pm_matrix`: covariance output parity is adopted for the represented matrix cases; R data-frame naming behavior is intentionally not asserted because the Python API uses NumPy arrays.
- Partial moments as a family: scalar original-test cases and broad cache-backed parity are strong, but this remains scoped to the tested public behavior and documented native/fallback routes.
- R cache parity generally: broad cache-backed coverage is present, but any test requiring an absent cache entry remains blocked in cache-only mode when `Rscript` is unavailable.

## Blocked or deferred cases

- `NNS.copula(..., continuous=FALSE)` discrete mode is blocked/deferred until the Python API supports that public behavior.
- `NNS.copula` multivariate / three-column mode is blocked/deferred until the Python API supports that public behavior.
- R plot artifacts, including `Rplots.pdf`, are not adopted because CI parity should compare values and should not create or compare graphics-device artifacts.
- `PM.matrix` R data-frame naming behavior is deferred because Python exposes NumPy-oriented structures rather than R data-frame name repair and labeling behavior.
- Any parity test requiring a missing `tests/_r_cache.json` entry is blocked under `PYNNS_R_CACHE_ONLY=1` or other offline modes when `Rscript` is unavailable.
- `python -m build` can be blocked by missing local build tooling; this is separate from runtime parity.

## Known gaps

- Full package parity has not been established.
- Discrete and multivariate copula parity is not complete.
- Graphics/plot parity is intentionally out of scope for current CI parity.
- R-specific data-frame naming quirks are not fully represented on Python NumPy surfaces.
- Some native original-source functions are private-only, intentionally unbound, or not routed from public Python APIs.
- Cache-only verification depends on the committed cache. Missing cache records require a developer-local R environment to regenerate.
- The current reports are snapshots of verified behavior; behavior outside the tested fixtures and cache entries should not be described as parity-complete.

## Status table

| Area | Python API | R source | Native routed | Python-vs-R cache parity | Original R test adopted | Native-vs-fallback tested | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| ANOVA | `nns_anova` | `NNS.ANOVA`, `test_ANOVA.R` | No | Yes | Yes | No | fixture-complete | Original certainty and pairwise matrix are fixture-backed. |
| Partial moments: scalar LPM/UPM | `lpm`, `upm` | `LPM`, `UPM`, `test_Partial_Moments.R` | Yes | Yes | Yes | Yes | native-complete | Includes non-finite fallback guard for public behavior. |
| Partial moments: ratios | `lpm_ratio`, `upm_ratio` | `LPM.ratio`, `UPM.ratio`, `test_Partial_Moments.R` | Yes | Yes | Yes | Yes | native-complete | Scalar and vector target routes have native/fallback coverage where supported. |
| Co/dependent partial moments | `co_lpm`, `co_upm`, `d_lpm`, `d_upm` | `Co.LPM`, `Co.UPM`, `D.LPM`, `D.UPM`, `test_Partial_Moments.R` | Yes | Yes | Yes | Yes | native-complete | Original scalar cases are adopted; broader behavior remains bounded by cache tests. |
| PM matrix covariance | `pm_matrix` | `PM.matrix`, `test_Partial_Moments.R` | Yes | Yes | Yes | Yes | partial | Numeric covariance parity is covered; R data-frame naming behavior is deferred. |
| Survival CDF from original partial-moment tests | `nns_cdf(type="survival")` | `NNS.CDF`, `test_Partial_Moments.R` | No | Yes | Yes | No | fixture-complete | Original survival function values are adopted. |
| Copula bivariate continuous | `nns_copula` | `NNS.copula`, `test_Copula.R` | No | Yes | Yes | No | fixture-complete | Original bivariate continuous value is adopted. |
| Copula discrete mode | none / not exposed as adopted behavior | `NNS.copula(..., continuous=FALSE)`, `test_Copula.R` | No | Fixture value only | No | No | blocked | Expected R value is recorded, but Python parity is deferred. |
| Copula multivariate / three-column mode | none / not exposed as adopted behavior | `NNS.copula` three-column cases, `test_Copula.R` | No | Fixture values only | No | No | blocked | Continuous and discrete multivariate expected values are recorded, but Python parity is deferred. |
| Partition map | `nns_part` | `NNS.part`, `test_Partition_Map.R` | No | Yes | Yes | No | fixture-complete | Original order, row labels, orientation, and regression points are adopted. |
| FSD/SSD/TSD labels | `fsd`, `ssd`, `tsd` | `NNS.FSD`, `NNS.SSD`, `NNS.TSD`, `test_FSD_SSD_TSD.R` | No | Yes | Yes | No | fixture-complete | Original dominance labels are adopted for represented cases. |
| Univariate SD routines | `fsd_uni`, `ssd_uni`, `tsd_uni` | `NNS.FSD.uni`, `NNS.SSD.uni`, `NNS.TSD.uni`, `test_Uni_SD_Routines.R` | No | Yes | Yes | No | fixture-complete | Original unidirectional cases are adopted. |
| SD efficient set | `sd_efficient_set` | `NNS.SD.efficient.set`, `test_SD_efficient_Set.R` | No | Yes | Yes | No | fixture-complete | Python indices are mapped back to original R names for parity. |
| Broad cached parity suite | Many public `pynns` APIs | Installed R NNS via test harness | Mixed | Yes | Mixed | Mixed | partial | `tests/parity/` is broad and cache-backed, but not full package parity; local consolidation verification currently has one `nns_boost` cache-parity failure. |
| Native original-source smoke coverage | Optional `_nnscore` routes and helpers | Vendored NNS-core C++ | Yes, where bound | No | No | Yes | native-complete | Covers currently exported native symbols and public fallback behavior. |
| R plot artifact | No Python API | `Rplots.pdf` and plot flags | No | No | No | No | no-python-equivalent | CI intentionally avoids graphics-device artifacts. |
| R testthat harness | pytest invocation | `testthat.R` | No | No | No | No | no-python-equivalent | Python uses pytest rather than R testthat. |
| Python-only invariants | Various Python APIs | n/a | Mixed | No | No | Yes where relevant | python-only | These verify Python contracts rather than R parity. |
| Missing R-cache entries offline | Any affected API | Installed R NNS | n/a | No | n/a | n/a | blocked | Cache misses require online regeneration with `Rscript` and R NNS. |

## Release-readiness assessment

The current merged state is suitable for continued prototype validation and internal parity hardening. It is not release-ready as a full R NNS replacement and should not be described as complete package parity.

Positive signals:

- Invariant checks have been observed passing at `314 passed`.
- Original-test parity has been observed passing at `9 passed`.
- Ruff and mypy have both been observed passing.
- Core partial-moment native/fallback behavior has targeted tests.
- Historical cache-only parity from PR #7 was `1765 passed, 11 skipped`, but the local consolidation-branch run currently shows one `nns_boost` parity failure that must be resolved or explicitly triaged before release.

Release blockers or cautions:

- Copula discrete and multivariate modes remain incomplete.
- R plotting behavior and artifacts remain intentionally unported.
- R-specific data-frame naming behavior for `PM.matrix` remains unrepresented.
- The parity claim is bounded by committed fixtures and cache entries.
- The local full parity run has one current `nns_boost` cache-parity failure.
- Packaging verification can be blocked in local environments without the `build` module.

## What remains before NNS-python migration

Before any final NNS-python migration, the project should:

1. Close or explicitly scope the discrete and multivariate copula gaps.
2. Decide whether plot artifacts and graphics behavior are permanently out of scope or need a separate visual/regression policy.
3. Decide how to document or emulate R data-frame naming behavior for Python users, especially around `PM.matrix`.
4. Regenerate and review R cache entries in a controlled environment with `Rscript` and R NNS installed.
5. Expand original R test adoption where additional upstream tests or stable public examples are available.
6. Keep native routing limited to verified public behavior and avoid adding new routes without parity and fallback tests.
7. Maintain the `pynns` package name until a separate migration plan explicitly covers NNS-python naming, compatibility, packaging, and publication.
