import colorama


colorama.init(autoreset=True)


class Color:
    """

    """
    RED = colorama.Fore.RED
    YELLOW = colorama.Fore.YELLOW
    BLUE = colorama.Fore.BLUE
    BOLD = '\033[1m'
    END = '\033[0m'

    def red(self, text):
        return self.RED + text

    def yellow(self, text):
        return self.YELLOW + text

    def blue(self, text):
        return self.BLUE + text

    def bold(self, text):
        return self.BOLD + text + self.END


color = Color()

print(Color().red(Color().bold("red bold")))
print(Color().blue("blue"))
print(Color().yellow(Color().bold("yellow")))
