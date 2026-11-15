from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.data.database import pool
from src.routes.userRoutes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open(wait=True)

    yield

    pool.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router)