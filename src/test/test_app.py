import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.anyio
async def test_healthcheck():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"response": "Ok"}
