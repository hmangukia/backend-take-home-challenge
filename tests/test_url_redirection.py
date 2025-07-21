from sqlmodel import Session
from models import URL
from tests.utils import clear_test_db, client, test_engine
from unittest.mock import patch, AsyncMock
from api.routes.redirect import log_visit


@patch("api.routes.redirect.redis_client.get", new_callable=AsyncMock)
@patch("fastapi.BackgroundTasks.add_task")
def test_redirect_to_long_url_when_slug_exists(mock_add_task, mock_redis_get):
    clear_test_db()
    mock_redis_get.return_value = None
    # create a new URL object in the database
    with Session(test_engine) as session:
        long_url = "https://example.com"
        slug = "test-slug"
        url = URL(long_url=long_url, slug=slug)
        session.add(url)
        session.commit()
        session.refresh(url)

    response = client.get(f"/{slug}", follow_redirects=False)
    assert response.status_code == 307

    mock_add_task.assert_called_once_with(log_visit, url.id)


@patch("api.routes.redirect.redis_client.get", new_callable=AsyncMock)
def test_raise_404_when_slug_does_not_exist(mock_redis_get):
    clear_test_db()
    mock_redis_get.return_value = None
    slug = "test-slug"
    response = client.get(f"/{slug}", follow_redirects=False)
    assert response.status_code == 404
