"""
Trajectory direction related functions
"""

from numpy import arctan2, ndarray, size


def calculate_angle_in_radians(start: ndarray, end: ndarray) -> float:
    """
    Calculate the angle of two coordinates in radians
    :param start: start coordinate
    :param end: end coordinate
    :return: angle in radians
    """
    assert size(start, 0) == 4
    assert size(end, 0) == 4

    [lat_start, lon_start, _, _] = start
    [lat_end, lon_end, _, _] = end

    return arctan2(lat_end - lat_start, lon_end - lon_start)
