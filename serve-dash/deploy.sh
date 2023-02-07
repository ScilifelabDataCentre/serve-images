#!/bin/bash
cd /app/$DEPLOYMENT_PATH
# [[ -f requirements.txt ]] && pip3 install -r requirements.txt
echo $DEBUG
echo "hello"
if [[ "$DEBUG" = "false" ]]
then
[[ -f requirements.txt ]] && pip3 install -r requirements.txt
# watchmedo auto-restart --recursive --directory=/app/$DEPLOYMENT_PATH/ --patterns="*.py;*.txt" -- /run_server.sh
# watchmedo auto-restart --directory=. --patterns="*.py;*.txt" -- sleep 2s && gunicorn app:server --bind :8050
gunicorn --reload app:server --bind :8050
else
python3 app.py
# watchmedo auto-restart --directory=. -- gunicorn app:server --bind :8050
fi