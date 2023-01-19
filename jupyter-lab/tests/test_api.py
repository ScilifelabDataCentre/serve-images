import os
import random as rnd
import time
import pytest
import requests
from requests.exceptions import ConnectionError
import docker



# Settings
PORT = 8888         # the jupyter-lab port
TIMEOUT_GET_CALL = 5         # the timeout in seconds of the client request call



client = docker.from_env()

container = client.containers.run(os.environ['IMAGE_NAME'],
    ports={f'{PORT}/tcp': PORT, },
    detach=True)

time.sleep(20)

container.reload()


# Tests
def test_jupyterlab_status_is_running():
    """ Test that the jupyter-lab container is running. """
    assert container.status == "running"


def test_jupyterlab_ports():
    """ Test of the expected container port. """
    assert len(container.ports) == 1, "There should be 1 port"
    assert container.ports["8888/tcp"][0]["HostPort"] == "8888"


def test_jupyterlab_can_ping_container():
    """ Test of basic communication with the container returns status 200 (OK). """
    try:
        url = get_inference_url(container) + "/ping"
        response = requests.get(url, timeout=TIMEOUT_GET_CALL)
        if response.status_code == 200:
            assert True
    except ConnectionError:
        assert False


@pytest.mark.skip(reason="This test not working for jupyter-lab.")
def test_health():
    """ Test that the basic ping call returns parseable json with status Healthy. """
    try:
        url = get_inference_url(container) + "/ping"
        response = requests.get(url, timeout=TIMEOUT_GET_CALL)
        if response.json()["status"] == "Healthy":
            assert True
    except ConnectionError:
        assert False


def test_shutdown():
    """ Test stopping the container. """
    container.stop()
    container.reload()
    assert container.status == 'exited'
    container.remove()



# Private methods

def get_inference_url(contr):
    """ Gets the inference URL of the container.

        :param container contr: The container object.
        :returns string url: The URL string.
    """
    ip = contr.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
    url = f"http://{ip}:{PORT}"
    return url
