import os
import platform
import sys
from fastapi import FastAPI, Request
import requests

app = FastAPI(title="app:a", version="1.0.0")

SERVICE_B = os.getenv("SERVICE_B_URL", "")
SERVICE_C = os.getenv("SERVICE_C_URL", "")

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}


@app.get("/info")
def get_service_info():
    return {
        "service": "app:a",
        "version": "1.0.0",
        "python_version": sys.version,
        "platform": platform.system(),
        "host": platform.node(),
    }
  
  
@app.get("/explore/services")
def get_service_info(request: Request):
    query_params = request.query_params
    target_service = query_params.get("service")
    
    print(f"Received request to explore service: {target_service}")
    if target_service == "app:b":
        response = requests.get(SERVICE_B)
        return {"service": "app:b", "url": SERVICE_B, "response": response.json()}
    
    if target_service == "app:c":
        response = requests.get(SERVICE_C)
        return {"service": "app:c", "url": SERVICE_C, "response": response.json()}
    return {"error": "Service not found"}