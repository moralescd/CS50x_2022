# TODO
from cs50 import get_int


def main():
    height = get_height()
    # number of spaces needed at start to align properly, decrease with each i
    spaces = height - 1
    # first row of blocks will only need one, increase with each i
    blocks = 1
    for i in range(height):
        print(" " * spaces, "#" * blocks, "  ", "#" * blocks, sep='')
        spaces -= 1
        blocks += 1


def get_height():
    while True:
        height = get_int("Height: ")
        if height >= 1 and height <= 8:
            break
    return height


main()