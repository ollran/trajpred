# pylint: disable=E0402

"""
Finding related functions
"""

from typing import List
from numpy import all, ndarray, size, where
from .distance import calculate_distance_in_meters


def find_closest_point(trajectory: ndarray, target_point: ndarray) -> ndarray:
    """
    Find the closest point to target_point from trajectory
    :param trajectory: trajectory
    :param target_point: target point
    :return: closest point
    """
    assert size(trajectory, 0) > 0
    assert size(trajectory, 1) == 4
    assert size(target_point, 0) == 4

    _minimum_distance, minimum_index = min(zip(map(
        lambda point: calculate_distance_in_meters(start=target_point, end=point),
        trajectory
    ), range(size(trajectory, 0))))
    return trajectory[minimum_index]


def find_trajectory_overlapping_trajectories(
        dataset_trajectories: List[ndarray],
        target_trajectory: ndarray,
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


def find_point_overlapping_trajectories(
        dataset_trajectories: List[ndarray],
        target_point: ndarray,
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


def find_target_point_indices(trajectory: ndarray, target_point: ndarray) -> ndarray:
    """
    Find target point indices from trajectory
    :param trajectory: trajectory
    :param target_point: target point
    :return: indices as ndarray
    """
    assert size(trajectory, 0) > 0
    assert size(trajectory, 1) == 4
    assert size(target_point, 0) == 4

    return where(all(
        trajectory == target_point,
        axis=1
    ))
