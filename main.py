#  ███╗   ███╗ ██████╗████████╗ ██████╗ ██╗    ██╗     █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗
#  ████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗██║    ██║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝
#  ██╔████╔██║██║  ███╗  ██║   ██║   ██║██║ █╗ ██║    ███████║██████╔╝██║     ███████║██║██║   ██║█████╗
#  ██║╚██╔╝██║██║   ██║  ██║   ██║   ██║██║███╗██║    ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝
#  ██║ ╚═╝ ██║╚██████╔╝  ██║   ╚██████╔╝╚███╔███╔╝    ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗
#  ╚═╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝
# https://github.com/PhoenixK7PB/mgtow-archive
#
# TODO: handling path for windows machines (home path)
# TODO: make a dominant "path" option using JSON
# TODO: printing filesize (MB) of video before downloading
# TODO: make callback functions for completed downloads,
#  displaying remaining videos (if channel or playlist), time elapsed
# TODO: make one more advanced progress bar
# TODO: add choose option for format when downloading
# TODO: add menu and options
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

from pytube import YouTube, Playlist
from progress.bar import IncrementalBar
from pathlib import Path
from time import sleep
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
    print("1) Download a Channel/playlist       |")
    print("2) Download a Single video           |")
    print("3) Check for new videos              |  path) Set download path")
    print("4) See downloaded channels           |")
    print("5) Make a torrent                    |")
    print("0) Exit                              |")


def get_path():
    """
    Should get a "path" for storing the downloaded content
    Uses json_handler ,
    If not data could be found, try to create a JSON file with it,
    Default path (if no input) the user home,
    The user can change it before creation and on the main menu
    :return: Make a global variable called "path",
    """
    try:
        global path
        path = Json.decode("path.json", return_content=0)

    except FileNotFoundError:
        clear()
        print("No path detected... Making one for you.")
        path_name = str(input("Type the (full) path.... Press enter to use your home path.\n>:"))

        if path_name == "":
            clear()
            Json.encode(str(Path.home()), "path.json")

        else:
            clear()
            Json.encode(path_name,"path.json")

        path = Json.decode("path.json", return_content=0)

        print("Path is:", path)
        input("Type something to continue...")
        clear()


def make_bar(youtube_obj, filesize, title):
    """
    make a bar object, need filesize for bar progress,
    :param filesize: filesize of video
    :return: nothing.
    """
    global bar
    global yt
    yt = youtube_obj
    bar = IncrementalBar("[download] " + title, max=filesize, suffix='%(percent).2f%%')


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

    if bytes_remaining == 0:
        del last_bytes, bytes_remaining, bytes_finished
        bar.finish()
        print()


def download_video(youtube_obj):
    """

    :param youtube_obj: YouTube(url) correspondent
    :param path: (optional) download location for saving the file,
    default one is current user home directory.
    if path does not exist, it's created.
    :return: Nothing # TODO change to call on end (register_on_complete_callback) and print stats
    """
    get_path()
    if not os.path.exists(path):
        os.makedirs(path)
    make_bar(youtube_obj, youtube_obj.streams.first().filesize, youtube_obj.title)
    youtube_obj.register_on_progress_callback(show_progress_bar)
    youtube_obj.streams.first().download(path)


def playlist_download(url_list):
    for url_pl in url_list:
        yt_pl = YouTube(url_pl)
        download_video(yt_pl)
    input("Finished... Press any key to go back.")
    clear()

# yt = YouTube(str(input("Video url to download: ")))
# path_location = str(input("Full path to save file (blank is home directory): "))
#
# if path_location != "":
#     download_video(yt, path_location)
# else:
#     download_video(yt)
# print()


if __name__ == "__main__":
    maintainer = True

    while maintainer:
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
                clear()
                print("Change path selected... Press enter to return.\n")
                get_path()
                print("Your current path is: ", path)
                new_path = str(input("\nType your new path.\n>:"))
                if new_path == "":
                    clear()
                    continue
                else:
                    if not os.path.exists(new_path):
                        os.makedirs(new_path)
                    Json.encode(new_path, "path.json")
                    clear()
                    continue
            else:
                clear()  # clear the screen
                input("Press any key to go back...\n")  # wait for user input
                clear()
                continue  # goes right back in the loop, skip the "else:" later on, save time

        if choice == 1:
            clear()
            print("Download channel/playlist selected... Press enter to return.\n")
            video_url = str(input("Video url to download: "))  # wait for user input,

            if video_url == "":  # validate user input,if it's empty, go to the menu
                clear()
                print("Going back...")
                sleep(1)
                clear()
                continue

            pl = Playlist(video_url)  # after validation make a Playlist() obj
            sleep(0.5)
            clear()
            print("Searching for videos...")
            try:
                parsed_links = pl.parse_links()
            except ValueError:
                clear()
                print("Unknown URL type... Going back.")
                sleep(2)
                clear()
                continue
            clear()
            choice = input("Founded %d videos... Continue? [Y/n]\n>:" % (len(parsed_links)))
            if choice.lower() in negative_choice:
                clear()
                print("Going back...")
                sleep(1)
                clear()
                continue
            else:
                clear()
                playlist_download(parsed_links)


        elif choice == 2:
            print
            "Menu 2 has been selected"
            ## You can add your code or functions here
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
