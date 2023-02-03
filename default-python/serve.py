import os
from typing import Optional

from fastapi import FastAPI, Header, File, UploadFile
from typing import List, Optional
from pydantic import BaseModel
import subprocess
import json

from fastapi import FastAPI

import time
from prometheus_client import Counter, Histogram
from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST,
    REGISTRY,
    multiprocess,
    CollectorRegistry,
)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.responses import Response

from src.models import predict

REQUEST_TIME = Histogram(
    "serve_predict_duration_seconds",
    "Prediction duration in seconds",
    ("method", "status_code", "path"),
)


REQUEST_COUNT = Counter(
    "serve_predict_total",
    "Total number of predict calls",
    ("method", "status_code", "path"),
)


class PromMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        method = request.method
        path = request.url.path
        timer_begin = time.time()

        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
        except:
            raise Exception("Call failed.")

        timer_end = time.time()

        labels = [method, status_code, path]

        REQUEST_COUNT.labels(*labels).inc()
        REQUEST_TIME.labels(*labels).observe(timer_end - timer_begin)
        return response


def metrics(request):
    registry = REGISTRY
    if "prometheus_multiproc_dir" in os.environ:
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)

    data = generate_latest(registry)
    response_headers = {"Content-Type": CONTENT_TYPE_LATEST}

    return Response(data, status_code=200, headers=response_headers)


try:
    from src.models import input_type

    PredType = input_type.PredType
    print("User defined input type.")
except:
    print("Using default input type.")

    class PredType(BaseModel):
        pred: str


try:
    from src.models import input_type

    defv = input_type.defv
except:
    defv = None

model_data = []
if hasattr(predict, "model_load"):
    print("Loading model...")
    model_data = predict.model_load()
    print("Done.")

app = FastAPI()
app.add_middleware(PromMiddleware)
app.add_route("/metrics/", metrics)


@app.post("/predict/")
async def predict_route(
    pred_request: PredType = defv, X_Auth_Username: Optional[List[str]] = Header(None)
):
    print("Username: {}".format(X_Auth_Username))
    print(pred_request)
    res = predict.model_predict(pred_request, model_data)
    return json.dumps(res)
