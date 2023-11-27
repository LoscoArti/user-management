from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth.router import router as auth_router
from log.logging_config import logger
from src.auth.redis import close_redis_client, get_redis_client
from user.router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_redis_client()
    yield
    await close_redis_client()


app = FastAPI(
    title="User Management service",
    description="Main service is responsible for registration \
                and authentication users",
    lifespan=lifespan,
)


@app.get("/healthcheck")
async def health_check():
    logger.info("Health check")
    return {"response": "Ok"}


app.include_router(auth_router)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
