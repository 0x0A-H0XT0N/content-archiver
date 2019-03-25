from time import sleep
from progress.bar import IncrementalBar
from pytube import YouTube, Playlist
import os


affirmative_choice = ["y", "yes", "s", "sim", "yeah" "yah", "ya"]
negative_choice = ["n", "no", "nao", "na", "nop", "nah"]

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
    print("   █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗")
    print("   ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝")
    print("   ███████║██████╔╝██║     ███████║██║██║   ██║█████╗")
    print("   ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝██╔══╝")
    print("   ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████╗")
    print("   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝")
    print("")
    print("1) Download a Channel/playlist")
    print("2) Download a Single video")
    print("3) Check for new videos")
    print("4) Set download path")
    print("5) See downloaded channels")
    print("6) Make a torrent")
    print("Press ENTER to exit")


maintainer = True


while maintainer:
    show_menu()     # show menu
    choice = input("\n>: ")     # wait for user input

    if choice == "":
        clear()
        exit()

    try:
        choice = int(choice)    # try to convert choice(str) to choice(int),
        # this is needed because the normal input is a str

    except ValueError:      # if the int() parser cant convert, raises a ValueError, this take care if it
        clear()     # clear the screen
        print("Numbers only.")
        input("Press any key to go back...\n")    # wait for user input
        clear()
        continue    # goes right back in the loop, skip the "else:" later on, save time

    if choice == 1:
        clear()
        print("Download channel/playlist selected... Press enter to return.\n")
        video_url = str(input("Video url to download: "))    # wait for user input,

        if video_url == "":    # validate user input,if it's empty, go to the menu
            clear()
            print("Going back...")
            sleep(1)
            clear()
            continue

        pl = Playlist(video_url)     # after validation make a Playlist() obj
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
        if choice in negative_choice:
            clear()
            print("Going back...")
            sleep(1)
            clear()
            continue
        else:
            clear()
            print("Downloading starting...")


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
    else:
        clear()
        input("No option located. Press any key to go back...")
        clear()
