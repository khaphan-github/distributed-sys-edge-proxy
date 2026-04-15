import platform
import sys
from fastapi import FastAPI

app = FastAPI(title="app:c", version="1.0.0")


@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}


@app.get("/info")
def get_service_info():
    return {
        "service": "app:c",
        "version": "1.0.0",
        "python_version": sys.version,
        "platform": platform.system(),
        "host": platform.node(),
    }
  