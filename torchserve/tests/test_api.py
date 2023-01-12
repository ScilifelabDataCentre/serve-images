import pytest
import requests
import os
from requests.exceptions import ConnectionError


def get_inference_url():
    return "http://localhost:8080"

def get_management_url():
    return "http://localhost:8081"

def get_metrics_url():
    return "http://localhost:8082"

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
        if response.json()['status'] == "Healthy":
            assert True
    except ConnectionError:
        assert False

def test_prediction():

    url = get_inference_url() + "/predictions/cnn"
    base_path = os.path.join(os.getcwd(), 'tests', 'test_data')
    file_1 = {'data': open(os.path.join(base_path, '0.png'), 'rb')}
    file_2 = {'data': open(os.path.join(base_path, '1.png'), 'rb')}
    response = requests.post(url, files=file_1)
    prediction = response.json()
    assert prediction == 0

    response = requests.post(url, files=file_2)
    prediction = response.json()
    assert prediction == 1




