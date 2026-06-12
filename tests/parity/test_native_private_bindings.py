from __future__ import annotations

from typing import Any

import numpy as np
import pytest
from _tolerances import COMPOUND
from numpy.typing import NDArray

from pynns._native import nnscore


def _native() -> Any:
    native = nnscore()
    if native is None:
        pytest.skip("pynns._nnscore is unavailable in this environment")
    return native


@pytest.mark.parity
def test_private_partial_moment_vector_bindings_match_python_formula() -> None:
    native = _native()
    x = np.array([-2.0, -1.0, 0.0, 0.0, 1.5, 3.0], dtype=np.float64)
    target = np.array([-1.0, 0.0, 2.0], dtype=np.float64)

    lower = np.mean(np.maximum(0.0, target[:, np.newaxis] - x) ** 2.0, axis=1)
    upper = np.mean(np.maximum(0.0, x - target[:, np.newaxis]) ** 2.0, axis=1)
    total = lower + upper

    np.testing.assert_allclose(native.lpm_v(2.0, target, x), lower, atol=COMPOUND)
    np.testing.assert_allclose(native.upm_v(2.0, target, x), upper, atol=COMPOUND)
    np.testing.assert_allclose(native.lpm_ratio_v(2.0, target, x), lower / total, atol=COMPOUND)
    np.testing.assert_allclose(native.upm_ratio_v(2.0, target, x), upper / total, atol=COMPOUND)


@pytest.mark.parity
def test_private_co_partial_moment_vector_bindings_match_python_formula() -> None:
    native = _native()
    x = np.array([-2.0, -1.0, 0.0, 0.0, 1.5, 3.0], dtype=np.float64)
    y = np.array([3.0, 1.0, 0.0, 0.0, -1.0, -2.0], dtype=np.float64)
    target_x = np.array([-1.0, 0.0, 2.0], dtype=np.float64)
    target_y = np.array([0.0, 0.5, -0.5], dtype=np.float64)

    lower_x = np.maximum(0.0, target_x[:, np.newaxis] - x) ** 2.0
    upper_x = np.maximum(0.0, x - target_x[:, np.newaxis]) ** 2.0
    lower_y = np.maximum(0.0, target_y[:, np.newaxis] - y) ** 2.0
    upper_y = np.maximum(0.0, y - target_y[:, np.newaxis]) ** 2.0

    np.testing.assert_allclose(
        native.co_lpm_v(2.0, 2.0, x, y, target_x, target_y),
        _rows_mean(lower_x, lower_y),
        atol=COMPOUND,
    )
    np.testing.assert_allclose(
        native.co_upm_v(2.0, 2.0, x, y, target_x, target_y),
        _rows_mean(upper_x, upper_y),
        atol=COMPOUND,
    )
    np.testing.assert_allclose(
        native.d_lpm_v(2.0, 2.0, x, y, target_x, target_y),
        _rows_mean(upper_x, lower_y),
        atol=COMPOUND,
    )
    np.testing.assert_allclose(
        native.d_upm_v(2.0, 2.0, x, y, target_x, target_y),
        _rows_mean(lower_x, upper_y),
        atol=COMPOUND,
    )


def _rows_mean(left: NDArray[np.float64], right: NDArray[np.float64]) -> NDArray[np.float64]:
    return np.mean(left * right, axis=1)


@pytest.mark.parity
def test_private_nd_partial_moment_bindings_match_python_formula() -> None:
    native = _native()
    values = np.array(
        [[-2.0, 3.0], [-1.0, 1.0], [0.0, 0.0], [0.0, 0.0], [1.5, -1.0], [3.0, -2.0]],
        dtype=np.float64,
    )
    target = np.array([0.0, 0.5], dtype=np.float64)
    flat = np.ravel(values, order="F")
    lower = np.maximum(0.0, target[np.newaxis, :] - values) ** 2.0
    upper = np.maximum(0.0, values - target[np.newaxis, :]) ** 2.0

    expected_clpm = float(np.mean(np.prod(lower, axis=1)))
    expected_cupm = float(np.mean(np.prod(upper, axis=1)))
    expected_dpm = float(np.mean(np.prod(np.abs(values - target[np.newaxis, :]) ** 2.0, axis=1)))

    assert native.clpm_nd(
        flat, values.shape[0], values.shape[1], target, 2.0, False
    ) == pytest.approx(expected_clpm, abs=COMPOUND)
    assert native.cupm_nd(
        flat, values.shape[0], values.shape[1], target, 2.0, False
    ) == pytest.approx(expected_cupm, abs=COMPOUND)
    assert native.dpm_nd(
        flat, values.shape[0], values.shape[1], target, 2.0, False
    ) == pytest.approx(expected_dpm, abs=COMPOUND)
    np.testing.assert_allclose(
        native.clpm_nd_batch(
            flat, values.shape[0], values.shape[1], np.tile(target, 2), 2, 2.0, False
        ),
        np.array([expected_clpm, expected_clpm], dtype=np.float64),
        atol=COMPOUND,
    )


@pytest.mark.parity
def test_private_fast_lm_bindings_return_expected_shapes() -> None:
    native = _native()
    x = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    y = np.array([2.0, 4.0, 6.0, 8.0], dtype=np.float64)
    result = native.fast_lm(x, y)

    np.testing.assert_allclose(result["coef"], np.array([0.0, 2.0]), atol=COMPOUND)
    np.testing.assert_allclose(result["fitted_values"], y, atol=COMPOUND)
    np.testing.assert_allclose(result["residuals"], np.zeros_like(y), atol=COMPOUND)
    assert result["df_residual"] == 2

    design = np.column_stack([np.ones_like(x), x])
    mult = native.fast_lm_mult(np.ravel(design, order="F"), y, design.shape[0], design.shape[1])
    np.testing.assert_allclose(mult["coefficients"], np.array([0.0, 2.0]), atol=COMPOUND)
    np.testing.assert_allclose(mult["fitted_values"], y, atol=COMPOUND)


@pytest.mark.parity
def test_private_internal_function_bindings_return_stable_payloads() -> None:
    native = _native()
    values = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    matrix = np.array([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]], dtype=np.float64)

    assert native.is_discrete(values)
    assert native.vec_sd(values) == pytest.approx(float(np.std(values, ddof=1)), abs=COMPOUND)
    np.testing.assert_allclose(
        native.col_sd(np.ravel(matrix, order="F"), 3, 2),
        np.std(matrix, axis=0, ddof=1),
        atol=COMPOUND,
    )

    dummy = native.factor_2_dummy([2, 1, 2], ["A", "B"])
    assert dummy["names"] == ["B"]
    assert dummy["nrow"] == 3
    assert dummy["ncol"] == 1
    np.testing.assert_allclose(dummy["data"], np.array([1.0, 0.0, 1.0]), atol=COMPOUND)

    full_rank = native.factor_2_dummy_fr([2, 1, 2], ["A", "B"])
    assert full_rank["names"] == ["A", "B"]
    assert full_rank["nrow"] == 3
    assert full_rank["ncol"] == 2

    lagged = native.generate_vectors(values, np.array([1, 2], dtype=np.int32))
    assert set(lagged) == {"series", "index"}
    linear = native.generate_lin_vectors(values, 2, 1)
    assert set(linear) == {"series", "index", "forecast_values", "forecast_index"}


@pytest.mark.parity
def test_private_stochastic_superiority_binding_matches_python_formula() -> None:
    native = _native()
    x = np.array([1.0, 2.0, 2.0, 4.0], dtype=np.float64)
    y = np.array([2.0, 3.0], dtype=np.float64)

    result = native.stochastic_superiority(x, y)

    assert result["p_gt"] == pytest.approx(0.125, abs=COMPOUND)
    assert result["p_tie"] == pytest.approx(0.25, abs=COMPOUND)
    assert result["p_star"] == pytest.approx(0.25, abs=COMPOUND)
