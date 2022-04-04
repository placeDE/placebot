import json
import time
import random

import requests
from bs4 import BeautifulSoup

# based on https://github.com/goatgoose/PlaceBot and https://github.com/rdeepak2002/reddit-place-script-2022/blob/073c13f6b303f89b4f961cdbcbd008d0b4437b39/main.py#L316


SET_PIXEL_QUERY = """mutation setPixel($input: ActInput!) {
      act(input: $input) {
        data {
          ... on BasicMessage {
            id
            data {
              ... on GetUserCooldownResponseMessageData {
                nextAvailablePixelTimestamp
                __typename
              }
              ... on SetPixelResponseMessageData {
                timestamp
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
    }
    """
PLACE_INTERVAL = 5*60


class Placer:
    REDDIT_URL = "https://www.reddit.com"
    LOGIN_URL = REDDIT_URL + "/login"
    INITIAL_HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "origin": REDDIT_URL,
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    }

    def __init__(self):
        self.password = None
        self.client = requests.session()
        self.client.headers.update(self.INITIAL_HEADERS)

        self.token = None
        self.logged_in = False
        self.last_placed = 0

        self.username = "Unknown"

    def login(self, username: str, password: str):
        self.username = username

        # get the csrf token
        print("Obtaining CSRF token...")
        r = self.client.get(self.LOGIN_URL)
        time.sleep(1)

        login_get_soup = BeautifulSoup(r.content, "html.parser")
        csrf_token = login_get_soup.find("input", {"name": "csrf_token"})["value"]

        # authenticate
        print("Logging in...")
        r = self.client.post(
            self.LOGIN_URL,
            data={
                "username": username,
                "password": password,
                "dest": self.REDDIT_URL,
                "csrf_token": csrf_token,
            },
        )
        time.sleep(1)

        if r.status_code != 200:
            print("Authorization failed!")  # password is probably invalid
            return
        else:
            print("Authorization successful!")

        # get the new access token
        print("Obtaining access token...")
        r = self.client.get(self.REDDIT_URL)
        data_str = (
            BeautifulSoup(r.content, features="html.parser")
            .find("script", {"id": "data"})
            .contents[0][len("window.__r = ") : -1]
        )
        data = json.loads(data_str)
        self.token = data["user"]["session"]["accessToken"]

        print("Logged in as " + username + "\n")
        self.logged_in = True
        self.username = username
        self.password = password

    def should_place(self) -> bool:
        return self.last_placed == 0 or self.last_placed + PLACE_INTERVAL + random.randrange(2, 15) <= time.time()

    def place_tile(self, x: int, y: int, color: int):
        canvas_id = Placer.get_canvas_id_from_coords(x, y)
        real_x = x
        real_y = y

        x = x % 1000  # we need to send relative to the canvas
        y = y % 1000  # we need to send relative to the canvas

        print("Target canvas: " + str(canvas_id) + " (" + str(x) + ", " + str(y) + ")")

        self.last_placed = time.time()

        headers = self.INITIAL_HEADERS.copy()
        headers.update(
            {
                "apollographql-client-name": "mona-lisa",
                "apollographql-client-version": "0.0.1",
                "content-type": "application/json",
                "origin": "https://hot-potato.reddit.com",
                "referer": "https://hot-potato.reddit.com/",
                "sec-fetch-site": "same-site",
                "authorization": "Bearer " + self.token,
            }
        )

        print(
            "Placing tile at "
            + str(real_x)
            + ", "
            + str(real_y)
            + " with color "
            + str(color)
            + " on canvas "
            + str(canvas_id)
        )
        r = requests.post(
            "https://gql-realtime-2.reddit.com/query",
            json={
                "operationName": "setPixel",
                "query": SET_PIXEL_QUERY,
                "variables": {
                    "input": {
                        "PixelMessageData": {
                            "canvasIndex": canvas_id,
                            "colorIndex": color,
                            "coordinate": {"x": x, "y": y},
                        },
                        "actionName": "r/replace:set_pixel",
                    }
                },
            },
            headers=headers,
        )

        if r.status_code != 200:
            print("Error placing tile")
            if "UNAUTHORIZED" in r.content.decode():
                print("UNAUTHORIZED")
                self.login(self.username, self.password)
            else:
                print(r.content)
            # TODO: handle error
        else:
            print("Placed tile")

    @staticmethod
    def get_canvas_id_from_coords(x: int, y: int):
        return int(x >= 1000) + int(y >= 1000) * 2
