from sqlmodel import Session
from models import URL, Visits
from tests.utils import clear_test_db, client, test_engine
import pytest


@pytest.mark.parametrize("number_of_links", [None, 1])
def test_url_analytics(number_of_links):
    clear_test_db()
    # create two URLs in the database and visit the second one
    with Session(test_engine) as session:
        long_url_1 = "https://example.com"
        slug_1 = "test-slug"
        url_1 = URL(long_url=long_url_1, slug=slug_1)

        long_url_2 = "https://example.com/blee/blah"
        slug_2 = "test-slug-2"
        url_2 = URL(long_url=long_url_2, slug=slug_2)

        session.add_all([url_1, url_2])
        session.commit()

        visit = Visits(url_id=url_2.id)
        session.add(visit)
        session.commit()
        session.refresh(visit)

    request_url = (
        f"/stats?number_of_links={number_of_links}" if number_of_links else "/stats"
    )
    response = client.get(request_url)
    assert response.status_code == 200

    if number_of_links:
        assert response.json() == [
            {
                "slug": slug_2,
                "long_url": long_url_2,
                "visits": 1,
                "last_visit": visit.visit_time.isoformat(),
            }
        ]
    else:
        assert response.json() == [
            {
                "slug": slug_2,
                "long_url": long_url_2,
                "visits": 1,
                "last_visit": visit.visit_time.isoformat(),
            },
            {"slug": slug_1, "long_url": long_url_1, "visits": 0, "last_visit": None},
        ]


@pytest.mark.parametrize("get_analytics_for_first_url", [True, False])
def test_get_url_stats(get_analytics_for_first_url):
    clear_test_db()
    # create two URLs in the database and visit the second one
    with Session(test_engine) as session:
        long_url_1 = "https://example.com"
        slug_1 = "test-slug"
        url_1 = URL(long_url=long_url_1, slug=slug_1)

        long_url_2 = "https://example.com/blee/blah"
        slug_2 = "test-slug-2"
        url_2 = URL(long_url=long_url_2, slug=slug_2)

        session.add_all([url_1, url_2])
        session.commit()

        visit = Visits(url_id=url_2.id)
        session.add(visit)
        session.commit()
        session.refresh(visit)

    request_url = (
        f"/stats/{slug_1}" if get_analytics_for_first_url else f"/stats/{slug_2}"
    )
    response = client.get(request_url)
    assert response.status_code == 200

    if get_analytics_for_first_url:
        assert response.json() == {
            "slug": slug_1,
            "long_url": long_url_1,
            "visits": 0,
            "last_visit": None,
        }
    else:
        assert response.json() == {
            "slug": slug_2,
            "long_url": long_url_2,
            "visits": 1,
            "last_visit": visit.visit_time.isoformat(),
        }
