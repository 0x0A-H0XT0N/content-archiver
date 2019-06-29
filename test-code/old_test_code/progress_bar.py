from pytube import YouTube
from progress.bar import IncrementalBar


def make_bar(filesize, title):
    """
    make a bar object, need filesize for bar progress,
    :param filesize: filesize of video
    :return: nothing.
    """
    global bar
    bar = IncrementalBar("[download] " + title, max=filesize, suffix='%(percent).2f%%')

# https://www.youtube.com/watch?v=nYpdhE1uG1Y


yt = YouTube("https://www.youtube.com/watch?v=X4q3oUm_jAA")
make_bar(yt.streams.first().filesize, yt.title)


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


yt.register_on_progress_callback(show_progress_bar)
yt.streams.first().download()
print()
