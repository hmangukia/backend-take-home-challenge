from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select
from main import app
from db import get_session
from models import URL, Visits
from tests.utils import clear_test_db, client, test_engine

def test_redirect_to_long_url_when_slug_exists():
    clear_test_db()
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
    
    # check if the visit is logged in the database
    with Session(test_engine) as session:
        visits_for_url = session.exec(select(Visits).where(Visits.url_id == url.id)).all()
        assert len(visits_for_url) == 1
        visit_for_url = visits_for_url[0]
        assert visit_for_url is not None
        assert visit_for_url.visit_time is not None


def test_raise_404_when_slug_does_not_exist():
    clear_test_db()
    slug = "test-slug"
    response = client.get(f"/{slug}", follow_redirects=False)
    assert response.status_code == 404