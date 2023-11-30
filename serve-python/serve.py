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


@app.post("/predict/")
async def predict_route(
    pred_request: PredType = defv, X_Auth_Username: Optional[List[str]] = Header(None)
):
    print("Username: {}".format(X_Auth_Username))
    print(pred_request)
    res = predict.model_predict(pred_request, model_data)
    return json.dumps(res)


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
)
def get_health():
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on.
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return {"status": "OK"}
