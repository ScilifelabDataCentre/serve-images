import requests


endpoint = "http://0.0.0.0:8080"

X = {'inputs': 1.2}
model_info = requests.post(endpoint+":predict",json=X, verify=False)
model_info.json()