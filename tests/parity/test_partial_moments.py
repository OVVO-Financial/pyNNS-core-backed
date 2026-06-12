from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, cast

import numpy as np
import pytest
from _tolerances import COMPOUND, EXACT
from numpy.typing import NDArray

import pynns.co_moments as co_module
import pynns.core as core_module
import pynns.pm_matrix as pm_module
from pynns import co_lpm, co_upm, d_lpm, d_upm, lpm, lpm_ratio, pm_matrix, upm, upm_ratio
from pynns._native import nnscore

FIXTURE_PATH = Path(__file__).with_name("fixtures") / "partial_moments.json"


def _fixture() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(FIXTURE_PATH.read_text(encoding="utf-8")))


def _array(values: object) -> NDArray[np.float64]:
    return np.asarray(values, dtype=np.float64)


@pytest.mark.parity
@pytest.mark.parametrize("degree", [0, 1, 2])
@pytest.mark.parametrize(
    ("name", "function"),
    [
        ("lpm", lpm),
        ("upm", upm),
        ("lpm_ratio", lpm_ratio),
        ("upm_ratio", upm_ratio),
    ],
)
def test_partial_moment_python_outputs_match_committed_r_fixture(
    degree: int,
    name: str,
    function: Callable[
        [float, float | NDArray[np.float64], NDArray[np.float64]], float | NDArray[np.float64]
    ],
) -> None:
    fixture = _fixture()
    values = _array(fixture["values"])
    targets = _array(fixture["targets"])
    expected = _array(fixture["cases"][f"degree_{degree}"][name])

    actual = function(float(degree), targets, values)

    assert isinstance(actual, np.ndarray)
    assert actual.shape == expected.shape
    np.testing.assert_allclose(actual, expected, atol=EXACT)


@pytest.mark.parity
@pytest.mark.parametrize("degree", [0, 1, 2])
def test_scalar_partial_moment_target_shape_is_stable(degree: int) -> None:
    fixture = _fixture()
    values = _array(fixture["values"])

    actual = lpm(float(degree), 0.0, values)

    assert isinstance(actual, float)


@pytest.mark.parity
@pytest.mark.parametrize("function", [lpm, upm, lpm_ratio, upm_ratio])
def test_partial_moment_empty_input_validation(
    function: Callable[
        [float, float | NDArray[np.float64], NDArray[np.float64]], float | NDArray[np.float64]
    ],
) -> None:
    with pytest.raises(ValueError, match="non-empty"):
        function(1.0, 0.0, np.array([], dtype=np.float64))


@pytest.mark.parity
@pytest.mark.parametrize("degree", [0, 1, 2])
@pytest.mark.parametrize(
    ("name", "function"),
    [
        ("co_lpm", co_lpm),
        ("co_upm", co_upm),
        ("d_lpm", d_lpm),
        ("d_upm", d_upm),
    ],
)
def test_co_partial_moment_python_outputs_match_committed_r_fixture(
    degree: int,
    name: str,
    function: Callable[..., float | NDArray[np.float64]],
) -> None:
    fixture = _fixture()["co_values"]
    x = _array(fixture["x"])
    y = _array(fixture["y"])
    target_x = _array(fixture["target_x"])
    target_y = _array(fixture["target_y"])
    expected = _array(fixture[f"degree_{degree}"][name])

    if name in {"d_lpm", "d_upm"}:
        actual = function(float(degree), float(degree), x, y, target_x, target_y)
    else:
        actual = function(float(degree), x, y, target_x, target_y)

    assert isinstance(actual, np.ndarray)
    assert actual.shape == expected.shape
    np.testing.assert_allclose(actual, expected, atol=EXACT)


@pytest.mark.parity
@pytest.mark.parametrize("target", ["mean", 0.0, np.array([0.0, 0.5], dtype=np.float64)])
@pytest.mark.parametrize("pop_adj", [True, False])
@pytest.mark.parametrize("norm", [True, False])
def test_pm_matrix_shape_keys_and_orientation_are_stable(
    target: str | float | NDArray[np.float64], pop_adj: bool, norm: bool
) -> None:
    fixture = _fixture()
    values = _array(fixture["pm_matrix"]["variable"])

    actual = pm_matrix(2.0, 2.0, target, values, pop_adj=pop_adj, norm=norm)

    assert list(actual) == fixture["pm_matrix_keys"]
    for value in actual.values():
        assert value.shape == (2, 2)


@pytest.mark.parity
@pytest.mark.parametrize("pop_adj", [True, False])
@pytest.mark.parametrize("norm", [True, False])
def test_pm_matrix_native_matches_python_fallback_when_available(
    monkeypatch: pytest.MonkeyPatch, pop_adj: bool, norm: bool
) -> None:
    native = nnscore()
    if native is None:
        pytest.skip("pynns._nnscore is unavailable in this environment")

    fixture = _fixture()
    values = _array(fixture["pm_matrix"]["variable"])
    target = np.array([0.0, 0.5], dtype=np.float64)

    monkeypatch.setattr(pm_module, "nnscore", lambda: None)
    expected = pm_module.pm_matrix(2.0, 2.0, target, values, pop_adj=pop_adj, norm=norm)
    monkeypatch.setattr(pm_module, "nnscore", lambda: native)
    actual = pm_module.pm_matrix(2.0, 2.0, target, values, pop_adj=pop_adj, norm=norm)

    assert list(actual) == list(expected)
    for key in expected:
        np.testing.assert_allclose(actual[key], expected[key], atol=COMPOUND)


@pytest.mark.parity
@pytest.mark.parametrize("degree", [0, 1, 2])
def test_public_partial_moment_native_matches_python_fallback_when_available(
    monkeypatch: pytest.MonkeyPatch, degree: int
) -> None:
    native = nnscore()
    if native is None:
        pytest.skip("pynns._nnscore is unavailable in this environment")

    fixture = _fixture()
    values = _array(fixture["values"])
    targets = _array(fixture["targets"])

    monkeypatch.setattr(core_module, "nnscore", lambda: None)
    expected = {
        "lpm": core_module.lpm(float(degree), targets, values),
        "upm": core_module.upm(float(degree), targets, values),
        "lpm_ratio": core_module.lpm_ratio(float(degree), targets, values),
        "upm_ratio": core_module.upm_ratio(float(degree), targets, values),
    }
    monkeypatch.setattr(core_module, "nnscore", lambda: native)
    actual = {
        "lpm": core_module.lpm(float(degree), targets, values),
        "upm": core_module.upm(float(degree), targets, values),
        "lpm_ratio": core_module.lpm_ratio(float(degree), targets, values),
        "upm_ratio": core_module.upm_ratio(float(degree), targets, values),
    }

    for key, expected_value in expected.items():
        np.testing.assert_allclose(actual[key], expected_value, atol=COMPOUND)


@pytest.mark.parity
@pytest.mark.parametrize("degree", [0, 1, 2])
def test_public_co_partial_moment_native_matches_python_fallback_when_available(
    monkeypatch: pytest.MonkeyPatch, degree: int
) -> None:
    native = nnscore()
    if native is None:
        pytest.skip("pynns._nnscore is unavailable in this environment")

    fixture = _fixture()["co_values"]
    x = _array(fixture["x"])
    y = _array(fixture["y"])
    target_x = _array(fixture["target_x"])
    target_y = _array(fixture["target_y"])

    monkeypatch.setattr(co_module, "nnscore", lambda: None)
    expected = _co_results(float(degree), x, y, target_x, target_y)
    monkeypatch.setattr(co_module, "nnscore", lambda: native)
    actual = _co_results(float(degree), x, y, target_x, target_y)

    for key, expected_value in expected.items():
        np.testing.assert_allclose(actual[key], expected_value, atol=COMPOUND)


def _co_results(
    degree: float,
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    target_x: NDArray[np.float64],
    target_y: NDArray[np.float64],
) -> Mapping[str, float | NDArray[np.float64]]:
    return {
        "co_lpm": co_module.co_lpm(degree, x, y, target_x, target_y),
        "co_upm": co_module.co_upm(degree, x, y, target_x, target_y),
        "d_lpm": co_module.d_lpm(degree, degree, x, y, target_x, target_y),
        "d_upm": co_module.d_upm(degree, degree, x, y, target_x, target_y),
    }
