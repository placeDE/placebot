import sys
import time
import traceback
from typing import List

from connection import SocketConnection
from local_configuration import local_configuration
from placer import Placer
from concurrent.futures import ThreadPoolExecutor

PLACE_INTERVAL = 5 * 60  # The interval that pixels can be placed at


def login_all():
    """
    Logs into all accounts in the local configuration file
    """
    placers = []
    def login(username: str, password: str):
        placer = Placer()
        placer.login(username, password)

        if not placer.logged_in:
            print("Failed to login to account: " + account["username"])
            return
        placers.append(placer)

    with ThreadPoolExecutor(max_workers=6) as e:
        for account in local_configuration["accounts"]:
            time.sleep(0.01)
            e.submit(login, account["username"], account["password"])

    print("\n" + str(len(placers)) + " accounts logged in\n")
    return placers


def run_websocket(placers: List[Placer]):
    socket = SocketConnection(local_configuration)
    socket.connect(len(placers))

    try:
        while True:
            request_sent = False
            for placer in placers:
                if placer.should_place():
                    request_sent = True
                    print("Requesting pixel placement for account: " + placer.username)
                    pixel = socket.request_pixel(placer)
                    print(pixel)
                    if pixel:
                        placer.place_tile(pixel["x"], pixel["y"], pixel["color"])
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
            if not request_sent:
                socket.ping()
            time.sleep(10)
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
