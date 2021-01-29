"""
Outputting related functions
"""

from typing import List
from numpy import ndarray, size

RESULT_DIRECTORY = './results'


def output_coordinates_to_file(filename: str, results: ndarray) -> None:
    """
    Output results to a file
    :param filename: filename as string
    :param results: results as ndarray
    :return: None
    """
    assert len(filename) > 0
    assert size(results, 0) > 0
    assert size(results, 1) == 4

    with open(filename, 'w') as file:
        for line in results:
            [lat, lon, _, _] = line
            file.write(f'{lat},{lon}\n')


def output_all_coordinates_to_file(filename: str, *results: List[ndarray]) -> None:
    """
    Output all results to a single file
    :param filename: filename as string
    :param results: results as ndarray
    :return: None
    """
    assert len(filename) > 0
    assert len(results) > 0

    with open(filename, 'w') as file:
        for result in results:
            for line in result:
                [lat, lon, _, _] = line
                file.write(f'{lat},{lon}\n')
            file.write('---\n')


def get_result_filename(
        user_id: int,
        trajectory_id: int,
        ratio: int,
        method: str,
        prediction_time: int,
) -> str:
    """
    Create a result filename as a string
    :param user_id: User id
    :param trajectory_id: Trajectory id
    :param ratio: Split ratio
    :param method: Prediction method
    :param prediction_time: Prediction time
    :return: Result filename string
    """
    assert user_id > 0
    assert trajectory_id > 0
    assert ratio >= 0.0
    assert ratio <= 1.0
    assert method
    assert prediction_time > 0

    return f'{RESULT_DIRECTORY}/{user_id}_{trajectory_id}_{ratio}_{method}_{prediction_time}.txt'
