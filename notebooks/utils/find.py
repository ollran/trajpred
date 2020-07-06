# pylint: disable=E0402

"""
Finding related functions
"""

from numpy import ndarray, size
from .distance import calculate_distance_in_meters


def find_closest_point(trajectory: ndarray, target_point: ndarray) -> ndarray:
    """
    Find the closest point to target_point from trajectory
    :param trajectory: trajectory
    :param target_point: target point
    :return: closest point
    """
    assert size(trajectory, 0) > 0
    assert size(trajectory, 1) == 4
    assert size(target_point, 0) == 4

    _min_distance, closest_point = min(zip(map(
        lambda point: calculate_distance_in_meters(start=target_point, end=point),
        trajectory
    ), trajectory))
    return closest_point
