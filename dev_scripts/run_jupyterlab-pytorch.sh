#!/bin/bash

set -o errexit
cp ./serve-jupyterlab-tests/basic.ipynb ./serve-jupyterlab-pytorch/
docker build -t jupyterlab-pytorch-dev-img -f ./serve-jupyterlab-pytorch/Dockerfile.test ./serve-jupyterlab-pytorch
rm ./serve-jupyterlab-pytorch/basic.ipynb
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-jupyterlab-tests/requirements.txt
export IMAGE_NAME=jupyterlab-pytorch-dev-img
python3 -m pytest ./serve-jupyterlab-tests/