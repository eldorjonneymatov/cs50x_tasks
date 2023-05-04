from sys import argv, exit
from random import choice
from pyfiglet import Figlet

figlet = Figlet()
fonts = figlet.getFonts()

def get_font():
    if len(argv) == 1:
        return choice(fonts)
    elif len(argv) == 3 and (argv[1] in ['-f', '-font']) and (argv[2] in fonts):
        return argv[2]
    return None


def main():
    ft = get_font()
    if not ft:
        exit('Invalid usage')
    f = Figlet(font = ft)
    text = input("Input: ")
    print('Output: ')
    print(f.renderText(text))


if __name__ == "__main__":
    main()