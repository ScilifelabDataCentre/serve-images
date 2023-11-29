"""Tests of the python image."""

import os
import time
import random as rnd
import requests
from requests.exceptions import ConnectionError
import pytest
import docker
import json
import numpy as np


# Settings
PORTS = [8501]  # the fastapi port
CONTAINER_PORTS = {f"{port}/tcp": port for port in PORTS}
TIMEOUT_CALL = 5  # the timeout in seconds of the client request call

client = docker.from_env()
container = client.containers.run(
    os.environ["IMAGE_NAME"],
    ports=CONTAINER_PORTS,
    detach=True,
)
time.sleep(20)
container.reload()


def test_container_status():
    """Test that the python container is running."""
    assert container.status == "running"


def test_container_ports():
    """Test of the expected container ports."""
    assert all(
        PORTS[i] == int(key.split("/")[0])
        for i, (key, _) in enumerate(container.ports.items())
    )


def test_container_access():
    """Test of basic communication with the container returns status 200 (OK)."""
    try:
        url = _get_api_url(container) + "/health"
        response = requests.get(url, timeout=TIMEOUT_CALL)
        if response.status_code == 200:
            assert True
    except ConnectionError:
        assert False


def test_prediction():
    """Verify that the model can be used for predictions."""
    # Set input string
    example = "Jag är ett barn, och det här är mitt hem. Alltså är det ett barnhem!"
    # msk_ind takes an index in order to mask (or hide) one of the word in the example sentence, which should then be predicted by the BERT trained model
    msk_ind = 4
    url = _get_api_url(container) + "/predict/"
    res = requests.post(url, json={"pred": example, "msk_ind": msk_ind})
    text_encoded = res.json().encode("latin1")
    text_decoded = text_encoded.decode("unicode-escape")
    print(json.loads(text_decoded))
    assert json.loads(text_decoded) == {
        "result": ["barn", "hem", "hus", "spädbarn", "##hem"]
    }


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


def _get_api_url(container):
    """Gets the correct adress for inference."""
    url = "http://{}:{}".format(_get_ip(container), PORTS[0])
    return url
