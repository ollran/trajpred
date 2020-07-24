# pylint: disable=E0402

"""
Bullet prediction method
"""

from typing import List
from numpy import array, ndarray, size
from .speed import calculate_speed_in_ms
from .distance import calculate_distance_in_meters


def bullet_predict_next_coords(start: ndarray, end: ndarray, ratio: float = 1) -> ndarray:
    """
    Calculate next coords
    :param start: start coordinate
    :param end: end coordinate
    :param ratio: distance ratio
    :return: predicted coordinate
    """
    assert size(start, 0) == 4
    assert size(end, 0) == 4

    [lat_start, lon_start, ts_start, alt_start] = start
    [lat_end, lon_end, ts_end, alt_end] = end
    delta_lat = lat_end - lat_start
    delta_lon = lon_end - lon_start
    delta_ts = ts_end - ts_start
    delta_alt = alt_end - alt_start

    return array([
        lat_end + ratio * delta_lat,
        lon_end + ratio * delta_lon,
        ts_end + ratio * delta_ts,
        alt_end + ratio * delta_alt
    ])


def bullet_prediction(trajectory: ndarray, time: float) -> ndarray:
    """
    Predict time interval
    :param trajectory: trajectory that is used in prediction
    :param time: time to be predicted in seconds
    :return: predicted coordinates
    """
    assert size(trajectory, 0) >= 2
    assert size(trajectory, 1) == 4
    assert time > 0

    start, end = trajectory[-2], trajectory[-1]
    speed = calculate_speed_in_ms(
        start=start,
        end=end
    )
    distance = calculate_distance_in_meters(
        start=start,
        end=end
    )
    distance_to_predict = (time * speed) if distance > 0 else 0
    number_of_coordinates = max(int(distance_to_predict // distance) - 1, 1) \
        if distance > 0 else 0

    prediction: List[ndarray] = [end]
    for _ in range(number_of_coordinates):
        next_coordinate = bullet_predict_next_coords(
            start=start,
            end=end
        )
        prediction.append(next_coordinate)
        start = end
        end = next_coordinate

    return array(prediction)
