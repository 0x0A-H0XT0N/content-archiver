#  ███╗   ███╗ ██████╗████████╗ ██████╗ ██╗    ██╗     █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗
#  ████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗██║    ██║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝
#  ██╔████╔██║██║  ███╗  ██║   ██║   ██║██║ █╗ ██║    ███████║██████╔╝██║     ███████║██║██║   ██║█████╗
#  ██║╚██╔╝██║██║   ██║  ██║   ██║   ██║██║███╗██║    ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝
#  ██║ ╚═╝ ██║╚██████╔╝  ██║   ╚██████╔╝╚███╔███╔╝    ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗
#  ╚═╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝
#


# TODO: make one more advanced progress bar
# TODO: add choose option for format when downloading
# TODO: add menu and options

from pytube import YouTube
from pathlib import Path
from progress.bar import IncrementalBar
import os


def make_bar(filesize, title):
    """
    make a bar object, need filesize for bar progress,
    :param filesize: filesize of video
    :return: nothing.
    """
    global bar
    bar = IncrementalBar("[download] " + title, max=filesize, suffix='%(percent).2f%%')


def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
    try:
        global last_bytes
    except NameError:
        pass
    bytes_finished = yt.streams.first().filesize - bytes_remaining
    try:
        bar.next(last_bytes - bytes_remaining)
    except NameError:
        bar.next(bytes_finished)
    last_bytes = bytes_remaining


def download_video(youtube_obj, path=str(Path.home())):
    """

    :param youtube_obj: YouTube(url) correspondent
    :param path: (optional) download location for saving the file,
    default one is current user home directory.
    if path does not exist, it's created.
    :return: Nothing # TODO change to call on end (register_on_complete_callback) and print stats
    """
    if not os.path.exists(path):
        os.makedirs(path)
    make_bar(youtube_obj.streams.first().filesize, youtube_obj.title)
    youtube_obj.register_on_progress_callback(show_progress_bar)
    youtube_obj.streams.first().download(path)


yt = YouTube(str(input("Video url to download: ")))
path_location = str(input("Full path to save file (blank is home directory): "))

if path_location != "":
    download_video(yt, path_location)
else:
    download_video(yt)
print()
