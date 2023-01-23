import requests
import time
import docker
import os


client = docker.from_env()
container = client.containers.run(
    os.environ["IMAGE_NAME"], ports={"8787/tcp": 8787}, detach=True
)
time.sleep(20)
container.reload()


def test_rstudio_container():
    assert container.status == "running"


def test_rstudio_port():
    assert container.ports["8787/tcp"][0]["HostPort"] == "8787"


def test_rstudio_access():
    rstudio_url = "http://{}:8787".format(
        container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
    )
    response = requests.get(rstudio_url)
    assert response.status_code == 200
    assert "RStudio" in response.text


def test_shutdown():
    container.stop()
    container.reload()
    assert container.status == "exited"
    container.remove()
