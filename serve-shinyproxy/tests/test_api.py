import os
import requests
import docker
import time

PORT = 8080  # Shinyproxy port
TIMEOUT_CALL = 5  # the timeout in seconds of the client request call

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
    url = _get_url(container)+"/api/proxyspec"
    max_attempts = 100

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, timeout=TIMEOUT_CALL)
            if response.status_code == 200:
                print("Shinyproxy is up and running!")
                assert True
                break
        except:
            pass

        if attempt == max_attempts:
            RuntimeError(f"Shinyproxy did not become ready after {max_attempts} attempts")
            assert False

        print(
            f"Attempt {attempt} failed, waiting for 10 seconds before trying again..."
        )
        time.sleep(10)

def _get_url(container):
    """Gets the URL of the container."""
    ip = container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
    url = "http://{}:{}".format(ip, PORT)
    return url
