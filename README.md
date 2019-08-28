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

To install the program, you will need [Python3.5+](https://www.python.org/downloads/) and the following dependencies:
* [youtube-dl](https://github.com/ytdl-org/youtube-dl)
* [qbittorrent-api](https://pypi.org/project/qbittorrent-api/)
* [dottorrent](https://dottorrent.readthedocs.io/en/latest/install.html)
* [colorama](https://github.com/tartley/colorama)

You can the following command to install all dependencies:
```
pip install qbittorrent-api dottorrent colorama youtube-dl
```

Alternatively, ou can use the following command to install the dependencies using _requirements.txt_:
```
pip install -r requirements.txt
```

**Note that depending on your OS, "pip" can be "pip3".**

# DOWNLOAD OPTIONS

By default, all metadata related to the videos will be downloaded, that includes: 
* Thumbnail
* General metadata
* Video description
* Subtitles
* Annotations


# BUGS

If you find a bug, report to one of these places:
* Contact PhoenixK7PB#8422 at Discord.
* Create a issue at the github page project 