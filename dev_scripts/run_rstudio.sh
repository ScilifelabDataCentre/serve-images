#!/bin/bash

docker build -t rstudio-dev-img ./serve-rstudio
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r ./serve-rstudio/tests/requirements.txt
export IMAGE_NAME=rstudio-dev-img
python3 -m pytest ./serve-rstudio/
