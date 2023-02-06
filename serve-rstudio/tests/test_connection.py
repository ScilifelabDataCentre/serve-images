"""Tests of the rstudio image."""

import os
import time
import requests
import docker


# Settings
PORT = 8787  # the RStudio port
TIMEOUT_CALL = 5  # the timeout in seconds of the client request call


client = docker.from_env()
container = client.containers.run(
    os.environ["IMAGE_NAME"],
    ports={
        f"{PORT}/tcp": PORT,
    },
    detach=True,
)
time.sleep(20)
container.reload()


def test_rstudio_container():
    """Test that the rstudio container is running."""
    assert container.status == "running"


def test_rstudio_port():
    """Test of the expected container port."""
    assert len(container.ports) == 1, "There should be 1 port"
    assert container.ports[f"{PORT}/tcp"][0]["HostPort"] == str(PORT)


def test_rstudio_access():
    """Test of basic communication with the container returns status 200 (OK)."""
    url = _get_url(container)
    try:
        response = requests.get(url, timeout=TIMEOUT_CALL)
        assert response.status_code == 200
        assert "RStudio" in response.text
    except ConnectionError:
        assert False


def test_shutdown():
    """Test stopping the container."""
    container.stop()
    container.reload()
    assert container.status == "exited"
    container.remove()


# Private methods


def _get_url(container):
    """Gets the URL of the container."""
    ip = container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
    url = "http://{}:8787".format(ip)
    return url
