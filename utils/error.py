# pylint: disable=E0402

"""
Error calculation
"""

from numpy import array, ndarray, size
from .distance import calculate_distance_in_meters


def calculate_error(point: ndarray, prediction: ndarray) -> ndarray:
    """
    Calculates error between point and prediction
    :param point: original point
    :param prediction: predicted point
    :return: error
    """
    assert size(point, 0) == 4
    assert size(prediction, 0) == 4

    [point_lat, point_lon, point_ts, point_alt] = point
    [pred_lat, pred_lon, pred_ts, pred_alt] = prediction

    return array([
        point_lat - pred_lat,
        point_lon - pred_lon,
        point_ts - pred_ts,
        point_alt - pred_alt,
        calculate_distance_in_meters(
            start=point,
            end=prediction
        )
    ])


def calculate_error_vector(trajectory: ndarray, prediction: ndarray) -> ndarray:
    """
    Calculates error vector from trajectory and predicted trajectory
    :param trajectory: original trajectory
    :param prediction: predicted trajectory
    :return: error vector
    """
    assert size(trajectory, 0) > 0
    assert size(trajectory, 1) == 4
    assert size(prediction, 0) > 0
    assert size(prediction, 1) == 4

    return array([
        calculate_error(
            point=point,
            prediction=pred
        ) for point, pred in zip(
            trajectory,
            prediction
        )
    ])
