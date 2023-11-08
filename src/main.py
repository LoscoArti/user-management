from fastapi import FastAPI

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
