# Parity Plan

## Target

Retarget Python parity to R NNS 13.0. R NNS 13.0 is the tensorized architecture target, and R NNS 12.1 cache data is superseded. NNS-core is v13.0.0 and remains the native C++ foundation.

## Plan

1. Install R and R dependencies.
2. Install R NNS 13.0 from the vendored source tarball used for this one-repo retarget.
3. Confirm `packageVersion("NNS") == "13.0"`.
4. Validate the R NNS 13.0 smoke values for partial moments, copula, ARMA, regression points, PM matrix naming, and seeded stack behavior.
5. Regenerate `tests/_r_cache.json` with R NNS 13.0 metadata and values.
6. Run cache-only parity, capture the full failure inventory, and fix Python behavior to R NNS 13.0 without loosening tolerances.
7. Keep full parity claims bounded by tests and cache.
8. Keep plot artifact policy unchanged.

## Current retarget focus

The first fixed root cause is the `NNS.reg(..., multivariate.call = TRUE)` regression-point construction used by nonlinear ARMA. Python now preserves R NNS 13.0's duplicate central-point contribution during endpoint consolidation.

## Environment note

In this run, apt package retrieval for R was blocked by HTTP 403 responses from the configured proxy. The cache metadata and Python behavior retarget are committed, but a full R-backed cache regeneration should be repeated where apt/R installation can complete.
