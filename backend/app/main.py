from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.config import config
from backend.app.routes import attacks, detection, replay, logs

app = FastAPI(title="SOC Shadow Box API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(attacks.router)
app.include_router(detection.router)
app.include_router(replay.router)
app.include_router(logs.router)

@app.get("/")
async def root():
    return {"message": "SOC Shadow Box API Running", "status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
from backend.app.routes import export
app.include_router(export.router)
