import os
import platform
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import requests

app = FastAPI(title="app:a", version="1.0.1")

SERVICE_B = os.getenv("SERVICE_B_URL", "")
SERVICE_C = os.getenv("SERVICE_C_URL", "")

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}


@app.get("/info")
def get_service_info():
    return {
        "service": "app:a",
        "version": "1.0.1",
        "python_version": sys.version,
        "platform": platform.system(),
        "host": platform.node(),
    }
  
  
class ExploreRequest(BaseModel):
    service: Literal["app:b", "app:c"]


@app.post("/explore/services")
def explore_services(body: ExploreRequest):
    service = body.service
    print(f"Received request to explore service: {service}")
    if service == "app:b":
        response = requests.get(SERVICE_B + '/info')
        return {"service": "app:b", "url": SERVICE_B, "response": response.json()}

    if service == "app:c":
        response = requests.get(SERVICE_C + '/info')
        return {"service": "app:c", "url": SERVICE_C, "response": response.json()}
    return {"error": "Service not found"}