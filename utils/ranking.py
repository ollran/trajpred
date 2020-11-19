# pylint: disable=E0402

"""
Trajectory ranking related functions
"""

from typing import List
from numpy import ndarray, size
from .speed import calculate_average_speed_in_ms
from .time import calculate_daytime_difference


def rank_by_average_speed_similarity(
        trajectory: ndarray,
        tails: List[ndarray]
) -> List[ndarray]:
    """
    Rank tails in ascending order by the average speed difference
    :param trajectory: base trajectory
    :param tails: list of possible tails
    :return: ranked tails in ascending order
    """
    assert size(trajectory, 0) >= 2
    assert size(trajectory, 1) == 4
    assert len(tails) > 0

    trajectory_average_speed = calculate_average_speed_in_ms(
        trajectory=trajectory
    )
    tails_with_average_speeds = list(map(
        lambda tail: (calculate_average_speed_in_ms(
            trajectory=tail
        ), tail),
        tails
    ))
    tails_with_speed_difference = list(map(
        lambda pair: (abs(trajectory_average_speed - pair[0]), pair[1]),
        tails_with_average_speeds
    ))

    return list(map(
        lambda sorted_pair: sorted_pair[1],
        sorted(
            tails_with_speed_difference,
            key=lambda pair: pair[0]
        )
    ))


def rank_by_time_of_day_similarity(
        trajectory: ndarray,
        tails: List[ndarray]
) -> List[ndarray]:
    """
    Rank tails in ascending order by the time of the day similarity
    :param trajectory: base trajectory
    :param tails: list of possible tails
    :return: ranked tails in ascending order
    """
    assert size(trajectory, 0) >= 2
    assert size(trajectory, 1) == 4
    assert len(tails) > 0

    trajectory_start_coordinate = trajectory[0]
    tails_with_start_coordinate = list(map(
        lambda tail: (tail[0], tail),
        tails
    ))
    tails_with_daytime_difference = list(map(
        lambda pair: (calculate_daytime_difference(pair[0], trajectory_start_coordinate), pair[1]),
        tails_with_start_coordinate
    ))

    return list(map(
        lambda sorted_pair: sorted_pair[1],
        sorted(
            tails_with_daytime_difference,
            key=lambda pair: pair[0]
        )
    ))
