from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import numpy as np
import pytest
from _tolerances import COMPOUND

import pynns._helpers as helpers_module
from pynns import nns_reg
from pynns._helpers import _fast_lm
from pynns._native import nnscore

FIXTURE_PATH = Path(__file__).with_name("fixtures") / "regression.json"


def _fixture() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(FIXTURE_PATH.read_text(encoding="utf-8")))


@pytest.mark.parity
def test_fast_lm_helper_native_matches_python_fallback_when_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    native = nnscore()
    if native is None:
        pytest.skip("pynns._nnscore is unavailable in this environment")

    x = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    y = np.array([2.0, 4.0, 6.0, 8.0], dtype=np.float64)

    monkeypatch.setattr(helpers_module, "nnscore", lambda: None)
    expected = helpers_module._fast_lm(x, y)
    monkeypatch.setattr(helpers_module, "nnscore", lambda: native)
    actual = helpers_module._fast_lm(x, y)

    assert actual == pytest.approx(expected, abs=COMPOUND)


@pytest.mark.parity
def test_fast_lm_helper_python_fallback_handles_repeated_x() -> None:
    intercept, slope = _fast_lm(
        np.array([1.0, 1.0, 1.0], dtype=np.float64),
        np.array([2.0, 3.0, 4.0], dtype=np.float64),
    )

    assert intercept == pytest.approx(3.0, abs=COMPOUND)
    assert slope == pytest.approx(0.0, abs=COMPOUND)


@pytest.mark.parity
def test_nns_reg_verified_example_matches_committed_r_fixture() -> None:
    expected = _fixture()["verified_example"]
    x = np.asarray(expected["x"], dtype=np.float64)
    y = np.asarray(expected["y"], dtype=np.float64)
    point_est = np.asarray(expected["point_est"], dtype=np.float64)

    actual = nns_reg(x, y, point_est=point_est)

    assert actual["R2"] == pytest.approx(float(expected["R2"]), abs=5e-2)
    assert actual["SE"] == pytest.approx(float(expected["SE"]), abs=5e-2)
    np.testing.assert_allclose(
        actual["Point.est"], np.asarray(expected["Point.est"], dtype=np.float64), atol=5e-2
    )


@pytest.mark.parity
@pytest.mark.parametrize(
    ("x", "y", "points"),
    [
        ([1, 2, 3, 4], [1, 2, 3, 4], [0.0, 2.5, 5.0]),
        ([1, 2, 3, 4, 5], [1, 4, 2, 5, 3], [1.5, 3.5, 6.0]),
        ([1, 1, 2, 3, 4], [1, 1.2, 2.1, 2.9, 4.2], [1.0, 2.5, 5.0]),
    ],
)
def test_nns_reg_additional_shape_parity_samples(
    x: list[float], y: list[float], points: list[float]
) -> None:
    point_est = np.asarray(points, dtype=np.float64)

    actual = nns_reg(
        np.asarray(x, dtype=np.float64),
        np.asarray(y, dtype=np.float64),
        point_est=point_est,
    )

    assert set(actual) >= {"R2", "SE", "Point.est"}
    assert np.asarray(actual["Point.est"]).shape == point_est.shape
    assert float(actual["SE"]) >= 0.0
