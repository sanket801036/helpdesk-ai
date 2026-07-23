"""Smoke test — root endpoint responds. (DB/Redis tests Phase 14 me expand.)"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root() -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert "app" in body["data"]
