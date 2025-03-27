"""Tests of the vscode container using API calls."""

import os
import time
import requests
import docker
import pytest
from requests.exceptions import ConnectionError

# Settings
PORT = 1234  # code-server port
HOST = f"localhost:{PORT}"
TIMEOUT = 20  # Time to wait for container startup
TEST_FILE_PATH = "/home/serve/tests/test.py"
IMAGE_NAME = os.environ["IMAGE_NAME"]

# Setup Docker client
client = docker.from_env()

# Start container with code-server
container = client.containers.run(
    IMAGE_NAME,
    command=["/bin/bash", "-l", "-c", "umask 007 && /usr/bin/code-server --auth=none --bind-addr=0.0.0.0:1234 /home/serve/"],
    ports={f"{PORT}/tcp": PORT},
    detach=True
)

# Wait for container to start
time.sleep(TIMEOUT)
container.reload()

# Tests
def test_container_status():
    """Verify container is running"""
    assert container.status == "running"

def test_port_mapping():
    """Test port mapping"""
    assert len(container.ports) == 1
    assert container.ports[f"{PORT}/tcp"][0]["HostPort"] == str(PORT)

def test_server_health():
    """Test code-server health endpoint"""
    try:
        response = requests.get(f"http://{HOST}/healthz", timeout=5)
        assert response.status_code == 200
    except ConnectionError:
        assert False, "Failed to connect to code-server"

def test_file_permissions():
    """Verify test file permissions"""
    # Execute command in container to check permissions
    exit_code, output = container.exec_run(f"stat -c '%a' {TEST_FILE_PATH}")
    assert exit_code == 0
    assert output.decode().strip() == "660"

def test_file_output():
    """Verify test file output"""
    exit_code, output = container.exec_run("python3 tests/test.py")
    assert exit_code == 0
    assert output.decode().strip() == "It works!"

def test_shutdown():
    """Test container shutdown"""
    container.stop()
    container.reload()
    assert container.status in ("exited", "stopped")
    container.remove()