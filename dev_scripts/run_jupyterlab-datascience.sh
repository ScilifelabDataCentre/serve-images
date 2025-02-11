#!/bin/bash

set -o errexit
cp ./serve-jupyterlab-tests/basic.ipynb ./serve-jupyterlab-datascience/
docker build -t jupyterlab-datascience-dev-img -f ./serve-jupyterlab-datascience/Dockerfile.test ./serve-jupyterlab-datascience
rm ./serve-jupyterlab-datascience/basic.ipynb
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-jupyterlab-tests/requirements.txt
export IMAGE_NAME=jupyterlab-datascience-dev-img
python3 -m pytest ./serve-jupyterlab-tests/