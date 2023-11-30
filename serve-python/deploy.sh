#!/bin/bash
# STACKN_MODEL_PATH is passed as an env variable to the serve app deployment.yaml
# It should contain the folder with models and code
cd $STACKN_MODEL_PATH
[[ -f requirements.txt ]] && pip3 install -r requirements.txt

# Go back to the home directory and start sever app
cd ..
uvicorn serve:app --host 0.0.0.0 --port 8501