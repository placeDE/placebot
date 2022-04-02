This is a fork for /r/placeDE of the oroginal bot located here: https://github.com/Geosearchef/placebot

to set the config file, you can either set the

`CONFIGURATION_FILE`  environment variable to the path to the config file  
append the path to the programm call as parameter  
or provide a file called `config.json`.

To run the programm you have to run `python src/placebot.py`  
Make sure, you have the dependencies installed.  

Pipenv and docker are not yet tested, so might not work!
  
Bot for the r/place event.

Based on code from https://github.com/goatgoose/PlaceBot and https://github.com/rdeepak2002/reddit-place-script-2022.

The script in converter can be used to convert an image to a target configuration. Alpha=255 pixels are ignored.

The bot (run via placebot.py) can be configured using config.json. It logs into multiple accounts and pulls the target config from a server via http every 60 seconds.
Every 5 minutes (+5-25 secs), each account pulls the board and attempts to place a misplaced pixel.


## Docker-Compose

```yml
version: '2'
services:
  placebot:
    build: https://github.com/TheCataliasTNT2k/placebot.git#main
    restart: unless-stopped
    volumes:
     - ./config.json:/app/config.json
```
1. Add above as docker-compose.yml
2. Add `config.json` to the same folder
3. Run `docker-compose up -d
4. Profit.
