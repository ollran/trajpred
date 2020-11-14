# pylint: disable=E0402, R0913, R0914

"""
Report generating functions
"""

from itertools import repeat
from multiprocessing import Pool
from typing import Dict, List, Tuple, Union
from numpy import average, median, std, size
from .bullet import bullet_prediction
from .dataset import get_list_of_user_ids, get_list_of_users_trajectory_ids, \
    load_users_trajectories_with_target
from .distance import calculate_trajectory_length_in_meters
from .error import calculate_error_vector
from .split import split_trajectory_with_overlap

Params = Dict[str, Union[float, int, str]]
Report = Dict[str, Union[float, int, str]]


def generate_report_for_user(
        user_id: int,
        method: str,
        ratio: float = 0.5,
        threshold: float = 10.0,
        time: float = 60.0,
        verbosity: int = 0
) -> Report:
    """
    Runs prediction method for all trajectories of an user and returns a report of the results
    :param user_id: user id
    :param method: prediction method
    :param ratio: split ratio
    :param threshold: threshold in meters
    :param time: time in seconds
    :param verbosity: verbosity of the generation process
    :return: report
    """
    assert user_id > 0
    assert method
    assert ratio >= 0.0
    assert ratio <= 1.0
    assert threshold > 0
    assert time > 0
    assert verbosity >= 0

    if verbosity > 0:
        print(f'Generating report for user {user_id}')

    trajectory_ids = get_list_of_users_trajectory_ids(user_id=user_id)
    failed = 0
    errors = []

    for trajectory_id in trajectory_ids:
        if verbosity > 1:
            print(trajectory_id, end='')
        target_trajectory, data = load_users_trajectories_with_target(
            user_id=user_id,
            trajectory_id=trajectory_id
        )
        head, tail = split_trajectory_with_overlap(
            trajectory=target_trajectory,
            ratio=ratio
        )
        if method == 'bullet':
            prediction = bullet_prediction(head, time)
        else:
            if verbosity > 0:
                print('unknown prediction method')
            return {}
        if size(prediction, 0) < 2:
            failed += 1
            if verbosity > 1:
                print(' failed')
            continue

        pred_dist = calculate_trajectory_length_in_meters(
            trajectory=prediction
        )
        if len(prediction) > 0 and \
                size(prediction, 0) > 0 and \
                size(prediction, 1) == 4 and \
                pred_dist > 0:
            error_amount = calculate_error_vector(tail, prediction)[:, 4]
            if verbosity > 1:
                print(' success', pred_dist, len(error_amount), sum(error_amount))
            errors.append(error_amount)
        else:
            failed += 1
            if verbosity > 1:
                print(' failed')

    errors_sum = list(map(sum, errors))
    report = {
        'user_id': user_id,
        'method': method,
        'ratio': ratio,
        'threshold': threshold,
        'time': time,
        'failed predictions': failed,
        'error average': average(errors_sum),
        'error median': median(errors_sum),
        'error standard deviation': std(errors_sum)
    }
    if verbosity > 0:
        print(
            '\nERROR STATISTICS',
            '\naverage\t\t\t', report['error average'],
            '\nmedian\t\t\t', report['error median'],
            '\nstandard deviation\t', report['error standard deviation'],
            '\nfailed predictions\t', report['failed predictions']
        )

    return report


def wrapped_generation(args: Tuple[int, Params]) -> Report:
    """
    This function wraps the report generation function since in Python, the worker pool
    cannot serialize local objects before sending them to worker processes.
    :param args: tuple that contains user id as the first element and parameter dictionary
    as the second element
    :return: generated report for the user
    """
    assert args
    assert args[0]
    assert args[1]

    user, params = args
    return generate_report_for_user(
        user_id=user,
        method=params['method'],
        ratio=params['ratio'],
        threshold=params['threshold'],
        time=params['time'],
        verbosity=params['verbosity']
    )


def generate_report_for_dataset(
        method: str,
        ratio: float = 0.5,
        threshold: float = 10.0,
        time: float = 60.0,
        verbosity: int = 0
) -> List[Report]:
    """
    Generate a list of reports for all users in the dataset
    :param method: prediction method
    :param ratio: split ratio
    :param threshold: threshold in meters
    :param time: time in seconds
    :param verbosity: verbosity of the generation process
    :return: list of reports
    """
    assert method
    assert ratio >= 0.0
    assert ratio <= 1.0
    assert threshold > 0
    assert time > 0
    assert verbosity >= 0

    users = get_list_of_user_ids()
    params = {
        'method': method,
        'ratio': ratio,
        'threshold': threshold,
        'time': time,
        'verbosity': verbosity
    }
    queue = list(zip(users, repeat(params)))

    with Pool() as pool:
        return pool.map(
            wrapped_generation,
            queue
        )
