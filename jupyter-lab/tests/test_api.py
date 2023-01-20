import os
import random as rnd
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
PORT = 8888         # the jupyter-lab port
TIMEOUT_CALL = 5    # the timeout in seconds of the client request call
TOKEN = "dev12345"      # "a268cff61a101aaefe53b02b5a787ddfc0e07d4119154bff"
HOST = "localhost:8888"
NOTEBOOK_PATH = "/notebooks/basic.ipynb"



client = docker.from_env()

container = client.containers.run(os.environ['IMAGE_NAME'],
    command="start-notebook.sh --NotebookApp.token='dev12345'",
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
        response = requests.get(url, timeout=TIMEOUT_CALL)
        if response.status_code == 200:
            assert True
    except ConnectionError:
        assert False


@pytest.mark.skip(reason="This test not working for jupyter-lab.")
def test_health():
    """ Test that the basic ping call returns parseable json with status Healthy. """
    try:
        url = get_inference_url(container) + "/ping"
        response = requests.get(url, timeout=TIMEOUT_CALL)
        if response.json()["status"] == "Healthy":
            assert True
    except ConnectionError:
        assert False


def test_notebook():
    """ Test of notebook outputs.
    """
    print("Begin run_api.py")

    headers = {'Authorization': 'Token {0}'.format(TOKEN)}

    cell_outputs = _get_notebook_cell_outputs(headers, HOST, NOTEBOOK_PATH, TIMEOUT_CALL)

    print(cell_outputs)
    assert len(cell_outputs) == 1, len(cell_outputs)

    val = cell_outputs[0]

    assert type(val) == str
    assert val == "9", val

    print("Done")


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


def _get_notebook_cell_outputs(headers, host, notebook_path, timeout_call):
    """ Gets the output contents of all notebook code cells.
    """
    base_url = f"http://{host}"

    url = base_url + '/api/kernels'
    response = requests.post(url,headers=headers, timeout=timeout_call)
    kernel = json.loads(response.text)

    # Load the notebook and get the code of each cell
    url = base_url + '/api/contents' + notebook_path
    response = requests.get(url,headers=headers, timeout=timeout_call)
    file = json.loads(response.text)

    print(file)

    code = [ c['source'] for c in file['content']['cells'] if c['cell_type']=="code" and len(c['source'])>0 ]

    print(code)
    print("Creating connection to api/kernels")

    ws = create_connection(f"ws://{host}/api/kernels/" + kernel["id"]+"/channels",
        header=headers)

    print("Sending code in loop")

    for c in code:
        ws.send(json.dumps(_send_execute_request(c)))

    # We ignore all the other messages, we just get the code execution output
    # (this needs to be improved for production to take into account errors, large cell output, images, etc.)

    print("Output of results:")

    outputs = []

    for i in range(0, len(code)):
        msg_type = ''
        while msg_type != "stream":
            rsp = json.loads(ws.recv())
            msg_type = rsp["msg_type"]
        val = rsp["content"]["text"].strip()
        outputs.append(val)

    ws.close()
    return outputs



def _send_execute_request(code):
    """ Gets a message body to send to a jupyter lab server.
    """
    msg_type = 'execute_request'
    content = { 'code' : code, 'silent':False }
    hdr = { 'msg_id' : uuid.uuid1().hex, 
        'username': 'test', 
        'session': uuid.uuid1().hex, 
        'data': datetime.datetime.now().isoformat(),
        'msg_type': msg_type,
        'version' : '5.0' }
    msg = { 'header': hdr, 'parent_header': hdr, 
        'metadata': {},
        'content': content }
    return msg
