#  ███╗   ███╗ ██████╗████████╗ ██████╗ ██╗    ██╗     █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗
#  ████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗██║    ██║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝
#  ██╔████╔██║██║  ███╗  ██║   ██║   ██║██║ █╗ ██║    ███████║██████╔╝██║     ███████║██║██║   ██║█████╗
#  ██║╚██╔╝██║██║   ██║  ██║   ██║   ██║██║███╗██║    ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝
#  ██║ ╚═╝ ██║╚██████╔╝  ██║   ╚██████╔╝╚███╔███╔╝    ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗
#  ╚═╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝
# https://github.com/PhoenixK7PB/mgtow-archive
#
# TODO: handling path for windows machines (home path)
# TODO: add choose option for format when downloading
# TODO: make a "Config" file for storing path and downloaded channels
#  (last update, total videos, etc)
# TODO: use colorama for font color
# TODO: Make a title for every "section" of the program (like lazy script) using 60 chars
#  like ------------------------------------------------------------
# TODO: add a logger that saves every error and prints it at the end of the download
# TODO: add torrent options
# TODO: comment every function
# TODO add options to edit, remove and download specific channels


import youtube_dl
from pathlib import Path
import signal
import sys
import os
import json
import threading
import time

affirmative_choice = ["y", "yes", "s", "sim", "yeah", "yah", "ya"]  # affirmative choices, used on user interaction
negative_choice = ["n", "no", "nao", "na", "nop", "nah"]    # negative choices, used on user interaction

founded_videos_dict = {}    # leave empty, used on youtube_hooker
founded_videos_limit = 3    # limit of videos that can be founded before exiting, default is 3, SHOULD BE INT


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
    """
    handler of CTRL + C, prints a blank line, then exit
    :param signal:
    :param frame:
    :return: prints a blank line and exit
    """

    print("\n")
    sys.exit(0)


def wait_input():
    """
    this function should be called when the program doesnt recognize user input,
    first clear the screen, then the user should press any key, then clear screen again,
    then user should have the option to choose again if possible
    :return: nothing, just clears the screen
    """

    clear()
    input("Press any key to continue...")
    clear()


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
    """
    log and check how much videos have been founded on the machine, this is used by every thread/daemon
    :param video: video being downloaded
    :return: if more than "X" videos have been founded on the machine, exit the current thread/download
    """

    if threading.currentThread() not in founded_videos_dict:
        # check if the current thread have already been logged on the dict,
        # if not, create a key using the current thread name and gives to it a value 0
        founded_videos_dict[threading.currentThread()] = 0

    if len(video) <= 4:
        # check if the video dict properties has more than 4 keys, this happens because when a video is founded, yt-dl
        # creates only 4 keys to it on the hooker dict
        founded_videos_dict[threading.currentThread()] += 1

    if founded_videos_dict[threading.currentThread()] >= founded_videos_limit:
        # if more than or equal than founded_videos_limit, exit the thread
        # this happens because threads/daemons consumes machine resources and time
        # if you want to download a full channel but you already have some videos, dont use the channels tab
        print("\n     LIMIT OF VIDEOS FOUNDED FOR CURRENT CHANNEL,"
              "\n     EXITING DAEMON: %s \n" % threading.currentThread())
        sys.exit(0)


def make_path():
    """
    create a JSON file on the program directory containing the path for downloaded videos,
    user can use home path
    :return: create a global variable called "path" containing the path, returns nothing
    """

    clear()
    print("Creating a JSON file containing the path...\n")
    path_name = str(input("Type the full path for storing the videos... Enter to use your home path.\n>:"))

    if path_name == "":     # if user input is blank,
        clear()
        if not os.path.exists(str(Path.home())):    # check if user home exists,
            os.makedirs(str(Path.home()))   # if not, create it
        Json.encode(str(Path.home()), "path.json")  # encode JSON file containing the path (home path in this case)

    else:   # if user input is not blank,
        clear()
        if not os.path.exists(path_name):   # check if user input path exists
            os.makedirs(path_name)  # if not, create it
        Json.encode(path_name, "path.json")     # encode JSON file containing the user path

    global path
    path = Json.decode("path.json", return_content=0)   # make a global variable containing the new path

    print("New path is:", path)     # print new path,
    input("\nEnter to continue.\n")     # wait input, and then exit
    clear()


def get_path():
    """
    Should get a "path" for storing the downloaded content
    Uses json_handler,
    If not data could be found, calls make_path()
    :return: Make a global variable called "path",
    """

    try:    # tries to decode path
        global path
        path = Json.decode("path.json", return_content=0)
        return path

    except FileNotFoundError:   # if the file is not founded, calls make_path() and makes it
        make_path()
        return path


def change_path():
    """
    option for changing/making new path
    :return: nothing, just changes path global variable
    """

    clear()
    print("Change path selected...\n")
    get_path()
    print("Your current path is: ", path)
    new_path = str(input("\nType your new path... Enter to return.\n>:"))
    if new_path == "":  # check user input, if blank, return
        clear()
        return
    else:   # else: check, encode, change global variable path and returns
        if not os.path.exists(new_path):    # checks if new path exists,
            os.makedirs(new_path)   # if not, create it,
        Json.encode(new_path, "path.json")  # then encode it
        get_path()  # change global variable path
        clear()
        print("New path is:", path)
        input("\nEnter to continue.\n")
        clear()
        return


youtube_config = {      # --------------------CHANGE-THIS!!!--------------------- #

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

yt_list_of_channels_config = {      # --------------------CHANGE-THIS!!!--------------------- #

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

youtube_default_config = {      # -----------------DO-NOT-CHANGE-THIS!!!----------------- #

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
    """
    function to reset the yt-dl config JSON
    changes yt_config variable, makes a new yt_config.json file
    :return: nothing
    """
    Json.encode(youtube_default_config, "yt_config.json")
    global yt_config
    yt_config = Json.decode("yt_config.json", return_content=0)


def apply_config():
    """
    used to write-down new changes to the yt config
    :return: nothing
    """
    Json.encode(youtube_config, "yt_config.json")
    global yt_config
    yt_config = Json.decode("yt_config.json", return_content=0)


def get_config():
    """
    access the json configuration file and make a global variable called yt_config
    :return: nothing
    """
    try:    # tries to decode the yt_config.json file
        global yt_config
        yt_config = Json.decode("yt_config.json", return_content=0)
    except FileNotFoundError:   # if the file doesnt exists, make a default one
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
                    print("CTRL + C to cancel download."
                          "\n"
                          "ENTER to resume program after the download is finished.")
                    time.sleep(2)
                    channel_count = 0
                    videos_threads = []
                    for channel in channels:
                        channel_count += 1
                        print()
                        print("     Channel %d of %d" % (channel_count, len(channels)))
                        print("     Channel: %s" % channel)
                        print("     URL: %s" % channels[channel])
                        print()
                        video_thread = threading.Thread(target=youtube_channel_download, args=(channels[channel],),
                                                        daemon=True)
                        videos_threads.append(video_thread)

                    print("\nStarting threads\n")
                    time.sleep(1)
                    for video_thread in videos_threads:
                        video_thread.start()
                    input()

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
