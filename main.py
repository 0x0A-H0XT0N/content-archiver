#  ███╗   ███╗ ██████╗████████╗ ██████╗ ██╗    ██╗     █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗
#  ████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗██║    ██║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝
#  ██╔████╔██║██║  ███╗  ██║   ██║   ██║██║ █╗ ██║    ███████║██████╔╝██║     ███████║██║██║   ██║█████╗
#  ██║╚██╔╝██║██║   ██║  ██║   ██║   ██║██║███╗██║    ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝
#  ██║ ╚═╝ ██║╚██████╔╝  ██║   ╚██████╔╝╚███╔███╔╝    ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗
#  ╚═╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝
# https://github.com/PhoenixK7PB/mgtow-archive
#
# TODO: handling path for windows machines (home path)
# TODO: printing filesize (MB) of video before downloading
# TODO: make callback functions for completed downloads,
#  displaying remaining videos (if channel or playlist), time elapsed
# TODO: make one more advanced progress bar
# TODO: add choose option for format when downloading
# TODO: handle exceptions from pytube
#  and making a file handler function for moving and etc
# TODO: make a list of downloaded video, when updating use data list for
#  not repeating downloads
# TODO: make a max of video length for downloading using yt.lenght
# TODO: make a "Config" file for storing path and downloaded channels
#  (last update, total videos, etc)
# TODO: use colorama for font color
# TODO: pass everything to yt-dl, currently pytube
#  does not support age restricted videos.
# TODO: re-write exit functions, put clear() inside exit() e.g. exit(clear)

import youtube_dl
from pathlib import Path
import os
import json

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
    print("2) Check for new videos              |  path) Set download path      ")
    print("3) See channels                      |                               ")
    print("4) Add channel                       |                               ")
    print("5) Make a torrent                    |                               ")
    print("0) Exit                              |                               ")


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


youtube_config = {
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
    choice_maintainer = True
    while choice_maintainer:
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


def youtube_download(url):
    youtube_dl.YoutubeDL(yt_config).download([url])


if __name__ == "__main__":
    maintainer = True

    while maintainer:
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
            print("Download video/playlist/channel selected... Press enter to return.\n")
            video_url = str(input("Type URL to download.\n>: "))  # wait for user input,

            if video_url == "":  # validate user input,if it's empty, go to the menu
                clear()
                continue

            youtube_download(video_url)
            input("\n\nFinished. Enter to continue.\n\n")

        elif choice == 3:
            print
            "Menu 3 has been selected"
            ## You can add your code or functions here
        elif choice == 4:
            print
            "Menu 4 has been selected"
            ## You can add your code or functions here
        elif choice == 5:
            print
            "Menu 5 has been selected"
            ## You can add your code or functions here
            loop = False  # This will make the while loop to end as not value of loop is set to False
        elif choice == 0:
            exit(clear())
        else:
            clear()
            input("Press any key to go back...\n")  # wait for user input
            clear()
