# app/main.py
from fastapi import FastAPI

from app.core.logging import setup_logging
from app.api.routes_campaign import router as campaign_router

setup_logging()

app = FastAPI(title="Multi Agents Marketing and Growth System")
app.include_router(campaign_router)

@app.get("/health")
def health():
    return {"status": "ok"}