from contextlib import asynccontextmanager

from fastapi import FastAPI


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

    return _app


app = create_app()