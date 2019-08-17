#  ███╗   ███╗ ██████╗████████╗ ██████╗ ██╗    ██╗     █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗
#  ████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗██║    ██║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝
#  ██╔████╔██║██║  ███╗  ██║   ██║   ██║██║ █╗ ██║    ███████║██████╔╝██║     ███████║██║██║   ██║█████╗
#  ██║╚██╔╝██║██║   ██║  ██║   ██║   ██║██║███╗██║    ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝
#  ██║ ╚═╝ ██║╚██████╔╝  ██║   ╚██████╔╝╚███╔███╔╝    ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗
#  ╚═╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝
# https://github.com/PhoenixK7PB/mgtow-archive
#
# TODO: re-make README.md
# TODO: make a list of all possible bit sizes for the user to choose from
# TODO: add filters to download option <-
# TODO: make shortcuts

# import tarfile
import json
import signal
import sys
import os
import tty
import termios
from fnmatch import fnmatch
import base64
from datetime import datetime

import youtube_dl
from colorama import Fore, init
import qbittorrentapi
from dottorrent import Torrent

from pathlib import Path
from time import sleep, process_time

affirmative_choice = ["y", "Y", "yes", "s", "sim", "yeah", "yah", "ya"]  # affirmative choices, user input detection
negative_choice = ["n", "no", "nao", "na", "nop", "nah"]  # negative choices, user input detection

original_stdin_settings = termios.tcgetattr(sys.stdin)

download_archive = True

sorted_folders_names = ["subtitles", "thumbnails", "descriptions", "metadata", "videos", "annotations"]

excluded_channels_names = ["test", "torrents"]

warnings = 0
errors = []


class Color:
    """
    Return text with color using colorama.
    Pretty much straight forward to read.
    Just use Color().wantedColorOrBold(textToBeColoredOrBolded).
    """
    def __init__(self):
        self.RED = Fore.RED
        self.YELLOW = Fore.YELLOW
        self.BLUE = Fore.BLUE
        self.GREEN = Fore.GREEN
        self.BOLD = '\033[1m'
        self.END = '\033[0m'

    def red(self, text):
        return self.RED + text

    def yellow(self, text):
        return self.YELLOW + text

    def blue(self, text):
        return self.BLUE + text

    def green(self, text):
        return self.GREEN + text

    def bold(self, text):
        return self.BOLD + text + self.END


class Logger(object):

    @staticmethod
    def debug(msg):
        print(msg)

    @staticmethod
    def warning(msg):
        global warnings
        warnings += 1

    @staticmethod
    def error(msg):
        global errors
        errors.append(color.red(color.bold(str(msg))))

        print(color.red(color.bold(msg)))


class Json:
    """
    Handle JSON requests.
    """

    @staticmethod
    def encode(data, write_filename):
        """
        Encode a obj (if available) to a file
        Do NOT handle exceptions or errors
        :param data: Data obj to write on the file, should be compatible with JSON
        :param write_filename: Name of the file to write
        Should have ".json" at the end.
        :return: Nothing.
        """
        with open(write_filename, "w") as write_file:
            json.dump(data, write_file)

    @staticmethod
    def decode(read_filename):
        """
        Read a .json file and transfer the data to a global variable
        :param read_filename: Name of the file to be read, NEED the .json at the end
        :return: content decoded
        """
        with open(read_filename) as json_data:
            return json.load(json_data)


class ConfigPath:
    def __init__(self):
        self.home = str(Path.home())
        self.config_path = self.home + "/.config/mgtow-archive/"

    def get(self):
        if not os.path.exists(self.config_path):  # check if config dir exists
            os.makedirs(self.config_path)
        return self.config_path

    def init_sub_folders(self):
        subfolders = [
            "groups",
            "torrents",
            "download_archives"
        ]
        if not os.path.exists(self.config_path):  # check if config dir exists
            os.makedirs(self.config_path)
        for subfolder in subfolders:
            subfolder_path = self.config_path + subfolder
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)


class Organizer:
    def get_sort_type(self):
        try:
            return Json.decode(ConfigPath().get() + "sort_type.json")
        except FileNotFoundError:
            self.sort_by_type(download_path)
            return Json.decode(ConfigPath().get() + "sort_type.json")

    def sort_by_type(self, root_path):
        for channel in self.get_downloaded_channels(root_path):
            self.make_folder_sorted_directories(channel + "/")
            for file in os.listdir(channel):
                absolute_file_path = channel + "/" + file
                if os.path.isfile(absolute_file_path):
                    if fnmatch(file, "*.tar.gz"):
                        pass
                    elif fnmatch(file, "*.jpg"):
                        os.rename(absolute_file_path, channel + "/thumbnails/" + file)
                    elif fnmatch(file, "*.description"):
                        os.rename(absolute_file_path, channel + "/descriptions/" + file)
                    elif fnmatch(file, "*.info.json"):
                        os.rename(absolute_file_path, channel + "/metadata/" + file)
                    elif fnmatch(file, "*.annotations.xml"):
                        os.rename(absolute_file_path, channel + "/annotations/" + file)
                    elif fnmatch(file, "*.mp4"):
                        os.rename(absolute_file_path, channel + "/videos/" + file)
                    if fnmatch(file, "*.vtt"):
                        os.rename(absolute_file_path, channel + "/subtitles/" + file)
                    elif fnmatch(file, "*.webm"):
                        os.rename(absolute_file_path, channel + "/videos/" + file)
                    elif fnmatch(file, "*.m4a"):
                        os.rename(absolute_file_path, channel + "/videos/" + file)
                    elif fnmatch(file, "*.mp3"):
                        os.rename(absolute_file_path, channel + "/videos/" + file)
                    elif fnmatch(file, "*.opus"):
                        os.rename(absolute_file_path, channel + "/videos/" + file)
                    elif fnmatch(file, "*.mkv"):
                        os.rename(absolute_file_path, channel + "/videos/" + file)
                    elif fnmatch(file, "*.torrent"):
                        pass
                elif os.path.isdir(absolute_file_path):
                    # handle?
                    pass
        Json.encode("sort_by_type", ConfigPath().get() + "sort_type.json")

    def all_in_one(self, root_path):
        for channel in self.get_downloaded_channels(root_path):
            for folder in os.listdir(channel):
                absolute_folder_path = channel + "/" + folder
                if os.path.isdir(absolute_folder_path) and folder in sorted_folders_names:
                    for file in os.listdir(absolute_folder_path):
                        os.rename(absolute_folder_path + "/" + file, channel + "/" + file)
            self.remove_folder_sorted_directories(channel + "/")
        Json.encode("all_in_one", ConfigPath().get() + "sort_type.json")

    @staticmethod
    def remove_folder_sorted_directories(channel_path):
        for folder in os.listdir(channel_path):
            absolute_folder_path = channel_path + "/" + folder
            if os.path.isdir(absolute_folder_path):
                try:
                    os.rmdir(absolute_folder_path)
                except OSError:
                    print(color.red(color.bold("\n    ERROR AT '%s':\n"
                                               "    DIRECTORY NOT EMPTY, NOT REMOVING IT!\n") % absolute_folder_path))

    @staticmethod
    def make_folder_sorted_directories(channel_path):
        for folder_name in sorted_folders_names:
            if not os.path.exists(channel_path + "/" + folder_name):
                os.makedirs(channel_path + "/" + folder_name)

    @staticmethod
    def get_downloaded_channels(root_path):
        downloaded_channels_list = []
        for directory in os.listdir(os.path.abspath(root_path)):
            if directory in excluded_channels_names:
                continue
            if os.path.isdir(root_path + directory):
                downloaded_channels_list.append(root_path + directory)
        return downloaded_channels_list


class YTConfig:
    class DownloadPath:
        def __init__(self, config_file=ConfigPath().get() + "path.json"):
            self.config_file = config_file

        def get(self):
            """
            Should get a "path" for storing the downloaded content
            Uses json_handler,
            If not data could be found, calls make_path()
            :return: Make a global variable called "path",
            """
            try:  # tries to decode path
                return Json.decode(self.config_file)
            except FileNotFoundError:  # if the file is not founded, calls make_path() and makes it
                self.make()
                return self.get()

        def make(self):
            """
            create a JSON file on the program directory containing the path for downloaded videos,
            user can use home path
            """

            clear()
            print(color.red(color.bold("-------------------------MAKE-PATH--------------------------")))
            path_name = str(input("Type the " + color.yellow(color.bold("full path")) +
                                  " for storing downloads...\n" +
                                  color.yellow(color.bold("Enter")) + " to use your " +
                                  color.yellow(color.bold("home path")) + "." + "\n>:"))

            if path_name == "":  # if user input is blank,
                clear()
                if not os.path.exists(str(Path.home())):  # check if user home exists,
                    os.makedirs(str(Path.home()))  # if not, create it
                Json.encode(str(Path.home()) + "/",
                            self.config_file)
                # encode JSON file containing the path (home path in this case)

            else:  # if user input is not blank,
                clear()
                if not os.path.exists(path_name):  # check if user input path exists
                    os.makedirs(path_name)  # if not, create it
                Json.encode(path_name + "/", self.config_file)
                # encode JSON file containing the user path

            clear()
            print("The program need to be restarted for the changes take effect. Exiting...")
            sys.exit(0)

        def set(self):
            """
            option for changing/making new path
            :return: nothing, just changes path global variable
            """
            clear()
            print(color.red(color.bold("------------------------CHANGE-PATH-------------------------")))
            print("Your current path is: " + color.yellow(color.bold(download_path)))
            new_path = str(input("\nType your new path...\n" + enter_to_return() +
                                 "\n>:"))
            if new_path == "":  # check user input, if blank, return
                return

            else:  # else: check, encode, change global variable path and returns
                if not os.path.exists(new_path):  # checks if new path exists,
                    os.makedirs(new_path)  # if not, create it,
                Json.encode(new_path + "/", self.config_file)  # then encode it
                clear()
                print("The program need to be restarted for the changes take effect. Exiting.")
                sys.exit(0)

    class Format:
        def __init__(self, config_file=ConfigPath().get() + "master_config.json"):
            self.config_file = config_file
            self.custom_file = ConfigPath().get() + "custom_formats.json"
            self.ytconfig = YTConfig(self.config_file)
            self.current_config = self.ytconfig.get()
            self.formats = {
                "mp4": "mp4[height=720]/mp4[height<720]/mp4",
                "mp3": "mp3",
                "bestaudio": "bestaudio",
                "best": "best",
            }

        def get(self, raw=False):

            current_format = self.current_config["format"]

            if not raw:
                try:
                    return list(self.formats.keys())[list(self.formats.values()).index(current_format)]
                except ValueError:
                    custom = self.get_custom()
                    if current_format in custom.values():
                        return list(custom.keys())[list(custom.values()).index(current_format)]
                    else:
                        return current_format
            elif raw:
                return current_format

        def get_custom(self):
            try:
                return Json.decode(self.custom_file)
            except FileNotFoundError:
                Json.encode({}, self.custom_file)
                return self.get_custom()

        def update(self, ext):
            self.current_config["format"] = ext
            if self.ytconfig.DownloadArchive(self.config_file).state():
                try:
                    self.current_config["download_archive"] = self.ytconfig.DownloadArchive().\
                        get(ext=list(self.formats.keys())[list(self.formats.values()).index(ext)])
                except ValueError:
                    custom = self.get_custom()
                    self.current_config["download_archive"] = self.ytconfig.DownloadArchive(). \
                        get(ext=list(custom.keys())[list(custom.values()).index(ext)])
            self.ytconfig.update(self.current_config)

        def handler(self):
            while True:
                clear()
                print(color.red(color.bold("-----------------------DOWNLOAD-FORMAT----------------------")))
                custom = self.get_custom()
                current_format = self.get()

                print(color.yellow(color.bold("1")) + ")    (" + color.red(color.bold("X")) + ") MP4") \
                    if current_format == "mp4" else print(color.yellow(color.bold("1")) + ")    ( ) MP4")

                print(color.yellow(color.bold("2")) + ")    (" + color.red(color.bold("X")) + ") MP3") \
                    if current_format == "mp3" else print(color.yellow(color.bold("2")) + ")    ( ) MP3")

                print(color.yellow(color.bold("3")) + ")    (" + color.red(color.bold("X")) +
                      ") Best audio only format available") \
                    if current_format == "bestaudio" else print(color.yellow(color.bold("3")) +
                                                                ")    ( ) Best audio only format available")
                print(color.yellow(color.bold("4")) + ")    (" + color.red(color.bold("X")) +
                      ") Best format available") if current_format == "best" else print(
                    color.yellow(color.bold("4")) + ")    ( ) Best format available")
                print(color.red(color.bold("---------------------------CUSTOM---------------------------")))
                custom_count = 0
                custom_dict = dict()
                if len(custom) > 0:
                    for custom_format in custom:
                        custom_count += 1
                        print(color.yellow(color.bold(str(custom_count) + "c")) + ")   (" + color.red(color.bold("X")) +
                              ") %s : %s" % (custom_format, custom[custom_format])) if current_format == custom_format \
                            else print(color.yellow(color.bold(str(custom_count) + "c")) + ")    ( ) %s : %s"
                                       % (custom_format, custom[custom_format]))
                        custom_dict[str(custom_count)] = custom_format
                    print()
                print(color.yellow(color.bold("add")) + ") Add a custom format")
                print(color.yellow(color.bold("del")) + ") Remove a custom format")
                print(enter_to_return())
                format_choice = str(input(">:"))

                if format_choice == "":
                    break
                elif format_choice == "add":
                    while True:
                        clear()
                        print(color.red(color.bold("-------------------------ADD-CUSTOM-------------------------")))
                        print(color.yellow(color.bold("Leave blank to cancel.\n")))
                        custom_name = str(input("Format name?\n>:"))
                        custom_code = str(input("\nFormat code?\n>:"))
                        if custom_name and custom_code != "":
                            custom[custom_name] = custom_code
                            Json.encode(custom, self.custom_file)
                            custom = self.get_custom()
                            add_another_format_choice = str(input("\nAdd another format? [y/N]\n>:"))
                            if add_another_format_choice not in affirmative_choice:
                                break
                        else:
                            break
                    continue
                elif format_choice == "del":
                    while True:
                        clear()
                        print(color.red(color.bold("------------------------REMOVE-CUSTOM-----------------------")))
                        if len(custom) == 0:
                            print("No custom format found.")
                            wait_input()
                            break
                        custom_count = 0
                        custom_dict = dict()
                        for custom_format in custom:
                            custom_count += 1
                            print(color.yellow(color.bold(str(custom_count))) + ") %s : %s"
                                  % (custom_format, custom[custom_format]))
                            custom_dict[str(custom_count)] = custom_format
                        print(enter_to_return())
                        remove_custom_choice = str(input(">:"))
                        if remove_custom_choice == "":
                            break
                        try:
                            custom_choice = int(remove_custom_choice)
                            if custom_choice < 1:
                                raise ValueError
                            if custom_choice > custom_count:
                                raise ValueError
                        except ValueError:
                            clear()
                            wait_input()
                            continue
                        del custom[custom_dict[remove_custom_choice]]
                        Json.encode(custom, self.custom_file)
                    continue

                if "c" in format_choice:
                    if len(custom) == 0:
                        clear()
                        wait_input()
                        continue
                    format_strip = format_choice.strip("c")
                    try:
                        custom_choice = int(format_strip)
                        if custom_choice < 1:
                            raise ValueError
                        if custom_choice > custom_count:
                            raise ValueError
                    except ValueError:
                        clear()
                        wait_input()
                        continue
                    self.update(custom[custom_dict[format_strip]])
                else:
                    if format_choice == "1":
                        self.update(self.formats["mp4"])
                        self.get()
                        continue
                    elif format_choice == "2":
                        self.update(self.formats["mp3"])
                        self.get()
                        continue
                    elif format_choice == "3":
                        self.update(self.formats["bestaudio"])
                        self.get()
                        continue
                    elif format_choice == "4":
                        self.update(self.formats["best"])
                        self.get()
                        continue
                    else:
                        clear()
                        wait_input()
                        continue

    class DownloadArchive:
        def __init__(self, config_file=ConfigPath().get() + "master_config.json"):
            self.config_file = config_file
            self.download_archive_path = ConfigPath().get() + "download_archives/"
            self.format = YTConfig.Format(self.config_file).get()

        def get(self, ext="auto"):
            if ext == "auto":
                return self.download_archive_path + "download_archive_" + self.format
            else:
                return self.download_archive_path + "download_archive_" + ext

        def state(self, raw=True):
            """

            :return: True if on, False if off
            """
            current_config = YTConfig(self.config_file).get()
            archive_state = True if "download_archive" in current_config.keys() else False
            if raw:
                return archive_state
            elif not raw:
                if archive_state:
                    return "on"
                else:
                    return "off"

        def handler(self):
            while True:
                current_state = self.state()
                current_state_formatted = self.state(raw=False)
                current_config = YTConfig(self.config_file).get()
                clear()
                print(color.red(color.bold("----------------------DOWNLOAD-ARCHIVE----------------------")))
                print(color.yellow(color.bold("1")) + ") Turn on/off            |  ", end="")
                print(color.yellow(color.bold(current_state_formatted)))
                print(enter_to_return())

                archive_choice = str(input(">:"))
                if archive_choice == "":
                    break

                elif archive_choice == "1":
                    if current_state:
                        del current_config["download_archive"]
                        YTConfig(self.config_file).update(current_config)

                    elif not current_state:
                        current_config["download_archive"] = self.get()
                        YTConfig(self.config_file).update(current_config)

                else:
                    clear()
                    wait_input()

    class Bool:
        def __init__(self, config_file=ConfigPath().get() + "master_config.json"):
            self.config_file = config_file

        def handler(self):
            while True:
                config = YTConfig(self.config_file).get()

                clear()
                print(color.red(color.bold("------------------------OTHER-OPTIONS-----------------------")))
                bool_count = 0
                bool_dict = dict()
                for option in config:
                    if not isinstance(config[option], bool):
                        continue
                    bool_count += 1
                    print(color.yellow(color.bold(str(bool_count))) + ") %s : %s" % (option, config[option]))
                    bool_dict[str(bool_count)] = option
                print(enter_to_return())
                bool_choice = str(input(">:"))
                if bool_choice == "":
                    break
                elif bool_choice in bool_dict.keys():
                    bool_value = self.alternate_bool(config[bool_dict[bool_choice]])
                    config[bool_dict[bool_choice]] = bool_value
                    YTConfig(self.config_file).update(config)
                    continue
                else:
                    clear()
                    wait_input()
                    continue

        @staticmethod
        def alternate_bool(obj):
            if obj:
                return False
            if not obj:
                return True

    class Filters:
        pass

    class PostProcessing:
        def __init__(self, config_file=ConfigPath().get() + "master_config.json"):
            self.config_file = config_file

        def handler(self):
            while True:
                current_config = YTConfig(self.config_file).get()
                postprocessor = current_config['postprocessors']
                clear()
                print(color.red(color.bold("----------------------EMBEDDING-OPTIONS---------------------")))
                print(color.yellow(color.bold("1")) + ") Embed thumbnail           " + color.red(color.bold("|")) +
                      color.yellow(color.bold("  %s" % self.get_thumbnail(raw=False))))
                print(color.yellow(color.bold("2")) + ") Embed metadata            " + color.red(color.bold("|")) +
                      color.yellow(color.bold("  %s" % self.get_metadata(raw=False))))
                print(color.yellow(color.bold("3")) + ") Embed subtitle            " + color.red(color.bold("|")) +
                      color.yellow(color.bold("  %s" % self.get_subtitle(raw=False))))
                print(enter_to_return())
                embed_choice = str(input(">:"))

                if embed_choice == "":
                    break
                elif embed_choice == "1":
                    thumbnail = {'key': "EmbedThumbnail"}
                    if self.get_thumbnail():
                        index = postprocessor.index(thumbnail)
                        del postprocessor[index]
                        YTConfig(self.config_file).update(current_config)
                    elif not self.get_thumbnail():
                        postprocessor.append(thumbnail)
                        YTConfig(self.config_file).update(current_config)

                elif embed_choice == "2":
                    metadata = {'key': "FFmpegMetadata"}
                    if self.get_metadata():
                        index = postprocessor.index(metadata)
                        del postprocessor[index]
                        YTConfig(self.config_file).update(current_config)
                    elif not self.get_metadata():
                        postprocessor.append(metadata)
                        YTConfig(self.config_file).update(current_config)
                elif embed_choice == "3":
                    subtitle = {'key': "FFmpegEmbedSubtitle"}
                    if self.get_subtitle():
                        index = postprocessor.index(subtitle)
                        del postprocessor[index]
                        YTConfig(self.config_file).update(current_config)
                    elif not self.get_subtitle():
                        postprocessor.append(subtitle)
                        YTConfig(self.config_file).update(current_config)
                else:
                    wait_input()
                    continue

        def get_thumbnail(self, raw=True):
            if raw:
                if {'key': "EmbedThumbnail"} in YTConfig(self.config_file).get()['postprocessors']:
                    return True
                else:
                    return False
            elif not raw:
                if {'key': "EmbedThumbnail"} in YTConfig(self.config_file).get()['postprocessors']:
                    return "On"
                else:
                    return "Off"

        def get_metadata(self, raw=True):
            if raw:
                if {'key': "FFmpegMetadata"} in YTConfig(self.config_file).get()['postprocessors']:
                    return True
                else:
                    return False
            elif not raw:
                if {'key': "FFmpegMetadata"} in YTConfig(self.config_file).get()['postprocessors']:
                    return "On"
                else:
                    return "Off"

        def get_subtitle(self, raw=True):
            if raw:
                if {'key': "FFmpegEmbedSubtitle"} in YTConfig(self.config_file).get()['postprocessors']:
                    return True
                else:
                    return False
            elif not raw:
                if {'key': "FFmpegEmbedSubtitle"} in YTConfig(self.config_file).get()['postprocessors']:
                    return "On"
                else:
                    return "Off"

    def __init__(self, config_file=ConfigPath().get() + "master_config.json"):
        self.config_file = config_file
        self.config = self.get()

    def get(self, dl_archive=True, logger=True):
        try:
            config = Json.decode(self.config_file)
        except FileNotFoundError:
            self.make_default()
            config = Json.decode(self.config_file)
        finally:
            if logger:
                config['logger'] = Logger()
            if not dl_archive:
                del config["download_archive"]
            return config

    def update(self, new_config):
        if "logger" in new_config.keys():
            del new_config["logger"]
        Json.encode(new_config, self.config_file)

    def make_default(self):
        dl_path = self.DownloadPath().get()
        youtube_default_config = {
            # POST PROCESSING
            'postprocessors':   [],
            # FILTERS
            'matchtitle': None,
            'rejecttitle': None,
            'daterange': None,
            'min_views': None,
            'max_views': None,
            # USER DEFINED
            'download_archive': dl_path + "download_archive_mp4",
            'format': "mp4[height=720]/mp4[height<720]/mp4",  # Video format code. See yt-dl for more info.
            'outtmpl': dl_path + '%(uploader)s/%(title)s.%(ext)s',
            # BOOLS
            'restrictfilenames': True,  # Do not allow "&" and spaces in file names
            'no_warnings': True,    # Do not print out anything for warnings.
            'ignoreerrors': True,   # Do not stop on download errors.
            'nooverwrites': True,   # Prevent overwriting files.
            'writedescription': True,   # Write the video description to a .description file
            'writeinfojson': True,  # Write metadata to a json file
            'writethumbnail': True,     # Write the thumbnail image to a file
            'writeautomaticsub': True,  # Write the automatically generated subtitles to a file
            'writeannotations': True,   # Write video annotations
            'prefer_ffmpeg': True,      # Prefer ffmpeg for post processing
            'keepvideo': False,     # Keep post processing video files
            'verbose': False,   # Print additional info to stdout.
            'quiet': False,     # Do not print messages to stdout.
            'simulate': False,  # Do not download the video files.
            'skip_download': False,     # Skip the actual download of the video file
            'noplaylist': False,    # Download single video instead of a playlist if in doubt.
            'playlistrandom': False,    # Download playlist items in random order.
            'playlistreverse': False,  # Download playlist items in reverse order.
            'forceurl': False,  # Force printing final URL.
            'forcetitle': False,  # Force printing title.
            'forceid': False,  # Force printing ID.
            'forcethumbnail': False,  # Force printing thumbnail URL.
            'forcedescription': False,  # Force printing description.
            'forcefilename': False,  # Force printing final filename.
            'forceduration': False,  # Force printing duration.
            'forcejson': False,  # Force printing info_dict as JSON.
        }
        Json.encode(youtube_default_config, self.config_file)

    def handler(self):
        while True:
            clear()
            print(color.red(color.bold("----------------------DOWNLOAD-OPTIONS----------------------")))
            print(color.yellow(color.bold("filters")) + ") Set download filters      " + color.red(color.bold("|")))
            print(color.yellow(color.bold("archive")) + ") Download archive options  " + color.red(color.bold("|")) +
                  "  " + color.yellow(color.bold(self.DownloadArchive(self.config_file).state(raw=False))))
            print(color.yellow(color.bold(" format")) + ") Set download format       " + color.red(color.bold("|")) +
                  "  " + color.yellow(color.bold(self.Format(self.config_file).get())))
            print(color.yellow(color.bold(" others")) + ") On or Off options         " + color.red(color.bold("|")))
            print(color.yellow(color.bold("  embed")) + ") Set embedding options     " + color.red(color.bold("|")))
            print(color.yellow(color.bold("  reset")) + ") Reset config to default   " + color.red(color.bold("|")))
            print(enter_to_return())
            download_options_choice = str(input(">:"))

            if download_options_choice == "":
                return
            elif download_options_choice == "format":
                self.Format(self.config_file).handler()
            elif download_options_choice == "others":
                self.Bool(self.config_file).handler()
            elif download_options_choice == "archive":
                self.DownloadArchive(self.config_file).handler()
            elif download_options_choice == "filters":
                pass    # TODO
            elif download_options_choice == "embed":
                self.PostProcessing(self.config_file).handler()
            elif download_options_choice == "reset":
                clear()
                print(color.yellow(color.bold("This will reset your config to default. ") +
                      color.yellow(color.bold("Proceed? [y/N]"))))
                reset_choice = str(input(">:"))
                if reset_choice in affirmative_choice:
                    self.make_default()
            else:
                clear()
                wait_input()
                continue

    # def master_popup(self):
    #     print(color.red(color.bold("You are editing the master download options.\n"
    #                                "These options will be the default for new groups and for non-group downloads."
    #                                "This will not effect or overwrite existing group options.")))
    #     wait_input()


class Base64:
    @staticmethod
    def encode64(password):
        if isinstance(password, str):
            return base64.b64encode(password.encode()).decode()
        else:
            return base64.b64encode(str(password).encode()).decode()

    @staticmethod
    def decode64(password):
        if isinstance(password, str):
            return base64.b64decode(password.encode()).decode()
        else:
            return base64.b64decode(str(password).encode()).decode()


class CreateTorrent:
    class Trackers:
        def __init__(self):
            self.trackers_config_path = ConfigPath().get() + "torrents/trackers.json"

        def make_default(self):
            default_trackers = [
                "udp://tracker4.itzmx.com:2710/announce",
                "udp://tracker2.itzmx.com:6961/announce",
                "https://t.quic.ws:443/announce",
                "https://tracker.fastdownload.xyz:443/announce",
                "http://torrent.nwps.ws:80/announce",
                "udp://explodie.org:6969/announce",
                "http://tracker2.itzmx.com:6961/announce",
                "https://tracker.gbitt.info:443/announce",
                "http://tracker4.itzmx.com:2710/announce",
                "udp://tracker.trackton.ga:7070/announce",
                "udp://tracker.tvunderground.org.ru:3218/announce",
                "http://explodie.org:6969/announce",
                "http://open.trackerlist.xyz:80/announce",
                "udp://retracker.baikal-telecom.net:2710/announce",
                "http://open.acgnxtracker.com:80/announce",
                "udp://tracker.swateam.org.uk:2710/announce",
                "udp://tracker.iamhansen.xyz:2000/announce",
                "http://tracker.gbitt.info:80/announce",
                "udp://retracker.lanta-net.ru:2710/announce",
                "http://tracker.tvunderground.org.ru:3218/announce",
                "udp://retracker.netbynet.ru:2710/announce",
                "udp://tracker.supertracker.net:1337/announce",
                "udp://ipv4.tracker.harry.lu:80/announce",
                "udp://tracker.uw0.xyz:6969/announce",
                "udp://zephir.monocul.us:6969/announce",
                "udp://tracker.moeking.me:6969",
                "udp://tracker.filemail.com:6969/announce",
                "udp://tracker.filepit.to:6969/announce",
                "wss://tracker.openwebtorrent.com:443/announce",
                "http://gwp2-v19.rinet.ru:80/announce",
                "http://vps02.net.orel.ru:80/announce",
                "http://tracker.port443.xyz:6969/announce",
                "http://mail2.zelenaya.net:80/announce",
                "http://open.acgtracker.com:1096/announce",
                "http://tracker.vivancos.eu/announce",
                "udp://carapax.net:6969/announce",
                "udp://tracker.novg.net:6969/announce",
                "http://tracker.novg.net:6969/announce",
                "http://carapax.net:6969/announce",
                "udp://torrentclub.tech:6969/announce",
                "udp://home.penza.com.ru:6969/announce",
                "udp://tracker.dyn.im:6969/announce",
                ]
            return Json.encode(default_trackers, self.trackers_config_path)

        def get(self):
            try:
                return Json.decode(self.trackers_config_path)
            except FileNotFoundError:
                self.make_default()
                return self.get()

        def update(self, new_list):
            return Json.encode(new_list, self.trackers_config_path)

    def __init__(self):
        self.source_str = "mgtow-archive"
        self.comment_str = "Videos downloaded using mgtow-archive, github project page: " \
                           "https://github.com/PhoenixK7PB/mgtow-archive"
        self.created_by_str = "https://github.com/PhoenixK7PB/mgtow-archive"
        self.exclude = [".torrent"]

    def make(self, path, trackers, save_torrent_path, piece_size=None):
        torrent = Torrent(path=path, trackers=trackers, piece_size=piece_size, exclude=self.exclude,
                          source=self.source_str, comment=self.comment_str, created_by=self.created_by_str,
                          creation_date=datetime.now())
        torrent.generate()
        with open(save_torrent_path, 'wb') as file:
            torrent.save(file)

    def generate_bit_size(self, path, trackers, piece_size=None):
        torrent = Torrent(path=path, trackers=trackers, piece_size=piece_size, exclude=self.exclude,
                          source=self.source_str, comment=self.comment_str, created_by=self.created_by_str)
        return torrent.get_info()


class Qbittorrent:
    def __init__(self):
        self.torrent_config_path = ConfigPath().get() + "torrents/" + "torrent_config.json"
        self.torrent_config_file = self.get_config()
        self.client_instance = self.get_client_instance()

    def make_default_config(self):
        default_config = {
            "ip": "localhost",
            "port": "8080",
            "username": "",
            "password": "",
        }
        Json.encode(default_config, self.torrent_config_path)
        self.get_config()

    def get_config(self):
        try:
            return Json.decode(self.torrent_config_path)
        except FileNotFoundError:
            self.make_default_config()
            return self.get_config()

    def update_config(self, new_config_file):
        return Json.encode(new_config_file, self.torrent_config_path)

    def get_client_instance(self):
        host = self.torrent_config_file["ip"] + ":" + self.torrent_config_file["port"]
        username = self.torrent_config_file["username"]
        password = Base64.decode64(self.torrent_config_file["password"])
        return qbittorrentapi.Client(host=host, username=username, password=password)

    def client_auth_log_in(self):
        """
        Check login credentials
        :return: If login successful returns True, If login failed returns False
        """
        try:
            self.client_instance.auth_log_in(username=self.torrent_config_file["username"],
                                             password=Base64.decode64(self.torrent_config_file["password"]))
            return True
        except qbittorrentapi.APIConnectionError:
            return False
        except qbittorrentapi.LoginFailed:
            return False
        except qbittorrentapi.Forbidden403Error:
            return False

    def client_version(self):
        return self.client_instance.app_version()

    def list_mgtow_torrents(self):
        return self.client_instance.torrents_info(status_filter="all", category="mgtow-archive")

    def add_mgtow_torrent(self, torrent_file=None):
        return self.client_instance.torrents_add(torrent_files=torrent_file, category="mgtow-archive",
                                                 save_path=download_path)


class Groups:

    def __init__(self):
        self.groups_config_path = ConfigPath().get() + "groups/groups.json"
        if not os.path.exists(self.groups_config_path):
            Json.encode([], self.groups_config_path)

    def get(self):
        return Json.decode(self.groups_config_path)

    def update_json(self, new_config):
        Json.encode(new_config, self.groups_config_path)
        return self.get()

    def add(self, name):
        current_time = str(datetime.now().replace(microsecond=0))
        group_attr = {
            "name":                 name,
            "channels":             {},
            "create_time":          current_time,
            "last_download":        "",
            "config_path":          ConfigPath().get() + "groups/" + name + "_" +
                                    current_time.replace(" ", "-").replace(":", "-") + ".config.json"
        }
        current = self.get()
        current.append(group_attr)
        YTConfig(group_attr["config_path"]).make_default()
        return self.update_json(current)

    def remove(self, list_item):
        current = self.get()
        del current[list_item]
        return self.update_json(current)


def clear():
    """
    check if the machine is windows or linux,
    then clear the screen
    :return: a clean screen :)
    """

    if os.name == "nt":
        os.system('cls')

    else:
        os.system('clear')


def signal_handler(signal, frame):
    """
    handler of CTRL + C, prints a blank line, then exit
    :param signal:
    :param frame:
    :return: prints a blank line and exit
    """
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_stdin_settings)
    # this line is somewhat useful if the user exit during the "press any key" thing,
    # because the "stdin" will be set to raw mode, if the user hit CTRL + C, the
    # terminal stays in raw mode, with he will be stuck, using this line, if the user
    # hit CTRL + C, the "stdin" will be restored (using the original_stdin_settings variable)
    # and he will not get stuck
    print("\n")
    sys.exit(0)


def wait_input():
    """
    this function will detect any key press, until that happens, the program will wait
    """
    print("Press " + color.yellow(color.bold("any key")) + " to continue...")
    tty.setcbreak(sys.stdin)  # set "stdin" in raw mode, no line buffering from here
    user_input = None  # used to control while loop, the user input will be None,
    # if the user input changes, the while loop should be broken
    while user_input is None:  # while the user input is None (e.i. no key press detect on "stdin"), wait...
        user_input = sys.stdin.read(1)[0]  # this will be reading "stdin" until a key is detected
        clear()  # this will only be reached when a key is detected, until that happens, this will not be reached
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_stdin_settings)  # set "stdin" to default (no raw input)


def enter_to_return():
    return color.yellow(color.bold("Enter")) + " to " + color.yellow(color.bold("return")) + "."


def exit_func():
    """
    this function should be called when exiting, first clear the screen, then exit
    :return: exits program and clear the screen
    """

    clear()
    sys.exit(0)


def show_menu():
    """
    function that prints the main menu options
    :return: menu banner with options
    """

    print(color.red(" ███╗   ███╗ ██████╗████████╗ ██████╗ ██╗    ██╗"))
    print(color.red(" ████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗██║    ██║"))
    print(color.red(" ██╔████╔██║██║  ███╗  ██║   ██║   ██║██║ █╗ ██║"))
    print(color.red(" ██║╚██╔╝██║██║   ██║  ██║   ██║   ██║██║███╗██║"))
    print(color.red(" ██║ ╚═╝ ██║╚██████╔╝  ██║   ╚██████╔╝╚███╔███╔╝"))
    print(color.red(" ╚═╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝  "))
    print(color.red(""))
    print(color.red("    █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗"))
    print(color.red("   ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝"))
    print(color.red("   ███████║██████╔╝██║     ███████║██║██║   ██║█████╗"))
    print(color.red("   ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝"))
    print(color.red("   ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗"))
    print(color.red("   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝"))
    print("                 by " + color.red(color.bold("PhoenixK7PB")))
    print(color.yellow(color.bold("1")) + ") Download video/playlist/channel  " +
          color.red(color.bold("|")) + "  " + color.yellow(color.bold("conf")) + ") Set download options")
    print(color.yellow(color.bold("2")) + ") Groups                           " +
          color.red(color.bold("|")) + "  " + color.yellow(color.bold("path")) + ") Set download path")
    print(color.yellow(color.bold("3")) + ") qBittorrent interface (v4.1+)    " +
          color.red(color.bold("|")) + "  " + color.yellow(color.bold("sort")) + ") Set sorting type")
    print(color.yellow(color.bold("0")) + ") Exit                             " +
          color.red(color.bold("|")) + "  ")


def get_channel_size(channel_path):
    channel_size = 0

    # use the walk() method to navigate through directory tree
    for dirpath, dirnames, filenames in os.walk(channel_path):
        for i in filenames:
            # use join to concatenate all the components of path
            f = os.path.join(dirpath, i)

            # use getsize to generate size in bytes and add it to the total size
            channel_size += os.path.getsize(f)
    return channel_size

def set_sorting_type():
    clear()
    organizer.get_sort_type()
    print(color.red(color.bold("------------------------SORTING-TYPE------------------------")))
    print(color.red(color.bold("1) All-in-one")) +
          ": This type of sorting will result in everything\ndownloaded in just one folder, only organized by channels."
          "\n%s: PATH/channel_name/downloaded_files\n" % color.yellow(color.bold("i.e.")))
    print(color.red(color.bold("2) Sort-by-type")) +
          ": This type of sorting will result in 6 folders:\n"
          "annotations, descriptions, metadata, videos, thumbnails, subtitles."
          "\n%s: PATH/channel_name/file_type/downloaded_files\n" % color.yellow(color.bold("i.e.")))
    print("Current sorting: %s" % color.red(color.bold(organizer.get_sort_type())))
    print(enter_to_return())
    sorting_choice = str(input("Choose:\n>:"))
    clear()
    if sorting_choice == "":
        return
    elif sorting_choice.lower() == "1":
        organizer.all_in_one(download_path)
    elif sorting_choice.lower() == "2":
        organizer.sort_by_type(download_path)
    wait_input()


def youtube_download(url, youtube_config=None):
    """
    Download a channel using the config
    :param url: url of the channel being downloaded
    :param youtube_config: yt-dl config dict, get from MASTER if none is provided
    :return:
    """
    if youtube_config is None:
        youtube_dl.YoutubeDL(YTConfig().get()).download([url])
    if youtube_config is not None:
        youtube_dl.YoutubeDL(youtube_config).download([url])


def download_choice():
    """
    user interface for downloading videos
    :return:
    """
    clear()
    print(color.red(color.bold("--------------------------DOWNLOAD--------------------------")))
    videos_lst = []
    video_url = str(input("Type the URL to download.\n" + enter_to_return() + "\n>:"))

    if video_url == "":
        clear()
        return
    else:
        videos_lst.append(video_url)
        while True:
            download_another_one = str(input("\nDownload another one? [y/N]"))
            if download_another_one not in affirmative_choice:
                break
            else:
                video_url = str(input("\nType the URL to download.\n" + enter_to_return() + "\n>:"))
                if video_url == "":
                    clear()
                    break
                else:
                    videos_lst.append(video_url)

        # use_download_archive = str(input("\nUse the download archive file for not repeating downloads? [Y/n]"))
        # if use_download_archive in negative_choice:
        #     global download_archive
        #     download_archive = False
        #     del youtube_config["download_archive"]

    clear()
    print(color.yellow(color.bold("CTRL + C")) +
          " to cancel download.\n")
    sleep(0.5)

    for url in videos_lst:
        youtube_download(url)

    if warnings >= 1:
        print("\n   Download fished with %d warnings..." % warnings)
    if len(errors) >= 1:
        print(color.red(color.bold("\n   Download fished with %s errors..." % str(len(errors)))))
        for error in errors:
            print(color.red(color.bold(error)))

    if organizer.get_sort_type() == "sort_by_type":
        print(color.yellow(color.bold("\n Applying sorting type...")))
        organizer.sort_by_type(download_path)
        print(color.yellow(color.bold(" DONE!")))

    print()
    wait_input()


def groups_handler():
    while True:
        clear()
        print(color.red(color.bold("---------------------------GROUPS---------------------------")))
        print(color.yellow(color.bold("use")) + ") Select a group")
        print(color.yellow(color.bold("add")) + ") Add a new group")
        print(color.yellow(color.bold("del")) + ") Delete a group")
        print(enter_to_return())
        groups_choice = str(input(">:"))

        groups.get()

        if groups_choice == "":
            break

        elif groups_choice == "use":
            while True:
                clear()
                print(color.red(color.bold("------------------------SELECT-GROUP------------------------")))
                current_groups = groups.get()
                if len(current_groups) == 0:
                    print("No groups where found.")
                    wait_input()
                    break

                group_count = 0
                for group in current_groups:
                    group_count += 1
                    print("     %s) %s\n"
                          % (color.yellow(color.bold(str(group_count))), group["name"]))
                print("Type the number of the group to be selected.")
                print(enter_to_return())
                selected_group = input(">:")
                if selected_group == "":
                    break
                try:
                    used_group = int(selected_group) - 1
                    if used_group < 0:
                        raise IndexError
                    current_group = current_groups[used_group]
                except ValueError:
                    clear()
                    print("Only numbers are accepted.")
                    wait_input()
                    continue
                except IndexError:
                    clear()
                    print("Number selected does not correspond to any group.")
                    wait_input()
                    continue
                while True:
                    group_ytconfig = YTConfig(config_file=current_group["config_path"])

                    clear()
                    print(color.red(
                        color.bold("-------------------------GROUP-STATS------------------------")))
                    print("Group name: %s" % color.yellow(color.bold(current_group["name"])))
                    print("Creation date: %s" % color.yellow(color.bold(current_group["create_time"])))
                    print("Last download: %s" % color.yellow(color.bold(current_group["last_download"])))
                    print("%s channel(s)" % color.yellow(color.bold(str(len(current_group["channels"])))))
                    print(color.red(
                        color.bold("------------------------GROUP-ACTIONS-----------------------")))
                    print(color.yellow(color.bold("1")) + ") Download")
                    print(color.yellow(color.bold("2")) + ") Add channel(s)")
                    print(color.yellow(color.bold("3")) + ") Remove channel(s)")
                    print(color.yellow(color.bold("4")) + ") Rename group")
                    print(color.yellow(color.bold("5")) + ") Set download options")
                    print(enter_to_return())
                    group_action = str(input(">:"))
                    if group_action == "":
                        break
                    elif group_action == "1":
                        clear()
                        print(color.red(color.bold("-----------------------DOWNLOAD-GROUP-----------------------")))
                        if len(current_group["channels"]) == 0:
                            print("No channel to download")
                            wait_input()
                            continue

                        print(color.yellow(color.bold(str(len(current_group["channels"])))) +
                              " channel(s) will be downloaded. " +
                              color.yellow(color.bold("Proceed? [y/N]")))
                        download_channels_choice = str(input(">:"))
                        if download_channels_choice not in affirmative_choice:
                            continue
                        clear()
                        print(color.yellow(color.bold("CTRL + C")) + " to cancel download.")
                        sleep(0.5)
                        channel_count = 0
                        for channel in current_group["channels"]:
                            channel_count += 1
                            print("     \nChannel %d of %d" % (channel_count, len(current_group["channels"])))
                            print("     Channel: %s" % channel)
                            print("     URL: %s" % current_group["channels"][channel])
                            print()
                            sleep(0.25)
                        youtube_download(current_group["channels"][channel],
                                         youtube_config=YTConfig(current_group["config_path"]).get())

                        print("Updating last download date to: %s" % str(datetime.now().replace(microsecond=0)))
                        current_group["last_download"] = str(datetime.now().replace(microsecond=0))
                        groups.update_json(current_groups)

                        if warnings >= 1:
                            print("\n   Download fished with %d warnings..." % warnings)
                        if len(errors) >= 1:
                            print(color.red(color.bold("\n   Download fished with %s errors..." % str(len(errors)))))
                            for error in errors:
                                print(color.red(color.bold(error)))

                        if organizer.get_sort_type() == "sort_by_type":
                            print(color.yellow(color.bold("\n Applying sorting type...")))
                            organizer.sort_by_type(download_path)
                            print(color.yellow(color.bold(" DONE!")))

                        print()
                        wait_input()
                        return

                    elif group_action == "2":
                        while True:
                            clear()
                            print(color.red(color.bold("--------------------ADD-CHANNEL-TO-GROUP--------------------")))
                            print(color.yellow(color.bold("Leave blank to cancel.\n")))
                            channel_name = str(input(color.yellow(color.bold("Name")) + " of the channel?\n>:"))
                            channel_url = str(input(color.yellow(color.bold("\nLink")) + " of the channel?\n>:"))
                            if channel_name and channel_url != "":
                                current_group["channels"][channel_name] = channel_url
                                groups.update_json(current_groups)
                                add_another_channel_choice = str(input("\nAdd another channel? [y/N]\n>:"))
                                if add_another_channel_choice not in affirmative_choice:
                                    break
                            else:
                                break
                    elif group_action == "3":
                        while True:
                            clear()
                            print(color.red(color.bold("------------------REMOVE-CHANNEL-FROM-GROUP-----------------")))
                            if len(current_group["channels"]) == 0:
                                print("No channel was found")
                                wait_input()
                                break
                            else:
                                print("Found %s channel(s)\n"
                                      % color.yellow(color.bold(str(len(current_group["channels"])))))

                            channel_count = 0
                            channel_count_dict = dict()
                            for channel in current_group["channels"]:
                                channel_count += 1
                                print("      %s) Name: %s\n"
                                      "      URL:  %s\n" % (color.yellow(color.bold(str(channel_count))),
                                                            channel, current_group["channels"][channel]))
                                channel_count_dict[channel_count] = channel
                            print("Use '@ALL' to delete all groups %s" % color.yellow(color.bold("[CAUTION]")))
                            print("Type the number of a channel to be removed")
                            print(enter_to_return())
                            removed_channel = str(input(">:"))
                            if removed_channel == "":
                                break
                            elif removed_channel == "@ALL":
                                clear()
                                sure = str(input("Delete all channels selected. Proceed? [y/N]"))
                                if sure in affirmative_choice:
                                    current_group["channels"] = {}
                                    groups.update_json(current_groups)
                                    break
                                else:
                                    continue
                            try:
                                removed_channel = int(removed_channel)
                                del current_group["channels"][channel_count_dict[removed_channel]]
                            except ValueError:
                                clear()
                                print("Only numbers are accepted.")
                                wait_input()
                                continue
                            except KeyError:
                                clear()
                                print("Number selected does not correspond to any group.")
                                wait_input()
                                continue
                            groups.update_json(current_groups)
                    elif group_action == "4":
                        clear()
                        print(color.red(
                            color.bold("------------------------RENAME-GROUP------------------------")))
                        print("Current group name: %s" % color.yellow(color.bold(current_group["name"])))
                        print("Type the new group name")
                        print(enter_to_return())
                        new_name = str(input(">:"))
                        if new_name == "":
                            continue
                        current_group["name"] = new_name
                        groups.update_json(current_groups)
                    elif group_action == "5":
                        group_ytconfig.handler()
                    else:
                        clear()
                        wait_input()
                        continue
        elif groups_choice == "add":
            while True:
                clear()
                print(color.red(color.bold("--------------------------ADD-GROUP-------------------------")))
                print("Type the name of the new group.")
                print(enter_to_return())
                group_name = str(input(">:"))
                if group_name == "":
                    break
                else:
                    groups.add(group_name)
                    break
        elif groups_choice == "del":
            while True:
                clear()
                print(color.red(color.bold("------------------------DELETE-GROUP------------------------")))
                current_groups = groups.get()
                if len(current_groups) == 0:
                    print("No groups where found.")
                    wait_input()
                    break
                else:
                    print("Use '@ALL' to delete all groups %s\n" % color.yellow(color.bold("[CAUTION]")))
                    group_count = 0
                    for group in current_groups:
                        group_count += 1
                        print("     %s) %s\n"
                              % (color.yellow(color.bold(str(group_count))), group["name"]))
                    print("Type the number of the group to be deleted.")
                    print(enter_to_return())
                    removed_group = input(">:")
                    if removed_group == "":
                        break
                    elif removed_group == "@ALL":
                        clear()
                        sure = str(input("Delete all groups selected. Proceed? [y/N]"))
                        if sure in affirmative_choice:
                            for group in current_groups:
                                os.remove(group["config_path"])  # remove each group config
                            groups.update_json([])  # wipe groups.json
                            break
                    try:
                        deleted_group = int(removed_group) - 1
                        if deleted_group < 0:
                            raise IndexError
                    except ValueError:
                        clear()
                        print("Only numbers are accepted.")
                        wait_input()
                        continue
                    except IndexError:
                        clear()
                        print("Number selected does not correspond to any group.")
                        wait_input()
                        continue
                    os.remove(current_groups[deleted_group]["config_path"])  # remove group config
                    groups.remove(deleted_group)    # remove group from groups.config
                    break
        else:
            clear()
            wait_input()


def torrent_handler():
    while True:
        clear()
        print(color.red(color.bold("----------------------TORRENT-INTERFACE---------------------")))
        print("Login status: %s" % color.green(color.bold("Successful  |  Client Version: %s"
                                                          % qbittorrent.client_version()))) if qbittorrent. \
            client_auth_log_in() else print("Login status: %s  |  Enable bypass for clients on the localhost."
                                            % color.red(color.bold("Failed")))
        print()
        print(color.yellow(color.bold("1")) + ") Create torrent                   " +
              color.red(color.bold("|")) + "")
        print(color.yellow(color.bold("2")) + ") List mgtow-archive torrents      " +
              color.red(color.bold("|")) + "")
        print(color.yellow(color.bold("3")) + ") Change login                     " +
              color.red(color.bold("|")) + "  %s:%s"
              % (qbittorrent.get_config()["ip"], qbittorrent.get_config()["port"]))
        print(color.yellow(color.bold("4")) + ") Change trackers                  " +
              color.red(color.bold("|")) + "  %d trackers"
              % (len(create_torrent.Trackers().get())))
        print(enter_to_return())
        torrent_choice = str(input(">:"))

        if torrent_choice == "1":
            while True:
                clear()
                print(color.red(color.bold("-------------------------ADD-TORRENT------------------------")))

                if not qbittorrent.client_auth_log_in():
                    print(color.red(color.bold("Login Failed. Check login credentials.")))
                    wait_input()
                    return

                if len(organizer.get_downloaded_channels(download_path)) == 0:
                    print(color.yellow(color.bold("No channels were found.")))
                    wait_input()
                    return

                count = 0
                count_list = []
                channel_dict = dict()

                for channel in organizer.get_downloaded_channels(download_path):
                    count += 1
                    count_list.append(str(count))
                    channel_dict[str(count)] = channel

                for channel in channel_dict:
                    print("%s)  Name: %s\n"
                          "    Path: %s\n"
                          "    Size: %.2fGB\n" % (color.yellow(color.bold(channel)),
                                                  channel_dict[channel].rsplit("/", 1)[1],
                                                  channel_dict[channel],
                                                  get_channel_size(channel_dict[channel]) / 1073741824))
                print(enter_to_return())
                add_channel_choice = str(input(">:"))

                if add_channel_choice == "":
                    return
                elif add_channel_choice in count_list:
                    clear()
                    print(color.red(color.bold("-------------------------ADD-TORRENT------------------------")))
                    add_torrent_continue = str(input("Are you sure you want to add channel %s to a .torrent? [y/N]"
                                                     % channel_dict[add_channel_choice].rsplit("/", 1)[1]))
                    if add_torrent_continue not in affirmative_choice:
                        return

                    clear()
                    print(color.red(color.bold("-------------------------ADD-TORRENT------------------------")))
                    if not os.path.exists(download_path + "torrents/"):
                        os.makedirs(download_path + "torrents/")
                    torrent_file_path = download_path + "torrents/"\
                                                      + channel_dict[add_channel_choice].rsplit("/", 1)[1] + ".torrent"
                    trackers = create_torrent.Trackers().get()
                    print(color.yellow(color.bold("Adding channel '" +
                                                  channel_dict[add_channel_choice].rsplit("/", 1)[1]
                                                  + "' to a .torrent\n")))
                    print(color.yellow(color.bold("Generating optimal bit size based on ~1500 pieces.")))
                    bit_size_info = create_torrent.generate_bit_size(path=channel_dict[add_channel_choice],
                                                                     trackers=trackers, piece_size=None)
                    print(color.yellow(color.bold("Using bit size of %dkb.\n" % (bit_size_info[2] // 1000))))
                    print(color.yellow(color.bold("Using %d trackers\n" % len(trackers))))
                    print(color.red(color.bold("     This could take a while depending on the channel size.\n"
                                               "     DO NOT EXIT!\n")))
                    channel_clock = process_time()
                    create_torrent.make(path=channel_dict[add_channel_choice], trackers=trackers, piece_size=None,
                                        save_torrent_path=torrent_file_path)
                    print(color.red(color.bold("\nSaved the .torrent file to %s\n" % torrent_file_path)))
                    print(color.red(color.bold("Finished .torrent file in %.0fs\n") % channel_clock))
                    print("\nAdding channel .torrent to qbittorrent... ", end="")
                    print(color.yellow(color.bold(qbittorrent.add_mgtow_torrent(torrent_file=torrent_file_path))))
                    wait_input()

                else:
                    clear()
                    wait_input()

        elif torrent_choice == "2":
            clear()
            print(color.red(color.bold("-------------------MGTOW-ARCHIVE-TORRENTS-------------------")))
            if not qbittorrent.client_auth_log_in():
                print(color.red(color.bold("Login Failed. Check login credentials.")))
                wait_input()
                return

            mgtow_torrents = qbittorrent.list_mgtow_torrents()
            if len(mgtow_torrents) == 0:
                print(color.yellow(color.bold("No torrents were found with the category 'mgtow-archive'.")))
                wait_input()
                return

            print("Found %s torrents with category 'mgtow-archive'."
                  % color.yellow(color.bold(str(len(mgtow_torrents)))))
            print()
            count = 0
            for torrent in mgtow_torrents:
                count += 1
                print("     Torrent %s of %s" % (count, len(mgtow_torrents)))
                print("     Name: %s" % torrent.name)
                print("     Size: %.2fGB" % (torrent.size / 1073741824))
                print()
            wait_input()

        elif torrent_choice == "3":
            clear()
            print(color.red(color.bold("BE CAREFUL WHEN CHANGING THE LOGIN IP AND PORT!"
                                       "\nANY MISLEADING CHANGES COULD BE CATASTROPHIC!"
                                       "\nRemove the file '~/.config/mgtow-archive/torrent_config.json' "
                                       "if any errors occur.")))
            wait_input()
            while True:
                clear()
                print(color.red(color.bold("------------------------CHANGE-LOGIN------------------------")))
                print("Login status: %s" % color.green(color.bold("Successful  |  Client Version: %s"
                                                                  % qbittorrent.client_version()))) if qbittorrent. \
                    client_auth_log_in() else print("Login status: %s" % color.red(color.bold("Failed")))
                print()
                print(color.yellow(color.bold("1")) + ") IP:        %s" % qbittorrent.get_config()["ip"])
                print(color.yellow(color.bold("2")) + ") Port:      %s" % qbittorrent.get_config()["port"])
                print(color.yellow(color.bold("3")) + ") Username:  %s" % qbittorrent.get_config()["username"])
                print(color.yellow(color.bold("4")) + ") Password:  %s" %
                      Base64.decode64(qbittorrent.get_config()["password"]))
                print(color.yellow(color.bold("0")) + ") Reset login to default")
                print(enter_to_return())
                change_login_choice = str(input(">:"))

                if change_login_choice == "1":
                    clear()
                    print(color.red(color.bold("--------------------------CHANGE-IP-------------------------")))
                    print(color.yellow(color.bold("Leave everything blank to cancel.\n")))
                    print("Current IP: %s" % qbittorrent.get_config()["ip"])
                    print("\nEnter the new IP to the used.")
                    new_ip = str(input(">:"))
                    if new_ip == "":
                        continue
                    else:
                        new_config = qbittorrent.get_config()
                        new_config["ip"] = new_ip
                        qbittorrent.update_config(new_config)

                elif change_login_choice == "2":
                    clear()
                    print(color.red(color.bold("-------------------------CHANGE-PORT------------------------")))
                    print(color.yellow(color.bold("Leave everything blank to cancel.\n")))
                    print("Current port: %s" % qbittorrent.get_config()["port"])
                    print("\nEnter the new port to the used.")
                    new_port = str(input(">:"))
                    if new_port == "":
                        continue
                    else:
                        new_config = qbittorrent.get_config()
                        new_config["port"] = new_port
                        qbittorrent.update_config(new_config)

                elif change_login_choice == "3":
                    clear()
                    print(color.red(color.bold("-----------------------CHANGE-USERNAME----------------------")))
                    print(color.yellow(color.bold("Leave everything blank to cancel.\n")))
                    print("Current username: %s" % qbittorrent.get_config()["username"])
                    print("\nEnter the new username to the used.")
                    new_username = str(input(">:"))
                    if new_username == "":
                        continue
                    else:
                        new_config = qbittorrent.get_config()
                        new_config["username"] = new_username
                        qbittorrent.update_config(new_config)

                elif change_login_choice == "4":
                    clear()
                    print(color.red(color.bold("-----------------------CHANGE-PASSWORD----------------------")))
                    print(color.yellow(color.bold("Leave everything blank to cancel.\n")))
                    print("Current password: %s" % Base64.decode64(qbittorrent.get_config()["password"]))
                    print("\nEnter the new password to the used.")
                    new_password = str(input(">:"))
                    if new_password == "":
                        continue
                    else:
                        new_config = qbittorrent.get_config()
                        new_config["password"] = Base64.encode64(new_password)
                        qbittorrent.update_config(new_config)

                elif change_login_choice == "0":
                    clear()
                    print(color.red(color.bold("--------------------RESET-TORRENT-CONFIG--------------------")))
                    torrent_reset_config_choice = str(input("This will undo all changes to the torrent configuration. "
                                                            "Proceed? [y/N]"))
                    if torrent_reset_config_choice in affirmative_choice:
                        qbittorrent.make_default_config()
                    else:
                        continue

                elif change_login_choice == "":
                    break
                else:
                    clear()
                    wait_input()

        elif torrent_choice == "4":
            while True:
                clear()
                print(color.red(color.bold("-----------------------CHANGE-TRACKERS----------------------")))
                print("%s trackers in use" % (color.yellow(color.bold(str(len(create_torrent.Trackers().get()))))))
                print()
                print(color.yellow(color.bold("1")) + ") See trackers                   ")
                print(color.yellow(color.bold("2")) + ") Add trackers                   ")
                print(color.yellow(color.bold("3")) + ") Remove trackers                ")
                print(enter_to_return())
                change_trackers_choice = str(input(">:"))
                if change_trackers_choice == "":
                    break

                elif change_trackers_choice == "1":
                    clear()
                    print(color.red(color.bold("------------------------SEE-TRACKERS------------------------")))
                    tracker_count = 0
                    for tracker in create_torrent.Trackers().get():
                        tracker_count += 1
                        print("     %s) %s" % (color.yellow(color.bold(str(tracker_count))), tracker))
                    wait_input()

                elif change_trackers_choice == "2":
                    clear()
                    print(color.red(color.bold("------------------------ADD-TRACKERS------------------------")))
                    new_trackers = []
                    print(enter_to_return())
                    print("Type the new tracker.")
                    new_tracker = str(input(">:"))
                    if new_tracker == "":
                        continue
                    else:
                        new_trackers.append(new_tracker)
                        while True:
                            add_another_tracker = str(input("\nAdd another one? [y/N]"))
                            if add_another_tracker not in affirmative_choice:
                                break
                            else:
                                new_tracker = str(input("\nType the new tracker.\n" + enter_to_return() + "\n>:"))
                                if new_tracker == "":
                                    clear()
                                    break
                                else:
                                    new_trackers.append(new_tracker)

                        old_trackers = create_torrent.Trackers().get()
                        for tracker in new_trackers:
                            old_trackers.append(tracker)
                        create_torrent.Trackers().update(old_trackers)

                elif change_trackers_choice == "3":
                    while True:
                        clear()
                        print(color.red(color.bold("-----------------------REMOVE-TRACKERS----------------------")))

                        old_trackers = create_torrent.Trackers().get()
                        tracker_count = 0
                        for tracker in old_trackers:
                            tracker_count += 1
                            print("     %s) %s" % (color.yellow(color.bold(str(tracker_count))), tracker))

                        remove_tracker = input("Type the number of the tracker to be deleted.\n>:")
                        print(enter_to_return())
                        if remove_tracker == "":
                            break
                        try:
                            deleted_tracker = int(remove_tracker) - 1
                            old_trackers.pop(deleted_tracker)
                            create_torrent.Trackers().update(old_trackers)
                        except ValueError:
                            clear()
                            print("Only numbers are accepted.")
                            wait_input()
                        except IndexError:
                            clear()
                            print("Number selected does not correspond to any tracker.")
                            wait_input()

                else:
                    clear()
                    wait_input()

        elif torrent_choice == "":
            break
        else:
            clear()
            wait_input()


if __name__ == "__main__":
    init(autoreset=True)
    signal.signal(signal.SIGINT, signal_handler)

    # start routines
    ConfigPath().init_sub_folders()

    # init instances
    color = Color()
    organizer = Organizer()
    create_torrent = CreateTorrent()
    qbittorrent = Qbittorrent()
    ytconfig = YTConfig()
    download_path = YTConfig.DownloadPath().get()
    download_format = YTConfig.Format()
    groups = Groups()

    while True:
        clear()
        show_menu()  # show menu
        choice = input(">:")  # wait for user input

        if choice == "":
            clear()
            continue

        try:
            choice = int(choice)  # try to convert choice(str) to choice(int),
            # this is needed because the normal input is a str

        except ValueError:  # if the int() parser cant convert, raises a ValueError, this take care if it
            if choice.lower() == "conf":
                ytconfig.handler()
                continue

            elif choice.lower() == "path":
                YTConfig.DownloadPath().set()
                continue

            elif choice.lower() == "sort":
                set_sorting_type()
                continue

            elif choice.lower() == "q":
                exit_func()

            else:  # if user type something that is not an option, ignore and wait for another input
                clear()
                wait_input()
                continue

        if choice == 1:
            download_choice()

        elif choice == 2:
            groups_handler()

        elif choice == 3:
            torrent_handler()

        elif choice == 0:
            exit_func()
        else:
            clear()
            wait_input()
