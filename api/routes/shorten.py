from models import ShortenUrlResponse, ShortenUrlRequest, URL
from db import get_session
from sqlmodel import Session, select
from fastapi import Depends, Request, APIRouter
from api.utils import generate_slug

router = APIRouter()


@router.post("/shorten", response_model=ShortenUrlResponse)
def shorten(
    shorten_url_request: ShortenUrlRequest,
    request: Request,
    session: Session = Depends(get_session),
):
    """
    Shortens a long URL and returns a short URL and slug.
    If the long URL already exists in the database, returns the existing shortened URL.
    Otherwise, generates a new unique slug and stores the new shortened URL.

    Args:
        shorten_url_request (ShortenUrlRequest): Request object containing the long URL to shorten.
        request (Request): Represents the HTTP request.
        session (Session): Database session dependency to access the database.

    Returns:
        ShortenUrlResponse: Response object containing the short URL and slug.
    """
    # checks if the long URL already exists in the database. If it does, return the short URL generated using the existing slug
    existing_url = session.exec(
        select(URL).where(URL.long_url == shorten_url_request.long_url)
    ).first()
    if existing_url:
        short_url = f"h{request.base_url}{existing_url.slug}"
        return ShortenUrlResponse(short_url=short_url, slug=existing_url.slug)

    # if the long URL does not exist, generate a new slug and check if it is already in use
    slug = generate_slug()
    while session.exec(select(URL).where(URL.slug == slug)).first():
        slug = generate_slug()

    # create a new URL object using the generated slug and add it to the database
    short_url = f"h{request.base_url}{slug}"
    url = URL(long_url=shorten_url_request.long_url, slug=slug)

    session.add(url)
    session.commit()
    session.refresh(url)

    return ShortenUrlResponse(short_url=short_url, slug=slug)
