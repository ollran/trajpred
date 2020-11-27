#!/usr/bin/env python3

"""
Helper is a CLI tool that contains miscellaneous helper procedures
"""

from argparse import ArgumentParser
from typing import List, Set
from utils.dataset import get_list_of_all_trajectory_ids


def check_duplicate_trajectory_ids(verbosity: int) -> List[int]:
    """
    Finds duplicate trajectory ids and returns them as a list
    :param verbosity: verbosity level
    :return: list of duplicate trajectory ids
    """
    assert verbosity >= 0

    trajectory_ids = get_list_of_all_trajectory_ids()
    trajectory_id_set: Set[int] = set()
    previous_len = len(trajectory_id_set)
    duplicates = []

    for trajectory_id in trajectory_ids:
        if verbosity > 0:
            print(f'{trajectory_id}\r', end='')
        trajectory_id_set.add(trajectory_id)
        trajectory_id_set_len = len(trajectory_id_set)
        if trajectory_id_set_len == previous_len:
            duplicates.append(trajectory_id)
        previous_len = trajectory_id_set_len
    if verbosity > 0:
        print('\n')

    return duplicates


def main() -> None:
    """
    Main procedure of the helper
    :return: None
    """
    parser = ArgumentParser(
        description='Helper, a CLI tool that contains miscellaneous helper procedures'
    )
    parser.add_argument(
        '--check-duplicate-trajectory-ids',
        help='Check dataset for duplicate trajectory ids',
        dest='check_duplicate_trajectory_ids',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--verbosity',
        help='Verbosity level (for debugging)',
        type=int,
        dest='verbosity',
        default=0
    )
    args = parser.parse_args()

    if args.check_duplicate_trajectory_ids:
        print('Checking dataset for duplicate trajectory ids...')
        duplicates = check_duplicate_trajectory_ids(
            verbosity=args.verbosity
        )
        print('duplicate trajectory ids:\n', duplicates)


if __name__ == '__main__':
    main()
