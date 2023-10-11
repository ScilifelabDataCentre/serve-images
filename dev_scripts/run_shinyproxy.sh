#!/bin/bash

set -o errexit

docker build -t shinyproxy-dev-img ../serve-shinyproxy
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ../serve-shinyproxy/tests/requirements.txt
export IMAGE_NAME=shinyproxy-dev-img
python3 -m pytest ../serve-shinyproxy/
