from models import URLStatsResponse, URL, Visits
from db import get_session
from sqlmodel import Session, select
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import func

router = APIRouter()


@router.get("/stats", response_model=list[URLStatsResponse])
def get_top_urls(number_of_urls: int = 10, session: Session = Depends(get_session)):
    """
    Retrieves statistics for the top URLs based on the number of visits.

    Args:
        number_of_urls (int): The number of top URLs to retrieve, default is 10.
        session (Session): Database session dependency to access the database.

    Returns:
        list[URLStatsResponse]: A list of URL statistics sorted by the number of visits in descending order.
    """
    query = (
        select(
            URL.id,
            URL.slug,
            URL.long_url,
            func.max(Visits.visit_time).label("last_visit"),
            func.count(Visits.id).label("visit_count"),
        )
        .join(Visits, Visits.url_id == URL.id, isouter=True)
        .group_by(URL.id, URL.slug, URL.long_url, URL.created_at)
        .order_by(func.count(Visits.id).desc())
        .limit(number_of_urls)
    )
    urls = session.exec(query).all()

    return [
        URLStatsResponse(
            slug=url.slug,
            long_url=url.long_url,
            visits=url.visit_count,
            last_visit=url.last_visit,
        )
        for url in urls
    ]


@router.get("/stats/{slug}", response_model=URLStatsResponse)
def get_url_stats_by_slug(slug: str, session: Session = Depends(get_session)):
    """
    Retrieve statistics for a specific URL identified by its slug.

    Args:
        slug (str): The slug of the URL to retrieve statistics for.
        session (Session): Database session dependency to access the database.

    Raises:
        HTTPException: Raises 404 if the URL with the specified slug does not exist.

    Returns:
        URLStatsResponse: Statistics including slug, original URL, total visits,
        and time of the last visit.
    """
    query = (
        select(
            URL.id,
            URL.slug,
            URL.long_url,
            func.max(Visits.visit_time).label("last_visit"),
            func.count(Visits.id).label("visit_count"),
        )
        .where(URL.slug == slug)
        .join(Visits, Visits.url_id == URL.id, isouter=True)
        .group_by(URL.id, URL.slug, URL.long_url, URL.created_at)
    )
    url = session.exec(query).first()

    if not url:
        raise HTTPException(
            status_code=404, detail=f"URL with the slug '{slug}' not found"
        )

    return URLStatsResponse(
        slug=url.slug,
        long_url=url.long_url,
        visits=url.visit_count,
        last_visit=url.last_visit,
    )
