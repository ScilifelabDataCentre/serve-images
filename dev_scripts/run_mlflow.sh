#!/bin/bash

docker build -t mlflow-dev-img -f ./mlflow-image/Dockerfile.test ./mlflow-image
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./mlflow-image/tests/requirements.txt
export IMAGE_NAME=mlflow-dev-img
python3 -m pytest ./mlflow-image
