#!/usr/bin/env python3


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


def main():
    pass


if __name__ == '__main__':
    main()
