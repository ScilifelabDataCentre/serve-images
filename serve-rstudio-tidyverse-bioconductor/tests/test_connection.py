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
time.sleep(1)
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
    max_attempts = 50

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, timeout=TIMEOUT_CALL)
            if response.status_code == 200:
                print("RStudio is up and running!")
                assert True
                break
        except:
            pass

        if attempt == max_attempts:
            RuntimeError(f"Rstudio did not become ready after {max_attempts} attempts")
            assert False

        print(
            f"Attempt {attempt} failed, waiting for 10 seconds before trying again..."
        )
        time.sleep(10)


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
    url = "http://{}:{}".format(ip, PORT)
    return url
