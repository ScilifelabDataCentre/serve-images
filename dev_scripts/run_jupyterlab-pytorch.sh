#!/bin/bash

set -o errexit

docker build -t jupyterlab-pytorch-dev-img -f ./serve-jupyterlab-pytorch/Dockerfile.test ./serve-jupyterlab-pytorch
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-jupyterlab-pytorch/tests/requirements.txt
export IMAGE_NAME=jupyterlab-pytorch-dev-img
python3 -m pytest ./serve-jupyterlab-pytorch/