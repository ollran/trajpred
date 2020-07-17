"""
Trajectory distance related functions
"""

from functools import reduce
from math import radians
from typing import Tuple
from numpy import arcsin, cos, ndarray, sqrt, sin, size


def calculate_distance_in_meters(start: ndarray, end: ndarray) -> float:
    """
    Calculates the distance of two coordinates in meters
    :param start: start coordinate
    :param end: end coordinate
    :return: distance in meters
    """
    assert size(start, 0) == 4
    assert size(end, 0) == 4

    [lat_start, lon_start, _, _] = map(radians, start)
    [lat_end, lon_end, _, _] = map(radians, end)
    radius = 6371.0088  # km
    lat = lat_end - lat_start
    lon = lon_end - lon_start

    return 2 * radius * arcsin(sqrt(
        sin(lat * 0.5) ** 2 + cos(lat_start) * cos(lat_end) * sin(lon * 0.5) ** 2
    )) * 1000  # meters


def calculate_trajectory_length_in_meters(trajectory: ndarray) -> float:
    """
    Calculates the length of the trajectory in meters
    :param trajectory: trajectory
    :return: length in meters
    """
    assert size(trajectory, 0) >= 2
    assert size(trajectory, 1) == 4

    def reducer(acc: Tuple[float, ndarray], cur: ndarray) -> Tuple[float, ndarray]:
        distance, last_coordinate = acc
        current_distance = calculate_distance_in_meters(
            start=last_coordinate,
            end=cur
        )
        return distance + current_distance, cur

    total_distance, _ = reduce(
        reducer,
        trajectory[1:],
        (0.0, trajectory[0])
    )

    return total_distance
