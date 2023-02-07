#!/bin/bash

docker build -t torchserve-dev-img -f ./serve-torchserve/Dockerfile.test ./serve-torchserve
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-torchserve/tests/requirements.txt
export IMAGE_NAME=torchserve-dev-img
python3 -m pytest ./serve-torchserve/
