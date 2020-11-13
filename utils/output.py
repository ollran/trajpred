"""
Outputting related functions
"""

from typing import List
from numpy import ndarray, size


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
