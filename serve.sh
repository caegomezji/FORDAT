#!/bin/bash

source .env



if [ $APP_ENV == 'PRODUCTION' ]
then

    mkdir log 

    touch log/access-logfile.log
    touch log/error-logfile.log

    gunicorn -c gunicornconfig.py fordat:server
else
    python appProphet.py


fi
