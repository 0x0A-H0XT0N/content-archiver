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


By default, the program will download all the video information, which can be customized with your own needs 
[here](#download-options). The goal is to be the closest as possible to the original video and have all 
information about it.

The program has [torrent integration](#torrent-integration) with, which helps to share any content downloaded.

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

# DOWNLOAD OPTIONS

All possible download options can be found at [youtube-dl home page](https://github.com/ytdl-org/youtube-dl/blob/master/README.md "Youtube-dl README.md") 
and [youtube-dl available options](https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312 "Youtube-dl options for embedding.")

To change any download option, just type "conf" at the main menu, or type "5" if you are in a group.

Every group have a separated config from the "main" one, this mean that each group can have its own properties (except for download path and the [output template](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#output-template "Read this for more info about the output template.")).
Once you create a new group, the config to be used is the program default one.

All program configs are stored at:
```
Linux:      ~/.config/mgtow-archive
Windows:    ~\.mgtowArchive
```


By default, to be the closest as possible to the original video, all metadata related will be downloaded, that includes: 
* Thumbnail
* General metadata
* Video description
* Subtitles
* Annotations

This can be changed at ""


# BUGS

If you find a bug, report to one of these places:
* Contact PhoenixK7PB#8422 at Discord.
* Create a issue at the github page project 