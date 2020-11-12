# pylint: disable=E0402,R0914

"""
Historical prediction method related functions
"""

from typing import List
from numpy import array, ndarray, row_stack, size
from numpy.random import choice
from .distance import calculate_distance_in_meters, calculate_trajectory_length_in_meters
from .find import find_point_overlapping_trajectories
from .ranking import rank_by_average_speed_similarity
from .speed import calculate_speed_in_ms
from .split import split_trajectories_from_closest_point_inclusively, split_trajectory_by_distance


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
    if len(overlapping_trajectories) == 0:
        return []
    split_trajectories = split_trajectories_from_closest_point_inclusively(
        trajectories=overlapping_trajectories,
        target_point=target_point
    )
    return list(map(lambda pair: pair[1], split_trajectories))


def generate_point_from_between_by_distance(
        start: ndarray,
        end: ndarray,
        distance: float
) -> ndarray:
    """
    Generate a coordinate point between 2 points by distance
    :param start: start coordinate
    :param end: end coordinate
    :param distance: distance in meters
    :return: generated coordinate point
    """
    assert size(start, 0) == 4
    assert size(end, 0) == 4
    assert distance > 0

    start_end_distance = calculate_distance_in_meters(
        start=start,
        end=end
    )
    ratio = (distance / start_end_distance) if start_end_distance > 0 else 0
    [lat_start, lon_start, ts_start, alt_start] = start
    [lat_end, lon_end, ts_end, alt_end] = end
    delta_lat = lat_end - lat_start
    delta_lon = lon_end - lon_start
    delta_ts = ts_end - ts_start
    delta_alt = alt_end - alt_start

    return array([
        lat_start + ratio * delta_lat,
        lon_start + ratio * delta_lon,
        ts_start + ratio * delta_ts,
        alt_start + ratio * delta_alt
    ])


def predict_by_picking_random_tail(
        dataset_trajectories: List[ndarray],
        trajectory: ndarray,
        time: float,
        threshold: float = 10
) -> ndarray:
    """
    Predict by picking random tail from the dataset
    :param dataset_trajectories: trajectories in the dataset (history)
    :param trajectory: target trajectory
    :param time: time in seconds
    :param threshold: threshold in meters
    :return: prediction
    """
    assert len(dataset_trajectories) > 0
    assert size(trajectory, 0) >= 2
    assert size(trajectory, 1) == 4
    assert time > 0
    assert threshold > 0

    base_case = array([[]])
    start, end = trajectory[-2], trajectory[-1]
    tails = construct_potential_tails(
        dataset_trajectories=dataset_trajectories,
        target_point=end,
        threshold=threshold
    )
    if len(tails) == 0:
        return base_case
    random_tail = choice(tails) if len(tails) > 1 else tails[0]
    speed = calculate_speed_in_ms(
        start=start,
        end=end
    )
    distance_to_predict = time * speed
    if distance_to_predict <= 0:
        return base_case
    if size(random_tail, 0) == 1:
        return random_tail

    prediction, rest = split_trajectory_by_distance(
        trajectory=random_tail,
        distance=distance_to_predict
    )
    predicted_distance = calculate_trajectory_length_in_meters(
        trajectory=prediction
    )
    remaining_distance_to_predict = distance_to_predict - predicted_distance
    if remaining_distance_to_predict > 0 and size(rest, 0) > 0 and size(rest, 1) == 4:
        remaining_point = generate_point_from_between_by_distance(
            start=prediction[-1],
            end=rest[0],
            distance=remaining_distance_to_predict
        )
        return row_stack((prediction, remaining_point))
    return prediction


def predict_by_picking_tail_with_similar_speed(
        dataset_trajectories: List[ndarray],
        trajectory: ndarray,
        time: float,
        threshold: float = 10
) -> ndarray:
    """
    Predict by ranking tails in the dataset and picking the one with most similar speed
    :param dataset_trajectories: trajectory history
    :param trajectory: target trajectory
    :param time: time in seconds
    :param threshold: threshold in meters
    :return: prediction
    """
    assert len(dataset_trajectories) > 0
    assert size(trajectory, 0) >= 2
    assert size(trajectory, 1) == 4
    assert time > 0
    assert threshold > 0

    base_case = array([[]])
    start, end = trajectory[-2], trajectory[-1]
    tails = construct_potential_tails(
        dataset_trajectories=dataset_trajectories,
        target_point=end,
        threshold=threshold
    )
    # Filter short tails from predictions
    filtered_tails = list(filter(
        lambda tail: len(tail) >= 2,
        tails
    ))
    if len(filtered_tails) == 0:
        return base_case

    ranked = rank_by_average_speed_similarity(
        trajectory=trajectory,
        tails=filtered_tails
    )
    if len(ranked) == 0:
        return base_case
    target = ranked[0]

    speed = calculate_speed_in_ms(
        start=start,
        end=end
    )
    distance_to_predict = time * speed
    if distance_to_predict <= 0:
        return base_case
    if size(target, 0) == 1:
        return target

    prediction, rest = split_trajectory_by_distance(
        trajectory=target,
        distance=distance_to_predict
    )
    predicted_distance = calculate_trajectory_length_in_meters(
        trajectory=prediction
    )
    remaining_distance_to_predict = distance_to_predict - predicted_distance
    if remaining_distance_to_predict > 0 and size(rest, 0) > 0 and size(rest, 1) == 4:
        remaining_point = generate_point_from_between_by_distance(
            start=prediction[-1],
            end=rest[0],
            distance=remaining_distance_to_predict
        )
        return row_stack((prediction, remaining_point))
    return prediction
