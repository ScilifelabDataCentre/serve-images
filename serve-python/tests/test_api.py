"""Tests of the Python serving image."""

import json
import os
import time

import docker
import pytest
import requests
from requests.exceptions import RequestException

PORT = 8501
CONTAINER_PORTS = {f"{PORT}/tcp": None}
TIMEOUT_CALL = 5
STARTUP_TIMEOUT = 300

client = docker.from_env()


@pytest.fixture(scope="module")
def container():
    """Run the image on a random host port and clean it up after the tests."""
    container = client.containers.run(
        os.environ["IMAGE_NAME"],
        ports=CONTAINER_PORTS,
        detach=True,
    )
    try:
        _wait_for_ready(container)
        yield container
    finally:
        container.stop()
        container.remove()
        client.close()


def test_container_status(container):
    """Test that the Python container is running."""
    container.reload()
    assert container.status == "running"


def test_container_ports(container):
    """Test that the serving port is published."""
    container.reload()
    assert container.ports[f"{PORT}/tcp"]


def test_container_access(container):
    """Test that the health endpoint returns status 200."""
    response = requests.get(_get_api_url(container) + "/health", timeout=TIMEOUT_CALL)
    assert response.status_code == 200


def test_prediction(container):
    """Verify that the model can be used for predictions."""
    response = requests.post(
        _get_api_url(container) + "/predict/",
        json={
            "pred": "Jag är ett barn, och det här är mitt hem. Alltså är det ett barnhem!",
            "msk_ind": 4,
        },
        timeout=60,
    )
    response.raise_for_status()
    text_encoded = response.json().encode("latin1")
    prediction = json.loads(text_encoded.decode("unicode-escape"))
    assert prediction == {"result": ["barn", "hem", "hus", "spädbarn", "##hem"]}


def _get_api_url(container):
    """Get the localhost URL for the port published by Docker."""
    container.reload()
    host_port = container.ports[f"{PORT}/tcp"][0]["HostPort"]
    return f"http://127.0.0.1:{host_port}"


def _wait_for_ready(container):
    deadline = time.monotonic() + STARTUP_TIMEOUT
    while time.monotonic() < deadline:
        container.reload()
        if container.status != "running":
            raise RuntimeError(container.logs().decode())
        try:
            response = requests.get(
                _get_api_url(container) + "/health",
                timeout=TIMEOUT_CALL,
            )
            if response.status_code == 200:
                return
        except RequestException:
            pass
        time.sleep(2)
    raise TimeoutError("Python deployment did not become ready in time")
