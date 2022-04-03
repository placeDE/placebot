import random
import time

from PIL import UnidentifiedImageError

from boards.board_de import BoardDE
from color import get_color_from_index
from local_configuration import local_configuration
from placer import Placer
from target_configuration.target_configuration_de import TargetConfigurationDE
from target_configuration import target_configuration
from color import get_color_from_index, Color


PLACE_INTERVAL = 5 * 60  #  The interval that pixels can be placed at
SLEEP_MISMATCH_THRESHOLD = 0.02  # The percentage of pixels mismatching that cause the bot to slow down (not stop) its refresh rate

target_config = TargetConfigurationDE()
board = BoardDE(target_config)

PLACE_INTERVAL = 5 * 60  #  The interval that pixels can be placed at
SLEEP_MISMATCH_THRESHOLD = 0.02  # The percentage of pixels mismatching that cause the bot to slow down (not stop) its refresh rate

"""
Logs into all accounts in the local configuration file
"""
def login_all():
    placers = []
    for account in local_configuration["accounts"]:
        placer = Placer(board)
        placer.login(account["username"], account["password"])

        if not placer.logged_in:
            print("Failed to login to account: " + account["username"])
            continue

        placers.append(placer)

    print("\n" + str(len(placers)) + " accounts logged in\n")
    return placers

"""
Periodically pulls the board and places a tile when required
"""
def run_board_watcher_placer(placers):
    # Tracks if the template was completed and how many mismatches there were, if yes and below threshold, goes to sleep
    total_pixel_count = 1000 * 1000
    last_mismatch_count = 1000 * 1000
    was_completed = False

    while True:
        for placer in placers:
            if placer.last_placed + PLACE_INTERVAL + random.randrange(5, 25) > time.time():  # Triggered every PLACE_INTERVAL seconds, + random offset (5-25 seconds)
                continue

            print("Attempting to place for: " + placer.username)

            # Fetch the required canvases
            try:
                placer.update_board()
            except UnidentifiedImageError:
                print("Unidentified image for: " + placer.username) # Download error
                print("ABORTING!!!!!!!!!!!!")
                continue

            target_pixel, count = placer.board.get_mismatched_pixel()

            # Get random mismatched target pixel
            target_pixel = placer.board.get_mismatched_pixel(target_configuration.get_config()["pixels"])

            if target_pixel is None:
                print("No mismatched pixels found")
                was_completed = True
                was_completed = True
                was_completed = True
                continue

                print(f"Mismatched pixel found ({count}/{(str(len(placer.board.target_configuration.get_pixels())))}): {str(target_pixel)}")
            placer.place_tile(target_pixel["x"], target_pixel["y"], get_color_from_index(target_pixel["color_index"]))
            print("Mismatched pixel found (" + (str(last_mismatch_count)) + "/" + (str(len(target_configuration.get_config()["pixels"]))) + "): " + str(target_pixel))

            # Place mismatched target pixel with correct color
            placer.place_tile(target_pixel["x"], target_pixel["y"], get_color_from_index(target_pixel["color_index"]))
            print()

            time.sleep(5)

        # Be nice and verbose so users don't look at nothing for 5 minutes
        print("ETA:   ", ",  ".join(
            [p.username + " - " + str(round(p.last_placed + PLACE_INTERVAL + 15 - time.time())) + " s" for p in
             placers]))

        # If we already completed the template and the mismatch is below threshold, it's time to go to sleep
        if was_completed and last_mismatch_count < (SLEEP_MISMATCH_THRESHOLD * total_pixel_count):
            print("\nLess than " + str(SLEEP_MISMATCH_THRESHOLD * total_pixel_count) + " mismatched pixels found, going to sleep, good night")
            time.sleep(90)

        time.sleep(30)

        # If we already completed the template and the mismatch is below threshold, it's time to go to sleep
        if was_completed and last_mismatch_count < (SLEEP_MISMATCH_THRESHOLD * total_pixel_count):
            print("\nLess than " + str(SLEEP_MISMATCH_THRESHOLD * total_pixel_count) + " mismatched pixels found, going to sleep, good night")
            time.sleep(90)

        time.sleep(30)

# Run the entire thing
def run_bot():
    placers = login_all()
    run_board_watcher_placer(placers)

# run the bot in a loop in case it crashes due to any unforeseen reason, e.g. a websocket being closed by the server
# (which happens exactly 1h after login probably due to some token being invalid)
# I could just refresh that token, but I have a life, feel free to create a PR
while True:
    try:
        run_bot()
    except Exception as e:
        print("\n\nError encountered while running bot: " + str(e))
        print("\nRestarting...\n")
        time.sleep(10)  # wait a bit in case the server lost connection


    time.sleep(5)
# Run the entire thing
def run_bot():
    placers = login_all()
    run_board_watcher_placer(placers)

# run the bot in a loop in case it crashes due to any unforeseen reason, e.g. a websocket being closed by the server
# (which happens exactly 1h after login probably due to some token being invalid)
# I could just refresh that token, but I have a life, feel free to create a PR
while True:
    try:
        run_bot()
    except Exception as e:
        print("\n\nError encountered while running bot: " + str(e))
        print("\nRestarting...\n")
        time.sleep(10)  # wait a bit in case the server lost connection


    if wasCompleted and lastMismatchCount < SLEEP_MISMATCH_THRESHOLD:
        print("\nLess than " + str(SLEEP_MISMATCH_THRESHOLD) + " mismatched pixels found, going to sleep, good night")
        time.sleep(90)

        time.sleep(30)

# Run the entire thing
def run_bot():
    placers = login_all()
    run_board_watcher_placer(placers)

# run the bot in a loop in case it crashes due to any unforeseen reason, e.g. a websocket being closed by the server
# (which happens exactly 1h after login probably due to some token being invalid)
# I could just refresh that token, but I have a life, feel free to create a PR
while True:
    try:
        run_bot()
    except Exception as e:
        print("\n\nError encountered while running bot: " + str(e))
        print("\nRestarting...\n")
        time.sleep(10)  # wait a bit in case the server lost connection

