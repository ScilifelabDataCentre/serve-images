import pytest
import requests
import os
import random as rnd
from requests.exceptions import ConnectionError


def get_inference_url():
    return "http://torchserve:8080"


def get_management_url():
    return "http://torchserve:8081"


def get_metrics_url():
    return "http://torchserve:8082"


def test_status():
    try:
        url = get_inference_url() + "/ping"
        response = requests.get(url)
        if response.status_code == 200:
            assert True
    except ConnectionError:
        assert False


def test_health():
    try:
        url = get_inference_url() + "/ping"
        response = requests.get(url)
        if response.json()["status"] == "Healthy":
            assert True
    except ConnectionError:
        assert False


def test_list_models():
    url = get_management_url() + "/models"
    response = requests.get(url)
    assert response.json()["models"][0]["modelName"] == "cnn"


def test_scale_workers():
    num_workers = rnd.randint(2, 6)
    url = get_management_url() + "/models/cnn"
    data = {"min_worker": num_workers, "synchronous": "true"}
    response = requests.put(url, params=data)
    assert response.json()["status"] == "Workers scaled to {} for model: cnn".format(
        num_workers
    )


def test_prediction():

    url = get_inference_url() + "/predictions/cnn"
    file_1 = {"data": open(os.path.join("tests", "test_data", "0.png"), "rb")}
    file_2 = {"data": open(os.path.join("tests", "test_data", "1.png"), "rb")}
    response = requests.post(url, files=file_1)
    prediction = response.json()
    assert prediction == 0

    response = requests.post(url, files=file_2)
    prediction = response.json()
    assert prediction == 1
