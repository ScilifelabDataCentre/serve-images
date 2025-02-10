#!/bin/bash

set -o errexit

docker build -t jupyterlab-datascience-dev-img -f ./serve-jupyterlab-datascience/Dockerfile.test ./serve-jupyterlab-datascience
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-jupyterlab-datascience/tests/requirements.txt
export IMAGE_NAME=jupyterlab-datascience-dev-img
python3 -m pytest ./serve-jupyterlab-datascience/