"""
Trajectory splitting related functions
"""

from typing import List, Tuple
from numpy import ndarray, size


def split_trajectory(trajectory: ndarray, ratio: float) -> Tuple[ndarray, ndarray]:
    """
    Splits trajectory by ratio
    :param trajectory: trajectory as ndarray
    :param ratio: ratio between 0.0 and 1.0
    :return: tuple containing both parts of the trajectory (train, test)
    """
    assert size(trajectory, 0) > 0
    assert size(trajectory, 1) == 4
    assert ratio >= 0.0
    assert ratio <= 1.0

    ratio_as_index = round(ratio * size(trajectory, 0))
    return trajectory[:ratio_as_index], trajectory[ratio_as_index:]


def split_trajectories(trajectories: List[ndarray], ratio: float) -> List[Tuple[ndarray, ndarray]]:
    """
    Splits trajectories by ratio
    :param trajectories: list of trajectories as ndarrays
    :param ratio: ratio between 0.0 and 1.0
    :return: list of split trajectories
    """
    assert len(trajectories) > 0
    assert ratio >= 0.0
    assert ratio <= 1.0

    return [
        split_trajectory(
            trajectory=trajectory,
            ratio=ratio
        ) for trajectory in trajectories
    ]
