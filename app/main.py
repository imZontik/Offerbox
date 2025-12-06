from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.auth.routers import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app():
    _app = FastAPI(
        title="Offerbox API",
        description="API for offers",
        version="1.0",
        lifespan=lifespan
    )

    _app.include_router(auth_router)

    return _app


app = create_app()