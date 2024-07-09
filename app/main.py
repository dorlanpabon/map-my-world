# main.py is the entry point of the application. It creates the FastAPI instance and includes the routers for locations, categories, and recommendations.
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import locations, categories, recommendations
from app.config.database import engine
from app.models import models
import asyncio

load_dotenv()

app = FastAPI(
    title="Map My World API",
    description="API for managing and exploring locations and categories",
    version="0.0.1",
    openapi_tags=[
        {"name": "Locations", "description": "Operations with locations"},
        {"name": "Categories", "description": "Operations with categories"},
        {"name": "Recommendations", "description": "Get location-category recommendations"}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(locations.router, prefix="/api", tags=["Locations"])
app.include_router(categories.router, prefix="/api", tags=["Categories"])
app.include_router(recommendations.router, prefix="/api", tags=["Recommendations"])


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Map My World API"}


async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def shutdown_event():
    await engine.dispose()

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)
