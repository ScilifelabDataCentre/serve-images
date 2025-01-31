"""Tests of the jupyter-lab image using API calls."""

import os
import time
import datetime
import uuid
import json
import requests
from requests.exceptions import ConnectionError
from websocket import create_connection
import pytest
import docker


# Settings
PORT = 8888  # the jupyter-lab port
HOST = f"localhost:{PORT}"  # the host
NOTEBOOK_PATH = "tests/basic.ipynb"  # the relative path to the jupyter test notebook
TOKEN = "a268cff61a101aaefe53b02b5a787ddfc0e07d4119154bff"  # the token to use
TIMEOUT_CALL = 5  # the timeout in seconds of the client request call


client = docker.from_env()

container = client.containers.run(
    os.environ["IMAGE_NAME"],
    command=f"start-notebook.sh --NotebookApp.token='{TOKEN}'",
    ports={
        f"{PORT}/tcp": PORT,
    },
    detach=True,
)

time.sleep(20)

container.reload()


# Tests
def test_jupyterlab_status_is_running():
    """Test that the jupyter-lab container is running."""
    assert container.status == "running"


def test_jupyterlab_ports():
    """Test of the expected container port."""
    assert len(container.ports) == 1, "There should be 1 port"
    assert container.ports[f"{PORT}/tcp"][0]["HostPort"] == str(PORT)


def test_jupyterlab_can_ping_container():
    """Test of basic communication with the container returns status 200 (OK)."""
    try:
        url = _get_inference_url(container) + "/ping"
        response = requests.get(url, timeout=TIMEOUT_CALL)
        if response.status_code == 200:
            assert True
    except ConnectionError:
        assert False


def test_verify_test_files():
    """Verify that the test notebooks exist and can be accessed."""
    headers = {"Authorization": "Token {0}".format(TOKEN)}
    nb_path = _get_notebooks(headers, HOST, TIMEOUT_CALL)
    assert nb_path == NOTEBOOK_PATH, "The notebook path"


def test_notebook():
    """Test of notebook outputs."""
    headers = {"Authorization": "Token {0}".format(TOKEN)}

    cell_outputs = _get_notebook_cell_outputs(
        headers, HOST, NOTEBOOK_PATH, TIMEOUT_CALL
    )
    assert len(cell_outputs) == 3, len(cell_outputs)

    val = cell_outputs[0]
    assert type(val) == str
    assert val == "9", val

    lfs_init_val = cell_outputs[1]
    assert type(lfs_init_val) == str
    assert lfs_init_val == "Git LFS initialized.", lfs_init_val
    
    lfs_ver_val = cell_outputs[2]
    assert type(lfs_ver_val) == str
    assert lfs_ver_val == "git-lfs/3.0.2 (GitHub; linux arm64; go 1.18.1)", lfs_ver_val


def test_shutdown():
    """Test stopping the container."""
    container.stop()
    container.reload()
    assert container.status == "exited"
    container.remove()


# Private methods


def _get_inference_url(contr):
    """Gets the inference URL of the container.

    :param container contr: The container object.
    :returns string url: The URL string.
    """
    ip = contr.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
    url = f"http://{ip}:{PORT}"
    return url


def _get_notebooks(headers, host, timeout_call):
    """Gets a list of relative paths to notebooks in jupyter-lab."""
    base_url = f"http://{host}"

    # Verify the notebook folder work exists
    url = base_url + "/api/contents"
    response = requests.get(url, headers=headers, timeout=timeout_call)
    assert response.status_code == 200, f"response status is {response.status_code}"
    contents = json.loads(response.text)

    for item in contents["content"]:
        print(f"{item['name']}, {item['path']}")

    assert len(contents["content"]) >= 2, "There should be 2 folders: tests and work"

    url = base_url + "/api/contents/tests"
    response = requests.get(url, headers=headers, timeout=timeout_call)
    assert response.status_code == 200, f"response status is {response.status_code}"

    folder_contents = json.loads(response.text)
    assert len(folder_contents["content"]) == 1, "There should be 1 tests folder"

    nb_path = folder_contents["content"][0]["path"]
    return nb_path


def _get_notebook_cell_outputs(headers, host, notebook_path, timeout_call):
    """Gets the output contents of all notebook code cells."""
    base_url = f"http://{host}"

    url = base_url + "/api/kernels"
    response = requests.post(url, headers=headers, timeout=timeout_call)
    assert response.status_code == 201, f"response status is {response.status_code}"
    kernel = json.loads(response.text)

    # Load the notebook and get the code of each cell
    url = base_url + "/api/contents/" + notebook_path
    response = requests.get(url, headers=headers, timeout=timeout_call)
    assert (
        response.status_code == 200
    ), f"response status is {response.status_code}. URL used {url}"

    file = json.loads(response.text)

    code = [
        c["source"]
        for c in file["content"]["cells"]
        if c["cell_type"] == "code" and len(c["source"]) > 0
    ]

    print(code)
    print("Creating connection to api/kernels")

    ws = create_connection(
        f"ws://{host}/api/kernels/" + kernel["id"] + "/channels", header=headers
    )

    print("Sending code in loop")

    for c in code:
        ws.send(json.dumps(_send_execute_request(c)))

    outputs = []

    for i in range(0, len(code)):
        msg_type = ""
        while msg_type != "stream":
            rsp = json.loads(ws.recv())
            msg_type = rsp["msg_type"]
        val = rsp["content"]["text"].strip()
        outputs.append(val)

    ws.close()
    return outputs


def _send_execute_request(code):
    """Gets a message body to send to a jupyter lab server."""
    msg_type = "execute_request"
    content = {"code": code, "silent": False}
    hdr = {
        "msg_id": uuid.uuid1().hex,
        "username": "test",
        "session": uuid.uuid1().hex,
        "data": datetime.datetime.now().isoformat(),
        "msg_type": msg_type,
        "version": "5.0",
    }
    msg = {"header": hdr, "parent_header": hdr, "metadata": {}, "content": content}
    return msg
