from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.log.logging_config import logger
from src.user.router import router as user_router

app = FastAPI(
    title="User Management service",
    description="Main service is responsible for registration \
                and authentication users",
)


@app.get("/healthcheck")
async def health_check():
    logger.info("Health check")
    return {"response": "Ok"}


app.include_router(auth_router)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
