"""Tests of the TorchServe image."""

import json
import os
import random as rnd
import time

import docker
import pytest
import requests
from requests.exceptions import RequestException

# Settings
PORTS = [8080, 8081, 8082, 7070, 7071]
CONTAINER_PORTS = {f"{port}/tcp": None for port in PORTS}
TIMEOUT_CALL = 5
STARTUP_TIMEOUT = 60

client = docker.from_env()


@pytest.fixture(scope="module")
def torchserve():
    """Run TorchServe with random host ports and clean it up after the tests."""
    container = client.containers.run(
        os.environ["IMAGE_NAME"],
        ports=CONTAINER_PORTS,
        detach=True,
    )
    try:
        tokens = _wait_for_tokens(container)
        _wait_for_ready(container, tokens["inference"]["key"])
        yield container, tokens
    finally:
        container.stop()
        container.remove()


def test_torchserve_status(torchserve):
    """Test that the TorchServe container is running."""
    container, _ = torchserve
    container.reload()
    assert container.status == "running"


def test_torchserve_ports(torchserve):
    """Test that all expected container ports are published."""
    container, _ = torchserve
    container.reload()
    assert all(container.ports[f"{port}/tcp"] for port in PORTS)


def test_torchserve_access(torchserve):
    """Test that the inference API returns status 200."""
    container, tokens = torchserve
    response = requests.get(
        _get_inference_url(container) + "/ping",
        headers=_authorization_header(tokens["inference"]["key"]),
        timeout=TIMEOUT_CALL,
    )
    assert response.status_code == 200


def test_health(torchserve):
    """Test that TorchServe reports itself as healthy."""
    container, tokens = torchserve
    response = requests.get(
        _get_inference_url(container) + "/ping",
        headers=_authorization_header(tokens["inference"]["key"]),
        timeout=TIMEOUT_CALL,
    )
    assert response.json()["status"] == "Healthy"


def test_list_models(torchserve):
    """Verify that the CNN model can be accessed."""
    container, tokens = torchserve
    response = requests.get(
        _get_management_url(container) + "/models",
        headers=_authorization_header(tokens["management"]["key"]),
        timeout=15,
    )
    assert response.json()["models"][0]["modelName"] == "cnn"


def test_scale_workers(torchserve):
    """Verify that the number of workers can be scaled."""
    container, tokens = torchserve
    num_workers = rnd.randint(2, 6)
    response = requests.put(
        _get_management_url(container) + "/models/cnn",
        params={"min_worker": num_workers, "synchronous": "true"},
        headers=_authorization_header(tokens["management"]["key"]),
        timeout=15,
    )
    assert (
        response.json()["status"] == f"Workers scaled to {num_workers} for model: cnn"
    )


def test_prediction(torchserve):
    """Test that two MNIST images produce the correct predictions."""
    container, tokens = torchserve
    url = _get_inference_url(container) + "/predictions/cnn"
    headers = _authorization_header(tokens["inference"]["key"])

    with open(
        os.path.join(os.getcwd(), "serve-torchserve", "tests", "test_data", "0.png"),
        "rb",
    ) as image:
        response = requests.post(
            url, files={"data": image}, headers=headers, timeout=15
        )
    assert response.json() == 0

    with open(
        os.path.join(os.getcwd(), "serve-torchserve", "tests", "test_data", "1.png"),
        "rb",
    ) as image:
        response = requests.post(
            url, files={"data": image}, headers=headers, timeout=15
        )
    assert response.json() == 1


def _authorization_header(token):
    return {"Authorization": f"Bearer {token}"}


def _get_url(container, port):
    """Get the localhost URL for a container port published by Docker."""
    container.reload()
    host_port = container.ports[f"{port}/tcp"][0]["HostPort"]
    return f"http://127.0.0.1:{host_port}"


def _get_inference_url(container):
    """Get the inference API URL."""
    return _get_url(container, 8080)


def _get_management_url(container):
    """Get the management API URL."""
    return _get_url(container, 8081)


def _wait_for_tokens(container):
    deadline = time.monotonic() + STARTUP_TIMEOUT
    while time.monotonic() < deadline:
        result = container.exec_run("cat /home/model-server/key_file.json")
        if result.exit_code == 0:
            return json.loads(result.output)
        time.sleep(1)
    raise TimeoutError("TorchServe did not create its authorization tokens in time")


def _wait_for_ready(container, token):
    deadline = time.monotonic() + STARTUP_TIMEOUT
    while time.monotonic() < deadline:
        container.reload()
        if container.status != "running":
            raise RuntimeError(container.logs().decode())
        try:
            response = requests.get(
                _get_inference_url(container) + "/ping",
                headers=_authorization_header(token),
                timeout=TIMEOUT_CALL,
            )
            if response.status_code == 200:
                return
        except RequestException:
            pass
        time.sleep(1)
    raise TimeoutError("TorchServe did not become ready in time")
