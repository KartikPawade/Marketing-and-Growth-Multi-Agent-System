# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import setup_logging
from app.api.routes_brand import router as brand_router
from app.api.routes_campaign import router as campaign_router

setup_logging()

app = FastAPI(title="Multi Agents Marketing and Growth System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(brand_router)
app.include_router(campaign_router)

@app.get("/health")
def health():
    return {"status": "ok"}