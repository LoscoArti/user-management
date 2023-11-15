from fastapi import FastAPI

from auth import router as auth_router
from log.logging_config import logger

app = FastAPI(
    title="User Management service",
    description="Main service is responsible for registration \
                and authentication users",
)


@app.get("/healthcheck")
async def health_check():
    logger.info("Health check")
    return {"response": "Ok"}


app.include_router(auth_router.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
