#!/bin/bash

set -o errexit
cp ./serve-jupyterlab-tests/basic.ipynb ./serve-jupyterlab-minimal/
docker build -t jupyterlab-minimal-dev-img -f ./serve-jupyterlab-minimal/Dockerfile.test ./serve-jupyterlab-minimal
rm ./serve-jupyterlab-minimal/basic.ipynb
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-jupyterlab-tests/requirements.txt
export IMAGE_NAME=jupyterlab-minimal-dev-img
python3 -m pytest ./serve-jupyterlab-tests/
