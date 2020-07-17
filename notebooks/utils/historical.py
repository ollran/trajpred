# pylint: disable=E0402

"""
Historical prediction method related functions
"""

# from itertools import chain
from typing import List
from numpy import array, ndarray, row_stack, size
from numpy.random import choice
from .distance import calculate_distance_in_meters, calculate_trajectory_length_in_meters
from .find import find_point_overlapping_trajectories
from .speed import calculate_speed_in_ms, calculate_average_speed_in_ms
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
    split_trajectories = split_trajectories_from_closest_point_inclusively(
        trajectories=overlapping_trajectories,
        target_point=target_point
    )
    return list(map(lambda pair: pair[1], split_trajectories))
    # heads + tails
    # return list(chain(*map(
    #    lambda pair: [pair[0], pair[1]],
    #    split_trajectories
    # )))


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
    ratio = distance / start_end_distance
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
    :param dataset_trajectories:
    :param trajectory:
    :param time:
    :param threshold:
    :return:
    """
    assert len(dataset_trajectories) > 0
    assert size(trajectory, 0) >= 2
    assert size(trajectory, 1) == 4
    assert time > 0
    assert threshold > 0

    start, end = trajectory[-2], trajectory[-1]
    tails = construct_potential_tails(
        dataset_trajectories=dataset_trajectories,
        target_point=end,
        threshold=threshold
    )
    random_tail = choice(tails)
    speed = calculate_speed_in_ms(
        start=start,
        end=end
    )
    distance_to_predict = (time * speed) if speed > 0 else (time * calculate_average_speed_in_ms(
        trajectory=trajectory
    ))
    prediction, rest = split_trajectory_by_distance(
        trajectory=random_tail,
        distance=distance_to_predict
    )

    predicted_distance = calculate_trajectory_length_in_meters(
        trajectory=prediction
    )
    remaining_distance_to_predict = distance_to_predict - predicted_distance
    remaining_point = generate_point_from_between_by_distance(
        start=prediction[-1],
        end=rest[0],
        distance=remaining_distance_to_predict
    )
    return row_stack((prediction, remaining_point))
