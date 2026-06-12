# Parity status

Status values: `complete`, `python-r-complete`, `native-complete`, `python-only-complete`, `blocked`, `not-started`, `intentionally-out-of-scope`.

| Python function | Python module | R equivalent | Native C++ equivalent | Python fallback test exists | Native-vs-fallback test exists | Python-vs-R fixture exists | Native-vs-R test exists | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `FactorDesign` | `pynns.regression` | none | none | yes | n/a | n/a | n/a | python-only-complete | Dataclass payload helper for Python regression factor expansion. |
| `causal_matrix` | `pynns.causation` | `NNS.caus` support behavior | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover public wrapper behavior; no native route planned. |
| `co_lpm` | `pynns.co_moments` | `Co.LPM` | `co_lpm`, `co_lpm_v` | yes | yes | yes | partial | complete | Native-routed public API covered against Python fallback and committed fixture. |
| `co_lpm_nd` | `pynns.dependence` | N-dimensional co-LPM helper | `clpm_nd`, `clpm_nd_batch` private only | yes | private only | partial | no | blocked | Public dependence semantics need complete R fixture coverage before routing. |
| `co_upm` | `pynns.co_moments` | `Co.UPM` | `co_upm`, `co_upm_v` | yes | yes | yes | partial | complete | Native-routed public API covered against Python fallback and committed fixture. |
| `co_upm_nd` | `pynns.dependence` | N-dimensional co-UPM helper | `cupm_nd` private only | yes | private only | partial | no | blocked | Public dependence semantics need complete R fixture coverage before routing. |
| `d_lpm` | `pynns.co_moments` | `D.LPM` | `d_lpm`, `d_lpm_v` | yes | yes | yes | partial | complete | Native-routed public API covered against Python fallback and committed fixture. |
| `dpm_nd` | `pynns.dependence` | N-dimensional DPM helper | `dpm_nd` private only | yes | private only | partial | no | blocked | Public dependence shape/orientation parity must be completed before routing. |
| `dy_d` | `pynns.diff` | `dy.d_` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover R-compatible behavior. |
| `dy_dx` | `pynns.diff` | `dy.dx` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover R-compatible behavior. |
| `d_upm` | `pynns.co_moments` | `D.UPM` | `d_upm`, `d_upm_v` | yes | yes | yes | partial | complete | Native-routed public API covered against Python fallback and committed fixture. |
| `ecdf_pm` | `pynns.classical` | classical PM helper | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover public classical helper behavior. |
| `encode_factor_codes` | `pynns.categorical` | factor coding conventions | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover level order and unseen values. |
| `factor_2_dummy` | `pynns.categorical` | `factor.2.dummy` | `factor_2_dummy` private only | yes | yes | yes | partial | complete | Public Python wrapper and private native binding covered. |
| `factor_2_dummy_fr` | `pynns.categorical` | `factor.2.dummy.fr` | `factor_2_dummy_fr` private only | yes | yes | yes | partial | complete | Public Python wrapper and private native binding covered. |
| `fsd` | `pynns.stochastic_dominance` | `FSD` | exists unbound | yes | no | yes | no | blocked | Matrix orientation and index-base fixtures must be complete before routing. |
| `fsd_uni` | `pynns.stochastic_dominance` | `FSD.uni` | exists unbound | yes | no | yes | no | blocked | Keep Python authoritative until dominance fixture suite is complete. |
| `kurt_pm` | `pynns.classical` | PM kurtosis helper | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover public classical helper behavior. |
| `lpm` | `pynns.core` | `LPM` | `lpm`, `lpm_v` | yes | yes | yes | partial | complete | Native-routed public API covered for degrees 0/1/2, scalar/vector targets, ties, zeros, signs, and empty input validation. |
| `lpm_ratio` | `pynns.core` | `LPM.ratio` | `lpm_ratio_v` | yes | yes | yes | partial | complete | Native-routed public API covered for degree and target variants. |
| `lpm_var` | `pynns.var` | `LPM.VaR` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover R-compatible value-at-risk behavior. |
| `mean_pm` | `pynns.classical` | PM mean helper | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover public classical helper behavior. |
| `nns_anova` | `pynns.anova` | `NNS.ANOVA` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover public ANOVA behavior. |
| `nns_arma` | `pynns.arma` | `NNS.ARMA` | ARMA helpers intentionally unbound | yes | no | yes | no | blocked | Stochastic/reproducibility policy must be documented before native routing. |
| `nns_arma_optim` | `pynns.arma` | `NNS.ARMA.optim` | ARMA helpers intentionally unbound | yes | no | yes | no | blocked | Stochastic/reproducibility policy must be documented before native routing. |
| `nns_boost` | `pynns.boost` | `NNS.boost` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover public boosting behavior. |
| `nns_causation` | `pynns.causation` | `NNS.caus` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover causation behavior. |
| `nns_cdf` | `pynns.cdf` | `NNS.CDF` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover CDF behavior. |
| `nns_copula` | `pynns.copula` | `NNS.copula` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover copula behavior. |
| `nns_cor` | `pynns.dependence` | `NNS.cor` | dependence C++ exists unbound | yes | no | yes | no | blocked | Dependence matrix orientation, normalization, and factor behavior must be fixture-locked before routing. |
| `nns_dep` | `pynns.dependence` | `NNS.dep` | dependence C++ exists unbound | yes | no | yes | no | blocked | Public dependence payload needs complete R fixture documentation before routing. |
| `nns_diff` | `pynns.diff` | `NNS.diff` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover wrapper behavior. |
| `nns_distance` | `pynns.distance` | `NNS.dist` | distance C++ exists unbound | yes | no | yes | no | blocked | Rescaling, weighting, k/path output, categorical handling, and index bases require dedicated fixture lock. |
| `nns_distance_bulk` | `pynns.distance` | bulk distance behavior | distance C++ exists unbound | yes | no | yes | no | blocked | Keep Python-only until bulk shape/orientation and index-base fixtures are complete. |
| `nns_gravity` | `pynns.central_tendencies` | `NNS.gravity` | `gravity` | yes | yes | yes | partial | complete | Public native path covered against fallback and committed central-tendency fixture. |
| `nns_mode` | `pynns.central_tendencies` | `NNS.mode` | `mode` | yes | yes | yes | partial | complete | Public native path covered against fallback and committed central-tendency fixture. |
| `nns_moments` | `pynns.classical` | `NNS.moments` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover moment payload. |
| `nns_m_reg` | `pynns.multivariate_regression` | `NNS.m.reg` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover multivariate regression behavior. |
| `nns_mc` | `pynns.mc` | `NNS.MC` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover Monte Carlo helper behavior. |
| `nns_meboot` | `pynns.meboot` | `NNS.meboot` | MEBoot helpers intentionally unbound | yes | no | yes | no | blocked | Stochastic seed/reproducibility tolerance must be documented before native routing. |
| `nns_norm` | `pynns.norm` | `NNS.norm` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover normalization behavior. |
| `nns_nowcast_panel` | `pynns.providers.nowcast` | none in current R NNS | none | yes | n/a | n/a | n/a | python-only-complete | R NNS nowcast equivalent is unavailable; Python contract is covered by invariants. |
| `nns_part` | `pynns.part` | `NNS.part` | partition C++ exists unbound | yes | no | yes | no | blocked | Exact rows, labels, regression points, segment payloads, and index bases must be fixture-locked. |
| `nns_reg` | `pynns.regression` | `NNS.reg` | no full C++ equivalent; `fast_lm` helper only | yes | helper only | yes | no | python-r-complete | Python remains authoritative; verified R example fixture added. |
| `nns_rescale` | `pynns.central_tendencies` | `NNS.rescale` | exists intentionally unbound | yes | no | yes | no | python-r-complete | Do not route until risk-neutral and edge-case fixtures pass. |
| `nns_seas` | `pynns.seasonality` | `NNS.seas` | seasonality C++ exists unbound | yes | no | yes | no | blocked | Modulo behavior, periods, keys, and output order require exact fixtures before routing. |
| `nns_sd_cluster` | `pynns.stochastic_dominance` | `NNS.SD.cluster` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover clustering behavior. |
| `nns_stack` | `pynns.stack` | `NNS.stack` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover stacking behavior. |
| `nns_ss` | `pynns.stochastic_superiority` | `NNS.SS` | `stochastic_superiority` private helper | yes | yes | yes | partial | complete | Empirical native helper and public stochastic superiority behavior covered. |
| `nns_var` | `pynns.var` | `NNS.VaR` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover VaR behavior. |
| `prepare_factor_predictors` | `pynns.regression` | none | none | yes | n/a | n/a | n/a | python-only-complete | Python helper for public factor design preparation. |
| `sd_efficient_set` | `pynns.stochastic_dominance` | SD efficient-set behavior | exists unbound support | yes | no | yes | no | blocked | Dominance fixtures and index conventions must be complete before routing. |
| `skew_pm` | `pynns.classical` | PM skewness helper | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover public classical helper behavior. |
| `ssd` | `pynns.stochastic_dominance` | `SSD` | exists unbound | yes | no | yes | no | blocked | Matrix orientation and index-base fixtures must be complete before routing. |
| `ssd_uni` | `pynns.stochastic_dominance` | `SSD.uni` | exists unbound | yes | no | yes | no | blocked | Keep Python authoritative until dominance fixture suite is complete. |
| `tsd` | `pynns.stochastic_dominance` | `TSD` | exists unbound | yes | no | yes | no | blocked | Matrix orientation and index-base fixtures must be complete before routing. |
| `tsd_uni` | `pynns.stochastic_dominance` | `TSD.uni` | exists unbound | yes | no | yes | no | blocked | Keep Python authoritative until dominance fixture suite is complete. |
| `upm` | `pynns.core` | `UPM` | `upm`, `upm_v` | yes | yes | yes | partial | complete | Native-routed public API covered for degrees 0/1/2, scalar/vector targets, ties, zeros, signs, and empty input validation. |
| `upm_ratio` | `pynns.core` | `UPM.ratio` | `upm_ratio_v` | yes | yes | yes | partial | complete | Native-routed public API covered for degree and target variants. |
| `upm_var` | `pynns.var` | `UPM.VaR` | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover value-at-risk behavior. |
| `var_pm` | `pynns.classical` | PM variance helper | none | yes | n/a | yes | n/a | python-r-complete | Existing parity tests cover public classical helper behavior. |

## Private native binding status

| Private binding | Public route | Status | Notes |
|---|---|---|---|
| `lpm_v`, `upm_v`, `lpm_ratio_v`, `upm_ratio_v` | partial moments | complete | Direct native tests compare to vectorized Python formulas. |
| `co_lpm_v`, `co_upm_v`, `d_lpm_v`, `d_upm_v` | co-partial moments | complete | Direct native tests compare to Python formulas. |
| `clpm_nd`, `cupm_nd`, `dpm_nd`, `clpm_nd_batch` | dependence helpers | native-complete | Private binding formulas covered; public dependence routing remains blocked. |
| `fast_lm`, `fast_lm_mult` | regression helper only | native-complete | Native helper output covered; `nns_reg` remains Python authoritative. |
| `stochastic_superiority` | `nns_ss` empirical helper | complete | Native helper covered against direct probability formulas. |
| `gravity`, `mode` | central tendencies | complete | Public fallback/native parity covered. |
| `is_discrete`, `vec_sd`, `col_sd`, `factor_2_dummy`, `factor_2_dummy_fr`, `generate_vectors`, `generate_lin_vectors` | private backend helpers | native-complete | Direct binding smoke/parity tests added; not exposed as new top-level APIs. |
| `is_fcl`, `arma_seas_weighting`, `meboot_part`, `meboot_expand_sd`, `force_clt`, `up_sample`, `down_sample` | none | intentionally-out-of-scope | Audited but intentionally unbound pending dedicated contracts for stochastic/mutable/class-balancing behavior. |
