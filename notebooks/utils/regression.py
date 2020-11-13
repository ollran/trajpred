# pylint: disable=E0402

"""
Regression related prediction methods
"""

from numpy import array, ndarray, size
from scipy.stats import linregress
from .bullet import bullet_prediction


def predict_with_linear_regression(
        trajectory: ndarray,
        time: float
) -> ndarray:
    """
    Predict time interval with linear regression
    :param trajectory: target trajectory
    :param time: time in seconds
    :return: prediction
    """
    assert size(trajectory, 0) >= 2
    assert size(trajectory, 1) == 4
    assert time > 0

    tra_x, tra_y, ts, alt = trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], trajectory[:, 3]
    slope, intercept, _r_value, _p_value, _std_err = linregress(tra_y, tra_x)
    line = array(list(zip(intercept + slope * tra_y, tra_y, ts, alt)))
    return bullet_prediction(line, time)
