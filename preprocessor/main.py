#!/usr/bin/env python3


from hashlib import sha256

from requests import get


def fetch_dataset(url: str, archive_filename: str) -> None:
    """
    Fetches the dataset from the URL and saves it into a file
    :param url: the URL of the dataset
    :param archive_filename: the destination filename
    :return: None
    """
    with get(url=url, stream=True) as response, \
            open(archive_filename, mode='wb') as file_handle:
        for chunk in response.iter_content(chunk_size=128):
            file_handle.write(chunk)


def verify_dataset(dataset_archive_filename: str, dataset_hash_sha2: str) -> bool:
    """
    Verifies the SHA2 hash of the dataset archive
    :param dataset_archive_filename: the filename of the ZIP archive
    :param dataset_hash_sha2: the SHA2 hash of the dataset ZIP archive
    :return: True of False depending on the result of the check
    """
    hash_sha2 = sha256()
    with open(dataset_archive_filename, mode='rb') as file_handle:
        for chunk in iter(lambda: file_handle.read(4096), b''):
            hash_sha2.update(chunk)
        return hash_sha2.hexdigest() == dataset_hash_sha2


def main():
    pass


if __name__ == '__main__':
    main()
