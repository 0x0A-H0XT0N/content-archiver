

def show_menu():
    # menu design
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
    # TODO show options

while True:
    show_menu()  # show menu
    choice = input("Enter your choice [1-5]: ")

    if choice == 1:
        print
        "Menu 1 has been selected"
        ## You can add your code or functions here
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
        # any wrong value goes here
        input("No option located. Press any key to go back...")
