from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from main import app
from db import get_session
from models import URL

test_engine = create_engine(
    "postgresql://hetalmangukia:postgres@localhost:5432/postgres_test",
    echo=True
)

SQLModel.metadata.create_all(test_engine)

client = TestClient(app)

def test_create_short_url():
    long_url = "https://example.com"
    response = client.post("/shorten", json={"long_url": long_url})
    data = response.json()

    assert response.status_code == 200
    assert "short_url" in data
    assert "slug" in data
    assert data["short_url"].endswith(data["slug"])


def test_same_url_returns_same_slug():
    long_url = "https://example.com"

    # First request
    res1 = client.post("/shorten", json={"long_url": long_url})
    slug1 = res1.json()["slug"]

    # Second request with same long_url
    res2 = client.post("/shorten", json={"long_url": long_url})
    slug2 = res2.json()["slug"]

    assert slug1 == slug2
