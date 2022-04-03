from enum import Enum

from PIL import ImageColor


class Color(Enum):
    BURGUNDY = {"id": 1, "hex": "#6d001a"}
    DARK_RED = {"id": 2, "hex": "#be0039"}
    RED = {"id": 3, "hex": "#ff4500"}
    ORANGE = {"id": 4, "hex": "#ffa800"}
    YELLOW = {"id": 5, "hex": "#ffd635"}
    PALE_YELLOW = {"id": 6, "hex": "#fff8b8"}
    DARK_GREEN = {"id": 7, "hex": "#00a368"}
    GREEN = {"id": 8, "hex": "#00cc78"}
    LIGHT_GREEN = {"id": 9, "hex": "#7eed56"}
    DARK_TEAL = {"id": 10, "hex": "#00756f"}
    TEAL = {"id": 11, "hex": "#009eaa"}
    LIGHT_TEAL = {"id": 12, "hex": "#00ccc0"}
    DARK_BLUE = {"id": 13, "hex": "#2450a4"}
    BLUE = {"id": 14, "hex": "#3690ea"}
    LIGHT_BLUE = {"id": 15, "hex": "#51e9f4"}
    INDIGO = {"id": 16, "hex": "#493ac1"}
    PERIWINKLE = {"id": 17, "hex": "#6a5cff"}
    LAVENDER = {"id": 18, "hex": "#94b3ff"}
    DARK_PURPLE = {"id": 19, "hex": "#811e9f"}
    PURPLE = {"id": 20, "hex": "#b44ac0"}
    PALE_PURPLE = {"id": 21, "hex": "#e4abff"}
    MAGENTA = {"id": 22, "hex": "#de107f"}
    PINK = {"id": 23, "hex": "#ff3881"}
    LIGHT_PINK = {"id": 24, "hex": "#ff99aa"}
    DARK_BROWN = {"id": 25, "hex": "#6D482F"}
    BROWN = {"id": 26, "hex": "#9C6926"}
    BEIGE = {"id": 27, "hex": "#FFB470"}
    BLACK = {"id": 28, "hex": "#000000"}
    DARK_GRAY = {"id": 29, "hex": "#515252"}
    GRAY = {"id": 30, "hex": "#898D90"}
    LIGHT_GRAY = {"id": 31, "hex": "#D4D7D9"}
    WHITE = {"id": 32, "hex": "#ffffff"}


# generate rgb values for all colors
for color in Color:
    color.value["rgb"] = ImageColor.getcolor(color.value["hex"], "RGB")


def get_matching_color(rgb) -> Color:
    """
    Returns the color object based on the given rgb tuple
    """
    for color in Color:
        if color.value["rgb"] == rgb:
            return color

    print("Color not found:", rgb)
    return None


def get_color_from_index(index) -> Color:
    """
    Returns the color object based on a given place color index
    """
    for color in Color:
        if color.value["id"] == index:
            return color
    return None


# Where has AI gotten us?
# This function was written in its entirety by GPT3, WTF
# def get_closest_color(r, g, b) -> Color:
#     min_distance = None
#     closest_color = None
#     for color in Color:
#         distance = (r - color.value["rgb"][0]) ** 2 + (g - color.value["rgb"][1]) ** 2 + (b - color.value["rgb"][2]) ** 2
#         if min_distance is None or distance < min_distance:
#             min_distance = distance
#             closest_color = color
#     return closest_color


def get_closest_color(r, g, b) -> Color:
    """
    Get the closest color available on place to any color for converting any image to a template
    """
    return min(
        list(Color),
        key=lambda color: (r - color.value["rgb"][0]) ** 2
        + (g - color.value["rgb"][1]) ** 2
        + (b - color.value["rgb"][2]) ** 2,
    )
