import os
import pytest
import requests
from requests.exceptions import ConnectionError
import random as rnd
import time
import docker


def get_inference_url(container):
    url = "http://{}:8080".format(
        container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
    )
    return url


def get_management_url(container):
    url = "http://{}:8081".format(
        container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
    )
    return url


def get_metrics_url(container):
    url = "http://{}:8082".format(
        container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
    )
    return url


client = docker.from_env()
container = client.containers.run(
    os.environ["IMAGE_NAME"],
    ports={
        "8080/tcp": 8080,
        "8081/tcp": 8081,
        "8082/tcp": 8082,
        "7070/tcp": 7070,
        "7071/tcp": 7071,
    },
    detach=True,
)
time.sleep(20)
container.reload()


def test_torchserve_status():
    assert container.status == "running"


def test_torchserve_ports():
    assert container.ports["8080/tcp"][0]["HostPort"] == "8080"
    assert container.ports["8081/tcp"][0]["HostPort"] == "8081"
    assert container.ports["8082/tcp"][0]["HostPort"] == "8082"
    assert container.ports["7070/tcp"][0]["HostPort"] == "7070"
    assert container.ports["7071/tcp"][0]["HostPort"] == "7071"


def test_torchserve_access():
    try:
        url = get_inference_url(container) + "/ping"
        response = requests.get(url)
        if response.status_code == 200:
            assert True
    except ConnectionError:
        assert False


def test_health():
    try:
        url = get_inference_url(container) + "/ping"
        response = requests.get(url)
        if response.json()["status"] == "Healthy":
            assert True
    except ConnectionError:
        assert False


def test_list_models():
    url = get_management_url(container) + "/models"
    response = requests.get(url)
    assert response.json()["models"][0]["modelName"] == "cnn"


def test_scale_workers():
    num_workers = rnd.randint(2, 6)
    url = get_management_url(container) + "/models/cnn"
    data = {"min_worker": num_workers, "synchronous": "true"}
    response = requests.put(url, params=data)
    assert response.json()["status"] == "Workers scaled to {} for model: cnn".format(
        num_workers
    )


def test_prediction():

    url = get_inference_url(container) + "/predictions/cnn"
    file_1 = {
        "data": open(
            os.path.join(os.getcwd(), "torchserve", "tests", "test_data", "0.png"), "rb"
        )
    }
    file_2 = {
        "data": open(
            os.path.join(os.getcwd(), "torchserve", "tests", "test_data", "1.png"), "rb"
        )
    }
    response = requests.post(url, files=file_1)
    prediction = response.json()
    assert prediction == 0

    response = requests.post(url, files=file_2)
    prediction = response.json()
    assert prediction == 1


def test_shutdown():
    container.stop()
    container.reload()
    assert container.status == "exited"
    container.remove()
