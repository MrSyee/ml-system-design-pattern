from logging import getLogger

from fastapi import FastAPI
from src.app.routers import routers


logger = getLogger(__name__)

app = FastAPI(
    title="Asynchronous pattern"
)

app.include_router(routers.router, prefix="", tags=[""])
