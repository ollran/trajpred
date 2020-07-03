"""
Dataset related functions
"""

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
