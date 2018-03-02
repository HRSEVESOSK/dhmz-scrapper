#!/bin/sh
APPLICATION_PATH=/usr/local/src/dhmz-scrapper/
cd "${APPLICATION_PATH}"
python scrapper.py > /usr/local/src/dhmz-scrapper/logs/$(date +%Y-%m-%dT%H-%M-%S).log 2>&1