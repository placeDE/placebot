import random
import time

from PIL import UnidentifiedImageError

from boards.board_de import BoardDE
from color import get_color_from_index
from local_configuration import local_configuration
from placer import Placer
from target_configuration.target_configuration_de import TargetConfigurationDE

PLACE_INTERVAL = 5 * 60

target_config = TargetConfigurationDE()
board = BoardDE(target_config)

placers = []
for account in local_configuration["accounts"]:
    placer = Placer(board)
    placer.login(account["username"], account["password"])

    if not placer.logged_in:
        print("Failed to login to account: " + account["username"])
        continue

    placers.append(placer)

print("\n", len(placers), " accounts logged in\n")

counter = 0

while True:
    for placer in placers:
        if placer.last_placed + PLACE_INTERVAL + random.randrange(5, 25) > time.time():
            continue

        print("Attempting to place for: " + placer.username)

        try:
            placer.update_board()
        except UnidentifiedImageError:
            print("Unidentified image for: " + placer.username)
            print("ABORTING!!!!!!!!!!!!")
            print("ABORTING!!!!!!!!!!!!")
            print("ABORTING!!!!!!!!!!!!")
            continue

        targetPixel, count = placer.board.get_mismatched_pixel()

        if targetPixel is None:
            print("No mismatched pixels found")
            continue

        print(
            f"Mismatched pixel found ({count}/{(str(len(placer.board.target_configuration.get_pixels())))}): {str(targetPixel)}")
        placer.place_tile(targetPixel["x"], targetPixel["y"], get_color_from_index(targetPixel["color_index"]))

        time.sleep(5)

    print("ETA:   ", ",  ".join(
            [p.username + " - " + str(round(p.last_placed + PLACE_INTERVAL + 15 - time.time())) + " s" for p in
             placers]))

    time.sleep(30)
