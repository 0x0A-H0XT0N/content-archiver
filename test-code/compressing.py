import tarfile
import os
from pathlib import Path
import fnmatch

path = "/mnt/phoenix/mgtow_archive/test/"
sorted_folders_names = ["subtitles", "thumbnails", "descriptions", "metadata", "videos", "annotations"]

titles = []

def compress_all_videos(root_path):
    for channel in get_downloaded_channels(root_path):
        list_channel = os.listdir(channel)
        mp4_videos = fnmatch.filter(list_channel, "*.mp4")
        for video in mp4_videos:
            title = os.path.splitext(channel + "/" + video)[0]
            titles.append(title)
        tar = tarfile.open(channel + "/happy_humble_hermit.tar.gz", "w:gz")
        tar.add(titles[0] + ".mp4", arcname="happy_humble_hermit")
        tar.close()
        print(titles[0])

def all_in_one(root_path):
    for channel in get_downloaded_channels(root_path):
        for folder in os.listdir(channel):
            absolute_folder_path = channel + "/" + folder
            if os.path.isdir(absolute_folder_path) and folder in sorted_folders_names:
                for file in os.listdir(absolute_folder_path):
                    os.rename(absolute_folder_path + "/" + file, channel + "/" + file)


def get_downloaded_channels(root_path):
    downloaded_channels_list = []
    for directory in os.listdir(os.path.abspath(root_path)):
        if os.path.isdir(root_path + directory):
            downloaded_channels_list.append(root_path + directory)
    print(downloaded_channels_list)
    return downloaded_channels_list


compress_all_videos(path)
