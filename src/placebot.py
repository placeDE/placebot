import datetime
import random
import sys
import time
import traceback
from typing import List

from PIL import UnidentifiedImageError

from color import get_color_from_index
from local_configuration import local_configuration
from placer import Placer
from connection import SocketConnection

PLACE_INTERVAL = 5 * 60  # The interval that pixels can be placed at


def login_all():
    """
    Logs into all accounts in the local configuration file
    """
    placers = []
    for account in local_configuration["accounts"]:
        placer = Placer()
        placer.login(account["username"], account["password"])

        if not placer.logged_in:
            print("Failed to login to account: " + account["username"])
            continue

        placers.append(placer)

    print("\n" + str(len(placers)) + " accounts logged in\n")
    return placers


def run_websocket(placers: List[Placer]):

    socket = SocketConnection(local_configuration)
    socket.connect()

    try:
        while True:
            for placer in placers:
                if placer.should_place():
                    print("Requesting pixel placement for account: " + placer.username)
                    pixel = socket.request_pixel(placer)
                    print(pixel)
                    if pixel:
                        placer.place_tile(pixel["x"], pixel["y"], get_color_from_index(pixel["color"]))

                    else:
                        print("No pixel available!")
                        continue

                # Be nice and verbose so users don't look at nothing for 5 minutes
                print(
                    "ETA:   ",
                    ",  ".join(
                        [
                            p.username
                            + " - "
                            + str(round(p.last_placed + PLACE_INTERVAL + 15 - time.time()))
                            + " s"
                            for p in placers
                        ]
                    ),
                )
            time.sleep(30)
    finally:
        socket.close()


# run the bot in a loop in case it crashes due to any unforeseen reason, e.g. a websocket being closed by the server
# (which happens exactly 1h after login probably due to some token being invalid)
# I could just refresh that token, but I have a life, feel free to create a PR
while True:
    try:
        run_websocket(login_all())
    except Exception as e:
        print("\n\nError encountered while running bot: ")
        traceback.print_exception(*sys.exc_info())
        print("\nRestarting...\n")
        time.sleep(10)  # wait a bit in case the server lost connection

    time.sleep(5)
