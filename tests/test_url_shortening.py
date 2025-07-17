from tests.utils import clear_test_db, client


def test_create_short_url():
    clear_test_db()
    long_url = "https://example.com"
    response = client.post("/shorten", json={"long_url": long_url})
    data = response.json()

    assert response.status_code == 200
    assert "short_url" in data
    assert "slug" in data
    assert data["short_url"].endswith(data["slug"])


def test_same_url_returns_same_slug():
    clear_test_db()
    long_url = "https://example.com"

    # First request
    res1 = client.post("/shorten", json={"long_url": long_url})
    slug1 = res1.json()["slug"]

    # Second request with same long_url
    res2 = client.post("/shorten", json={"long_url": long_url})
    slug2 = res2.json()["slug"]

    assert slug1 == slug2
