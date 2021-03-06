#!/usr/bin/env python3

"""
Preprocessor script that downloads the dataset, verifies it and finally extracts it
"""

from configparser import ConfigParser
from hashlib import sha256
from itertools import chain
from os import listdir, mkdir, remove
from os.path import isdir, isfile
from shutil import move, rmtree
from timeit import default_timer
from zipfile import ZipFile

from requests import get

# Constants
DATASET = 'DATASET'
URL = 'URL'
HASH_SHA2 = 'HASH_SHA2'
DIRECTORY = 'DIRECTORY'


def fetch_dataset(url: str, dataset_archive_filename: str) -> None:
    """
    Fetches the dataset from the URL and saves it into a file
    :param url: the URL of the dataset
    :param dataset_archive_filename: the destination filename
    :return: None
    """
    assert url
    assert dataset_archive_filename

    with get(url=url, stream=True) as response, \
            open(dataset_archive_filename, mode='wb') as file_handle:
        for chunk in response.iter_content(chunk_size=128):
            file_handle.write(chunk)


def verify_dataset(dataset_archive_filename: str, dataset_archive_hash_sha2: str) -> bool:
    """
    Verifies the SHA2 hash of the dataset archive
    :param dataset_archive_filename: the filename of the ZIP archive
    :param dataset_archive_hash_sha2: the SHA2 hash of the dataset ZIP archive
    :return: True of False depending on the result of the check
    """
    assert dataset_archive_filename
    assert dataset_archive_hash_sha2

    hash_sha2 = sha256()
    with open(dataset_archive_filename, mode='rb') as file_handle:
        for chunk in iter(lambda: file_handle.read(4096), b''):
            hash_sha2.update(chunk)
        return hash_sha2.hexdigest() == dataset_archive_hash_sha2


def extract_dataset(dataset_archive_filename: str, dataset_directory: str) -> None:
    """
    Extracts the files from the ZIP archive
    :param dataset_archive_filename: the filename of the ZIP archive
    :param dataset_directory: the name of the directory where the dataset is extracted
    :return: None
    """
    assert dataset_archive_filename
    assert dataset_directory

    mkdir(dataset_directory)
    tmp_directory = f'{dataset_directory}_tmp'
    with ZipFile(dataset_archive_filename, mode='r') as file_handle:
        ZipFile.extractall(file_handle, path=tmp_directory)
    subdirectories = list(chain(*[
        [f'{subdirectory}/{trajectory}' for trajectory in listdir(subdirectory)]
        for subdirectory in [
            f'{tmp_directory}/{directory}'
            for directory in listdir(tmp_directory)
        ]
    ]))
    for subdirectory in subdirectories:
        move(subdirectory, dataset_directory)
    rmtree(tmp_directory)


def main() -> None:
    """
    Main preprocessor program
    :return: None
    """

    # Parse configuration file
    config = ConfigParser()
    config.read('config.ini')
    dataset_url = config[DATASET][URL]
    dataset_archive_filename = dataset_url.split('/')[-1]
    dataset_archive_hash_sha2 = config[DATASET][HASH_SHA2]
    dataset_directory = config[DATASET][DIRECTORY]

    # Fetch dataset from the server if it does not exist already
    if isfile(dataset_archive_filename):
        print(f'{dataset_archive_filename} already exists\n')
    else:
        print(f'fetching the dataset from {dataset_url}')
        fetch_start_time = default_timer()
        fetch_dataset(
            url=dataset_url,
            dataset_archive_filename=dataset_archive_filename
        )
        fetch_end_time = default_timer()
        print(f'fetching took {fetch_end_time - fetch_start_time} seconds\n')

    # Verify the dataset
    verification_start_time = default_timer()
    hash_match = verify_dataset(
        dataset_archive_filename=dataset_archive_filename,
        dataset_archive_hash_sha2=dataset_archive_hash_sha2
    )
    verification_end_time = default_timer()
    if hash_match:
        print(
            f'dataset matches the SHA2 checksum {dataset_archive_hash_sha2}\n'
            f'dataset verification took {verification_end_time - verification_start_time} seconds\n'
        )
    else:
        print(
            f'CORRUPTED DATASET, ABORTING!\n'
            f'dataset verification took {verification_end_time - verification_start_time} seconds\n'
        )
        return

    # Extract the dataset
    if isdir(dataset_directory):
        print(f'{dataset_directory} already exists, removing the old dataset directory')
        rmtree(dataset_directory)

    print(
        f'extracting the fetched dataset {dataset_archive_filename} into {dataset_directory}'
    )
    extract_start_time = default_timer()
    extract_dataset(
        dataset_archive_filename=dataset_archive_filename,
        dataset_directory=dataset_directory
    )
    extract_end_time = default_timer()
    print(f'extraction took {extract_end_time - extract_start_time} seconds\n')

    # Remove the ZIP archive
    print(f'removing {dataset_archive_filename}')
    remove(dataset_archive_filename)


if __name__ == '__main__':
    main()

"""
Should I ship with assertions on? Should I even write assertions?

- Axiom: Your program will crash.
- Lemma: Even if our code won't crash, someone else's code will."
https://wiki.c2.com/?ShipWithAssertionsOn

I guess it is better to fail early and loud when a condition that should never happen happens anyway.
Just like in Erlang: program the happy path, crash otherwise.
https://youtu.be/HCwRGHj5jOE
"""
