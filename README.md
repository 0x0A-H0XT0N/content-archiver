![MGTOW-Archive interface.](https://i.imgur.com/qe60Skq.png)

- [DESCRIPTION](#description)
- [INSTALLATION](#installation)
- [GROUPS](#groups)
- [DOWNLOAD OPTIONS](#download-options)
- [VIDEO SORTING](#sorting)
- [TORRENT INTEGRATION](#torrent-integration)
- [FAQ](#faq)
- [BUGS](#bugs)

# DESCRIPTION

MGTOW Archive is a Multi OS, Python3 CLI program 
designed to download, store, update and share large quantities of youtube videos and channels. Keep in mind that small 
quantities of video can be downloaded just as easy.

This guide will introduce the not-so-obvious features, where to get help, customization, etc. 

By default, the program will download all the video information, which can be customized with your own needs 
[here](#download-options). The goal is to be the closest as possible to the original video and have all 
information about it.

The program has [torrent integration](#torrent-integration), which helps to share any content downloaded.

**Remember: You can download any type of content you want, but the idea of the project is to store MGTOW videos.**

# INSTALLATION

The program is available to Windows, Linux and MacOS.

To install the program, you will need [Python3.5+](https://www.python.org/downloads/ "Python download page.") and the following dependencies:
* [youtube-dl](https://github.com/ytdl-org/youtube-dl "Youtube-dl home page.")
* [qbittorrent-api](https://pypi.org/project/qbittorrent-api/ "QBittorrent-api home page.")
* [dottorrent](https://dottorrent.readthedocs.io/en/latest/install.html "Dottorrent home page.")
* [colorama](https://github.com/tartley/colorama "Colorama home page")

You can the following command to install all dependencies:
```
pip install qbittorrent-api dottorrent colorama youtube-dl
```
Alternatively, ou can use the following command to install the dependencies using _requirements.txt_:
```
pip install -r requirements.txt
```
**Note: Depending on your OS, "pip" could be "pip3".**

You may want to add the .py program to your environment variables.

# GROUPS

Groups are a list (or group) of channels, every group has its own download configuration and channels. You can have a channel in more than one group.

Groups configs can be shared by coping or pasting then at this folder:
```
Windows:    ~\.mgtowArchive\groups
Linux:      ~/.config/mgtow-archive/groups
```

# DOWNLOAD OPTIONS

All download options can be found at [youtube-dl home page](https://github.com/ytdl-org/youtube-dl/blob/master/README.md "Youtube-dl README.md") 
and [youtube-dl available options](https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312 "Youtube-dl options for embedding.")

To change any download option, just type "conf" at the main menu, or type "5" if you are in a group.

Every group have a separated config from the "main" one, this mean that each group can have its own properties (except for download path and the [output template](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#output-template "Read this for more info about the output template.")).
Once you create a new group, the config used is the default one.

All program configs are stored at:
```
Windows:    ~\.mgtowArchive
Linux:      ~/.config/mgtow-archive
```
You can share your config to another person (even groups configs), these files are universal, so you can share using a windows machine, and a linux machine will be able to use it. Be aware that if you copy the config from a person, you will lose your current config.

By default, to be the closest as possible to the original video, all metadata related will be downloaded, that includes: 
* Thumbnail
* General metadata
* Video description
* Subtitles
* Annotations

This can be changed by entering the "others" option, at the download options menu.

You can manually change the download options by editing the .json file, this is not the recommended way, but if you know what you are doing, go ahead.

The program have a lot of options, this guide will not cover all of them, almost all of them are straight forward, and if you dont know what a option does, just search by the youtube-dl links.

# SORTING

Sorting is the way the program should organize the downloaded files. There are two types of sorting:

- All in one (default)
- Sort by type

In "all in one", the program does not organize any files, downloads are only separated by channels.

In "sort by type", the program organizes all files into subfolders, these subfolders are:
- Annotations
- Descriptions
- Metadata
- Subtitles
- Thumbnails
- Videos

**NOTE 1: Be aware that in "sort by type", all the files and folders in the download path will be sorted. Not only the program downloads.**

**NOTE 2: As a failsafe, the program will never delete any files.**

**NOTE 3: The "all in one" sort does the reverse operation of "sort by type". If you want to revert the changes, just go back to "all in one" and the program will undo the operations.**

**NOTE 4: The "all in one" sort will automatically detect any non-program folders that are not empty. As a failsafe, the user should manually correct the program.**

**NOTE 5: A folder named "test" will not be sorted.**

# TORRENT INTEGRATION

The program has torrent integration with QBittorrent v4.1+

To enable it, you first need to enable the Web UI at:
```
QBittorrent > "Tools" > "Preferences" > "Web UI"
```
**NOTE: Enable the check box "Bypass authentication for clients on localhost" for better functionality.**

The program can do these operations:
- Create a torrent from a downloaded channel.
- List mgtow-archive torrents (using tags).
- Change authentication options.
- Change trackers.

All torrents created will be stored at its respective channels folders. These files will have the extension ".torrent"

Created torrents will be automatically added to QBittorent,

# FAQ

If you have any question or feature request, contact  **PhoenixK7PB#8422** at Discord.

# BUGS

If you find a bug, report to one of these places:
* Contact PhoenixK7PB#8422 at Discord.
* Create a issue at the github page project.