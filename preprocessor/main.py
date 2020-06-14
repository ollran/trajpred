#!/usr/bin/env python3


from configparser import ConfigParser
from hashlib import sha256
from itertools import chain
from os import listdir, mkdir
from shutil import move, rmtree
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


if __name__ == '__main__':
    main()
