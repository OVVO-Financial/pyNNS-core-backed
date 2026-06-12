from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import numpy as np
import pytest
from _tolerances import COMPOUND

import pynns.central_tendencies as central_module
from pynns import nns_gravity, nns_mode, nns_rescale
from pynns._native import nnscore

FIXTURE_PATH = Path(__file__).with_name("fixtures") / "central_tendencies.json"


def _fixture() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(FIXTURE_PATH.read_text(encoding="utf-8")))


@pytest.mark.parity
def test_central_tendency_python_outputs_match_committed_r_fixture() -> None:
    fixture = _fixture()
    ties = np.asarray(fixture["samples"]["ties"], dtype=np.float64)
    mixed = np.asarray(fixture["samples"]["mixed"], dtype=np.float64)

    np.testing.assert_allclose(
        nns_mode(ties, discrete=True, multi=True),
        np.asarray(fixture["mode_discrete_multi"], dtype=np.float64),
        atol=COMPOUND,
    )
    assert nns_mode(ties, discrete=True, multi=False) == pytest.approx(
        float(fixture["mode_discrete_single"]), abs=COMPOUND
    )
    assert nns_mode(mixed, discrete=False, multi=False) == pytest.approx(
        float(fixture["mode_continuous_single_mixed"]), abs=COMPOUND
    )
    assert nns_gravity(mixed) == pytest.approx(float(fixture["gravity_mixed"]), abs=COMPOUND)
    np.testing.assert_allclose(
        nns_rescale(mixed, 0.0, 1.0),
        np.asarray(fixture["rescale_mixed_unit"], dtype=np.float64),
        atol=COMPOUND,
    )


@pytest.mark.parity
def test_central_tendency_native_matches_python_fallback_when_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    native = nnscore()
    if native is None:
        pytest.skip("pynns._nnscore is unavailable in this environment")

    mixed = np.asarray(_fixture()["samples"]["mixed"], dtype=np.float64)

    monkeypatch.setattr(central_module, "nnscore", lambda: None)
    expected_gravity = central_module.nns_gravity(mixed)
    expected_mode = central_module.nns_mode(mixed, discrete=False, multi=False)

    monkeypatch.setattr(central_module, "nnscore", lambda: native)
    assert central_module.nns_gravity(mixed) == pytest.approx(expected_gravity, abs=COMPOUND)
    assert central_module.nns_mode(mixed, discrete=False, multi=False) == pytest.approx(
        expected_mode, abs=COMPOUND
    )
