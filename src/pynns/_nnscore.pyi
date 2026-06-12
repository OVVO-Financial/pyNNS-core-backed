from collections.abc import Sequence
from typing import TypedDict

import numpy as np
from numpy.typing import NDArray

class FastLmResult(TypedDict):
    coef: Sequence[float]
    fitted_values: Sequence[float]
    residuals: Sequence[float]
    df_residual: int

class StochSupResult(TypedDict):
    p_gt: float
    p_tie: float
    p_star: float

def lpm(
    degree: float,
    target: float | NDArray[np.float64],
    x: Sequence[float] | NDArray[np.float64],
) -> float | Sequence[float]: ...
def upm(
    degree: float,
    target: float | NDArray[np.float64],
    x: Sequence[float] | NDArray[np.float64],
) -> float | Sequence[float]: ...
def gravity(x: NDArray[np.float64], discrete: bool) -> float: ...
def mode(x: NDArray[np.float64], discrete: bool, multi: bool) -> Sequence[float]: ...
def fast_lm(x: NDArray[np.float64], y: NDArray[np.float64]) -> FastLmResult: ...
def stochastic_superiority(x: NDArray[np.float64], y: NDArray[np.float64]) -> StochSupResult: ...
