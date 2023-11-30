#!/bin/bash

set -o errexit

docker build -t python-dev-img -f ./serve-python/Dockerfile.test ./serve-python
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-python/tests/requirements.txt
export IMAGE_NAME=python-dev-img
python3 -m pytest ./serve-python/
