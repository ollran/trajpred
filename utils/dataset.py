"""
Dataset related functions
"""

from itertools import chain
from os import fwalk
from typing import List, Tuple
from numpy import loadtxt, ndarray

# CONSTANTS
DATASET_DIRECTORY = '../dataset'


def load_trajectory(user_id: int, trajectory_id: int) -> ndarray:
    """
    Loads trajectory from the dataset by user_id and trajectory_id
    :param user_id: user's id
    :param trajectory_id: trajectory's id
    :return: trajectory as numpy array
    """
    assert user_id > 0
    assert trajectory_id > 0

    return loadtxt(
        f'{DATASET_DIRECTORY}/{user_id}/{trajectory_id}'
    )


def load_users_trajectories(user_id: int) -> List[ndarray]:
    """
    Loads all user's trajectories and returns them as a list of numpy arrays
    :param user_id: user's id
    :return: List of trajectories
    """
    assert user_id > 0

    return list(chain(*[
        [loadtxt(f'{dirpath}/{f}') for f in filenames]
        for dirpath, _, filenames, _ in fwalk(f'{DATASET_DIRECTORY}/{user_id}')
    ]))


def load_users_trajectories_with_target(
        user_id: int,
        trajectory_id: int
) -> Tuple[ndarray, List[ndarray]]:
    """
    Loads target trajectory and the rest of target user's trajectories and returns them as a tuple
    :param user_id: user's id
    :param trajectory_id: trajectory's id
    :return: target trajectory and the rest of user's trajectories as a tuple
    """
    assert user_id > 0
    assert trajectory_id > 0

    return (
        loadtxt(f'{DATASET_DIRECTORY}/{user_id}/{trajectory_id}'),  # target trajectory
        list(chain(*[  # the rest of them
            [loadtxt(f'{dirpath}/{f}')
             for f in filenames if f != f'{trajectory_id}']  # omit the target trajectory
            for dirpath, _, filenames, _ in fwalk(f'{DATASET_DIRECTORY}/{user_id}')
        ]))
    )


def load_all_trajectories() -> List[ndarray]:
    """
    Loads all trajectories and returns them as a list of numpy arrays
    :return: List of trajectories
    """
    return list(chain(*[
        [loadtxt(f'{dirpath}/{f}') for f in filenames]
        for dirpath, _, filenames, _ in fwalk(f'{DATASET_DIRECTORY}')
    ]))


def get_list_of_users_trajectory_ids(user_id: int) -> List[int]:
    """
    Get list of trajectory ids by user_id
    :param user_id: user's id
    :return: list of trajectory ids
    """
    assert user_id > 0

    return list(chain(*[
        [int(f) for f in filenames]
        for dirpath, _, filenames, _ in fwalk(f'{DATASET_DIRECTORY}/{user_id}')
    ]))
