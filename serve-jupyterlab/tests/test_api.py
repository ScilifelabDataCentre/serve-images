"""Tests of the JupyterLab image using API calls."""

import datetime
import json
import os
import time
import uuid

import docker
import pytest
import requests
from requests.exceptions import RequestException
from websocket import create_connection

PORT = 8888
NOTEBOOK_PATH = "tests/basic.ipynb"
TOKEN = "a268cff61a101aaefe53b02b5a787ddfc0e07d4119154bff"
TIMEOUT_CALL = 5
STARTUP_TIMEOUT = 120

client = docker.from_env()


@pytest.fixture(scope="module")
def jupyterlab():
    """Run JupyterLab on a random host port and clean it up after the tests."""
    container = client.containers.run(
        os.environ["IMAGE_NAME"],
        command=f"start-notebook.sh --NotebookApp.token='{TOKEN}'",
        ports={f"{PORT}/tcp": None},
        detach=True,
    )
    try:
        _wait_for_ready(container)
        yield container
    finally:
        container.stop()
        container.remove()
        client.close()


def test_jupyterlab_status_is_running(jupyterlab):
    """Test that the JupyterLab container is running."""
    jupyterlab.reload()
    assert jupyterlab.status == "running"


def test_jupyterlab_ports(jupyterlab):
    """Test that the JupyterLab port is published."""
    jupyterlab.reload()
    assert jupyterlab.ports[f"{PORT}/tcp"]


def test_jupyterlab_can_ping_container(jupyterlab):
    """Test that the JupyterLab API returns status 200."""
    response = requests.get(
        _get_base_url(jupyterlab) + "/api",
        headers=_authorization_headers(),
        timeout=TIMEOUT_CALL,
    )
    assert response.status_code == 200


def test_verify_test_files(jupyterlab):
    """Verify that the test notebook exists and can be accessed."""
    notebook_path = _get_notebooks(
        _authorization_headers(),
        _get_host(jupyterlab),
        TIMEOUT_CALL,
    )
    assert notebook_path == NOTEBOOK_PATH


def test_notebook(jupyterlab):
    """Test the notebook outputs."""
    cell_outputs = _get_notebook_cell_outputs(
        _authorization_headers(),
        _get_host(jupyterlab),
        NOTEBOOK_PATH,
        TIMEOUT_CALL,
    )
    assert len(cell_outputs) == 3
    assert cell_outputs[0] == "9"
    assert cell_outputs[1] == "Git LFS initialized."
    assert cell_outputs[2].startswith("git-lfs/")
    assert "linux" in cell_outputs[2]


def _authorization_headers():
    return {"Authorization": f"Token {TOKEN}"}


def _get_host(container):
    """Get the localhost address for the port published by Docker."""
    container.reload()
    host_port = container.ports[f"{PORT}/tcp"][0]["HostPort"]
    return f"127.0.0.1:{host_port}"


def _get_base_url(container):
    return f"http://{_get_host(container)}"


def _wait_for_ready(container):
    deadline = time.monotonic() + STARTUP_TIMEOUT
    while time.monotonic() < deadline:
        container.reload()
        if container.status != "running":
            raise RuntimeError(container.logs().decode())
        try:
            response = requests.get(
                _get_base_url(container) + "/api",
                headers=_authorization_headers(),
                timeout=TIMEOUT_CALL,
            )
            if response.status_code == 200:
                return
        except RequestException:
            pass
        time.sleep(2)
    raise TimeoutError("JupyterLab did not become ready in time")


def _get_notebooks(headers, host, timeout_call):
    """Get a list of relative paths to notebooks in JupyterLab."""
    base_url = f"http://{host}"

    response = requests.get(
        base_url + "/api/contents",
        headers=headers,
        timeout=timeout_call,
    )
    response.raise_for_status()
    contents = response.json()
    assert len(contents["content"]) >= 2

    response = requests.get(
        base_url + "/api/contents/tests",
        headers=headers,
        timeout=timeout_call,
    )
    response.raise_for_status()
    folder_contents = response.json()
    assert len(folder_contents["content"]) == 1
    return folder_contents["content"][0]["path"]


def _get_notebook_cell_outputs(headers, host, notebook_path, timeout_call):
    """Get the output contents of all notebook code cells."""
    base_url = f"http://{host}"

    response = requests.post(
        base_url + "/api/kernels",
        headers=headers,
        timeout=timeout_call,
    )
    assert response.status_code == 201
    kernel = response.json()

    response = requests.get(
        base_url + "/api/contents/" + notebook_path,
        headers=headers,
        timeout=timeout_call,
    )
    response.raise_for_status()
    notebook = response.json()
    code = [
        cell["source"]
        for cell in notebook["content"]["cells"]
        if cell["cell_type"] == "code" and cell["source"]
    ]

    websocket = create_connection(
        f"ws://{host}/api/kernels/{kernel['id']}/channels",
        header=headers,
    )
    try:
        for cell in code:
            websocket.send(json.dumps(_send_execute_request(cell)))

        outputs = []
        for _ in code:
            message_type = ""
            while message_type != "stream":
                response = json.loads(websocket.recv())
                message_type = response["msg_type"]
            outputs.append(response["content"]["text"].strip())
        return outputs
    finally:
        websocket.close()


def _send_execute_request(code):
    """Get a message body to send to a JupyterLab server."""
    header = {
        "msg_id": uuid.uuid1().hex,
        "username": "test",
        "session": uuid.uuid1().hex,
        "data": datetime.datetime.now().isoformat(),
        "msg_type": "execute_request",
        "version": "5.0",
    }
    return {
        "header": header,
        "parent_header": header,
        "metadata": {},
        "content": {"code": code, "silent": False},
    }
