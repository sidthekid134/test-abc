import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_ping_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"ping": "pong"}