import json
from os import environ
from sys import argv

local_configuration = {}

if (path := environ.get("CONFIGURATION_FILE")) is None:
    if len(argv) >= 2:
        path = argv[1]
    else:
        path = 'config.json'

print(f"using {path} as config")
with open(path, 'r') as f:
    local_configuration = json.load(f)
