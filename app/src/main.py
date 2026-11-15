from fastapi import FastAPI
from contextlib import asynccontextmanager

from data.database import pool
from routes.serverHealth import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open(wait=True)

    yield

    pool.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router)