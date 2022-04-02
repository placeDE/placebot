import json
import random
import time

import requests

from local_configuration import local_configuration
from target_configuration.target_configuration_base import TargetConfigurationBase

UPDATE_INTERVAL = 60


class TargetConfigurationDE(TargetConfigurationBase):
    def get_config(self):
        if self.last_update + UPDATE_INTERVAL < time.time():
            self.refresh_config()
            self.last_update = time.time()

        lst = []
        priorities = self.config["priorities"]
        for s in self.config["structures"].values():
            prio = (priorities.get(str(s.get("priority"))) or 0) * random.randint(0, 100) / 100
            for p in s.get("pixels"):
                lst.append({"x": p["x"], "y": p["y"], "color_index": p["color"], "priority": [prio, priorities.get(str(p.get("priority"))) or 0]})
        self.pixels = lst

        return self.config

    def refresh_config(self):
        print("Refreshing target configuration...")
        r = requests.get(local_configuration["target_configuration_url"])

        if r.status_code != 200:
            print("Error: Could not get config file from " + local_configuration["target_configuration_url"])
            return

        # parse config file
        self.config = json.loads(r.text)


target_configuration = TargetConfigurationDE()
