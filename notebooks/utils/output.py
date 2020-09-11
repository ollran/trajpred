"""
Outputting related functions
"""

from numpy import ndarray, size


def output_coordinates_to_file(filename: str, results: ndarray) -> None:
    """
    Output results to a file
    :param filename: filename as string
    :param results: Results as ndarray
    :return: None
    """
    assert size(results, 0) > 0
    assert size(results, 1) == 4
    assert len(filename) > 0

    with open(filename, 'w') as file:
        for line in results:
            [lat, lon, _, _] = line
            file.write(f'{lat},{lon}\n')
