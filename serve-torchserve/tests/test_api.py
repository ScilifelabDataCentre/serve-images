"""Tests of the torchserve image."""

import os
import time
import random as rnd
import requests
from requests.exceptions import ConnectionError
import pytest
import docker


# Settings
PORTS = [8080, 8081, 8082, 7070, 7071]  # the torchserve ports
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


def test_torchserve_status():
    """Test that the torchserve container is running."""
    assert container.status == "running"


def test_torchserve_ports():
    """Test of the expected container ports."""
    assert all(
        value[0]["HostPort"] == key.split("/")[0]
        for key, value in container.ports.items()
    )


def test_torchserve_access():
    """Test of basic communication with the container returns status 200 (OK)."""
    try:
        url = _get_inference_url(container) + "/ping"
        response = requests.get(url, timeout=TIMEOUT_CALL)
        if response.status_code == 200:
            assert True
    except ConnectionError:
        assert False


def test_health():
    try:
        url = _get_inference_url(container) + "/ping"
        response = requests.get(url, timeout=TIMEOUT_CALL)
        if response.json()["status"] == "Healthy":
            assert True
    except ConnectionError:
        assert False


def test_list_models():
    """Verify that the CNN model can be accessed."""
    url = _get_management_url(container) + "/models"
    response = requests.get(url, timeout=15)
    assert response.json()["models"][0]["modelName"] == "cnn"


def test_scale_workers():
    """Verify that the number of workers can be scaled."""
    num_workers = rnd.randint(2, 6)
    url = _get_management_url(container) + "/models/cnn"
    data = {"min_worker": num_workers, "synchronous": "true"}
    response = requests.put(url, params=data)
    assert response.json()["status"] == "Workers scaled to {} for model: cnn".format(
        num_workers
    )


def test_prediction():
    """Test that we can send MNIST images to the model an get the correct prediction in return.
    Do this twice to avoid false positive"""
    url = _get_inference_url(container) + "/predictions/cnn"
    file_1 = {
        "data": open(
            os.path.join(os.getcwd(), "torchserve", "tests", "test_data", "0.png"), "rb"
        )
    }
    file_2 = {
        "data": open(
            os.path.join(os.getcwd(), "torchserve", "tests", "test_data", "1.png"), "rb"
        )
    }
    response = requests.post(url, files=file_1)
    prediction = response.json()
    assert prediction == 0

    response = requests.post(url, files=file_2)
    prediction = response.json()
    assert prediction == 1


def test_shutdown():
    container.stop()
    container.reload()
    assert container.status == "exited"
    container.remove()


# Private methods


def _get_ip(container):
    """Gets the IP of the container."""
    return container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]


def _get_inference_url(container):
    """Gets the correct adress for inference."""
    url = "http://{}:8080".format(_get_ip(container))
    return url


def _get_management_url(container):
    """Gets the correct adress for torchserve management."""
    url = "http://{}:8081".format(_get_ip(container))
    return url
