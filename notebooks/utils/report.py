# pylint: disable=E0402

"""
Report generating functions
"""

from typing import Dict
from numpy import average, median, std, size
from .bullet import bullet_prediction
from .dataset import get_list_of_users_trajectory_ids, load_users_trajectories_with_target
from .distance import calculate_trajectory_length_in_meters
from .error import calculate_error_vector
from .split import split_trajectory_with_overlap


def generate_report_for_user(
        user_id: int,
        method: str,
        ratio: float = 0.5,
        threshold: float = 10,
        time: float = 60,
        verbosity: int = 0
) -> Dict[str, str]:
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
            return
        if size(prediction, 0) < 2:
            failed += 1
            if verbosity > 1:
                print(' failed')
            continue

        pred_dist = calculate_trajectory_length_in_meters(trajectory=prediction)
        if len(prediction) > 0 and size(prediction, 0) > 0 and size(prediction, 1) == 4 and pred_dist > 0:
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
