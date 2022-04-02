import random
import time

from PIL import UnidentifiedImageError

from boards.board_de import BoardDE
from color import get_color_from_index
from local_configuration import local_configuration
from placer import Placer
from target_configuration.target_configuration_de import TargetConfigurationDE

PLACE_INTERVAL = 5 * 60  #  The interval that pixels can be placed at
SLEEP_MISMATCH_THRESHOLD = 0.02  # The percentage of pixels mismatching that cause the bot to slow down (not stop) its refresh rate

target_config = TargetConfigurationDE()
board = BoardDE(target_config)

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

            if target_pixel is None:
                print("No mismatched pixels found")
                was_completed = True
                continue

            print(
                f"Mismatched pixel found ({count}/{(str(len(placer.board.target_configuration.get_pixels())))}): {str(target_pixel)}")
            placer.place_tile(target_pixel["x"], target_pixel["y"], get_color_from_index(target_pixel["color_index"]))

            time.sleep(5)

    print("ETA:   ", ",  ".join(
            [p.username + " - " + str(round(p.last_placed + PLACE_INTERVAL + 15 - time.time())) + " s" for p in
             placers]))

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


    time.sleep(30)





# Traceback (most recent call last):
# File "src/placebot.py", line 52, in <module>
# placer.update_board()
# File "/home/place/place/src/placer.py", line 162, in update_board
# self.update_canvas(1)
# File "/home/place/place/src/placer.py", line 223, in update_canvas
# temp = json.loads(ws.recv())
# File "/home/place/place/.venv/lib/python3.8/site-packages/websocket/_core.py", line 357, in recv
# opcode, data = self.recv_data()
# File "/home/place/place/.venv/lib/python3.8/site-packages/websocket/_core.py", line 380, in recv_data
# opcode, frame = self.recv_data_frame(control_frame)
# File "/home/place/place/.venv/lib/python3.8/site-packages/websocket/_core.py", line 401, in recv_data_frame
# frame = self.recv_frame()
# File "/home/place/place/.venv/lib/python3.8/site-packages/websocket/_core.py", line 440, in recv_frame
# return self.frame_buffer.recv_frame()
# File "/home/place/place/.venv/lib/python3.8/site-packages/websocket/_abnf.py", line 338, in recv_frame
# self.recv_header()
# File "/home/place/place/.venv/lib/python3.8/site-packages/websocket/_abnf.py", line 294, in recv_header
# header = self.recv_strict(2)
# File "/home/place/place/.venv/lib/python3.8/site-packages/websocket/_abnf.py", line 373, in recv_strict
# bytes_ = self.recv(min(16384, shortage))
# File "/home/place/place/.venv/lib/python3.8/site-packages/websocket/_core.py", line 524, in _recv
# return recv(self.sock, bufsize)
# File "/home/place/place/.venv/lib/python3.8/site-packages/websocket/_socket.py", line 122, in recv
# raise WebSocketConnectionClosedException(
#     websocket._exceptions.WebSocketConnectionClosedException: Connection to remote host was lost.

