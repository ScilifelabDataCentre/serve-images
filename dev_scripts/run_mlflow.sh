#!/bin/bash

set -o errexit

docker build -t mlflow-dev-img -f ./serve-mlflow/Dockerfile.test ./serve-mlflow
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-mlflow/tests/requirements.txt
export IMAGE_NAME=mlflow-dev-img
python3 -m pytest ./serve-mlflow
