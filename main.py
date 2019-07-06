#  ███╗   ███╗ ██████╗████████╗ ██████╗ ██╗    ██╗     █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗
#  ████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗██║    ██║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝
#  ██╔████╔██║██║  ███╗  ██║   ██║   ██║██║ █╗ ██║    ███████║██████╔╝██║     ███████║██║██║   ██║█████╗
#  ██║╚██╔╝██║██║   ██║  ██║   ██║   ██║██║███╗██║    ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝
#  ██║ ╚═╝ ██║╚██████╔╝  ██║   ╚██████╔╝╚███╔███╔╝    ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗
#  ╚═╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝
# https://github.com/PhoenixK7PB/mgtow-archive
#
# TODO: handling path for windows machines (home path)
# TODO: make one more advanced progress bar
# TODO: add choose option for format when downloading
# TODO: make a list of downloaded video, when updating use data list for
#  not repeating downloads
# TODO: make a max of video length for downloading using yt.lenght
# TODO: make a "Config" file for storing path and downloaded channels
#  (last update, total videos, etc)
# TODO: use colorama for font color
# TODO: Make a title for every "section" of the program (like lazy script) using 45 chars
# like ------------------------------------------------------------
# TODO: add a logger that saves every error and prints it at the end of the download

import youtube_dl
from pathlib import Path
import signal
import sys
import os
import json
import threading

affirmative_choice = ["y", "yes", "s", "sim", "yeah", "yah", "ya"]
negative_choice = ["n", "no", "nao", "na", "nop", "nah"]


class Json:
    """
    Handle JSON requests.
    """
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

    def decode(read_filename, return_content=1):
        """
        Read a .json file and transfer the data to a global variable
        :param read_filename: Name of the file to be read, NEED the .json at the end
        :param return_content:  1 (default) for not returning the content inside the json file
                                0 for returning the content at the end
        :return: Make a global variable called "json_decode", all content in there
        If return_content is 1, does NOT return anything
        If return_content is 0, DOES return the content
        """
        global json_decode

        with open(read_filename) as json_data:
            json_decode = json.load(json_data)

            if return_content == 0:
                return json_decode


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
    print("\n")
    sys.exit(0)


def wait_input():
    clear()
    input("Press any key to continue...")
    clear()


def exit_func():
    exit(clear())


def show_menu():
    """
    :return: menu banner with options
    """
    print(" ███╗   ███╗ ██████╗████████╗ ██████╗ ██╗    ██╗")
    print(" ████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗██║    ██║")
    print(" ██╔████╔██║██║  ███╗  ██║   ██║   ██║██║ █╗ ██║")
    print(" ██║╚██╔╝██║██║   ██║  ██║   ██║   ██║██║███╗██║")
    print(" ██║ ╚═╝ ██║╚██████╔╝  ██║   ╚██████╔╝╚███╔███╔╝")
    print(" ╚═╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝  ")
    print("")
    print("    █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗")
    print("   ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝")
    print("   ███████║██████╔╝██║     ███████║██║██║   ██║█████╗")
    print("   ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝")
    print("   ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗")
    print("   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝")
    print("")
    print("1) Download video/playlist/channel   |  conf) Configure yt-dl        ")
    print("2) Channels                          |  path) Set download path      ")
    # print("4) Make a torrent                    |                               ")
    print("0) Exit                              |                               ")


def youtube_hooker(video):

    if len(video) <= 4:
        global founded_videos
        founded_videos += 1
        print("         FOUND ONE!!!")
    if founded_videos >= 3:
        print("EXITING CURRENT THREAD!")
        # TODO



def make_path():
    clear()
    print("Creating a JSON file containing the path...\n")
    path_name = str(input("Type the full path for storing the videos... Enter to use your home path.\n>:"))

    if path_name == "":
        clear()
        if not os.path.exists(str(Path.home())):
            os.makedirs(str(Path.home()))
        Json.encode(str(Path.home()), "path.json")

    else:
        clear()
        if not os.path.exists(path_name):
            os.makedirs(path_name)
        Json.encode(path_name, "path.json")

    global path
    path = Json.decode("path.json", return_content=0)

    print("New path is:", path)
    input("\nEnter to continue.\n")
    clear()


def get_path():
    """
    Should get a "path" for storing the downloaded content
    Uses json_handler ,
    If not data could be found, calls make_path()
    :return: Make a global variable called "path",
    """
    try:
        global path
        path = Json.decode("path.json", return_content=0)
        return path

    except FileNotFoundError:
        make_path()
        return path


def change_path():
    """

    :return:
    """
    clear()
    print("Change path selected...\n")
    get_path()
    print("Your current path is: ", path)
    new_path = str(input("\nType your new path... Enter to return.\n>:"))
    if new_path == "":
        clear()
        return
    else:
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        Json.encode(new_path, "path.json")
        clear()
        print("New path is:", path)
        input("\nEnter to continue.\n")
        clear()
        return


youtube_config = {      # --------------------CHANGE THIS!!!--------------------- #

    'format':                   'bestaudio/best',   # Video format code. See options.py for more information.
    'outtmpl':                  get_path() + '/%(uploader)s/%(title)s.%(ext)s',
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

yt_list_of_channels_config = {      # --------------------CHANGE THIS!!!--------------------- #

    'progress_hooks': [youtube_hooker],     # DONT CHANGE

    'format':                   'bestaudio/best',   # Video format code. See options.py for more information.
    'outtmpl':                  get_path() + '/%(uploader)s/%(title)s.%(ext)s',
    'restrictfilenames':        True,               # Do not allow "&" and spaces in file names
    'no_warnings':              True,               # Do not print out anything for warnings.
    'ignoreerrors':             False,               # Do not stop on download errors.
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

youtube_default_config = {

    'format':                   'bestaudio/best',   # Video format code. See options.py for more information.
    'outtmpl':                  get_path() + '/%(uploader)s/%(title)s.%(ext)s',
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


def make_default_config():
    Json.encode(youtube_default_config, "yt_config.json")
    global yt_config
    yt_config = Json.decode("yt_config.json", return_content=0)


def apply_config():
    Json.encode(youtube_config, "yt_config.json")
    global yt_config
    yt_config = Json.decode("yt_config.json", return_content=0)


def get_config():
    """
    access the json configuration file and make a global variable called "yt_config"
    :return: None
    """
    try:
        global yt_config
        yt_config = Json.decode("yt_config.json", return_content=0)
    except FileNotFoundError:
        make_default_config()


def config_handler():
    config_maintainer = True

    while config_maintainer:
        clear()
        get_config()
        print("Enter to return...\n")
        print("Youtube-dl version: %s" % youtube_dl.update.__version__)
        print("\napply) Apply your changes (from code to disk) using 'youtube_config'")
        print("\nreset) Reset to default the config file for you")
        print("\nsee) See the config file")
        print("")
        config_choice = str(input("\n>:"))
        if config_choice == "":
            return

        elif config_choice.lower() == 'apply':
            clear()
            apply_config()
            input("Config wrote down to disk... Enter to continue.\n")
            return

        elif config_choice.lower() == 'reset':
            clear()
            sure = str(input("Resetting the config file will wipe out all changes to it. Are you sure? [y/n]\n>:"))
            if sure in affirmative_choice:
                make_default_config()
                continue
            else:
                continue

        elif config_choice.lower() == 'see':
            clear()
            get_config()
            print("Found %d options...\n")
            for config in yt_config:
                print("%s: %s" % (str(config), str(yt_config[config])))
            input()


def get_channels():
    try:
        global channels
        channels = Json.decode("channels.json", return_content=0)

    except FileNotFoundError:
        clear()
        input("No channels found... maybe add one?")
        return False


def add_channel(channel_name, channel_url):
    try:
        old_channels = Json.decode("channels.json", return_content=0)
        old_channels[channel_name] = channel_url
        Json.encode(old_channels, "channels.json")
        get_channels()

    except FileNotFoundError:
        new_channel = {channel_name: channel_url}
        Json.encode(new_channel, "channels.json")
        get_channels()


def youtube_download(url):
    """
    Download a channel using the normal config
    :param url: url of the channel being downloaded
    :return: nothing
    """
    youtube_dl.YoutubeDL(yt_config).download([url])


def youtube_channel_download(url):
    """
    Download a channel using the config for channels (calls a progress hooker)
    :param url: url of the channel being downloaded
    :return: nothing
    """
    youtube_dl.YoutubeDL(yt_list_of_channels_config).download([url])


if __name__ == "__main__":
    maintainer = True

    while maintainer:
        signal.signal(signal.SIGINT, signal_handler)
        clear()
        get_config()
        get_path()
        clear()
        show_menu()  # show menu
        choice = input("\n>: ")  # wait for user input

        if choice == "":
            clear()
            continue

        try:
            choice = int(choice)  # try to convert choice(str) to choice(int),
            # this is needed because the normal input is a str

        except ValueError:  # if the int() parser cant convert, raises a ValueError, this take care if it
            if choice.lower() == "path":
                change_path()
                continue

            elif choice.lower() == "conf":
                config_handler()
                continue

            else:   # if user type something that != path, ignore and return to main menu
                clear()  # clear the screen
                input("Press any key to go back...\n")  # wait for user input
                clear()
                continue  # goes right back in the loop, skip the "else:" later on, save time

        if choice == 1:
            clear()
            print("--------------------------DOWNLOAD--------------------------")
            video_url = str(input("Type URL to download.\n>: "))  # wait for user input,

            if video_url == "":  # validate user input,if it's empty, go to the menu
                clear()
                continue

            youtube_download(video_url)
            input("\n\nFinished. Enter to continue.\n\n")

        elif choice == 2:
            channel_maintainer = True

            while channel_maintainer:
                clear()
                print("--------------------------CHANNELS--------------------------")
                print("1) Search for new videos in every channel")
                print("2) View channels")
                print("3) Add a channel")
                print("b) Go back")
                channel_choice = input("\n>:")

                try:
                    channel_choice = int(channel_choice)

                except ValueError:
                    if channel_choice.lower() == "b":
                        break
                    else:
                        wait_input()

                if channel_choice == 1:
                    clear()
                    print("----------------------DOWNLOAD-CHANNELS---------------------")
                    if get_channels() is False:
                        continue

                    print("Found %d channels...\n" % len(channels))
                    download_channels_choice = str(input("All videos from all channels will be downloaded. "
                                                         "Do you want to continue? [y/N]\n>:"))
                    if download_channels_choice not in affirmative_choice:
                        clear()
                        continue

                    clear()
                    channel_count = 0
                    for channel in channels:
                        global founded_videos
                        channel_count += 1
                        print()
                        print("     Channel %d of %d" % (channel_count, len(channels)))
                        print("     Channel: %s" % channel)
                        print("     URL: %s" % channels[channel])
                        print()
                        founded_videos = 0
                        threading.Thread(target=youtube_channel_download, args=(channels[channel],)).start()




                elif channel_choice == 2:
                    clear()
                    if get_channels() is False:
                        continue

                    print("------------------------VIEW-CHANNELS-----------------------")
                    print("Found %d channels...\n" % len(channels))
                    count = 0

                    for channel in channels:
                        count += 1
                        print("     %d) %s == %s" % (count, channel, channels[channel]))
                    input("\nPress any key to continue...")
                    # TODO add options to edit, remove and download specific channels

                elif channel_choice == 3:
                    add_channel_maintainer = True

                    while add_channel_maintainer:
                        clear()
                        print("-------------------------ADD-CHANNEL------------------------")
                        channel_name = str(input("Name of the channel?\n>:"))
                        channel_url = str(input("\nFull channel url?\n>:"))
                        add_channel(channel_name, channel_url)

                        add_another_channel_choice = str(input("\nAdd another channel? [y/N]\n>:"))
                        if add_another_channel_choice not in affirmative_choice:
                            clear()
                            break

        elif choice == 3:
            print
            "Menu 4 has been selected"
            ## You can add your code or functions here
        elif choice == 4:
            print
            "Menu 5 has been selected"
            ## You can add your code or functions here
            loop = False  # This will make the while loop to end as not value of loop is set to False
        elif choice == 0:
            exit_func()
        else:
            wait_input()
