# dhmz-scrapper
## Create DB
- sudo -u postgres createuser meteouser
- sudo -u postgres createdb meteodb
- psql=# alter user <username> with encrypted password 'meteopwd';

## Create table
- from db/createDB.sql

## Test
- python scrapper.py > logs/$(date +%Y-%m-%dT%H-%M-%S).log

## Setup cronjob
- run_scrapper.sh