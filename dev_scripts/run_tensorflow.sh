#!/bin/bash

docker build -t serve-tensorflow-dev-img -f ./serve-tensorflow/Dockerfile.test ./serve-tensorflow
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-tensorflow/tests/requirements.txt
export IMAGE_NAME=serve-tensorflow-dev-img
python3 -m pytest ./serve-tensorflow/
