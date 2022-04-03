import random

from boards.board_base import BoardBase
from color import get_color_from_index


class BoardDE(BoardBase):
    def get_mismatched_pixel(self):
        mismatched_pixels = self.get_mismatched_pixels()

        if len(mismatched_pixels) == 0:
            return None, 0

        for p in mismatched_pixels:
            p.update({"priority": [p["priority"][0], p["priority"][1] * random.randint(0, 100) / 100]})

        mismatched_pixels = list(sorted(mismatched_pixels, key=lambda x: x["priority"]))
        return mismatched_pixels[0], len(mismatched_pixels)  # TODO: does this work?

    def get_mismatched_pixels(self):
        mismatched_pixels = []
        for target_pixel in self.target_configuration.get_pixels():
            currentColor = self.get_pixel_color(target_pixel["x"], target_pixel["y"])
            if currentColor is None:
                print("Couldn't determine color for pixel at " + str(target_pixel["x"]) + ", " + str(target_pixel["y"]))
                continue

            if currentColor is None or currentColor.value["id"] != target_pixel["color_index"] and get_color_from_index(target_pixel["color_index"]):
                mismatched_pixels.append(target_pixel)
        return mismatched_pixels
