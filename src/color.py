from enum import Enum

from PIL import ImageColor


class Color(Enum):
    RED = {"id": 2, "hex": "#FF4500"}
    ORANGE = {"id": 3, "hex": "#FFA800"}
    YELLOW = {"id": 4, "hex": "#FFD635"}
    DARK_GREEN = {"id": 6, "hex": "#00A368"}
    LIGHT_GREEN = {"id": 8, "hex": "#7EED56"}
    DARK_BLUE = {"id": 12, "hex": "#2450A4"}
    BLUE = {"id": 13, "hex": "#3690EA"}
    CYAN = {"id": 14, "hex": "#51E9F4"}
    DARK_PURPLE = {"id": 18, "hex": "#811E9F"}
    PURPLE = {"id": 19, "hex": "#B44AC0"}
    PINK = {"id": 23, "hex": "#FF99AA"}
    BROWN = {"id": 25, "hex": "#9C6926"}
    BLACK = {"id": 27, "hex": "#000000"}
    GREY = {"id": 29, "hex": "#898D90"}
    LIGHT_GREY = {"id": 30, "hex": "#D4D7D9"}
    WHITE = {"id": 31, "hex": "#FFFFFF"}


# generate rgb values for all colors
for color in Color:
    color.value["rgb"] = ImageColor.getcolor(color.value["hex"], "RGB")


def get_matching_color(rgb) -> Color:
    for color in Color:
        if color.value["rgb"] == rgb:
            return color
    return None


def get_color_from_index(index) -> Color:
    for color in Color:
        if color.value["id"] == index:
            return color
    return None


# def get_closest_color(r, g, b) -> Color: # This function was written in its entirety by GPT3, WTF
#     min_distance = None
#     closest_color = None
#     for color in Color:
#         distance = (r - color.value["rgb"][0]) ** 2 + (g - color.value["rgb"][1]) ** 2 + (b - color.value["rgb"][2]) ** 2
#         if min_distance is None or distance < min_distance:
#             min_distance = distance
#             closest_color = color
#     return closest_color

def get_closest_color(r, g, b) -> Color:
    return min(list(Color), key=lambda color: (r - color.value["rgb"][0]) ** 2 + (g - color.value["rgb"][1]) ** 2 + (
                b - color.value["rgb"][2]) ** 2)
