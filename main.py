# TODO: add progress bar when downloading (using progress)
# TODO: add choose option for format when downloading
# TODO: add menu and options

from pytube import YouTube
from pathlib import Path
import progress
import os


def download_video(url, path=str(Path.home())):
    """

    :param url: URL to download
    :param path: (optional) download location for saving the file,
    default one is current user home directory.
    if path does not exist, it's created.
    :return: True or False
    """
    if not os.path.exists(path):
        os.makedirs(path)
    YouTube(url).streams.first().download(path)


if __name__ == "__main__":
    # TODO
    video_url = str(input("Video url to download: "))
    path_location = str(input("Full path to download (blank is default (home directory): "))
    print(path_location)

    if path_location != "":
        download_video(video_url, path_location)
    else:
        download_video(video_url)
