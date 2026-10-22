"""The application of this instance starts and answers below its path."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):
    from ifdd.ts.core.config import reset_settings

    from app.settings import Settings

    reset_settings()
    from ifdd.ts.core import create_app

    with TestClient(create_app(Settings())) as test_client:
        yield test_client
    reset_settings()


def path(client) -> str:
    from ifdd.ts.core import get_settings

    return get_settings().IFDD_TS_API_PATH


def test_version_and_documentation(client):
    prefix = path(client)
    assert client.get(f"{prefix}/version").status_code == 200
    assert client.get(f"{prefix}/docs").status_code == 200
    assert client.get(f"{prefix}/redoc").status_code == 200
    document = client.get(f"{prefix}/openapi.json").json()
    assert document["servers"] == [{"url": prefix}]
    assert "/stores/{store}/samples/batch" in document["paths"]


def test_data_needs_a_token(client):
    prefix = path(client)
    assert client.get(f"{prefix}/whoami").status_code == 401
    response = client.post(f"{prefix}/stores/temperature.ops.example.ifdd.de/samples", json={})
    assert response.status_code == 401


def test_the_entry_point_imports():
    import app.main

    assert app.main.app is not None
