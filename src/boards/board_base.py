import random
import time

from PIL import Image

from color import get_matching_color, Color
from target_configuration.target_configuration_base import TargetConfigurationBase

BOARD_SIZE_X = 2000
BOARD_SIZE_Y = 2000


class BoardBase:
    def __init__(self, target_configuration: TargetConfigurationBase):
        self.last_update = 0
        self.colors = []  # 2D array of the entire board (BOARD_SIZE_X x BOARD_SIZE_Y), Color objects
        self.target_configuration: TargetConfigurationBase = target_configuration

        # Fill with white preset
        for x in range(BOARD_SIZE_X):
            column = []
            for y in range(BOARD_SIZE_Y):
                column.append(Color.WHITE)
            self.colors.append(column)

    def update_image(self, raw_image, offset_x, offset_y):
        self.last_update = time.time()

        image = Image.open(raw_image)
        image_data = image.convert("RGB").load()

        # convert to color indices
        for x in range(image.width):
            for y in range(image.height):
                self.colors[x + offset_x][y] = get_matching_color(image_data[x, y])

        print("Board updated.")

    def get_pixel_color(self, x: int, y: int) -> Color:
        return self.colors[x][y]

    def get_mismatched_pixel(self):
        mismatched_pixels = self.get_mismatched_pixels()

        if len(mismatched_pixels) == 0:
            return None

        # return random.choice(mismatched_pixels) # TODO: does this work?
        return mismatched_pixels[min(random.randrange(0, 8), len(mismatched_pixels) - 1)]

    def get_mismatched_pixels(self):
        mismatched_pixels = []
        for target_pixel in self.target_configuration.get_pixels():
            currentColor = self.get_pixel_color(target_pixel["x"], target_pixel["y"])

            if currentColor is None:
                print("Couldn't determine color for pixel at " + str(target_pixel["x"]) + ", " + str(target_pixel["y"]))
                continue

            if currentColor is None or currentColor.value["id"] != target_pixel["color_index"]:
                mismatched_pixels.append(target_pixel)
        return mismatched_pixels
