from models import URLStatsResponse, URL, Visits
from db import get_session
from sqlmodel import Session, select
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import func

router = APIRouter()


@router.get("/stats", response_model=list[URLStatsResponse])
def get_top_links(number_of_links: int = 10, session: Session = Depends(get_session)):
    urls = session.exec(
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
        .limit(number_of_links)
    ).all()

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
def get_url_stats(slug: str, session: Session = Depends(get_session)):
    url = session.exec(
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
    ).first()

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
