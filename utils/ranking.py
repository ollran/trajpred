# pylint: disable=E0402

"""
Trajectory ranking related functions
"""

from typing import List
from numpy import ndarray, size
from .speed import calculate_average_speed_in_ms


def rank_by_average_speed_similarity(trajectory: ndarray, tails: List[ndarray]) -> List[ndarray]:
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
