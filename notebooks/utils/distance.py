"""
Trajectory distance related functions
"""

from math import radians
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
