#!/bin/bash

set -o errexit

docker build -t jupyterlab-dev-img -f ./serve-jupyterlab/Dockerfile.test ./serve-jupyterlab
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-jupyterlab/tests/requirements.txt
export IMAGE_NAME=jupyterlab-dev-img
python3 -m pytest ./serve-jupyterlab/