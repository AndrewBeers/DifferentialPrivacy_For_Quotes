from colour import Color
from pprint import pprint


def test_function():

    red = Color("red")
    green = Color("green")
    colors = list(red.range_to(green, 20))
    # pprint(colors)

    # pprint(dir(colors[0]))
    for color in colors:
        print(color.get_hex())

    return


if __name__ == '__main__':

    test_function()