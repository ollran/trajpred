# pylint: disable=E0402

"""
Historical prediction method related functions
"""

from itertools import chain
from typing import List
from numpy import ndarray, size
from .find import find_point_overlapping_trajectories
from .split import split_trajectories_from_closest_point_inclusively


def construct_potential_tails(
        dataset_trajectories: List[ndarray],
        target_point: ndarray,
        threshold: float = 10
) -> List[ndarray]:
    """
    Construct a list of potential tails
    :param dataset_trajectories: list of trajectories to use
    :param target_point: target point
    :param threshold: threshold in meters (default 10 meters)
    :return: list of potential tail trajectories
    """
    assert len(dataset_trajectories) > 0
    assert size(target_point, 0) == 4

    overlapping_trajectories = find_point_overlapping_trajectories(
        dataset_trajectories=dataset_trajectories,
        target_point=target_point,
        threshold=threshold
    )
    split_trajectories = split_trajectories_from_closest_point_inclusively(
        trajectories=overlapping_trajectories,
        target_point=target_point
    )
    return list(chain(*map(
        lambda pair: [pair[0], pair[1]],
        split_trajectories
    )))
