#!/bin/bash
# Git sync will cause the app.py to not exist for a short time.
# Therefore we retry restarting the server a couple of times.
n=0
until [ "$n" -ge 60 ]
do
   cd /app/$DEPLOYMENT_PATH/
   [[ -f requirements.txt ]] && pip3 install -r requirements.txt
   gunicorn app:server --bind :8050
   n=$((n+1)) 
   sleep 1
done