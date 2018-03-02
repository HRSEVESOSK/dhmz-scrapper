# dhmz-scrapper
## Create DB
- sudo -u postgres createuser meteouser
- sudo -u postgres createdb meteodb
- psql=# alter user meteouser with encrypted password 'meteopwd';

## Add postgis extension
-  sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" meteodb

## Create table
- from db/createDB.sql

## Test
- python scrapper.py > logs/$(date +%Y-%m-%dT%H-%M-%S).log

## Setup cronjob
- run_scrapper.sh
