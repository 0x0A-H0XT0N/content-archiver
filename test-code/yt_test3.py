import youtube_dl
import signal
import sys
import threading


def signal_handler(signal, frame):
    sys.exit(0)


def youtube_hooker(video):
    print("\n   Status: %s" % video["status"])
    print(video)
    print("\n   Len: %d" % len(video))


youtube_config = {      # --------------------CHANGE THIS!!!--------------------- #

    'progress_hooks': [youtube_hooker],
    'daterange':                youtube_dl.DateRange.day("20190701").start + youtube_dl.DateRange.day("20190702").end,
    'format':                   'bestaudio/best',   # Video format code. See options.py for more information.
    'outtmpl':                  '/mnt/phoenix/mgtow_archive/test/daterange_test' + '/%(uploader)s/%(title)s.%(ext)s',
    'restrictfilenames':        True,               # Do not allow "&" and spaces in file names
    'no_warnings':              True,               # Do not print out anything for warnings.
    'ignoreerrors':             True,               # Do not stop on download errors.
    'nooverwrites':             True,               # Prevent overwriting files.
    'writedescription':         True,              # Write the video description to a .description file
    'writethumbnail':           True,              # Write the thumbnail image to a file
    'writeautomaticsub':        False,              # Write the automatically generated subtitles to a file
    'verbose':                  False,              # Print additional info to stdout.
    'quiet':                    False,              # Do not print messages to stdout.
    'simulate':                 False,              # Do not download the video files.
    'skip_download':            False,              # Skip the actual download of the video file
    'noplaylist':               False,              # Download single video instead of a playlist if in doubt.
    'playlistrandom':           False,              # Download playlist items in random order.
    'playlistreverse':          False,              # Download playlist items in reverse order.
    'forceurl':                 False,              # Force printing final URL.
    'forcetitle':               False,              # Force printing title.
    'forceid':                  False,              # Force printing ID.
    'forcethumbnail':           False,              # Force printing thumbnail URL.
    'forcedescription':         False,              # Force printing description.
    'forcefilename':            False,              # Force printing final filename.
    'forceduration':            False,              # Force printing duration.
    'forcejson':                False,              # Force printing info_dict as JSON.
}


def youtube_download(url):
    youtube_dl.YoutubeDL(youtube_config).download([url])


signal.signal(signal.SIGINT, signal_handler)
youtube_download("https://www.youtube.com/channel/UCd4xRbTbKS3CI8I17YjTBNQ")

