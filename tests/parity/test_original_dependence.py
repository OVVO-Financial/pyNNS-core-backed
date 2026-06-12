from __future__ import annotations

import pytest

from pynns import nns_copula

from ._original import expected, r_vector


@pytest.mark.parity
def test_original_bivariate_copula_continuous_matches_r_fixture() -> None:
    x = r_vector("test_Copula.R", "x")
    y = r_vector("test_Copula.R", "y")
    exp = expected("test_Copula.R")

    assert nns_copula(x, y) == pytest.approx(exp["bivariate_continuous"], abs=1e-5)


@pytest.mark.parity
def test_original_copula_discrete_and_multivariate_are_documented_gaps() -> None:
    exp = expected("test_Copula.R")
    assert exp["bivariate_discrete"] == pytest.approx(0.4472136, abs=1e-7)
    assert exp["multivariate_continuous"] == pytest.approx(0.2519783, abs=1e-7)
    assert exp["multivariate_discrete"] == pytest.approx(0.2725541, abs=1e-7)
