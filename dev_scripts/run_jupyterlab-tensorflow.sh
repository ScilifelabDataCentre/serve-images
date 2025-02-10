#!/bin/bash

set -o errexit

docker build -t jupyterlab-tensorflow-dev-img -f ./serve-jupyterlab-tensorflow/Dockerfile.test ./serve-jupyterlab-tensorflow
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-jupyterlab-tensorflow/tests/requirements.txt
export IMAGE_NAME=jupyterlab-tensorflow-dev-img
python3 -m pytest ./serve-jupyterlab-tensorflow/