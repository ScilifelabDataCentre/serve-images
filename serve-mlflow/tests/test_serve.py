#!/usr/bin/env python3
"""Tests of the mlflow image using API calls."""

import os
import time
import random as rnd
import requests
from requests.exceptions import ConnectionError
import docker
import pytest

PORT = 5000  # MLFlow port
HOST = "0.0.0.0"
USER = "jovyan"
MODELPATH = "/home/{}/test_model".format(USER)
TIMEOUT_CALL = 5  # the timeout in seconds of the client request call
EXPERIMENT_NAME = "Exp123"
MODEL_NAME = "test_model"

client = docker.from_env()
container = client.containers.run(
    image=os.environ["IMAGE_NAME"],
    command='/bin/bash -c "python3 mlrun_example.py {} {}  && mlflow models serve -m {} --host {} --port {}"'.format(
        EXPERIMENT_NAME, MODEL_NAME, MODELPATH, HOST, PORT
    ),
    ports={f"{PORT}/tcp": PORT},
    detach=True,
)
time.sleep(10)  # Update this somehow.
container.reload()


def test_container_status():
    """Test that the MLFlow container is running."""
    assert container.status == "running"


def test_container_ports():
    """Test of the expected container port."""
    assert len(container.ports) == 1, "There should be 1 port"
    assert container.ports[f"{PORT}/tcp"][0]["HostPort"] == str(PORT)


def test_mlflow_access():
    """Test of basic communication with the container returns status 200 (OK)."""
    url = _get_url(container) + "/ping"
    # check the API endpoint every 10 seconds
    max_attempts = 50

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, timeout=TIMEOUT_CALL)
            if response.status_code == 200:
                print("mlflow server is up and running!")
                assert True
                break
        except:
            pass

        if attempt == max_attempts:
            RuntimeError(
                f"mlflow server did not become ready after {max_attempts} attempts"
            )
            assert False

        print(
            f"Attempt {attempt} failed, waiting for 10 seconds before trying again..."
        )
        time.sleep(10)


def test_prediction():
    """Test of a basic prediction using the LogisticRegression model created in 'mlrun_example.py"""
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = '{"dataframe_split": {"columns": ["X"],"data": [-2, -1, 0, 1, 2, 1]}}'
    response = requests.post(
        "http://{}:{}/invocations".format(HOST, PORT), data=data, headers=headers
    ).json()
    assert all([x == y for x, y in zip(response["predictions"], [0, 0, 0, 1, 1, 1])])


def test_shutdown():
    container.stop()
    container.reload()
    assert container.status == "removing" or container.status == "exited"
    container.remove()
    client.close()


# Private methods


def _get_ip(container):
    """Gets the IP of the container."""
    return container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]


def _get_url(container):
    """Gets the correct adress for inference."""
    url = "http://{}:{}".format(_get_ip(container), PORT)
    return url
