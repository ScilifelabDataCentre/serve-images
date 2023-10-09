import os
import requests
import docker
import time

PORT = 8080  # Shinyproxy port

client = docker.from_env()
container = client.containers.run(
    image=os.environ["IMAGE_NAME"],
    ports={f"{PORT}/tcp": PORT},
    detach=True,
)
time.sleep(10)  # Update this somehow.
container.reload()


def test_container_status():
    """Test that the Shinyproxy container is running."""
    assert container.status == "running"


def test_container_ports():
    """Test of the expected container port."""
    assert len(container.ports) == 1, "There should be 1 port"
    assert container.ports[f"{PORT}/tcp"][0]["HostPort"] == str(PORT)

def test_proxyspec():
    url = _get_url
    r = requests.get(f"{url}/api/proxyspec")
    assert r.status_code == 200
    assert len(r.json()) == 2

def _get_url(container):
    """Gets the URL of the container."""
    ip = container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
    url = "http://{}:{}".format(ip, PORT)
    return url
