# pylint: disable=E0402

"""
Speed related functions
"""

from numpy import average, ndarray, size
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


def calculate_average_speed_in_ms(trajectory: ndarray) -> float:
    """
    Calculate the average speed of the trajectory in m/s
    :param trajectory: target trajectory
    :return:  average speed in m/s
    """
    assert size(trajectory, 0) >= 2
    assert size(trajectory, 1) == 4

    return average(list(map(
        lambda pair: calculate_speed_in_ms(start=pair[0], end=pair[1]),
        zip(list(trajectory), list(trajectory[1:]))
    )))
