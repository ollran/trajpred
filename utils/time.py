"""
Time related functions
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from numpy import ndarray, size


def calculate_daytime_difference(
        start: ndarray,
        end: ndarray
) -> float:
    """
    Calculates daytime difference between two coordinates.
    :param start: start coordinate
    :param end: end coordinate
    :return: daytime difference in milliseconds
    """
    assert size(start, 0) == 4
    assert size(end, 0) == 4

    [_, _, ts_start, _] = start
    [_, _, ts_end, _] = end
    date_start = datetime.fromtimestamp(ts_start // 1000)
    date_end = datetime.fromtimestamp(ts_end // 1000)
    delta = relativedelta(date_start, date_end)

    return abs(delta.hours) * 3600000 + abs(delta.minutes) * 60000 + abs(delta.seconds) * 1000
