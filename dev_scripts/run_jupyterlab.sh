#!/bin/bash

#docker build -t jupyterlab-dev-img -f ./jupyter-lab/Dockerfile.test ./jupyterlab
docker build -t jupyterlab-dev-img ./jupyter-lab
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./jupyter-lab/tests/requirements.txt
export IMAGE_NAME=jupyterlab-dev-img
python3 -m pytest ./jupyter-lab/