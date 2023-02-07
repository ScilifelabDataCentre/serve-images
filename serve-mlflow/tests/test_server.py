#!/usr/bin/env python3
"""Tests of the mlflow image using API calls."""

import os
import time
import random as rnd
import importlib
import requests
from requests.exceptions import ConnectionError
import docker
import pytest

PORT = 5001  # MLFlow port
HOST = "0.0.0.0"
TIMEOUT_CALL = 5  # the timeout in seconds of the client request call
STORAGE_PATH = "/home/{}/mlruns".format("jovyan")
EXPERIMENT_NAME = "Exp123"
MODEL_NAME = "test_model"

client = docker.from_env()
container = client.containers.run(
    image=os.environ["IMAGE_NAME"],
    command='/bin/bash -c "mlflow server --host {} --port {} --backend-store-uri {}"'.format(
        HOST, PORT, STORAGE_PATH
    ),
    ports={f"{PORT}/tcp": PORT},
    detach=True,
)

time.sleep(10)
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
    try:
        url = _get_url(container)
        response = requests.get(url, timeout=TIMEOUT_CALL)
        if response.status_code == 200:
            assert True
    except ConnectionError:
        assert False


def test_example_run():
    try:
        container.exec_run(
            cmd="python3 mlrun_example.py {} {}".format(EXPERIMENT_NAME, MODEL_NAME)
        )
        assert True
    except:
        assert False


def test_search_experiments():
    """Verify that the experiment can be accessed."""
    url = _get_url(container) + "/api/2.0/mlflow/experiments/search"
    response = requests.post(
        url, json={"max_results": 3, "view_type": "ALL"}, timeout=TIMEOUT_CALL
    )
    assert response.json()["experiments"][0]["name"] == EXPERIMENT_NAME


def test_get_run():
    """Verify that metrics and params can be accessed."""

    # Get experiment ID to get RUN
    url = _get_url(container) + "/api/2.0/mlflow/experiments/search"
    response = requests.post(
        url, json={"max_results": 3, "run_view_type": "ALL"}, timeout=TIMEOUT_CALL
    )
    id = int(response.json()["experiments"][0]["experiment_id"])

    # Get run and check that our test_param can be fetched and has the correct value
    url = _get_url(container) + "/api/2.0/mlflow/runs/search"
    response = requests.post(
        url,
        json={"experiment_ids": [id], "max_results": 3, "run_view_type": "ALL"},
        timeout=TIMEOUT_CALL,
    )
    assert response.json()["runs"][0]["data"]["params"][0]["key"] == "test_param"
    assert (
        response.json()["runs"][0]["data"]["params"][0]["value"] == "1.0"
    )  # Params returns string
    assert response.json()["runs"][0]["data"]["metrics"][0]["key"] == "test_metric"
    assert (
        response.json()["runs"][0]["data"]["metrics"][0]["value"] == 0.1
    )  # Metric returns double


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
