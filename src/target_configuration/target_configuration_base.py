import json
import time

import requests

from local_configuration import local_configuration

UPDATE_INTERVAL = 60

"""
Represents the target configuration containing the template / pixels to be drawn
Is refreshed periodically by pulling it from a server 
"""
class TargetConfigurationBase:
    def __init__(self):
        self.last_update = 0
        self.config = {}
        self.pixels: list[dict] = []

    """
    Get the config and refresh it first if necessary
    """
    def get_config(self):
        if self.last_update + UPDATE_INTERVAL < time.time():
            self.refresh_config()
            self.last_update = time.time()

        self.pixels = self.config["pixels"]

        return self.config

    """
    Pulls the config from the server configured in config.json or falls back to reading a local file if specified as such
    """
    def refresh_config(self):
        print("\nRefreshing target configuration...\n")

        url = local_configuration["target_configuration_url"]

        if url.startswith("http"):
            r = requests.get(url)

            if r.status_code != 200:
                print("Error: Could not get config file from " + local_configuration["target_configuration_url"])
                return

            # parse config file
            self.config = json.loads(r.text)
        else:
            # not a remote url, fallback to local file
            with open(url, "r") as f:
                self.config = json.load(f)

    def get_pixels(self) -> list[dict]:
        self.get_config()
        return self.pixels


target_configuration = TargetConfigurationBase()
