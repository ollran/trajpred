# pylint: disable=E0402

"""
History prediction method related functions
"""

from typing import List
from numpy import ndarray, size
from .distance import calculate_distance_in_meters


def find_trajectory_overlapping_trajectories_from_history(
        target_trajectory: ndarray,
        dataset_trajectories: List[ndarray],
        threshold: float
) -> List[ndarray]:
    """
    Find trajectories from history that have overlaps with target trajectory
    :param target_trajectory: target trajectory
    :param dataset_trajectories: list of trajectories to compare to
    :param threshold: distance threshold in meters
    :return: list of trajectories with overlaps
    """
    assert size(target_trajectory, 0) > 0
    assert size(target_trajectory, 1) == 4
    assert len(dataset_trajectories) > 0
    assert threshold > 0

    matches: List[ndarray] = []
    for dataset_trajectory in dataset_trajectories:
        match = False
        for dataset_trajectory_point in dataset_trajectory:
            for target_point in target_trajectory:
                distance = calculate_distance_in_meters(
                    start=dataset_trajectory_point,
                    end=target_point
                )
                if distance <= threshold:
                    matches.append(dataset_trajectory)
                    match = True
                    break
            if match:
                break
    return matches


def find_point_overlapping_trajectories_from_history(
        target_point: ndarray,
        dataset_trajectories: List[ndarray],
        threshold: float
) -> List[ndarray]:
    """
    Find trajectories from history that have overlaps with target point
    :param target_point: target coordinate point
    :param dataset_trajectories: list of trajectories to compare to
    :param threshold: distance threshold in meters
    :return: list of trajectories with overlaps
    """
    assert size(target_point, 0) == 4
    assert len(dataset_trajectories) > 0
    assert threshold > 0

    matches: List[ndarray] = []
    for dataset_trajectory in dataset_trajectories:
        for dataset_trajectory_point in dataset_trajectory:
            distance = calculate_distance_in_meters(
                start=dataset_trajectory_point,
                end=target_point
            )
            if distance <= threshold:
                matches.append(dataset_trajectory)
                break
    return matches
