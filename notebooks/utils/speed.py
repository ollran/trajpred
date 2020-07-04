# pylint: disable=E0402

"""
Speed related functions
"""

from numpy import ndarray, size
from .distance import calculate_distance_in_meters


def calculate_speed_in_ms(start: ndarray, end: ndarray) -> float:
    """
    Calculate speed between 2 adjacent coordinates
    :param start: start coordinate
    :param end: end coordinate
    :return: speed m/s
    """
    assert size(start, 0) == 4
    assert size(end, 0) == 4

    [_, _, ts_start, _] = start
    [_, _, ts_end, _] = end
    time = (ts_end - ts_start) / 1000  # ms -> s

    return (calculate_distance_in_meters(
        start=start,
        end=end
    ) / time) if time > 0 else 0
