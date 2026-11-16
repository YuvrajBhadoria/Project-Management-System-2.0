from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.data.database import pool
from src.routes.userRoutes import router as userRoutes
from src.routes.organizationRoutes import router as organizationRoutes

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open(wait=True)

    yield

    pool.close()


app = FastAPI(lifespan=lifespan)

app.include_router(userRoutes)
app.include_router(organizationRoutes)