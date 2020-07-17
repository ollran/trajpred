# pylint: disable=E0402

"""
Bullet prediction method
"""

from functools import reduce
from typing import List
from numpy import append, array, expand_dims, ndarray, size
from .speed import calculate_speed_in_ms
from .distance import calculate_distance_in_meters


def bullet_predict_next_coords(start: ndarray, end: ndarray, ratio: float) -> ndarray:
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
    prediction_distance = time * speed
    number_of_coordinates = int(prediction_distance // distance) if distance > 0 else 0
    last_coordinate_distance_ratio = (1 + prediction_distance % distance / distance) if distance > 0 else 0
    r = (distance / prediction_distance) if prediction_distance > 0 else 0
    ratio = 1 + r if r > 0 else -1 + r

    def reducer(acc: List[ndarray], _: int) -> List[ndarray]:
        [head, tail] = acc[-2:]
        return list(
            acc + [bullet_predict_next_coords(
                start=head,
                end=tail,
                ratio=ratio
            )]
        )

    prediction = array(reduce(
        reducer,
        range(number_of_coordinates),
        [end, bullet_predict_next_coords(
            start=start,
            end=end,
            ratio=ratio
        )]
    ))

    return append(prediction, expand_dims(bullet_predict_next_coords(
        start=prediction[-2],
        end=prediction[-1],
        ratio=last_coordinate_distance_ratio
    ), 0), axis=0)
