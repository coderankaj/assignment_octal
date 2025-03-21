from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import FastAPI, HTTPException

from src.app.routes import v1_router
from src.config import settings


# Caching settings for efficient access
@lru_cache
def get_settings():
    return settings


# Lifespan context manager to initialize models and setup the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"FastAPI running in {get_settings().fastapi_env} environment")

    # Include API router
    app.include_router(v1_router, prefix="/api")

    # Yield control back to FastAPI for the lifespan duration
    yield


# Create FastAPI application instance
app = FastAPI(
    debug=get_settings().debug,
    title=get_settings().app.name,
    description=get_settings().app.description,
    version=get_settings().app.version,
    summary=get_settings().app.summary,
    terms_of_service=get_settings().app.terms_of_service_url,
    contact={
        "name": get_settings().app.contact.name,
        "email": get_settings().app.contact.email,
        "url": get_settings().app.contact.url,
    },
    lifespan=lifespan,
)

# setup app middleware here
# .....

# setup exception handlers here
# ....
